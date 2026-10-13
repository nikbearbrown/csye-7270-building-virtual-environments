# Capture plan: Vertex Shaders

**What this is.** Every Godot render the build session must record for this film, with the scene, the exact shader file, the canvas, when each scripted event happens, how long to record, what must be on screen at the 50 % and 85 % marks, and the result already verified. Nothing is recorded yet; every number below comes from planning runs in `evidence/planning-checks/` (real Godot 4.7.2 windows, Apple M4 Pro, Forward+).
**Why.** Films show only what was really done and recorded. This is the list of things to really do, written so a medium-effort session can do them without further judgment. Two things make this film different from the pilot: most pictures are **custom scenes** (a mesh, a polygon, two nodes side by side), and their events must land on the words, so they are timed as fractions of each beat's measured audio.
**Found.** 25 captures: 24 custom scenes and one Lab still (C18), plus one terminal run (B40). **No editor frames, no screenshots, no scripted key presses.** All 24 scenes are built from code in `evidence/planning-checks/scratch-project/capture_scenes.gd` (with `vscene.gd` beside it) and were run once in planning; the frames are in `evidence/planning-checks/png/scene-*.png` so the build session can compare. Several are reused: C01 serves B01 and B33, C15 serves B23 and B26.

## Conventions for every capture

- 30 fps; the scene's own logical canvas (**640 x 360** for the one-square scenes, **1280 x 720** for everything with a flag) rendered at 3840 x 2160 through a SubViewport (the pilot's proven route); stage colour `#D9D5CA` (set in `vscene.gd`, same as the Lab); Forward+. Pixel numbers in the film (40 px, 50 px, 24 px, minus 64 to 64) are in the logical canvas.
- **Offline fixed tick.** Capture frame by frame at 1/30 s per frame, so a shader's `TIME` starts at 0 on the first frame and advances exactly 1/30 s per frame. Nothing here says anything about real-time frame rate, and the film never does.
- **Events are fractions of D**, the beat's measured audio in seconds (`f x D`), so the picture lands on the sentence that says it. Record **after** the audio exists (or re-record when the audio changes the beat length by more than half a second). Unless a row says "loop", record from 0 to the last event plus 1.5 s and let ShaderLab hold the last frame.
- **Loops.** `final` (C01) and `dials-rest` (C15) run on a live clock at speed 3, whose wave period is 2.094 s: record 252 frames (8.4 s, four periods) and loop them; the seam is under 1 % of a period out, invisible.
- Every scripted change (a shader switched on, a dial turned, a mesh cut again) is labelled "scripted" in `videoLabel`. Nothing is drawn over a capture except the scene's own overlays (the grey node outline in C25, the terracotta vertex dots in C08, the grey pole), all made by the scene script; ShaderLab adds its own rings and readouts.
- Output to `runtime/remotion/public/vertex-shaders/` with the names in `lanes/` (`flag-final.mp4`, `slide.mp4`, ...; stills `.png`).

## Harness features this list needs

The shared harness (`../_godot-shaders-series/COMPONENT-SPECS.md`) offers `--frames`, `--fps`, `--out`, `--renderer`, `--animate`, `--steps`, `--scene PATH.gd`, `--length SECONDS` (keyframes as fractions of the clip), `--set-at`, `--call-at`, `--material-at` and `--time-origin`, then ffmpeg. This film needs only: (1) **`--scene`** loading `scratch-project/capture_scenes.gd` and `vscene.gd`: it calls `build(id, parent, shader_dir, duration)` once and `tick(ctx, t)` once per frame with `t = frame / 30` (the file holds all 24 scenes, so pass the scene id as a scene argument, or write a three-line wrapper per id if `--scene` expects one scene per file); (2) the scene's `ctx.canvas` as the logical size; (3) **`--length D`** for the beat's measured audio; (4) the shader directory = this film's `lab-shaders/`. Every shader switch, uniform sweep and `set_shader_parameter` call is made by the scene itself, so `--material-at`, `--set-at`, `--call-at`, `--animate` and `--time-origin` are not needed (they may replace the scene's own events if the harness prefers; the timings are in the table below). No key events. The scene library has no dependency on the planning scripts; `scene_frames.gd` shows how to drive it.

## Godot renders

| ID | Beat | Scene (`capture_scenes.gd`) | Shader(s) in `lab-shaders/` | Canvas | Events (fractions of D) | Record | On screen at 50 % and 85 % | Verified result to reproduce |
|---|---|---|---|---|---|---|---|---|
| C01 | B01, B33 | `final` | `11-flag-final` | 1280 x 720 | none: from frame 0 at the defaults (24, 8, 3) | 8.4 s loop | both: the lit checker flag mid-wave on its pole, left edge still | frame `scene-final-t3.00.png`: left edge pinned, ripple travelling right; compiles in the Lab |
| C02 | B05 | `slide` | `01-slide` | 640 x 360 | shader at 0.22 | to event + 1.5 s | 50 %: square at +40 px (left edge x 296); 85 %: same | left edge 256 to 296 (Lab `01-slide-white`) |
| C03 | B06 | `local` | `01-slide` | 640 x 360 | both squares at 0.52 | to event + 1.5 s | 50 %: both squares not yet moved; 85 %: left +40, right (scale 2.0) +80 | +40 at scale 1.0, +80 at 2.0 (+90 at the Lab's 2.25) |
| C04 | B07 | `squash` | `02-squash` | 640 x 360 | at 0.35 | to event + 1.5 s | both: 192 x 64 px, centred | box 224..415 x 148..211 (Lab `02-squash-white`) |
| C05 | B09 | `lean` | `03-lean` | 640 x 360 | at 0.72 | to event + 1.5 s | 50 %: plain square; 85 %: leaning, bottom edge +50 px | left edge 256 to 306, straight within 0.49 px |
| C06 | B11 | `triptych` | `01-slide`, `02-squash`, `03-lean` | 640 x 360 | all three at 0.12 | to event + 1.5 s | both: slid, squashed and leaned squares | as C02, C04, C05 |
| C07 | B12 | `tilt` | `04-ripple` | 1280 x 720 | at 0.58 | to event + 1.5 s | 50 %: flat flag; 85 %: tilted, right end 24 px lower, edges straight | on the Lab's 128 px sprite the right end goes 116 to 140 (24 px), straight within 0.49 px |
| C08 | B15 | `mesh-recipe` | none (plain mesh, dots) | 1280 x 720 | cuts 1 at 0.6, cuts 3 at 0.8 | whole beat | 50 %: 4 terracotta dots on the square; 85 %: 25 dots | 4, 9, 25 vertices (`verify1.gd`); the five code lines give 25 (`verify12.gd`) |
| C09 | B17 | `pair` | `04-ripple` | 1280 x 720 | both at 0.1 | to event + 1.5 s | both: left flag tilted, right flag rippled | frame `scene-pair-t3.00.png` |
| C10 | B18 | `densities` | `04-ripple` | 1280 x 720 | all three at 0.1 | to event + 1.5 s | both: 4, 10 and 32 pieces rippled, joints visible on the left only | worst gap 10.8, 2.0, 0.35 px (`verify11.gd`, 3x zoom) |
| C11 | B19 | `cut-along` | `04-ripple` | 1280 x 720 | both at 0.1 | to event + 1.5 s | both: two flags that look the same | 0 of 288,000 pixels differ |
| C12 | B20 | `polygon` | `04-ripple` | 1280 x 720 | both at 0.1 | to event + 1.5 s | both: left twisted along diagonal lines, right clean | 64 triangles; one point in 34; longest edge 408 px (`verify5.gd`, `verify8.gd`) |
| C13 | B21 | `travel` | `04-ripple`, then `05-flag-travelling` | 1280 x 720 | 04 from 0; 05 at 0.58 | whole beat | 50 %: static ripple; 85 %: ripple travelling right | fitted clock advances with real time, mean error 0.25 px (`flag_motion.py`) |
| C14 | B22 | `pinned` | `05-flag-travelling`, then `06-flag-pinned` | 1280 x 720 | 05 from 0; 06 at 0.3 | whole beat | both: left end still beside the pole | top-left row y = 276 in every pinned frame; unpinned bobs between 256 and 300 |
| C15 | B23, B26 | `dials-rest` | `07-flag-dials` | 1280 x 720 | none | 8.4 s loop | both: the flag waving at the defaults | compiles; three uniforms; amplitude 0 gives a flat edge |
| C16 | B24 | `sweeps` | `07-flag-dials` | 1280 x 720 | sweeps (smoothstep): amplitude 24-40-0-24 over 0.03 to 0.28; frequency 8-16-2-8 over 0.34 to 0.60; speed 3-8-0-3 over 0.66 to 0.92 | whole beat | 50 %: frequency mid-sweep; 85 %: speed mid-sweep | amplitude 0 is flat (Lab `07-flag-dials-amplitude0`) |
| C17 | B25 | `wind` | `07-flag-dials` | 1280 x 720 | `material.set_shader_parameter("amplitude", 40.0)` at 0.75 | whole beat | 50 %: default waves; 85 %: taller waves | top edge follows the amplitude-24 then the amplitude-40 formula within 1 px (`verify13.gd`) |
| C18 | B29 | Lab still | `08-corner-colors` | Lab sprite, white, default fit scale | none | still PNG | the four-colour blended square | probes 2 px inside: TL (0.02, 0.02, 0.98), TR (0.98, 0.02, 0.02), BL (0.02, 0.98, 0.98), BR (0.98, 0.98, 0.02), mid-top (0.50, 0.02, 0.50), centre (0.50, 0.50, 0.50); Compatibility the same |
| C19 | B30 | `flat-mesh` | `08-corner-colors`, `09-corner-colors-flat` | 1280 x 720 | none | still PNG | left smooth blend, right broken into diagonal tiles | one colour on a four-vertex sprite with flat (Lab `09`) |
| C20 | B32 | `lit` | `06-flag-pinned`, then `10-flag-lit` | 1280 x 720 | 06 from 0; 10 at 0.62 | whole beat | 50 %: flat-looking flag; 85 %: folds darkened where the cloth slopes away | frames `scene-lit-t3.00.png`, `scene-lit-t10.00.png` |
| C21 | B34 | `stripes` | `12-stripes-from-vertex`, `13-stripes-from-fragment` | 1280 x 720 | none | still PNG | left plain grey, right six stripes | left 0.749 at every probe; right 0.58 to 0.92 (Lab) |
| C22 | B35 | `flip` | none | 1280 x 720 | `mesh.size = Vector2(256, -256)` at 0.6 | whole beat | 50 %: mesh upside down beside the upright sprite; 85 %: both upright | eyes below the middle with +size.y, above with -size.y (`verify1.gd`) |
| C23 | B37 | `vertex-two` | `15-position-from-vertex` (top), `14-position-from-fragment` (bottom) | 1280 x 720 | both squares slide x 300 to 1000 over 0.3 to 0.7 | whole beat | 50 %: mid-slide; 85 %: at the right, top gradient unchanged, bottom square changed colour | corner pixel red 0.02 (top) against 0.45 (bottom) in both renderers (Lab) |
| C24 | B38 | `polygon-uv` | `06-flag-pinned` | 1280 x 720 | both at 0.1 | whole beat | both: left a still teal rectangle, right a waving flag | UV (0, 0) without a texture (`verify7.gd`) |
| C25 | B39 | `drawing-only` | `16-slide-far` | 640 x 360 | at 0.3 | to event + 1.5 s | 50 %: picture slid 200 px, grey outline stays; 85 %: same | `get_rect()` unchanged; collision overlaps the node's position only; picture +200 px (`verify9.gd`) |

C18 is the only Lab-only render (`check_shader.sh lab-shaders/08-corner-colors.gdshader --kind sprite --sprite-tex white`, still). Everything else is a custom scene, because it needs a mesh, a polygon, two nodes or a scripted event.

## Terminal run (B40)

Not a render: a real run of the one line, recorded as text for `CCPlainShell`. Create a scratch project whose scene has a `MeshInstance2D` named `Flag` (QuadMesh 384 x 168, subdivide width 31, subdivide depth 7) and a script on the root with `print($Flag.mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX].size())` in `_ready()`; run `godot --path <project> --headless`; paste the **verbatim** output lines (the engine banner, any renderer line, then `297`) into the lane's `lines`. The planning run (`evidence/planning-checks/logs/verify10.log`) printed `297`; the banner lines in the lane are from that machine and must be replaced by the real ones if the build machine prints different ones.

## Editor frames and screenshots

**None.** The narration never points at the editor. (Optional, not needed by any beat: the Inspector's Shader Parameters group showing `amplitude`, `frequency` and `speed`; do not add it without a beat that says it.)

## Not captured on purpose

GPU timing (not needed; no cost claim anywhere in this film). Real-time frame rate (offline capture says nothing about it). The compile error for a varying read in the wrong stage (real but unreadable; FACTCHECK row 50). Any Manim picture: those are drawings with numbers taken from the runs above (B04, B08, B10, B16, B36).

## If a capture disagrees with its verified result

Stop and report; do not edit the shader or the narration. The most likely causes: a different mesh orientation (check `mesh.size` signs), a scene scaled by the harness (VERTEX is local, so a scaled node moves farther), or the harness starting `TIME` at a different value (the film never quotes a `TIME` value).
