# Sources: Light Shaders

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** One source is a third-party work. The film follows its order of ideas and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every number on screen comes from a run in `evidence/planning-checks/`. The third-party course is not named in the text Bear gave us; its creator is an open question for Bear.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable), read 2026-10-13, fetched with `curl` and read as text (not stored):
  - 2D lights and shadows: `tutorials/2d/2d_lights_and_shadows.html` (unshaded default, CanvasModulate and the ambient color, the PointLight2D texture and the GradientTexture2D recipe, DirectionalLight2D, normal maps)
  - CanvasItem shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html` (the Light built-ins table, the replace-even-if-empty rule, the unshaded and light_only render modes, the normal-map example, TIME)
  - Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html` (what vertex, fragment and light run for; unshaded skips the built-in light processor)
  - Shader functions: `tutorials/shaders/shader_reference/shader_functions.html` (step, smoothstep, mod, dot, length, distance, abs, floor)
  - Shading language: `tutorials/shaders/shader_reference/shading_language.html` (uniforms; setting uniforms from code)
  - Class references: `classes/class_light2d.html`, `class_pointlight2d.html`, `class_directionallight2d.html`, `class_canvasmodulate.html`, `class_tween.html`
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS; Forward+ for every number on screen, repeated on Compatibility (every comparison agreed within one step of 255). The renderer is stated on every pixel value.
- Bear's own chapter on shader foundations (`csye-7270-building-virtual-environments/chapters/06-shader-foundations.md`), which already says that an empty `light()` replaces Godot's lighting "with nothing" (consistent with this film's result). Not named on screen: the film is standalone.

## Third-party source followed (not copied)

- A long course on 2D shaders in Godot; its two chapters on the light function are about 28 minutes. The brief for this film describes what its author does, in the brief writer's words. The creator is not named in the text Bear gave us.
- **Not stored.** No transcript, no scene, no image and no sentence of it is in this folder or anywhere in the repository; `ACTS.md` paraphrases which ideas appear where. Every demonstration here was rebuilt and measured in Godot 4.7.2.
- **Where the course was loose or wrong:** it says a light shader cannot read `UV` (the 4.7 docs say it can: FACTCHECK row 23). The brief also asks whether the "rebuilt default" matches: it does exactly on a plain sprite and not with a normal map (rows 28 and 39).
- **Open for Bear:** the creator's name and URL, if you want them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot result on screen is a capture of a scene in `evidence/planning-checks/light_scene.gd` (described by `captures.json`) running a file in `lab-shaders/`; scripts and raw logs are in `evidence/planning-checks/`. Failed and inconclusive runs are kept: a parse error (`run-8a`), probe bugs (`run-8b`, `run-8c`, `run-8d`), a script that hung on an awaited signal (`run-9a`), and a coarse 8-bit decode (`run-2`, resolved by `run-6` case X).

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/` for compile checks, plus scratch projects for the lit scenes), Python with Pillow for contact sheets, curl for the documentation. No paid generation, no model call, no recording of a screen.
