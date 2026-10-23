# CLAUDE.md — walker-magic-zhefan, Assignment 5

Treat `fall-2026/zhefan-z/assignment-5/` as the repository root; do not read or change anything outside it.
Paths below are relative to that folder. `res://` = `walker-magic-zhefan/`.

## Project context

**Engine.** Godot 4.7.2-stable (official build `ed1daf0bf`): `logs/baseline-before/test_wolf_60fps.log:1`, binary path in
`scripts/run-test.sh:5`. The project declares feature `"4.7"` (`walker-magic-zhefan/project.godot:15`).

**Renderer.** Not set: the `[rendering]` section (`project.godot:39–43`) has only the 2D texture filter
and pixel snapping, no `rendering_method`, so the engine default applies; `CHANGE-BRIEF.md:195` records
that as Forward+. 2D: 640×360 viewport, `stretch/mode="viewport"`, integer scaling (`project.godot:23–29`);
no `hdr_2d` key. Physics tick rate is not set, so the default 60 per second applies (`CHANGE-BRIEF.md:26`).

**Main scene.** `res://game/main.tscn` (`project.godot:14`). The player is instanced there as `Player`
(`game/main.tscn:90–91`); `UI` and `SessionInput` run while paused (`process_mode = 3`,
`game/main.tscn:97,117`); pause is toggled by `toggle_pause()` (`game/main.gd:53–61`).

**How the shaded object is drawn.** The player's `Sprite2D` child (`features/player/player.tscn:15–18`):
`centered = false`, `offset = (-31, -67)`, no material today. Its texture is swapped per state by
`_set_state()` (`features/player/player.gd:130–133`) from the `TEXTURES` table (`player.gd:17–26`);
`fail()` sets the texture directly (`player.gd:178`). The existing blink sets `sprite.visible` every
physics tick while invulnerable, toggling it every `BLINK_PERIOD` = 0.1 s (`player.gd:81`, `BLINK_PERIOD` at `features/player/tuning.gd:19`).

**Game state that drives the effect.** Owned by `features/player/player.gd` (class `Player`):
- `invulnerable`, seconds left (`player.gd:37`); set to `Tuning.INVULNERABLE_TIME` = 1.0 when a hit
  lands (`player.gd:155`, `tuning.gd:16`); counted down with physics `delta` (`player.gd:80`).
- Hits are ignored while `invulnerable > 0.0`, failing or cleared (`player.gd:152`).
- `win()` clears it to 0.0 and sets `is_cleared` (`player.gd:137–146`).
- `fail()` sets `is_failing` and stops `_physics_process` without clearing `invulnerable`
  (`player.gd:170–180`); the final hit sets it to 1.0 first (`player.gd:155`, `player.gd:162–163`).

**3D object for the textured shader.** `res://assets/models/rock.glb`, instanced as node `Rock` at
x = −1.2 in `showcase3d/prop_room.tscn:46–47`. Its material today comes from the `.glb` itself: two glTF
materials, `Rock_Main` and `Rock_Top` (read from the file's glTF JSON chunk), imported with
`materials/extract=0` and `_subresources={}` (`assets/models/rock.glb.import:39–42`), so no external
material is set yet. Lighting: `DirectionalLight3D` "Sun" with shadows (`prop_room.tscn:28–30`) and an
`Environment` with a solid background colour (`prop_room.tscn:16–18`, `:25–26`). The planned textures are
present in `walker-magic-zhefan/assets/textures/rock_01/` (diff, nor_gl, nor_dx, rough, 1K PNG).

**Tests.** Every test runs through `scripts/run-test.sh <test-file.gd> <fps>`, from this folder in Git Bash
(`scripts/run-test.sh:2–3`). It runs Godot headless with `--fixed-fps <fps>` under a 120 s timeout, writes
(and overwrites) `logs/<test>_<fps>fps.log`, and fails on a non-zero exit or any `SHADER ERROR` /
`SCRIPT ERROR` line (`scripts/run-test.sh:7–11`).

```bash
bash scripts/run-test.sh test_player.gd 60
bash scripts/run-test.sh test_cast.gd 60
bash scripts/run-test.sh test_wolf.gd 60
bash scripts/run-test.sh test_flow.gd 60
bash scripts/run-test.sh test_audio.gd 60
bash scripts/run-test.sh test_sound_triggers.gd 60
bash scripts/run-test.sh test_a3_assets.gd 60
# new tests for this change run at 30, 60 and 144:
# bash scripts/run-test.sh <new_test>.gd 30   (then 60, 144)
```

Baseline before this change, at 60 fps, all passing (`logs/baseline-before/*.log`): a3_assets 22,
audio 13, cast 11, flow 14, player 11, sound_triggers 11, wolf 13 checks, 0 failures.
`tests/capture_scene.gd` is not a run-test.sh test: it needs a real window and an output folder
argument (`walker-magic-zhefan/tests/capture_scene.gd:2–4`).

## Headless facts

From the assignment text; to be confirmed on this machine in Step 2, then this block is updated.

- A headless run uses a dummy renderer: it draws nothing, so no test here can judge colour or look.
- `get_shader_uniform_list()` reports declared uniforms headlessly; a shader that fails to parse returns an
  empty list. Defaults are not reported, so tests read them from the shader source text.
- `set_shader_parameter()` with a name the shader does not declare raises no error, and reading it back
  returns the stored value; only the uniform-list assertion catches a renamed uniform.
- Exit code 0 does not mean no errors: `scripts/run-test.sh:10` fails on `SHADER ERROR` / `SCRIPT ERROR`.
  Texture import detection only runs when a real editor draws the texture, so `git status` after the first
  editor session.

## Current change

@CHANGE-BRIEF.md

## Ownership

Files in `walker-magic-zhefan/shaders/` are hand-written by the human and are never edited by an agent.
This includes `shaders/hurt_tint.gdshader`, `shaders/rock_frost.gdshader` (`CHANGE-BRIEF.md:30,125`), the
hint-experiment shader, and `shaders/standard_generated.gdshader` (written by the editor's convert action):
an agent may read them, report problems and suggest changes, but never creates, edits, moves or deletes them.

## Out of scope

- Game logic stays as it is: player movement, collision, input, the state machine, `take_damage`,
  `fail`, `win`, every value in `tuning.gd`, and the existing blink. The tint driver only reads `Player`
  state and never writes it; a retrigger is not added, because it would need a game-logic change.
- Everything else in the 2D game: the wolf (including its own `features/wolf/flash.gdshader`), the level,
  audio, the HUD and the camera. Only the player's sprite gets a new material.
- In 3D, only the rock: `rock.glb` is never changed (only `rock.glb.import`), and the crystal, the chest,
  the floor and the prop room's light and environment stay as they are.
- Existing tests and their expectations are not edited, weakened or deleted; new checks go in new files.
- `project.godot` settings, including the renderer, are not changed.
- No file outside `fall-2026/zhefan-z/assignment-5/`.

## Unconfirmed

- **Renderer at run time.** Forward+ is the engine default, not a value in `project.godot`; the headless
  tests use a dummy renderer (`tests/capture_scene.gd:2`), so no log here shows the renderer.
- **Two rock materials: resolved.** `rock.glb` has `Rock_Main` and `Rock_Top`. Only `Rock_Main` gets the shader
  material; `Rock_Top` keeps its imported material (CHANGE-BRIEF revision 2026-10-23). The surface index of
  `Rock_Main` is still to be confirmed in the editor.
- **Not created yet:** `walker-magic-zhefan/shaders/`, `assets/materials/` (`mat_rock_dry.tres`,
  `mat_rock_frosted.tres`), `showcase3d/material_compare.tscn`, `assets/textures/hint/`, the tint driver
  script, and the new test files. Their names come from `CHANGE-BRIEF.md`; the driver's path and wiring
  are still open (`CHANGE-BRIEF.md:35`).
- **Texture imports.** The `rock_01` PNGs have no `.import` files yet, so none of the import settings in
  `CHANGE-BRIEF.md:131–138` are applied, and the format of the 16-bit roughness file is unknown.
- **Other frame rates.** Only 60 fps baseline logs exist; behaviour at 30 and 144 fps has not been run.
- **Physics rate.** 60 per second is the engine default for an unset key, not read from a file.
- No `AGENTS.md` or `README.md` exists at this folder's root.
