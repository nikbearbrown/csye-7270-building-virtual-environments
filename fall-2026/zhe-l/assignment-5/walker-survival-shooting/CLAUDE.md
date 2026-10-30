# CLAUDE.md — Assignment 5 (screen-glow shader, then the crate shader)

## Project context

- **Engine version:** Godot 4.7 (`godot/project.godot` line 15, `config/features` lists "4.7"); the baseline log was produced by `Godot Engine v4.7.2.stable.official` (`logs/a3_asset_check_60fps.log` line 1).
- **Renderer:** Forward+ (`godot/project.godot` line 15 lists "Forward Plus"; no `rendering_method` override in the `[rendering]` section, lines 72–74). Windows driver: D3D12 (`godot/project.godot` line 74). Physics: Jolt (`godot/project.godot` line 70).
- **Main scene:** `godot/base.tscn` (`godot/project.godot` line 14 names `uid://b78l24afmav2c`, which is the uid on `godot/base.tscn` line 1). The player is instanced in it at `godot/base.tscn` line 184.
- **Environment:** `WorldEnvironment` in `godot/base.tscn` lines 11–16 and 23–24 sets a background colour and ambient light only; no tonemap, exposure or glow keys are written there.

### How the shaded object (the tablet screen) is drawn
- Chain: `godot/base.tscn` line 184 instances `godot/characters/human/player/player.tscn`, which inherits `godot/characters/human/humanoid/humanoid.tscn` (`player.tscn` line 9); the humanoid instances `godot/items/tablet/tablet_device.tscn` as `Visual/TabletDevice` (`humanoid.tscn` lines 53–54).
- The screen is the `Screen` node, a `MeshInstance3D` (`godot/items/tablet/tablet_device.tscn` lines 28–31), with a `QuadMesh` of size 0.18 × 0.108 (`tablet_device.tscn` lines 7–8) placed at z = 0.012 in front of the tablet model (`tablet_device.tscn` line 29).
- Its material is `surface_material_override/0` = a `ShaderMaterial` sub-resource (`tablet_device.tscn` line 31 → lines 10–15) with `resource_local_to_scene = true` (line 11), using `res://shaders/pad_base_light.gdshader` (lines 5 and 13). Stored parameters: `cold_white = Color(0.902, 0.969, 0.969, 1)` and `pad_light_data = 0.0` (lines 14–15).
- The shader is `spatial`, `unshaded`, with uniforms `cold_white` (`vec4`, `source_color`) and `pad_light_data` (`float`, `hint_range(0.0, 1.0)`), and writes `ALBEDO = mix(vec3(0.0), cold_white.rgb, pad_light_data)` (`godot/shaders/pad_base_light.gdshader` lines 1–7).
- Outside code reaches the node through `TabletDevice.get_screen()` (`godot/items/tablet/tablet_device.gd` lines 23–24).
- The tablet's position is animated by `Humanoid._update_tablet_visual()` (`godot/characters/human/humanoid/humanoid.gd` lines 115–130), which moves it between the hip, one-hand and two-hand `Marker3D` slots (`humanoid.tscn` lines 44–51) over `tablet_move_seconds` = 0.35 (`humanoid.gd` line 36).
- A debug `UpMarker` box (black `StandardMaterial3D`) sits above the tablet (`tablet_device.tscn` lines 17–21 and 33–36); the brief requires it hidden or deleted before captures (`CHANGE-BRIEF.md` line 100).

### Which script owns the game state that drives the effect
- `godot/characters/human/humanoid/humanoid.gd` (class `Humanoid`, line 4) owns `_tablet_hold` (line 43), of type `enum TabletHold { NONE, ONE_HAND, TWO_HAND }` (lines 13–17).
- It is changed only in `_apply_tablet_press()` (lines 158–163), using the table in `_next_tablet_hold()` (lines 167–175). Read with `get_tablet_hold()` (lines 152–153). Announced by `signal tablet_hold_changed(old_hold, new_hold)` (line 25, emitted at line 163).
- "Arrived at the hand slot" = `_tablet_move_progress` (line 47) reaching `TABLET_MOVE_DONE` (line 19); `_tablet_shown_hold` (line 45) is the slot being moved to. Both are presentation variables (comment on line 44).
- The key press comes from the player brain: `PlayerController._read_tablet_press()` with `tablet_long_press_seconds` = 0.4 (`godot/characters/human/player/player_controller.gd` lines 24 and 127–136), passed in `CharacterIntent.tablet_press` (`godot/characters/character_intent.gd` line 27). The `tablet` input action is bound to Tab (`godot/project.godot` lines 62–66).
- No driver script for `pad_light_data` exists yet (no `.gd` file under `godot/` mentions `pad_light_data`).

### The 3D object for the textured shader and where its material comes from
- Objects: `crate_long` and `crate_cube` in `godot/base.tscn` (lines 141–142 and 144–145), named in `CHANGE-BRIEF.md` line 115.
- They are instances of `godot/assets/furniture/crate_long.glb` and `godot/assets/furniture/crate_cube.glb` (`godot/base.tscn` lines 4–5).
- Their current materials are the ones embedded in the `.glb` files: both import files have `materials/extract=0` and `_subresources={}` (`godot/assets/furniture/crate_long.glb.import` lines 39 and 42; `crate_cube.glb.import` lines 39 and 42). No external material file exists yet; the brief says the new materials go behind the importer's Use External setting (`CHANGE-BRIEF.md` line 115).

### Test commands (always through `scripts/run-test.sh`)
- Run from this folder (the one holding `godot/` and `scripts/`). The wrapper picks `godot/` as the project when `godot/project.godot` exists (`scripts/run-test.sh` lines 21–25) and uses `$GODOT`, else `godot_console`, else `godot` (lines 28–34).
- It runs `timeout 120 <godot> --headless --path godot --script res://tests/<file> --fixed-fps <fps>`, writes `logs/<test>_<fps>fps.log`, and fails on `SHADER ERROR` or `SCRIPT ERROR` (`scripts/run-test.sh` lines 40–45). Exit 124 = hung.
- Existing test (the only file in `godot/tests/`):

```bash
./scripts/run-test.sh a3_asset_check.gd 60
```

  Expected: 55 `PASS` lines and `== ALL PASS: 0 failure(s) ==` (`logs/a3_asset_check_60fps.log`), exit 0 (`godot/tests/a3_asset_check.gd` line 133). This result must not change (`CHANGE-BRIEF.md` line 61).
- The screen-glow test the brief asks for must be run at 30, 60 and 144 fps (`CHANGE-BRIEF.md` lines 63–71), i.e. `./scripts/run-test.sh <screen test>.gd 30`, then `60`, then `144`. Its file name is not decided yet (see Unconfirmed).

## Current change

@CHANGE-BRIEF.md

## Ownership

- Every file in `godot/shaders/` (currently `pad_base_light.gdshader` and its `.uid`) is hand-written by the human. An agent never creates, edits, reformats or deletes anything in `godot/shaders/`, even to fix an error; it reports the problem instead.
- Material set-up done by the human in the editor (the `Screen` `ShaderMaterial` with Local To Scene) is not reworked by an agent.

## Out of scope

- No changes to movement, collision, input actions or `project.godot`.
- No changes to the tablet state machine: `_tablet_hold`, `_apply_tablet_press()`, `_next_tablet_hold()`, the 0.4 s long press or the 0.35 s tablet move. The driver may read `TabletHold` and the move progress; it never writes them.
- No change to the existing test `godot/tests/a3_asset_check.gd` or its 55-PASS result.
- No object other than the tablet `Screen` gets the screen-glow effect: not the tablet model, not the `UpMarker`, not the display tablet prop `tablet` in `godot/base.tscn` line 147.
- The shared material is never edited at runtime in a way that affects other tablets; each driver touches only its own tablet's screen.
- The `.glb` source models and the Blender files are not changed.
- Parts 2 (hint experiment) and 3 (crate wear shader) are not started until their dated revisions are added to `CHANGE-BRIEF.md` (lines 104–120).
- Sound, UI and other presentation code never decide game state.

## Unconfirmed

- There is no `README.md` and no `AGENTS.md` in this folder, so nothing from them is included.
- Where the driver lives (a new script, or a function on `TabletDevice` / `Humanoid`) and the name of the screen-glow test file are not stated in the files.
- Which `godot_console` / `godot` binary is on `PATH` on the machine that runs the tests is not recorded; set `GODOT` if neither is found.
- The brief says the `Screen` quad is 1 mm in front of the model's screen; the scene only shows z = 0.012 relative to `TabletDevice` (`tablet_device.tscn` line 29), so the 1 mm gap was not checked against the model.
- The default tonemap / exposure values the pixel predictions rely on come from a headless check recorded in `CHANGE-BRIEF.md` (line 85), not from a file I could read.
- The doc comment in `godot/items/tablet/tablet_device.gd` lines 21–22 still says every tablet shares one material; the scene now has Local To Scene ticked (`tablet_device.tscn` line 11). Whether that comment should be updated is the human's call.
- `godot/base.tscn` has only one character; the two-body independence test needs a second humanoid that does not exist in any scene yet.
- The crate wear look, textures, uniforms and the external material file names are listed in the brief as "to be added" (`CHANGE-BRIEF.md` lines 112–120).
