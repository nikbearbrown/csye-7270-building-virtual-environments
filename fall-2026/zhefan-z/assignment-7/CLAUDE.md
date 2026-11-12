# CLAUDE.md — walker-magic-zhefan, Assignment 7

Treat `fall-2026/zhefan-z/assignment-7/` as the repository root; do not read or change anything outside it.
Paths below are relative to that folder. `res://` = `walker-magic-zhefan/`. No `AGENTS.md` or `README.md` exists here.

## Project context

**Engine.** Godot 4.7.2-stable (official build `ed1daf0bf`): `logs/baseline-before/test_wolf_60fps.log:1`, binary path in
`scripts/run-test.sh:5`. Feature `"4.7"` (`walker-magic-zhefan/project.godot:15`); no physics rate set, so 60 ticks/s.
**Renderer.** Not set: `[rendering]` (`project.godot:39–43`) has no `rendering_method`, so the default, Forward+
(`CHANGE-BRIEF.md:5`). 2D, 640×360 viewport, window 1280×720, stretch `viewport`, integer scale (`project.godot:23–29`).

**Clip 1, mage run cycle** (`CHANGE-BRIEF.md:23–31`). Route: `Sprite2D` + one AnimationPlayer frame track on a new sheet
`assets/sprites/mage/mage_run_sheet.png` (124×69, `hframes = 2`, frame 0 contact, 1 passing; `:27`), built by a committed
tool from `mage_run_contact.png` and `mage_run_passing.png`. Driven by `features/player/player.gd`: states
`IDLE, RUN, RISE, FALL, CAST, HURT, FAIL, WIN` (`:15`), one texture each (`TEXTURES`, `:17–26`). `_physics_process`
(`:58–97`) ends in `_update_state()` (`:115–127`), which calls `_set_state()` (`:130–133`: sets `state`, `sprite.texture`,
`flip_h`). Also writing the texture: `_ready()` (`:55`), `win()` (`:145`), `take_damage()` (`:165`), `fail()` (`:177–179`,
FALL image for the pit, FAIL otherwise), `capture_pose()` (`:184–188`). `player.gd:81` sets `sprite.visible` (blink).

**Clip 2, wolf lunge** (`CHANGE-BRIEF.md:33–55`). Route: cutout rig keyed as resource text in `wolf.tscn` or a committed
`.tres`; parts are `region_rect`s of `assets/sprites/wolf/wolf_lunge.png`; nodes `Facing → Rig → RearPivot/FrontPivot`;
one clip `lunge`, 1.45 s, `LOOP_NONE`, played from 0 on GROWL entry. Driven by `features/wolf/wolf.gd`: states
`PATROL, GROWL, LUNGE, RECOVER, DEAD` (`:11`); `GROWL_TIME` 0.5, `LUNGE_SPEED` 220, `LUNGE_TIME` 0.35, `RECOVER_TIME` 0.6
(`:21–24`). `_physics_process` (`:58–92`): `_timer` counts down per tick (`:59`), PATROL → GROWL on sight (`:67–68`),
GROWL → LUNGE (`:72–73`), the hit loop and LUNGE → RECOVER (`:74–82`), RECOVER → PATROL (`:83–86`). `_enter()` (`:95–111`)
sets timers and textures; hitbox `monitoring = true` on LUNGE (`:106`), `set_deferred(... false)` on RECOVER (`:110`).
`take_damage()` (`:137–151`): flash, HP −1, DEAD only at 0 HP, freed after `DOWN_TIME` 0.6 s on a SceneTree timer (`:150`).
Facing is `sprite.flip_h` plus shape offsets (`:126–129`); the flash material is duplicated per wolf (`:54`, `:154–159`).

**Scenes.** `res://game/main.tscn` is the main scene (`project.godot:14`): `Level/Wolf` at (860, 327) in group `wolves`
(`main.tscn:67–68`), `Player` at (60, 327) (`:90–91`), `UI` and `SessionInput` with `process_mode = 3` (`:97, :117`).
`Main` gives each wolf its `target` (`game/main.gd:36–38`), follows the player with the camera in `_process` (`:47–50`),
toggles pause (`:53–61`); `test_mode` stops reloads (`:11, :91–98`). `features/player/player.tscn`: `Sprite2D` with the
hurt-tint `ShaderMaterial`, `centered = false`, `offset (-31, -67)` (`:21–25`), 14×44 body (`:27–29`), `HurtTint` driver
(`:31–32`, reads `invulnerable`, writes `intensity`: `hurt_tint_driver.gd:10–15`). `features/wolf/wolf.tscn`: `Sprite2D`
with the flash material, `offset (-40, -38)` (`:21–25`), body 48×28 at (8, −14) (`:27–29`), `LungeHitbox` (`:31–36`).

**Tests.** Every test runs through `scripts/run-test.sh <test-file.gd> <fps|realtime> [timeout-seconds]` from this folder in
Git Bash (`:2`). A number runs headless with `--fixed-fps <fps>`; `realtime` passes none (`:7–11`); timeout 120 s by default
(`:13`). It overwrites `logs/<test>_<fps>fps.log` (`:12`) and fails on a non-zero exit or any `SHADER ERROR`, `SCRIPT ERROR`,
`Failed loading resource`, `Failed to load resource` or `Parse Error` line (`:15`).

```bash
./scripts/run-test.sh test_wolf.gd 60        # same for the other 60-only suites in the baseline below
./scripts/run-test.sh test_hurt_tint.gd 30   # also 60 and 144; same for test_fireball_impact and test_fireball_trail
```

Baseline (`logs/baseline-before/`, commit `2276069`), 13 suites, all 0 failures: a3_assets 22, audio 13, cast 11, flow 14,
player 11, sound_triggers 11, wolf 13, materials 32, fireball_impact_config 54, fireball_trail_config 32 at 60 fps;
hurt_tint 17, fireball_impact 14, fireball_trail 20 at 30, 60 and 144. New suites: `CHANGE-BRIEF.md:74–80`.

## Headless facts

Confirmed on this machine (Godot 4.7.2, 2026-10-23) unless marked.

- `get_shader_uniform_list()` works headless only after the main loop starts (in a SceneTree `_init()`:
  `Parameter "shader" is null`). A parse failure gives an empty list (A5 `logs/mutation-1-semicolon_60fps.log` at `2b68e0a`).
- A uniform renamed in the shader only raises no error: the driver's `set_shader_parameter("intensity")`
  is stored and read back, so 15 checks still passed; only the uniform-list and source-default checks
  failed (A5 `logs/mutation-2-rename_60fps.log` at `2b68e0a`). Defaults are not reported; tests read the source text.
- `--fixed-fps` is not in `OS.get_cmdline_args()`; `tests/test_hurt_tint.gd` reads fps from frame deltas.
- `invulnerable` changes only on physics ticks; across a pause, summed frame time drifts (CHANGE-BRIEF R7 revision).
- A6, 2026-11-05 (`logs/test_fireball_impact_config_60fps.log`): headless draws no particles and runs no GPU particle
  process (0 draw calls, empty `capture_rect()`); instance counts, `one_shot`, `amount_ratio`, visibility are observable.
  `emitting` turns false once all are emitted, not when they die; `finished` did not fire: test aliveness by instance.
  A GPU effect's headless CPU price is near zero by construction (4.6 vs 6.6 µs/frame with 6 impacts). Frame strips
  come from a windowed Movie Maker run, which I start.
- From the assignment text: import detection runs only in a real editor (`git status` after an editor session);
  `scripts/run-test.sh` fails on `SHADER ERROR` / `SCRIPT ERROR` because exit 0 does not mean no errors.

## Current change
@CHANGE-BRIEF.md

## Ownership

- Files in `walker-magic-zhefan/shaders/` are hand-written by the human and are never edited by an agent: an agent may read
  them, report problems and suggest changes, but never creates, edits, moves, deletes or commits them.
- Clip keys live in scene (`.tscn`) or resource (`.tres`) files, never in code. A bake script may write a `.tres` once; game
  code only calls `play()` / `seek()` and never builds tracks or keys at run time.
- One AnimationPlayer per sprite (mage, wolf), sole owner of what it keys (mage `texture`, `hframes`, `frame`; wolf rig
  transforms). Code keeps `flip_h` / `Facing.scale.x`, `visible` (blink, `player.gd:81`) and the materials.
## Godot 4 names

Use Godot 4.7 names, never Godot 3: `loop_mode` (`Animation.LOOP_NONE / LOOP_LINEAR`), not `loop`; `speed_scale`, not
`playback_speed`; `AnimatedSprite2D.sprite_frames` and `play()`, not `frames` and `playing`; `callback_mode_process`, not
`playback_process_mode`; tracks through `Animation.track_*` and an `AnimationLibrary`. If unsure a property exists, check it
headless on this binary with `ClassDB.class_has_method()` / `ClassDB.class_get_property_list()` and report misses.

## Input

Tests drive input with `Input.parse_input_event` by default: key and mouse events as in `tests/test_fireball_impact.gd:125–149`
and `tests/test_hurt_tint.gd:85–95`. `Input.action_press` makes no event, so it never reaches `_input` or `_unhandled_input`
(Esc, R, M, N go through `game/session_input.gd:6–14`); it only changes what `player.gd:191–223` polls.

## Two clocks

Each AnimationPlayer's `callback_mode_process` decides its clock; both must be `ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS`
(`CHANGE-BRIEF.md:31, 54`), the tick gameplay reads: `Player._physics_process` (`player.gd:58`) and the wolf's `_timer`
(`wolf.gd:59`). Process-clock code: the camera (`main.gd:47–50`), the hurt-tint driver, and SceneTree timers for the wolf's
flash and its removal (`wolf.gd:150, 157`). Compare clip frame n with physics tick n, never with summed frame time.

## Commits
Commit only what the human asks for. Every message says who wrote the content, e.g. "(agent, unedited)" or
"(mine, committed by Claude Code at my request)". No `Co-Authored-By` trailer. Never push. Nothing under `shaders/`.
## Resuming
After an interrupted session, first run `git status` and rerun the last test (newest file in `logs/`) before any edit.
## Out of scope
- Everything in `CHANGE-BRIEF.md:83–85` (Boundaries): collision, movement, input, damage, every timing in `tuning.gd` and
  `wolf.gd`, the fireball and both A6 effects, the hurt tint, the A3 prop room, `project.godot`, the original sprite PNGs.
- The only gameplay change is the growl interrupt (`CHANGE-BRIEF.md:57–66`), made after the pin and re-pinned only after the
  human plays it. Existing tests are not edited, weakened or deleted. The capture overlay is debug-only (`:89`).

## Unconfirmed
- GROWL/LUNGE/RECOVER tick counts (brief assumes 30, 21, 36; `CHANGE-BRIEF.md:55`): the pin measures them.
- Brief line references for the wolf are off by a few lines (`:18–20` vs `wolf.gd:121–129, 137–151, 154–159`).
- `scripts/run-test.sh:3` and test headers name the A5/A6 folders (e.g. `tests/test_fireball_impact.gd:5`).
- Hip and shoulder pivots are not measured yet (`CHANGE-BRIEF.md:37`); no AnimationPlayer property has been checked
  with ClassDB on this binary; whether the wolf's removal timer (`wolf.gd:150`) lands on the same tick at every fps.
