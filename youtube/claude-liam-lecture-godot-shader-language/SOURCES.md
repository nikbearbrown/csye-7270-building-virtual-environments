# Sources: Godot Shader Language

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** The idea order of this film follows a long third-party course on 2D shaders in Godot. The film teaches those ideas in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** The primary sources are the Godot 4.7 documentation and the installed Godot 4.7.2; every behavior and every engine message in the film comes from a run in `evidence/planning-checks/`. The third-party course is described only in the series brief; its creator is not named in the text Bear gave, and crediting them is an open question for Bear.

## Primary

All read on 2026-10-13. The documentation address is `docs.godotengine.org/en/stable`, which was version 4.7 that day (its upgrade guides run up to "Godot 4.6 to Godot 4.7").

- Shading language: `tutorials/shaders/shader_reference/shading_language.html` (types, casting, swizzling, constructing, operators, flow control, discarding, functions, varyings, uniforms and hints, constants, comments).
- Canvas item shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html` (processor functions, render modes, built-ins, global built-ins, the sentence that a `light()` function replaces the built-in one).
- Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html` (shader types, first line, render modes on the second line, what vertex, fragment and light run over).
- Built-in shader functions: `tutorials/shaders/shader_reference/shader_functions.html` (the `vec_type` aliases, the signatures of `sin`, `mix`).
- Shader preprocessor: `tutorials/shaders/shader_reference/shader_preprocessor.html` (the section "`#if` preprocessor versus `if` statement: Performance caveats": the only place the documentation discusses what branches cost).
- Converting GLSL to Godot shaders: `tutorials/shaders/converting_glsl_to_godot_shaders.html` (`gl_FragColor` corresponds to `COLOR`; `main` becomes `fragment`).
- Shaders style guide: `tutorials/shaders/shaders_style_guide.html` (tabs; a digit on both sides of the point).
- Using VisualShaders: `tutorials/shaders/visual_shaders.html` (read; "The visual shader graph is converted to a script shader behind the scene". Not used in the narration; see `ACTS.md`).
- Text search of every page in the shader tutorial section (the eight above plus the three first-shader pages, compute shaders, screen-reading shaders, advanced post-processing, and the sky, fog, particle, spatial and texture-blit references: nineteen pages) for "slow", "branch", "performance", "expensive" and "faster": the only statements about branch cost are on the preprocessor page.
- The installed engine: Godot **4.7.2 stable (official)**, Apple M4 Pro (Metal), macOS. The Shader Lab is `../_godot-shaders-series/lab/` (`check_shader.sh`, `runner.gd`). Renderer: Forward+ for every pixel value quoted.
- Nothing else is a source: no book, no course text, no other film.

## Third-party source followed (not copied)

- **A seven-hour course on 2D shaders in Godot**, a YouTube cut of a paid course; its creator is not named in the text Bear gave, and its pricing is not relevant here. It is known to this film only through the series brief (`../_godot-shaders-series/briefs/godot-shader-language.md`), which describes in the brief author's words what its variables, shader-code, function and outline chapters cover. The ideas this film follows: code is the thing to read; the language is C-like with semicolons, braces and strict types; vectors, constructors and swizzles; declarations and uniforms with hints; a function must receive `UV` as an argument; a loop replaces repeated lines; the remark about `if` and speed. The film checks every one of them by running Godot or reading the documentation, and corrects the ones that are loose (`ACTS.md`, `FACTCHECK.md`).
- **Not stored.** The course's transcript or text was not given to this layout, was not saved anywhere, and no sentence of it is reused. Every demonstration is new (the pastel gradient, the stripes, the split picture, the 14-line `breathe` file).
- **Open for Bear:** the creator's name and address, if you want them credited in the YouTube description. Nothing in the film names them.

## What this film's demonstrations come from

Every Godot result on screen is a Shader Lab render of a file in `lab-shaders/` (thirty-five working files and twenty-four that are meant to fail, prefix `err`); every error shown is the engine's own log, in `evidence/planning-checks/logs/`. The index of runs, with commands and dates, is `evidence/planning-checks/RESULTS.md`. Runs that were inconclusive or that changed the script are kept and labelled there.

## Tools used (all free)

Godot 4.7.2 (the Shader Lab and a throwaway copy of it for the full error logs), Python with Pillow for pixel measurements, `curl` and a small HTML-to-text script to search the documentation, Manim's text layout used only to measure how wide code lines are at the 32-point floor (nothing was rendered), Kokoro's phonemizer used only to read how a few words would be pronounced (no audio was made). No paid generation.
