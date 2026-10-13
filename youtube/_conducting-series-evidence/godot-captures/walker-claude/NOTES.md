# walker-claude: capture notes

**What this is.** Real renders of the walker-claude Godot project (the Jumpman platformer starring Clawd, plus the separate 18-animation Clawd gallery scene). They were recorded 2026-10-09 with Godot 4.7.2 Movie Maker in a windowed run at a fixed 30 fps. Input came from a script that sent real keyboard events. None of this is a mock: every pixel was drawn by the project's own `_draw()` code.

**Source:** `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/godot` (unchanged).
**Run from:** the scratch copy `/private/tmp/claude-501/capture-work/walker-claude/godot`, made with rsync and excluding `.godot`, `evidence` and `youtube`.

## Changes made to the scratch copy only
1. I added `res://capture/capture_driver.gd` (copied here as `capture_driver.gd`) and registered it as the autoload `CaptureDriver` in the copy's `project.godot`.
2. In the copy's `project.godot`, I changed `window_width_override` / `window_height_override` from 1280x720 to 1920x1080, so Movie Maker records at 1080p. Rendering is unchanged: it is still a 640x360 canvas, `canvas_items` stretch and vector drawing, now drawn at a 3x scale.
3. The driver sets `session.test_mode = true`. In this game, that flag's only effect is that the game does not auto-pause when the window loses focus.

## How the input was scripted
The driver calls `Input.parse_input_event()` with `InputEventKey` events. The game reads them through its own InputMap actions (`confirm`, `move_right`, `jump`), the same path a real keyboard takes. Nothing sets the player's position or velocity.

Scripted input in the game run (frame numbers are at 30 fps, copied from `raw-log-game.txt`):
- f36 (1.20 s): Enter down; f38: Enter up. The title card closes and the run starts.
- f42 (1.40 s): Right arrow pressed and held for the whole run.
- Space is tapped for one frame each time Clawd is on the floor and passes x = 138, 292, 424, 548 and 712. These are the same jump marks as the project's own `tests/route_driver.gd`. Taps landed at f58, f87, f112, f135 and f168.
- f205 (6.83 s): the level reports COMPLETE (5.63 s in-game, 0 deaths) and Right is released.

Scripted input in the gallery run: Right arrow tapped at f120 (page 1 to page 2) and at f240 (page 2 to page 3). Otherwise the gallery autoplays.

## Files (all 1920x1080)
| File | What is on screen |
|---|---|
| `01-title-screen.png` | The title card "First steps. Real jumps." with the ENTER / START button over the First Steps level. The HUD reads "WALKER / JUMPMAN", the controls line, "RETRIES 00  00.0s". Clawd is idle at spawn (f25). |
| `02-clawd-running.png` | Gameplay at 0.6 s: Clawd running right on the ground in zone "01 / GET MOVING", legs mid-stride, with the progress bar starting (f53). |
| `03-clawd-jumping-the-gap.png` | Clawd airborne over the first pit under "02 / MIND THE GAP" at 2.8 s, after the spike trio (f119). |
| `04-level-complete.png` | The "Course complete." card: "5.6 seconds / 0 retries", ENTER / PLAY AGAIN. Clawd is at the FINISH flag; the game switches him to its "celebrate" animation, but this single frame does not show raised arms (f225). |
| `05-gallery-page-1.png` | CLAWD / ANIMATION LIBRARY, Gallery 1/3: idle, bounce, wave, look, walk, run. |
| `06-gallery-page-2.png` | Gallery 2/3: think, type, sleep (eyes closed), error, nod, shake. |
| `07-gallery-page-3.png` | Gallery 3/3: dance, stretch, crouch, jump, spin, celebrate. **Note:** spin happens to be caught edge-on (a thin sliver); that is a real frame of the spin animation. |
| `walker-claude-jumpman-gameplay.mp4` | **7.17 s**, H.264, 1920x1080, 30 fps, no audio. Movie frames 30–245: 0.2 s of title card, then Enter, Clawd runs right and makes 5 jumps (over the step, the spikes, both pits and the block), touches the flag, and the Course complete card appears. |
| `walker-claude-clawd-gallery.mp4` | **7.0 s**, H.264, 1920x1080, 30 fps, no audio. Movie frames 90–300: page 1 animating for 1 s, a Right-arrow tap, page 2 animating for 4 s, another tap, page 3 animating for 2 s. |
| `contact-sheet-*.png` | One frame per second from each MP4, for checking. |
| `capture.sh`, `capture_driver.gd` | The exact command and the driver used. |
| `raw-log-game.txt`, `raw-log-gallery.txt` | Raw Godot stdout: every INPUT and SHOT line, the movie summary, and a distinct-frame count. |

## Problems and how they were handled
- **The 1280x720 override.** The project's window override made Movie Maker record at 720p even with `--resolution 1920x1080`. I fixed this by changing the override in the copy (change 2 above).
- **Occluded windows record frozen frames.** One 1080p run recorded only 8 real frames (6 distinct images across 246 PNGs), because Godot stops drawing when macOS reports its window covered. The final run used `--always-on-top` and recorded 215 distinct frames of 245 for the game and 270 of 300 for the gallery. The duplicate frames are the static title-card hold and the gallery's static moments. `capture.sh` now prints this check every run.
- **No audio.** The project has none; the MP4s are silent.
