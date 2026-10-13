# Sources: SubViewports

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** One source is a third-party work. The film follows its order of ideas and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources are the Godot 4.7 documentation, the installed Godot 4.7.2 and its real editor. Every number on screen comes from a run in `evidence/planning-checks/`; every Inspector label that the narration or the screen names was read from the editor itself. The third-party source is not named in the text Bear pasted; its creator is an open question for Bear.

## Primary

Godot 4.7 documentation (docs.godotengine.org/en/stable), read 2026-10-13. Each page was downloaded and read as text so the quotes in FACTCHECK.md are exact:

- Using Viewports: `tutorials/rendering/viewports.html`
- SubViewport class: `classes/class_subviewport.html`
- ViewportTexture class: `classes/class_viewporttexture.html`
- Viewport class: `classes/class_viewport.html` (`transparent_bg`, `get_texture()`)
- SubViewportContainer class: `classes/class_subviewportcontainer.html`
- MeshInstance2D class: `classes/class_meshinstance2d.html`
- QuadMesh and PlaneMesh classes: `classes/class_quadmesh.html`, `classes/class_planemesh.html`
- Sprite2D class: `classes/class_sprite2d.html` (the note that +Y is down)
- CanvasItemMaterial class: `classes/class_canvasitemmaterial.html` (`BLEND_MODE_PREMULT_ALPHA`)
- CanvasItem class: `classes/class_canvasitem.html` (texture filter modes)
- Color class: `classes/class_color.html` (`from_hsv`)
- Canvas item shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html` (render modes, `TIME`, `UV`, `TEXTURE`, `VERTEX`)
- Shader functions: `tutorials/shaders/shader_reference/shader_functions.html` (`fract`, `step`, `mix`, `clamp`, `abs`)
- 2D meshes: `tutorials/2d/2d_meshes.html`

The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS. Renderer stated on every pixel value; the checks that could differ were run in both Forward+ and Compatibility.

The real editor: Godot 4.7.2's own Inspector, read on 2026-10-13 in a scratch project (`evidence/planning-checks/editor-scratch/`, driver plugin `addons/shot/plugin.gd`): each property's label (`EditorProperty.label`), the enum texts the Inspector offers (`hint_string`), and real frames (`evidence/planning-checks/editor-frames/`). The film's editor frames were recorded by the series' editor driver (`../_godot-shaders-series/editor-capture/`, read and run, not edited; its plugin is copied into a scratch project at run time) from this film's state scripts (`evidence/planning-checks/editor-driver/`), and are in `editor-frames/series-driver/`. Nothing on screen is drawn from memory.

Reference implementations used only as checks, never shown: the engine's `Color.from_hsv` and Python's `colorsys.hsv_to_rgb` (standard library), against the film's own hue function.

## Third-party source followed (not copied)

- A long third-party course on 2D shaders in Godot (a paid course in a long YouTube cut); the SubViewport chapter, about 23 minutes (creator not named in the pasted text). The series planner's description of it is the brief (`../_godot-shaders-series/briefs/subviewports.md`), which lists what the course does in the planner's words; the course's own text was not in the working folder when this film was laid out.
- **Followed:** the order of ideas: a `SubViewport` with a size and a `ViewportTexture` on a sprite, the origin and offset, an inner shader and an outer shader, `transparent_bg`, diagonal stripes from a saw wave and a step, moving them with `TIME`, a hue function, and a wobble on a subdivided mesh.
- **Not stored.** No transcript of the course was saved to this folder or anywhere in the repository. No sentence was reused; every demonstration was rebuilt and run; the hue function was written from the definition (a plateau shifted by thirds) rather than from the course's version.
- **Open for Bear:** the creator's name and address, if you want them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot result on screen is one of:

- a capture of a scene in `evidence/planning-checks/capture_scene.gd` (scenes c01 to c21), run and probed in `verify7_capture_rehearsal.gd`;
- a real editor frame of the scratch project, re-recorded at build time with the same driver;
- a shader file in `lab-shaders/`, each compiled through the Shader Lab (`check_shader.sh`) in both renderers.

Failed and inconclusive runs are kept and labelled in `evidence/planning-checks/RESULTS.md` (an early rehearsal in which the plain display differed from the shader display at the moving blob's edges, which turned out to be the premultiplied-alpha finding itself; two badly chosen probe pixels; an editor view that showed a placeholder for a mesh; a viewport that stopped updating in one script order).

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/`, the series' editor driver, and scratch projects), Python with Pillow and numpy for pixel measurements, `curl` to read the documentation pages, `ffmpeg` is not needed until the build. No paid generation, no model call.
