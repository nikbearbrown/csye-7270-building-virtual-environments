# Planning checks: results index (Making Water in Godot)

**What this is.** The index of every measurement the layout stage ran before a number or a picture went into the film: sixteen numbered experiments (E1 to E16), four engine-fact scripts (facts1 to facts4), the power-curve, normal-map, repeat, silhouette and render-mode renders, the compile check of all nineteen shaders, and the openable project's smoke run. Each row names the question, the script, the log and the number the film uses.
**Why.** The film may only say what a run showed ("Films = things actually done"). A reader of `FACTCHECK.md` must be able to follow a PASS row back to a log in one step, and the build session must know which numbers it can re-measure and which it must not edit around.
**Found.** Every number in the narration traces to a saved log below. One provenance gap was found and closed on 2026-10-16: the clock offset (E10) had once been quoted as "0.28 to 0.79 s", but the 0.79 s run had been printed and not saved; three more runs were logged (`logs/e10-clock-rerun.txt`) and the film now says "about three tenths of a second" (0.28 to 0.32 s over six logged runs). There is no E4, E5 or E6: those numbers were never used (the plan was reordered before they were run), so the list skips them on purpose.

All runs: Godot 4.7.2-stable (official), Apple M4 Pro, Metal. Offline harness runs (`capture_shader.sh`, fixed tick rate 30) say nothing about real-time frame rate. Real-time runs (E10, the smoke run) keep their window on top. Shaders under test are in `check-shaders/`; the film's own shaders are in `../../lab-shaders/`. Folder: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot/evidence/planning-checks/` (all paths below are relative to it).

## Numbered experiments

| Id | Question | Script and shader | Log | Result the film uses |
|---|---|---|---|---|
| E1 | Do typed `source_color` numbers read back as typed? | `scripts/run_e1_e2_e10.sh`, `check-shaders/e1-source-color.gdshader` | `logs/e1-source-color.txt` | Typed (0.10, 0.45, 0.70) reads (25, 115, 178) in Forward+ and (22, 115, 179) in Compatibility; without the hint it reads (89, 179, 218) in Forward+ |
| E2 | What does `TIME` read in the offline harness? | same script, `e2-time-clock.gdshader` | `logs/e2-time-clock.txt` | Offline frame f reads 0.025 to 0.036 s above (f + 1) / 30 (frames 0, 1, 15, 30, 59); used only to explain why the clock experiment is run in real time |
| E3 | How does alpha 0.7 blend over the sand floor? | `scripts/e3_alpha_scene.gd`, `e3-alpha.gdshader`, `scripts/analysis.py` | `logs/analysis.txt` | Forward+ measured (108, 129, 162) against a linear-light prediction (108, 129, 161) and a typed-number mix (73, 128, 158); Compatibility measured (71, 128, 158) = the typed-number mix |
| E7 | How big are the cells, and does a 3 x 3 search suffice? | `e7-cells-values.gdshader`, `scripts/analysis.py` | `logs/analysis.txt`, `png/e7-*.png` | Mean nearest distance 0.429 of a cell, maximum 1.042; 3 x 3 against 5 x 5 differ at 0.142 percent of pixels (second minus nearest); foam coverage 6.6, 12.8, 24.4, 34.9 percent at edge_width 0.05, 0.1, 0.2, 0.3 |
| E8, E8b | Does the depth gap read correctly in both renderers? | `scripts/run_e8.sh`, `scripts/e8_depth_scene.gd`, `e8-depth-gap.gdshader` | `logs/e8-depth-gap.txt`, `logs/e8b-gap-three-heights.txt` | Floors at 0.2, 0.5, 0.9 m read 0.200, 0.500, 0.902 m in Forward+; Compatibility 0.180, 0.494, 0.902 m with the renderer branch and 0.000 m everywhere without it |
| E9, E9b | Does the GPU's wave height match the CPU's? | `e9-wave-height.gdshader`, `e9b-wave-height-clock.gdshader` | `logs/e9b-cpu-gpu-wave-clock.txt`, `png/e9b-*.png` | rms 0.93 mm, maximum 3.11 mm on a 192 mm peak (one 8-bit level is about 2 mm) at three clock values |
| E10 | Do the shader's `TIME` and the script's clock agree? | `scripts/e10_clock.gd`, `e10-clock.gdshader`, run by `scripts/run_e1_e2_e10.sh` | `logs/e10-clock.txt`, `logs/e10-clock-rerun.txt` | Script clock minus TIME: 0.316, 0.281, 0.283, 0.321, 0.308, 0.286 s (six logged real-time runs, 0.28 to 0.32 s, spread about 0.02 s within a run); different on every run, so the script writes `wave_clock`. An earlier unlogged run read 0.79 s: not used |
| E11 | What does a scrolled normal map do without `repeat_enable`? | `scripts/run_exps_batch1.sh`, `e11-no-repeat.gdshader` | `logs/repeat-disable.log`, `logs/repeat-enable.log`, `png/repeat-*.png` | Without repeat the scrolled map smears into streaks; with it the water tiles |
| E12 | Which built-ins are visible in a helper function? | `scripts/e12_builtins.sh`, `e12-builtin-*.gdshader` (six) | `logs/e12-builtins-in-helper.txt`, `logs/e12-builtin-in-helper-engine-log.txt`, `logs/e12-transcript.txt` | `TIME` and `TAU` compile; `UV`, `VERTEX`, `SCREEN_UV`, `INV_PROJECTION_MATRIX` give `Unknown identifier` |
| E13 | What happens to the glare when `NORMAL` is not updated after the vertices move? | `scripts/run_exps_batch1.sh`, `e13-no-normal.gdshader` against `05b-synced-clock` | `logs/normal-missing*.log`, `logs/normal-updated*.log`, `png/normal-*.png` | Without the matching normal (ripples and foam off) the glare stays one flat oval; with it the glare breaks into glints on the crests (`png/normal-missing2.png` against `normal-updated2.png`) |
| E14 | Does `cull_back` hide the water from underneath? | `e14-cull-disabled.gdshader` | `logs/e14-cull-under.txt`, `png/under-cull-*.png` | Camera 1.2 m under the water: 0.0 percent of the frame is water-blue with cull_back, 55.5 percent with cull_disabled |
| E15 | Do the two renderers draw the ripple shader alike? | `scripts/run_exps_batch1.sh` (r04c, r04d) | `logs/e15-renderers-ripples.txt`, `png/r04c-*.png`, `png/r04d-*.png` | Median red 132 (Forward+) against 100 (Compatibility); medians for green and blue within 5 |
| E16 | Do the three written-out render-mode defaults change anything, and what does `depth_draw_always` do to a sorted plane? | `e16-no-render-mode.gdshader`, `e16-depth-always.gdshader` | `logs/e16-sorting.txt`, `png/sort-*.png` | The defaults written out give 0 differing pixels; `depth_draw_always` changes 56,099 pixels, and the red plane under the water goes from (196, 100, 126) to (124, 150, 188) |

## Engine-fact scripts

| Id | Question | Script | Log | Result |
|---|---|---|---|---|
| facts1 | Does Godot have a Voronoi or a noise node? | `scripts/facts1_classdb.gd` | `logs/facts1-classdb.txt` | 110 `VisualShaderNode` classes, none makes noise; no Voronoi class; `NoiseTexture2D` and `FastNoiseLite` (type Cellular) exist; the `PlaneMesh`, `FastNoiseLite` and `NoiseTexture2D` property lists |
| facts2 | Is a NoiseTexture2D seamless, and how steep is its normal map? | `scripts/facts2_noise_texture.gd` | `logs/facts2-noise-texture.txt` | Grey texture: edge jump 0.2354 not seamless against 0.0086 seamless; normal map: edge jump 0.3532 not seamless against 0.0063 seamless, where one neighbouring step is about 0.0065 (53 times a step); the normal map's mean colour is (0.498, 0.498, 0.996); mean lean 3.4 degrees, maximum 12.8 at bump strength 6 |
| facts3 | What does the FastNoiseLite default do to a cellular texture? | `scripts/facts3_cell_texture.gd` | `logs/facts3-cell-texture.txt` | With the default fractal (FBM, five octaves) the minimum is 0.004 and the cells smear; with Fractal Type None it is 0.000 |
| facts4 | What does `get_shader_parameter` return for a parameter never set? | `scripts/facts4_get_param.gd` | `logs/facts4-get-param.txt` | `<null>` (TYPE_NIL), even though the shader declares a default; after a set it returns the value |

## Other renders and checks

| What | Where | Result |
|---|---|---|
| Power curve: negative base without and with the clamp (top view) | `logs/pow-broken.log`, `pow-clamped.log`, `pow-static-*.log`, `png/pow-*.png` | With the points frozen (cell_speed 0) 462 exactly-black pixels (four specks of 258, 167, 22 and 15) of 1,166,400 without the clamp and 0 with it; with moving points one frame had 88; the 258-pixel speck at (221, 545) is the one B23's ring boxes |
| Function foam against baked-texture foam (top view) | `logs/foam-function.log`, `foam-texture.log`, `png/foam-*.png` | the pair B24 compares side by side (C16); the texture needs Fractal Type None and Seamless on, and its points cannot move (see FACTCHECK rows 67 to 71) |
| Silhouette from the low camera: normal-map water against real waves | `logs/low-flat.log`, `low-waves.log`, `png/low-*.png`, `logs/edge-spread.txt` (re-measured 2026-10-16 on the re-recorded clips) | Flat clip: near edge on row 487 or 488 (spread 0, one row of encoding noise); wave clip: spread 40 to 96 rows, mean 78, over 122 frames; the still reads 95 rows. B38 says "up to ninety-five" |
| PlaneMesh vertex counts | `logs/facts1-classdb.txt`; the smoke run | cuts 0, 1, 3, 31, 63, 127 give 4, 9, 25, 1,089, 4,225 and 16,641 vertices: (cuts + 2) squared |
| Compile check, all 19 shaders in both renderers | `scripts/run_compile_check.sh`, `logs/compile-check.txt` | all compile in both renderers except `06c-builtin-in-helper-error`, which fails on purpose with `Unknown identifier ... INV_PROJECTION_MATRIX` |
| `water-project/shaders` against `lab-shaders` | `logs/project-sha256.txt` | byte-identical (sha256 prefixes listed) |
| Smoke run of the openable project in a real window | `png/project-smoke.png` | 16,641 vertices; the buoy rides a wave |
| Docs-site wording | `../../SOURCES.md`, `../../FACTCHECK.md` | fetched with curl as text (the docs site bot-checks headless browsers); every docs line is shown as quoted, never as a screenshot |
| Scripted editor session (B48) | `EDITOR-LABELS.md`, `../../captures/editor/` | 22 stills and native twins; the folder names Color, Clarity, Foam, Ripples, Waves and Shore replace any Shader Parameters header |

## Kept failed runs (so the build does not repeat them)

- `logs/pow-broken.log`, `logs/pow-static-broken.log` and `png/pow-*broken.png`: the unclamped power curve, kept as the evidence for B23.
- `logs/repeat-disable.log` and `png/repeat-disable.png`: the smeared normal map, kept as the evidence for B28.
- `logs/normal-missing.log` and `png/normal-missing*.png`: the glare that stays one oval, kept as the evidence for B37.
- `logs/e12-builtins-in-helper.txt` and `check-shaders/e12-builtin-*.gdshader`: the four compile errors, kept as the evidence for B45; `lab-shaders/06c-builtin-in-helper-error.gdshader` is the same error as a film shader.
- `logs/e8-depth-gap.txt`: the "renderer branch: NO" rows (0.000 m everywhere), kept as the evidence for B47.
- `logs/under-cull-back.log` and `png/under-cull-back.png`: the invisible water from underneath (E14).

Runs that were wrong and were replaced, not kept: the first E8 (its "no branch" rows did not reach the scene's material), the first Compatibility depth readout (decoded as sRGB, 0.099 m), and the first driver that read `get_shader_parameter`. Their mistakes are in `../../BUILD-LOG.md`.
