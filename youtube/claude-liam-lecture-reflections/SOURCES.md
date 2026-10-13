# Sources: Reflections

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** The film follows the order of ideas of a third-party video course and teaches them in new words, on a new scene, with new tested demonstrations. This file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every number on screen comes from a run in `evidence/planning-checks/`. The third-party course is not named in what Bear supplied; its creator is an open question for Bear. The layout agent never saw the course itself, only the brief's paraphrase.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable), read 2026-10-13:
  - BackBufferCopy class: `classes/class_backbuffercopy.html`
  - Screen-reading shaders: `tutorials/shaders/screen-reading_shaders.html`
  - RemoteTransform2D class: `classes/class_remotetransform2d.html`
  - CanvasItem class: `classes/class_canvasitem.html` (tree order, z index)
  - Canvas layers: `tutorials/2d/canvas_layers.html`
  - Shading language, Flow control (the floating-point comparison warning): `tutorials/shaders/shader_reference/shading_language.html#flow-control`
  - Canvas item shaders (COLOR, SCREEN_UV): `tutorials/shaders/shader_reference/canvas_item_shader.html`
  - Built-in functions (distance, mix): `tutorials/shaders/shader_reference/shader_functions.html`
  - Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html`
  - Sprite2D class (flip_v): `classes/class_sprite2d.html`
  - Viewport class (use_hdr_2d) and Project settings (rendering/viewport/hdr_2d): `classes/class_viewport.html`, `classes/class_projectsettings.html`
  - A first look at the editor (the "Scene dock"): `getting_started/introduction/first_look_at_the_editor.html`
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS. The renderer is stated on every pixel value.
- Godot's own editor, recorded with Movie Maker from a scratch project (two planning frames in `evidence/planning-checks/png/`).

## Third-party source followed (not copied)

- A video course on 2D shaders in Godot (about 13 minutes on this topic; creator not named in what Bear supplied).
- **Not stored.** No transcript, text, image or art from it is in this folder or anywhere in the repository. The brief paraphrases what it does; `ACTS.md` maps the ideas by topic.
- **What the film follows:** the hidden mask (this film's word: label map) under opaque art, `BackBufferCopy` between them, a flipped reflection kept in step with `RemoteTransform2D`, a shader that reads the screen texture and keeps the water, a lower alpha for the coast, a tint with `mix`.
- **What the film does differently:** it compares with a distance instead of `==` (FACTCHECK 66); the Rect-mode finding, the canvas-layer rule, the eight-bit explanation, the HDR 2D numbers and the renderer comparison are its own measurements; the pond, the sandbar, the three-sprite window and every demonstration were built and run for this film.
- **Open for Bear:** the creator's name and URL, if you want them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot result on screen is a capture of a scene in `evidence/planning-checks/capture_scenes.gd` (art from `pond_common.gd`, shaders from `lab-shaders/`) or a real editor frame of the scratch project built by `make-editor-project.sh`. Scripts and raw logs are in `evidence/planning-checks/` (index: `RESULTS.md`). Failed and inconclusive runs are kept: `run-00-expD-first-run-wrong-probe-pixel-FAILED.log` and `run-02-expB-modes-and-readers-INCONCLUSIVE-rect*.log`.

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/` for compile checks, scratch projects for everything the Lab cannot do), Python with Pillow (contact sheets, crops), ffmpeg (the capture tool's encodes: all nineteen clips at their beat lengths, 3840 x 2160). No paid generation, no model call.
