# Sources: Reading the Screen

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** Two of the sources are third-party works. The film follows their order of ideas and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2, which was run for every behaviour the film claims (77 rows in `FACTCHECK.md`, scripts and logs in `evidence/planning-checks/`). The two third-party sources are not named in the text Bear pasted; their creators are an open question for Bear. The one outside fact is the gray weights, from Wikipedia.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable), fetched and read 2026-10-13:
  - Screen-reading shaders: `tutorials/shaders/screen-reading_shaders.html` (the copy, `hint_screen_texture`, `textureLod` and mipmaps, "Behind the scenes", "Back-buffer logic")
  - Canvas item shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html` (`SCREEN_UV`, `SCREEN_PIXEL_SIZE`, the removed `SCREEN_TEXTURE`, `TIME`)
  - Shading language: `tutorials/shaders/shader_reference/shading_language.html` (uniform hints, `discard`)
  - Built-in functions: `tutorials/shaders/shader_reference/shader_functions.html` (`texture`, `textureLod`, `mix`, `dot`, `distance`, `sin`)
  - CanvasLayer: `classes/class_canvaslayer.html`; BackBufferCopy: `classes/class_backbuffercopy.html`; Control: `classes/class_control.html` (`PRESET_FULL_RECT`, `mouse_filter`); Size and anchors: `tutorials/ui/size_and_anchors.html`; `@GlobalScope`: `classes/class_@globalscope.html` (PropertyHint); Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html`
  - Overview of renderers: `tutorials/rendering/renderers.html` (Forward+, Mobile and Compatibility; "the renderer, or rendering method"; switching in the editor) and ProjectSettings: `classes/class_projectsettings.html` (`rendering/renderer/rendering_method`), read 2026-10-13 for B36's one-line definition of a renderer
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS. Renderer stated on every claim that depends on it; every check was run in both Forward+ and Compatibility (the capture-size check, `verify10`, also compares three capture routes).
- **The real editor.** A plugin (`evidence/planning-checks/editor-labels/`) walked the Inspector and its menus in the actual Godot 4.7.2 editor (headless: the editor builds its whole UI) and printed the labels the film names. Nothing was typed from memory.
- Wikipedia, "Grayscale" (section "Luma coding in video systems": `Y' = 0.299R' + 0.587G' + 0.114B'`, and "Human vision is most sensitive to green, so this has the greatest coefficient value", said there of the sRGB weights) and "Luma (video)" (Rec. 601 and Rec. 709 weights), read 2026-10-13.
- Bear's chapter on shader foundations (`csye-7270-building-virtual-environments/chapters/06-shader-foundations.md`), line 83: it already records that `SCREEN_TEXTURE` is gone, the declaration with `hint_screen_texture, repeat_disable, filter_nearest`, the compiler's message, and the docs' overlap sentence. This film agrees with all of it and adds one refinement the chapter does not have: the shared copy is per canvas layer (measured). Not named on screen; the film is standalone.

## Third-party sources followed (not copied)

- The canvas part of a long course on 2D shaders in Godot (about 19 minutes in the brief's account; creator not named in the text Bear pasted).
- The water section of a short introduction to Godot shaders (about 2 of its 8 minutes; creator not named).
- **Not stored.** Neither transcript was available to this layout and none was saved anywhere; the layout worked from the brief's description of what each does. `ACTS.md` paraphrases which ideas appear where. No sentence was reused; every demonstration is a new scene on a new test world, every shader is new and was run.
- **Open for Bear:** the creators' names and URLs, if you want them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot result on screen is a capture of a scene script in `evidence/planning-checks/` (`scene_c01_pool.gd` to `scene_c23_finale.gd`) and every shader shown is a tested file in `lab-shaders/`. Failed and inconclusive runs are kept and labelled in `evidence/planning-checks/run-00-first-attempts-transcribed.txt` (a wrong expectation about layers, an inconclusive filter probe, a wrong reference in an edge measurement, a Lab batch whose probes were dropped by a quoting slip, an editor search that looked in the wrong place).

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/` and scratch projects built from `evidence/planning-checks/`), Python with Pillow for contact sheets, `curl` for the docs pages. No paid generation, no model call.
