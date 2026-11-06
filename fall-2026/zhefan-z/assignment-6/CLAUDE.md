# CLAUDE.md — walker-magic-zhefan, Assignment 6

Treat `fall-2026/zhefan-z/assignment-6/` as the repository root; do not read or change anything outside it.
Paths below are relative to that folder. `res://` = `walker-magic-zhefan/`. No `AGENTS.md` or `README.md` exists here.

## Project context

**Engine.** Godot 4.7.2-stable (official build `ed1daf0bf`): `logs/baseline-before/test_wolf_60fps.log:1`, binary path in
`scripts/run-test.sh:5`. The project declares feature `"4.7"` (`walker-magic-zhefan/project.godot:15`).

**Renderer.** Not set: `[rendering]` (`project.godot:39–43`) has no `rendering_method`, so the default, Forward+;
confirmed at run time in A5 ("Vulkan 1.4.312 - Forward+", RTX 5060 Laptop GPU; A5 `TEST-REPORT.md` at `2b68e0a`). 2D, 640×360 viewport, window 1280×720, stretch `viewport`, integer scale (`project.godot:23–29`).

**Node types** (`CHANGE-BRIEF.md`). Effect A: `effects/fireball_impact.tscn`, root `Node2D` `FireballImpact` that frees
itself after 0.9 s (`:38`), children `Sparks` and `Smoke`, both `GPUParticles2D` (`:42`). The A2 `burst.tscn` flash is
not inside it: `explode()` still instances it into `Main` as before (brief revision 2026-11-05). Effect B: `effects/fireball_trail.tscn`, one `GPUParticles2D`, a child of the fireball
(`:95`). `walker-magic-zhefan/effects/` and `assets/textures/fx/` (`spark.png`, `smoke.png`, `:52, :58`) do not exist yet.

**Who owns each event or condition.**
- `Fireball` (`features/fireball/fireball.gd:1–2`, an `Area2D`) declares no signals. `_ready()` connects the built-in
  `body_entered` (`:20`) to `_on_body_entered()`, which calls `take_damage` on a body that has it, then `explode()` (`:30–33`).
- Effect A event: `explode()` (`fireball.gd:37–45`): `_spent` guard (`:38–40`), instances `BURST` (`:9`) at
  `global_position` into `get_parent()` (`:41–43`), then `queue_free()` (`:45`). `burst.tscn` is a `Sprite2D` with
  `fx_burst.png` (`burst.tscn:6–8`); `burst.gd` frees it after `DURATION` = 0.15 s on a pausable timer (`burst.gd:4, 8`).
- Effect B condition: from `_ready()` (`fireball.gd:16`) until `explode()` or the timeout, where `_physics_process`
  frees it after `LIFETIME` = 2.0 s with no burst (`fireball.gd:7, 23–27`). `SPEED` = 260 (`:6`).
- `Player.cast()` adds each fireball to the player's parent, `Main`, and emits `cast_fired(origin, direction)`
  (`features/player/player.gd:9, 101–112`); casts are `Tuning.CAST_COOLDOWN` = 0.35 s apart (`features/player/tuning.gd:13`).
- Pause: `Main.toggle_pause()` sets `tree.paused` (`game/main.gd:53–61`). `fireball.tscn` and `Main` set no
  `process_mode`, so fireballs pause; only `UI` and `SessionInput` run while paused (`game/main.tscn:97, 117`).

**Scenes.** `res://game/main.tscn` is the main scene (`project.godot:14`); fireballs and impacts are children of `Main`
(`main.tscn:27`). Camera fixed at (320, 180) (`main.tscn:93–94`); background `CanvasLayer` at layer −10 (`:30–35`);
pit `Level/PitDark` (`:51–57`); walls at x −8 and 1288 (`:78–88`). `res://features/fireball/fireball.tscn`: `Area2D`
root, `Sprite2D` (offset (−6, 0)), `CollisionShape2D` with a `CircleShape2D` of radius 4 (`fireball.tscn:6–17`).

**Tests.** Every test runs through `scripts/run-test.sh <test-file.gd> <fps|realtime> [timeout-seconds]`, from this
folder in Git Bash (`scripts/run-test.sh:2–3`). A number runs Godot headless with `--fixed-fps <fps>`; `realtime`
passes no `--fixed-fps` (`:7–11`); timeout defaults to 120 s (`:13`). It overwrites `logs/<test>_<fps>fps.log` or
`logs/<test>_realtime.log` (`:12`) and fails on a non-zero exit or any `SHADER ERROR` / `SCRIPT ERROR` line (`:14–16`).

```bash
bash scripts/run-test.sh test_player.gd 60
bash scripts/run-test.sh test_cast.gd 60
bash scripts/run-test.sh test_wolf.gd 60
bash scripts/run-test.sh test_flow.gd 60
bash scripts/run-test.sh test_audio.gd 60
bash scripts/run-test.sh test_sound_triggers.gd 60
bash scripts/run-test.sh test_a3_assets.gd 60
bash scripts/run-test.sh test_materials.gd 60
bash scripts/run-test.sh test_hurt_tint.gd 30   # also 60 and 144
bash scripts/run-test.sh <test>.gd realtime 180  # realtime mode; third argument = timeout in seconds
```

Baseline before this change (`logs/baseline-before/*.log`, commit `1cebbd8`), all 0 failures: a3_assets 22, audio 13,
cast 11, flow 14, player 11, sound_triggers 11, wolf 13, materials 32 at 60 fps; hurt_tint 17 at 30, 60 and 144.
Not tests: `tests/capture_scene.gd` needs a real window (`:2–4`); `calibrate_normal_check.gd:3`, `inspect_rock_surfaces.gd:4` only print.

## Headless facts

Confirmed on this machine (Godot 4.7.2, 2026-10-23) unless marked.

- `get_shader_uniform_list()` works headless only after the main loop starts (in a SceneTree `_init()`:
  `Parameter "shader" is null`). A parse failure gives an empty list (A5 `logs/mutation-1-semicolon_60fps.log` at `2b68e0a`).
- A uniform renamed in the shader only raises no error: the driver's `set_shader_parameter("intensity")`
  is stored and read back, so 15 checks still passed; only the uniform-list and source-default checks
  failed (A5 `logs/mutation-2-rename_60fps.log` at `2b68e0a`). Defaults are not reported; tests read the source text.
- `--fixed-fps` is not in `OS.get_cmdline_args()`; `tests/test_hurt_tint.gd` reads fps from frame deltas.
- `invulnerable` changes only on physics ticks; across a pause, summed frame time drifts (CHANGE-BRIEF R7 revision).
- Not observed here, from the assignment text: the dummy renderer draws nothing; import detection runs only
  in a real editor, so run `git status` after the first editor session. `scripts/run-test.sh:10` fails on
  `SHADER ERROR` / `SCRIPT ERROR` because exit 0 does not mean no errors.

## Current change
@CHANGE-BRIEF.md

## Ownership

- Files in `walker-magic-zhefan/shaders/` are hand-written by the human and are never edited by an agent (`CHANGE-BRIEF.md:125`):
  an agent may read them, report problems and suggest changes, but never creates, edits, moves, deletes or commits them.
- Effect settings (every value in the brief's Settings tables) live in scene files in `walker-magic-zhefan/effects/`,
  not in code. Scripts may instance, move, stop and free an effect; they never set its particle or material values.

## Godot 4 names

Use Godot 4 class and property names for 4.7.2, never Godot 3 names. From the Godot 4 API, not checked on this binary:
- `GPUParticles2D` (not `Particles2D`); `ParticleProcessMaterial` (not `ParticlesMaterial`) in `process_material`;
  `CanvasItemMaterial`, `blend_mode = BLEND_MODE_ADD`; `GradientTexture1D` (not `GradientTexture`) for `color_ramp`;
  `CurveTexture` for `scale_curve`. Emission shapes: `EMISSION_SHAPE_POINT`, `EMISSION_SHAPE_SPHERE` + `emission_sphere_radius`.
- Ranges are `_min` / `_max` pairs: `initial_velocity_*`, `damping_*`, `scale_*`, `hue_variation_*`, `turbulence_influence_*`
  (Godot 3 had single `initial_velocity`, `scale`, ...). `direction` and `gravity` are `Vector3`: (1, 0) is `Vector3(1, 0, 0)`.
- Unsure, confirm first: `use_fixed_seed` / `seed` (`CHANGE-BRIEF.md:143` says 4.7 has them); whether 2D needs
  `particle_flag_disable_z`; how a `Curve` goes above 1 for the smoke's 1 → 2 scale (`:56`). Before writing a scene
  file, check every property you set with `ClassDB.class_get_property_list()` on this binary, headless; report misses.

## Commits

Commit only a commit the human asks for; its message says who wrote the content, e.g. "(agent draft, unedited)" or
"(mine, committed by Claude Code at my request)". No `Co-Authored-By` trailer, no push, nothing under `shaders/`.

## Out of scope

- Game logic: collision, movement, input, the player and wolf state machines, damage, every value in `tuning.gd`, every
  timing in `fireball.gd` (`CHANGE-BRIEF.md:125`). The only gameplay-script change is in `fireball.gd`: `explode()` also
  instances the impact, and the trail is stopped and detached (brief revision 2026-11-05; `CHANGE-BRIEF.md:111`).
- `burst.tscn`, `burst.gd` and how `explode()` instances the burst stay exactly as they are (`tests/test_cast.gd:55–56`).
  Presentation code reads game state and never writes it. Existing tests are not edited, weakened or deleted.
- A5 shaders, A3 prop room and 3D showcase, wolf, level, audio, HUD, camera, `project.godot`; nothing outside this folder.

## Unconfirmed

- **Camera.** Fixed in `main.tscn:93–94`; whether a script moves it (the walls are at x −8 and 1288) is not checked.
- **GPU particles headless.** Predicted to run no GPU particle process (`CHANGE-BRIEF.md:173`); not observed. Whether a
  hidden emitter keeps simulating is open (`CHANGE-BRIEF.md:120`). Physics rate: unset, so the 60/s engine default.
- The `logs/mutation-*.log` files in Headless facts are Assignment 5's, not in this `logs/`; test headers still say to
  run from `fall-2026/zhefan-z/assignment-5/` (e.g. `tests/test_hurt_tint.gd:4`).
- On screen: every look (timing, contrast, scale, `visibility_rect` at the walls) is a human check in the running game.
