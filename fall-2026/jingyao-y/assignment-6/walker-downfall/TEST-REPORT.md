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

All 89 `tests/test_*.gd` at fixed 60 fps through `scripts/run-baseline.sh`
(10 in parallel, each via `run-test.sh <file> 60 <300|1200>`):
**78 of 89 pass** (`logs/baseline-before/summary.txt`). The 11 failures were
rerun one at a time (`run-test.sh <file> 60 600`,
`logs/baseline-before-serial/summary.txt`): `test_audio` and `test_market`
pass alone (load-sensitive); amiya_input, base_crew, hotbar_input, loot_input
time out (124) and builds, combat, item_icons, lappland_input fail (1) alone as
well; `test_ui_v1` was not rerun alone (the serial run was stopped before it).
The Step 3 session measured why the real-input suites fail headless:
`Input.parse_input_event` never reaches `GameManager._input`, so their mouse
pointer stays at (0,0). None of these are touched by A6.

## Effect A state test (Step 3 session, 2026-11-07)

`./scripts/run-test.sh test_hit_spark_state.gd 60 600` — fixed 60 fps,
headless, real `main.tscn`, real game loop, real left-mouse events
(`Input.parse_input_event`, plus `root.push_input` when headless so the event
takes the game's own Window → SubViewport → `GameManager._input` path). The test
never calls `_hit_spark`, `CombatVfx.spawn`, `attack()` or `attack_direction()`.
Result: **22 PASS, 0 FAIL, exit 0** (`logs/test_hit_spark_state_60fps.log`).

| Rule | What was asserted |
|---|---|
| A1 | none on load (game, base, field, +30 frames); 拉普兰德 held attack: 4 landed hits → 4 HitSparks at the struck enemy's position (max offset 0.0), each a child of GameManager; cross cut adds one on the second enemy; frame-by-frame match of sparks to landed melee hits; sword-wave projectile hit → none; ground click → walk, no swing, none; enemy hits her → none |
| A2 | 阿米娅's double cut: sparks added 0.117 s apart, two distinct nodes alive together, first not restarted (its own clock never went back) |
| A3 | all 13 freed; each lived 32 frames = 0.533 s (between 0.45 s and 0.55 s + 1 frame) |
| A4 | a 1-HP enemy killed by a real hit left the tree on frame 407, its spark on frame 439 |

Parent mutation (burst parented to the enemy): 3 checks fail (GameManager
parent, A4, A3 lower bound), `logs/test_hit_spark_state_60fps_mutation_parent.log`;
code restored, diff re-checked by the main session.

Not provable headlessly: that the bursts emit or look right, "both emitting"
on screen, A4's full play on screen, legibility, screen-edge clipping. Not
drivable by real input: a swing that misses (a ground click walks since
2026-10-20; `attack()` only swings at a target in reach and sight).

After the change, all suites in parallel (`logs/baseline-after-step3/summary.txt`):
**80 of 91** (the two new A6 suites pass). Differences from before:
`test_audio` FAIL→PASS (load-sensitive, passes alone before too);
`test_elevation` PASS→FAIL in parallel, passes alone
(`run-test.sh test_elevation.gd 60 1200`, exit 0). The other ten failures are
the same as before.

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
