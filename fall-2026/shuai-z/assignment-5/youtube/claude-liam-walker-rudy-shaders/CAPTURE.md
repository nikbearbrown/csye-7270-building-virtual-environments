# CAPTURE — how the film's evidence was recorded

**Film:** `claude-liam-walker-rudy-shaders` · **Project:** walker-rudy, Assignment 5 (`fall-2026/shuai-z/assignment-5/`) · **Recorded:** 2026-10-28 (EDT) · **Skill:** `godot-gamedev`, `walker` modifier. Claude Code (Claude Opus 5.5) made every capture in this file, on 2026-10-28, while building the film.

## The source being demonstrated

| | |
| --- | --- |
| Source revision | `a2a3a77d50c5c9d8a65663d21898b7de54096604`, the branch tip `shuai-z/assignment-5`; the working tree was clean apart from this reel folder when every capture below was made |
| Runtime source | unchanged since `bd797945` in `game/` and `fe795908` in `godot/`; later commits touched only `game/tests/`, `godot/tests/`, `godot/tools/` and documents (TEST-REPORT.md, "What it ran on") |
| Godot | 4.7.2.stable.official.ed1daf0bf: GL Compatibility (OpenGL 4.1 Metal) for `game/`, Forward+ (Metal 3.2) for `godot/`, Apple M3, macOS 15.1 |

## 1 · The game in play: `capture/play-01.mp4` (B02, B08, B09)

`game/` was copied with `rsync --exclude .godot` to a scratch directory and imported there with a separate `HOME`. Two harness-only changes were made to the copy (`capture/game-project.godot.diff`):

1. `window_width_override` / `window_height_override` 1280 × 720 → **3840 × 2160**, so the game renders natively at 4K (the viewport is still 1920 × 1080 with `canvas_items` stretch, as in the project).
2. An autoload, `PlayDriver` (`capture/play_driver.gd`, copied verbatim here). The real main scene, `res://app/main.tscn`, boots as F5 runs it. The driver presses input actions with `Input.action_press()`, as `game/tests/invulnerable_tint_checks.gd` does: Enter on the title; `move_right` into the first spikes; `move_right` back onto them inside the window; `move_left` off them; a second hit; the last heart and the respawn. It never calls `take_hit()`, `respawn_at()` or `set_shader_parameter()`, and assigns nothing in the game. Each frame, after every other `_process()`, it prints the `tint_amount` the hearts' material holds.

```bash
HOME="$SCRATCH/home-game" godot --path game --resolution 3840x2160 --write-movie frames/play.png --fixed-fps 30
ffmpeg -framerate 30 -i frames/play%08d.png -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -r 30 play-01.mp4
```

- Movie Maker wrote 425 PNG frames (3840 × 2160) and a 48 kHz stereo WAV with the game's own music and effects, kept as `capture/play-01.wav`. The MP4 has 425 frames (`ffprobe -count_frames`). Run log, with the driver's steps and one `frame N tint_amount …` line per frame: `capture/play-01-run.log`.
- **The log's frame numbers are the MP4's.** Checked by pixel: P1 (heart 1's red, (108, 116) at 4K) reads (201, 63, 53) at frames 129–130, where the log says 0.000000, and (182, 126, 132) at frame 131, where it says 0.986111. The brief's formula gives (181.5, 127.2, …) for 0.986.
- **What the log records:** hit 1 at frame 131 (0.986111, two hearts); the walk back onto the spikes inside the window, no heart lost, no rise; 0.000000 from frame 167; hit 2 at 223 (0.972222); hit 3, the last heart, at 308 (0.986111); the respawn at 343, which jumps from 0.041667 to 0.972222, three hearts.
- Movie Maker renders offline at a fixed step, so this is not evidence of real-time frame rate. Physics ran at the project's 60 ticks a second, two ticks per frame.

**The inset.** `tools/make_play_inset.py` writes `capture/play-01-inset.mp4` from `play-01.mp4`, frame for frame: a panel at the top right with that frame's hearts (the region (48, 40)–(432, 180)) enlarged 3× nearest-neighbour, and the frame's `tint_amount` and heart count from the log. Nothing else in the frame changes, and no frame is added, dropped or retimed. The film uses the inset version; both are hashed below.

**On screen:** every frame carries `GODOT 4.7.2 · MOVIE MAKER · NATIVE 4K ENGINE CAPTURE · play-01, hearts inset added · frames …` and `SCRIPTED INPUT · a film-only driver on a copy presses Enter, move_right and move_left`. The replays are labelled `REPLAY 0.5×` (B08) and `REPLAY ⅓×` (B09), with the game's sound off; the 3.4 s and 3.1 s holds at the ends of B08 and B09 are labelled `HELD FINAL FRAME`.

## 2 · The props scene: `capture/stone-01.mp4` (B02, B14)

A second scratch copy of `godot/`, imported with its own `HOME`, with two harness-only changes (`capture/godot-project.godot.diff`): the 4K window override, and an autoload, `StoneOrbitDriver` (`capture/stone_orbit_driver.gd`). The real main scene, `res://scenes/props_room.tscn`, boots as F5 runs it; the driver only moves its `Camera`:

- **A**, frames 0–689: 45 frames on the scene's own camera, one orbit about (−0.3, 0.25, 0) at its radius (4.6 m) and height (2.2 m) over 600 frames, 45 frames back home (the same path as Assignment 3's `orbit-01`);
- **B**, frames 690–989: a cut to an arc in front of the waystone, 1.7 m out and 0.95 m up, from −55° to 55°;
- **C**, frames 990–1289: a cut to an arc over the teleport circle, 2.0 m out and 1.5 m up, from −40° to 40°.

It changes no prop, light, floor or material, so the waystone's Stone and the circle's DarkStone are drawn by `weathered_stone.gdshader` through `waystone_stone.tres` and `circle_darkstone.tres` as saved.

```bash
HOME="$SCRATCH/home-godot" godot --path godot --resolution 3840x2160 --write-movie frames/stone.png --fixed-fps 30
ffmpeg -framerate 30 -i frames/stone%08d.png -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -r 30 stone-01.mp4
```

Movie Maker wrote 1291 frames and a WAV that is digital silence (peak 0): the scene has no sound. The MP4 has 1291 frames. Run log: `capture/stone-01-run.log`. The film uses frames 0–689, 690–929 and 1000–1239 at 1.0×, with the cuts labelled `CUT · …` and every frame carrying the provenance chip and `CAMERA MOVED BY A FILM-ONLY SCRIPT · props, light, floor and materials untouched`.

## 3 · The windowed captures reused from Use It (B06, B12, B16, B18, B23)

These were made on 2026-10-27 by the tools in `game/tests/` and `godot/tests/`, with shuai-z's approval, and are committed in `evidence/use-it/` with their logs in `logs/`. The film crops, scales and labels them (`tools/make_stills.py`); pixel crops of the hearts and the grey bands use nearest-neighbour enlargement, so no value is blended. TEST-REPORT.md §§4, 6, 7, 8 and 12 say who ran and judged each.

| Still | Sources |
| --- | --- |
| `stills/tint-captures.png` | `evidence/use-it/hearts-tint-{0.0,0.5,1.0,2.0}.png`; `logs/capture_tint.log` |
| `stills/sweep.png` | `evidence/use-it/sweep/close-*.png`; `logs/capture_sweep.log` |
| `stills/hint-result.png` | `evidence/use-it/hint-experiment.png`; `logs/capture_hint.log` |
| `stills/two-materials.png` | `evidence/use-it/sweep/two-materials-*.png`; `logs/capture_sweep.log` |
| `stills/headless-limits.png` | `evidence/use-it/os-compare/engine.png`, `os-screenshot.png`; `logs/capture_hint_vs_os.log` |
| `stills/tint-tests.png`, `stills/mutations.png` | recorded headless logs: `logs/game_invulnerable_tint_checks_{30,60,144}fps.log`, `_60fps_no_semicolon.log`, `_60fps_renamed.log`, `logs/godot_test_materials_60fps.log`, `_60fps_no_source_color.log` |
| `stills/game-card.png` | frame 134 of `capture/play-01.mp4`, frame 20 of `capture/stone-01.mp4` |

## Hashes (SHA-256)

```
2a6595bbacb090fd1deed5e748e0129c8e1567b45713130aa6e7c88f4343dda4  capture/play-01.mp4         (not in git)
67b2634737acf364c929bdd18ce1b8f96ea3bbd7d95b59abb8f1a0afef5887ad  capture/play-01-inset.mp4   (not in git)
5d52d75a5a8cd25569c0620621fe2ae706a839b39bd8af53e0fdc4da99f0f6b0  capture/play-01.wav         (not in git)
779acb2f3b30ef6447832908ea761a52ae39cd8fb51d7f6ea9305ff3c07a36fb  capture/play-01-run.log
02c6827c3505151342312704a86ad4384c2047d13f122e063b056ab9b472dab1  capture/play_driver.gd
0c6a8fdffeafc3f234c46fc16a3aa78b4c08b520764d2d6c1e6b387946af7823  capture/game-project.godot.diff
f5f16dcac3f4c4c06b79057f2f9f5dc8e2adb13d2a97029304d4adea284c6418  capture/stone-01.mp4        (not in git)
6a67ccef7279bc304ff303d613dfc5b40a4a0586146f17c1021c08ce33b1129a  capture/stone-01-run.log
ef77e6340997a6f867b8ef2e2c2b30388728606cbf1b8103cf8c17b16f59a612  capture/stone_orbit_driver.gd
5debee14c8f9304b6c9a44970a51ae620b6866321a2467d4243d15858783c654  capture/godot-project.godot.diff
```
