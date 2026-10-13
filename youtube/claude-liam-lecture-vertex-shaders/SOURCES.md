# Sources: Vertex Shaders

**What this is.** What the film is built from, with addresses and dates, and what was deliberately not stored.
**Why.** One source is a third-party work. The film follows its order of ideas and teaches them in new words with new, tested demonstrations; this file records that nothing was copied and who still needs crediting.
**Found.** Primary sources: the Godot 4.7 documentation and the installed Godot 4.7.2. Every number on screen comes from a run in `evidence/planning-checks/`. The third-party course behind the brief is not named in the material Bear passed on; its creator is an open question for Bear.

## Primary

- Godot 4.7 documentation (docs.godotengine.org/en/stable), read 2026-10-13, saved as plain text only for quoting in `FACTCHECK.md` (not stored in the repository):
  - Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html` (what `vertex()` and `fragment()` run over; the shader types)
  - Canvas item shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html` (the vertex and fragment built-ins tables: `VERTEX`, `UV`, `COLOR`, `TIME`)
  - Shading language: `tutorials/shaders/shader_reference/shading_language.html` (varyings, interpolation qualifiers `flat` and `smooth`, uniforms)
  - Class references: `classes/class_polygon2d.html`, `classes/class_meshinstance2d.html`, `classes/class_quadmesh.html`, `classes/class_planemesh.html`, `classes/class_mesh.html`, `classes/class_shadermaterial.html`, `classes/class_geometry2d.html`
- The installed engine: Godot 4.7.2 stable (official), Apple M4 Pro, macOS. Renderer stated wherever a pixel value is shown (Forward+; Compatibility checked for the five shaders named in `FACTCHECK.md` row 73).
- The series glossary (`../_godot-shaders-series/GLOSSARY.md`) for every on-screen definition, and the series Shader Lab (`../_godot-shaders-series/lab/`) for the renders.

## Third-party source followed (not copied)

- A long third-party course on 2D shaders in Godot (the vertex parts, about 40 minutes: basic vertex work, variables with `varying`, the vertex chapter and the flag). The creator is not named in the material Bear passed on.
- **Not stored.** No transcript or text of the course was saved to this folder or anywhere in the repository. The brief paraphrases it; `ACTS.md` paraphrases the brief. No sentence was reused; every demonstration (the four-corner tilt, the 297-vertex flag, the pinned and travelling wave, the corner colours, the pitfalls) was rebuilt and run on this machine.
- **Open for Bear:** the creator's name and address, if you want them credited in the YouTube description. Nothing in the film itself names them.

## What this film's demonstrations come from

Every Godot picture is a Shader Lab render or a capture of a custom scene (`evidence/planning-checks/scratch-project/capture_scenes.gd`) using a tested file in `lab-shaders/`; scripts, raw logs and measured numbers are in `evidence/planning-checks/` (`RESULTS.md` is the index). Failed and inconclusive runs are kept and labelled there: the compile error for a varying read in the wrong stage (`c6`, shown in no beat), the first vertex-id run that saturated (`verify4`), and the frozen-clock runs.

## Tools used (all free)

Godot 4.7.2 (the Shader Lab and a scratch project), Python with Pillow and numpy for pixel measurements, no paid generation, no model calls.
