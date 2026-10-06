# Headless shader findings: Godot 4.7.2 on macOS, 2026-09-27

## Executive summary

**What this is.** A record of an experiment run before Chapters 6–8 were written: what `godot --headless` can and cannot tell you about shaders, materials and textures.

**Why it exists.** The course forbids opening a visible Godot window during agent work, and a shader's job is to change pixels. The chapters needed to know which shader claims a headless run can check and which ones only a person looking at a screen can check.

**What was found.**

- A headless run uses the dummy renderer, and the dummy renderer still runs Godot's own shader compiler. Syntax errors, type errors, unknown identifiers, wrong-stage built-ins and removed Godot 3 built-ins are all reported.
- The report is lazy. It appears the first time the shader is used, such as on assignment to a material, not when it is loaded. It goes to stderr only. The exit code stays 0.
- Headless runs produce no shader output at all. There is no RenderingDevice and no local RenderingDevice, and a viewport texture reads back as `null`.
- Compute GLSL files compile to SPIR-V at import, but a compile error is stored inside the imported resource and never printed in the import log. One import of 13 crashed.
- The editor's automatic texture detection (Detect 3D, normal-map detect) never fires headless.
- On this Mac, two flag combinations that look headless fall back to the normal windowed display server.

## Setup

- Engine: `Godot Engine v4.7.2.stable.official.ed1daf0bf` (`/opt/homebrew/bin/godot`), macOS (Darwin 25.5).
- Probe project: `headless-probe/`. Its `project.godot` sets feature tags `4.7` and `Forward Plus`. The probes were run twice: first in a scratch folder that another agent also wrote to (its `project.godot` replaced this one), then again in a private folder with exactly the `project.godot` shipped here. The two sets of logs are identical except for object IDs. The logs in `headless-probe/logs/` come from the private run.
- Every command used `--headless` unless the table says otherwise.

## Results

| # | Question | Command (from `headless-probe/`) | Real output (trimmed) | What it means |
|---|---|---|---|---|
| 1 | Does import report a broken `.gdshader`? | `godot --headless --path . --import` | nothing about the four broken shaders; exit 0 | `.gdshader` files are not imported resources. Import is not a shader check. |
| 2 | When does a broken shader report? | `godot --headless --path . --script res://tests/probe_lazy.gd` | `STEP after_load` prints with no error. The error appears at `mat.shader = sh` (`probe_lazy.gd:8`): `SHADER ERROR: Expected a ';'.` then `ERROR: Shader compilation failed. at: shader_set_code (servers/rendering/dummy/storage/material_storage.cpp:192)` | `load()` succeeds on a broken shader. The parser runs on first use. |
| 3 | Which errors are caught? | `probe_load.gd`, `probe_modes.gd` | `Expected a ';'.` / `Invalid assignment of 'vec4' to 'vec3'.` / `Unknown identifier in expression: 'flash_color'.` / `Unknown identifier in expression: 'ALBEDO'.` (a spatial built-in in a `canvas_item` shader) / `SCREEN_TEXTURE has been removed in favor of using hint_screen_texture with a uniform.` | Everything Godot's shader language front end checks. The dummy storage calls `dummy_compiler.compile(...)`, a `ShaderCompiler` (source at commit `ed1daf0bf`). It does not run a GPU driver's compiler, because there is no driver. |
| 4 | Does a scene run fail on a broken shader? | `godot --headless --path . --quit-after 10 res://broken_scene.tscn` | `SHADER ERROR: Expected a ';'.`; exit 0 | "The game runs headless" says nothing about its shaders. Grep logs for `SHADER ERROR`. |
| 5 | What does the uniform list show? | `probe_load.gd` | good shader: `flash_color` type 20 (Color), `flash_amount` type 3 (float), hint 1 (range), `"0.0,1.0,0.001…"`. Broken shaders: `[]` | A non-empty, correct uniform list is machine evidence that the parse succeeded. An empty list is the failure signal a test can assert on. |
| 6 | Can a test read uniform defaults? | `probe_lazy.gd` | `get_shader_parameter("flash_amount")` → `<null>`; `property_get_revert(...)` → `<null>`; `RenderingServer.shader_get_parameter_default(...)` → `<null>` | Defaults live only in the shader text headless. Check them with a text match, and say that is what you did. |
| 7 | Does `hint_range` clamp? | `probe_lazy.gd` | `set_shader_parameter("flash_amount", 7.0)` then get → `7.0` | The hint shapes the Inspector. It does not clamp values set from code. |
| 8 | Do all shader types parse? | `probe_modes.gd`, `probe_blit.gd` | modes spatial 0, canvas_item 1, particles 2, sky 3, fog 4, texture_blit 5. A `hint_screen_texture` sampler does not appear in the uniform list. | All six 4.7 shader types are checkable headless. |
| 9 | Does VisualShader work headless? | `probe_modes.gd` | A graph built in code returns readable `shader_type canvas_item; … uniform float flash_amount; … COLOR.rgb = n_out4p0;` from `.code` | A VisualShader is shader-language text underneath. An agent can read the generated code. |
| 10 | Is there a GPU device? | `probe_rd.gd`, `probe_lazy.gd` | `RS.get_rendering_device=<Object#null>`; `RS.create_local_rendering_device=<Object#null>`; `SubViewport` texture `get_image()` → `ERROR: Parameter "t" is null. at: texture_2d_get (./servers/rendering/dummy/storage/texture_storage.h:110)` and `null` | No compute dispatch and no pixel readback. **Shader output cannot be observed headless on this machine.** |
| 11 | Does the renderer report honestly? | `probe_load.gd` | `RENDERING_METHOD=forward_plus`, `RENDERING_DRIVER=metal`, `VIDEO_ADAPTER=` (empty) | These getters report configuration, not what is running. To detect headless, use `DisplayServer.get_name() == "headless"` or a null rendering device. |
| 12 | Do compute GLSL errors surface? | `godot --headless --path . --import`, then `probe_compute.gd` | good: `SPIRV_BYTES=824`, empty error. Broken: `SPIRV_BYTES=0`, `COMPILE_ERROR=… syntax error, unexpected RIGHT_BRACE, expecting COMMA or SEMICOLON`. Import logs: 13 imports with the broken file present; 12 exited 0 and none of the 12 saved logs contains the GLSL error text; each prints `…/ShaderFile: The function is_visible_in_tree() on this node can only be accessed from either the main thread…` twice. The first import (not saved to a file) ended `handle_crash: Program crashed with signal 11`. | The import compiles GLSL to SPIR-V with no GPU, but you must load the `RDShaderFile` and read `compile_error_compute` to see a failure. Compiled bytecode is not executed-shader evidence. |
| 13 | Does texture detection fire headless? | `detect_probe.tscn` (StandardMaterial3D with `scifi_1_albedo.png` and `scifi_1_normal.png`, in a copy of walker-3d-decals): headless run, re-import, then `godot --headless --editor --path . --quit-after 200 res://detect_probe.tscn` | both `.import` files byte-identical before and after | Detection is driven by renderer callbacks (`_texture_reimport_3d`, `_texture_reimport_normal` in `editor/import/resource_importer_texture.cpp`) that the dummy renderer never calls. An agent-edited material keeps its textures' old import settings until the scene renders in a real editor. |
| 14 | Can a test inspect textures? | `probe_pixels.gd`, `probe_alpha.gd` (in a copy of walker-3d-graphics-settings) | `Image.load_from_file` and `CompressedTexture2D.get_image()` both work: formats, mipmaps and per-texel statistics | Texture data is CPU-side, so headless tests can check imports and pixels. Only the rendered result is off-limits. |
| 15 | What if a test script errors before `quit()`? | `timeout 20 godot --headless --path . --script res://tests/probe_hang.gd` | `SCRIPT ERROR: Cannot call method 'get_name' on a null value.`, then nothing; `timeout` killed it after 20 s (exit 124) | Headless Godot keeps running after a script error. Wrap every test run in `timeout`. |

Agreement with the rest of the course: the Chapter 9 (particles) writer's runs on the same day were reported to show the same split (shader type errors caught headless; capture and readback empty). Nothing in this experiment contradicts that.

## A flag trap: headless is not always headless

These four probe runs (`probe_rd.gd`, about one second each) reported `DISPLAY=macOS` and a real Metal device (`Apple M4 Pro`), not the headless display server:

- `godot --display-driver headless …`
- `godot --display-driver headless --rendering-driver metal …`
- `godot --display-driver headless --rendering-driver vulkan …`
- `godot --headless --rendering-driver metal …`

Godot's command-line documentation describes `--headless` as shorthand for `--display-driver headless --audio-driver Dummy`. On this machine the long form on its own did not stay headless: the headless display driver does not support the project's rendering driver, and Godot fell back to the macOS display server. Each script quit inside `_initialize()`, but the macOS display server had started, so a window may have appeared briefly. This broke the course's no-window rule, it is reported here, and the runs were not repeated. **Use `--headless` exactly, and never add `--rendering-driver` to it.**

## Colour space in 2D (read from source, not observed)

Relevant to Chapter 8's predicted pixel values. In Godot 4.7.2's Compatibility renderer, the canvas material's uniform-buffer upload has no sRGB-to-linear step (`drivers/gles3/storage/material_storage.cpp`, `CanvasMaterialData::update_parameters`). The RD renderers (Forward+ and Mobile) keep two uniform sets per canvas material and use the linear-converted one only when the render target uses HDR (`renderer_canvas_render_rd.cpp`: `render_target_is_using_hdr`). So in default, non-HDR 2D, a `source_color` uniform arrives with the hex values you wrote. This is a reading of the source; no pixel was observed.

## The verification design this forces (used in Chapters 6–8)

Machine evidence, headless:

- The shader parses: a non-empty, correct `get_shader_uniform_list()`, plus a log with no `SHADER ERROR` line.
- The uniforms have the right names, types and hints, and defaults match the spec (checked in the source text).
- The gameplay code drives the uniform correctly: sample the value every frame at several pinned `--fixed-fps` rates, and send real input events.
- Material slots, channels and texture import settings are correct: read the `.import` files, and read the imported texture with `get_image()`.
- Texture data is plausible, for example a normal map's blue channel above 0.5.
- A CPU model of the shader's math at controlled inputs gives predicted pixel values. It is a specification written as arithmetic, not a measurement of the GPU.

Human evidence, on a display:

- The actual look, in the editor or the running game. Use a fixed test scene, controlled inputs (known uniform values, a known background, known lighting), and a screenshot sampled with a colour picker against the predicted values.

## Not tried

- A virtual display on Linux, other GPUs, other operating systems.
- Godot's Movie Maker mode (`--write-movie`), because it is video capture.
- Any run with a visible window, other than the four accidental fallbacks above.
