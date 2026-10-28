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

**3D object for the textured shader.** `res://assets/models/rock.glb` (two surfaces: 0 `Rock_Main`, 1
`Rock_Top`). The shader material is only in `showcase3d/material_compare.tscn`, as
`surface_material_override/0` on both rocks (dry and frosted); `rock.glb`, `rock.glb.import` and
`prop_room.tscn` stay as in Assignment 3 (CHANGE-BRIEF revision 2026-10-27). Lighting copied from
`prop_room.tscn:16–18, 28–30`. Materials and import settings: `walker-magic-zhefan/MATERIALS.md`.

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

Confirmed on this machine (Godot 4.7.2, 2026-10-23) unless marked.

- `get_shader_uniform_list()` works headless only after the main loop starts (in a SceneTree `_init()`:
  `Parameter "shader" is null`). A parse failure gives an empty list (`logs/mutation-1-semicolon_60fps.log`).
- A uniform renamed in the shader only raises no error: the driver's `set_shader_parameter("intensity")`
  is stored and read back, so 15 checks still passed; only the uniform-list and source-default checks
  failed (`logs/mutation-2-rename_60fps.log`). Defaults are not reported; tests read the source text.
- `--fixed-fps` is not in `OS.get_cmdline_args()`; `tests/test_hurt_tint.gd` reads fps from frame deltas.
- `invulnerable` changes only on physics ticks; across a pause, summed frame time drifts (CHANGE-BRIEF R7 revision).
- Not observed here, from the assignment text: the dummy renderer draws nothing; import detection runs only
  in a real editor, so run `git status` after the first editor session. `scripts/run-test.sh:10` fails on
  `SHADER ERROR` / `SCRIPT ERROR` because exit 0 does not mean no errors.

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
- In 3D: `rock.glb`, `rock.glb.import` and `prop_room.tscn` are never changed; the textured shader lives
  only in `material_compare.tscn` and `hint_experiment.tscn`.
- Existing tests and their expectations are not edited, weakened or deleted; new checks go in new files.
- `project.godot` settings, including the renderer, are not changed.
- No file outside `fall-2026/zhefan-z/assignment-5/`.

## Unconfirmed

- **Renderer at run time.** Forward+ is the engine default, not a value in `project.godot`; the headless
  tests use a dummy renderer (`tests/capture_scene.gd:2`), so no log here shows the renderer.
- **On screen.** Every look (tint, frost, hint quads, normal-map lighting) is a human check in the editor.
- **Physics rate.** 60 per second is the engine default for an unset key, not read from a file.
- No `AGENTS.md` or `README.md` exists at this folder's root.
