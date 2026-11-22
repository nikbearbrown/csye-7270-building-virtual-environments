# CLAUDE.md — downfall-godot (Assignment 7: two animations)

## Project context

- Engine: Godot 4.7.2-stable. The wrapper runs `Godot_v4.7.2-stable_win64_console.exe` five
  folders above the repo (`scripts/run-test.sh:11`); `project.godot:16` records only "4.7".
  The repo root is the Godot project: `--path .` (`scripts/run-test.sh:10,19`).
- Renderer: Forward+, D3D12, RTX 4060 Laptop GPU (engine, windowed: `logs/a7_renderer_windowed.log:1`).
  `project.godot` sets only `rendering_device/driver.windows="d3d12"` (`:27`), no
  `rendering_method` and no `physics_ticks_per_second` (default 60, `CHANGE-BRIEF.md:14-15`).
- Main scene `res://game/main.tscn` (`project.godot:15`) is one `PixelDisplay` node
  (`game/main.tscn:5-6`). Everything else is built in code: `GameManager` adds
  `ContinuousWorldMap` and `BaseMap` (`game/game_manager.gd:379-382`) and the `Player`
  (`:5857-5861`). Other scenes: `effects/*.tscn`, `tests/*.tscn`, `art/models/asset_preview.tscn`;
  `animations/` does not exist yet.
- Player state machine: `entities/player.gd`, no state enum; state is fields read in
  `_physics_process` (`:478`): `swing_remaining` (`:143`), `_attack_cooldown` (`:140`),
  `sword_charge` (`:168`), `hitstop_remaining`/`dash_remaining` (`:170-171`), `control_timer`
  (`:236`). Swing `attack_direction()` (`:838`); release test `:849`; spawn on the click tick
  (`:879-899`); interrupts `interrupt_actions_for()` (`:698-709`); Lappland only
  `has_sword_wave()` (`:775-776`). Her sprite is `_sprite: LapplandAnimator3D` (`:160`, `:271`),
  `extends AnimatedSprite3D` (`godot_assets/lappland_animator_3d.gd:1-2`), `ACTIONS.wave =
  [10, 3]` (`:43`), own clock `action_time += delta` in `_process` (`:217`, `:229`).
- Clip 1 `npc_idle` (`CHANGE-BRIEF.md:47-68,134-151`): route Sprite3D + AnimationPlayer frame
  track. Planned node `res://animations/npc_idle.tscn`: `NpcIdle` (Sprite3D) / `AnimationPlayer`,
  library `""`, clip `idle`, autoplay. Today: `FieldArt.npc_idle()` builds `SpriteFrames` in
  code (`art/field_art.gd:162-183`). Appears in the base store as `store/Closure`
  (`world/base_map.gd:762-770`) and in field set pieces (`world/continuous_world_map.gd:2681-2724`;
  kinds chosen at `:2498-2504`), both built in code, not in scene files.
- Clip 2 `wave_release` (`CHANGE-BRIEF.md:70-109,153-182`): route 2D cutout rig keyed as
  resource text, in a `SubViewport` drawn by a `Sprite3D` billboard. Planned node
  `res://animations/lappland_wave_rig.tscn`: `WaveRig` / `AnimationPlayer` (`root_node =
  ../Viewport/Rig`, clips `RESET`, `wave_release`). Instanced on the `Player` (child of
  `GameManager`, `game/game_manager.gd:5861`); swings need `simulation_active()`
  (`entities/player.gd:841`), so it plays on field floors, not in the base walk.
- Tests, always through the wrapper: `./scripts/run-test.sh <file>.gd <fps|realtime> [timeout_s]`
  (`scripts/run-test.sh:2`): `--headless [--fixed-fps N] --path . --script res://tests/<file>`,
  log `logs/<name>_<N>fps.log`/`_realtime.log`; timeout `$3`, else `TEST_TIMEOUT`, else 120 s;
  fails on non-zero exit, `SHADER ERROR`, `SCRIPT ERROR`, `Failed loading resource` (`:13-22`).
  - Realtime drops `--fixed-fps`: `./scripts/run-test.sh <file>.gd realtime` (`:13-14`). No
    suite in the brief is pinned to realtime.
  - Existing suites run at 60 (`scripts/run-baseline.sh:3,14`), e.g. `./scripts/run-test.sh
    test_lappland.gd 60`; test_bosses, test_elevation, test_layout, test_run_save, test_v1 take
    `1200` (`:10,13`). Baseline: `./scripts/run-baseline.sh <label> [jobs]` (`:2-20`).
  - New suites, not written yet, each `./scripts/run-test.sh <suite>.gd 60` (`CHANGE-BRIEF.md:249-256`):
    test_npc_idle_readback, test_wave_rig_readback, test_wave_state_machine, test_wave_edges, test_a7_pins.

## Current change

@CHANGE-BRIEF.md

## Ownership

- Shaders: existing files in `shaders/` stay unchanged (the A5/A6 rule; A6 added only
  `shaders/particles_generated.gdshader`). A7 adds and edits nothing there.
- Agents do not edit `scripts/run-test.sh`. A6 effect settings stay in `effects/` scene files.
- Clips live as resources in `animations/` or in the scene that owns them, and are never
  built in code at runtime. Scripts only instance, `play`/`seek`/`advance`/`stop`, set unkeyed props.

## One authority

Exactly one node writes each animated property. Never add a second writer to a node that has one.
- `NpcIdle.frame`: its own `AnimationPlayer`, nothing else. Callers set `texture` and placement
  only; `continuous_world_map.gd:2716` (`figure.frame = ...`) must go, replaced by one
  `seek(offset, true)` (`CHANGE-BRIEF.md:65-68`). Unkeyed writers that stay: `GmCamera` writes
  `scale.y` on `upright_figures` (`game/gm_camera.gd:84-85`) and `offset.y` on `upright_sprites`,
  which includes base `Closure` (`:77-83`; `world/base_map.gd:769`). Never key `scale`/`offset`.
- `Body`, `ArmBack`, `ArmFront`, `BladeBack`, `BladeFront`: the rig's `AnimationPlayer` alone.
  Its only caller (`play`, `stop`, `advance`) is `Player`'s wave state machine, which is also
  the only writer of `Billboard.visible` and `Rig.scale.x`; those are never keyed.
- Operator sprite frames/animation/`flip_h`: `LapplandAnimator3D` itself; `player.gd` and kits
  only call its methods (`entities/operator_kit.gd:245-250`). Its `visible`: `Player` only
  (`entities/player.gd:1867,1963`); the wave state hides/shows it; no `show_rig()` (brief r1).
- `wave_frame`/`wave_state`: `Player._physics_process` only; gameplay never reads the clip.

## Godot 4 names

- Use: `AnimationPlayer`, `Animation`, `AnimationLibrary`, `Animation.loop_mode` with
  `LOOP_NONE`/`LOOP_LINEAR`, `Animation.step`, `Animation.length`,
  `value_track_set_update_mode(..., Animation.UPDATE_DISCRETE)`,
  `track_set_interpolation_type(..., Animation.INTERPOLATION_NEAREST)`,
  `AnimationPlayer.speed_scale`, `autoplay`, `root_node`, `callback_mode_process` with
  `AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_IDLE`/`_MANUAL`, `advance()`, `seek()`,
  `current_animation_position`; `Sprite3D.hframes`/`vframes`/`frame`; `AnimatedSprite3D`;
  `SubViewport.transparent_bg`, `render_target_update_mode` (`SubViewport.UPDATE_ALWAYS` is used
  in this repo, `game/pixel_display.gd:26,67`); `ViewportTexture`; `Node2D.rotation` (radians).
- Never: `loop = true` on an Animation, `playback_speed`, `playback_process_mode`,
  `AnimatedSprite`, `Spatial`. Every name above, present or absent, is confirmed in 4.7.2 by
  `tests/a7_probe_headless.gd` (`logs/a7_probe_headless_60fps.log`). Unsure of another? Say so.

## Out of scope

- Hit and wave gameplay values: damage, crit, multipliers (still computed on the click,
  `CHANGE-BRIEF.md:166-167`), cooldowns, hitstop, dodge, control, combo and charge rules, other
  than the release changes the brief lists (`:231-239`).
- Collision, movement, input, enemies, every non-release swing and every other operator's
  sprites and kits; NPC placement, scale, billboard mode, look and names (`Closure` is
  excluded by name in `tests/test_base_scene.gd:109`).
- The delivered sheets (`godot_assets/lappland_combat_64.png`, `art/characters/npc/*`),
  `shaders/`, `effects/`, `project.godot`, `scripts/run-test.sh`, base crew walkers
  (`tests/test_base_crew.gd:57`), and no `AnimationTree`, no method tracks.

## Headless facts

Confirmed on this machine by `tests/a7_probe_headless.gd` (`logs/a7_probe_headless_60fps.log`):
- A headless run advances clips and reads their structure. It draws
  nothing, so whether the motion reads is not observable here.
- Key times are 32-bit floats; compare them with a tolerance.
- value_track_get_update_mode applies only to value tracks.
- Frame strips come from a windowed Movie Maker run, which I start.

## Unconfirmed

- AGENTS.md does not exist. `README.md:51` says "three folders up"; the wrapper uses five (`:11`).
- Rig source sheet path and model/terms: "pending" (`CHANGE-BRIEF.md:116-127`). Lines drift.
