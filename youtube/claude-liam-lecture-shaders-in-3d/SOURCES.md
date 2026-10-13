# Sources: Shaders in 3D

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** This film is not cut from either third-party source: the brief says so, and a check of both confirmed that neither teaches three-D. Its facts come from Godot's own documentation and from runs of the installed engine, so the paper trail is primary sources plus logs.
**Found.** Primary sources: the Godot 4.7 documentation (fetched and read 2026-10-13) and Godot 4.7.2 on Apple M4 Pro. One real shader from a small game is shown (a byte-identical copy). Every number on screen comes from a run in `evidence/planning-checks/`. The two third-party works are not named in what Bear pasted; their creators are an open question for Bear, and nothing from them is in this film.

## Primary

- **Godot 4.7 documentation** (`docs.godotengine.org/en/stable`, the 4.7 release: the page sidebar's newest upgrade guide is "Upgrading from Godot 4.6 to Godot 4.7"), fetched and read 2026-10-13. The raw pages were read from a scratch folder and are not stored here; the exact sentences used are quoted in `FACTCHECK.md`:
  - Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html`
  - Spatial shaders: `tutorials/shaders/shader_reference/spatial_shader.html` (render modes, fragment built-ins, global built-ins, light built-ins)
  - CanvasItem shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html` (the two-D `COLOR` and `UV`; "used to draw all 2D elements")
  - Shading language: `tutorials/shaders/shader_reference/shading_language.html` (uniforms, uniform hints, `source_color`, swizzling)
  - Built-in functions: `tutorials/shaders/shader_reference/shader_functions.html` (`fract`, `step`, `mix`)
  - Your first 3D shader: `tutorials/shaders/your_first_shader/your_first_3d_shader.html` (meshes, the default vertex step, uniforms from GDScript)
  - Standard Material 3D: `tutorials/3d/standard_material_3d.html` (albedo, unshaded, cull mode)
  - Overview of renderers: `tutorials/rendering/renderers.html` (the three renderers; switching in the editor)
  - Class references: `classes/class_shadermaterial.html`, `class_geometryinstance3d.html` (`material_override`), `class_boxmesh.html` (the 3 by 2 UV layout), `class_quadmesh.html`, `class_mesh.html` (`ARRAY_TEX_UV`), `class_spheremesh.html`, `class_tween.html` (what a tween is)
- **The installed engine**: Godot 4.7.2 stable (official), Apple M4 Pro, macOS (Darwin 25.5.0). The renderer is stated wherever a pixel value is shown: Forward+ unless the line says Compatibility or Mobile.
- **A shader from a small game**: `lab-shaders/12-signal-pad.gdshader` is byte-identical to the game's own `walker-claude/godot/signal-garden/signal.gdshader` (read-only copy, `diff` clean). The game's scene script (`garden.gd`, read only) was read for two facts: the pad is a `BoxMesh` of 1.55 by 0.10 by 1.55 with the shader set as its `material_override`, and the game's camera looks from the direction (5.8, 9, 11) at the origin. The game's pixel test (`tests/test-shader-pixel.gd`) draws the shader on a `QuadMesh` and expects the Compatibility numbers (its project uses the Compatibility renderer); the film does not say so, but the color film may want it. Nothing in the game was edited or run.
- **Bear's own chapters** (`csye-7270-building-virtual-environments/chapters/06-shader-foundations.md`, `07`, `08`): read for earlier 4.7.2 runs (a hint does not clamp; a tween needs the uniform set first; `get_shader_parameter` is null before any set; `SCREEN_TEXTURE` removed). Not named on screen; the film is standalone. Everything the film says from them was re-run in 3D here (verify3, verify3b).
- **The editor driver's frames (B43 only)**, recorded 2026-10-13 in the real Godot 4.7.2 editor on a scratch project, by script (`../_godot-shaders-series/editor-capture/README.md`, section 11; `png/1920x1080/renderer-path/`): the source of the Project Settings path and its labels, read from the live UI. Where the docs and the editor disagree (the docs say the renderer's name always sits in the editor's upper right corner; the shipped editor hides it by default), the editor run wins and `FACTCHECK.md` row 97 records it.
- **The series files**: `../_godot-shaders-series/` (GLOSSARY as of 2026-10-13, whose wording the on-screen definitions use; COMPONENT-SPECS; the Lab). The Lab's `quad3d` scene (orthographic camera, white ambient light at energy 1, no lamp) renders every single-shader capture; its limits are in `CHECKS-REPORT.md`.
- **Phonemizer check** (text only, no audio made; `brutalist.art/runtime/scripts/pronunciation.py --say`): "Shaders in three D" reads as three D, "U V" as two letters, "t" as "tee", "albedo" as "al-BEE-doh", and "unshaded" normally; the single letter "a" (B24) is read like the article. Reported for the build, not changed.

## Third-party sources (not used)

- A short introduction to Godot shaders, about 8 minutes, and a long course on two-D shaders in Godot (creators not named in the pasted text). Neither covers three-D. **Not stored. Nothing copied. No idea from either is followed:** this film recaps the shape of a two-D shader only to say what stays the same in three-D, and that shape is from the Godot documentation.
- **Open for Bear:** the creators' names and URLs, if you want them credited in the series' YouTube descriptions. Nothing in this film names them.

## What this film's demonstrations come from

Every Godot result on screen is a Shader Lab render, a scripted scene capture, an editor frame recorded by script (B43) or a docs screenshot, of a tested file in `lab-shaders/` and of the numbers in `evidence/planning-checks/`. Scripts and raw logs are there. Failed and inconclusive runs are kept: `run-3b-tween-without-set-FAILS-as-expected.log` (the tween failure the film warns about), `run-lab-checks` checks 04 and 05 (the two compile errors the film shows), and the brief's own stripe probes (`12-signal-pad-brief-probes` in `lab-results.jsonl`: both land on a dark stripe).

## Not stored

- The fetched documentation pages (HTML or text): they are third-party text; only short quotations are kept, in `FACTCHECK.md`.
- Any transcript of the two third-party works.
- Scratch PNGs from exploration runs (the scripts that make the kept PNGs are in `evidence/planning-checks/`).

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/` and scratch projects under `/private/tmp/`), Python with Pillow for pixel measurements, `curl` for the docs pages, the toolkit's phonemizer for the title check. No paid generation, no model call, no voice, no render.
