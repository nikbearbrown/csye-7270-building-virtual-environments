# Capture record — A8 pitch film

All game footage in the film is **scripted input recorded with Godot Movie Maker**, not human play. Every clip is labelled SCRIPTED INPUT on screen, with the source commit.

## Source
- Commit `f13431bf` of the course repository, folder `assignment-8/walker-survival-shooting/godot/`, extracted with `git archive` to `<film-work>/a8/game/godot/`; `--headless --import` exit 0. The course repository and my working project were not modified; my Godot editor was not touched.
- Capture-only files were added to the copy's `film_capture/` folder (kept in `<film-work>/a8/capture-tools/`): `a8_capture.gd/.tscn`, `a8_capture_os.gd/.tscn`, and `mome_demo_doc2.tscn` (instances the unmodified ThoughtPad debug scene with `demo_file_uid = 2`, the editable demo memo).
- Run: Godot 4.7.2-stable console, windowed, Forward+ / D3D12, NVIDIA GeForce RTX 5070 Ti Laptop GPU, Movie Maker 30 fps (`--write-movie`, `--fixed-fps 30`, `--resolution 1920x1080`). Windows display scaling made the frames 2048 x 1152; ffmpeg (lanczos) scaled them to 1920 x 1080, libx264 crf 18, no audio.

## How input is sent
- Keys: `Input.parse_input_event` with the physical keycodes the InputMap binds (Tab = tablet, Space = jump, W = forward).
- Mouse: injected `InputEventMouseButton` / `InputEventMouseMotion` with a marker device id; every other mouse event (the real mouse) is dropped. Movie Maker does not record the system cursor, so a **white arrow is drawn by the capture script** where the injected mouse is.
- To click a spot on the held tablet, the script finds the screen point whose ray hits that spot, using the game's own `PlayerController._get_mouse_screen_uv()` (the same function a real click goes through).
- Not through normal input: in `b11` the lights are toggled by calling `LightSwitch.interact()` (the function F calls) without walking to the switch; in `dust` the camera pitch is set by the script.

## Clips
| File | Beats | Length | SHA-256 |
|---|---|---|---|
| `captures/b10-scripted.mp4` | B10 | 8.37 s | 757fe9072620010b344cc600c493c93d774466f81db04298969f61faa7785356 |
| `captures/b11-scripted.mp4` | B11 | 13.37 s | 481673417d6f29ce2d0f329c537acb4fe7b46879e367af7509d75483d0beb965 |
| `captures/tablet-scripted.mp4` | B00, B07, B13 | 22.47 s | 28fb3894623ab8e74fade3342ca0eb97599d01e3679d9973a4c84b8297e0fec4 |
| `captures/dust-scripted.mp4` | (B11 alternative) | 12.03 s | 6705b1e878a3217ab68bcd1cddb8e4c78c35902b5313839b373ac4de69763ecb |
| `captures/mome1-scripted.mp4` | B08 | 6.73 s | e5f69fc71abd39b91b43046862bf27492f91c8b110e1faa4fa05a7fb06c4a6fa |
| `captures/mome2-scripted.mp4` | B08 | 7.63 s | 1ad331222307174bbe1c9b4c7ca054798bad0c8ce2ec2902d2e1c9a16c58c57c |

## Engine log (from `logs/capture-*.log`)
- **b10** (front view, camera pivot turned 180 degrees): short Tab at frame 30; one hand held on 33, screen lit on 54. Short Tab at 110: back on the hip on 113. Raise again at 172, interrupted by a short Tab at 176–178: back on the hip on 179, screen never lit.
- **b11** (default camera): jumps at 30 and 110; landed on 59 and 139 (landing dust). Lights off at 200, on at 290.
- **tablet**: B00 short Tab at 30 (one hand, lit), long Tab at 92 (two hands). B07: double-click This PC at 165 (window opens), double-click the first folder "home" at 222, Up at 279, minimize at 330, taskbar button at 383 (window back), show desktop at 436. B13: W held 45 frames with two hands from 501, body moved 0.000 m; short Tab at 561 (one hand); W held 50 frames from 593, body moved 5.698 m.
- **mome1** (read-only "Introduction"): typing " Can I type here?" left the text unchanged ("Here I cast aside my dignity.").
- **mome2** (editable "My Notes"): typing " Clue from the north gate." was added to the text.

## Document frames (B09, B12)
Made by `capture-tools/make_doc_frames.py`: it copies text verbatim from the files into an HTML page and screenshots it with headless Microsoft Edge at 1920 x 1080. Nothing is retyped by hand.
| File | Beat | Source of the text | SHA-256 |
|---|---|---|---|
| `captures/docs/b09-readme-keys.png` | B09 | the "Keys" section of `assignment-8/pitch/README.md` (English draft, not yet committed when rendered) | 937d71a954b6ee54b9f82ee60ebb6cf191544ec737b9337847c8a23afb3df465 |
| `captures/docs/b12-tests.png` | B12 | the last lines of a fresh run of the six tests in the f13431bf copy (`logs/b12-*.txt`, all exit 0; 55 / 29 / 157 / 27 / 110 / 41 PASS lines, counted by the script and marked "counted") | 3c8ea455dd0e63eb6146efbdb5ea405e2a785538c7934e286a3bd0afbbaaf56f |

## Problems found while capturing
1. First `b10` take: when the tablet went back to the hip, the game captured the mouse, and the real cursor's jump turned the camera. Fixed by dropping real mouse events during capture.
2. First `tablet` take: single clicks (Up, minimize, taskbar, show desktop) did nothing. Injected positions are read as window pixels, and the window was 2048 x 1152 under display scaling while the viewport is 1920 x 1080, so every click landed 6.7 % off. Fixed by converting viewport points to window points (`get_final_transform()`).
3. The light dust is almost invisible from the player camera: between two frames one second apart only 24 pixels change, by at most 19 of 255. The specks are too small at this distance.
4. The drag to select text in ThoughtPad shows no visible highlight in the frames; the film does not claim selection.
5. In the two-hand view only the tablet and the hands are visible (first-person view, as designed).
