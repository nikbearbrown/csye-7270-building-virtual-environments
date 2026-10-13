# Sources: The Shader Math Toolkit

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** One of the sources is a third-party work. The film follows its order of ideas and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every number on screen comes from a run in `evidence/planning-checks/` or from a quoted docs line. The third-party course is not named in the brief Bear's team wrote; its creator is an open question for Bear.

## Primary

- Godot 4.7 documentation, read 2026-10-13 (the `/en/stable/` pages and the pinned `/en/4.7/` address carry the same text; the pinned address is the one the screenshot D1 uses):
  - Built-in shader functions: `docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/shader_functions.html` (step, smoothstep, mix, clamp, min, max, abs, floor, fract, mod, pow, length, distance, normalize, sin: signatures, formulas and the two "undefined" sentences quoted in FACTCHECK rows 12 to 59).
  - Shading language: `.../shader_reference/shading_language.html` ("Godot uses a shading language similar to GLSL ES 3.0"; vector construction `vec4 a = vec4(0.0);`; "Uniforms can't be written from within the shader."; `set_shader_parameter()`).
  - Canvas item shaders: `.../shader_reference/canvas_item_shader.html` (`UV` "Normalized texture coordinates. Range from 0.0 to 1.0."; `COLOR` is a `vec4`).
  - Introduction to shaders: `.../tutorials/shaders/introduction_to_shaders.html` ("The fragment() function runs for every pixel covered by the mesh."; "once or more for each pixel it has to draw").
  - GDScript `@GlobalScope`: `docs.godotengine.org/en/stable/classes/class_@globalscope.html` (`fmod` "keeping the sign of x", `fposmod` "wrapping equally in positive and negative", `lerp` allows extrapolation).
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro (Apple9), macOS 26.5.1, Forward+ on Metal 4.0 (`evidence/planning-checks/run-2-verify-env.log`). The renderer is stated on every credit line that shows a measured value.
- The series files this film obeys: `GLOSSARY.md` (wording of ramp, mask, uniform, fragment, COLOR, UV, vector), `COMPONENT-SPECS.md`, `BUILDER-BRIEF-COMMON.md`, the content brief `briefs/shader-math-toolkit.md` (all under `csye-7270-building-virtual-environments/youtube/_godot-shaders-series/`).

## Third-party source followed (not copied)

- **A long course on 2D shaders in Godot** (a seven-hour YouTube cut of a paid course; creator not named in the material this film was briefed from). The film follows the order in which it introduces the math functions (step first, then mix, smoothstep, pow, normalize, abs, floor, mod, fract) and its idea of building a circle from distance and step. Everything else is new: the standard plot, the pixel-for-pixel proofs, the measured corrections, the mod trap, the ring.
- **Not stored.** The course's transcript was not saved to this folder or anywhere in the repository; `ACTS.md` paraphrases which ideas appear where. No sentence was reused; every demonstration was rebuilt and run.
- **Open for Bear:** the creator's name and address, if you want them credited in the YouTube description. Nothing in the film itself names them.
- Four of its claims are corrected or qualified in `FACTCHECK.md`: `smoothstep` as a straight line (row 22), "swap the arguments to invert" (row 65), "fragments are stretched" as the reason for the oval (row 54), and silence about `mod` of a negative number (row 45).

## What this film's demonstrations come from

Every Godot result on screen is a Shader Lab capture of a file in `lab-shaders/`; every curve is the formula in `evidence/planning-checks/plot_data.py`, proved identical to Godot's render in `dense-compare.md`. Scripts, logs and the index are in `evidence/planning-checks/` (`RESULTS.md`). One failed start is kept in `RESULTS.md` (the GDScript check's first run never found its script in the scratch folder: a setup error, not a measurement).

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/`), Python with Pillow, numpy and scipy (pixel measurements; scipy only through the toolkit's own blob detector, read-only, for the advisory type-gate check), no paid generation.
