# Sources: Trigonometry for Shaders

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** Two of the sources are third-party works. The film follows their order of ideas and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every number on screen comes from a run or a derivation in `evidence/planning-checks/`. The two third-party sources are known to this layout only through the series brief's description, and their creators are not named there: an open question for Bear.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable), read 2026-10-13; exact quotes are in `evidence/planning-checks/docs-quotes.txt`:
  - Vector2 class reference: `classes/class_vector2.html` (`from_angle()`, `angle()`, `DOWN`; anchor `#class-vector2-method-from-angle`). Shown on screen in B08.
  - CanvasItem shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html` (Global built-ins: `PI`, `TAU`, `E`, `TIME`; `UV`; `COLOR`; anchor `#global-built-ins`).
  - Built-in shader functions: `tutorials/shaders/shader_reference/shader_functions.html` (`sin`, `cos`, `tan`, both `atan` forms, `radians`, `degrees`, `length`, `distance`, `fract`, `mix`; anchors `#shader-func-atan2` (the two-argument entry), `#shader-func-atan` (the one-argument entry), `#shader-func-sin`, `#shader-func-radians`). Shown on screen in B33.
  - Matrices and transforms: `tutorials/math/matrices_and_transforms.html` (y points down in 2D, rotation is clockwise, all rotations are radians).
  - Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html` (`fragment()` runs for every pixel covered by the mesh).
  - Shading language: `tutorials/shaders/shader_reference/shading_language.html` (uniforms cannot be written from the shader). It does **not** list `PI`, `TAU` or `E`.
- Khronos, OpenGL ES 3 reference page for `atan`: registry.khronos.org/OpenGL-Refpages/es3.0/html/atan.xhtml, read 2026-10-13 (a second source for the range minus pi to pi and for "undefined if x = 0").
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS 26.5.1. Renderer stated on every capture; plain-colour shaders were also read in Compatibility and match.
- The series' own files: `../_godot-shaders-series/GLOSSARY.md` (the wording of terms), `COMPONENT-SPECS.md` (what the build makes), `lab/` (the Shader Lab).

## Third-party sources followed (not copied)

- **A.** The trigonometry and orbit chapters of a long third-party course on 2D shaders in Godot (the brief counts about 27 minutes). **B.** A short third-party introduction to Godot shaders, for its clock-hand reveal. Neither creator is named in the brief; Bear has not yet named them.
- **Not stored.** No transcript of either was saved to this folder or anywhere in the repository, and none was in this layout's inputs; the brief's own description (`../_godot-shaders-series/briefs/trigonometry-for-shaders.md`) is the only account of them used. No sentence was reused. The coverage map in `ACTS.md` paraphrases which ideas appear where.
- **Ideas followed, rebuilt in new words with new demonstrations and new numbers:** the right triangle and its three ratios with the memory trick; that the ratio depends only on the angle; sine and cosine as the across and up of a point on a circle; radians; centering the address with `UV * 2.0 - 1.0`; a planet and a moon (the film adds a meteor) placed with cosine and sine of an angle driven by `TIME`; reversing by negating the angle; the arc tangent clock-hand reveal compared with a growing sweep value.
- **Open for Bear:** the creators' names and URLs, if you want them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot picture is a Shader Lab render of a file in `lab-shaders/`; scripts, raw logs, frames and the batch measurements are in `evidence/planning-checks/` (`RESULTS.md` lists them). The runs that did not go straight are kept and described there: the first Lab runner was stopped while it queued (no reading from it was used), and the first flower shape was redrawn after looking at it.

## Tools used (all free)

Godot 4.7.2 (the series' Shader Lab, plus a scratch project for the one-process batch), Python with Pillow and NumPy for pixel measurements, a web fetch of the documentation pages. No paid generation, no voice engine, no render.
