# EVIDENCE-INDEX: the real material "Making Water in Godot" shows

**What this is.** A map from every picture the film shows to the real thing it is: which shader, which scene, which capture, which measured run; and what the film may and may not claim.
**Why.** The film's rule (Bear): everything shown was really done and recorded. This index is how a reviewer checks that, beat by beat, without reading code.
**Found.** Every Godot picture is a render of a shader in `lab-shaders/` run on Godot 4.7.2 (Apple M4 Pro, Metal, Forward+; Compatibility where the caption says so); the Inspector frames are a scripted editor session of the real editor; the nine Manim pictures are drawings (labelled) built from measured numbers and real images; the docs are quoted as quoted. Nothing was mocked.

REEL = `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot`. Paths below are relative to REEL.

## What may and may not be claimed (read this twice)

1. **Every captured frame is OFFLINE at a fixed tick rate** (the Lab harness, `--fixed-fps 30`). It says nothing about real-time frame rate, and the film makes no speed or cost claim: the only costs named are what the docs and the counts show (nine hash squares against one texture read, 16,641 vertices).
2. **A pixel value is only quoted with its renderer.** The film quotes: the typed colour (Forward+ 25, 115, 178; Compatibility 22, 115, 179), the blend (Forward+ 108, 129, 162; Compatibility 71, 128, 158), the median red of the ripple shader (132 against 100), the depth gap (Forward+ 0.500 m; Compatibility 0.494 m with the renderer branch, 0.000 m without). Every other picture is Forward+.
3. **Scripted events are labelled.** Shader swaps, colour changes and parameter sweeps inside clips are named in the `videoLabel` of the lane (`lanes/act*.json`); the wave clock in the later clips is the capture's own clock (the driver script writes it into the shader).
4. **The cove is a teaching scene.** Floating objects ride the waves because a script runs the same function; the film says the shader alone cannot move a node.
5. **The Inspector frames are a scripted editor session** (no human click, no visible mouse pointer; the Opacity value was set by script; the colour picker needed one scripted click). The scratch project had a driver addon: the full frame's FileSystem dock shows scratch folders, so the film uses the Inspector-only crop (cut from the real native frame, never redrawn).
6. **The docs are quoted as quoted** (render modes, the transparency sorting paragraph, the hints table, the `pow` note, the depth-texture recipe); the headless browser was not used (the docs site shows it a bot-check page); the raw pages were read with a plain HTTP fetch on 2026-10-16. The text of the pages read is kept in `evidence/docs-read-2026-10-16/` (22 files; `visualshadernodevoronoinoise`, `perlinnoise3d` and `randomrange` are the docs site's 'Page not found' page, kept as the evidence that those classes do not exist; `idx.txt` is the class index).
7. **The Unity video is a model of the order of ideas only**: nothing of its wording, jokes, sponsor material or steps is used (`SOURCES.md`).
8. **No number is rounded into a better story.** Where the measurement has a floor (8-bit readouts, about 2 mm for the wave check), the film says "about".

## What each beat shows

| Beat | Picture | Real thing |
|---|---|---|
| B01 | the finished water | `captures/hook.mp4`: `lab-shaders/06-shore-foam.gdshader`, plane cut 127 x 127, `water_driver.gd` clock |
| B02 | three links | Manim drawing; the labels are the real Inspector's (Mesh, Material Override), `captures/editor/W1-...png` |
| B03 to B07 | blue, dial, roughness, alpha, opacity | `captures/blue-applied.mp4`, `blue-dial.mp4`, `roughness.mp4`, `alpha-switch.mp4`, `opacity.mp4`; `lab-shaders/01-blue`, `02-transparent` |
| B08, B09 | the blend arithmetic | `captures/blend-fp.png`, `blend-compat.png` (the unshaded test, `evidence/planning-checks/scripts/e3_alpha_scene.gd`); Manim numbers from `logs/analysis.txt` |
| B10, B12, B13 | tables | `LectureEvidenceTable`; quoted docs and counted engine facts (`logs/facts1-classdb.txt`) |
| B11 | the red plane under the water | `captures/sorting.mp4`; `lab-shaders/02-transparent` and `02a-depth-draw-always`; E16 |
| B14, B16 | the squares and the nine | Manim drawings (labelled) |
| B15, B17, B18 | points, cones, edges | `captures/foam-points.mp4`, `foam-nearest.mp4`, `foam-edge.mp4`: `03a-cells-debug` (show 0, 1, 2) |
| B19 to B21 | foam | `captures/foam-width.mp4`, `foam-matte.mp4`, `foam-move.mp4`: `03-noise-foam` |
| B22, B23 | the power curve and its specks | `captures/power-curve.mp4`, `power-specks.mp4`: `03b-power-curve`; 462 black pixels (`png/pow-static-broken.png`) |
| B24 | function against texture | `captures/foam-vs-texture.mp4`: `03-noise-foam` and `03d-foam-from-texture` |
| B25 | normal-map strength | `captures/normal-strength.mp4`: `04a-normal-map` |
| B26, B27 | the normal map, seamless | Manim around the real `captures/normal_a.png`, `tiles-not-seamless.png`, `tiles-seamless.png` (`logs/facts2-noise-texture.txt`) |
| B28 to B30 | repeat, scroll, two layers | `captures/repeat-switch.mp4`, `scroll.mp4`, `two-layers.mp4`: `04e-no-repeat`, `04b`, `04c` |
| B31 | the straight edge | `captures/low-flat.mp4`: `04d`, low camera, 1280 x 720; `png/low-flat.png` |
| B32, B33 | warp; two renderers | `captures/warp.mp4`, `renderers-ripples.mp4`: `04d` |
| B34 to B38 | cuts, waves, normal, edge | `captures/cuts-compare.mp4`, `waves-low.mp4`, `waves-iso.mp4`, `normal-swap.mp4`, `low-waves.mp4`: `05`, `05b`, `05c-no-normal-update` |
| B39 to B41 | floaters, one clock, dials | `captures/floaters.mp4`, `wave-dials.mp4`; Manim for the clocks (E10, `logs/e10-clock.txt`, `logs/e10-clock-rerun.txt`); `water-project/scripts/wave_math.gd`, `water_driver.gd` |
| B42 to B44 | depth | Manim drawing (E8 numbers); `captures/gap-view.mp4`, `gap-test.mp4`: `06a-gap-view` |
| B45 | the helper error | `CCPlainShell` with `logs/e12-transcript.txt` (the output of `scripts/e12_builtins.sh`) |
| B46, B47 | shore band; the renderer branch | `captures/shore-width.mp4`, `compat-branch.mp4`: `06-shore-foam`, `06b-no-renderer-branch` |
| B48 | the Inspector | `captures/editor-inspector-dock.png` (the real editor's Inspector, native crop); EDITOR-LABELS.md |
| B49 | three looks | `captures/restyle.mp4`: `06-shore-foam` with three sets of numbers (`captures.py`) |

## The project the viewer can open

`water-project/` (a Godot 4.7.2 project): `scenes/water.tscn`, `shaders/` (copies of the film's shaders, byte-identical: `evidence/planning-checks/logs/project-sha256.txt`), `scripts/`, `tools/`. It ran in a real window (`tools/smoke.gd`, `evidence/planning-checks/png/project-smoke.png`).
