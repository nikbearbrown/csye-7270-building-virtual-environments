# walker-3d-kinematic-character: capture notes

**What this is.** A real windowed Godot 4.7.2 Movie Maker run of the 3D kinematic-character demo, recorded 2026-10-09 at a fixed 30 fps from a scratch copy. It uses the Forward+ renderer on Metal and Jolt physics, and the player is "Cubio", a cube, in a GridMap level. The source at `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-3d-kinematic-character/godot` was not touched. The copy got only the capture autoload and a 1920x1080 window.

## Scripted input
A "waypoints" controller in the driver uses the same steering as the project's own `tests/test_route.gd`. Each frame it projects the vector to the next waypoint into the follow camera's frame. It then **presses** move_left/right/forward/back (InputEventAction), and jump when the target is above and close.

The waypoints are the first three of the project's own route: (0.5, 1.45, 0.5), then (0.5, 2.45, -1.5), then (-0.5, 3.45, -1.5). All three were reached, at f95, f134 and f160 (WAYPOINT lines in `raw-log.txt`). After that, all keys were released.

## Files (all 1920x1080)
| File | What is on screen |
|---|---|
| `01-start.png` | Cubio (a white-grey wooden cube) on the purple tiled floor, under the follow camera. |
| `02-walking-to-the-steps.png` | Cubio walking toward the step blocks. |
| `03-jumping-up-a-step.png` | Cubio landing on the first raised step. |
| `04-jumping-to-the-top-step.png` | Cubio in the air, jumping to the upper level. |
| `05-on-the-upper-level.png` | Cubio standing on the upper level. |
| `walker-3d-kinematic-character-clip.mp4` | **6.0 s**, H.264, 30 fps, no audio. Movie frames 40–220: walk, two step jumps, arrival on the upper level. The last ~2 s are Cubio standing still. |

**Problems:**
- A longer take, following the project's 10-point perimeter route, failed at waypoint 4: Cubio fell off the upper level and got stuck. Steering only 30 times a second is coarser than the project's test, which steers on every 120 Hz physics tick. That take was discarded, and only the verified 3-waypoint climb is delivered.
- Recording ran at about 11% of real time (Forward+, 120 Hz physics); fixed-fps output is unaffected.
- The project has no sound.
