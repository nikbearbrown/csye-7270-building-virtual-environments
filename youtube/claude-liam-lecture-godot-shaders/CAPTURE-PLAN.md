# Capture plan: Godot Shaders

**What this is.** Every Godot render, editor frame and screenshot the build session must record for this film, with the exact shader file, target, values over time, duration, renderer and the result already verified. Nothing is recorded yet; the numbers below come from planning runs in `evidence/planning-checks/`.
**Why.** Films show only what was really done and recorded. This is the list of things to really do, written so a medium-effort session can do them without further judgment.
**Found.** 17 Godot renders (13 Lab, 4 custom scenes), 3 editor frames (2 shown, 1 evidence only), 1 docs screenshot. All shaders compile and every probe value below was read in a real Godot 4.7.2 window on Forward+. The Shader Lab covers one-shader renders; the custom scenes need small scene scripts (given). Editor frames need an editor driver (section E) or Bear's recording.

Conventions for all captures: 30 fps; render at 3840 × 2160 using the Signal Garden SubViewport native-size route (see `../_godot-shaders-series/COMPONENT-SPECS.md`); the Lab stage color `#D9D5CA`; Forward+ unless stated; offline fixed tick rate (so nothing here says anything about real-time frame rate); every scripted input is logged and labelled "scripted input". Output to `runtime/remotion/public/godot-shaders/` (video or PNG as named in the lane).

## Godot renders

| ID | Beat | Shader (in `lab-shaders/`) | Target and setup | Values over time | Length | Verified result to reproduce |
|---|---|---|---|---|---|---|
| C01 | B01 | `02-hook-wobble` | sprite scene, teal test sprite, scale to fit | no material for 2.0 s, then the shader is assigned (`--material-at 2.0`) | 10 s | wobble visible after 2 s (png `02-hook-wobble.png`) |
| C02 | B06 | `01-gradient` | rect, full frame, still PNG | none | still | red channel 0.0196 / 0.498 / 0.9804 at x = 0.02 / 0.5 / 0.98 |
| C03 | B13 | `03-red` | rect, still PNG | none | still | (1.0, 0.0, 0.0) |
| C03b | B16 | `04-lean` | sprite, checker 128 px at scale 1.0, centered | shader assigned at 1.0 s | 4 s | edge shift 50 px over 128 rows; also render the white-square version for the edge readouts (`lean-edge.txt`: 257, 268, 281, 293, 305 from 256) |
| C04 | B20 | `05-discard-half` | rect, still PNG | none | still | left (0.498, 0.498, 0.2); right = stage (0.851, 0.835, 0.792) |
| C05 | B21 | `13-light-count` | custom scene (script of `verify4.gd`): CanvasModulate black; Sprite2D 100 px white; PointLight2D (white 128 px texture, texture_scale 4, energy 1) added at 1.0, 2.5, 4.0 s | lights 1, 2, 3 | 6 s | centre red channel 0.2, 0.4, 0.6 (and 0.0 before any light) |
| C06a | B26 | `06-dial` | rect, still | default red 0.5 | still | (0.502, 0.451, 0.451) |
| C07 | B28 | `07-mixer` | rect | red 0 to 1 over 0 to 2 s, then green 2 to 4 s, then blue 4 to 6 s (`--animate` sequence) | 6 s | at red 1, green 0.5, blue 0: (1.0, 0.502, 0.0) |
| C09 | B31 | `06-dial` | custom scene: ColorRect named `Rect`, script calls `$Rect.material.set_shader_parameter("red", 0.9)` at 1.0 s | red 0.5 then 0.9 | 3 s | 0.502 then 0.898 |
| C10 | B32 | `06-dial` | as C09 | `"rd"` = 0.9 at 1.0 s (no change); `"red"` = 0.9 at 2.2 s (changes) | 3.5 s | 0.2 stays 0.2 after the typo (`verify3.gd` G); no error in the log |
| C11 | B33 | `06-dial` | as C09 | `set_shader_parameter("red", 0.0)` first, then `tween_property(..., "shader_parameter/red", 1.0, 2.0)` | 3 s | 0.0, 0.49 at 0.25 s, 1.0 (`verify3.gd` H) |
| C12 | B37 | `08-uv-colors` | rect, still | none | still | corners (0.0196, 0.0196, 0), (0.98, 0.02, 0), (0.02, 0.98, 0), (0.98, 0.98, 0) |
| C13 | B38 | `09-uv-fade` | sprite, white 128 px, scale to fit, still | none | still | 0.851 (stage) at x = 0.05; 0.859 at 0.30; 0.992 at 0.70 |
| C14 | B39 | `10-pulse` | rect | live `TIME` | 4 s | the green channel moves between about 0.69 and 0.99 in half a second (two probes) |
| C15 | B40 | `11-time-bar` | custom scene: two ColorRects side by side, the second added at 3.0 s | live `TIME` | 6 s | both bars at the same height when the second appears |
| C16 | B42 | `12-iris` | sprite, checker 128 px, scale to fit | radius 0.0 to 0.8 over 3 s | 3 s | radius 0.0: centre = stage; 0.3: centre cream, corner hidden; 0.8: everything visible |
| C17 | B43 | `12-iris` | custom scene: the script shown on screen on the scene root; the harness pushes one physical key event at 1.0 s (logged) | `_ready` sets radius 0.0; the key tweens to 0.8 in 1.5 s | 4 s | centre stage color before the key, sprite color (0.373, 0.639, 0.569 in the scratch run) after (`verify5.gd` 5b) |

Harness features this list needs (all in `../_godot-shaders-series/COMPONENT-SPECS.md`): `--material-at SECONDS`, `--animate name:from:to` (and a sequence form for C07), a scene-script option for the custom scenes (C05, C09 to C11, C15, C17), scripted key events, PNG-sequence output then ffmpeg to MP4.

## Editor frames (Godot's own editor, never drawn from memory)

Method (proven 2026-10-09): `godot --editor --path <scratch copy> <scene> --write-movie out/f.png --fixed-fps 30 --quit-after N`, take a frame; set the project's window override to 1920 × 1080. Always a scratch copy. To get the Inspector showing the right object, add a 15-line `EditorPlugin` to the scratch copy that, after the scene loads, calls `EditorInterface.edit_node(node)` or `EditorInterface.edit_resource(material)` and scrolls the Inspector. If that does not work in one sitting, Bear records these three clips (one script for the whole series is gathered in `RECORDING-SESSION.md`).

| ID | Beat | Frames | Verifies |
|---|---|---|---|
| E1 | B10 | four states of a Sprite2D's Inspector: Material empty; ShaderMaterial in the slot; a Shader in its slot; the shader editor open | FACTCHECK row 14 (the click path). **DONE by script**: `_godot-shaders-series/editor-capture/png/1920x1080/godot-shaders/godot-shaders_E1-*.png` (also the dropdown and Create Shader dialog frames) |
| E2 | B27 | the ShaderMaterial's Shader Parameters group with `red` saved at 0.2, 0.5, 0.9 (value stored in the scene file) | rows 38, 39 (group label, slider). **DONE by script**: `godot-shaders_E2-2_red-0.2.png`, `E2-3_red-0.5-after-0.2.png`, `E2-4_red-0.9.png` |
| E3 | evidence only | a `source_color` uniform in the Inspector | row 39 (color picker); not shown in this film. **DONE by script**: `godot-shaders_E3-1_source-color-swatch-next-to-red-slider.png`, `E3-2_color-picker-popup-open.png` |

## Screenshot

| ID | Beat | What | How |
|---|---|---|---|
| D1 | B11 | The Godot 4.7 "Shading language" page, 1600 × 900 at device scale 2.4, from `https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html`; the camera pushes in on "similar to GLSL ES 3.0" | Playwright (BrowserCapture convention); caption with the capture date |

## Not captured on purpose

No GPU timing (unreadable on this setup, FACTCHECK row 12). No real-time frame-rate claim anywhere.
