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

## The process shader (Step 6)

**Who did what.** Godot 4.7.2 does not expose a material's shader RID to
scripts (`get_shader_rid` and `_get_shader_rid` both fail from GDScript:
`logs/a6_dump_process_shader_windowed.log`), so the agent could not dump the
code itself. The agent wrote `tests/a6_make_scratch_process_scene.gd`, which
saves `previews/scratch_process_shader.tscn`: one `GPUParticles3D` with a
unique deep copy of `effects/hit_spark.tscn` Sparks' `ParticleProcessMaterial`.
**The user** opened it in the editor and used the Inspector's Process Material
menu → Convert to ShaderMaterial → Shader → Save As. The agent moved the saved
file into `shaders/` (the dialog put it under `previews/shaders/` the first
time and the project root the second).

**Attempt 1 was not the material's shader.** Converted straight after opening,
the code had a POINT emission shape and no `color_ramp` / `scale_curve`
sampling (line 157 held only `// Compile-time add textures.`), though the copy
has a radius-0.1 sphere, a ramp and a curve. Kept as
`evidence/a6/step6/attempt1_particles_generated.gdshader.txt`. For attempt 2
the user first changed Spawn → Position → Emission Shape to Point and back to
Sphere, forcing the material to regenerate, then converted. Attempt 2 has the
sphere, the ramp and the curve: it is `shaders/particles_generated.gdshader`
(371 lines; nothing in the game uses it). Conclusion: the converter copies
whatever shader the material last generated; on a freshly loaded material
that was a default one.

| What | Line(s) in `shaders/particles_generated.gdshader` |
|---|---|
| `shader_type particles;` | 3 |
| `start()` / `process()` | 224 / 274 |
| initial velocity from its min and max | 140: `params.initial_velocity_multiplier = mix(initial_linear_velocity_min, initial_linear_velocity_max, rand_from_seed(alt_seed));` (uniforms 10–11); used as the start velocity at 263 |
| gravity changes velocity | 307 `force = gravity;` then 320 `USERDATA1.xyz += force * DELTA;` (accumulated velocity), 338 `VELOCITY = final_velocity;`, 339 position step |
| colour over life sampled | 162 `parameters.color *= texture(color_ramp, vec2(lifetime));` inside `process_display_param` (159), called from `process()` at 341 with `lifetime_percent`, written at 346 `COLOR = params.color;` |
| scale over life applied | 161 `parameters.scale *= texture(scale_curve, vec2(lifetime)).rgb;`, applied to the transform at 361–363 |
| tie to the brief | 140 ↔ Sparks `initial_velocity_min–max` **3.0–6.0** (CHANGE-BRIEF Effect A settings); also 132 damping ↔ **6.0–10.0** |
| `amount_ratio` | 236 `if (rand_from_seed(alt_seed) > AMOUNT_RATIO) { ACTIVE = false; }`: a particle is skipped at spawn, the buffer is not reallocated (why Effect B drives `amount_ratio`, not `amount`) |

**Which brief settings live here, which in the draw step.** In this process
shader: emission shape and radius, direction and spread, initial velocity,
gravity, damping, scale min/max and scale curve, colour ramp, hue variation,
angle, lifetime randomness, and the per-particle `AMOUNT_RATIO` test. Not here:
`amount`, `lifetime`, `one_shot`, `explosiveness`, `preprocess`,
`local_coords`, `visibility_aabb` (node settings the engine feeds in as
built-ins such as `LIFETIME`, `EMISSION_TRANSFORM`, `RESTART_*`), and the whole
draw step: the `QuadMesh` size and its `StandardMaterial3D` (unshaded,
`BILLBOARD_PARTICLES`, `vertex_color_use_as_albedo`, transparency, blend mode,
fog) and the gradient texture. The colour this shader writes to `COLOR` only
shows because the draw material uses vertex colour as albedo.

## Effect B wiring and state test (Step 5 session, 2026-11-07)

`entities/fire_pit.gd`: the two code-made `CPUParticles3D` are replaced by one
`effects/fire_pit_flames.tscn` instance; `_show_fuel()` reads `burn_left` and
sets only `emitting` and `amount_ratio = 0.3 + 0.7·clamp(burn_left/120, 0, 1)`
on both emitters (a fire lit from cold is `restart()`ed so preprocess applies);
`_ready` ends with `_set_lit(lit())` so a pit fuelled before it enters the tree
starts lit. `burn_left`, `feed()`/`burn()` arithmetic, warmth, the model and
the Glow halo are unchanged; reviewed by the main session.

`./scripts/run-test.sh test_fire_pit_flames_state.gd 60 600` — fixed 60 fps,
headless; real `main.tscn`, seed 2026 + `seed_rng`, 萨米 floor, pit 1.
Feeding only by a real E key event and a real click on the fuel picker row;
burning only through the physics loop. Result: **0 failures**
(`logs/test_fire_pit_flames_state_60fps.log`). A per-frame monitor checked
11 846 samples (352 distinct ratios): `emitting == (burn_left > 0)`,
`amount_ratio == mapping` (±1e-4), `amount` 24/10 every frame.

| Rule | Asserted |
|---|---|
| B1 | on the sample where `burn_left` first goes 0→>0 (E + plank, ~60) both emitters emit; same for a relight (solid fuel, ~120) |
| B2 | on the sample where it reaches 0 in the loop both stop; still stopped 2.3 s later, ratio 0.3 |
| B3 | ratio = mapping after feeding (0.65), burning (0.59), refuelling (≈1.0), clamped at 180 (1.0); `amount` never changes |
| B4 | tree paused: `burn_left` frozen, state unchanged, emitters `can_process() == false`, still frozen 30 frames on; Esc pause menu: `simulation_active()` false, tree not paused, fuel frozen, GPU nodes keep processing |
| B5 | pit hidden, and effect root hidden: state keeps following `burn_left`; shown again at the current ratio |
| B6 | rest-stop campfire (fed 300 at load): first sampled frame both emitting, ratio 1.0 (route column set to "rest" as a fixture, then the real `advance(0)`) |

Headless `emitting` on these continuous emitters reads back correctly (true
while lit, false after); only one-shot emitters misreport (r1 b).
Not driven: the boss hammer's `burn()` and the arena's first fire (same code
paths). Not provable headlessly: preprocess on the first drawn frame, the die-out
on screen, freezing on screen, nothing drawn while hidden.

After wiring, the fixture strip `captures/fire_pit_flames/r1-wired/` is
pixel-identical in warm-pixel counts to r1 (12:170 40:164 54:162 70:108 99:33
105:27, 10/130/175: 0): the in-game pit draws exactly what the fixture did.

All suites in parallel after the change (`logs/baseline-after-step5/summary.txt`):
**82 of 93** (both new B suites pass). Versus after-step3: `test_elevation`
FAIL→PASS (load-sensitive); `test_arenas` PASS→FAIL on three 血债 values, passes
alone (85/0). The other ten failures are the known pre-existing ones. No
existing test reads the old `_flames`/`_embers`.

## Headless CPU price (Step 7 session, 2026-11-07)

`./scripts/run-test.sh cost_effects.gd 60 300` (fixed 60 fps, headless;
`tests/cost_effects.gd`, adapted from Example 09's `particle_cost.gd`;
log `logs/cost_effects_60fps.log`). Metric: wall-clock time between consecutive
frames; 60 warm-up + 300 timed frames, 5 rounds, the four game cases
interleaved with rotating order and each compared with the same round's
effects-off control. 萨米 floor 1, seed 2026 (+ `seed_rng`), 3 pits, 89 enemies.

| Case | Mean ms/frame | sd over rounds | vs effects off (paired) |
|---|---|---|---|
| empty scene (control) | 0.0032 | 0.0001 | — |
| game, both effects off | 7.6759 | 0.0498 | — |
| A, 8 HitSparks alive (7–8 at any time, 73 added per window) | 7.7008 | 0.0606 | +0.025 ± 0.029 |
| B, one pit at ratio 1.0 | 7.6627 | 0.0446 | −0.013 ± 0.078 |
| B, all 3 pits at ratio 1.0 | 7.7380 | 0.1336 | +0.062 ± 0.114 |

Instrument check: empty and game differ 2400×, and the empty frame (3 µs) is far
below the 6.9 ms low-processor sleep that made the chapter's script report one
number for every case, so the script measures the scene, not itself. The
effect cases are **not distinguishable** from the effects-off control (each
within two standard errors of zero) even though the sparks and fires were
really alive (+36 nodes for A). Headless runs a dummy renderer: no particle
process, no draw; only node bookkeeping (HitSpark's age counter and spawn/free,
the pit's `amount_ratio` writes and glow flicker) reaches the CPU, which is
microseconds against a 7.7 ms game frame. Consistent with the brief's
predictions (A +0.02, B +0.005/+0.02 ms) but not resolvable; it says nothing
about the GPU budgets, which are judged on Visual Profiler GPU time.
`Performance.TIME_PROCESS`/`TIME_PHYSICS_PROCESS` were tried and rejected (they
summed to more than the frame headless). The floor has 3 pits, not the 4 the
brief priced.

## GPU price (human check, windowed, 2026-11-07)

**Executor: the user**, in the Godot 4.7.2 editor, running `previews/gpu_price.tscn`
(fixture; F6) with Debugger → Visual Profiler, on **NVIDIA GeForce RTX 4060
Laptop GPU** (CPU AMD Ryzen 9 7940HX), D3D12 / Forward+, 1280×720, vsync on.
Keys U / I / O toggle Effect A at peak (≈8 HitSparks alive), Effect B (all 3
pits at 300 s, ratio 1.0) and vsync. (F7/F8 were tried first: they are the
editor's pause/stop for a running scene, found by the user; keys moved.)
The table reads one selected frame per state, from the user's screenshots in
`evidence/a6/gpu/`.

| State | Render Viewport GPU (whole frame) | `Update GPU Particles` GPU (the process step) | Screenshot |
|---|---|---|---|
| both off | 3.73 ms | row absent | `visual_profiler_round3_both_off.png` |
| A on (≈8 bursts) | 3.71 ms | **0.14 ms** | `visual_profiler_round2_U_A_on.png` |
| B on (3 pits full) | 3.68 ms | **0.09 ms** | `visual_profiler_round2_I_B_on.png` |

- The whole-frame difference (−0.02 / −0.05 ms) is smaller than frame-to-frame
  variation (round-1 frames read 3.7–10.7 ms), so the whole-frame on/off
  comparison cannot resolve either effect from single frames.
- The `Update GPU Particles` row exists only while these GPU effects run (every
  other particle system in the game is a `CPUParticles3D`), so it is a direct
  reading of their process step on the GPU.
- **Budget:** A 0.14 ms ≤ 0.25 ms; B 0.09 ms (3 pits) ≤ 0.15 ms (budget set for
  4 pits). Both within budget on the process step. Predicted 0.05 / 0.06 ms:
  the readings are about 2–3× the prediction.
- **Not measured:** the draw step (particles' share of the transparent pass was
  not isolated in the screenshots), averages over many frames, and the vsync-off
  FPS comparison (optional; not done).
