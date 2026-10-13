# Sources: Lines and Shine

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** The one non-primary source is a third-party work. The film follows its order of ideas and teaches them in new words with new, tested demonstrations; this file records that nothing was copied, that I did not see the video itself, and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every number on screen comes from a run in `evidence/planning-checks/` or from the arithmetic written next to it. The third-party video is described only through the content brief; its creator is not named there, which is an open question for Bear.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable), read 2026-10-13:
  - Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html` (a shader runs on the GPU; `vertex()`, `fragment()`, `light()`).
  - Shading language: `tutorials/shaders/shader_reference/shading_language.html` (uniforms and `set_shader_parameter`, precision, casting rules, float literals).
  - Canvas item shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html` (`COLOR` multiplied by `TEXTURE` at the start of `fragment()`, `UV` range, `TIME`).
  - Built-in shader functions: `tutorials/shaders/shader_reference/shader_functions.html` (`abs`, `sqrt`, `step`, `mix`, `dot`, `radians`, `sin`, `cos`, `tan`, `fract`).
  - ShaderMaterial class reference: `classes/class_shadermaterial.html` (`set_shader_parameter`: "case-sensitive and must match the name of the uniform in the code exactly").
  - Tween class reference: `classes/class_tween.html` (`tween_property`).
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS, Forward+ unless a line says Compatibility. Renderer stated on every pixel value.

## Third-party source followed (not copied, not seen)

- One video of about 14 minutes on drawing a line with a rule in a shader and using it as a shine (as described in `../_godot-shaders-series/briefs/lines-and-shine.md`). **I did not watch or transcribe it**; the brief's own paraphrase is the only form in which it reached this film. The brief names the idea order: slope-intercept form, centring the address, `y - m*x`, `tan` for slope, a distance formula, `step(distance, thickness)`, a white `mix`, a `center` uniform.
- **Not stored.** No transcript or text of the video is in this folder or anywhere in the repository. Every sentence of the narration is new; every demonstration was rebuilt and run.
- **Open for Bear:** the creator's name and address, if you want them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot result on screen is a Shader Lab render or a scene capture of a file in `lab-shaders/`; the scripts and raw logs are in `evidence/planning-checks/` (`run_lab_checks.py` re-runs everything; `measurements.txt` and `lab-results.jsonl` are its output; `verify1.gd` and `run-1-verify1.log` are the GDScript-side check). Failed or surprising runs are kept and labelled in `RESULTS.md`: the first bit-reading attempt that ignored its `--set` options, the step-order probe that I aimed at the wrong pixel, and the tween run that must fail.

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/` and a scratch project for the scene scripts), Python with Pillow for pixel measurements. No paid generation, no model calls.
