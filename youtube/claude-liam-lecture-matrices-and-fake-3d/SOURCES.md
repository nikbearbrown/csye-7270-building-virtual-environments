# Sources: Matrices and Fake 3D

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** One source is a third-party work. The film follows its order of ideas as the brief describes them and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every number on screen comes from a run in `evidence/planning-checks/`. The third-party course is not named in anything this session received (and its transcript was not given to it); its creator is an open question for Bear.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable), read 2026-10-13 with the session's fetch tool, which returns a model-assisted extract of each page; the excerpts used are in `evidence/planning-checks/docs-quotes.md`:
  - Shading language: `tutorials/shaders/shader_reference/shading_language.html` (matrix types are column major; construction "interpreted as columns"; `mat4(1.0)` is the identity; building a matrix from another size; matrix times vector, vector times matrix and matrix times matrix are the linear-algebra products; `m[column][row]`)
  - Built-in shader functions: `tutorials/shaders/shader_reference/shader_functions.html` (`radians`, `transpose`)
  - Canvas item shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html` (`VERTEX` in `vertex()` is "in local space (pixel coordinates, relative to the Node2D's origin)"; the Global built-ins table lists `PI`, `TAU` and `E` and says they are available everywhere, including custom functions)
  - Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html` (`vertex()` "runs over all the vertices in the mesh")
  - Matrices and transforms: `tutorials/math/matrices_and_transforms.html` (rotation is represented clockwise because Y points down; rotations are in radians; order matters; X and Y are the first and second columns; `Transform2D` has `x`, `y` and `origin`)
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS. Renderer stated on every pixel value: Forward+ unless a FACTCHECK row says Compatibility (`gl_compatibility`).
- The series' shared files: `../_godot-shaders-series/GLOSSARY.md` (wording of vector, vertex, uniform, built-in) and the Shader Lab (`lab/check_shader.sh`, `lab/runner.gd`).

## Third-party source followed (not copied)

- A video course on matrices and fake 3D in Godot shaders (about 27 minutes in the brief's account; creator not named in anything this session received). **Not stored.** This session never had its transcript; it worked from the brief's paraphrase (`../_godot-shaders-series/briefs/matrices-and-fake-3d.md`), and `ACTS.md` paraphrases which ideas appear where. No sentence of the course was reused; the table for the five-and-six example is the film's own, chosen so that its product is the brief's 23 and 34; every demonstration was rebuilt as a shader and run.
- **Open for Bear:** the creator's name and address, if you want them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot result on screen is a Shader Lab capture of a file in `lab-shaders/` (eleven shaders, each run through `lab/check_shader.sh`); scripts and raw logs are in `evidence/planning-checks/`. Unit-test shaders that are not shown on screen are in `evidence/planning-checks/shaders/`. Failed runs are kept: `run-v2a-verify2-FAILED-gdscript-parse-error.log` (a typing error in a scratch script, fixed in `verify2-origin-and-corners.gd`) and the two expected compile failures `e1` and `e2` (mixed sizes), labelled as such in `lab-results.jsonl`. The compiler message shown in B19 is the real one from `e1`.

The `card` texture used in the captures is drawn by `evidence/planning-checks/runner-card.gd` (a scratch copy of the Lab runner with a `card` texture, a `--sprite-n` option and a `--dot` marker; nothing else changed). It is the film's own artwork (a cream card, a teal arrow, a teal square), not a copy of anything.

## Not stored on purpose

No transcript, no third-party text, no screenshot of the course. The docs pages are quoted by short excerpts only, with their addresses.

## Tools used (all free)

Godot 4.7.2 (the Shader Lab in `../_godot-shaders-series/lab/`), Python with Pillow and NumPy for pixel measurements, the session's fetch and search tools for the docs. No paid generation, no voice, no render.
