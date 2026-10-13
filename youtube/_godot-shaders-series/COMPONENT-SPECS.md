# Components and tools the shader films need built (once, shared)

**What this is.** The few pieces that do not exist yet and that almost every shader film leans on: one Remotion component, one Manim helper kit, one capture harness, and the way to capture Godot's own editor.
**Why.** The lecture skill says a miss is a build, not a slate. Building each piece once, in the first film's build, means the other nineteen reuse it. Layout agents may cite these names in lanes; the build session creates them first.
**Found.** The library already has what the rest need: `LectureCodeTrace` (code with paced line focus), `LectureEvidenceTable`, `CCPlainShell`, `ClaudeCodeBeat`, `GodotDevWorkbench` (a labelled reconstruction of the Godot editor), `BrowserCapture` (a still of a real web page), `DesignPipelineClaim` (flows, with a show-tell isometric style) and `LibraryIconRow`. What is missing is anything that plays a *moving* Godot render next to its code. Everything below is free to build.

Headings of the form `### Name (NEW)` are read by `lint_series.py` as "this component is planned"; a lane may cite it.

---

### ShaderLab (NEW)

A Remotion composition (16:9, 4K design, registered in `Root.tsx`, then `./art scene-index`). Shows **shader code and its real result together**. The result is a video (or still) captured from the Shader Lab or the Godot editor, shown in a framed window on the cream Claude stage; the tool inside the window keeps its own look (SHOW-THE-THING).

Props (zod):

| Prop | Type | Meaning |
|---|---|---|
| `title` | string, optional | label top-left (Title Case serif, ≤ 40 chars); the first beat of an act carries the act title here |
| `layout` | `'side'`, `'stack'`, `'video'` or `'code'` (all four must work) | code left + result right; result above + code below; result only; code only |
| `code` | string | the real `.gdshader` text, ≤ 14 lines, shown in monospace ≥ 44 px at 4K design, line numbers |
| `codeFile` | string | provenance caption, e.g. `lab-shaders/01-dial.gdshader` |
| `cues` | `{at: number 0..1, lines: number[], label?: string}[]` | which line(s) are highlighted when (a cue may target a **blank line**: the highlight and its label are drawn on it); `at` is a fraction of the beat; no cue starts inside 45 to 55 %. **`label` must be rendered** (it is how a film defines a word on the very line that uses it, e.g. `floor: rounds down`): a short definition tag attached to the highlighted line(s), at most 60 characters, GATE T type floors apply, ink on a pale ground, never terracotta text. The Patterns film uses about ten per beat sheet; the Glossary's small math words are defined this way |
| `video` | string (staticFile path) | the capture; MP4 at the film's frame rate, or a PNG for a still |
| `videoLabel` | string | e.g. `Godot 4.7.2 · scripted run · recorded 2026-10-14` |
| `readouts` | `{at, text, x, y}[]` | short value labels placed on the result (≤ 3 words each; "x = 300", "0.5"). A readout at the same `x, y` **replaces** the earlier one (a changing number), it does not stack. `x, y` are fractions of the result window and anchor the readout pill's centre |
| `rings` | `{at, box: [x0,y0,x1,y1]}[]` | one terracotta ring (grey backing) around a part of the result |
| `ramp` | `{at, from, to, period?}` optional (the marker moves linearly; a sine-shaped path is not supported, so a film that needs one draws it in Manim) | a thin 0→1 strip under the result with a marker at the probed value; `period` (seconds, optional) makes the marker repeat from `from` to `to` every period, for a looping sweep |
| `caption` | string | one line under the result: either the source/provenance line or a one-line definition (at most 80 characters, GATE T floors apply); the Lines film uses it for definitions |
| `durationSeconds` | number | the measured audio |

The `stack` layout must also work with a **short excerpt** of one to three lines under the result (no empty gap, no stretched card); several films quote only the one line that matters.

`LectureCodeTrace`'s line focus can only move **downward**; a beat whose focus goes back up the code uses `ShaderLab`'s `code` layout instead.

Capacity: code up to 14 lines. (`LectureCodeTrace`, the registered code card, holds only about 10 lines at 4K: its card is 700 px high at 42 px per line. Layouts using it must keep code to 10 lines; `lint_series.py` checks.)

The result window follows the capture's aspect (16:9 by default; a square capture gets a square window), and the `video` layout carries the title, caption and readouts like the others.

Rules it must obey: GATE T type floors at 4K; the 45–55 % frame is a settled still; the capture is never cropped past the window; ring backed in grey, never ink over text; terracotta is never text.

### ShaderLab916 is **not** needed. Portrait is out of scope.

---

### shader_kit.py (NEW, Manim helper kit, pasted into `scenes.py` by `assemble_scenes.py` like the show-tell `iso_kit.py`)

Reusable drawings so twenty films look like one series (ONE CAST PER ACT, ONE LOOK). All in the Claude palette; terracotta only as dots, rings and small sparks, never as text.

- `ramp_strip(width, label0="0", label1="1")`: a horizontal bar of values from 0 to 1, **drawn as a row of 48 to 64 narrow tiles with gaps between them** (measured with the toolkit's own blob detector: a continuous strip of grays 27 to 113 of 255 forming one compact blob of aspect 1.5 to 15 is read by GATE T as a text-like run; separate tiles with gaps are not; pure black, white, stage grey, teal, cream and gold are outside that band), with end labels; `ramp_marker(strip, v)` a terracotta dot riding it. **The signature object of the series**: "a ramp goes in, a function reshapes it, a ramp comes out."
- `pixel_grid(cols, rows, cell)`: a grid of outline-only cells (no fill behind text) with `highlight(cells)`.
- `plot(fn, x_range, y_range, size)`: axes + curve + a travelling dot; used for every function in the math film.
- `vertex_quad(w, h)`: a rectangle with four terracotta corner dots; `fill_in(quad)` tints the covered pixel-grid cells to show the GPU filling between corners.
- `uv_square(n)`: a square with 0→1 axes, Y pointing down, a draggable dot and its (u, v) label.
- `worker_grid(rows, cols)` and `worker_one()`: the many-small-workers vs one-fast-worker picture used for CPU vs GPU.
- `code_card(text, lines_to_mark)`: monospace Menlo ≥ 32, explicit coordinates (Pango may drop single spaces: LOOK at the still).

**Promotion rule.** Several films define small Manim helpers of their own (for example `world_window_scene`, `origin_marker`, `address_tag`, `matrix_table`, `plot_with_strip`, `number_line`, `vec_arrow`, `chip`). The build that needs a helper a previous build already wrote copies it into `shader_kit.py` instead of writing a second one; `grep -rn "def <name>" claude-liam-lecture-*/` first.

Follow the Manim laws in `BUILDER-BRIEF-COMMON.md` (Gate A: at least one new non-text shape after the first frame; midpoint rule; no fills behind text).

### Capture harness (NEW), extends `lab/runner.gd`

`lab/capture.gd` + `lab/capture_shader.sh`: render a shader (and optional scripted uniform sweeps or key presses) to a PNG sequence at the film's frame rate, then `ffmpeg` to MP4. Required options: `--frames N --fps 30 --out DIR`, `--animate name:t0:v0,t1:v1,...` (a **piecewise-linear schedule** of a uniform over time: hold, reset and rise are all just breakpoints; also accept the simple `name:from:to` form for a linear sweep across the frames), `--steps name:t0:v0,t1:v1,...` (a **stepped schedule**: the value is v0 from t0 until t1, then v1, and so on, with no ramp between; the frame at each time already shows the new value; used where a value is held for a time each, e.g. block size 1, 2, 4, 8, 16), `--texture KIND_OR_PATH` (a registry of named test textures plus any PNG path; the Textures and Color film adds `tiny_f`, `swatches`, `ramp_grey`, `burn_ramp_tex`, `noise2d`, with `--rect-color`, `--modulate`, `--hdr2d` and `--size`; its CAPTURE-PLAN section H and the verified reference `evidence/planning-checks/runner_plus.gd` define them), `--scene PATH.gd` (a scene script builds the captured content; the Matrices film uses one for a drawn "card" texture at 1024 px with pixel-valued uniforms multiplied by 8, verified to give identical geometry, instead of the default single shape; used for **two panels side by side**, e.g. `evidence/planning-checks/two_panels.gd` in the Lines film, where each panel takes its own `--animate panel.name:...` schedule), `--call-at SECONDS:method` (call a method on the scene script at a time), `--time-origin SECONDS` (offset the shader clock so `TIME` has a chosen value at a chosen frame, for a loop that is on a given pose at 50 %), keyframes may be given as fractions of the clip (`--length SECONDS` converts them), stills as PNG, `--material-at SECONDS[:SHADER_B]` (assign a ShaderMaterial at that time: with no `SHADER_B` it applies the run's shader to a node that started with no material, for the "before and after" beats; with `SHADER_B` it swaps shader A for shader B mid-clip; a harness that cannot swap renders the two parts and joins them with `ffmpeg`, which the capture plan may name as its fallback), `--set-at SECONDS:name=value`, `--keys file.json` (scripted physical-key events, logged), `--renderer`. Use the **SubViewport native-size route** proven for Signal Garden (capture a 3840×2160 SubViewport over a 1280×720 logical canvas) for shaders that work in the node's own units (`UV`, `VERTEX` in the vertex stage). **Shaders that read window pixels (`FRAGCOORD`, `LIGHT_POSITION`, `LIGHT_VERTEX`, `SCREEN_PIXEL_SIZE`) must be captured at the size they will be shown, 1920×1080 at scale 1**, because the SubViewport route changes their numbers (measured in the Light Shaders layout); the capture plan says which route each capture uses and note these proven traps: `content_scale_size` is Window-only so a SubViewport needs a small shim; Movie Maker `--resolution` is clamped to the window; awaiting `frame_post_draw` can stall. **Drive a window-free capture loop like this (SubViewports layout, run-16b and 16c):** `RenderingServer.render_loop_enabled = false`, then per step `await process_frame` and `RenderingServer.force_draw(false, 1.0 / 30.0)`. Shader `TIME` advances only inside a draw, by that draw's frame step: regular draws pass 1/30, but `force_draw(false)` with no step passes 0, so the older advice "`process_frame` + `force_draw(false)`" leaves `TIME` frozen on every skipped frame. With the step given, `TIME` rises exactly 1.0 per 30 steps. **Movie Maker still needs the window on top** (`WINDOW_FLAG_ALWAYS_ON_TOP`): a covered window is drawn on only some frames (137, 136, 108, 125 of 299 seen; 73 distinct of 400 in one recording), `Update Mode Once` is spent late and Movie Maker repeats frames; with always-on-top 400 of 400 frames differed in five runs. Frame 0 of a SubViewport recording lacks the pictures in 14 of 22 scenes: wait a few frames before the first captured one; keys must be released between runs; capture offline at a fixed tick rate and say so (it proves nothing about real-time frame rate). Label scripted input "scripted input".

### Capturing Godot's own editor (PROVEN 2026-10-13)

**Route: the editor driver.** An `EditorPlugin` inside the real Godot 4.7.2 editor runs a JSON state script (open a scene, select a node, inspect a resource, open a dropdown, pick a menu entry, set a property, open the Create Shader dialog, ...) while Movie Maker records the editor window; each state is a named still. 62 real states (40 for four films, 22 for the renderer path) were recorded with no human click and no driver errors. **Read `editor-capture/README.md` before recording anything**: it has the driver, the scratch project, the launcher (`capture_editor_states.sh`, which takes the shared Lab lock), the state scripts, the finished frames (`png/1920x1080/<film>/`, native `png/3456x1944/<film>/`), the true on-screen labels, and the traps.

Conditions, all handled by the launcher and its settings files:
- Popups and dialogs are recorded **only** with the editor setting `interface/editor/display/single_window_mode` on; with it off (the factory default) each menu and dialog is its own OS window and Movie Maker never sees it.
- The renderer selector in the editor's upper right is **hidden by default in 4.7.2** (`interface/editor/appearance/show_renderer_selector` is false); do not write "the renderer's name sits in the upper right corner" unless the setting is on and the film says so.
- Window 3456x1944 resampled to a 1920x1080 movie (a maximized window with a 1080p movie is a centre crop that loses the title bar and bottom strip). The movie file number is `Engine.get_process_frames()`, not `get_frames_drawn()`.
- Movie Maker records no mouse pointer. Label every such clip "scripted editor session". A visible cursor needs an optional human take (README section 9); nothing in the series requires one.
- Always on a **scratch copy**, never on a project Bear is working in.

True labels the films must use (from the frames): the Material slot's menu has a heading **New** then **CanvasItemMaterial**, **ShaderMaterial**; the Shader slot (inside the ShaderMaterial view) offers **New Shader...**; the **Create Shader** dialog starts on Mode **Spatial** (pick **Canvas Item** for 2D); uniforms sit under **Shader Parameters** with the property name in Title Case, underscores becoming spaces (`red` is **Red**, `body_color` is **Body Color**, `ring_distance` is **Ring Distance**); a `hint_range` float is a number box with a slider bar; a `source_color` vec4 is a color swatch that opens a picker (a `vec3 : source_color` too, its picker has no A row); a plain vec4 is four boxes x y z w. Resource-picker menus show a heading **New** then bare class names, never "New NoiseTexture2D"; the NoiseTexture2D view has Width, Height, Noise and a **Seamless** checkbox but no preview, and the clouds show in the FastNoiseLite view one click deeper.

Fallback only if a state cannot be scripted: `GodotDevWorkbench` reconstruction, labelled "reconstruction, not a live session". Never draw an Inspector that claims to be live.
