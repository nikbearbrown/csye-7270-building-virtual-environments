# walker-3d-platformer: capture notes

**What this is.** A real windowed Godot 4.7.2 Movie Maker run of the 3D platformer, recorded 2026-10-09 at a fixed 30 fps from a scratch copy. It uses the Forward+ renderer on Metal, Jolt physics, and the robot player model. The source at `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-3d-platformer/godot` was not touched. The copy got only the capture autoload and a 1920x1080 window.

**Global RNG seeded to 7375**, the same seed as the project's `tests/feature_route.gd`.

## Scripted input
A "seek" controller in the driver uses the same logic as the project's own `tests/feature_route.gd`, run from f45. Each frame it finds the nearest untaken coin at or below y = 0 and turns that direction, relative to the follow camera, into **pressed move_* actions** with analog strength. It holds jump for about 1 s whenever the player is on the floor and at least 1.5 s has passed since the last jump, and taps shoot every 15 frames. It never writes a position, a velocity or a score. There are 162 press/release events in `raw-log.txt`.

Outcome, from the log's STATE lines: coins went 0 to 2 between f120 and f150. A red enemy was shot and burst (visible around f125–135).

## Files (all 1920x1080)
| File | What is on screen |
|---|---|
| `01-start.png` | The player robot at spawn, seen from behind, on the grass, in front of a striped earth wall. |
| `02-running-and-shooting.png` | The robot running with a shot's dotted trail; coin counter 0; a red enemy beside it. |
| `03-enemy-hit-first-coin.png` | The red enemy beside the robot as it is hit; counter 1; coin sparkles. |
| `04-coin-burst.png` | Counter 2, a coin-collect burst at the robot's feet, and an enemy beside it. |
| `05-two-coins.png` | The robot jumping, with a shot trail; counter 2. |
| `06-lower-level-coin-ahead.png` | The robot on a lower level, with a coin on the ground ahead; counter 2. |
| `walker-3d-platformer-clip.mp4` | **5.5 s**, H.264, 30 fps, **AAC game audio** (jump/shoot/coin sounds). Movie frames 25–190: run, shots, enemy hit, two coins. |

**Problems:**
- The clip is cut at 5.5 s on purpose. From about f195 onward, the automatic follow camera is repeatedly blocked by level geometry, so the frame fills with a wall. The project's own CAPTURE.md reports the same camera obstruction.
- The game's audio peaks at 0.0 dBFS, the full-scale clipping the project's CAPTURE.md already notes. It was left as recorded.
