# CLAUDE.md — Assignment 7 (animation: pixel head in the taskbar + one-handed tablet raise)

## Project context

### Engine and project
- **Godot version:** 4.7.2-stable: every baseline log starts with `Godot Engine v4.7.2.stable.official.ed1daf0bf` (`logs/a3_asset_check_60fps.log` line 1); the project declares `"4.7"` (`godot/project.godot` line 15); the brief pins 4.7.2-stable (`CHANGE-BRIEF.md` line 12).
- **Renderer:** Forward+ (`godot/project.godot` line 15, `"Forward Plus"`; the `[rendering]` section, lines 98–100, sets only the Windows driver `d3d12`). Physics engine: Jolt (line 96).
- **Physics tick:** 60 ticks/s, the default: `project.godot` has no `physics_ticks_per_second`; the screen-glow baseline prints `physics 60 ticks/s` (`logs/screen_glow_check_60fps.log` line 11).
- **Main scene:** `godot/base.tscn` (`project.godot` line 14 = `uid://b78l24afmav2c` = `base.tscn` line 1). The player is `Player` at (2, 0.25, 1.5) (`base.tscn` lines 194–195), an instance of `characters/human/player/player.tscn`, which inherits `characters/human/humanoid/humanoid.tscn` (`player.tscn` lines 3 and 12). Autoload: `FileService` (`project.godot` line 24).

### Tablet hold state (the game state the rig clip follows)
- Owner: `Humanoid` (`godot/characters/human/humanoid/humanoid.gd` line 4, extends `CharacterBody3D`, line 5). State = `_tablet_hold` (line 47), enum `TabletHold { NONE, ONE_HAND, TWO_HAND }` (lines 13–17); public read `get_tablet_hold()` (lines 205–206).
- How it changes: the brain `PlayerController._physics_process()` calls `_body.apply_intent()` every physics frame (`player_controller.gd` lines 90–93). `_read_tablet_press()` turns Tab into SHORT / LONG (long = 0.4 s, lines 24 and 140–150). `apply_intent()` calls `_apply_tablet_press()` first (`humanoid.gd` line 78), which sets `_tablet_hold = _next_tablet_hold(...)` and emits `tablet_hold_changed(old, new)` (lines 217–222, signal line 26). Table: NONE + short → ONE_HAND, + long → TWO_HAND; ONE_HAND + short → NONE, + long → TWO_HAND; TWO_HAND + short → ONE_HAND, + long → NONE (lines 226–234).
- Per-hold input filter, in the brain: ONE_HAND = walk only; TWO_HAND = no walk, sprint, jump or aim; F (`interact`) only with NONE (`player_controller.gd` lines 122–135).

### Where the tablet and its screen are driven today (removed or changed by the brief, `CHANGE-BRIEF.md` lines 105–107, 172–177)
- Held tablet: `TabletDevice` instance at `Visual/TabletDevice` (`humanoid.tscn` lines 53–54; `humanoid.gd` line 65). `_update_tablet_visual()` (`humanoid.gd` lines 139–155) slides it between `TabletHipSlot` / `TabletOneHandSlot` / `TabletTwoHandSlot` (`humanoid.tscn` lines 44–51; lookup `_get_tablet_slot()`, `humanoid.gd` lines 170–177) over `tablet_move_seconds` = 0.35 (line 40), on the physics tick (called from `_update_visual()`, lines 131–133, at the end of `apply_intent()`, line 104).
- Held screen: `_update_tablet_screen()` (`humanoid.gd` lines 160–165) lights it when the slide is done, darkens it on NONE, and calls `TabletDevice.set_screen_lit()` (`items/tablet/tablet_device.gd` lines 47–53), which writes `pad_light_data` (line 13) on the `Screen` `ShaderMaterial` (Local To Scene; `items/tablet/tablet_device.tscn` lines 10–15, 28–31).
- Character look today: `Visual/human_model` = capsule `Body` + `FacingMarker` (`humanoid.tscn` lines 34–42); collision capsule r 0.3, h 1.6 (lines 6–8, 28–30). `set_visual_visible()` hides `human_model` in first person (`humanoid.gd` lines 200–201; called from `player_controller.gd` line 229).
- Demo tablet (bottom right): `ScreenTablet` (`characters/human/player/screen_tablet.gd`) slides its own `TabletDevice` between `HiddenSlot` and `ShownSlot` over `moving_time` = 0.35 (line 20) in `_process()` (lines 47–58, process tick) and lights it in `_update_screen()` when shown and arrived (lines 86–89). `PlayerController._on_tablet_hold_changed()` calls `set_shown(new_hold == ONE_HAND)` (`player_controller.gd` line 197). Nodes: `player.tscn` lines 60–70.
- Tablet OS canvas: `TabletOSViewport` 1280 × 768, starts with update mode 0 (`player.tscn` lines 72–76); drawn every frame while held, disabled when put away (`player_controller.gd` lines 198–201); its texture goes to both screens (lines 68–70).

### Tablet OS taskbar (where the pixel head goes)
- `godot/computer_system/tablet_os/tablet_os.tscn`: `Taskbar` `ColorRect`, 64 px high (`offset_top = -64`), lines 54–63 → `Row` `HBoxContainer` (lines 65–71) → `TaskbarButtons` `HBoxContainer` (expand-fill, lines 73–75) and `ShowDesktopButton` (lines 77–79). The brief puts the head at the far left, left of the window buttons (`CHANGE-BRIEF.md` line 43); cell 56 × 56 px at native size (line 42).
- `tablet_os.gd` reaches these by path: `$Taskbar`, `$Taskbar/Row/TaskbarButtons`, `$Taskbar/Row/ShowDesktopButton` (lines 31–33). Existing system UI folder: `computer_system/tablet_os/system/desktop/` only.

### Folders the brief names for new files (none in the committed tree, `git ls-files` at a399a863)
- Head scene, its script, `avatar-idle-front-blink-8x1-56.png` and `ATTRIBUTION.md`: `godot/computer_system/tablet_os/system/pixel_head/` (`CHANGE-BRIEF.md` lines 21, 47, 58). The sheet exists today only in `design/avatar-sprite/`.
- Character `.glb` exported from `xz_anim.blend` + `ATTRIBUTION.md`: `godot/assets/characters/main_character/` (`CHANGE-BRIEF.md` line 118); loop modes in its `.glb.import` (line 119). `godot/assets/` today has `furniture/`, `props/`, `shader/` only. No `godot/animations/` folder exists.

### Tests (always through `scripts/run-test.sh`, run from this folder)
- Usage: `./scripts/run-test.sh <file.gd> <fps|realtime> [timeout-seconds]` (`scripts/run-test.sh` line 5). Project = `godot/` when `godot/project.godot` exists (lines 26–30). Binary = `$GODOT`, else `godot_console`, else `godot` (lines 33–39). A number adds `--fixed-fps`; `realtime` does not (lines 44–50). Always `--headless`, timeout 120 s by default, exit 124 = hung (lines 9, 57). Log: `logs/<test>_<mode>.log` (line 56). Fails on `SHADER ERROR`, `SCRIPT ERROR` or `Failed loading resource` (line 59).
- Baseline, all at 60 fps (counts = `PASS` lines in each log; the summary is the log's last line):

```bash
./scripts/run-test.sh a3_asset_check.gd 60            # 55 PASS, 0 failures (logs/a3_asset_check_60fps.log line 73)
./scripts/run-test.sh screen_glow_check.gd 60         # 24 PASS, 0 failures (logs/screen_glow_check_60fps.log line 31)
./scripts/run-test.sh test_landing_dust_config.gd 60  # 157 passed, 0 failed (logs/test_landing_dust_config_60fps.log line 161)
./scripts/run-test.sh test_landing_dust_events.gd 60  # 27 passed, 0 failed (logs/test_landing_dust_events_60fps.log line 30)
./scripts/run-test.sh test_light_dust_config.gd 60    # 110 passed, 0 failed (logs/test_light_dust_config_60fps.log line 113)
./scripts/run-test.sh test_light_dust_state.gd 60     # 41 passed, 0 failed (logs/test_light_dust_state_60fps.log line 44)
```

- `screen_glow_check.gd` pins the 0.35 s slide (`MOVE_SECONDS`, line 22; cases 5, 6, 8, 9, 11 at lines 233–300) and the path `Visual/TabletDevice` (lines 18, 239); the brief lets the slide-dependent cases change (`CHANGE-BRIEF.md` line 176). `a3_asset_check.gd`, `screen_glow_check.gd` and the two dust event/state tests load `res://base.tscn`.
- Headless runs use a dummy renderer: node and resource state can be read back, nothing is drawn. Frame strips are windowed Movie Maker runs at 30 fps that the human starts (`CHANGE-BRIEF.md` line 199).

### Headless facts (confirmed on this machine, Godot 4.7.2 `--headless`, 2026-11-22)
- A headless run advances clips and reads their structure. It draws nothing, so whether the motion reads is not observable here. (`DisplayServer.get_name()` = `headless`; `test_pixel_head_clip.gd` reads `Sprite2D.frame` stepping 0..7 and back to 0 while the clip plays.)
- Key times are 32-bit floats; compare them with a tolerance. (The imported raise stores `step` = 0.033333335, not 1/30.)
- `value_track_get_update_mode` applies only to value tracks. (On the raise's position track it prints `Condition "t->type != TYPE_VALUE" is true. Returning: UPDATE_CONTINUOUS`.)
- Frame strips come from a windowed Movie Maker run, which I start.
- Injected input goes through `Input.parse_input_event`, flushed with `Input.flush_buffered_events()` so the brain reads it on the same physics frame (`test_tablet_pins.gd`, `test_tablet_raise_edges.gd`).
- Measured: the game reads "raise finished" on physics frame N + 42 after a press read on N (clip frame 20 is N + 40): one frame from the state machine's first frame in `raise_1h` not advancing, one from the process-tick clip read on the physics tick (`CHANGE-BRIEF.md`, revision of 2026-11-22).

## Current change

@CHANGE-BRIEF.md

## Ownership

- Every file in `godot/shaders/` is hand-written by the human. An agent never creates, edits, reformats or deletes anything there, even to fix an error; it reports the problem instead.
- Material set-up done by the human in the editor (the tablet `Screen` `ShaderMaterial` with Local To Scene) is not reworked by an agent.
- Clips are resources: they live in `godot/animations/` or in the scene that owns them (the rig clips in the imported `.glb`, owned by the character scene; the head clip in the head scene's `AnimationPlayer`, `CHANGE-BRIEF.md` line 13). No `Animation` is built, keyed or edited in code at runtime. Loop modes of imported clips live in the `.glb.import` settings, never only in the imported scene (line 119).
- Exactly one authority writes to each animated node (`CHANGE-BRIEF.md` lines 24, 105–107, 125, 150, 177):
  - xz `Skeleton3D` (bone poses), and through the `tablet` bone the `BoneAttachment3D` and the held `TabletDevice`'s transform → the character's `AnimationTree` (root `AnimationNodeStateMachine`). No script writes the tablet's transform; the imported `.glb`'s own `AnimationPlayer` must not play the skeleton on its own.
  - Head `Sprite2D`'s `frame` → the head scene's `AnimationPlayer` (autoplay, looping). Nothing else in the tablet OS writes `frame`.
  - Held tablet's `pad_light_data` → `Humanoid` via `TabletDevice.set_screen_lit()`; the `AnimationTree` has no track on it.
  - Demo tablet's transform and screen → `ScreenTablet` (`_process()` / `_update_screen()`).
- Animation nodes only read game state (`get_tablet_hold()`); they never write it (`CHANGE-BRIEF.md` lines 149, 180).

## Godot 4 names

- Pinned version: Godot 4.7.2-stable. Use Godot 4 class and property names only: `AnimationPlayer`, `AnimationTree`, `AnimationNodeStateMachine`, `AnimationMixer` (base of both), `Animation.loop_mode` with `Animation.LOOP_NONE` / `Animation.LOOP_LINEAR`, `Animation.step`, `Animation.UPDATE_DISCRETE` (via `value_track_set_update_mode()`), `callback_mode_process` with `AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_IDLE`, `AnimationTree.advance_expression_base_node`, `BoneAttachment3D` (`bone_name`), `Skeleton3D`, `Sprite2D` `hframes` / `vframes` / `frame`.
- Not Godot 3 or 4.0–4.1 names: no `AnimationTreePlayer`, `Spatial`, `Sprite`, `Skeleton`, `BoneAttachment`, `Animation.loop` (bool), `playback_process_mode`, `process_callback` / `process_mode` on animation nodes.
- Transition names used by the brief (`CHANGE-BRIEF.md` lines 139, 148): `AnimationNodeStateMachineTransition` with `xfade_time`, `switch_mode` (`SWITCH_MODE_IMMEDIATE`, `SWITCH_MODE_AT_END`), `advance_mode` (`ADVANCE_MODE_AUTO`), `advance_expression`.
- I could not check any of these against 4.7.2 here (no engine run was allowed in this step; no existing script uses them except `AnimationPlayer` in `a3_asset_check.gd` line 89). They are the Godot 4.2+ names as I know them. Before relying on one, confirm it with `ClassDB.class_exists()` / `class_get_property_list()` / `class_get_integer_constant_list()` in a headless test (as `test_landing_dust_config.gd` does, `logs/test_landing_dust_config_60fps.log` line 3), and if it is missing say so instead of guessing a replacement. I am least sure of the exact enum spelling `ANIMATION_CALLBACK_MODE_PROCESS_IDLE` and of the key names the importer writes into `.glb.import` for per-animation loop mode.

## Out of scope

- Movement speeds, collision (the capsule stays as it is), jumping, interaction, input bindings and `project.godot`.
- The hold-state table and how Tab presses become states in `humanoid.gd` / `player_controller.gd`; the animation follows that logic, it does not replace it.
- Both hand-written shaders in `godot/shaders/`, the Assignment 6 effects (`godot/effects/`, both dusts and their scripts), the light switch and ceiling lights, every other object in `base.tscn`, the existing `.glb` assets and their import settings.
- The rest of the tablet OS (desktop, windows, This PC, the backend): only the head is added to the taskbar.
- The demo tablet's 0.35 s slide stays; only when its screen lights changes.
- No clips or poses beyond the two clips and the hold poses in the brief; the planned extra animations (`CHANGE-BRIEF.md` lines 248–260) are not part of this change. No method tracks.
- Existing tests keep their expected values, except the slide-dependent screen-glow cases the brief names (`CHANGE-BRIEF.md` line 176), which are listed one by one before any pin changes.

## Unconfirmed

- No `AGENTS.md` and no `README.md` exist in this folder.
- Review (2026-11-22, Godot 4.7.2 ClassDB): every class, constant and property named under "Godot 4 names" exists, including `AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_IDLE`, the transition's `xfade_time` / `switch_mode` / `advance_mode` / `advance_expression`, `AnimationTree.advance_expression_base_node`, and the playback methods `get_current_node()`, `get_fading_from_node()`, `travel()`, `start()`.
- Review: no `godot/animations/` folder. The rig clips stay in `godot/assets/characters/main_character/main_character.glb` (exported by `tools/blender/export_main_character.py`; clips `tablet_hold_hip`, `tablet_raise_one_hand`, `tablet_hold_one_hand`); the state machine is a sub-resource of the `AnimationTree` node in `humanoid.tscn`; the head clip is in the head scene. Per-animation loop mode goes under `_subresources` → `animations` → `<name>` → `settings/loop_mode` in `main_character.glb.import`; the empty-cache read-back confirms it.
- Review, decided (implementation, within the brief): `Humanoid` reads the state machine through `AnimationTree["parameters/playback"]`: `get_current_node()` names the state and an empty `get_fading_from_node()` means the 0.2 s blend has ended. The brain gives `ScreenTablet` the held screen's lit state every physics frame, and the demo screen lights only when shown, arrived and allowed. "No walking, running or jumping while raising" is a query on the body, `Humanoid.is_raising_tablet()` (state `raise_1h`), which the brain's input filter asks.
- Review, decided: `set_visual_visible()` hides only the model's `MeshInstance3D` nodes, not the skeleton, so the tablet on the `tablet` bone stays visible in two-handed first person (`humanoid.gd` line 197). This and the new tablet path (`Visual/human_model/.../Skeleton3D/TabletBone/TabletMount/TabletDevice`; `screen_glow_check.gd` lines 18 and 239 follow it) are added to the brief as a dated revision.
- Review, measured (2026-11-22): the glb puts the 5.0684 scale on node `rig` above `Skeleton3D`. Between the `tablet` bone's global pose and where the tablet must be, the offset is the same on raise frames 0, 5, 10, 16, 20 and the one-handed hold pose: origin 0, uniform scale 0.1973 (= 1 / 5.0684), +90 degrees about X. A fixed `TabletMount` node under the `BoneAttachment3D` carries it; the pins check the tablet's global scale is 1.
- Review: the baseline counts are 55 and 24 `PASS` lines for `a3_asset_check` / `screen_glow_check` (commit e466c00d's 56 / 25 also counted the summary line). All baseline runs exit 0. A7 runs every test at 60 fps only.
- Review: the untracked files the agent saw (`test_tablet_pins.gd`, the `.glb`, the export script, a probe) were written by my main Claude session preparing steps 4 and 5; the probe is deleted and the rest is committed in its own step.
- Which `godot_console` / `godot` is on `PATH` on the test machine is not recorded; set `GODOT` if neither is found.
