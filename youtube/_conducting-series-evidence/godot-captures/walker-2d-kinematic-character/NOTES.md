# walker-2d-kinematic-character: capture notes

**What this is.** A real windowed Godot 4.7.2 Movie Maker run of the 2D kinematic-character demo (CharacterBody2D, moving platforms, a spinning circle, one-way platforms), recorded 2026-10-09 at a fixed 30 fps from a scratch copy. The source at `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-2d-kinematic-character/godot` was not touched. The copy got only the capture autoload and a 1920x1080 window.

## Scripted input (InputEventAction, frames at 30 fps)
- move_right held f40–120, with jump taps at f60 and f95.
- move_left held f125–260, with jump taps at f150, f185 and f230.
- move_right held f265–320, with a jump tap at f280.

The route was not tuned to reach the princess, and the run does not reach it.

## Files (all 1920x1080)
| File | What is on screen |
|---|---|
| `01-start-riding-the-spinning-circle.png` | The level at 1 s; the player (small grey square) sits on top of the rotating teal circle. |
| `02-airborne-moving-right.png` | The player in the air, right of the circle, moving right. |
| `03-on-the-right-ramp-moving-left.png` | The player on the right-hand slanted ramp, moving left. |
| `04-by-the-left-steps.png` | The player at the bottom left, by the steps. |
| `05-back-on-the-right-floor.png` | The player back on the lower right floor. |
| `walker-2d-kinematic-character-clip.mp4` | 8.0 s, H.264, 30 fps, no audio. Movie frames 30–270: the player falls off the circle, runs and jumps right, then runs and jumps left across ramps and steps, while the teal moving platforms travel. |

**Problems:**
- The player sprite is small (about 35 px at 1080p), which is the game's own scale.
- The level is 530x495 logical with "expand" aspect, so dark margins left and right are part of the frame.
- The project has no sound, so the MP4 has no audio.
