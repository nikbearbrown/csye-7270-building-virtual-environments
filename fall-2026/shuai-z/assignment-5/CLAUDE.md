# CLAUDE.md — walker-rudy, Assignment 5

## Project context

This folder holds two Godot projects, `game/` and `godot/`.

**Engine.** Godot 4.7: both `project.godot` files list the feature `"4.7"` (`game/project.godot:16`, `godot/project.godot:16`). The baseline logs print `Godot Engine v4.7.2.stable.official.ed1daf0bf` (`logs/game_checks_60fps.log:1`, `logs/godot_check_props_60fps.log:1`).

**`game/`, the 2D game ("Walker Rudy")**
- Renderer: GL Compatibility, `renderer/rendering_method="gl_compatibility"` on desktop and mobile (`game/project.godot:95-96`).
- Main scene: `res://app/main.tscn` (`game/project.godot:15`).
- Viewport 1920 × 1080, stretch mode `canvas_items` (`game/project.godot:25-29`). No `physics_ticks_per_second` and no HDR 2D setting, so both are at their defaults (`game/project.godot`, whole file).

**`godot/`, the 3D props scene ("Walker Rudy Props 3D")**
- Renderer: Forward+, the feature `"Forward Plus"` with no `rendering_method` override (`godot/project.godot:16`).
- Main scene: `res://scenes/props_room.tscn` (`godot/project.godot:15`).

**The object the 2D effect changes: the hearts**
- `Hud/Hearts` is one `Control` with `hearts.gd`, `texture_filter = 4` and the material `res://ui/hearts_tint.tres` (`game/ui/hud.tscn:6`, `hud.tscn:11-21`). That `ShaderMaterial` uses `res://shaders/invulnerable_tint.gdshader` and is local to the scene (`game/ui/hearts_tint.tres:3-7`).
- `Hearts._draw()` draws all the hearts with `draw_texture_rect()`, using `UI-HEART-FULL.png` for the first `shown` and `UI-HEART-EMPTY.png` for the rest, `SPACING` 60 px apart, at 1/`DENSITY` (`game/ui/hearts.gd:6-9`, `game/ui/hearts.gd:21-24`).
- `hud.gd` sets `max_hearts` and `shown` from Rudy (`game/ui/hud.gd:25-33`). It hides the hearts on the title with `modulate.a = 0.0` (`game/ui/hud.gd:55`) and fades them in with a tween (`game/ui/hud.gd:62`). With the material on, the fade-in still works, checked by eye on 2026-10-28 (`TEST-REPORT.md` section 4).
- The driver: every frame, `_process()` calls `_tint_hearts()` before the debug line's early return, and `_tint_hearts()` sets only `tint_amount`, to Rudy's `_invulnerable_left / invulnerable_time` (`game/ui/hud.gd:89-94`, `hud.gd:110-111`).
- `hint_range` does not clamp a value set from code: with `tint_amount` set to 2.0, the material reads back 2.0 and the hearts' pixels land on the unclamped prediction (`logs/capture_tint.log:27-29`).

**Game state that drives the effect: Rudy's invulnerability, owned by `game/content/rudy/rudy.gd`**
- `invulnerable_time := 1.2` (`rudy.gd:75`); `_invulnerable_left := 0.0` (`rudy.gd:88`).
- `is_invulnerable()` returns `_invulnerable_left > 0.0` (`rudy.gd:112-113`). While it is true, `take_hit()` returns false (`rudy.gd:129-130`).
- The window opens in `take_hit()` (`rudy.gd:144`) and in `respawn_at()` (`rudy.gd:188`).
- `_count_down()` runs it down once per physics tick (`rudy.gd:263-264`); `_physics_process()` calls it (`rudy.gd:230`).
- The existing flicker on `Look` is `modulate.a` (`rudy.gd:232`).
- Tree order in `main.tscn` is Level1, Rudy, Camera, Hud, SystemKeys (`game/app/main.tscn:12-26`).
- The spikes and the goblins call `take_hit()` from their own `_physics_process()` (`game/content/level_1/spikes.gd:15-18`, `game/content/goblin/goblin.gd:49`, `goblin.gd:60`). In that tree order they run before Rudy's countdown in the same tick.
- Esc pauses with `get_tree().paused` (`game/app/main.gd:159`). Only `app/system_keys.gd:15` and `systems/audio/music.gd:40` use `PROCESS_MODE_ALWAYS`; everything else stops while paused.
- A defeat respawns Rudy after `DEFEAT_HOLD` 0.8 s and `FADE_TIME` 0.35 s (`main.gd:41-42`, `main.gd:128`). Enter on the end card reloads the scene (`main.gd:209`).
- The tint colour comes from the waystone: `GLOW := Color(0.6, 0.88, 1.0)` (`game/content/level_1/waystone.gd:19`).

**3D objects for the textured shader** (in `godot/scenes/props_room.tscn`)
- `Waystone` is an instance of `res://assets/props/waystone.glb` (`props_room.tscn:4`, `props_room.tscn:50-51`). Its material `Stone` must stay `#8C8A80` in the imported `.glb` (`godot/tests/check_props.gd:20-21`).
- `TeleportCircle` is an instance of `res://assets/props/teleport_circle.glb` (`props_room.tscn:6`, `props_room.tscn:56-57`). Its material `DarkStone` must stay `#4A4440` (`check_props.gd:22-23`).
- The meshes inside the instances are `Waystone/Waystone`, with surfaces 0 `Stone`, 1 `Moss` and 2 `Rune`, and `TeleportCircle/TeleportCircle`, with surfaces 0 `Gold`, 1 `DarkStone` and 2 `PaleGold`. All are `StandardMaterial3D` (`logs/probe_surfaces.log`, from `evidence/headless-probe/probe_surfaces.gd`). So the overrides go on surface 0 of the waystone's mesh and surface 1 of the circle's.
- The imported materials stay embedded in each `.glb`; nothing is extracted (`materials/extract=0` and `_subresources={}` in `godot/assets/props/waystone.glb.import:39-42` and `teleport_circle.glb.import:39-42`).
- The scene overrides surface 0 of `Waystone/Waystone` with `res://materials/waystone_stone.tres` and surface 1 of `TeleportCircle/TeleportCircle` with `res://materials/circle_darkstone.tres` (`props_room.tscn:5`, `props_room.tscn:7`, `props_room.tscn:53-54`, `props_room.tscn:59-60`, `props_room.tscn:71-72`). `godot/tools/add_stone_overrides.gd` set them; the other six surfaces keep their imported materials (`logs/probe_overrides.log`).
- `check_props.gd` reads every imported material's `albedo_color` by `resource_name`, but only while the material is a `BaseMaterial3D` (`check_props.gd:81-89`). That is why the brief uses surface material overrides in the scene and not *Use External* (`CHANGE-BRIEF.md` section 5).
- Lighting is the Environment sub-resource and `Sun` (`props_room.tscn:9-15`, `props_room.tscn:42-45`).

**The textured shader, its textures and the hint experiment** (in `godot/`)
- `shaders/weathered_stone.gdshader` has the samplers `albedo_tex`, `normal_tex` and `roughness_tex` (lines 3-5) and the groups `surface` and `relief` (lines 7-14). `materials/waystone_stone.tres` and `materials/circle_darkstone.tres` both use it, with the Rock 01 textures.
- The textures are in `assets/textures/rock_01/`, with `ATTRIBUTION.md`; each one's import settings are in the `.import` file beside it. They import as DXT1 (colour, roughness) and RGTC_RG (OpenGL normal) with 10 mipmap levels, and `_nor_dx`, which no material uses, as RGB8 with none (`logs/probe_textures.log`).
- The hint experiment is `shaders/hint_experiment.gdshader`, `materials/hint_source_color.tres` and `materials/hint_plain.tres`, and `scenes/hint_experiment.tscn`, built by `tools/build_hint_experiment.gd`. Its strip, `assets/hint_experiment/grey_strip_3x1.png`, is written by `tools/write_grey_strip.gd`. The scene's tonemap, exposure, glow, fog and adjustments are at their defaults, so the file leaves them out (`hint_experiment.tscn:6-8`, `logs/probe_hint_scene.log`). In a window, its bands show 64, 128 and 192 with `source_color` and 137, 188 and 225 without, as the brief predicted (`logs/capture_hint.log:7-12`).
- `tests/normal_map_check.gd` is the assignment's curl check, unchanged. Calibrated on Rock 01, `_nor_gl` gives 0.1444 with `directx = false` and 1.8556 with `true`, and `_nor_dx` the reverse (`logs/godot_calibrate_normal_map_check_60fps.log`). The threshold is 0.5, the human's choice: each file, read in its own convention, must come out under it (`tests/calibrate_normal_map_check.gd:14-17`, `calibrate_normal_map_check.gd:38-41`).
- Under the scene's lighting, `normal_strength` and `roughness_offset` move the waystone's pixels by under 3 steps on average across their ranges, a change Claude could not see in the captures (`logs/capture_sweep.log:21-31`, `TEST-REPORT.md` section 7).
- `shaders/standard_generated.gdshader` is the shader Godot generated from a StandardMaterial3D with Rock 01's textures, annotated by the human, and nothing uses it (`fe795908`). It compiles with 16 uniforms (`logs/probe_standard_generated.log:6`). `LANGUAGE-NOTES.md` cites its line numbers.

**Tests: always run through `scripts/run-test.sh <game|godot> <test-file> <fps>`** (`scripts/run-test.sh:2`)
- Run from this folder: `scripts/run-test.sh game checks.tscn 60` gives 141 checks and ends `all checks passed` (`logs/game_checks_60fps.log`). `checks.tscn` runs `checks.gd` as the scene (`game/tests/checks.tscn`).
- `checks.gd` prints one `PASS` or `FAIL` line per check and ends `all checks passed` or `N check(s) FAILED` (`game/tests/checks.gd:1659`, `checks.gd:111`). The 141 is its `PASS` lines.
- `scripts/run-test.sh godot check_props.gd 60` gives 44 `ok` lines and `PASS: 0 failed check(s)` (`logs/godot_check_props_60fps.log`).
- `scripts/run-test.sh godot calibrate_normal_map_check.gd 60` prints the four ratios, gives 4 `PASS` lines and ends `all checks passed` (`logs/godot_calibrate_normal_map_check_60fps.log`).
- `scripts/run-test.sh game invulnerable_tint_checks.tscn <fps>`, at 30, 60 and 144, gives 15 `PASS` lines and ends `all checks passed` at each rate (`logs/game_invulnerable_tint_checks_30fps.log`, `_60fps.log`, `_144fps.log`).
- `scripts/run-test.sh godot test_materials.gd 60` gives 125 `PASS` lines and ends `all checks passed` (`logs/godot_test_materials_60fps.log`).
- The wrapper does five things (`scripts/run-test.sh:19-38`):
  - it runs a `.tscn` as the scene and a `.gd` with `--script`;
  - it pins `--fixed-fps`;
  - it times out after 120 s (status 124 means a hang);
  - it writes `logs/<project>_<test>_<fps>fps.log`;
  - it fails on any `SHADER ERROR` or `SCRIPT ERROR` line, whatever the exit code.
- Exit 0 alone is not a pass. Read the log.
- `game/tests/capture.tscn` and `capture_tint.tscn`, and `godot/tests/capture_props.gd`, `capture_hint.gd`, `capture_sweep.gd` and `capture_hint_vs_os.gd`, open a window and save screenshots; each script's first comment lines give its command (`game/tests/capture.gd:1-7`, `capture_tint.gd:2-10`, `godot/tests/capture_props.gd:1-7`, `capture_hint.gd:2-8`, `capture_sweep.gd:2-16`, `capture_hint_vs_os.gd:2-8`). They are not headless tests.
- Checks that guard this change:
  - Rudy's `Look/Sprite` must keep `res://systems/art/outline.gdshader` (`game/tests/checks.gd:871-877`);
  - only `SpikesA`, `SpikesB` and `GoblinA` may carry a material among the placed level sprites (`game/tests/checks.gd:1056-1061`).
- `systems/art/outline.tres` is one material shared by Rudy, the goblin and the spikes (`game/content/rudy/rudy.tscn:6`, `game/content/goblin/goblin.tscn:5`, `game/content/level_1/spikes.tscn:5`).

**Headless facts on this machine** (checked 2026-10-26 and 2026-10-27 with Godot 4.7.2 on macOS 15.1, in `evidence/headless-probe/`):
- `--headless` gives the headless display server and the dummy renderer, with no video adapter. It runs Godot's shader parser, so a broken shader prints `SHADER ERROR`, but it draws nothing, and the frame cannot be read back (`logs/probe_headless.log`).
- A shader error does not change Godot's exit code: the probe exited 0 after one (`logs/probe_headless.log` for the error, `logs/probe_headless_rendering_driver.log` for the `exit 0` lines). Any `SHADER ERROR` line in a log is a failure, whatever the exit code; the wrapper enforces this.
- A `.gdshader` error is reported when the shader is set on a `ShaderMaterial`, not when it is loaded. A shader that failed to parse has an empty `get_shader_uniform_list()`. The dummy renderer reports no uniform defaults (`shader_get_parameter_default()` is null), so a test reads defaults from the source text (`logs/probe_headless.log`).
- `get_shader_uniform_list()` reports a sampler as an `Object` with the hint string `Texture2D`, and none of its hints (`source_color`, `hint_normal`, filters), so a test reads them from the source text (`logs/probe_weathered_stone.log`).
- An imported texture's format and mipmaps can be read headlessly with `get_image()` (`logs/probe_textures.log`).
- A headless `--import` compiles only the shaders the main scene uses. A broken shader that nothing uses yet raises no error on import, so a clean import says nothing about it (`logs/probe_import_check.log`, from `evidence/headless-probe/import_check.sh`).
- A windowed capture waits for `RenderingServer.frame_post_draw`, which a headless run never sends, so the first headless dry runs of the capture tools hung until `timeout` ended them with 124. The four capture tools this assignment added quit with exit 1 when the display server is `headless` (`game/tests/capture_tint.gd:32-34`, `godot/tests/capture_hint.gd:23-25`, `capture_sweep.gd:38-40`, `capture_hint_vs_os.gd:16-18`; `FRICTIONAL.md`, "The windowed captures of the hearts and the hint experiment").
- Use `--headless` exactly, as the wrapper does. Here, adding `--rendering-driver metal` or `vulkan` to it, in either order, still stayed headless (`logs/probe_headless_rendering_driver.log`). Example 06 saw the long form, `--display-driver headless`, fall back to a window on macOS, and nothing in this folder needs `--rendering-driver`.

## Current change

@CHANGE-BRIEF.md

## Ownership

Every file in `game/shaders/` and `godot/shaders/` is written by hand by the human. An agent never creates, edits, reformats or "fixes" any of them, even to make a test pass. If a shader looks wrong, report it and stop. `game/shaders/` holds `invulnerable_tint.gdshader` (`ae0a3757`), and `godot/shaders/` holds `weathered_stone.gdshader` (`a87a18be`), `hint_experiment.gdshader` (`9481663a`) and `standard_generated.gdshader`, generated by the editor and annotated by the human (`fe795908`), each committed on its own.

## Out of scope

- `game/content/rudy/rudy.gd` stays byte for byte. Presentation code may read `_invulnerable_left` and `invulnerable_time`, but never assigns them or any other game state.
- Don't touch movement, collision, input, or the state machine and its timings in `rudy.gd` and `game/app/main.gd`. That covers the 1.2 s window, the 0.35 s hurt time and the 0.12 s flicker.
- Leave the outline material (`systems/art/outline.tres` / `outline.gdshader`) and where it is used alone. In `game/`, Rudy, the goblins, the spikes, the waystone, the circle and the pickup get no new material.
- No HUD element except `Hud/Hearts` changes: not the title, debug line, fade, end card or "Paused".
- No existing test, or anything it expects, changes: 141 checks in `game/`, 44 in `godot/`. New tests are added beside them.
- In `godot/`, the `.glb` files and their `.import` files stay as they are. Don't switch the imported materials to *Use External*, and don't re-run `godot/tools/build_props_room.gd` once the overrides are in.
- Only the waystone's Stone surface and the circle's DarkStone surface get the textured material. Moss, Rune, Gold, PaleGold and the spikes keep their imported colours.
- Leave the lighting and environment of `props_room.tscn` unchanged.
- No project setting changes in either `project.godot`: not the renderer, HDR 2D, physics tick rate or stretch.

## Unconfirmed

- **Why the hearts need no sRGB step.** The brief computes on the values as written, from Chapter 6's reading of the Compatibility renderer's source, not from a file here. The captures match those predictions exactly at 0.0, 0.5 and 1.0 (`logs/capture_tint.log:10-25`), but the reason itself is not checked in this folder.
- **Missing files.** There is no `AGENTS.md` in this folder, so this file does not begin with `@AGENTS.md`.
