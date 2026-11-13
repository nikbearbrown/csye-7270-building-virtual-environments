# TEST-REPORT — Assignment 7

Godot 4.7.2-stable (`ed1daf0bf`), Forward+ (Vulkan), Windows, Git Bash, RTX 5060 Laptop GPU. Every test ran through `scripts/run-test.sh` (fixed-fps headless unless stated), which now also fails on resource-load and parse errors (`c2fc155`). Game source: the commit that adds this report. Human checks are mine *(translated from my Chinese)*. Strips from the preview scenes are fixture captures; in-game strips are windowed Movie Maker runs of scripted input (real engine output), `--fixed-fps 60`, `--debug-collisions`.

## Pin first

| Step | Result | Commit |
|---|---|---|
| Baseline | 13 earlier suites, 19 runs, 0 failures | `2276069` |
| Pin recorded before any change | `tests/test_pin_behaviour.gd`: 8 scenarios (walk and stop, jump, cast, take a lunge, hit in GROWL, LUNGE, RECOVER, kill), every physics tick: player state, position, velocity; wolf state, position, HP, hitbox `monitoring`; real input via `Input.parse_input_event`. 16 checks / 0 failures at 30, 60, 144 | `a9b4bc1` |
| Clips added, not wired | pin unchanged at 30, 60, 144 | `72e8d21` |
| Clips wired into both state machines | pin unchanged at 30, 60, 144 (run reported in the session; the pin logs committed there date from `72e8d21`) | `33d78ae` |
| Behaviour change: growl hit cancels the lunge | pin differs only in `hit_growl` and `kill`, both from tick 24 (GROWL → RECOVER); not re-pinned | `72f37b8` |
| Played by me, accepted | see Human checks | — |
| Re-pinned in its own commit | only `hit_growl.json` and `kill.json` changed; the other six byte-identical; 16/16 at 30, 60, 144 | `ff71bbb` |
| Run r2, before the re-pin | pin at 60: 14/16, only the two known differences | `32eed66` |
| Every later visual change | pin 16/16 at 30, 60, 144 after each | `a1b6f44`, `7a9a65e`, `272fb39` |

The prediction in my brief that only `hit_growl` would change was wrong: `kill` also hits the wolf during GROWL, so its second fireball now misses. The pin found it.

**Measured, not assumed:** the pin measured the wolf's phases at 31 / 22 / 36 ticks, not 30 / 21 / 36: `wolf.gd:71` subtracts 1/60 per tick and switches only at exactly 0, and after 30 steps from 0.5 (21 from 0.35) the timer is still about 1e-16 above zero. The phase table and every key follow the measurement (brief revision 2026-11-10).

## Clip read-backs and structure

| Test | Checks | Result (60 fps) |
|---|---|---|
| `test_clip_run.gd` | the assignment's `track_problems()` verbatim (`a87ed0a`); key times 0, 0.1, 0.2, 0.3; length 0.4; `LOOP_LINEAR`; every track discrete; every frame key < `hframes × vframes` (4); seam; sheet 248×69 in A2 colours only; all nine state clips present | 16 / 0 |
| `test_clip_lunge.gd` | `track_problems()`; key times = frame / 60 to 1e-6 at 0, 25, 31, 37, 53, 65, 89; length 89/60; `LOOP_NONE`; key value types match the property | 17 / 0 |
| `test_clip_flicker.gd` | `track_problems()`; continuous-track seam (value at 0 = value at length) per track; `LOOP_LINEAR`; energy swing 20–32 %, scale 6–9 %; nothing else keys or writes the lights | 11 / 0 |
| `test_anim_structure.gd` | every player and wolf state maps to an existing clip; `autoplay` empty; both players on the physics callback; a source scan: no script writes a property a clip keys; one AnimationPlayer per sprite; RUN re-entry restarts at frame 0 | 11 / 0 |

Silent failures these caught: rotation keys of 0° and light keys of 1.0 written as integers on float properties (key-type check, twice).

## Edges at the phase boundaries

`tests/test_anim_edges.gd`, real clicks timed so the fireball lands on the target tick (growl from tick 80, lunge 111, recovery 133), **13 / 0 at 30, 60 and 144 fps**:

| Case | Result |
|---|---|
| hit on the first and the last GROWL tick | cancel: RECOVER on the hit tick, clip frame 53, hitbox never armed |
| hit on the first and the last LUNGE tick | no cancel: matches the unhit run |
| hit on the first RECOVER tick | only HP changes |
| killing hit in GROWL, LUNGE, RECOVER | DEAD, `dead` clip, hitbox off from the next tick |
| real Esc mid-lunge | position, state and clip freeze on the same tick and resume tick for tick |
| RUN → jump → land → RUN | cycle restarts at frame 0 |
| clip frame = phase tick | on all 119 lunge-clip ticks (a full growl, lunge and recovery plus a second growl) |

Two alignment bugs, both fixed visually only (`272fb39`): the edges test found that a cancel drew frame 54 on the hit tick (now seeks 52); the windowed lunge capture's tick log showed that a growl after a one-tick PATROL started at frame 1 (both players now run first, `process_physics_priority = -1`), and the edges test was extended to cover it: with the fix removed it fails on tick 170. `test_afterimage.gd`: 6 / 0 at 30, 60, 144 (ghosts only during LUNGE, every 3 ticks, gone after 0.25–0.267 s).

## Mutations (each in a temporary `git worktree`, removed)

| # | Mutation | Caught by | Exit |
|---|---|---|---|
| a7-1 | run clip written with Godot 3 `loop = true` | — : Godot 4.7.2 loads it as `loop_mode = 1`, the run still loops; my predicted failure F1 does not occur | 0 |
| a7-2 | run frame track continuous | `test_clip_run` `every-track-discrete` | 1 |
| a7-3 | run frame key 4 (past the last cell) | `test_clip_run` frame-range and frame-key checks | 1 |
| a7-4 | lunge track to a missing node | `track_problems()`: no node at `FrontPivotX` | 1 |
| a7-5 | growl cancel removed from `wolf.gd` | `test_anim_edges` (both growl hits: the lunge continues, hitbox armed 23 ticks) | 1 |

None printed an error in a 600-frame headless run of the game without input; that run never plays the lunge or reaches the run's bad frame, so whether a7-2 to a7-4 would play silently wrong in a real lunge or run is not shown. The tests are what catch them. Logs: `logs/mutation-a7-*_60fps.log`.

## Earlier suites

All 13, at their baseline counts and 0 failures, after every commit above: player 11, cast 11, wolf 13, flow 14, audio 13, sound_triggers 11, a3_assets 22, materials 32, fireball_impact_config 54, fireball_trail_config 32 at 60; hurt_tint 17, fireball_impact 14, fireball_trail 20 at 30, 60, 144. Three earlier tests read `Player.TEXTURES`; it stays as a read-only table of what each state's clip shows, checked by the structure test against the clip keys.

## Two clocks

Both AnimationPlayers: `callback_mode_process = PHYSICS`, the tick gameplay reads, and they run before their owner's script. No gameplay fact is keyed on a track (the hitbox stays in `wolf.gd`), no method tracks, no AnimationTree, no AnimatedSprite2D. One frame-clock timer remains in today's game: the wolf's removal after death (`wolf.gd:170`) lands on physics tick 79 at 60 fps and 80 at 30 and 144 (`captures/figures/two_clocks.png`); gameplay never reads it.

## Strips and play

| Strip | Shows | My verdict in the game, 1280×720 |
|---|---|---|
| `captures/run/game-r0/` | two frames, 1 px hat hop, foot slides 13–15 px then snaps back | twitching while sliding sideways |
| `captures/run/game-r1/` | four beats; hat rows 268 / 270 / 267 / 265 exactly as predicted; no shimmer | still twitching: **reverted** |
| r2 (4-frame Gemini cycle at 10 fps) | ticks per frame 6/6/6/7 on entry, 5/6/6/7 per loop (the clip wraps on the tick it reaches 0.4 s) | **much better: kept** |
| `captures/lunge/game-r0/` (left and right) | logged rig values equal the phase table at growl + 0, 25, 31, 37, 53, 65; PATROL at +89 | the stretch and the dash work together; white flash reaches the rig; the left-facing wolf is right |
| `captures/look/` | torches, embers, afterimage, hurt tint, trail, impact after the darkening | r0 not noticeable; r1 **clearly visible: kept** |

Claude against me: Claude estimated a 2.6–3.3 px step at the waist seam; I saw none, and neither did it at 4× in the game strip. Claude read the r1 bob as matching its prediction exactly; I rejected it in play.

## Human checks

Run, stop, jump and land switch clips correctly; the lunge reads in both facings; the growl cancel works when the cast is early enough (and I kept the 0.2 s window); the hurt tint, fireball trail and impact still read in the darker cave; the mage stays readable.

## What no headless run shows

How any clip looks or feels, whether the darkening keeps the scene readable, and the frame-clock removal timing; those are the strips and my checks above.
