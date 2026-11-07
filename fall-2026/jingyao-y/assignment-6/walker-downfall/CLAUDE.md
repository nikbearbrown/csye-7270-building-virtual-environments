# CLAUDE.md — downfall-godot (Assignment 6: particle effects)

## Project context

- Engine: Godot 4.7.2-stable. The wrapper runs `Godot_v4.7.2-stable_win64_console.exe`, five
  folders above the repo, in `D:\CSYE 7370` (`scripts/run-test.sh:11`; `CHANGE-BRIEF.md:9`).
  `project.godot:16` records only the feature tag "4.7". The repo root is the Godot project
  (`--path .`, `scripts/run-test.sh:10,19`).
- Renderer: Forward+ with D3D12 on Windows (`README.md:3`, `CHANGE-BRIEF.md:9`). `project.godot`
  sets no `rendering_method`, only `driver.windows="d3d12"` (`project.godot:24-27`).
  `tests/run_all.ps1:70` forces `gl_compatibility` for older visual suites; the wrapper doesn't.
- Main scene: `res://game/main.tscn` (`project.godot:15`), which holds one `PixelDisplay`
  (`game/main.tscn:5-6`). That node makes a `SubViewport`, creates the `GameManager` and adds it
  to the viewport (`game/pixel_display.gd:22,44,80`). Field maps are built in code, not scenes.
- Effect A `hit_spark`: three `GPUParticles3D` under a `Node3D` named `HitSpark`, in
  `res://effects/hit_spark.tscn` (`CHANGE-BRIEF.md:44-48,94`).
  - Event: a landed operator melee hit, a direct call, not a signal. Each site in
    `entities/player.gd` calls `CombatVfx.spawn(game, <enemy>.global_position, direction,
    "spark"|"amiya_spark")`: the basic hit in `attack_direction()` (`:838`, `:901-914`);
    拉普兰德's cross cut in `_lappland_cross()` (`:947-962`); 阿米娅's cut in `_amiya_cut()`
    (`:1762-1768`). Her later cuts are queued 0.08 s apart (`:80`, `:1756-1758`, `:1798-1802`).
  - The current spark is not a particle system: unlit meshes in `game/combat_vfx.gd:163-192`.
  - Signal `Enemy.died(enemy)` (`entities/enemy.gd:12`) fires at `:1500`, before `queue_free()`
    (`:1501`). Appears on field floors under the `GameManager` (`CHANGE-BRIEF.md:132-133`).
- Effect B `fire_pit_flames`: two `GPUParticles3D` under a `Node3D` named `FirePitFlames`, in
  `res://effects/fire_pit_flames.tscn` (`CHANGE-BRIEF.md:200-201,237`). It replaces the
  code-made `CPUParticles3D` "Flames" and "Embers" (`entities/fire_pit.gd:18-19,37-42,74-103`).
  - Condition: `FirePit.burn_left` (`entities/fire_pit.gd:17`). The pit is lit while `lit()`
    is true (`burn_left > 0`, `:105-106`). `FirePit` declares no signals.
  - Fuel goes up through `feed()` (`:113-115`). Callers: the player picking fuel with E
    (`game/gm_features.gd:227`), the boss arena's first fire (`:152`), and the camp rest fire
    (`game/gm_route.gd:225`).
  - Fuel goes down through `burn()` (`entities/fire_pit.gd:117-120`). Callers: `_tick_features()`
    (`game/gm_features.gd:114-116`), which `GameManager._physics_process()` runs only while
    `simulation_active()` is true (`game/game_manager.gd:441-442,848-853`); and the boss hammer
    (`entities/boss.gd:1724-1728`).
  - Constants: `FIRE_RADIUS` 4.5 and `FIRE_MAX` 300 (`game/feature_catalog.gd:91,95`).
  - Appears on 萨米 (`snow`) floors only (`game/gm_features.gd:143`). Pits are added in code
    under `world_map._generated_root`: ordinary floors (`:180-182`), the boss arena
    (`:145-152`) and the camp rest stop (`game/gm_route.gd:218-226`).
- Tests: always run through the wrapper: `./scripts/run-test.sh <file>.gd <fps|realtime> [timeout_s]`.
  - It runs `--headless [--fixed-fps N] --path . --script res://tests/<file>`, logs to
    `logs/<name>_<N>fps.log` or `logs/<name>_realtime.log`, and times out after `$3`, else
    `TEST_TIMEOUT`, else 120 s. A non-zero exit or a `SHADER ERROR`/`SCRIPT ERROR` line fails
    the run (`scripts/run-test.sh:2,13-22`). Suites `extends SceneTree` and `quit(1)` on
    failure (`tests/test_new_enemies.gd:1,61`; `tests/test_map_features.gd:1,36`).
  - Existing suites are pinned at 60 fps (`scripts/run-baseline.sh:3,14`), e.g.
    `./scripts/run-test.sh test_map_features.gd 60` (fire pits). Realtime mode drops
    `--fixed-fps`: `./scripts/run-test.sh <file>.gd realtime` (`scripts/run-test.sh:6,13-14`).
  - Slow suites need a 1200 s timeout, e.g. `./scripts/run-test.sh test_bosses.gd 60 1200`:
    test_bosses, test_elevation, test_layout, test_run_save, test_v1 (`scripts/run-baseline.sh:10,13`).
  - Baseline: `./scripts/run-baseline.sh <label> [jobs]` writes
    `logs/baseline-<label>/summary.txt` (`scripts/run-baseline.sh:2-20`).
  - The brief names four new suites, none written yet: `test_hit_spark_config.gd`,
    `test_hit_spark_state.gd` (60), `test_fire_pit_flames_config.gd` and
    `test_fire_pit_flames_state.gd` (60) (`CHANGE-BRIEF.md:92,149,235,296`).

## Current change

@CHANGE-BRIEF.md

## Ownership

- Shaders: earlier prompts reserved shader edits for the student, and the user later
  explicitly authorized the agent for the A5 shaders. In A6, existing files in `shaders/` stay
  unchanged; only `shaders/particles_generated.gdshader` may be added, in Step 6
  (`CHANGE-BRIEF.md:392-394`). SOURCES.md records the actual assistance.
- Agents do not edit `scripts/run-test.sh`.
- Effect settings live in scene files in `effects/`, not in code. Scripts only instance,
  restart or free the effects and set `emitting`/`amount_ratio` from game state.

## Godot 4 names

- Use Godot 4 classes: `GPUParticles3D`, `ParticleProcessMaterial`, `StandardMaterial3D`
  (`BaseMaterial3D` enums), `QuadMesh`, `Gradient`, `GradientTexture2D`, `Curve`, `CurveTexture`.
- Never use Godot 3 names: `Particles`, `ParticlesMaterial`, `SpatialMaterial`,
  `flags_unshaded`, `params_billboard_mode`, `scale_random`.
- Confirmed in 4.7.2 by `tests/a6_probe_headless.gd` (`logs/a6_probe_headless_60fps.log`): every
  property and enum the brief names exists, including `BILLBOARD_PARTICLES`, `BLEND_MODE_MIX`,
  `EMISSION_SHAPE_SPHERE`, `GradientTexture2D.FILL_RADIAL`, `turbulence_*`, `amount_ratio`.
  `CPUParticles3D` has no `amount_ratio`; `ParticlesMaterial` and `scale_random` do not exist.
- Trap: `initial_velocity` and `scale` still exist as Vector2 compatibility properties that
  map onto `*_min/*_max`. Write `initial_velocity_min/max` and `scale_min/max` anyway.

## Headless facts

Measured by `tests/a6_probe_headless.gd` (`logs/a6_probe_headless_60fps.log`):
- A headless run uses a dummy renderer (adapter name empty): it draws no particles and runs
  no GPU particle process. Node state (amount_ratio, visibility, instance counts) is
  observable; the look is not.
- A one-shot `GPUParticles3D` reads `emitting == false` from the first frame after it is set,
  and `finished` never fires headlessly. Do not use either to free or count bursts in a test.
- A GPU effect's headless CPU price is near zero by construction (predicted; the cost script
  in Step 7 measures it against an empty-scene control).
- Frame strips come from a windowed Movie Maker run, which the agent starts.

## Out of scope

- Hit gameplay: damage, hitstop, aggro, charge, hit timing, which hits land, and the `Enemy`
  kill and `queue_free()` path.
- Fuel: `burn_left` and every rule that reads or writes it (warmth, cold, fuel values,
  `FIRE_RADIUS`/`FIRE_MAX`, the hammer cost, the burn loop). Presentation reads state only.
- Collision, movement, input, the player/enemy state machines and timings, and the expected
  values in every existing test.
- The mesh `CombatVfx` spark and the fire pit model and `Glow` halo stay. No effect on ranged
  hits, enemy-to-player hits or misses.
- Other code-made particles (shower, traces, boss VFX, weather), A5 shaders and materials,
  source textures, the `project.godot` renderer/driver settings and `scripts/run-test.sh`.

## Unconfirmed

- `rendering_method` is left at the default; the probe reports `forward_plus`/`d3d12` headless.
  The GPU (RTX 4060) is from memory until the Visual Profiler run names it.
- `effects/`, `previews/` and the four new test files do not exist yet. The baseline is in
  `logs/baseline-before/summary.txt`.
- The brief's flames (24, 0.8 s) differ from today's CPU flames (18, 0.7 s,
  `entities/fire_pit.gd:37`) on purpose. Line numbers drift; recheck before citing.
