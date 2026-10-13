# Sources: Drawing Shapes with Math

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** One source is a third-party video course. The film follows its order of ideas and its habit of working one pixel by hand, and teaches everything in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every picture and number on screen comes from a run in `evidence/planning-checks/`. The third-party course is known to this layout only through the content brief's description in the brief's own words; its transcript was never read or saved. Its creator is not named in anything this film was given, which is an open question for Bear.

## Primary

- Godot 4.7 documentation (`docs.godotengine.org/en/stable`, page header "Godot Engine 4.7 documentation in English"), read 2026-10-13:
  - Built-in functions (`distance`, `length`, `step`, `abs`, `min`, `max`, `clamp`): `tutorials/shaders/shader_reference/shader_functions.html`
  - Shading language (functions, uniforms and hints, `set_shader_parameter`): `tutorials/shaders/shader_reference/shading_language.html`
  - Canvas item shaders (`blend_mix`, the fragment and vertex built-ins `COLOR`, `UV`, `TEXTURE`, the global built-ins such as `TIME`): `tutorials/shaders/shader_reference/canvas_item_shader.html`
  - Introduction to shaders (what a shader is; "The fragment() function runs for every pixel covered by the mesh."): `tutorials/shaders/introduction_to_shaders.html`
  - `EditorSpinSlider` (how the Inspector shows a numeric property; the slider rule): `classes/class_editorspinslider.html`
  - `@GlobalScope`, `PROPERTY_HINT_RANGE` (the hint string `"min,max"` or `"min,max,step"`): `classes/class_@globalscope.html`
  - `ColorRect` (what the node is: "A control that displays a solid color rectangle.", read again 2026-10-13 for B01's caption): `classes/class_colorrect.html`
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS, Metal. Renderer stated on every pixel value; the hard-edged shapes were also rendered on the Compatibility renderer and agree pixel for pixel (`evidence/planning-checks/analysis-crosshair-and-renderers.txt`).
- Method documents of the toolkit: `brutalist.art/docs/MATH-TYPESETTING.md` (the distance arithmetic in B04 is typeset, not typed) and `brutalist.art/docs/EXECUTABLE-EVIDENCE.md` (every number is computed, not drawn).

## Third-party work followed (not copied)

- A long third-party video course on 2D shaders in Godot, its crosshair chapter (about thirty minutes in the course's own running order, per the content brief at `../_godot-shaders-series/briefs/drawing-shapes-with-math.md`). The creator is not named in what this film was given, and Bear has not yet named them.
- **Ideas followed:** the order circle, ring, cross, crosshair; the six crosshair dials (center size, ring distance, ring width, arm length, arm width, arm gap); the habit of plugging numbers in for one pixel and doing the arithmetic by hand; the discovery that a cutout can subtract below zero, which is why the film teaches clamping with `min` and `max`.
- **Not followed:** its explanation of why a circle turns into an oval (it blamed pixels being square and fragments being stretched). That is not the reason: `UV` runs from 0 to 1 on both axes whatever the shape's proportions. B33 says the corrected thing and the measurement behind it (FACTCHECK rows 54 to 56).
- **Not stored.** No transcript, caption file or text of the course was saved to this folder or anywhere in the repository; this layout never saw one. Every sentence in the film is new, every shader is new, every number is new and re-measured.
- **Open for Bear:** the creator's name and the course address, if you want them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot result on screen is a Shader Lab render, a scripted sweep of a Lab render, or an editor capture of a file in `lab-shaders/`; the scripts and the raw logs are in `evidence/planning-checks/`. Failed and inconclusive runs are kept and labelled: `run-b0-verify-b-PARSE-ERROR-first-attempt.log` (a typing mistake in a scratch script), the third check of `run-a-verify-a.log` (the window did not resize; replaced by check 3b of `run-b2-verify-b-final-failing-file.log`), the slow first editor attempt (`run-e1-...SLOW.log`, frames written inside the project), and the compile failure of `lab-shaders/16-uv-inside-function-FAILS.gdshader`, kept on purpose because it is shown on screen. The shader files' SHA-256 sums are in `evidence/planning-checks/shader-sha256.txt`. The first design of five pictures (B18, B19, B25 to B27, replaced after an independent review, not because it was wrong) is kept with its runs in `evidence/planning-checks/superseded-first-design/`.

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/`, plus a scratch project under the session scratchpad), Python 3 with Pillow and NumPy for the pixelwise checks, no paid generation, no model call.
