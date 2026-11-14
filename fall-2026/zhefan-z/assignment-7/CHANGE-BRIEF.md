# CHANGE-BRIEF — Assignment 7: a mage run cycle and a wolf lunge rig

Author: Zhefan Zhang (zhefan-z). Original version, 2026-11-10. Dated revisions go at the end. The A6 brief is in history at `7672d5a`. My decisions here: both clips, the run rate, the lunge's amplitude and the per-phase interrupt rule; claude.ai compiled the file from those decisions and the code facts. Paths are relative to `walker-magic-zhefan/` (`res://`).

Engine: Godot 4.7.2-stable, Forward+, 2D, viewport 640×360 at 2× (1280×720). Physics 60 ticks/s (engine default; `project.godot` sets none).

## Objectives

Four ideas this change shows, each with a test: **tracks of keys** (every clip is read back key by key), **one authority** (one AnimationPlayer per sprite; the state machine only calls `play()`), **two clocks** (animation on the physics tick, the same tick gameplay reads), **feel designed in frames** (the lunge is a phase table before it is keys).

## Facts from the code

| Fact | Reference |
|---|---|
| Player states `IDLE, RUN, RISE, FALL, CAST, HURT, FAIL, WIN`, one static image each; `_set_state()` sets `sprite.texture` and `flip_h`; a fall into the pit shows the FALL image in FAIL | `features/player/player.gd:15–25, 130–133, 177–178` |
| RUN shows only `mage_run_contact.png`; `mage_run_passing.png` (A2 key pose) is unused | `player.gd:19`, A2 CHARACTER-SHEET revision |
| Player state is chosen in `_physics_process` → `_update_state()` | `player.gd:58, 116–127` |
| Wolf states `PATROL, GROWL, LUNGE, RECOVER, DEAD`; `_timer` counts down per physics tick; GROWL 0.5 s standing, LUNGE 0.35 s at 220 px/s with `LungeHitbox.monitoring` on, RECOVER 0.6 s standing | `features/wolf/wolf.gd:11–28, 58–96` |
| Wolf images 80×40, Sprite2D `offset (-40, -38)`, not centred; the art faces right; facing is `sprite.flip_h`; `_flash()` sets a `flash` uniform on the sprite's own material | `wolf.gd:120–126, 150–155`, `wolf.tscn:21–25` |
| `take_damage()` flashes and lowers HP; it never changes the wolf's state unless HP reaches 0 | `wolf.gd:130–147` |
| Mage images 62×69, Sprite2D `offset (-31, -67)`, not centred | `player.tscn:21–25` |

## Clip 1 — mage run cycle (sprite, loops, player state machine)

- **Route:** Sprite2D with an AnimationPlayer frame track.
- **Source:** my own Assignment 2 sprites, `assets/sprites/mage/mage_run_contact.png` and `mage_run_passing.png` (provenance in `walker-magic-zhefan/SOURCES.md`, Assignment 2). The originals stay committed and unchanged.
- **Sheet and slicing:** `assets/sprites/mage/mage_run_sheet.png`, 124×69, written by a committed tool script from the two originals side by side. Cell 62×69, grid `hframes = 2`, `vframes = 1`, frame order `0 = contact, 1 = passing`. Claude slices from these numbers, not from the image.
- **Cycle spec:** 8 fps; keys `frame 0` at 0.000 s and `frame 1` at 0.125 s; length 0.250 s; `LOOP_LINEAR`; update mode **discrete**. Seam rule (frame track): no duplicate across the wrap, and the gap from the last key to the length (0.125 s) equals the key interval.
- **Registration:** both cells share the A2 canvas and the feet anchor at `offset (-31, -67)`; the frame strip shows any drift.
- **One authority:** the player's AnimationPlayer owns `texture`, `hframes` and `frame` of `Sprite2D` for every state. Each state has a clip (`idle, run, rise, fall, cast, hurt, fail, fail_pit, win`; single-key clips except `run`); `_set_state()` only calls `play()` and keeps setting `flip_h`. `autoplay` is empty.
- **Clock:** `callback_mode_process = ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS`, the tick `_update_state()` runs on. Every RUN entry starts the cycle at frame 0.

## Clip 2 — wolf lunge (cutout rig, committing action, wolf state machine)

- **Route:** cutout rig keyed as resource text in the wolf scene (or baked by a headless script to a committed `.tres`).
- **Source:** my own Assignment 2 sprite `assets/sprites/wolf/wolf_lunge.png`, unchanged. The parts use `region_rect` on that texture: **Rear** (hindquarters, tail) and **Front** (shoulders, head), overlapping by a few pixels so no seam opens when they rotate. No new image file.
- **Rig:** `Facing` (Node2D; code sets only `scale.x = facing`) → `Rig` (Node2D at the feet; keyed `position`, `scale`) → `RearPivot` at the hip and `FrontPivot` at the shoulder (Node2D; keyed `rotation`) → the two part Sprite2Ds. The existing `Sprite2D` stays for PATROL and DEAD (run and down images). The white flash reaches every visible part (shared material on `Facing`, parts using the parent material). The agent measures the hip and shoulder from the image and lists them.
- **Amplitude (my choice: clear):** in the growl the body crouches low and pulls back; in the lunge it stretches out far; in the recovery it settles back.

**Phase table** (frames at 60 fps; the wolf's timers are physics ticks):

| Phase | State | Frames | Key at | Rig pose at the key | Transition into it |
|---|---|---|---|---|---|
| start | GROWL entered | 0 | 0 | neutral | — |
| startup | GROWL | 0–30 | 24 | crouch: `Rig.scale (1.08, 0.86)`, `Rig.position.x −4`, `FrontPivot.rotation +10°` (head down) | ease in |
| startup end | GROWL → LUNGE | 30 | 30 | crouch held | — |
| active | LUNGE | 30–51 | 36 | stretch: `Rig.scale (1.22, 0.84)`, `Rig.position.x +3`, `FrontPivot −12°`, `RearPivot +8°` | fast, accelerating |
| active end | LUNGE → RECOVER | 51 | 51 | stretch held | — |
| recovery | RECOVER | 51–87 | 63 | overshoot: `Rig.scale (0.94, 1.06)`, pivots 0° | ease out |
| end | RECOVER → PATROL | 87 | 87 | neutral | settle |

- One clip, `lunge`, length 87/60 = 1.45 s, `LOOP_NONE`, keys at the frames above divided by 60. Claude lists each key time beside its source frame.
- GROWL entry plays `lunge` from 0. The hitbox stays in code (`wolf.gd` LUNGE), not on a track; no method tracks.
- **Clock:** `callback_mode_process = PHYSICS`, the tick the wolf's timers and hitbox run on, so the clip's frame n is the wolf's tick n.
- The pin test measures the real tick count of each phase; if the timers give 31 or 37 ticks instead of 30 or 36, the table is revised to the measured counts before any key is written.

## Behaviour change — per-phase interrupts (my decision)

| Phase | A fireball hit, today | After this change |
|---|---|---|
| startup (GROWL) | flash, HP −1, the lunge still comes | flash, HP −1, **the lunge is cancelled**: the wolf goes straight to RECOVER, and the clip jumps to the recovery section (frame 51) |
| active (LUNGE) | flash, HP −1, the lunge continues | unchanged: a committed lunge can't be stopped |
| recovery, patrol | flash, HP −1 | unchanged |
| any phase, last HP | DEAD | unchanged: death wins over every phase |

This is the only gameplay change. It is made after the pin and re-pinned only after I play it.

## Pin first

Before any change, a pin test records today's behaviour from real input (`Input.parse_input_event`, never `action_press`) through the real game loop, at 30, 60 and 144 fps: per physics tick, the player's state, position and velocity, and the wolf's state, position, HP and hitbox `monitoring`, for scripted runs (walk and stop, jump, cast, take a lunge, hit the wolf during each phase). The trace is committed as the pin. Wiring the clips must leave it identical; the interrupt change must change it only in the growl-hit scenario, and that is re-pinned in its own commit after play.

## Tests

| Test | What it proves |
|---|---|
| Pin (`tests/test_pin_behaviour.gd`) | behaviour unchanged by the clips; changed only as the interrupt rule says |
| Read-back, run (`tests/test_clip_run.gd`) | every track resolves; frame keys 0 and 1 at 0 and 0.125 s; length 0.25; `LOOP_LINEAR`; discrete; every frame key < `hframes × vframes` |
| Read-back, lunge (`tests/test_clip_lunge.gd`) | every track resolves to a real node and property; key times equal the table's frames / 60; length 1.45; `LOOP_NONE` |
| State-machine structure (`tests/test_anim_structure.gd`) | every player state has its clip and `play()` uses it; `autoplay` empty; both AnimationPlayers on the physics callback; no code writes `texture`, `hframes`, `frame` or a rig transform the clips own |
| Edges (`tests/test_anim_edges.gd`) | hits on the first and last GROWL tick (cancel), the first LUNGE tick (no cancel), the last LUNGE tick, the first RECOVER tick; a killing hit in each phase; Esc mid-lunge freezes the clip and the wolf on the same tick and resumes aligned; RUN → jump → land restarts the cycle at frame 0; the same at 30, 60 and 144 fps |
| Earlier suites | the 13 suites in `logs/baseline-before/` unchanged |

## Boundaries

Unchanged: collision, movement, input, damage, every timing in `tuning.gd` and `wolf.gd`, the fireball and both A6 effects, the hurt tint shader and its driver, the A3 prop room, existing tests and their expectations, `shaders/`, `project.godot`, the original sprite PNGs.

## Watching and evidence

Strips come from windowed Movie Maker runs of the pin scenarios with `--debug-collisions`, so frame N of a strip is log line N (fixture captures). A debug-only overlay in the capture harness shows the wolf's phase and tick over its head; the game itself has no overlay. Claude's reading of a strip is a claim; my verdict comes from play at 1280×720 and at `--time-scale 0.25`. Mutations run in a `git worktree`: `loop = true` instead of `loop_mode` (Godot 3), a continuous frame track, a frame key of 2, a track path to a missing node.

## Predicted failures

| # | Failure | What it would look like | Check |
|---|---|---|---|
| F1 | Godot 3 `loop = true` | the run plays once and stops | read-back `loop_mode`; mutation |
| F2 | frame track left continuous | the run flickers or holds the wrong cell between keys | read-back update mode; mutation |
| F3 | sheet sliced 1×2 or a frame key past the last cell | wrong cell, no error | frame-range check; mutation |
| F4 | two authorities: code still sets `sprite.texture` | a state's image flips back for one tick | structure test; pin trace |
| F5 | facing flip and a keyed `scale` on the same node | the wolf faces the wrong way mid-lunge | `Facing` and `Rig` are separate nodes; strip of a leftward lunge |
| F6 | part seam opens when Front rotates | a gap in the wolf's back at the stretch | strip frame 36; my eyes |
| F7 | clip on the idle tick while timers run on physics | key and state drift apart at 144 fps | callback mode in the structure test; 144 fps edges |
| F8 | the growl interrupt leaves the hitbox armed | a cancelled wolf still hurts | edges test reads `monitoring` |

## Revisions

### 2026-11-10 — phase table from the measured ticks; a second clock found

The pin (`a9b4bc1`, `logs/pin/`) measured the wolf's phases at **31, 22 and 36 ticks**, not 30, 21 and 36. Cause, confirmed by the agent with the same double arithmetic: `wolf.gd:59` subtracts 1/60 per tick and switches only at exactly 0; after 30 steps from 0.5 (and 21 from 0.35) the timer is still about 1e-16 above zero, so GROWL and LUNGE end one tick late; 0.6 lands just below zero and is clamped, so RECOVER is on time. The hitbox is on for 23 ticks (31–53), because switching it off is deferred one tick. By this brief's own rule the table follows the measurement before any key is written. The phase table is now:

| Phase | State | Frames | Key at | Rig pose at the key |
|---|---|---|---|---|
| start | GROWL entered | 0 | 0 | neutral |
| startup | GROWL | 0–31 | 25 | crouch (values unchanged) |
| startup end | GROWL → LUNGE | 31 | 31 | crouch held |
| active | LUNGE | 31–53 | 37 | stretch (values unchanged) |
| active end | LUNGE → RECOVER | 53 | 53 | stretch held |
| recovery | RECOVER | 53–89 | 65 | overshoot (values unchanged) |
| end | RECOVER → PATROL | 89 | 89 | neutral |

Clip length 89/60 s (1.4833 s); key times are frames / 60, compared to 1e-6. A growl interrupt jumps the clip to frame 53. Transitions as before.

**A second clock in today's game.** After the killing hit, `wolf.gd:150` removes the wolf with a `create_timer` that runs on the process (frame) clock, not the physics tick: the removal lands on physics tick 79 at 60 fps and tick 80 at 30 and 144 fps. Gameplay never reads it after death, so it stays as it is; the pin stops before it and the test prints it, unpinned. Both AnimationPlayers stay on the physics callback.

### 2026-11-12 — run cycle replaced after play; growl window recorded

After r1 was reverted in play (`TUNING.md`), clip 1 now uses a 4-frame sheet: `assets/sprites/mage/mage_run_cycle_sheet.png`, 248×69, cell 62×69, `hframes = 4`, frame order contact, down, passing, up; drawn by Gemini (app, model shown as 4 Hydrogen) from my prompt v3 with my contact A as the only reference, cleaned by `tools/clean_run_cycle.py` onto my A2 palette. Provenance under Assignment 2's rules: the raw JPEG, both references and the prompt are committed (`design/a7/`, `design/IMAGE-PROMPTS-from-chat.md`). Cycle spec: keys at 0, 0.1, 0.2, 0.3 s, length 0.4 s, 10 fps (6 ticks per frame at 60 Hz), `LOOP_LINEAR`, discrete; seam: no duplicate across the wrap, last-key-to-length gap 0.1 s equals the key interval. My two A2 run frames stay committed and unchanged.

The growl-cancel timings are unchanged by my decision: the reachable window from sight distance is the first 12 of 31 growl ticks (0.2 s), measured with real clicks (`tests/probe_growl_cancel.gd`).

### 2026-11-12 — two clip-alignment fixes from the edges test; F1 does not occur

Found by the edges test (`272fb39`), visual only, pin still 8/8 at 30, 60, 144:

- **A growl cancel showed clip frame 54 on the hit tick, not 53.** The hit is handled before the wolf's physics step and the clip then advances once in that tick. The cancel now seeks to frame 52, so the hit tick shows 53, as a normal RECOVER entry does.
- **A growl right after a one-tick PATROL started at clip frame 1.** Both AnimationPlayers now run before their owner's script (`process_physics_priority = -1` in the scene files), so a newly started clip is never advanced on its first tick. With the setting removed, the edges check fails (frame 1 on tick 170).
- **Failure F1 does not occur on Godot 4.7.2:** a clip written with the Godot 3 `loop = true` loads with `loop_mode = 1` (linear) and still loops (mutation a7-1). The read-back still checks `loop_mode`.

### 2026-11-12 — correction to the revision above

The second alignment bug (a growl after a one-tick PATROL starting at clip frame 1) was found in the windowed lunge capture's tick log, not by the edges test; the edges test was then extended to cover it and verified by removing the fix. Line references in this commit: the timer is `wolf.gd:71`, the removal timer `wolf.gd:170` (they were lines 59 and 150 before A7).

### 2026-11-13 — the brief in the published structure

This revision restates the contract in the structure the assignment asks for. Where it repeats earlier revisions, the earlier text and its dates stand; nothing above is edited.

**The two clips.**

| | Clip 1: run cycle | Clip 2: wolf lunge |
|---|---|---|
| Communicates | the mage is moving under the player's control; speed and direction | the wolf is about to strike (crouch), is striking (stretch, afterimage), and is open (settle) |
| Why the player needs it | to read her own motion in a game with no other movement feedback | to read when to dodge and when the wolf is punishable |
| Object | the mage's `Sprite2D` (`features/player/player.tscn`) | the wolf's rig `Facing → Rig → pivots → parts` (`features/wolf/wolf.tscn`) |
| Route, and why | Sprite2D + AnimationPlayer frame track: one AnimationPlayer and the player's state machine drive every mage image, and the AnimationPlayer read-back sees it | cutout rig keyed as resource text: the phase table becomes exact key times and every key is a reviewable diff |
| Authority, and what it reads | the player's AnimationPlayer; `player.gd` `_set_state()` calls `play()` from the state chosen in `_update_state()` | the wolf's AnimationPlayer; `wolf.gd` `_enter()` plays on GROWL entry and `take_damage()` seeks on a growl cancel |
| Cycle or committing | cycle | committing action |

**The sheet.** Clip 1: `assets/sprites/mage/mage_run_cycle_sheet.png`, generated with the Gemini app (model shown as "4 Hydrogen") on 2026-11-12 from prompt v3 (`design/IMAGE-PROMPTS-from-chat.md`) with my A2 contact sprite as the only reference; output under Google's Terms of Service and Generative AI Additional Terms; checked 2026-11-13. Original as downloaded: `design/a7/mage_run_cycle_gemini_raw.jpg`. Cell 62×69, grid 4 × 1 (`hframes = 4`, `vframes = 1`), frame order 0 contact, 1 down, 2 passing, 3 up. Credits: `assets/sprites/mage/ATTRIBUTION.md`. Clip 2 uses my A2 `assets/sprites/wolf/wolf_lunge.png` (80×40), unchanged, as two `region_rect`s.

**The cycle spec (clip 1).** 4 frames at 10 fps; `Animation.LOOP_LINEAR`; `Animation.step` 0.1. Seam rule for a frame track: no duplicate across the wrap, and the gap from the last key (0.3 s) to the length (0.4 s) equals the key interval (0.1 s).

**The phase table (clip 2).** At 60 fps, the wolf's physics tick; `Animation.step` = 1/60 s.

| Phase | Frames (begins on) | What the player may do | What the game reads |
|---|---|---|---|
| Startup (GROWL) | 0–30 (0) | move, jump, cast; a non-lethal hit cancels the lunge (RECOVER, clip to frame 53) | hitbox off |
| Active (LUNGE) | 31–52 (31) | dodge or jump over; a hit lands but does not cancel | hitbox `monitoring` on (31–53; read on 32–53) |
| Recovery (RECOVER) | 53–88 (53) | punish freely; the wolf stands | hitbox off from 54 |

A hit on the first tick of a phase is handled before the wolf's update that tick, so it follows the phase before (edges test).

**The state machine.**

| Object | State | Clip | Entered when |
|---|---|---|---|
| mage | IDLE / RUN | `idle` / `run` (re-entry restarts at frame 0) | on floor, \|velocity.x\| < 5 / ≥ 5 |
| mage | RISE / FALL | `rise` / `fall` | airborne, velocity.y < 0 / ≥ 0 |
| mage | CAST / HURT | `cast` / `hurt` | cast hold / hurt hold active |
| mage | FAIL / WIN | `fail` or `fail_pit` / `win` | hit at 0 HP or pit / exit reached |
| wolf | PATROL | `patrol` | start; RECOVER timer ends |
| wolf | GROWL → LUNGE → RECOVER | `lunge` (one clip, 89 frames) | player in sight → timer → timer; a GROWL hit jumps to RECOVER |
| wolf | DEAD | `dead` | HP reaches 0, from any phase |

No AnimationTree. **Two clocks:** both clip players `ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS`, run before their owners (`process_physics_priority = -1`); no AnimatedSprite2D; the torch flicker player stays on the process clock and nothing reads it. Gameplay reads the hitbox on the physics tick, in the overlap check inside `wolf.gd`'s LUNGE branch, which first runs on the tick after LUNGE starts and last on the tick it switches to RECOVER: clip frames 32–53 against the active 31–52, a measured largest disagreement of 1/60 s. (`monitoring` itself is on for 31–53 because it is switched off with `set_deferred`.)

**Evidence split.** Read-backs: tracks, key times (half-frame tolerance), step, loop mode, update mode, frame range. Pins: behaviour and the phase timings. Edges: an interrupt one tick before, on and after every phase boundary. Strips (fixtures and real renders): the lunge at each boundary, the run's seam and registration. My eyes in the running game: the cycle over five wraps, the three phases and an interrupt in each, both clips over the darkest and lightest art.

**Short answers** *(mine, translated from my Chinese)*.

1. **Routes.** The run uses Sprite2D + an AnimationPlayer frame track; the lunge is a cutout rig keyed as resource text. The AnimationPlayer read-back sees every track's node and property path, exact key times, `loop_mode`, and a frame track's update mode and range; with AnimatedSprite2D the animation lives in a separate SpriteFrames resource that the AnimationPlayer read-back cannot see.
2. **Continuous frame track.** Between two keys the sprite sweeps through every intermediate frame number, because `frame` is an integer and continuous updates interpolate between keys and round; the motion scrambles or flickers.
3. **Step.** 1/60 s for the lunge, written at 60 fps; 0.1 s for the run at 10 fps. Left at the default 1/30 s, editor snapping puts keys on a 30 fps grid, so odd-frame times shift and no longer meet the 60 Hz phase boundaries.
4. **One authority.** The mage's `Sprite2D` frame belongs to her AnimationPlayer; the wolf's pivots belong to its AnimationPlayer; the state machines only call `play()`. Other writers in the project: the old `_set_state()` texture writes (replaced), and facing (`flip_h`, `Facing.scale.x`) if it were ever keyed; the hurt tint writes a shader parameter, not these properties.
5. **Two clocks.** Both AnimationPlayers and the hitbox run on the physics tick, so the clip and gameplay advance together; but gameplay reads the hitbox in the overlap check inside the LUNGE branch, which first runs on the tick after LUNGE starts and last on the tick it switches to RECOVER, so it reads one tick later than the clip's active section: the largest disagreement is 1/60 s. *(I first wrote 0 s; corrected to the measurement from `tests/probe_two_clocks.gd`.)*
6. **Seam.** No duplicate frame at the ends, and the gap from the last key (frame 3 at 0.3 s) to the length (0.4 s) equals the frame interval (0.1 s). A duplicated frame 0 at 0.4 s would show frame 0 for twice as long every loop: a visible hitch in the step.
7. **Imported rig.** Not used.

**The four ideas** *(mine, translated)*. A clip is a timeline of keys on named node properties; a track resolves its target from a NodePath string at run time, so a wrong path or a missing property is skipped with no error and no change on screen. One authority means each animated property is written by exactly one player; with two, they overwrite each other every frame and the picture twitches or falls out of step. The two clocks are the variable-rate process clock and the fixed-step physics clock; my state machines, the hitbox and both clip players run on the physics clock. Designing feel in frames means splitting an action into startup, active and recovery frame counts and shaping how it reads and how predictable it is through those counts, not by dragging keys by eye.

### 2026-11-13 — note on the four ideas

My answer that a track to a missing property "is skipped with no error and no change on screen" is my understanding, not a measurement: no run here played a broken clip. What was measured is that the read-back catches it (M1 and the earlier a7-4 exit 1).

### 2026-11-14 — why the published structure arrived late; presentation rule; the frame strip

**Timing.** The full assignment text appeared on Canvas on 2026-11-13. Before that, the page showed the instructor's revision notes, and this brief's original (`2cc97d0`, committed before the first prompt) was written to them. The revision of 2026-11-13 restates the contract in the published structure; nothing above it was edited.

**Boundaries, added rule.** Presentation code may read game state; it never writes it (`player.gd` and `wolf.gd` only call `play()` / `seek()` and set facing; `lunge_afterimage.gd` reads the wolf and writes only its ghosts).

**The frame strip.** Preview background: the real cave level from `game/main.tscn` (the lunge is captured in the game itself through a harness that places the two characters, so it is labelled a fixture). Trigger frame: the tick the wolf enters GROWL. Frames read: growl start + 0, 25, 31, 37, 53, 65 and 89, one per key and phase boundary of the phase table, for a left-facing and a right-facing lunge (`captures/lunge/game-r0/`). Each should show: 0 neutral; 25 the crouch; 31 the crouch held at the GROWL → LUNGE boundary; 37 the stretch with the dash under way; 53 the stretch held at LUNGE → RECOVER; 65 the overshoot; 89 the wolf back in PATROL. Captured at 60 fps, not 30, because the phase table is in the wolf's 60 Hz physics ticks: at 60 fps strip frame n is tick n, while at 30 fps the boundaries at odd ticks (25, 31, 37, 53, 65, 89) fall between frames.
