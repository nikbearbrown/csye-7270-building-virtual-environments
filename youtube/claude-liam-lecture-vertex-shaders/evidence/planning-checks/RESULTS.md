# Planning checks: results

**What this is.** The runs behind the numbers in `FACTCHECK.md`, in the order of the film, with the script, the log, and what was found. All on Bear's Mac: Apple M4 Pro, macOS, Godot 4.7.2 stable (official), Forward+ unless stated, 2026-10-13.
**Why.** So any figure on screen can be re-run, and so the failed and inconclusive runs are visible next to the good ones.
**Found.** 37 Shader Lab runs, 14 verification scripts, 4 analysis scripts and 58 frames of 26 capture scenes. Three runs did not go cleanly the first time and are described below; one compile error is expected and kept. Everything the film asserts about Godot was either read in the 4.7 docs or run here.

## How to re-run

- Lab batch: `python3 run-lab-checks.py` (writes `lab-results.jsonl` and `png/<check>.png`; each check is one `../../../_godot-shaders-series/lab/check_shader.sh` call, the command is in the jsonl). Summary: `lab-summary.txt`.
- A verification script: `./run-check.sh verify1.gd` (log in `logs/verify1.log`; scripts live in `scratch-project/`, a tiny Godot project that finds this film's `lab-shaders/` and `check-shaders/` itself). Add a renderer as the second argument (`gl_compatibility`) to repeat a check there.
- Capture scenes: `./run-scene.sh <scene-id> <times> --duration 12` for one scene, `./render-scene-frames.sh` for all (real time, planning only; frames in `png/scene-*.png`).
- Numbers from the pictures: `python3 -I analyze_pngs.py`, `analyze_equal_pictures.py`, `analyze_densities.py`, `flag_motion.py` (Pillow and numpy; all printed together in `measurements.txt`).

## Runs

| Script or batch | Log or output | Finding |
|---|---|---|
| `run-lab-checks.py`: `01-slide` at scale 1.0, 2.0 and 2.25 | `lab-results.jsonl`, `measurements.txt` | `VERTEX.x += 40.0` moves a 128 px sprite 40 px at scale 1.0, 80 px at 2.0, 90 px at 2.25: `VERTEX` is local (row 12) |
| `02-squash`, `03-lean` | same | squash box 192 x 64, centre unchanged; lean left edge 256 to 306, straight within 0.49 px, samples 257, 268, 281, 293, 305 (rows 13, 16, 17) |
| `c1-vertex-local`, `c4-uv-passes-through` | `lab-summary.txt` | `VERTEX` reads -62..+62 at 2 px inside the corners of a 128 px sprite at two scales; a UV halved in `vertex()` reaches `fragment()` blended (rows 8, 9, 54) |
| `04-ripple` on a four-vertex sprite | `measurements.txt` | top edge 116, 128, 140: a straight tilt of 24 px, edges straight within 0.49 px (row 22) |
| `05`, `06`, `07` (flag steps), `10`, `11` | `lab-results.jsonl` | all compile; `07` with `amplitude` 0.0 has a flat top edge (rows 43, 44, 47) |
| `08-corner-colors` (Forward+ and Compatibility), `09-corner-colors-flat` | `lab-summary.txt` | mid-top red 0.502, centre (0.502, 0.502, 0.498); both renderers identical; with `flat` a four-vertex sprite is one colour (rows 51, 52) |
| `12-stripes-from-vertex`, `13-stripes-from-fragment` | `lab-summary.txt` | 0.749 at every probe against 0.58 to 0.92 (row 59) |
| `c6-varying-written-in-fragment-read-in-vertex` | `lab-results.jsonl` | **Expected failure, kept.** Godot's parser accepts it; the generated vertex shader fails with `'m_v' : undeclared identifier`. Not shown in any beat (row 50) |
| `c7` (control), `14`, `15` (both renderers), `16-slide-far`, compatibility `01` and `03` | `lab-summary.txt`, `measurements.txt` | the control compiles; fragment `VERTEX` reads the screen position (0.451 at pixel 578 of 1280), vertex-stage `VERTEX` reads -62 (0.0196); both renderers agree; far slide +200 px; pixel counts equal in Compatibility (rows 61, 62, 66, 73) |
| `verify1.gd` | `logs/verify1.log` | `QuadMesh` vertices = (cuts + 2) x (cuts + 2): 4, 9, 25, 18, 18, 441, 297; a 0 by 0 mesh has 6 indices (2 triangles); width cuts run across (x), depth cuts run down (y); with +size.y the texture is upside down in 2D, with -size.y upright like a Sprite2D (rows 28, 30, 31, 52, 60) |
| `verify2.gd` | `logs/verify2.log` | `VERTEX` and `UV` read the same on a `Sprite2D`, a `MeshInstance2D` with a `QuadMesh` and a `Polygon2D` (row 8) |
| `verify3.gd` (first look) | `logs/verify3.log`, `png/verify3-flags-*.png` | The same one-line wave on four kinds of flag. **Panel D was a failed first attempt, kept:** a `Polygon2D` given outline points, interior points and `internal_vertex_count` but no `polygons` list drew a garbled picture and the wave did not reach the interior. It led to the `polygons` cell-list version (`polygon-grid`), which equals the mesh pixel for pixel (row 38) |
| `verify4.gd` | `logs/verify4.log` | `VERTEX_ID`: a `Sprite2D` reads 0 to 3, a six-point `Polygon2D` 0 to 5, a 3 by 3 `QuadMesh` 0 to 24 (rows 24, 36). **The first version saturated for the mesh** (id/16 over 25 vertices); it now takes an `id_scale` uniform |
| `verify5.gd` | `logs/verify5.log` | 31 by 7 mesh prints 297; polygon prints 66; a 19 by 19 mesh reads ids up to about 440 of 441 vertices; 66 outline points triangulate into 64 triangles, one point in 34 of them, longest edge 408 px on a flag 384 px wide (rows 30, 31, 37). The log ends with harmless engine messages about resources freed at exit |
| `verify6.gd` | `logs/verify6.log` | `COLOR` in `vertex()` includes `modulate` and `self_modulate`; `COLOR.rgb *= 0.5` halves the picture colour; assigning `vec4(1.0)` drops the modulate (rows 55, 75) |
| `verify7.gd` | `logs/verify7.log` | a `Polygon2D` has `UV` 0, 0 everywhere without a texture, even with `uv` set; with a texture it reads 0.02, 0.988, 0.502 (row 64) |
| `verify8.gd` | `logs/verify8.log` | the default render of an outline-only polygon equals the `Geometry2D.triangulate_polygon` triangles pixel for pixel (row 37) |
| `verify9.gd` | `logs/verify9.log` | after a 200 px slide: `get_rect()` unchanged, position unchanged, an `Area2D` collision shape overlaps the probe at the node and not the probe at the picture; picture left edge 156 to 356 (row 66) |
| `verify10.gd` | `logs/verify10.log` | the one-line count run in a node's `_ready()` prints 297 (row 68) |
| `verify11.gd` + `analyze_densities.py` | `logs/verify11.log`, `png/density-x3-*.png`, `measurements.txt` | worst gap from the true sine 10.76, 1.99 and 0.35 px for 4, 10 and 32 pieces at 3x zoom; formula 11.03, 1.89, 0.19 px; rule of thumb 1 - cos(pi / pieces per wave) (rows 33, 34) |
| `verify12.gd` | `logs/verify12.log` | the five GDScript lines of beat B15 as shown give 25 vertices and 32 triangles (row 29) |
| `verify13.gd` | `logs/verify13.log` | the call of beat B25 as shown moves the top edge from the amplitude-24 formula to the amplitude-40 formula within 1 px (row 46). **Two earlier versions gave a misleading answer because `TIME` stopped advancing while they read a frame every frame for several seconds; this version takes `TIME` out of the measurement (the speed dial is set to 0 first)** |
| `verify14.gd` | `logs/verify14.log`, `png/verify14-border.png` | the `Polygon2D` border artifact named in the brief: with uv outside 0 to 1 the border pixels repeat outward; four steps on `UV` hide them. Not narrated (the UV film's topic); checked for the record (row 74) |
| `analyze_equal_pictures.py` | `measurements.txt` | 0 of 288,000 pixels differ for: 297 against 66 vertices; explicit varying against the `COLOR` line; grid `Polygon2D` against the mesh (rows 35, 38, 58) |
| `flag_motion.py` + scenes `pinned`, `travel` | `measurements.txt`, `logs/scene-pinned.log`, `logs/scene-travel.log` | the fitted clock advances 0.196 to 0.208 s per 0.20 s of real time (the wave moves right); pinned left edge y = 276 in every frame; unpinned left end bobs between 256 and 300 (rows 40, 42). **The first frames were taken while another Godot window was open: the window was covered and `TIME` did not advance (clock advanced 0.000 s). The planning scripts now keep their window on top and the frames were re-taken** |
| `render-scene-frames.sh` | `logs/scene-*.log`, `png/scene-*.png` (58 frames) | every capture scene of `CAPTURE-PLAN.md` ran without an error and was looked at: tilt, pair, densities, cut-along, polygon, pinned and travelling flags with the grey pole, lit flag, stripes, flip, vertex-two, polygon-uv, drawing-only |

## Earlier runs that were superseded, not hidden

The Lab batch was run twice before the final one: once before the flag steps were reordered (unpinned travelling first, then pinned) and the hint ranges were taken out of the uniform lines, and once with the old file numbering. Their outputs were overwritten by the final batch; the shaders they ran no longer exist. The logs of the covered-window `flag_motion` frames and of the first two `verify13` versions were overwritten by the re-runs described above.

## Side findings for the series

- A `Polygon2D` has `UV` only with a texture (row 64); a flag shader that multiplies by `UV.x` does nothing on a textureless polygon.
- `get_shader_parameter` returns null for a uniform never set from code (`verify13.gd` prints it as `amplitude_before_call`), matching the pilot's finding.
- In a windowed script run, a covered window stops being drawn and `TIME` stops with it. Offline fixed-tick capture is not affected.
