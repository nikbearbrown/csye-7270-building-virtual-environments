# Shot list: Godot Shaders

**What this is.** One row per body beat: what the sentence is about, the picture chosen, the lane that came second, and why this one won. Every beat was auditioned against at least one other lane.

**Why.** The lecture skill's BEST-BEAT LAW: no lane is the default and none has a quota; the picture whose motion is the claim wins. A reviewer can disagree with any row without reading code.

**Found.** 43 body beats. Lane histogram: manim 18, capture 17, remotion 6, editor 2. Every Godot render shown is a Shader Lab or editor capture of a tested file in `lab-shaders/`. Five things must be built or recorded first (below).

## Must exist before the build

1. **`ShaderLab`** Remotion component (spec: `../_godot-shaders-series/COMPONENT-SPECS.md`). 2. **`shader_kit.py`** Manim helpers (same file). 3. **Capture harness** `lab/capture.gd` + `capture_shader.sh` (same file). 4. **Editor frames E1, E2** (same file, section on capturing the editor; see `CAPTURE-PLAN.md`). 5. **Docs screenshot** for B09 via Playwright.

## Rows

| beat | about | lane picked | runner-up | why this one wins | evidence / capture |
|---|---|---|---|---|---|
| B01 | a game that works but looks flat | capture · ShaderLab | manim drawing of a flat versus lively sprite | A real render is the honest picture of 'looks flat' versus 'looks alive'; a drawing would only claim it. | Lab render (C01); shader compiled in Lab |
| B02 | what a shader is; what game code vs shader decide | manim · B02_WhatAndWhere | DesignPipelineClaim, show-tell isometric | A two-box handoff is the whole claim; an icon that visibly changes on arrival says it with motion. | Manim only (shader_kit objects) |
| B03 | CPU as a few fast workers, GPU as a crowd | manim · B03_ManyWorkers | isometric workers on a conveyor (show-tell) | A grid filled one cell at a time versus all at once is the CPU/GPU difference, as motion. | Manim only (shader_kit objects) |
| B04 | the slow way: a GDScript loop over every pixel | remotion · LectureCodeTrace | CCPlainShell | LectureCodeTrace's paced line focus matches the sentence; the shell has no per-line cue. | verify.gd (naive loop, run 2026-10-13) |
| B05 | 55 ms against a 16.7 ms frame | manim · B05_FrameBudget | LectureEvidenceTable | A bar crossing a line shows 'over budget'; a table only lists the numbers. | verify.gd D (53.8 and 58.4 ms) and run 2 |
| B06 | the shader way: one line describes one pixel | capture · ShaderLab | LectureCodeTrace alone | Code and its result side by side is the claim: one line, the whole picture. | Lab probes 01-gradient |
| B07 | what the shader way cost the processor | manim · B07_HandOver | LectureEvidenceTable, two rows | A handoff arrow with a speck of a cost label shows the idea; the grey note keeps the claim honest. | verify2.gd E (0.035 to 0.038 ms CPU; GPU timer returned 0) |
| B08 | the flip: describe one pixel, run it everywhere | manim · B08_OnePixelThenAll | ShaderLab | This is the film's central claim; only a grid shows 'one rule, every pixel' at a glance. | Manim only (shader_kit objects) |
| B11 | Godot's shader language, in the docs | remotion · BrowserCapture | manim: GDScript line beside a shader line | The language claim is a documentation claim; the documentation itself is the evidence (SHOW-THE-THING). | Playwright capture of the live docs page (1600x900 at 2.4x) at build time; read 2026-10-13: 'similar to GLSL ES 3.0' |
| B09 | node, ShaderMaterial, Shader | manim · B09_ThreeBoxes | DesignPipelineClaim, show-tell isometric | Three nested things is a structure with a shape; a drawn chain with a travelling dot is clearer than prose. | Manim only (shader_kit objects) |
| B10 | the editor clicks that attach a shader | editor · ShaderLab | GodotDevWorkbench (labelled reconstruction) | Real editor frames are the rung-1 SHOW-THE-THING answer; the reconstruction is the labelled fallback. | Editor capture E1 (recorded by script: _godot-shaders-series/editor-capture/png/1920x1080/godot-shaders/) |
| B12 | the first line: shader types | manim · B12_TwoWorlds | LectureEvidenceTable | Two worlds side by side, each with its own first line, is the contrast the sentence names. | Manim only (shader_kit objects) |
| B13 | the smallest working shader | capture · ShaderLab | LectureCodeTrace alone | The whole shader fits on screen with its result; nothing else teaches it faster. | Lab probe 03-red |
| B14 | vertex, fragment, light: the engine calls them | remotion · LectureCodeTrace | manim | The skeleton is real code; paced line focus is exactly 'here are the three'. | lab-shaders/14-skeleton.gdshader compiles in the Lab |
| B15 | vertex runs once per corner; a rectangle has four | manim · B15_FourCorners | ShaderLab | Four dots flashing in turn is the literal meaning of 'once for each vertex'. | Manim only (shader_kit objects) |
| B16 | a real vertex() leaning a rectangle by fifty pixels | capture · ShaderLab | manim | A real shear measured to the pixel; a drawing could only illustrate it. | Lab + analyze-lean.py (shift 50 px over 128 rows) |
| B17 | the GPU fills between corners; even steps | manim · B17_EvenSteps | ShaderLab with readouts | The even spacing of five real measurements is the proof that nothing was calculated between the corners. | evidence/planning-checks/lean-edge.txt (edge x = 257, 268, 281, 293, 305 from 256) |
| B18 | fragment runs once per covered pixel | manim · B18_FillIn | ShaderLab | The covered-cell grid is the only way to see 'each pixel the shape covers'. | Manim only (shader_kit objects) |
| B19 | pixel shader and fragment shader are two names | manim · B19_TwoNames | LectureEvidenceTable | Two names for one thing, and a pixel-to-be travelling to a pixel, are both motions. | Manim only (shader_kit objects) |
| B20 | discard: a fragment that never becomes a pixel | capture · ShaderLab | manim | A real render with half the shape gone, and the code that did it. | Lab probes 05-discard |
| B21 | light() runs once per light; an empty one replaces the default | capture · ShaderLab | manim | Three measured steps (0.2, 0.4, 0.6) prove 'once per light, and the results add' better than a sentence. | verify4.gd run 4b (0.2, 0.4, 0.6) |
| B22 | the fixed order: corners, fill, colors | manim · B22_Order | DesignPipelineClaim, show-tell isometric | A token moving forward through three stages is the order of work. | Manim only (shader_kit objects) |
| B23 | built-ins: values handed in and out | manim · B23_FunctionBox | LectureEvidenceTable | Inputs arriving and an output leaving makes 'values handed in and out' literal. | Manim only (shader_kit objects) |
| B24 | the three functions in one table | remotion · LectureEvidenceTable | manim | A summary of three parallel facts is exactly what the table component is for. | Run C, verify4.gd, docs |
| B25 | the shader is out of reach of the game | manim · B25_OutOfReach | LectureCodeTrace | The problem is 'no way through'; a pane of glass is the picture of it. | Manim only (shader_kit objects) |
| B26 | a uniform declared outside the functions | capture · ShaderLab | LectureCodeTrace alone | Declaration and use side by side with the result. | Lab probes 06-dial |
| B27 | the uniform becomes a slider in the Inspector | editor · ShaderLab | ShaderLab video of the Lab render with the same values | Real editor frames are the strongest evidence that a slider appears. | Editor capture E2 (recorded by script: _godot-shaders-series/editor-capture/png/1920x1080/godot-shaders/) |
| B28 | three uniforms make a color mixer | capture · ShaderLab | ShaderLab stills | Motion of the color under three sweeps is the point. | Lab probe 07-mixer |
| B29 | hints: how the editor shows a uniform | remotion · LectureEvidenceTable | editor frames | Two facts in two rows; the real widgets already appeared in the previous editor beat. | docs hint list; E2 |
| B30 | a hint does not clamp a value set from code | manim · B30_NoClamp | ShaderLab | An arrow leaving the end of a slider is the literal picture of 'does not clamp'. | verify3.gd F (stored 7.0, run 2026-10-13) |
| B31 | set_shader_parameter from the game | capture · ShaderLab | LectureCodeTrace | The cause (one line) and the effect (the color) together. | verify3.gd G (correct name 0.898) |
| B32 | a misspelled uniform name is a silent no-op | capture · ShaderLab | LectureCodeTrace | A non-event is hard to show; the two-line contrast with a held frame makes it visible. | verify3.gd G |
| B33 | tween a uniform (after setting its start) | capture · ShaderLab | ShaderLab stills | A smooth sweep is the claim: 'the shader follows, every frame'. | verify3.gd H; run-5a (failure) and run-5b (fix) |
| B34 | uniform: the same for every pixel, unlike the pixel's address | manim · B34_SameForAll | LectureEvidenceTable | A fan of lines from one dial versus a different label in each cell is the contrast itself. | Manim only (shader_kit objects) |
| B35 | uniform and built-ins compared | remotion · LectureEvidenceTable | manim | A short comparison table is the right shape; the previous beat already drew the picture. | docs; run B (UV), A2 (TIME) |
| B36 | UV: the pixel's address | manim · B36_Address | ShaderLab | Address is a position; a dot with a live label is the clearest picture of it. | run B: UV.y about 0.04 at the top, 0.96 at the bottom (canvas_item) |
| B37 | UV used as a color | capture · ShaderLab | manim | The picture itself is the evidence that the address became a color. | Lab probes 08-uv-colors |
| B38 | UV used as a fade | capture · ShaderLab | manim | A fade is best seen on the real thing, next to the one line that makes it. | Lab probes 09-uv-fade |
| B39 | TIME inside a sine makes a pulse | capture · ShaderLab | manim sine plot | A real pulse with its value riding a ramp shows both the result and the number behind it. | Lab probes 10-pulse-a/b |
| B40 | TIME is one clock: a node added later sees time already gone | capture · ShaderLab | manim timeline | A late node appearing already full is the surprising fact; the capture shows it as it happened (the run is the proof). | verify2.gd A2 (12 stripes on both) |
| B41 | one-time effects need a uniform you drive | manim · B41_ClockVsDial | ShaderLab | The relation between a global clock and an event-started dial is a timeline. | Manim only (shader_kit objects) |
| B42 | the iris: distance, discard and a radius uniform | capture · ShaderLab | manim | The film's payoff: all of the earlier ideas working together, shown on the real thing. | Lab probes 12-iris-0.0/0.3/0.8 |
| B43 | the game drives the radius on a key press | capture · ShaderLab | ShaderLab with the earlier capture | The shader holds the rule and the game holds the moment: cause (key) and effect (iris) together. | verify5.gd run 5b (key path and tween verified) |
