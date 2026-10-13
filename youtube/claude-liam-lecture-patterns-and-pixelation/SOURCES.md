# Sources: Patterns and Pixelation

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** One of the sources is a third-party work. The film follows its order of ideas where they are sound and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every number on screen comes from a run in `evidence/planning-checks/`. The third-party course is not named in the material Bear supplied; its creator is an open question for Bear.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable; the page header reads "Godot Engine 4.7 documentation in English"), read 2026-10-13:
  - Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html` ("Shaders are a special kind of program that runs on Graphics Processing Units (GPUs)."; "canvas_item for 2D rendering.")
  - Built-in shader functions: `tutorials/shaders/shader_reference/shader_functions.html` (`floor`: "Rounds to the integer below."; `fract`: "Fractional (returns x - floor(x))."; `mod`: "Modulo (division remainder)." and "This is computed as x - y * floor(x/y)."; `step`: "b < a ? 0.0 : 1.0"; `length`: "Vector length."; `mix`: "Linear interpolate between a and b by c."; `texture`: "Performs a texture read.")
  - Canvas item shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html` (`TEXTURE_PIXEL_SIZE`: "Normalized pixel size of the default 2D texture. For a Sprite2D with a texture of size 64×32 pixels, TEXTURE_PIXEL_SIZE = vec2(1.0 / 64.0, 1.0 / 32.0)."; `UV` in `vertex()`: "Normalized texture coordinates. Range from 0.0 to 1.0."; in `fragment()`: "For a Sprite2D with region enabled, this will sample the entire texture."; `TIME`: "Global time since the engine has started, in seconds."; `COLOR`)
  - Shading language: `tutorials/shaders/shader_reference/shading_language.html` (uniforms: "the uniforms will appear as editable parameters in the material's inspector. Uniforms can't be written from within the shader."; `hint_range(min, max[, step])` for `int` and `float`: "Restricted to values in a range (with min/max/step)."; "implicit casting between scalars and vectors of the same size but different type is not allowed"; `vec2`: "Two-component vector of floating-point values."; "Godot uses a shading language similar to GLSL ES 3.0.")
  The three reference pages were also fetched as plain text into a scratch folder to confirm each quotation verbatim; the scratch copies are not kept in the repository.
- The installed engine: Godot 4.7.2 stable (official), `4.7.2.stable.official.ed1daf0bf`, Apple M4 Pro, macOS. Renderer stated on every pixel value.
- The series glossary (`../_godot-shaders-series/GLOSSARY.md`) for the wording of the terms it defines (UV, texture, uniform, vector, COLOR, TIME, shader type).

## Third-party source followed (not copied)

- A long third-party course on 2D shaders in Godot (creator not named in the material Bear supplied), whose pixel-grid, pixelate, stripes and dot-grid chapters this film covers. The film follows the course's order of ideas (cells, pixel grid with its admitted drift, checkerboard from a sum and a remainder, `pixel_size` from the texture's size, stripes from `fract` of a diagonal, dots from a centered cell) and corrects one claim (the half inside the `floor` is not centering).
- **Not stored.** The course's text, transcript and code were not saved to this folder or anywhere in the repository; the coverage map in `ACTS.md` paraphrases the brief's own summary. No sentence, code listing or example was reused: every shader was written fresh, every demonstration was run, and the finale (the dot screen) is not in the course.
- **Open for Bear:** the creator's name and URL, if you want them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot result on screen is a Shader Lab render or a small scene-script capture of a file in `lab-shaders/` (fifteen shaders, `01` to `15`, the hook and the rounded dot screen included); scripts, logs and the render measurements are in `evidence/planning-checks/`. Failed and inconclusive runs are kept and labelled: the first version of the "Your turn" check (`run-bhtf-1-INCONCLUSIVE-window-metric.log`, with the script that produced it), the percent-on-decimals shader error (`chk-percent-on-floats-EXPECTED-ERROR` in `lab-results.jsonl`), and one moving-stripes render that fits the formula less well than its three siblings (1.1 % of pixels differ; kept and noted in FACTCHECK row 49). Evidence-only reference shaders (not shown on screen) are in `evidence/planning-checks/reference-shaders/`.

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/` and one scratch project), Python with Pillow and NumPy for pixel measurements, `curl` and a small HTML-to-text script to read the docs pages, no paid generation.
