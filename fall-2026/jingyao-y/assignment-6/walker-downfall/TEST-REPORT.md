# TEST-REPORT.md — Assignment 6

Machine: Windows 11, Godot 4.7.2-stable (official) console build, Forward+ / D3D12.
Every run goes through `scripts/run-test.sh`; the mode is given with each result.

## Headless facts probe

`./scripts/run-test.sh a6_probe_headless.gd 60` → `logs/a6_probe_headless_60fps.log`
(agent, 2026-11-07). Headless reports `forward_plus` / `d3d12` with an empty
adapter name (dummy renderer). Every class, property and enum CHANGE-BRIEF.md
names exists in 4.7.2. `CPUParticles3D` has no `amount_ratio`;
`ParticlesMaterial` and `scale_random` do not exist; `initial_velocity` and
`scale` exist as Vector2 compatibility properties that set the min/max pair.
A one-shot `GPUParticles3D` reads `emitting == false` from frame 1 and never
emits `finished` headlessly.

## Baseline (before any A6 code)

Pending: the serial rerun of the parallel failures is still running.

## Effect A configuration test and mutations (agent, 2026-11-07)

`./scripts/run-test.sh test_hit_spark_config.gd 60` (fixed 60 fps):
165 checks, 0 failed, exit 0 (`logs/test_hit_spark_config_60fps.log`).
Each mutation was made in `effects/hit_spark.tscn`, run, and the file restored
byte-for-byte from a copy; the clean rerun is again 165/0.

| Mutation | Edit (Sparks process material) | Config test | Evidence |
|---|---|---|---|
| M1 Godot 3 name | `initial_velocity_min = 3.0` → `initial_velocity = 3.0` | **exit 1**: `FAIL Sparks initial_velocity_min/max [3.0, 6.0] (got 0.0, 6.0)` | `evidence/a6/mutations/m1_godot3_name.log` |
| M1, game | same mutation, preview run windowed | the effect still fires at frames 10 and 16, no load warning or error; sparks start at speed 0–6 instead of 3–6 | `m1_godot3_name_preview.log`, `m1_godot3_name_frame12_fixture.png` (fixture) |
| M1b compat form | `initial_velocity = Vector2(3, 6)` (min/max lines removed) | **exit 0**, 165/0: 4.7.2 still has `initial_velocity` as a Vector2 compatibility property that sets min and max, so this spelling is translated, not dropped | `m1b_compat_vector2.log` |
| M2 drift | `damping_max = 10.0` → `4.0`, brief unchanged | **exit 1**: `FAIL Sparks damping_min/max [6.0, 10.0] (got 4.0, 4.0)`; Godot also pulled `damping_min` down to the new max | `m2_value_drift.log` |

So the Godot 3 *float* spelling fails silently in the game and is caught only
by the read-back test; the Vector2 spelling works because the old name survives
as a compatibility alias in this version.
