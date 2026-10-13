# Sources: Soft Edges, Glow and Noise

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** One source is a third-party work. The film follows its order of ideas and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every number on screen comes from a run in `evidence/planning-checks/` or from arithmetic shown beside it. The third-party video is not named in what Bear pasted; its creator is an open question for Bear.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable), read 2026-10-13. The pages were downloaded as HTML so the quotes in `FACTCHECK.md` are verbatim:
  - Built-in shader functions: `tutorials/shaders/shader_reference/shader_functions.html` (step, smoothstep, pow, distance, clamp, mix, max)
  - Shading language: `tutorials/shaders/shader_reference/shading_language.html` (uniform hints, `source_color`, `repeat_enable`, the operators table)
  - Canvas item shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html` (`TIME`, blend modes)
  - NoiseTexture2D: `classes/class_noisetexture2d.html`; Noise: `classes/class_noise.html`; FastNoiseLite: `classes/class_fastnoiselite.html`
  - Environment: `classes/class_environment.html` (glow, `glow_hdr_threshold`, `BG_CANVAS`); WorldEnvironment: `classes/class_worldenvironment.html`
  - Viewport: `classes/class_viewport.html` (`use_hdr_2d`); ProjectSettings: `classes/class_projectsettings.html` (`rendering/viewport/hdr_2d`)
  - Environment and post-processing (the section "Using glow in 2D"): `tutorials/3d/environment_and_post_processing.html#using-glow-in-2d`
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS. Renderer stated on every pixel value; Forward+ unless a row says Compatibility.
- The editor driver's frames, recorded 2026-10-13 in the real Godot 4.7.2 editor on a scratch project, by script (`../_godot-shaders-series/editor-capture/README.md`): this film's own run for B19 (`png/1920x1080/soft-edges-glow-and-noise/`; scene, state script and log in `evidence/planning-checks/editor-capture/`) and two frames recorded for another film that show the same two noise views (B24, `png/1920x1080/textures-and-color/`). They are the source of every Inspector label the film shows, read from the live UI.
- The series GLOSSARY (wording of hint, uniform, UV, mask, ramp, step, alpha, TIME, texture) and COMPONENT-SPECS (the Shader Lab, `ShaderLab`, the capture harness).

## Third-party source followed (not copied)

- A third-party video build of an energy-shield effect in Godot 2D, about 25 minutes (the brief's description). Its creator has not been named by Bear. Ideas followed, in its order: a circle from `step` and `distance`, a soft edge from `smoothstep` with a width control, a highlight from one minus a distance raised to a power, two `source_color` colors, a glow multiplier, a noise texture scrolled with `TIME`. The short intro video's noise reveal (named in the brief) is also followed.
- **Not stored.** The source's transcript or text was not saved in this folder or anywhere in the repository. No sentence was reused; every shader, number and demonstration is new and was run.
- **Open for Bear:** the creators' names and URLs, if you want them credited in the YouTube description. Nothing in the film names them.

## What this film's demonstrations come from

Every Godot result on screen is a Shader Lab, custom-scene or editor capture of a file in `lab-shaders/`; scripts and raw logs are in `evidence/planning-checks/` (`RESULTS.md` is the index). Failed and inconclusive runs are kept and labelled in `RESULTS.md`: the first glow attempts that showed no halo because the environment's background mode was not Canvas (runs C and G4), and the first stage color for the glow demonstration (`#57625E`, 19 RGB from the type gate's MUTE grey, dropped for `#5F7A96`).

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/` and scratch projects under the session scratch folder), Python with Pillow for pixel measurements, `curl` and a small HTML-to-text script for the documentation quotes. No paid generation, no model call.
