# CLAUDE.md — Assignment 6 (landing dust + dust under the ceiling light)

## Project context

### Engine and project
- **Godot version:** 4.7.2-stable: every baseline log starts with `Godot Engine v4.7.2.stable.official.ed1daf0bf` (`logs/a3_asset_check_60fps.log` line 1); the project declares `"4.7"` (`godot/project.godot` line 15).
- **Renderer:** Forward+ (`godot/project.godot` line 15, `"Forward Plus"`; the `[rendering]` section, lines 90–92, sets no `rendering_method`). Windows driver D3D12 (line 92). Physics: Jolt (line 88). No `physics_ticks_per_second`, so physics runs at the default 60 ticks/s.
- **Main scene:** `godot/base.tscn` (`project.godot` line 14 = `uid://b78l24afmav2c` = `base.tscn` line 1). Window 2048 × 1152 (`project.godot` lines 24–25).
- `godot/effects/` does not exist yet; the brief creates `landing_dust.tscn` and `light_dust.tscn` there (`CHANGE-BRIEF.md` lines 50 and 148).

### Effect A — landing dust
- **Node types:** root `Node3D` with two `GPUParticles3D` children, `Dust` and `GroundRing` (`CHANGE-BRIEF.md` lines 46–52); scene file `godot/effects/landing_dust.tscn` (line 50).
- **Event owner:** `godot/characters/human/humanoid/humanoid.gd` (class `Humanoid`, line 4, extends `CharacterBody3D`, line 5). The signal `landed` does **not** exist yet; the brief allows adding it, notify-only, emitted once when `is_on_floor()` goes false → true (`CHANGE-BRIEF.md` lines 25 and 205). The only signal today is `tablet_hold_changed` (line 26).
- Where landing becomes known: `apply_intent()` (lines 69–95) reads `is_on_floor()` at line 75 before moving, then calls `move_and_slide()` at line 94. `jump_velocity` = 4.5 (line 36); gravity from project settings (line 42).
- `Humanoid` is shared by the player and future human enemies (line 6), so every humanoid would emit `landed`.
- **Scene it appears in:** `godot/base.tscn`, in the world, not under the player (`CHANGE-BRIEF.md` line 54). The player is `Player` at `base.tscn` lines 189–190 (spawn y = 0.25), an instance of `godot/characters/human/player/player.tscn`, which inherits `humanoid.tscn` (`player.tscn` lines 3 and 11). Capsule radius 0.3, height 1.6 (`humanoid.tscn` lines 6–8).
- Floor: `room/floor`, a `CSGBox3D` 16 × 0.5 × 10 at y = 0 (`base.tscn` lines 31–32), so its top is y = 0.25.
- Retrigger must call `restart()`, not only `emitting = true` (`CHANGE-BRIEF.md` line 91).

### Effect B — dust under the ceiling light
- **Node type:** one `GPUParticles3D` (`CHANGE-BRIEF.md` line 149); scene file `godot/effects/light_dust.tscn` (line 148).
- **Condition owner:** `godot/world/lights/ceiling_lights.gd` (class `CeilingLights`, line 4, extends `Node`): `signal lights_changed(lights_on: bool)` (line 19), emitted only from `set_lights_on()` when the state really changes (lines 45–50); `is_lights_on()` (lines 57–58); `start_on = true` (line 24). `_ready()` sets the start state and does **not** emit (lines 36–38), so the effect must query `is_lights_on()` once at start.
- The switch: `godot/world/light_switch/light_switch.gd` `interact()` → `ceiling_lights.toggle()` (lines 40–41); action `interact` = physical key F (`project.godot` lines 80–84). Lights are found through group `ceiling_lights` (`ceiling_lights.gd` line 13).
- **Scene it appears in:** `godot/base.tscn`, under `ceiling_light_1` (`OmniLight3D` at (0.02, 2.60, -3.66), shadows on, range 8; `base.tscn` lines 161–166). `CeilingLights` node: lines 158–159; `LightSwitch` wired to it: lines 192–194. Lights 2 and 3: lines 168–173 and 182–187.
- Environment: background (0.03, 0.035, 0.045), ambient (0.45, 0.5, 0.6) energy 0.35 (`base.tscn` lines 12–18).

### Tests (always through `scripts/run-test.sh`, run from this folder)
- Usage: `./scripts/run-test.sh <file.gd> <fps|realtime> [timeout-seconds]` (`scripts/run-test.sh` line 5). Project = `godot/` when `godot/project.godot` exists (lines 25–29). Binary = `$GODOT`, else `godot_console`, else `godot` (lines 32–38).
- A number pins `--fixed-fps <fps>`; `realtime` adds no `--fixed-fps` and names the log `<test>_realtime.log` (lines 43–49). Timeout defaults to 120 s (line 56). Always `--headless` (line 56). Log: `logs/<test>_<mode>.log` (line 55). Fails on `SHADER ERROR` / `SCRIPT ERROR` (line 58); exit 124 = hung.
- Baseline (`CHANGE-BRIEF.md` lines 209–211; logs in `logs/`):

```bash
./scripts/run-test.sh a3_asset_check.gd 60       # 55 PASS, exit 0
./scripts/run-test.sh screen_glow_check.gd 30    # 24 PASS (also 60 and 144)
./scripts/run-test.sh normal_map_check.gd 60     # 2 PASS
./scripts/run-test.sh test_materials.gd 60       # 168 PASS, 1 FAIL, exit 1
./scripts/run-test.sh <test>.gd realtime         # realtime mode (no pinned fps)
./scripts/run-test.sh <test>.gd 60 300           # longer timeout, e.g. a cost run
```

- The one known failure: `FAIL base.tscn: 3 Light3D nodes (got 4)` (`logs/test_materials_60fps.log`), from `test_materials.gd` lines 369–370 counting every `Light3D`; the extra one is `ScreenTabletLight` (`player.tscn` line 56). Report "168 passed, 1 failed", never "all pass".
- `screen_glow_check.gd` and `test_materials.gd` load `res://base.tscn` (lines 16 and 30); `a3_asset_check.gd` too (line 101). Whatever is added to `base.tscn` must keep these results.

## Current change

@CHANGE-BRIEF.md

## Ownership

- Every file in `godot/shaders/` is hand-written by the human. An agent never creates, edits, reformats or deletes anything there, even to fix an error; it reports the problem instead.
- Material set-up done by the human in the editor (the tablet `Screen` `ShaderMaterial` with Local To Scene) is not reworked by an agent.
- Effect settings (amounts, lifetimes, shapes, curves, ramps, materials, `visibility_aabb`, `preprocess`, `local_coords`) live in scene files in `godot/effects/`, not in code. Scripts only listen to events and call `restart()` / set `emitting` / `visible`.

## Godot 4 names

- Use Godot 4 names for 4.7.2: `GPUParticles3D` (not `Particles`), `ParticleProcessMaterial` (not `ParticlesMaterial`), `StandardMaterial3D` (not `SpatialMaterial`), `GradientTexture2D`, `QuadMesh`, `Node3D` (not `Spatial`).
- Material switches are properties, not Godot 3 `flags_*` / `params_*`: `shading_mode`, `transparency`, `blend_mode`, `vertex_color_use_as_albedo`, `billboard_mode`, `albedo_texture`. Shadows: `cast_shadow` on the node.
- Velocity is the `initial_velocity_min` / `initial_velocity_max` pair. The brief records that 4.7.2's ClassDB still also lists `initial_velocity` (`CHANGE-BRIEF.md` line 276), so a write to it may not fail; read values back to prove a setting took effect.
- I could not check the other property names against 4.7.2 here (no engine run was allowed outside this repo). The names in the brief's tables are the Godot 4.x names as I know them; before relying on one, confirm it with `ClassDB.class_get_property_list()` or by reading it back in a headless test, and say so if it is missing instead of guessing a replacement.

## Out of scope

- No change to collision, movement, velocity, jumping, input actions or `project.godot`.
- In `humanoid.gd`, only the notify-only `landed` signal may be added; nothing else there (tablet state machine, timings, facing) changes.
- `CeilingLights`, the light switch and the three ceiling lights stay as they are; the dust only listens and queries.
- Effect code reads game state and never writes it; it never decides whether the lights are on or whether the player is on the floor.
- No change to the existing tests or their expected values (55 / 24 × 3 / 2 / 168 + 1 known failure).
- Nothing in `godot/shaders/`, no `.glb` or Blender source, and no other object or scene is changed for this effect.
- No extra effects beyond A (two emitters) and B (one emitter under light 1).

## Unconfirmed

- No `AGENTS.md` and no `README.md` exist in this folder.
- Which script listens to `landed` / `lights_changed` and drives the emitters (a script on each effect root, or elsewhere), and how Effect A finds the player, are not stated in the files.
- Where `landing_dust.tscn` is instanced (the brief says "in the world"; I assume `base.tscn`, not confirmed). Whether `light_dust.tscn` is placed by its own transform at (0, 1.45, -3.20) or under another node is not stated.
- Whether `landed` should fire for every `Humanoid` or only the player; the brief says "the player lands".
- If the dust node's `_ready()` runs before `CeilingLights._ready()`, `is_lights_on()` returns the field default `true`, not `start_on` (`ceiling_lights.gd` lines 24, 29, 37). Order in `base.tscn` decides this.
- The rendered frame strips use `--quit-after` and real drawing; `run-test.sh` always passes `--headless` (line 56), so those captures cannot run through it. How they are run is not recorded.
- The preview scenes for the frame strips (light off at start, retrigger switch) do not exist yet; their paths are not named.
- New test file names (configuration, event, logic) are not named in the brief.
- Brief "Unconfirmed" items (lines 274–277): whether `restart()` re-runs `preprocess`; whether a hidden `GPUParticles3D` keeps simulating in 4.7.2; why `initial_velocity` still exists; whether 0.006–0.012 m specks are visible.
- The `interact` action's key event has `"device": 16` (`project.godot` line 82), not `-1` like the others; I did not check whether this affects F in the running game.
- Which `godot_console` / `godot` is on `PATH` on the test machine is not recorded; set `GODOT` if neither is found.
