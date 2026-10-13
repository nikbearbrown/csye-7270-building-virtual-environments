# Sources: Time and Waves

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** The film's idea order follows a third-party course; this file records that nothing was copied, which ideas were followed, and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every number on screen comes from a run in `evidence/planning-checks/`. The third-party course is not named in the brief; its creator is an open question for Bear.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable), read 2026-10-13; the exact passages are in `evidence/planning-checks/docs-quotes.md`:
  - Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html`
  - Canvas item shaders (Global built-ins: `TIME`, `PI`, `TAU`): `tutorials/shaders/shader_reference/canvas_item_shader.html`
  - Built-in functions (`sin`, `fract`, `abs`, `mix`, `step`, `distance`, `texture`): `tutorials/shaders/shader_reference/shader_functions.html`
  - Shading language (uniforms, hints, per-instance uniforms, setting uniforms from code): `tutorials/shaders/shader_reference/shading_language.html`
  - Class references: `classes/class_shadermaterial.html`, `class_canvasitem.html`, `class_curvetexture.html`, `class_curve.html`, `class_engine.html`, `class_time.html`, `class_scenetree.html`, `class_node.html`, `class_tween.html`, `class_projectsettings.html` (the `rendering/limits/time/time_rollover_secs` entry)
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS. Renderer stated on every pixel value; the probe checks ran in both Forward+ and Compatibility.
- The series' own tools: the Shader Lab (`../_godot-shaders-series/lab/`), used read-only.

## Third-party source followed (not copied)

- A long third-party course on 2D shaders in Godot, specifically its stretch on the `TIME` node, the waves chapter and the flag (about 25 minutes), and the fade-in at the end of a short third-party introduction to Godot shaders (`TIME / duration`, then a Tween). The creators are not named in the brief. The course repeats one error this film corrects (that `TIME` is the time since the node or scene was created).
- **Not stored.** No transcript of either work was saved to this folder or anywhere in the repository. `ACTS.md` paraphrases which ideas appear where. No sentence, demonstration, variable name or picture was reused: every demonstration (the pulse, the five squares, the stripes, the rings, the ripple, the breathing logo, the banner and its wind) was designed here and run.
- **Open for Bear:** the creators' names and URLs, if you want them credited in the YouTube description. Nothing in the film itself names them.
- Ideas followed, in the source's order: `TIME` inside a sine; the normalized curve; a curve texture sampled with a restarting ramp; the observation that a symmetric curve plays forward then back; a speed uniform; a flag pinned by multiplying with the address across.

## What this film's demonstrations come from

Every Godot result on screen is a Shader Lab render or a scene capture of a tested file in `lab-shaders/`; scripts and raw logs are in `evidence/planning-checks/`. Failed, inconclusive and side runs are kept and labelled: `gd/logs/run-0a` (the first clock run, inconclusive: the window stopped being drawn after about four seconds and `TIME` froze), `run-0b` (the same, reproduced), `run-0c` (the fix: `--always-on-top`), `run-1a` (a minimized window freezes `TIME`: a side finding, not in the film).

## Not used

The unscaled-clock advice in the docs' `TIME` row (a global shader uniform you update every frame) is quoted in `docs-quotes.md` but not taught: the film already carries `TIME`, the tick counter, an age and a progress uniform, and a fifth clock would overload it.

## Tools used (all free)

Godot 4.7.2 (the Shader Lab and scratch projects), Python with Pillow and NumPy for pixel measurements, `curl` for the docs pages. No paid generation, no model call, no recording of anyone's screen.
