# CHANGE-BRIEF.md — Assignment 7: two animations

The Assignment 6 brief (hit_spark, fire_pit_flames) is at tag `a6`,
`fall-2026/jingyao-y/assignment-6/walker-downfall/CHANGE-BRIEF.md`. This file
replaces it. Written by the agent (Claude Code) on 2026-11-22, before any
animation setup prompt. The user chose where the work lives, the art source
(the game's Sol art) and the rig route (2D cutout rig on a 3D billboard); the
agent chose the two clips and wrote everything below, for the user's review.
Dated revisions go at the end; nothing above them is edited afterwards.

Pinned engine: Godot 4.7.2-stable (official), Forward+, D3D12 on Windows
(`project.godot:16,27`; `scripts/run-test.sh:11`). The repository root is the
Godot project (`--path .`), so the course's `godot/animations/` is
`animations/` here. Physics runs at the default 60 ticks/s (`project.godot`
sets no `physics_ticks_per_second`).

## What exists today (audit, 2026-11-22, at game source 22651e36)

No `AnimationPlayer`, `AnimationTree` or `Animation` resource exists in the
game. Every moving sprite is an `AnimatedSprite3D` whose `SpriteFrames` are
**built in code at run time**:

- Operators: `LapplandAnimator3D extends AnimatedSprite3D`
  (`godot_assets/lappland_animator_3d.gd:1-2`) builds walk, idle and combat
  animations in `_load_character()` (`:181`), `_build_idle_frames()`
  (`:328`) and `_build_combat_frames()` (`:341`). Actions run on the
  animator's own clock: `action_time += delta` in `_process` (`:217`),
  frame = `action_time * 12 * action_rate` (`_action_frame()`, `:381`).
- NPCs: `FieldArt.npc_idle(kind)` (`art/field_art.gd:162-182`) builds a
  4-frame, 3 fps looping `SpriteFrames` and calls `play("default")`. Callers:
  可露希尔 behind the base store counter (`world/base_map.gd:762`) and the
  field set pieces (squad, trader, camp) in
  `world/continuous_world_map.gd:2713-2724`, which also writes a random
  `figure.frame` so they do not breathe in step (`:2716`).

The player has no explicit state enum. Its state lives in fields read by
`Player._physics_process` (`entities/player.gd:478`): `swing_remaining`,
`dash_remaining`, `hitstop_remaining`, `control_timer`, `sword_charge`,
`_attack_cooldown`. A swing is `attack_direction()` (`:838`); when Lappland's
sword charge is full the swing is a **release**: the sword wave is spawned
and the charge cleared on the same physics tick as the click (`:849`,
`:879-899`). A dodge or loss of control calls `interrupt_actions_for()`
(`:698-709`), which zeroes `swing_remaining` and cancels the sprite action.

## The two clips

### Clip 1 — `npc_idle` (the cycle)

- **What it communicates:** "this person is alive and waiting for you." The
  NPCs (可露希尔 at the base store; the squad, the trader 坎诺特 and 可露希尔 at
  camps in the field) are where the player trades or talks. A frozen figure
  reads as scenery; a slow breathing loop reads as someone to walk up to.
- **Object:** every NPC figure (`FieldArt.npc_idle` callers above), a second
  object, not the player.
- **Route: Sprite3D with an AnimationPlayer frame track** — the 3D twin of
  the course's "Sprite2D with an AnimationPlayer frame track". `Sprite3D` has
  the same `hframes`, `vframes` and `frame` properties. Chosen because it is
  the preferred route: the clip is a resource the read-back can see, and
  `FieldArt.npc_idle` stops building `SpriteFrames` in code.
- **Scene:** `res://animations/npc_idle.tscn`: root `NpcIdle` (`Sprite3D`)
  with child `AnimationPlayer`, library `""`, clip `idle`, `autoplay = "idle"`.
  `FieldArt.npc_idle(kind)` instances this scene and sets only `texture` (the
  kind's sheet) and the existing placement properties; it never writes
  `frame`.
- **Authority:** that `AnimationPlayer`, alone. It reads no game state; it
  starts on `autoplay`. The random breathing phase becomes a one-time
  `AnimationPlayer.seek(offset, true)` at placement
  (`continuous_world_map.gd:2716` stops writing `figure.frame`).

### Clip 2 — `wave_release` (the committing action)

- **What it communicates:** "the stored sword wave is being thrown *now*, and
  you are committed to it." Today the release is the same 3-frame sprite
  flourish as a normal swing (`ACTIONS.wave`, 0.25 s), and the wave leaves on
  the click frame, so a release reads like any hit. A wind-up the player can
  read, a sweep on which the wave visibly leaves, and a recovery that holds
  her in place make the big hit read as big, and give the dodge a real choice:
  dodge during the wind-up and the charge is kept.
- **Object:** the player, Lappland only (`has_sword_wave()`, `:775-776`;
  `"signature": "wave"` in `CHARACTERS.lappland`).
- **Route: cutout rig keyed as resource text.** A 2D cutout rig — `Sprite2D`
  parts under `Node2D` pivots — lives in a `SubViewport` whose texture is
  drawn by a `Sprite3D` billboard at the player, at the game's sprite scale.
  The clip's keys are written by the agent in the `.tscn`, so every diff is
  reviewable. Chosen because the user picked a 2D cutout rig, and a
  `SubViewport` lets 2D parts play inside the 3D world exactly where the
  sprite stands.
- **Scene:** `res://animations/lappland_wave_rig.tscn`: root `WaveRig`
  (`Node3D`) → `Billboard` (`Sprite3D`, texture = the viewport's
  `ViewportTexture`) and `Viewport` (`SubViewport`, 96×96, transparent) →
  `Rig` (`Node2D`) → `Body` (`Sprite2D`), `ArmBack` (`Node2D` pivot at the
  rear shoulder) → `BladeBack` (`Sprite2D`), `ArmFront` (`Node2D` pivot at the
  front shoulder) → `BladeFront` (`Sprite2D`). `AnimationPlayer` child of
  `WaveRig`, `root_node` = `../Viewport/Rig`, clips `RESET` and
  `wave_release`.
- **Parts:** cut from Lappland's combat sheet
  (`godot_assets/lappland_combat_64.png`, row `west`, the `wave` pose columns
  10–12, `ACTIONS.wave = [10, 3]`, `lappland_animator_3d.gd:43`) by a committed
  tool script, `tools/a7_cut_rig_parts.py`, into
  `animations/lappland_rig/*.png`. The combat sheet is not edited.
- **Authority:** the rig's `AnimationPlayer` is the only writer to `Body`,
  `ArmBack`, `ArmFront`, `BladeBack`, `BladeFront`. It is driven by the
  player's state machine in `entities/player.gd` (state `wave_state`, below),
  which is the only caller of `play()`, `stop()` and `advance()` on it, and
  the only writer of `Billboard.visible` and `Rig.scale.x` (facing). Those
  two are never keyed. During a release, `LapplandAnimator3D` hides itself
  (`visible = false`, its own property, written by itself through a new
  method `show_rig(on)`), so the operator sprite and the rig are never drawn
  together.

## The sheets

Provenance, as the user stated it (2026-11-22): the art is **fan art of
Arknights characters generated with OpenAI's GPT "sol" image model** ("gpt
sol模型生成的同人图"). The user's position: "正常同人二创，无违规" (ordinary fan
derivative work, no violation). Recorded, not judged here. **Not yet
recorded, to be supplied by the user:** the exact model name and version, the
terms of use and the date checked, and where the prompts are logged. Until
then the credits file (`animations/ATTRIBUTION.md`) says "pending" for each.
The course's own note applies and is repeated in SOURCES.md: Assignment 2's
rule for generated sprites asks for a free or local model and no copyrighted
character; this art does not meet the second part, and the user chose to use
it anyway.

| | Clip 1 `npc_idle` | Clip 2 `wave_release` (rig parts) |
|---|---|---|
| Original as delivered (committed) | `art/portraits/batch_P1_v3/source_paintings/portrait_closure_chibi.png` (可露希尔); `art/field/batch_F1C_v1/source_paintings/squad_field_lineup.png` (squad, trader) | Lappland's combat sheet as delivered in Sol's batch (path recorded by the Step 4 session from `godot_assets/`'s provenance; pending) |
| Sheet as used | `art/characters/npc/npc_*_idle.png`, written by code (`art/characters/npc/prepare_npc.py:195-249`), committed with the code | `godot_assets/lappland_combat_64.png` |
| Cell size | 64×64 px | 64×64 px |
| Grid | `hframes = 4`, `vframes = 1` (256×64) | 16 columns × 5 rows (`COMBAT_ROWS`) |
| Frame order | left to right, 0 1 2 3 = one breath (`prepare_npc.py:22-24`) | row 2 = `west`; columns 10, 11, 12 = the wave pose; parts cut from column 10 (wind-up) |
| Registration | feet 2 px above the cell bottom, centred (`field_art.gd:158`) | parts placed by pivot, checked in the strip |

## The cycle spec — `npc_idle`

- **Frame rate:** 12 fps design rate; `Animation.step = 1/12 s` (0.0833).
  Not the default 1/30.
- **Frames:** 4 sheet cells, each held 4 design frames: keys at frames
  **0, 4, 8, 12** (t = 0, 0.3333, 0.6667, 1.0 s) with values **0, 1, 2, 3**.
  `length = 16/12 = 1.3333 s`. This is today's look exactly (4 frames at
  3 fps, `field_art.gd:166-167`).
- **Loop mode:** `Animation.LOOP_LINEAR`.
- **Track:** one value track, path `.:frame` (relative to `root_node` =
  `..`, the `NpcIdle` Sprite3D), `Animation.UPDATE_DISCRETE`,
  interpolation `INTERPOLATION_NEAREST`.
- **Seam rule (frame track):** no duplicate across the wrap — the last key
  (value 3) differs from the first (value 0) — and the gap from the last key
  (1.0 s) to `length` (1.3333 s) equals the key interval (0.3333 s). Every key
  value is < `hframes * vframes` = 4.
- **Clock:** `callback_mode_process = ANIMATION_CALLBACK_MODE_PROCESS_IDLE`
  (process tick). No gameplay reads it.

## The phase table — `wave_release`

Frame rate **30 fps**; `Animation.step = 1/30 s` (0.0333, which is also the
default — set explicitly anyway, and asserted). Frame 0 is the physics tick
of the release click. One design frame = 2 physics ticks.

| Phase | Frames | Begins on | What the player may do | What the game reads |
|---|---|---|---|---|
| Startup | 6 (0–5, 0.000–0.200 s) | frame 0 | Dodge: cancels the release, **no wave, charge kept**. Loss of control (stun etc.): same. No move, no new swing. | `wave_state == STARTUP`; nothing spawned; `sword_charge` unchanged |
| Active | 4 (6–9, 0.200–0.333 s) | frame 6 | Dodge: cuts the rest; the wave is already out. No move, no new swing. | On frame 6, once: the wave(s) spawn, the charge clears, the `burst` VFX and wave relic/trigger effects fire. `wave_state == ACTIVE` |
| Recovery | 10 (10–19, 0.333–0.667 s) | frame 10 | Dodge: cuts recovery. No move. A new swing still waits on the existing attack cooldown (`current_cooldown()`, unchanged). | `wave_state == RECOVERY`; `swing_remaining > 0` |
| (end) | — | frame 20 (0.667 s) | everything | `wave_state == READY`; rig hidden, sprite shown |

Damage, crit and multipliers are computed on the click frame as today
(`:856-866`) and stored; only the spawn moves to frame 6. Attack speed does
not scale this clip (today the release flourish scales with
`animation_rate()`, `:879`); the phase table is the design and stays in frames.
The source of these numbers: today's release is 3 frames at 12 fps = 7.5
frames at 30; the measured reference is that 0.25 s flourish plus the user's
existing rule that a dodge interrupts everything (`:498-503`). The agent's
starting split 6/4/10 is a design proposal for the user to judge in play.

**Keys (Step 4 builds them from this table).** A key at every phase boundary
on every rig track: t = 0 (f0), 0.2 (f6), 0.3333 (f10), 0.6667 (f20).
`ArmFront:rotation` and `ArmBack:rotation` wind back through startup with an
ease-in transition (accelerating into frame 6), sweep forward across active,
and settle with an ease-out through recovery; `Body:position` leans back in
startup, lunges forward on frame 6, returns in recovery. `RESET` holds the
rest pose. Exact angles are Step 4's, listed beside their frames.
`loop_mode = Animation.LOOP_NONE`.

## The state machine

The player's wave state machine, a new field `wave_state` in
`entities/player.gd` with a frame counter `wave_frame` advanced in
`Player._physics_process` (every physics tick that is not frozen by hitstop
or a closed simulation, i.e. after the existing early returns, `:479-480`,
`:494`, `:505-507`). No `AnimationTree`.

| State | Clip played on the rig | Enters when | Leaves when |
|---|---|---|---|
| `READY` | `RESET` (rig hidden) | start; any exit below | a release swing → `STARTUP` |
| `STARTUP` | `wave_release` from t = 0 | `attack_direction()` with `release == true` and Lappland's own swing path (`:879`) | `wave_frame == 6` → `ACTIVE`; interrupt → `READY` |
| `ACTIVE` | `wave_release` (continues) | frame 6 (spawns the wave) | `wave_frame == 10` → `RECOVERY`; interrupt → `READY` |
| `RECOVERY` | `wave_release` (continues) | frame 10 | `wave_frame == 20` → `READY`; interrupt → `READY` |

"Interrupt" = `interrupt_actions_for()` (dodge or loss of control), operator
swap (`set_operator`), death, or leaving the floor. On `READY` the state
machine calls `play("RESET")`, hides `Billboard`, and calls
`_sprite.show_rig(false)`.

## The two clocks

| Clip | Node | `callback_mode_process` | Advances on |
|---|---|---|---|
| `npc_idle` | `NpcIdle/AnimationPlayer` | `ANIMATION_CALLBACK_MODE_PROCESS_IDLE` | process tick |
| `wave_release` | `WaveRig/AnimationPlayer` | `ANIMATION_CALLBACK_MODE_PROCESS_MANUAL` | the player's physics tick: `Player._physics_process` calls `advance(delta)` on the same tick that it increments `wave_frame` |
| (operator sprite) | `LapplandAnimator3D` (`AnimatedSprite3D`) | no such setting | process tick (unchanged) |

Gameplay reads one keyed fact: **the active window opens on frame 6** (the
wave spawns). It is read on the **physics tick**, from `wave_frame`, never
from the clip. The clip is advanced by the same function on the same tick, so
the largest disagreement is **0 s** by construction; hitstop and a paused
simulation stop both together. (For comparison: on
`ANIMATION_CALLBACK_MODE_PROCESS_IDLE` the clip would run on the process tick
and keep running through hitstop; at 60 Hz physics and a 144 Hz display the
disagreement would be up to one physics tick, 16.7 ms, plus the whole
hitstop.) No method track is used: method tracks are deferred.

## Boundaries

Unchanged: collision, movement, input, enemies, the existing timings of
every non-release swing, the dodge, hitstop, control and cooldowns, the
operator walk/idle/combat sprites for every action except Lappland's release,
existing test expectations, the A5 shaders in `shaders/`, the A6 effects
(`effects/hit_spark.*`, `effects/fire_pit_flames.tscn`), the NPCs' placement,
scale, billboard and look, every other object, and the sheets as delivered.

**Changes this brief names** (each predicted in the pins):

1. Lappland's release: the wave spawns 12 physics ticks (0.2 s) after the
   click, not on it; the charge clears at the spawn, not at the click; a
   dodge or loss of control during startup spawns no wave and keeps the
   charge; `swing_remaining` for a release is 0.667 s (was 0.25 s at rate 1);
   during the release the operator sprite is hidden and the rig is drawn.
2. NPC idles are `Sprite3D` + `AnimationPlayer` from a scene instead of
   `AnimatedSprite3D` built in code; same cells, same 1.333 s breath.

Presentation code may read game state; it never writes it. The wave state
machine is gameplay (it decides when the wave spawns); the rig and the NPC
clips are presentation.

## The evidence split

| Rule | Checked by |
|---|---|
| Every track of both clips resolves to a real node and property | read-back (`tests/test_npc_idle_readback.gd`, `tests/test_wave_rig_readback.gd`, `track_problems`) |
| `npc_idle`: keys 0/4/8/12 → 0/1/2/3, length 16/12, step 1/12, `LOOP_LINEAR`, discrete, every key < 4, seam gap = interval | read-back |
| `wave_release`: keys at f0/6/10/20 on every track, step 1/30, `LOOP_NONE` | read-back |
| `npc_idle` has no second writer (nothing writes `frame`) | structure test (scene + grep of callers) and the one-authority rule in CLAUDE.md |
| State table: every clip the code requests exists; each state plays its clip; transitions at f6/10/20 | structure test `tests/test_wave_state_machine.gd` against the rig's AnimationPlayer resource |
| States in order under real input (`Input.parse_input_event`) | state test (same file), 60 fps |
| Interrupt one frame before, on, and after each boundary (f5/6/7, f9/10/11, f19/20/21) | edge tests `tests/test_wave_edges.gd`, 60 fps |
| Existing behaviour unchanged except changes 1–2 | pins `tests/test_a7_pins.gd`, before and after |
| Motion reads; phases read as distinct | frame strip (fixture) + the user in play |
| Cycle wraps without a seam; no drift in cells | the user, 5+ wraps at normal speed; cycle strip |
| Against the background | the user, darkest and lightest ground the clips appear on |

## The frame strip — `wave_release`

Preview `res://previews/wave_release_preview.tscn`: a real Chernobog floor
loaded with a fixed seed and `game.seed_rng(seed)` (TUNING.md A6 lesson),
camera at the game's default size and pitch, Lappland with a full charge, an
enemy stand-in in range. The release is triggered at **frame 10** of the
capture (`--fixed-fps 30`, `--quit-after 45`). A design frame = a capture
frame.

| Capture frame | Design frame | Should show |
|---|---|---|
| 10 | 0 (trigger) | sprite gone, rig in rest pose, blades starting back |
| 15 | 5 (last startup) | blades fully drawn back, body leaning back; no wave |
| 16 | 6 (active opens) | blades sweeping forward, body lunging; the wave leaves this frame |
| 19 | 9 (last active) | sweep nearly done; wave ~0.3 units out |
| 20 | 10 (recovery opens) | blades past the front, starting to settle |
| 29 | 19 (last recovery) | nearly at rest |
| 30 | 20 (end) | rig hidden, operator sprite back, same foot position |

Cycle strip: `res://previews/npc_idle_preview.tscn`, 可露希尔 at the base
store, captured at `--fixed-fps 30 --quit-after 90`. A cell lasts 1/3 s =
10 capture frames, a breath 40. Read frames 0, 10, 20, 30 (cells 0–3), 40
(the wrap, cell 0 again) and 80 (second wrap) — for registration and the seam.

## Predicted failures

| # | Failure | Check that catches it |
|---|---|---|
| P1 | Godot 3 names: `loop = true` on the Animation (clip does not loop), `playback_speed`, an `AnimatedSprite` class | read-back asserts `loop_mode`; scene load + grep |
| P2 | Frame track left on `UPDATE_CONTINUOUS` (sweeps 0→3 between keys) | read-back asserts `UPDATE_DISCRETE` |
| P3 | `step` left at 1/30 for the 12 fps NPC clip; keys snap to 1/30 multiples | read-back `step` and key times with tolerance 0.5/12 s |
| P4 | Track path names a node or property that does not exist (`Arm_Front:rotation`, `.:frames`) — silently inert | `track_problems` |
| P5 | NPC caller still writes `figure.frame`: two writers, the random start is overwritten or fights the clip | structure test; the user sees NPCs breathing in step / skipping |
| P6 | Rig clip on the process tick drifts from `wave_frame` (wave leaves before the sweep, or during hitstop) | brief clock rule; edge test asserts the clip's `current_animation_position` equals `wave_frame / 30` at the spawn tick |
| P7 | Duplicate frame at the NPC wrap (a key at length with value 0) — a stutter each breath | read-back seam assertion; the user's 5-wrap check |
| P8 | Rig `SubViewport` not transparent or not updating (`UPDATE_DISABLED`): a black or frozen square | strip; the user in play |
| P9 | Operator sprite and rig drawn together (sprite not hidden) | strip frame 10–29; state test asserts `_sprite.visible == false` in each wave state |
| P10 | Dodge in startup still clears the charge (spawn logic left on the click) | edge test f5 |

## Answers

1. **Routes.** `npc_idle`: Sprite3D + AnimationPlayer frame track.
   `wave_release`: cutout rig keyed as resource text. Both are AnimationPlayer
   clips, so one read-back (`track_problems` plus key/step/loop checks) sees
   both. The read-back of the AnimatedSprite route would only see a
   `SpriteFrames` resource — frame counts, speed, loop — and nothing about
   which node it drives; ours sees the track paths and can prove each resolves.
2. **Continuous frame track.** Between keys 0 and 1 the integer `frame` would
   be interpolated and rounded, so between two keys four cells apart it would
   step through every cell in between; here keys are adjacent cells, so it
   would change cell half-way between keys (at frame 2, 6, 10 instead of 4, 8,
   12) and blend 3→0 across the wrap through 2 and 1 — a visible rewind each
   breath.
3. **step.** `npc_idle`: `1/12`; `wave_release`: `1/30`. Left at the default
   1/30 for the 12 fps clip, the editor snaps keys to multiples of 1/30: frame
   4 at 0.3333 s would snap to 0.3333 (10/30) by luck, but a revised table at
   an odd frame (e.g. 5/12 = 0.4167) would snap to 0.4 and the key-time
   assertion (tolerance 0.0417) still passes it — so the `step` assertion is
   what pins it.
4. **One authority.** NPC sprite: its `AnimationPlayer` (others that could
   write it: `continuous_world_map.gd:2716`'s `figure.frame`, which this change
   removes; `GmCamera._keep_sprites_upright` writes only `scale`, not keyed).
   Rig parts: the rig's `AnimationPlayer`, driven by the player's
   `wave_state`; nothing else references the parts. Operator sprite:
   `LapplandAnimator3D` itself; `player.gd` only calls its methods
   (`play_attack`, `start_dash`, `cancel_action`, new `show_rig`).
5. **Ticks.** `npc_idle`: process tick, no gameplay read. `wave_release`:
   manual, advanced from `Player._physics_process`, the same tick gameplay
   reads frame 6 on; largest disagreement 0 s (measured by the edge test).
6. **Seam.** Frame track: no duplicate value across the wrap, gap last key →
   length = key interval (0.3333 s). A duplicated frame at the wrap would hold
   cell 0 for two intervals (0.667 s) once per breath — a hitch at the bottom
   of each breath.
7. **Imported rig:** not applicable; the rig is a keyed 2D cutout. Mutation 4
   (empty import cache) is still run: the rig's part PNGs and the NPC sheets
   reimport, and both read-backs must still pass.

## Revisions

- **2026-11-22 r1 (agent, from the Step 1 review; user: "Accept both").**
  (a) One authority over the operator sprite's `visible`: `Player` already
  writes `_sprite.visible` for Amiya's shadow (`entities/player.gd:1867,1963`),
  so `Player` stays its only writer. The wave state machine (in `Player`)
  hides the sprite on entering `STARTUP` and shows it again on `READY`; the
  method `LapplandAnimator3D.show_rig()` named above is dropped, and the
  animator never writes its own `visible`. (b) Existing expectations that
  change 1 changes, predicted here and updated only in the re-pin step, each
  in its own commit with this reason: `tests/test_lappland.gd:100` (wave out
  and charge 0 on the release call; `action_name == "wave"`),
  `tests/test_lappland.gd:147` (air-swing release: wave out and charge 0 on
  the call) and `tests/test_lappland_input.gd:78` (held mouse sees the
  `"wave"` pose). After the change the wave exists 12 physics ticks after the
  release and the sprite plays no `"wave"` action (the rig does). Every other
  existing expectation stays unchanged.
- **2026-11-22 r2 (agent, from the Step 4 review; user: "Commit Step 4").**
  (a) The combat sheet's grid is **14 columns × 5 rows** (896×320 px,
  measured), not "16 columns × 5 rows" as "The sheets" table says; the brief's
  error, found by the Step 4 session. Row 2 = `west`, column 10 exists, and it
  is the cell the parts were cut from. (b) Original as delivered for the rig
  parts: `godot_assets/lappland_combat_source.png` (the image-generation
  source), turned into `lappland_combat_64.png` by
  `godot_assets/prepare_combat_atlas.py`; both are now committed. This closes
  the "pending" path in "The sheets"; model name, version and terms are still
  pending from the user. (c) With keys only at the phase boundaries, the
  body's lean back peaks on the f6 key and the lunge runs f6→f10 with an
  ease-out; the brief's "leans back in startup, lunges forward on frame 6"
  reads that way from here on. (d) Two tracks beyond the brief's list:
  `ArmBack:position` and `ArmFront:position` carry the body's lean/lunge
  offsets, because the arm pivots are siblings of `Body`, not children, and
  the blades would otherwise leave the hands. Keys at the same four frames.
- **2026-11-22 r3 (agent, from the Step 5 plan; user: "Accept all five").**
  (1) Existing expectations change 1 also alters, beyond r1's list: pin
  `tests/test_a7_pins.gd` S1 (the sprite plays no `"wave"` action; it should
  have been marked BRIEF-CHANGES at Step 2 and was not, the agent's miss);
  `tests/test_lappland.gd:60-154`, `tests/test_builds.gd:116,269,586,608` and
  `tests/test_growth.gd:68,377,422`, which switch the player's physics off and
  expect the wave on the release call. In the re-pin step these suites change
  only **how they reach the wave** (advance the player until `wave_state`
  leaves `STARTUP`), never their expected values; each in its own commit with
  this reason. `tests/test_hit_spark_state.gd` P0b is at risk (the wave leaves
  later in its hold) and is re-run, not edited unless it fails for that reason.
  (2) New transition: a swing during `RECOVERY` → `READY` (recovery cancelled,
  the swing proceeds); swings stay refused in `STARTUP` and `ACTIVE`.
  (3) "12 physics ticks after the click" means 12 ticks **not frozen by
  hitstop**: `wave_frame` stops while `hitstop_remaining > 0`, as the clock
  rule says, so a landed release spawns 12 + (frozen ticks) after the click;
  the re-pin records the measured number. (4) Bonuses: damage, crit and
  `attack_multiplier()` (incl. 赏善郎) are still taken on the click (that
  swing's melee hit lands then); the gear signature bonus
  (`gear_fx.spend_signature_bonus()`) is spent at frame 6 with the wave, so a
  dodge in `STARTUP` keeps it, like the charge. (5) Leaving the floor or the
  simulation stopping mid-release → `READY`, no wave. The rig `Billboard`
  joins `upright_sprites`, so `GmCamera._keep_sprites_upright` becomes the
  writer of `Billboard.offset.y` (never keyed, not written by `Player`).
