# CLAUDE.md — downfall-godot

## Project context

- Engine: Godot 4.7 (`project.godot:16`, `config/features=PackedStringArray("4.7")`);
  the test wrapper runs `../Godot_v4.7.2-stable_win64_console.exe` (`scripts/run-test.sh:8`).
  The Godot project is the repository root (`project.godot` at root; `--path .` in `scripts/run-test.sh:11`).
- Renderer: `project.godot` sets no `rendering_method`; it only sets the Windows
  driver `rendering_device/driver.windows="d3d12"` (`project.godot:27`). A runtime
  check recorded in `CHANGE-BRIEF.md:27-31` read `renderer=forward_plus`, `driver=d3d12`.
  The visual suites in `tests/run_all.ps1:70` force `--rendering-method gl_compatibility`.
- Main scene: `res://game/main.tscn` (`project.godot:15`), a single `PixelDisplay` node
  (`game/main.tscn:5-6`) whose script renders the 3D world in a `SubViewport`
  and creates the `GameManager` (`game/pixel_display.gd:22`, `game/pixel_display.gd:44`).
- Field environment: created in `game/game_manager.gd:6500-6509`; in the field
  `apply_scene_look(false)` swaps in `field_environment()` (`game/game_manager.gd:6620-6630`),
  built from `base_environment()`: ACES tonemap, SSAO, SSIL, glow, fog, adjustment
  (`game/game_manager.gd:6536-6562`, `game/game_manager.gd:6588-6603`).
- How the shaded object is drawn: the burning-bottle fire is a `GroundHazard`
  (`entities/ground_hazard.gd:1-2`, `extends Node3D`). It has no `.tscn`; it is made in
  code by `GameManager.spawn_hazard()` (`game/game_manager.gd:794-805`), called from
  `Molotov._land()` with `fuse` 0 and `lasting = fire_time` (`entities/molotov.gd:66-67`).
  Today the fire is only a `Decal` with a code-made circle texture and emission
  texture (`entities/ground_hazard.gd:31-39`, `entities/ground_hazard.gd:52-60`).
- State that drives the effect: `fuse` and `lasting` on `GroundHazard`
  (`entities/ground_hazard.gd:14-15`), counted down by physics `delta` in
  `_physics_process()` only while `game.simulation_active()` is true
  (`entities/ground_hazard.gd:62-78`, `game/game_manager.gd:386-387`); the node frees
  itself when `lasting <= 0` (`entities/ground_hazard.gd:78`). Fire duration
  comes from `fire_time` 3.0 (`game/enemy_attacks.gd:34`), zeroed when the thrower is
  silenced (`entities/enemy.gd:1200`). Non-fire users of the same class
  (`lasting` 0): `entities/enemy.gd:1443`, `entities/boss.gd:347`.
- 3D object for the textured shader: the base crate, prop model `"crate"`
  (`world/base_map.gd:90`), loaded from `res://art/kit/base_crate.glb`
  (`KIT` pattern at `world/base_map.gd:57`; file listed in `art/kit/`).
  Material origin: `TerraceDressing.kit_mesh()` takes each glb surface's baked
  `BaseMaterial3D` albedo/normal textures into a `ShaderMaterial` using
  `res://world/kit_piece.gdshader` (`world/terrace_dressing.gd:38`,
  `world/terrace_dressing.gd:933-955`); `BaseMap._place_kit()` then overrides each surface
  with a `ShaderMaterial` on `res://world/base_kit_see_through.gdshader`, copying
  `albedo_tex`/`normal_tex`, possibly shared per room (`world/base_map.gd:58`,
  `world/base_map.gd:1744-1766`). Baked textures: `art/kit/base_crate_base_crate_body.png`,
  `..._label.png` and their `_normal.png` files.
  The planned review fixture is `res://tests/material_review.tscn` (`CHANGE-BRIEF.md:225`; does not exist yet).
- Tests: every test goes through `scripts/run-test.sh <test-file.gd> <fps>`, which runs
  Godot `--headless --path . --script res://tests/<file> --fixed-fps <fps>`, logs to
  `logs/<name>_<fps>fps.log`, and fails on a non-zero exit or a `SHADER ERROR`/`SCRIPT ERROR`
  line (`scripts/run-test.sh:2`, `scripts/run-test.sh:10-14`). Suites are `extends SceneTree`
  and `quit(1 if failures else 0)` (`tests/test_new_enemies.gd:1`, `tests/test_new_enemies.gd:59`).
  - Existing thrower/Molotov/GroundHazard regression (`tests/test_new_enemies.gd:227-247`):
    `bash scripts/run-test.sh test_new_enemies.gd 60`
  - R3 timing tests, per `CHANGE-BRIEF.md:104-106`, at three fixed render rates:
    `bash scripts/run-test.sh <fire_test>.gd 30`
    `bash scripts/run-test.sh <fire_test>.gd 60`
    `bash scripts/run-test.sh <fire_test>.gd 144`
  - Long suites: `TEST_TIMEOUT=600 bash scripts/run-test.sh <test>.gd 60` (`scripts/run-test.sh:5`, `scripts/run-test.sh:11`).

## Current change

@CHANGE-BRIEF.md

## Ownership

- Files in `shaders/` (`res://shaders/`) are hand-written by the human and are never
  edited by an agent. This includes the planned `res://shaders/burning_bottle_fire.gdshader`
  and `res://shaders/cargo_panel.gdshader` (`CHANGE-BRIEF.md:44`, `CHANGE-BRIEF.md:234`).
  An agent does not create, edit, reformat or "fix" them; report a problem instead.

## Out of scope

- Gameplay: damage formulas, the bottle's direct hit, fire tick damage, who gets hurt,
  `GroundHazard.TICK` 0.5, first-tick timing, the 3.0 s fire life, radius 1.3,
  the 0.6 s bottle flight, and silence setting `fire_time` to 0.
- Collision, movement, input, the enemy state machine, windup/recovery, and the
  expected values in existing tests.
- The existing Decal scorch: its texture, colour, projection and lifetime stay as they are;
  the new flame mesh sits beside it and only draws flames.
- Slug bursts and boss last rites (`lasting` 0) get no flame; their `Warning`
  markers, burst VFX, other objects and scene lighting are untouched.
- The display driver only reads `fuse`, `lasting`, the cached initial duration and the pause
  state. It never writes game state, deals damage or uses its own timer to decide
  the hazard's life.
- Calibration settings (Linear tonemap, post-processing off) are for one-off capture runs only:
  copy the Environment, restore it afterwards, and never save them as game defaults.
- No changes to `project.godot` renderer/driver settings or to the existing
  `world/*.gdshader` files.

## Unconfirmed

- `AGENTS.md` does not exist, so there is no `@AGENTS.md` line. `shaders/` does not exist yet.
- Renderer: the file sets no `rendering_method`. Forward+ comes from the runtime check in
  `CHANGE-BRIEF.md:27-31`, which I did not re-run. `README.md:3` says "GL Compatibility",
  which conflicts with that.
- I did not run Godot, so I have not confirmed that `scripts/run-test.sh` or
  `test_new_enemies.gd` currently pass. Headless runs use a dummy renderer and cannot
  prove pixels. The wrapper does not grep `FAIL ` lines; it relies on the suite's exit code.
- The R3 fire test file name is not decided yet; `<fire_test>` above is a placeholder.
- `git status` shows many uncommitted edits (including `game/game_manager.gd`,
  `entities/enemy.gd`, `game/enemy_attacks.gd`), so line numbers can drift.
- I did not confirm where the `"crate"` model is placed in the base, whether its UVs suit
  the planned textures, or whether `_share_materials` makes crates in one room share a material.
- I read only the thrower-related tests (`tests/test_new_enemies.gd`) and `tests/run_all.ps1`,
  not all 168 files in `tests/`. A grep found GroundHazard/Molotov only in `test_new_enemies.gd`.
- `CHANGE-BRIEF.md:144` says the measuring script still writes to the old path outside the repo.
