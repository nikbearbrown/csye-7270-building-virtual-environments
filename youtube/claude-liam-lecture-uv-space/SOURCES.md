# Sources: UV Space

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** One source is a third-party work. The film follows its order of ideas in places and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every number on screen comes from a run in `evidence/planning-checks/`. The third-party course's creator is not named in what Bear gave the series; whether to credit it in the YouTube description is an open question for Bear.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable), read 2026-10-13:
  - CanvasItem shaders (`tutorials/shaders/shader_reference/canvas_item_shader.html`): `UV` in `vertex()` (inout) and `fragment()` (in), `TEXTURE`, `TEXTURE_PIXEL_SIZE`, `SCREEN_PIXEL_SIZE`, `TIME`, `COLOR`.
  - Shading language (`.../shading_language.html`): uniforms, uniform hints (the `repeat[_enable, _disable]` and `filter[...]` rows).
  - Built-in functions (`.../shader_functions.html`): `texture`, `step`, `abs`, `length`, `distance`.
  - Introduction to shaders (`tutorials/shaders/introduction_to_shaders.html`) and Your first 2D shader (`tutorials/shaders/your_first_shader/your_first_2d_shader.html`): what a shader is, what `fragment()` runs over, "UV varies between 0-1", "you can only read from UV".
  - CanvasItem class reference (`classes/class_canvasitem.html`): the `TextureRepeat` enum and the `texture_repeat` property.
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS. Renderer stated on every pixel value; geometry also run on Compatibility.

## Third-party source followed (not copied)

- A long third-party course on 2D shaders in Godot (the YouTube cut of a paid course). Its creator is not named in the text Bear gave the series. The brief (`../_godot-shaders-series/briefs/uv-space.md`) describes its UV material, about 35 minutes across its UV-control, texture, vertex-basics and canvas chapters.
- **Ideas the film follows:** `UV` drawn as red and green; scaling the address; offsetting it; the inverted effect of an offset explained with numbers; texture repeat; masking the border with `step`; centering with `2.0 * UV - 1.0`; mirroring with `abs`; correcting a circle with the aspect ratio.
- **Where it was loose or wrong:** its explanation of the oval (stretched "potential pixels") is corrected, and "scaling by 2 shows only the top-left corner" is qualified (FACTCHECK rows 23 and 46).
- **Not stored.** The course's text was not saved to this folder or anywhere in the repository. The coverage map in `ACTS.md` paraphrases the brief. No sentence, number or demonstration was reused: every shader was rewritten (different numbers, a different picture) and run.
- **Open for Bear:** the creator's name and URL, if he wants them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot picture on screen is a Shader Lab render of a file in `lab-shaders/`; scripts and raw logs are in `evidence/planning-checks/`. Failed or expected-failure runs are kept and labelled: `uv-write-error-EXPECTED-FAIL` (assigning to `UV` in `fragment()` does not compile) in `lab-results.jsonl`.

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/` and four scratch scripts), Python with Pillow and NumPy for pixel measurements (`measure.py`), curl for the docs pages. No paid generation, no voice, no render.
