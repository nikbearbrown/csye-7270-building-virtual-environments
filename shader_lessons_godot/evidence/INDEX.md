# Evidence index

**What this is.** Every log, render and check output behind `CONVERSION-NOTES.md`, with what was run to make it. All runs 2026-10-16 on one Mac (Apple M4 Pro), Godot 4.7.2.stable.official, windowed (never headless), one run at a time under the series Lab's lock, each with a hard `timeout`. Paths are relative to the project folder.
**Why.** So a later session can re-run any check, or a film can cite a number and find the line it came from.
**Found.** 16 of 16 shaders compile in both renderers; 134 numeric checks per renderer pass, 0 fail; the engine logs contain no `ERROR` or `WARNING` lines (scanned at the end).

## Compile (the series Lab's `check_shader.sh`)

| File | Command | Result |
|---|---|---|
| `compile/check_shader-forward_plus.txt` | `tools/check_all.sh` (`check_shader.sh <shader> --kind quad3d --renderer forward_plus`) | 16 of 16: exit 0, `ok: true`, uniform lists match the shaders |
| `compile/check_shader-gl_compatibility.txt` | same with `--renderer gl_compatibility` | 16 of 16 |
| `compile/negative-control.txt` | the Lab's own `broken.gdshader` | `SHADER ERROR: Expected a ';'`, exit 1: the check can fail |
| `compile/cg-isms.txt` | `tools/cg_isms.sh` (Cg habits pasted into minimal shaders) | 14 of 16 cases fail with the compiler's message; the control and the row-versus-column index compile |

## Run-time traps (`tools/traps.gd`, lines `TRAP-n`)

| File | Command |
|---|---|
| `logs/traps-forward_plus.txt` (+ `.engine.txt`, the full console) | `tools/run_godot.sh res://tools/traps.gd forward_plus <log>` |
| `logs/traps-gl_compatibility.txt` (+ `.engine.txt`) | same with `gl_compatibility` |

## Numeric checks (`tools/verify.gd`, lines `CHECK` and `SUMMARY`)

Each log is one group of lessons; each line says what pixel or image was compared, the expected value, the rendered value, and PASS or FAIL.

| Files | Lessons |
|---|---|
| `logs/verify-forward_plus-L0-3.txt`, `-L4-7`, `-L8-11`, `-L12-15` | Forward+ |
| `logs/verify-gl_compatibility-L0-3.txt`, `-L4-7`, `-L8-11`, `-L12-15` | Compatibility |
| `logs/info-mips-forward_plus-L08.txt` | informational: lesson 8 with mip chains on (99.92 percent within 3 bytes) |

Command, for example: `tools/run_godot.sh res://tools/verify.gd forward_plus <log> --lessons 4-7`. Each `.engine.txt` beside a log is the full console of that run (it also holds the `CHECK` lines).

## Renders (`renders/`)

48 PNG frames (1280 by 720, the root viewport as the renderer drew it), one per lesson and variant per renderer: `NN_name-forward_plus.png` and `NN_name-gl_compatibility.png`. Variants: `02_lambert_cg_default_light` (the Cg default light), `05_phong_specular_only`, `11_uv_manip_scale_translate`, `11_uv_manip_scroll`, `12_techniques_0_opaque` to `_3_additive`, `14_car_shader_offset`, `15_uber_spread`. The small coloured square in the top-left corner of the lesson 10 and 11 frames is the TIME probe, not part of the lesson.

## What the evidence does not cover

No Maya or CgFX run; no real-time frame rate (the harness draws at fixed steps); the scene `scenes/stage.tscn` was run through the script harness only, not opened in the editor; nothing was listened to or filmed.
