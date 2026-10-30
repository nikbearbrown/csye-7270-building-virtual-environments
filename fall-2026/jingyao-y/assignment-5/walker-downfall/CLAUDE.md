# CLAUDE.md — downfall-godot

## Project context

- Engine: Godot 4.7 (`project.godot:16`); the wrapper runs
  `../Godot_v4.7.2-stable_win64_console.exe` (`scripts/run-test.sh:8`). The Godot
  project is the repository root (`--path .`, `scripts/run-test.sh:11`).
- Renderer: Forward+. `project.godot` names no `rendering_method`, so the default
  applies; it sets the Windows driver to D3D12 (`project.godot:27`). Confirmed
  at run time as `forward_plus` / `d3d12` (`CHANGE-BRIEF.md:27-31`; headless:
  `logs/a5_probe_headless_60fps.log`). `README.md:3` still says "GL Compatibility"
  from Assignment 2; that is out of date. The visual suites force
  `gl_compatibility` (`tests/run_all.ps1:70`); they are not used for A5.
- Main scene: `res://game/main.tscn` (`project.godot:15`), one `PixelDisplay` node
  (`game/main.tscn:5-6`) that renders the 3D world in a `SubViewport` and creates
  the `GameManager` (`game/pixel_display.gd:22`, `game/pixel_display.gd:44`).
- Field look: the field `Environment` is built by `field_environment()` from
  `base_environment()` when `apply_scene_look(false)` runs: ACES tonemap, SSAO,
  SSIL, glow, fog, adjustment (`game/game_manager.gd:6536-6562`,
  `game/game_manager.gd:6588-6603`, `game/game_manager.gd:6620`).
- Shaded object (shader from code): the burning-bottle fire is a `GroundHazard`
  (`entities/ground_hazard.gd:1-2`, `extends Node3D`), made in code by
  `GameManager.spawn_hazard()` (`game/game_manager.gd:794-805`), called when the
  bottle lands with `fuse` 0 and `lasting = fire_time` (`entities/molotov.gd:66-67`).
  Today the fire is only a `Decal` with code-made circle textures
  (`entities/ground_hazard.gd:31-39`, `entities/ground_hazard.gd:52-60`). The new
  flame mesh is added beside the Decal (`CHANGE-BRIEF.md`, "The shader").
- Game state: `fuse` and `lasting` on `GroundHazard` (`entities/ground_hazard.gd:14-15`),
  counted down by physics `delta` in `_physics_process()` only while
  `game.simulation_active()` is true (`entities/ground_hazard.gd:62-78`,
  `game/game_manager.gd:386-387`); the node frees itself at `lasting <= 0`
  (`entities/ground_hazard.gd:78`). Duration: `fire_time` 3.0 (`game/enemy_attacks.gd:34`),
  0 when the thrower is silenced (`entities/enemy.gd:1200`). The same class with
  `lasting` 0 draws the slug burst and a boss's last rite (`entities/enemy.gd:1443`,
  `entities/boss.gd:347`); those are not fires.
- Textured-shader object: the base crate, prop `"crate"` (`world/base_map.gd:90`),
  from `res://art/kit/base_crate.glb` (`world/base_map.gd:57`). Its current material:
  `TerraceDressing.kit_mesh()` moves each glb surface's baked albedo/normal textures
  into a `ShaderMaterial` on `world/kit_piece.gdshader` (`world/terrace_dressing.gd:38`,
  `world/terrace_dressing.gd:933-955`); `BaseMap._place_kit()` then overrides it with
  `world/base_kit_see_through.gdshader` (`world/base_map.gd:58`,
  `world/base_map.gd:1744-1766`), shared per room while `_share_materials` is set
  (`world/base_map.gd:519`, `world/base_map.gd:829-831`). The judging fixture
  `res://tests/material_review.tscn` is planned, not yet made (`CHANGE-BRIEF.md`, "Material plan").
- Tests: always through the wrapper, which runs `--headless --path . --script
  res://tests/<file> --fixed-fps <fps>`, logs to `logs/<name>_<fps>fps.log`, and
  fails on a non-zero exit or any `SHADER ERROR` / `SCRIPT ERROR` line
  (`scripts/run-test.sh:10-14`). It does not read `FAIL` lines, so every suite must
  exit non-zero on failure, as existing ones do (`tests/test_new_enemies.gd:59`).
  - Existing thrower/bottle/fire suite: `./scripts/run-test.sh test_new_enemies.gd 60`
  - New A5 tests, each at three rates (`CHANGE-BRIEF.md`, R3):
    `./scripts/run-test.sh <test>.gd 30`, `... 60`, `... 144`
  - Slow suites (test_bosses, test_elevation, test_layout, test_run_save, test_v1):
    `TEST_TIMEOUT=1200 ./scripts/run-test.sh <test>.gd 60` (`logs/baseline/summary.txt`).
  - Baseline at 60 fps: 70 of 73 pass. `test_combat` and `test_loading_screen` fail
    only under `--fixed-fps`; `test_item_icons` fails either way. These are
    pre-existing; do not "fix" them in this change (`logs/baseline/summary.txt`).

## Headless facts

Measured on this machine by `tests/a5_probe_headless.gd` at 30, 60 and 144 fps
(`logs/a5_probe_headless_{30,60,144}fps.log`):
- Headless reports `forward_plus` / `d3d12` but the video adapter name is empty: it
  is a dummy renderer and draws nothing. No headless run shows what the screen shows.
- `Shader.get_shader_uniform_list()` works headlessly: names, types and hints
  (`hint_range` comes back as its hint string). Defaults are not reported:
  `RenderingServer.shader_get_parameter_default()` and an unset
  `ShaderMaterial.get_shader_parameter()` both return null. Read defaults from the
  `.gdshader` source text.
- A shader with a missing semicolon prints `SHADER ERROR: Expected a ';'.` and its
  uniform list is empty; the wrapper then exits 1.
- `set_shader_parameter()` with an undeclared name raises nothing and reads back the
  stored value; a value of 2.0 on a `hint_range(0.0, 1.0)` uniform reads back as 2.0.
  Only the uniform-list assertion catches a renamed uniform. What the GPU receives
  for 2.0 needs a rendered capture.
- `--fixed-fps` fixes the process step; physics stays at 60 Hz. After 144 process
  frames: 30 fps gives 287 physics ticks in 4.79 s, 60 fps gives 144 ticks in 2.40 s,
  and 144 fps gives 60 ticks in 1.01 s.

## Current change

@CHANGE-BRIEF.md

## Ownership

- Files in `shaders/` (`res://shaders/`) are hand-written by the human and are never
  edited by an agent: create, edit, reformat or "fix" none of them. That includes the
  planned `burning_bottle_fire.gdshader` and `cargo_panel.gdshader`, and the
  hint-experiment shader. If one looks wrong, say so and stop.
- `scripts/run-test.sh` is not edited by an agent either.

## Out of scope

- Gameplay: damage formulas, the bottle's direct hit, fire tick damage and who it
  hurts, `GroundHazard.TICK` 0.5, first-tick timing, the 3.0 s fire life, radius 1.3,
  the 0.6 s bottle flight, and silence zeroing `fire_time`.
- Collision, movement, input, the enemy state machine and its timings, and the
  expected values in every existing test.
- The Decal scorch keeps its texture, colour, projection and lifetime; the flame mesh
  only draws flames. Slug bursts and boss last rites get no flame; their `Warning`
  markers, burst VFX and scene lighting stay as they are.
- The driver reads `fuse`, `lasting`, the cached initial duration and the pause state.
  It never writes game state, deals damage, or uses its own timer for the hazard's life.
- Calibration settings (Linear tonemap, post-processing off) are for one-off capture
  runs: copy the Environment, restore it afterwards, never save them as defaults.
- No changes to `project.godot` renderer/driver settings or to the existing
  `world/*.gdshader` and `game/*.gdshader` files.

## Unconfirmed

- `AGENTS.md` does not exist, so there is no `@AGENTS.md` line. `shaders/` does not exist yet.
- Whether the `crate` model's UVs suit the planned textures, and where crates stand in
  the base, are not checked yet.
- Whether shader `TIME` follows `Engine.time_scale` is a prediction in the brief (R5),
  not yet measured.
- The working tree has many uncommitted edits (`git status`), so line numbers in this
  file can drift; recheck them before citing.
