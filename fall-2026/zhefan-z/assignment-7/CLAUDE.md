# CLAUDE.md — walker-magic-zhefan, Assignment 7

Treat `fall-2026/zhefan-z/assignment-7/` as the repository root; do not read or change anything outside it.
Paths below are relative to that folder. `res://` = `walker-magic-zhefan/`. No `AGENTS.md`; `README.md` is the reviewer's entry.

## Project context

**Engine.** Godot 4.7.2-stable (official build `ed1daf0bf`): `logs/baseline-before/test_wolf_60fps.log:1`, binary path in
`scripts/run-test.sh:5`. Feature `"4.7"` (`walker-magic-zhefan/project.godot:15`); no physics rate set, so 60 ticks/s.
**Renderer.** Not set in `project.godot` `[rendering]`, so the default, Forward+ (`CHANGE-BRIEF.md:5`). 2D, 640×360
viewport, window 1280×720, stretch `viewport`, integer scale (`project.godot:23–29`).

**Clip 1, mage run cycle** — the cycle. Route: `Sprite2D` + AnimationPlayer frame track (`features/player/player.tscn`).
Sheet `assets/sprites/mage/mage_run_cycle_sheet.png`, 248×69, cell 62×69, `hframes = 4`, order contact, down, passing, up
(CHANGE-BRIEF revision "run cycle replaced after play"). Clip `run`: keys 0, 0.1, 0.2, 0.3 s, length 0.4, 10 fps,
`step` 0.1, `LOOP_LINEAR`, discrete. Nine state clips (`idle, run, rise, fall, cast, hurt, fail, fail_pit, win`) in the
same player. Driven by `features/player/player.gd`: `_update_state()` → `_set_state()`, which calls `play()` and sets
`flip_h`; `TEXTURES` is a read-only table of what each clip shows, read by three earlier tests (`tests/test_player.gd`).

**Clip 2, wolf lunge** — the committing action. Route: cutout rig keyed as resource text in `features/wolf/wolf.tscn`:
`Facing → Rig → RearPivot (−11, −22) / FrontPivot (15, −22)`, parts are `region_rect`s (0, 0, 40, 40) and (36, 0, 44, 40)
of `assets/sprites/wolf/wolf_lunge.png`. Clip `lunge`: 89/60 s, `LOOP_NONE`, `step` 1/60, keys at frames
0, 25, 31, 37, 53, 65, 89; clips `patrol` and `dead` switch which node shows. Driven by `features/wolf/wolf.gd`: GROWL
entry plays `lunge` from 0; a non-lethal GROWL hit enters RECOVER and seeks frame 52, so the hit tick shows 53.
Measured phases 31 / 22 / 36 ticks (`logs/pin/take_lunge.json`); the timer subtracts 1/60 per tick (`wolf.gd:71`).

**Torch flicker** (`effects/cave_lights.tscn`): continuous `energy` and `texture_scale` tracks, 2.4 s, `LOOP_LINEAR`.
Visual only too: `effects/embers.tscn`, `features/wolf/lunge_afterimage.gd`. Both clip players run on the physics
callback with `process_physics_priority = -1`, before their owner's script (`player.tscn`, `wolf.tscn`).
**Scenes.** `res://game/main.tscn` is the main scene (`project.godot:14`): `Level/Wolf`, `Player`, the following camera
(`game/main.gd`), the cave lights and embers; pause and restart in `game/session_input.gd`.

**Tests.** Every test runs through `scripts/run-test.sh <test-file.gd> <fps|realtime> [timeout-seconds]` from this
folder in Git Bash. A number runs headless with `--fixed-fps`; `realtime` passes none; timeout 120 s by default. It fails
on a non-zero exit or any `SHADER ERROR`, `SCRIPT ERROR`, `Failed loading resource`, `Failed to load resource` or
`Parse Error` line (`scripts/run-test.sh`).

```bash
./scripts/run-test.sh test_pin_behaviour.gd 60   # also 30 and 144; PIN_MODE=record re-records
./scripts/run-test.sh test_anim_edges.gd 60      # also 30, 144; same for test_afterimage.gd
./scripts/run-test.sh test_clip_run.gd 60        # same for test_clip_lunge, test_clip_flicker, test_anim_structure
./scripts/run-test.sh test_wolf.gd 60            # and the other 60-only baseline suites below
./scripts/run-test.sh test_hurt_tint.gd 30       # also 60 and 144; same for test_fireball_impact, test_fireball_trail
```

Baseline (`logs/baseline-before/`, `2276069`), 13 suites, 0 failures: a3_assets 22, audio 13, cast 11, flow 14, player 11,
sound_triggers 11, wolf 13, materials 32, fireball configs 54 and 32 at 60; hurt_tint 17, fireball_impact 14,
fireball_trail 20 at 30, 60, 144. Shared clip checks: `tests/anim_checks.gd`.

## Headless facts

Confirmed on this machine (Godot 4.7.2) unless marked.

- Earlier: `get_shader_uniform_list()` needs the main loop; a shader-only uniform rename raises no error (A5 at
  `2b68e0a`); `--fixed-fps` is not in the command-line args; headless runs no GPU particle process (A6).
- A headless run advances clips and reads their structure. It draws nothing, so whether the motion reads is not
  observable here.
- Key times are 32-bit floats; compare them with a tolerance.
- `value_track_get_update_mode` applies only to value tracks.
- Frame strips come from a windowed Movie Maker run, which I start.

## Current change
@CHANGE-BRIEF.md

## Ownership

- Files in `walker-magic-zhefan/shaders/` are hand-written by the human and never edited by an agent: an agent may
  read them and suggest changes, but never creates, edits, moves, deletes or commits them.
- Clips live as resources in the scene that owns them (`features/player/player.tscn`, `features/wolf/wolf.tscn`,
  `effects/cave_lights.tscn`) and are never built in code at runtime. A tool script may bake a `.tres` once.

## One authority

Exactly one node writes to each animated node. Never add a second writer to a node that already has one.
- Mage `Sprite2D` `texture`, `hframes`, `frame`: the player's AnimationPlayer. `player.gd` only calls `play()` and sets
  `flip_h` and `visible` (blink); its `material` uniform `intensity` belongs to the HurtTint driver.
- Wolf `Sprite2D` `texture` and `visible`, `Facing.visible`, `Rig` position and scale, both pivots' rotation: the wolf's
  AnimationPlayer. `wolf.gd` only calls `play()` and `seek()` and sets `Facing.scale.x`; its flash uniform is `_flash()`'s.
- Torch `energy` and `texture_scale`: the CaveLights AnimationPlayer. Lunge ghosts: `lunge_afterimage.gd`, which reads
  the wolf and writes only its own ghost nodes. `tests/test_anim_structure.gd` and `test_clip_flicker.gd` check this.

## Godot 4 names

Use Godot 4.7 names, never Godot 3: `loop_mode` (`Animation.LOOP_NONE / LOOP_LINEAR`), not `loop`; `speed_scale`, not
`playback_speed`; `AnimatedSprite2D.sprite_frames` and `play()`, not `frames` and `playing`; `callback_mode_process`, not
`playback_process_mode`. Set `Animation.step` to one frame period at the brief's rate. If unsure a property exists, check
it headless with `ClassDB.class_get_property_list()` and report misses.

## Input

Tests use `Input.parse_input_event` (`tests/test_pin_behaviour.gd`); `Input.action_press` never reaches `_input`.

## Two clocks

Every clip player uses `ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS`, the tick gameplay reads (`player.gd`
`_physics_process`, the wolf's `_timer` at `wolf.gd:71`, its hitbox in `_enter()`), so the largest disagreement is 0 s.
No gameplay fact is keyed on a track; no method tracks; no AnimationTree; no AnimatedSprite2D. Process-clock code: the
camera (`game/main.gd`), the hurt-tint driver, and the wolf's flash and removal timers (removal at `wolf.gd:170`: tick 79
at 60 fps, 80 at 30 and 144). Compare clip frame n with physics tick n, never with summed frame time.

## Commits
Commit only what the human asks for. Every message says what was checked and who wrote the content, e.g. "(agent,
unedited)" or "(mine, committed by Claude Code at my request)". No `Co-Authored-By` trailer. Never push. Nothing under
`shaders/`. After every session, `git diff --stat walker-magic-zhefan/shaders/` must print nothing.

## Resuming
A session that stopped early may describe work it never did: do not continue it; run `git status` and the tests, then
start a new session stating what is done and what is not.

## Out of scope
Collision, movement, input, damage, every timing in `tuning.gd` and `wolf.gd`, the fireball and both A6 effects, the hurt
tint, the A3 prop room, `project.godot`, the original sprite PNGs and the Gemini raw files (`CHANGE-BRIEF.md`, Boundaries).
The only gameplay change is the growl interrupt, re-pinned after play (`ff71bbb`). Existing tests are not edited, weakened
or deleted. The capture overlays are debug-only and live in the capture harnesses under `tests/`.

## Unconfirmed
- Test headers still name the A5/A6 folders (`tests/test_fireball_impact.gd:5`). The desktop app writes no session
  `.jsonl`, so the result-event check is replaced by reading each session's final report.
