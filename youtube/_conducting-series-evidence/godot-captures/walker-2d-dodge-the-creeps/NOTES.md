# walker-2d-dodge-the-creeps: capture notes

**What this is.** A real windowed Godot 4.7.2 Movie Maker run of Dodge the Creeps, recorded 2026-10-09 at a fixed 30 fps from a scratch copy. The source at `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-2d-dodge-the-creeps/godot` was not touched. A script pressed the keys; nobody played by hand.

**Copy-only edits:** the autoload `_capture/capture_driver.gd` was added, and the window override was set to 720x1080. The game is portrait (480x720 logical), and a 16:9 window made Movie Maker record a mis-cropped, zoomed frame, so the window keeps the game's own aspect.

**Global RNG seeded to 11** (plan key `seed`). Mob spawns are random. Seed 11 was chosen after trying seeds 3 and 11: with seed 3 (and with no seed) the player died about 4 s into the clip. The seed is the only thing chosen; the mobs and the collisions are the game's own.

## Scripted input (from `raw-log.txt`, frames at 30 fps)
- f40–42: Enter (the start_game shortcut). This closes the title and shows "Get Ready".
- Then held movement actions in a loop of up, left, down, right: up f60–80, left f80–105, down f105–120, right f120–160, up f160–175, left f175–200, down f200–215, right f215–250, up f250–270, left f270–300.

## Files
| File | Size | What is on screen |
|---|---|---|
| `01-title-screen.png` | 720x1080 | "Dodge the Creeps" title, Start button, score 0. |
| `02-get-ready.png` | 720x1080 | "Get Ready" message; the player sprite at its start position. |
| `03-dodging-creeps.png` | 720x1080 | Score 1; the player moving right with its motion trail; three creeps on screen. |
| `04-dodging-creeps-later.png` | 720x1080 | Score 4; the player moving right; several creeps around it. |
| `05-end-state.png` | 720x1080 | Score 6, "Game Over": a creep hit the player about 9 s into the run, after the clip window. |
| `walker-2d-dodge-the-creeps-clip.mp4` | 1920x1080, 8.0 s, H.264, 30 fps, AAC | Movie frames 40–280: Enter, then "Get Ready", then the player dodging while the score climbs 0 to 5. The player survives the whole clip. The 720x1080 game is centred with black pillarbox bars. The audio is the game's own music, recorded by Movie Maker. |

**Problems:**
- The PNGs are 720x1080 (the game's full native area at 1.5x), not 1920 wide. Only the MP4 is padded to 1920x1080.
- Movie Maker's audio follows simulated time, so it matches the video. It is not a real-time listening test.
