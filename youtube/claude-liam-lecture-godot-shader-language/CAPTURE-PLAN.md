# Capture plan: Godot Shader Language

**What this is.** Every Godot render and documentation screenshot the build session must record for this film, with the exact shader file, target, values, duration, renderer and the result already verified. Nothing is recorded yet; the numbers below come from planning runs in `evidence/planning-checks/` (`lab-summary.txt`, `png-analysis.txt`, `pulse-range.txt`).
**Why.** Films show only what was really done and recorded. This is the list of things to really do, written so a medium-effort session can do them without further judgment.
**Found.** Eleven capture items: two clips of the pulsing shader, one dissolve built from two stills, and eight items that are stills (C03 and C10 are a pair of stills each); plus two documentation screenshots, and no editor action. Five beats show the engine's own log instead of a capture: their lines are already in `lanes/` word for word. Nothing needs scripted input, keys or sliders. All stills are of **even width** on purpose (beat B32 depends on it).

Conventions for all captures: render stills as PNG at 1920 × 1080 with the Shader Lab (`lab/check_shader.sh <file> --kind rect --size 1920x1080 --png <out>`; the Lab window clamps to the screen height, so never request 3840 × 2160 from the Lab) and the video at 3840 × 2160 on the SubViewport native-size route (`../_godot-shaders-series/COMPONENT-SPECS.md`, capture harness). Frame rate 30. Renderer: **Forward+** (state it on screen: "Godot 4.7.2 · Forward+"). The Lab stage color is `#D9D5CA`. Offline fixed tick rate: nothing here says anything about real-time frame rate. Output to `brutalist.art/runtime/remotion/public/godot-shader-language/` with the names below.

## Godot renders

| ID | Beat | Shader (in `lab-shaders/`) | Target and setup | Values over time | Length | Verified result to reproduce |
|---|---|---|---|---|---|---|
| C01a | B01 | `01-breathe` | `rect`, full frame, `--set tint=#5FA391` (what the Inspector would set; label "tint set to teal"), live `TIME` | none scripted | video a little longer than the beat's measured audio (about 16 s), 30 fps | Red channel swings between about 0.38 (teal) and 0.90 (pale gray) every 3.2 s (`pulse-range.txt`). With tint unset the file pulses between gray and black, so do not forget the `--set`. **Pose rule:** Gate V samples the 50 % and 85 % frames and fails a pale fill on the cream stage; set `--time-origin t0` so that wave = 0.5 + 0.5 * sin(2 * (t0 + t)) is 0.4 or less at t = 0.5 and 0.85 times the beat's measured audio (search t0 over one period, 3.14 s; for 16.0 s, t0 about 0.98 s gives 0.11 at both) |
| C01b | B40 | `01-breathe` | as C01a, a separate clip | none | about 12 s | Same swing. **Its own `--time-origin`** from B40's measured audio by the same rule (for 11.6 s, t0 about 2.38 s gives 0.20). One origin cannot serve both beats: the best common value leaves the wave at 0.79 at one of the four sample times |
| C02 | B07 | `02-spacing-neat` | `rect`, still | none | still (`spacing.png`) | Corners (0.4118, 0.4118, 0.698), (0.9882, 0.4118, 0.698), (0.4118, 0.9843, 0.698), (0.9882, 0.9843, 0.698). The squeezed, spread and one-line spellings render the same pixels (0 of 230,400 differ at 640 × 360), so one picture serves all three |
| C03 | B08 | `03-comment-on`, `03-comment-off` | `rect`, two stills (`comment-on.png`, `comment-off.png`) | none | stills | On: pastel, as C04. Off: corners (0.0196, 0.0196, 0.502), (0.9804, 0.0196, 0.502), (0.0196, 0.9765, 0.502), (0.9804, 0.9765, 0.502); every pixel differs from On (largest channel difference 102 of 255) |
| C04 | B15 | `05-pastel` | `rect`, still (`pastel.png`) | none | still | Corners (0.4118, 0.4118, 0.702), (0.9882, 0.4118, 0.702), (0.4118, 0.9843, 0.702), (0.9882, 0.9843, 0.702); center (0.698, 0.698, 0.702) |
| C05 | B17 | `05-pastel`, `06-pastel-bgr` | two Lab stills (1920 × 1080) joined by ffmpeg into `pastel-to-bgr.mp4`: 1.8 s hold of the first, 0.7 s dissolve, then a hold of the second to 14 s (re-time so the dissolve starts at about 14 % of the beat) | none | 14 s, 30 fps | Second frame corners (0.702, 0.4118, 0.4118), (0.702, 0.4118, 0.9882), (0.702, 0.9843, 0.4118), (0.702, 0.9843, 0.9882). Both frames are real renders; the dissolve is an edit and is labelled "two real renders, dissolved" |
| C06 | B24 | `10-pass-uv-in` | `rect`, still (`pass-uv.png`) | none | still | Identical to C04 (0 of 230,400 pixels differ) |
| C07 | B27 | `15-overload` | `rect`, still (`overload.png`) | none | still | Left half (0.3686, 0.6392, 0.5686) teal; right half (0.949, 0.8, 0.502) sand |
| C08 | B28, B29 | `16-split-if` | `rect`, still (`split-if.png`) | none | still | Left (0.3686, 0.6392, 0.5686); right (0.949, 0.949, 0.949). The ternary file renders the same pixels, so B29 reuses this picture and says so on screen |
| C09 | B30 | `18-stripes` | `rect`, still (`stripes.png`) | none | still | Five teal stripes on pale (0.949), centered at 0.1, 0.3, 0.5, 0.7, 0.9 of the height (at 640 × 360: rows 25-46, 97-118, 169-190, 241-262, 313-334) |
| C10 | B32 | `19-float-equals`, `20-float-range` | `rect`, two stills at **1920 × 1080 exactly** (`float-equals-1920.png`, `float-range-1920.png`) | none | stills | Equals: NO teal pixel on the middle row (verified at 640, 1280 and 1920 wide; one column lights at some odd widths such as 641 and 1001, none at 321: never use an odd width). Range: 20 teal columns (950 to 969) on the middle row |

Features the harness needs for this film (all in `../_godot-shaders-series/COMPONENT-SPECS.md`): `--set name=value`, still PNG, `--size`, `--time-origin`, two live-`TIME` clips (about 16 s and 12 s). Nothing here needs `--animate`, `--steps`, `--scene`, `--call-at`, keys or a scripted uniform sweep.

## Engine logs shown verbatim (no capture; the lines are already in `lanes/`)

Each is the full engine output of the named file, from `--Main Shader--` through the `at:` line, with trailing spaces trimmed (`run-error-logs.sh`, `evidence/planning-checks/logs/`).

| Beat | Log | Lines on screen |
|---|---|---|
| B06 | `40-err-semicolon.log` | the 7-line excerpt; ring on the marked line (line 5, the closing brace) |
| B11 | `42-err-int-to-float.log`, `43-err-int-plus-float.log` | two 3-line excerpts (header, marked line, message) in one window |
| B18 | `44-err-vec3-to-color.log` | the 8-line excerpt; ring on "'vec4, vec3'" |
| B22 | `47-err-call-before-define.log` | the 8-line excerpt; ring on the message |
| B41 | `57-err-alpha-on-vec3.log` | the 8-line excerpt; ring on the message |

Messages quoted as short labels inside Manim scenes (B21) come from `45-err-return-type.log`. If GATE T flags the dark terminal window, use the cream `ClaudeCodeBeat` card with the same lines.

## Documentation screenshots

| ID | Beat | What | How |
|---|---|---|---|
| D1 | B26 | The Godot 4.7 "Built-in shader functions" page, scrolled to the "Trigonometric functions" table (Return Type, Function, Description; rows radians, degrees, sin, cos, tan), 1600 × 900 at device scale 2.4; the camera pushes in on the `sin(vec_type x)` row | Playwright (BrowserCapture convention), from `https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shader_functions.html`; caption with the capture date. Read 2026-10-13: `vec_type`, `sin(vec_type x)`, "Sine." |
| D2 | B31 | The Godot 4.7 "Shading language" page at "Flow control": the `for` and `while` snippets and the paragraph "Keep in mind that in modern GPUs, an infinite loop can exist and can freeze your application (including editor)"; the camera pushes in on that paragraph | Playwright, from `https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html`; caption with the capture date |

## Editor frames

None are required. The film shows no Inspector, no slider and no editor panel. Two optional upgrades, if the build wants a real editor frame: **the editor driver records Godot's own editor by script, no human click and no recording by hand** (`../_godot-shaders-series/editor-capture/README.md`, sections 5, 7 and 11; one run takes about 20 to 60 seconds and holds the shared Lab lock). `P` below is `../_godot-shaders-series/editor-capture/png/1920x1080/` (native 3456x1944 twins in `png/3456x1944/`). Label any such clip "scripted editor session".

| ID | Beat | What | Nearest existing frames, and how to record the exact one |
|---|---|---|---|
| E1 (optional) | B35 | The Inspector's "Shader Parameters" group for a ShaderMaterial using `01-breathe.gdshader`: `tint` as a color control, `speed` as a number (engine-level fact already verified: `verify1.gd` finds the group "Shader Parameters", `tint` as a Color property) | **Nearest real frames:** `P/godot-shaders/godot-shaders_E3-1_source-color-swatch-next-to-red-slider.png` (a `uniform vec4 tint : source_color` is a color swatch labelled **Tint**, next to a `hint_range` float drawn as a number box with a slider bar, under the group **Shader Parameters**), `godot-shaders_E3-2_color-picker-popup-open.png` (the picker a click on the swatch opens) and `P/textures-and-color/textures-and-color_E2_picked-swatch-and-typed-four-boxes.png` (a hinted vec4 as a swatch, a plain vec4 as four boxes x y z w). **To record the exact one:** copy `editor-capture/state-scripts/final/pilot-E2.json` (ColorRect, `unfold_resource`, `unfold_group shader_parameter/tint`, `mark`), point it at a scratch scene whose ColorRect holds a ShaderMaterial of `01-breathe.gdshader` (the scenes `e3_tint.tscn` and `tc_picker.tscn` in the scratch project are the model); `speed` is a plain float, so its widget (a number box) is not among the recorded frames and should be read from the first run |
| E2 (optional) | B11 | The shader editor's bottom panel with the int-to-float error | **Nearest real frames:** `P/drawing-shapes-with-math/drawing-shapes_E2_shader-editor-error-16-uv-inside-function.png` ("Error at line 3: Unknown identifier in expression: 'UV'.") and `P/local-world-and-screen-space/local-world_E2_shader-editor-error-04-broken-matrix-in-fragment.png` ("Error at line 4: Unknown identifier in expression: 'MODEL_MATRIX'."): the shader editor opens as a bottom panel, the failing line is highlighted red, and one red line under the code reads "Error at line N: " followed by the engine's own message (no column; the status row shows zoom and the cursor's line and column). **To record the exact one:** the driver's `edit_resource_file` step opens `42-err-int-to-float.gdshader` in the Shader Editor (copy the state script of either frame above and change the file); expect the message "Invalid assignment of 'int' to 'float'." (the Lab's wording, `lab-results.jsonl`); that exact frame is not recorded yet |

## Not captured on purpose

No GPU timing and no real-time frame-rate claim anywhere. The infinite loop is never run (it would freeze the machine). The missing-`shader_type` error is not shown: run through the Lab, a shader without it prints no error and is simply not applied (`builtins-results.txt`), so the film cites the documentation for "first line" only.
