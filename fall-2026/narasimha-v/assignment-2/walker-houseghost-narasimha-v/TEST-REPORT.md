# TEST REPORT — HOUSEGHOST, Night 1 slice

**Engine:** Godot 4.7.2.stable.official.ed1daf0bf · **Platform:** macOS 26.x, Apple Silicon
**Source revision:** see the final commit on branch `narasimhaReddyValam`
**Project path:** `fall-2026/narasimha-v/assignment-2/walker-houseghost-narasimha-v/godot`

---

## 1. Startup and controls

Run from a clean checkout with:

```bash
godot --path godot
```

**Run it from a terminal rather than from the editor.** Godot keeps an open scene in memory, so an editor left running while the files change will play an older build. A terminal launch is also how a grader will run it.

**A correction worth recording.** A repeated report of "the character will not move" was twice attributed to that stale editor, and that diagnosis was wrong. The real cause was a race between two tween `finished` signals in the opening sequence: awaiting one that has already fired waits forever, and which of the two fired first depended on frame timing. The same build therefore handed over control on one machine and froze on another. It was found by putting the four relevant values on screen and asking for a single screenshot, after four rounds of reasoning had not found it.

| Check | Result |
|---|---|
| Project opens on Godot 4.7.2 with no missing resources | Pass — headless boot reports no errors |
| Main scene loads and runs | Pass |
| Opening sequence plays and hands over control | Pass — each line waits for a key press, so the opening is read at the player's pace and cannot overrun |
| Read the story again (I) during play | Pass — holds the player still while open, returns control when closed |
| Move left and right | Pass |
| Jump | Pass |
| Flip the world | Pass |
| Contact a relic, tap and hold | Pass |
| Mute music (M) and effects (N) independently | Pass |
| Restart (R) | Pass |

## 2. The automated check

```bash
godot --headless --path godot --script tests/test_sound_triggers.gd
```

Twelve assertions, zero failures at the time of writing. It covers one sound per event under rapid repeats and held input, and the walking-versus-drifting contrast in both directions.

```
PASS  one flip produces exactly one flip sound
PASS  12 flip calls during a turn still produce one sound
PASS  two resolves inside the cooldown produce one contact sound
PASS  one frost sound per day torn
PASS  muted SFX still counts the event (state is unchanged by audio)
PASS  a held jump fires one jump sound
PASS  landing from that jump fires one land sound
PASS  walking in the memory produces footsteps
PASS  the ghost makes no real footsteps
PASS  but he keeps a rhythm of his own
PASS  the ghost displaces air while he moves
PASS  and the air stops when he stops
--- 12 checks, 0 failed ---
```

**What this check cannot do, stated plainly.** It verifies that an event fires exactly once and that muting changes no game state. It cannot hear, see, or understand. Every audio fault and every comprehension fault in this project was found by a person playing, while these assertions passed throughout.

It also cannot catch a timing race. Three runs of this check passed while a player could not move at all, because it drives input directly and never exercises the real frame timing of the opening sequence. Passing tests and a person who cannot play are not a contradiction; they are measuring different things. That is the single most useful thing this project taught about verification.

## 3. My own playtest

Played on 2026-10-07 from a terminal launch, with sound on and then with both music and effects muted.

| Check | Result |
|---|---|
| Plays through with sound on | Pass — movement, the flip, all three relics, the day cost, and the ending all behaved as designed |
| Plays through fully muted (M and N) | **Pass** — everything the slice communicates was still understandable with no audio at all |
| Music loop seam | **Not checked.** I did not listen specifically for the wrap, and the Ogg conversion postdates this session. Recorded as outstanding rather than passed |
| Revised effects balance | **Not judged by ear** since the levels changed |

The muted result is the one that matters most here, because readability without sound is a scored criterion and the only honest way to establish it is to take the sound away and still be able to play. Two rows above are deliberately left failing-to-report rather than marked pass; an unlistened check is not a passed one.

## 4. Another person played it

A friend played the build without being told anything about the story or the controls. Her feedback, as reported to me:

> It's confusing. I didn't know what to do, or when to turn upside down, or why I was doing that.

This is recorded as given and was not solicited with leading questions. It is the most useful result in this report, because it isolates a failure I could not see: I already knew the story, so I could not tell that the game never conveyed it.

**What it exposed.** The slice had an opening that establishes *who the player is* — a boy who was erased, a family living in his house, a wish to be noticed — but nothing that teaches *what to do*. The central verb, turning the world over, was never taught at all. It appeared in a hint line at the bottom of the screen that listed every control at all times, which a player reads once and then stops seeing.

**What changed in response.**

- The permanent hint line is gone. In its place, a prompt appears beside the thing it refers to, only when it can be acted on, and stops appearing once it has been used.
- Arrow keys are shown until the player first moves.
- Standing below a relic that cannot be reached from the floor shows **F**, next to the relic itself.
- Once inverted and within reach, that becomes **E**.
- Once a relic has been taken, its prompt and its light both go out, so what remains lit is always what is left to do.

Verified in engine: before moving the cue reads the arrow keys; standing under the music box in the normal world it reads F; after flipping, in reach, it reads E; after the contact lands it fades out.

**Not yet retested with her.** The changes above are a response to her session, not a result she has confirmed. A second session with the same player, or a fresh one, is the honest next step and has not happened.

## 5. Character against the sheet

| Sheet element | In engine |
|---|---|
| Two states, one static image each | Pass — the boy in the memory, the ghost in the truth |
| Orientation follows input, left flipped at runtime | Pass |
| Collision aligns with the art | Pass — capsule 52 × 250 px centred on the body, after a correction recorded in the character sheet |
| Silhouette reads at on-screen size | Pass — 33 × 96 px, recorded in `design/character/silhouette-test-card.png` |
| One body size across every pose | Pass after three failed measures; body area is what worked, and the idle is the walk cycle's own legs-together frame so standing and walking cannot disagree |

## 6. Storyboard against the slice

| Panel | In the slice |
|---|---|
| 1 — first sight of the room | Covered, and strengthened: the slice opens on the *stripped* room with the child and the ghost, before the memory blooms in |
| 2 — the flip | Covered |
| 3 — the music box | Covered |
| 4 — she looks up | Covered, and literal: her posture is the recognition meter |
| 5 — the hallway corrects itself | **Not covered.** Out of scope for the slice; semester work |
| 6 — the father at the cellar door | **Not covered.** Out of scope for the slice; semester work |

## 7. Sound

| Check | Result |
|---|---|
| Four events minimum, each firing once per occurrence | Pass — nine events, twelve assertions |
| Rapid repeats and held input do not double-fire | Pass |
| Music loops without an audible click | Verified in engine: both tracks load as `AudioStreamOggVorbis`, 59.5 s and 61.9 s, and loop is set in code because the importer defaults it to false. **Human listening confirmation outstanding**, and now also needs a check that Ogg encoding did not introduce a seam artefact the WAV master did not have |
| Music behaviour on flip, failure, success and end | Pass — crossfade on the flip, long clean fade on either ending |
| Mute works for music and effects separately | Pass |
| Slice readable with all sound muted | **Pass, confirmed by a muted human playthrough** on 2026-10-07: played with both M and N muted, and everything the slice communicates was still legible. The visual carriers are the nights counter, the relic lights going out as each is answered, the contextual key cues, and the child's posture turning further toward the room |

## 8. Revision driven by observation

Several, all recorded in FRICTIONAL.md and CHANGE-BRIEF.md. The two most consequential:

**Sounds that fired and could not be heard.** Measurement showed `contact` audible for 19 % of its length, `correct` 15 %, `frost` 29 % — brief ticks surrounded by silence, lost under a score at full level. All were compressed to be dense rather than spiky (contact now 84 %, correct 77 %, flip 96 %) and the music now ducks 15 dB beneath each one. The automated check had passed the whole time.

**A level where nothing the player did mattered.** The floating platforms could be ignored entirely by walking on flat ground. They were removed and replaced with gaps in the floor that cost a night to fall through, and with obstacles that exist in only one world.

## 9. Honest limitations

- The three room tiles repeat; the middle one is mirrored to break the repetition, which puts two doors adjacent at the seam.
- The floor gaps exist in both worlds although the fiction says only the real house has been pulled apart.
- Three character-sheet poses are specified but not generated.
- The floorboard relic, the floor holes, the glow and the heartbeat are drawn or synthesised in code and satisfy no generative requirement; the asset log marks each as such.
- Storyboard panels 5 and 6 are not covered.
- The music loop seam has **not** been confirmed by human listening, and the Ogg re-encode happened after the last human session, so nothing yet rules out an artefact the WAV master did not have. The engine check confirms both tracks load and loop; it cannot hear the seam.
- The revised effects mix (everything 3 dB down, footsteps 9–11 dB down) has **not** been judged by ear since the change.
