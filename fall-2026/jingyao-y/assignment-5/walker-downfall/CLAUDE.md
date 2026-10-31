# CLAUDE.md — downfall-godot

## Project context

- Engine: Godot 4.7 (`project.godot:16`); the wrapper runs
  `../Godot_v4.7.2-stable_win64_console.exe` (`scripts/run-test.sh:8`). The Godot
  project is the repository root (`--path .`, `scripts/run-test.sh:11`).
- Renderer: Forward+. `project.godot` names no `rendering_method`, so the default
  applies; it sets the Windows driver to D3D12 (`project.godot:27`). Confirmed
  at run time as `forward_plus` / `d3d12` (`CHANGE-BRIEF.md:27-31`; headless:
  `logs/a5_probe_headless_60fps.log`). README now documents Forward+.
  The older visual suites force
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
  The fire keeps its `Decal` with code-made circle textures and adds a `FireFlame`
  mesh when `fuse <= 0` and `lasting > 0`. FireFlame uses a separate ShaderMaterial
  per fire, reads lasting after the hazard's physics update, and faces the camera.
- Game state: `fuse` and `lasting` on `GroundHazard` (`entities/ground_hazard.gd:14-15`),
  counted down by physics `delta` in `_physics_process()` only while
  `game.simulation_active()` is true (`entities/ground_hazard.gd:62-78`,
  `game/game_manager.gd:386-387`); the node frees itself at `lasting <= 0`
  (`entities/ground_hazard.gd:78`). Duration: `fire_time` 3.0 (`game/enemy_attacks.gd:34`),
  0 when the thrower is silenced (`entities/enemy.gd:1200`). The same class with
  `lasting` 0 draws the slug burst and a boss's last rite (`entities/enemy.gd:1443`,
  `entities/boss.gd:347`); those are not fires.
- Textured-shader objects: the two hall `crate_stack` props at layout x=98.0
  and x=101.5 (`world/base_map.gd`, CARGO_PANEL and the hall prop table).
  `BaseMap._place_kit()` assigns `cargo_panel_mild.tres` and
  `cargo_panel_weathered.tres` to surface 0; the clasps retain their kit material.
  Both materials share `shaders/cargo_panel.gdshader` and the three cargo textures.
  The judging fixture `res://tests/material_review.tscn` exists and supplies
  separate review and raking lights. `MATERIALS.md` records its UV and lighting limits.
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

- The earlier prompts reserved shader edits for the student. The current explicit
  user instructions authorized Codex to write the three custom shaders, perform
  mutations/restoration and complete A5 through scripts. Preserve the exact brief
  color statement and current interfaces; follow the user's current authorization
  for subsequent edits. SOURCES.md records the actual assistance.
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

- `AGENTS.md` does not exist, so there is no `@AGENTS.md` line. `shaders/` now contains
  the fire, cargo, hint-experiment and generated comparison programs.
- The selected `crate_stack` surfaces have UVs and tangents; the base placement,
  BoxMesh UV magnification and texture response are recorded in `MATERIALS.md`.
- Shader TIME was measured with the real renderer: 120 fixed-60-fps frames advance
  TIME by 2/1/4/0 seconds at time_scale 1/0.5/2/0. See TEST-REPORT.md and
  evidence/a5/use-it/measurement.json. The menu's simulation_active pause is separate.
- The working tree has many uncommitted edits (`git status`), so line numbers in this
  file can drift; recheck them before citing.
