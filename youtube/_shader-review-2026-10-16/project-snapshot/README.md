# Shader Lessons (Cg to Godot)

**What this is.** A Godot 4.7.2 project holding 16 hand-converted shaders, one for each CgFX lesson in `../shader_lessons/` (Eat 3D "Shader Production DVD", 2012), plus the test rig and scripts that checked them. Converted by AI (Claude) under Bear's direction, 2026-10-16.
**Why.** The lessons teach lighting by writing the math yourself, which is what a series of Godot lecture films will teach in the same order. The shaders keep the math explicit (`render_mode unshaded`) so a film can point at each line, and every number a film quotes was measured here.
**Found.** All 16 compile and render in Forward+ and Compatibility and pass 134 numeric checks per renderer against a CPU re-implementation of the Cg arithmetic. The conversion notes list 17 findings (for example, `01_base` is already Lambert, and the cube-map lesson shows no reflection on any surface that faces the camera) and 19 traps met by running.

Third-party source, rights not confirmed by Bear: read `SOURCES.md` before sharing any of this. Do not `git add` this folder or `../shader_lessons/` without reading it.

## Open it

Open this folder in Godot 4.7.2, run the main scene (`scenes/stage.tscn`): a sphere and a torus wearing one lesson shader. Left / Right arrows (or A / D) step through the lessons; the label shows the file name. Lesson 12 has four techniques: edit the number in `#define TECHNIQUE` at the top of `shaders/12_techniques.gdshader`.

## Files

- `shaders/NN_name.gdshader`: the 16 conversions (the numbers are the original CgFX numbers, nothing else). Each opens with a header comment: source file, the conversion statement, what the original did, what changed.
- `textures/`: code-authored test textures and six cube-map faces (`tools/make_textures.py`).
- `scripts/`: `rig.gd` (camera, sphere, torus), `lessons.gd` (the lesson table, materials, texture binding), `stage.gd` (the stage scene).
- `tools/`: `check_all.sh` (compile every shader through the series Lab, both renderers), `cg_isms.sh` (compile-time Cg habits), `traps.gd` and `verify.gd` (run-time traps and numeric checks), `harness.gd`, `run_godot.sh` (one windowed Godot at a time, with a hard timeout), `make_textures.py`.
- `CONVERSION-NOTES.md`: results, departures, traps, findings. `SOURCES.md`: provenance. `evidence/INDEX.md`: every log and what was run.

## Re-run the checks

From this folder (each needs a real screen; one windowed Godot at a time):

```
tools/check_all.sh
tools/run_godot.sh res://tools/traps.gd forward_plus   <abs log path>
tools/run_godot.sh res://tools/verify.gd forward_plus  <abs log path> --lessons 0-15
tools/run_godot.sh res://tools/verify.gd gl_compatibility <abs log path> --lessons 0-15
```

`verify.gd` over all 16 lessons takes longer than the 240 s timeout in `run_godot.sh`; the logs in `evidence/logs/` were made in four groups (`--lessons 0-3`, `4-7`, `8-11`, `12-15`).
