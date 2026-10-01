# HOUSEGHOST — Change brief (Assignment 2 slice)

## Asset list

| ID | Asset | Serves panel |
|---|---|---|
| CHAR-GHOST-REF | Turnaround reference (generates all poses) | all |
| CHAR-GHOST-IDLE | Idle drift, ghost state | 1, 4 |
| CHAR-GHOST-DRIFT | Drift-move, ghost state | 1 |
| CHAR-GHOST-WALK | Walk contact + passing, remembered state | 3, 5 |
| CHAR-GHOST-FLIP | Flip transition pose | 2 |
| CHAR-GHOST-REACH | Kind-contact reach, remembered state | 3 |
| CHAR-GHOST-SCARE | Scare pose, ghost state | (alt of 3) |
| CHAR-GHOST-HURT | Dispersed pose | 5 |
| CHAR-CHILD-PLAY | The child playing on the floor (yellow raincoat) | 1 |
| CHAR-CHILD-LOOKUP | The child looking up, mid-gasp | 4 |
| CHAR-FATHER-BACK | Father, back view only | 6 |
| CHAR-HOLLOW-GLIMPSE | Hollow, distant, off-center | 5 |
| ENV-ROOM-EMPTY | Living room, upright/bare | 1, 4 |
| ENV-ROOM-MEMORY | Same room, inverted/lamplit | 2, 3 |
| ENV-HALL-MEMORY | Hallway, memory state | 5 |
| ENV-HALL-CORRECTED | Same hallway, corrected (extra door) | 5 |
| ENV-CELLAR-DOOR | Cellar door + salt line | 6 |
| PROP-MUSICBOX | Music box, both states | 3, 4 |
| PROP-CALENDAR | Wall calendar with tear-off pages | 1, 4, 6 |
| SFX-FLIP | World flip (held breath + reversed swell) | 2 |
| SFX-CONTACT | Kind contact (music-box chime with paper tear inside) | 4 |
| SFX-CORRECT | Room correction (wood groan + de-tuned note) | 5 |
| SFX-FROST | Frost creep (crystalline crackle) | 5, 6 |
| MUS-LULLABY | Music-box lullaby loop (inverted world only) | 2, 3, 5 |

## Event-to-sound map

| Sound | Exact trigger | Double-trigger prevention |
|---|---|---|
| SFX-FLIP | `world_flipped` signal, emitted once per state change in the gravity controller | Signal fires on the state EDGE only; input is ignored while the flip tween runs (~0.8 s), so mashing the key cannot re-trigger |
| SFX-CONTACT | `contact_landed` signal from the interactable, after the arm-up delay completes | The interactable sets `used = true` for a cooldown; a held interact key arms once — trigger on `just_pressed`, never on `pressed` |
| SFX-CORRECT | `room_corrected` signal when the player crosses the hallway's trigger area | The trigger Area2D disconnects itself after first fire; corrections are one-time per room |
| SFX-FROST | `calendar_day_torn` signal (fires inside contact resolution) | Same edge as the calendar decrement — one tear, one sound, by construction |

Rule (from the assignment): sound never decides state. Every trigger above is a signal emitted by game logic that already changed state; muting everything changes nothing mechanical.

## Music behavior

- **Plays:** MUS-LULLABY loops only while inverted; hard-cut on flip (no crossfade — the cut IS the threshold).
- **Pause:** all audio ducks to silence except the clock tick; lullaby resumes at its loop position on unpause.
- **Failure (Hollow touch / scare backfire):** lullaby stops mid-phrase; silence until the player flips upright; next inversion restarts it de-tuned one step further.
- **Success (contact lands):** lullaby continues; SFX-CONTACT plays over it.
- **End of slice:** lullaby finishes its current phrase once, cleanly, then stops. The only clean musical resolution in the slice.
- **Mute:** M toggles music, N toggles SFX, independently.

## Predicted failure cases and the checks for them

1. **Generated pose frames drift in proportion from the turnaround** (image models resist consistency). Check: overlay each accepted frame on the turnaround at 50% opacity; reject any frame whose head height or sweater hem drifts more than ~5%. Logged per frame in the asset log.
2. **The ghost disappears against the memory-world's dark amber rooms** (a translucent character on near-black). Check: screenshot each room at game resolution, desaturate, and confirm the character reads in grayscale; if not, adjust rim-light in the art, not the room.
3. **The lullaby loop clicks at the seam.** Check: cut at a bar boundary in Audacity, listen to three consecutive repetitions with eyes closed; also verify Godot's OGG loop flag is set so the engine loops, not a script timer.
4. **SFX-FLIP double-fires on rapid key mashing.** Check: automated — scripted input toggles invert 20 times in 5 seconds; a signal counter asserts flips == sounds played. This is the slice's automated check.
5. **The slice is unreadable muted.** Check: full playthrough with master bus muted; the calendar page tear and frost creep must carry the cost information visually. If a tester can't say "I lost a day" with sound off, the calendar gets a stronger animation.
