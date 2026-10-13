# Sources: Textures and Color

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** One source is a third-party work. The film follows its order of ideas and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2 on Bear's Mac. Every number on screen comes from a run in `evidence/planning-checks/`. The third-party course is not named in the text Bear pasted, and I was given only Bear's description of its texture and color chapters (the brief), never its transcript. Its creator is an open question for Bear.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable), read and quoted 2026-10-13:
  - Shading language, uniform hints and "Using source_color": `tutorials/shaders/shader_reference/shading_language.html`
  - Built-in functions (`texture`, `mix`, `step`, `dot`): `tutorials/shaders/shader_reference/shader_functions.html`
  - Canvas item shaders (`TEXTURE`, `COLOR`, `UV`): `tutorials/shaders/shader_reference/canvas_item_shader.html`
  - Spatial shaders (`OUTPUT_IS_SRGB`): `tutorials/shaders/shader_reference/spatial_shader.html`
  - Introduction to shaders (`fragment()` runs for every pixel covered by the mesh): `tutorials/shaders/introduction_to_shaders.html`
  - Overview of renderers (Forward+, Mobile, Compatibility; switching in the editor; the 2D HDR column): `tutorials/rendering/renderers.html`
  - Command line (`--headless`): `tutorials/editor/command_line_tutorial.html`
  - Class references: `Color` (sRGB encoding; `srgb_to_linear`, `linear_to_srgb`, `get_luminance`), `Viewport` (`use_hdr_2d`, `get_texture`), `ProjectSettings` (`rendering/viewport/hdr_2d`, `rendering/textures/canvas_textures/default_texture_filter`), `CanvasItem` (`texture_filter`, `texture_repeat`), `NoiseTexture2D`, `GradientTexture1D`, `ShaderMaterial` (`set_shader_parameter`), `Shader` (`get_shader_uniform_list`), `FastNoiseLite`, `Image`.
- Wikipedia, "Rec. 709" (en.wikipedia.org/wiki/Rec._709), read 2026-10-13: the primaries' chromaticities, the white point, the luma coefficients and the statement that sRGB shares the primaries. Cross-checked by derivation (`evidence/planning-checks/derive-bt709-weights.py`).
- Wikipedia, "sRGB" (en.wikipedia.org/wiki/SRGB), read 2026-10-13: the nonlinear curve places digital values closer together near black and further apart near white, where changes in brightness are less visible. Paraphrased in `FACTCHECK.md` (the claim that a color picker's numbers are spaced for the eye); nothing is quoted.
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS. Renderer stated on every pixel value. Compatibility on this Mac runs through OpenGL 4.1 on Metal ("OpenGL API 4.1 Metal"); other platforms and GPUs were not tested.
- The editor driver's frames, recorded 2026-10-13 in the real Godot 4.7.2 editor on a scratch project, by script (`../_godot-shaders-series/editor-capture/README.md`; `png/1920x1080/textures-and-color/` and `png/1920x1080/renderer-path/`): the source of every Inspector, menu and Project Settings label the film speaks or shows (B18, B34, B40), read from the live UI. Where the docs and the editor disagree (the renderer's name in the editor's corner), the editor run wins and `FACTCHECK.md` row 106 records it.
- Bear's own chapter notes on color spaces (the brief quotes them): tested here, not named on screen; the film is standalone.

## Third-party source followed (not copied)

- A seven-hour course on 2D shaders in Godot, the YouTube cut of a paid course (creator not named). Followed for the order of its two texture chapters and its color exercises (as described in the brief): reading a texture with `sampler2D`, gradient and noise textures, one minus, step on noise, mix, gray by channel. Not followed: its visual-node editor material, its type-conversion rules, its time exercise.
- **Not stored.** No transcript, caption file or page of the course was saved to this folder or anywhere in the repository; I never had one. `ACTS.md` paraphrases which ideas appear where. No sentence of it was reused; every demonstration was rebuilt and run.
- **Open for Bear:** the creator's name and URL, if you want them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot result on screen is a Shader Lab render, a harness capture, an editor frame of a scratch project, or the live docs page, each of a file in `lab-shaders/` (or the scene scripts in `evidence/planning-checks/`); scripts and raw logs are in `evidence/planning-checks/`. Failed and inconclusive runs are kept and labelled in `RESULTS.md`: the first set of plus-checks that dropped its probe arguments (a shell array was passed as one word), the first swatch picture (a coral patch too near the type gate's accent color) and the first burn ramp (a middle stop too near the same accent) are each superseded by a re-run and said so; the Lab's `noise` kind and a NoiseTexture2D were compared and are identical, not assumed.

## Not stored on purpose

The documentation pages and the two Wikipedia pages were read from downloaded copies kept in the session scratch folder only; the film folder holds short quotes (inside `FACTCHECK.md`) and nothing else from them.

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/` and a scratch project for the checks the Lab cannot make), Python with Pillow, NumPy and SciPy for pixel measurements, curl for the docs pages. No paid generation.
