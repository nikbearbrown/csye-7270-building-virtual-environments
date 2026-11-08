# CAPTURE — how the film's evidence was recorded

**Film:** `claude-liam-walker-rudy-particles` · **Project:** walker-rudy, Assignment 6 (`fall-2026/shuai-z/assignment-6/`) · **Recorded:** 2026-11-07 (EST) · **Skill:** `godot-gamedev`, `walker` modifier. Claude Code (Claude Opus 5.5) made the new capture in this file on 2026-11-07, while building the film, at shuai-z's request to make the film ("接下来按照作业要求做影片", "next, make the film as the assignment asks").

## The source being demonstrated

| | |
| --- | --- |
| Source revision | `d0ed4152ba4c5dc88ac2d712dbdb5889b07c9f54`, the branch tip `shuai-z/assignment-6`; the working tree was clean apart from this reel folder when the capture was made |
| Game source | unchanged since `d60fb037` (the F9 key); `d0ed4152` added only Use It evidence and documents |
| Godot | 4.7.2.stable.official.ed1daf0bf, GL Compatibility (OpenGL 4.1 Metal), Apple M3, macOS 15.1 |

## 1 · The game in play: `capture/play-01.mp4` (B02, B10, B11, B18, B20, B22)

`game/` was copied with `rsync --exclude .godot` to a scratch directory outside the repository and imported there with a separate `HOME`. Two harness-only changes were made to the copy (`capture/game-project.godot.diff`):

1. `window_width_override` / `window_height_override` 1280 × 720 → **3840 × 2160**, so the game renders natively at 4K (the viewport is still 1920 × 1080 with `canvas_items` stretch, as in the project).
2. An autoload, `FilmDriver` (`capture/film_driver.gd`, copied here byte for byte as it ran). The real main scene, `res://app/main.tscn`, boots as F5 runs it. The driver presses input actions with `Input.action_press()`, as the game's state tests do: Enter on the title; run right; jump the first spikes and the first goblin; walk into the sword; one cut; five cuts as fast as the game allows; two cuts facing left; run left and Esc while running, then Esc again; a jump with a cut at the top; the cut that defeats the second goblin; a cut with Esc at once, then Esc again. It never calls the effects driver, never starts, stops or moves an emitter, and assigns nothing in the game. It runs with `PROCESS_MODE_ALWAYS` so it can log and resume while the tree is paused. Each frame, after every other `_process()`, it prints Rudy's place and mode, whether the hitbox is live, how many `SlashSparks` bursts are alive, whether `RunDust` is emitting, and whether the tree is paused.

```bash
HOME="$SCRATCH/home" godot --path game --resolution 3840x2160 --write-movie frames/play.png --fixed-fps 30
ffmpeg -framerate 30 -i frames/play%08d.png -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -r 30 play-01.mp4
```

- Movie Maker wrote 663 PNG frames (3840 × 2160) and a 48 kHz stereo WAV with the game's own music and effects (22.1 s), kept as `capture/play-01.wav`. The MP4 has 663 frames (`ffprobe -count_frames`). Run log, with the driver's steps and one `frame N …` line per frame: `capture/play-01-run.log`.
- **A dry run first.** Before the windowed take, Claude ran the same copy headless at `--fixed-fps 30` to check the route (a first version waited 4.5 s for the second goblin; the order was changed so the goblin walks towards Rudy). The windowed take's log has the same state changes on the same frame numbers as that final dry run.
- **The log's frame numbers are the MP4's.** Checked by pixel: frame 213 shows the swing with no flash and frame 214, where the log first counts a burst, shows the flash on the hitbox; the whole frame changes between 594 and 595, where the log says the tree paused, frames 595–630 are pixel-identical, and it changes back at 631, where the log says the tree resumed. The same holds at 375/376 and 411/412.
- **What the log records:** the run starting at frame 61 with `RunDust` emitting; off in the air from 97 and on again at the landing on 118 (the spikes), off at 136 and on at 157 (the goblin); the sword at 178; the stop at 190; one burst at 214; five fast cuts with two bursts alive on frames 250–253, 260–263, 270–273 and 280–283; two cuts facing left at 318 and 328; the run left from 356, paused 376–411, stopped at 422; the cut at the top of a jump at 469; the cut that defeats the second goblin at 561, the goblin hidden from 573, the burst alive until 574; a cut at 592 and the tree paused 595–630; three hearts throughout.
- Movie Maker renders offline at a fixed step, so this is not evidence of real-time frame rate. Physics ran at the project's 60 ticks a second, two ticks per frame.

**On screen:** every frame carries `GODOT 4.7.2 · MOVIE MAKER · NATIVE 4K ENGINE CAPTURE · play-01 · frames …` and `SCRIPTED INPUT · a film-only driver on a copy presses Enter, move, jump, slash and Esc`. Replays are labelled with their speed (`REPLAY 0.5×`, `⅓×`, `¼×`) and play without the game's sound. Replays that show a 16:9 region of the same frames scaled up to 3840 × 2160 (Lanczos) say `ENLARGED 2×` or `ENLARGED 1.5×`; the regions are in `tools/make_sheet.py` (`STAND`, `APEX`, `RUN`, `RUN_START`). The paused stretches are labelled `ESC · THE GAME IS PAUSED`. Where narration outlasts the footage, the last frame is held and labelled `HELD FINAL FRAME` (1.7 s in B10, 3.4 s in B11, 4.1 s in B18, 2.8 s in B20, 4.6 s in B22).

## 2 · The frame strips: fixture captures (B06, B08, B13–B16, B28)

These are the strips committed with each tuning round (`captures/slash_sparks/r0–r1/`, `captures/run_dust/r0–r3/`, `captures/*/mutation_godot3_name/`): Movie Maker runs of the two preview scenes in a 1280 × 720 window at 30 fps, made by Claude at shuai-z's request on 2026-11-04 and 2026-11-05, with their logs in `logs/capture_*.log`. They are fixtures (a frozen level, a sprite of Rudy), not the game, and every card that shows them says `FIXTURE CAPTURE(S)`. `tools/make_stills.py` crops them (`SPARK_BOX`, `DUST_BOX`) and enlarges the crops with nearest-neighbour, so no pixel is blended. Every reading and measurement on those cards is quoted from `TUNING.md`, and the script asserts each quoted phrase is in it.

## 3 · Codex's Use It captures (B27, B28)

`evidence/use-it-code/` holds the editor measurements and captures Codex (OpenAI's coding agent) recorded on 2026-11-06 at shuai-z's request, from a scratch copy at `d60fb037` (its README gives the method). The PNGs there are half-size copies. The film uses a crop of `02_A_heavy_editor.png` (the Visual Profiler, GPU column 0.0 ms) and crops of `supplement/80_sparks_visible_paused_a.png` and `81_…_b.png` (paused 0.7 s apart, pixel-identical in `pixel-checks.json`).

## 4 · Recorded logs (B23–B27)

`stills/tests.png`, `mutations.png` and `prices.png` print lines read from `logs/test_*_60fps.log`, `logs/checks_60fps.log`, `logs/invulnerable_tint_checks_60fps.log`, `logs/mutation_*_60fps.log` and `logs/cost_effects_60fps_rerun.log`, labelled `HEADLESS TEST OUTPUT` or `HEADLESS LOG`. `stills/shader-lines.png` prints lines read from `game/shaders/particles_generated.gdshader` and `CHANGE-BRIEF.md`.

| Still | Sources |
| --- | --- |
| `stills/game-card.png` | crops of frames 281 and 90 of `capture/play-01.mp4` |
| `stills/strip-a-r0.png`, `strip-a-r1.png` | `captures/slash_sparks/r0/`, `r1/`; `TUNING.md`, Effect A r1 |
| `stills/strip-b-r0.png` … `strip-b-r3.png` | `captures/run_dust/r0/` … `r3/`; `TUNING.md`, Effect B r1–r3 |
| `stills/shader-lines.png` | `game/shaders/particles_generated.gdshader` 10–11, 43, 139, 311; `CHANGE-BRIEF.md` §2 |
| `stills/tests.png`, `mutations.png` | the logs above |
| `stills/prices.png` | `logs/cost_effects_60fps_rerun.log`; `evidence/use-it-code/02_A_heavy_editor.png`, `summary.json` |
| `stills/headless-limits.png` | `captures/slash_sparks/r1/frame00000015.png`, `mutation_godot3_name/frame00000015.png`; `evidence/use-it-code/supplement/80–81` |
| `stills/three-parts.png`, `intent-a.png`, `intent-b.png` (figures) | `game/effects/slash_sparks.tscn` 79, 108, 109; `particles_generated.gdshader` 311; `CHANGE-BRIEF.md` §§2–3 |

## Hashes (SHA-256)

```
d1c89b532534be4b02c0dc6bd1e7129fe3e3f67121845087798e27294ad4614e  capture/play-01.mp4         (not in git)
329236afb85e4defa06ea733ae0890231dedbd91942e9191d5183cd4e6d074ad  capture/play-01.wav         (not in git)
c1c8885650a9d7af2267b248cfdc418c3d32bbcf6e9518ed19c53920eff1227f  capture/play-01-run.log
9af6ac910c0974711c285680c29596c6eb596e1b7499c88c30591a755982c85f  capture/film_driver.gd
7dcb5f2e0722ca6282a291ca1702b58db1a59fcbc2c0ac7d818b191187a2fccb  capture/game-project.godot.diff
```
