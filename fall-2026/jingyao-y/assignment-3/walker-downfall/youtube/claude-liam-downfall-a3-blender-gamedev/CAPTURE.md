# CAPTURE.md

All engine footage was captured by Claude on 2026-10-12 from an **isolated clone of `ceada15`** (`git clone` of the local repo, then checkout).

**Changes in the capture clone** (they are not committed anywhere):
1. In `project.godot`: `window/size/window_width_override=3840`, `window/size/window_height_override=2160`, and `[editor] movie_writer/mjpeg_quality=0.95`.
2. `tests/capture_a3_film.gd`, copied from `capture/capture_a3_film.gd`.

**Build:** Godot `4.7.2.stable.official.ed1daf0bf`, GL Compatibility, Windows 11.

| Clip | Command | What it is |
|---|---|---|
| `stills.avi` (102 frames) | `--write-movie stills.avi --fixed-fps 30 --script res://tests/capture_a3_film.gd -- stills` | Mine floors through the game's camera. Seed 1729: the player is **teleported** to the first ramp's foot, then 7 m past its middle. Seed 1333 (the first seed that `capture_terrain.gd`'s search finds): teleported to the low side of a cliff between terraces. Teleporting is a test shortcut, not play. Frames 28, 52 and 98 became `images/game-ramp-4k.png`, `game-terrace-4k.png` and `game-cliff-4k.png`. |
| `orbit.avi` (540 frames) | `… -- orbit` | `art/models/asset_preview.tscn`: 2 s through the game-style camera, then a perspective camera on one 16 s orbit (radius 15, height 6.5), starting in front of the cliff's face. |
| `light.avi` (120 frames) | `… -- light` | Rubble close-up. For 2 s the sun has the basis as first written (TEST-REPORT loop 3: rows read as columns, light direction (−0.354, 0.707, 0.612), pointing up). For the next 2 s it has the corrected basis from `ceada15` (direction (−0.5, −0.612, 0.612)). This is a **re-render**: the original wrong render was overwritten during the work. |

**Why stills come from the movie:** under Movie Maker the window is capped at the screen size, 2564×1442 here, so `get_image()` stills came out at that size. The movie is written at the 3840×2160 override, so the film takes frames from the movie by number.

**Blender views:** these are Claude's MCP `look` images from the build session. They are 560–640 px and are shown scaled up and labelled.

**The author's screenshot (B17):** the author took it with the Windows snipping tool. It is `a3/screenshots/user-01-blender-ui.png`.

Narration is the master clock. Every engine clip is a contiguous window, **trimmed only, never retimed**. Stills are labelled holds.
