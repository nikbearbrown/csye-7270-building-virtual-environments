# walker-pong: capture notes

**What this is.** A real windowed Godot 4.7.2 Movie Maker run of the Pong demo, recorded 2026-10-09 at a fixed 30 fps from a scratch copy. The source at `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-pong/godot` was not touched.

**Copy-only edits:** the capture autoload was added, and the window was set to 2134x1200. The project uses integer stretch scaling, so a 1920x1080 window would only draw at 2x (1422x800). 2134x1200 lets it draw at 3x. The clip is scaled down to 1920x1080.

**Global RNG seeded to 7375.** The game picks random paddle deflections; 7375 is the seed the project's own tests use.

## Scripted input
Both paddles are driven by a "track" controller in the driver. Each frame it compares the paddle's y with the ball's y and **presses or releases** the `left_move_up/down` and `right_move_up/down` actions (InputEventAction, deadzone 3 px). It never moves a paddle or the ball itself. The right paddle's controller stops at f420. The right paddle then sits still, misses, and the ball resets to the centre (around f480). There are 224 press/release events in `raw-log.txt`.

## Files
| File | Size | What is on screen |
|---|---|---|
| `01-serve.png` | 2133x1200 | Ball leaving the centre toward the left paddle (cyan); right paddle magenta; dotted separator. |
| `02-left-paddle-return.png` | 2133x1200 | Ball at the left paddle as it is returned. |
| `03-rally.png` | 2133x1200 | Mid-rally; ball near the right paddle, top of the court. |
| `04-rally-later.png` | 2133x1200 | Rally continuing (11 s in). |
| `05-after-right-miss.png` | 2133x1200 | After the right paddle stopped tracking and missed: the ball has been reset and is in play again. |
| `walker-pong-clip.mp4` | 1920x1080, 8.0 s, H.264, 30 fps, no audio | Movie frames 30–270: a rally of several returns, with both paddles tracking the ball. |

**Problems:**
- The court is the game's 640x400 with "expand" aspect, so dark side margins are part of the real frame.
- The Movie Maker WAV was silent (-91 dB), so the MP4 has no audio track.
