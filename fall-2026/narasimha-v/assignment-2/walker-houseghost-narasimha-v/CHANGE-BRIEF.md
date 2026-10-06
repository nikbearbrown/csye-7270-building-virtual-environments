# HOUSEGHOST — Change brief (Assignment 2 slice)

## Asset list

**Status 2026-10-06.** Built means the asset exists and is in the running slice.

| ID | Asset | Panel | Status |
|---|---|---|---|
| CHAR-REF / CHAR-SHEET | Turnaround and eight-view model sheet, both states | all | Built — `design/character/model-sheet-8-views.png` |
| CHAR-GHOST | Idle drift, ghost state | 1, 4 | Built — `assets/art/char_ghost.png` |
| CHAR-REMEMBERED | Idle, remembered state | 2, 3 | Built — `assets/art/char_remembered.png` |
| CHAR-WALK-01..04 | Walk cycle, remembered state | 3 | Built — `assets/art/char_walk_1..4.png` |
| ENV-ROOM-EMPTY | The bedroom, stripped (upright world) | 1, 4 | Built — `assets/art/env_room_empty.png` |
| ENV-ROOM-MEMORY | The same bedroom, remembered (inverted world) | 2, 3 | Built — `assets/art/env_room_memory.png` |
| UI-GLOW | Marker for an available contact | 3 | Built — code-drawn, not a generated asset |
| SFX-FLIP | World flip (held breath, reversed swell) | 2 | Wired, file pending |
| SFX-CONTACT | Contact (music-box chime with a paper tear inside) | 4 | Wired, file pending |
| SFX-FROST | A day tearing off (crystalline crackle) | 4 | Wired, file pending |
| SFX-CORRECT | The house reacting to a loud contact (wood groan, de-tuned note) | 4 | Wired, file pending |
| MUS-LULLABY | Music-box lullaby loop, inverted world only | 2, 3 | Wired, file pending |
| CHAR-GHOST-REACH, CHAR-GHOST-SCARE, CHAR-GHOST-HURT | Contact, scare and dispersed poses | 3, 5 | Specified, not generated — the slice shows these states by image swap and engine motion |
| CHAR-CHILD-PLAY, CHAR-CHILD-LOOKUP | The child, playing and looking up | 1, 4 | Specified, not in the slice |
| CHAR-FATHER-BACK, CHAR-HOLLOW-GLIMPSE | The father at the cellar door, the Hollow glimpsed | 5, 6 | Specified, semester work |
| ENV-HALL-MEMORY, ENV-HALL-CORRECTED, ENV-CELLAR-DOOR | Hallway and cellar door | 5, 6 | Specified, semester work — panels 5 and 6 are outside this slice |
| PROP-MUSICBOX, PROP-CALENDAR | Music box and wall calendar as drawn props | 3, 4, 6 | Not separately generated; the music box is marked by UI-GLOW and the calendar is the HUD counter |

## Event-to-sound map

**Revision 2026-10-06 — as built.** The original plan is kept below the table; the differences are named, because the slice was built before the audio existed and the wiring is what the sounds will attach to.

| Sound | File | Exact trigger in the built slice | Double-trigger prevention |
|---|---|---|---|
| SFX-FLIP | `assets/sfx/sfx_flip.ogg` | `world.gd` `flip()` — played immediately after `is_inverted` is changed and `world_flipped` is emitted | A `_flipping` guard rejects any further call until the 0.6 s tween finishes, so a held or mashed key cannot flip or sound twice. Verified: twelve calls during one turn produce one sound |
| SFX-CONTACT | `assets/sfx/sfx_contact.ogg` | `contact_point.gd` `_resolve()` via the `contact_landed` signal, on key release, after the tap-or-hold has been decided | The contact arms on `just_pressed` and resolves on release, never on `pressed`; a 1.2 s cooldown is enforced inside `_resolve` itself, so a second resolve is refused regardless of who calls it. Verified: two resolves inside the cooldown produce one sound |
| SFX-FROST | `assets/sfx/sfx_frost.ogg` | `meters.gd` emits `day_torn` once per day removed; `world.gd` plays one sound per emission | One tear, one sound, by construction — the loop that decrements the calendar is the same loop that emits. Verified: a two-day cost produces exactly two sounds |
| SFX-CORRECT | `assets/sfx/sfx_correct.ogg` | A **scary** contact only: the loud way to be seen also wakes the house | Rides the same single `contact_landed` emission as SFX-CONTACT, so it inherits that cooldown |

**Changed from the plan:** SFX-CORRECT was planned for a hallway trigger in a room that the slice does not include, so it now fires on the scary contact, which is the slice's equivalent beat — the loud choice disturbing the house. SFX-FLIP's guard is 0.6 s rather than the estimated 0.8 s, matching the tween actually used.

**Rule, enforced in code:** sound never decides state. Every trigger above is played *after* the game has already changed state and emitted a signal. An automated assertion covers this directly: with sound effects muted, a flip still counts as having happened, because the audio layer only observes. The slice also runs with all five audio files absent — it prints a notice and plays silently.

## Music behavior

- **Plays:** MUS-LULLABY loops only while inverted; hard-cut on flip (no crossfade — the cut IS the threshold).
- **Pause:** all audio ducks to silence except the clock tick; lullaby resumes at its loop position on unpause.
- **Failure (Hollow touch / scare backfire):** lullaby stops mid-phrase; silence until the player flips upright; next inversion restarts it de-tuned one step further.
- **Success (contact lands):** lullaby continues; SFX-CONTACT plays over it.
- **End of slice:** lullaby finishes its current phrase once, cleanly, then stops. The only clean musical resolution in the slice.
- **Mute:** M toggles music, N toggles SFX, independently.

## Predicted failure cases, the checks, and what actually happened

1. **Generated poses drift in proportion from the reference.** Check: compare each accepted image against the model sheet; reject anything whose head height or proportions drift. **Outcome: this happened repeatedly and was the main cause of rejection.** Five character references were rejected before one was accepted (asset log CHAR-REF-01 to 05). The accepted walk cycle held proportions well enough to use, and was additionally normalised to a common height and canvas so the figure does not jitter between frames.
2. **The character disappears against a room.** Check: screenshot at game resolution and confirm the character reads; if not, adjust the art, not the room. **Outcome: partly failed and not yet fixed.** Green was reserved for the character and excluded from both rooms, which works in the remembered world. In the upright world the ghost is pale on grey and reads faint — visible in `evidence/01-upright-ghost.png`. The planned fix is a rim light on the ghost sprite; it is an open limitation, recorded in the README.
3. **The music loop clicks at the seam.** Check: cut at a bar boundary, listen to at least three repetitions, and set Godot's OGG loop flag so the engine loops rather than a script timer. **Outcome: not yet testable — the music has not been generated.**
4. **A sound fires twice on one event.** Check: an automated script asserts one sound per event under mashing and held input. **Outcome: a real defect was caught.** The contact cooldown guarded only the input path, so the resolve function could still fire twice when called directly; the guard now lives inside the function. The check also caught a flaw in itself — it measured waits in frames, and headless frames are not real time. Five assertions now pass.
5. **The slice is unreadable muted.** Check: play it with all audio off and confirm the cost is still legible. **Outcome: designed for and visible in the captures, but the human playtest is still outstanding.** The calendar counter jolts when a day is torn, recognition pips fill, and a frost vignette deepens as the anniversary nears — none of which depend on sound. The slice currently runs silent by necessity, which has made this easy to observe but does not substitute for a real playtest with the audio present and then muted.

### Found while building, not predicted

6. **The core verb was unreachable.** The music box sat at the room's vertical centre while the player walks four hundred pixels below it, so a contact could never be made by playing. Found by a probe that walks the player with the real input action; fixed by moving the music box onto the floor and out of the rotating room.
7. **The collision shape did not match the art.** The capsule was specified as 40 × 80 px before any art existed and covers only the shins of the 320 px sprite that was made. Found while drawing the required collision overlay; corrected to 52 × 250 px, with the character sheet recording the correction.
