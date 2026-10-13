# Sources: Local, World and Screen Space

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** One source is a third-party course. The film follows its order of ideas and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every number on screen comes from a run in `evidence/planning-checks/`. The third-party source is described in the brief that started this layout and is not named there; its creator is an open question for Bear.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable), fetched and read 2026-10-13; the raw pages were kept only in the scratch folder, not in this repository:
  - Canvas item shaders (built-ins, render modes, the skip_vertex_transform example): `tutorials/shaders/shader_reference/canvas_item_shader.html`
  - Shading language (matrix constructors and indexing, varyings, uniform hints, operators): `tutorials/shaders/shader_reference/shading_language.html`
  - Viewport and canvas transforms (transform order, "directed from right to left"): `tutorials/2d/2d_transforms.html`
  - Canvas layers (the viewport's canvas transform, Camera2D, UI fixed in screen space): `tutorials/2d/canvas_layers.html`
  - 2D coordinate systems and 2D transforms (canvas coordinates are also called world coordinates): `engine_details/architecture/2d_coordinate_systems.html`
  - Class references: Node2D (`position`, `global_position`), Sprite2D (`centered`), Camera2D, CanvasLayer (`classes/class_node2d.html`, `class_sprite2d.html`, `class_camera2d.html`, `class_canvaslayer.html`)
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS, Forward+; the position checks were repeated on Compatibility (OpenGL on Metal). The renderer is stated wherever a pixel value is shown.
- The editor driver's frames (B11 only), recorded 2026-10-13 in the real Godot 4.7.2 editor on a scratch project, by script (`../_godot-shaders-series/editor-capture/README.md`, section 2.5; `png/1920x1080/local-world-and-screen-space/`): the Inspector's Transform and Position rows for a parent and a child, with the labels read from the live UI.
- The Shader Lab (`../_godot-shaders-series/lab/check_shader.sh`) for the 17 shaders in `lab-shaders/`, and scratch Godot projects for everything the Lab cannot do (cameras, moving nodes, parents, stretch, the 4K route).

## Third-party source followed (not copied)

- A section of a long third-party course on 2D shaders in Godot (about 27 minutes: the model matrix, then the canvas coordinates), and the world-space part of a short third-party introduction video, as described in the series brief `../_godot-shaders-series/briefs/local-world-and-screen-space.md`. The creators are not named in the material this layout was given.
- **Not stored.** No transcript, no text and no screenshot of either work is in this folder or anywhere in the repository. This layout did not read the originals; it followed the brief's account of what they do. Every sentence of the narration is new, and every demonstration was rebuilt and run.
- **What the film follows:** the idea of three sets of numbers for one corner; the matrix expression for world position and the varying that carries it; a texture and a cutout locked to world position; the four ways to read the screen position; the "spacing out" payoff.
- **What the film corrects:** the unexplained zero and one in the vec four (reason given and tested); the texture-pixel-size shortcut for world-locked textures (shown as a pitfall: it ties the pattern to the sprite's art); the claim that the four screen methods are interchangeable (tested: they agree; the real differences are units and window size); the documentation's range for `FRAGCOORD`.
- **Open for Bear:** the creators' names and URLs, if you want them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot result on screen is a custom-scene or editor capture of a file in `lab-shaders/` (scene builders: `evidence/planning-checks/scenes_lib.gd`, `sky_lib.gd`; checks: `verify1.gd` to `verify8.gd`; Lab batch: `run-lab-checks.sh`). The star sky is procedural (seed 7); no external art. Failed and inconclusive runs are kept: `run-2a-verify2-FIRST-two-probes-missed-the-sprite.log` (two probe pixels missed the sprite) and the note on the first Lab batch (its arguments were dropped by a shell quirk) in `evidence/planning-checks/RESULTS.md`.

## Tools used (all free)

Godot 4.7.2, Python 3 (standard library only) for the checks and the generators, curl for the documentation pages. No paid generation, no model call.
