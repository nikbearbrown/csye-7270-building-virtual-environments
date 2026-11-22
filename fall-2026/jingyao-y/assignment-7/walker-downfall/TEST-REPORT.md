# TEST-REPORT.md — Assignment 7: two animations

The A6 report is at tag `a6`. This file replaces it. Written by the agent
(Claude Code) from executed checks (logs cited) and the user's own reported
observations (`evidence/a7/human-checks.md`, `TUNING.md`). Anything not
performed is marked **pending**.

- **Source revision:** game source as of `5ebdda9b` (the last game-code
  change is `45cf5845`; later commits change tests, docs and evidence only).
- **Engine:** Godot 4.7.2-stable (official), Forward+, D3D12, NVIDIA GeForce
  RTX 4060 Laptop GPU (`logs/a7_renderer_windowed.log`), Windows 11.
- **Mode:** every suite through `./scripts/run-test.sh <suite> <mode>`; all
  A7 suites at `60` (`--fixed-fps 60`); none waits on audio, so realtime mode
  was not needed.

## Summary

| Check | Result | Evidence |
|---|---|---|
| Baseline before the change | 93 of 103 suites pass | `logs/baseline-before/summary.txt` (commit `573e244b`) |
| Baseline after the change | 99 of 108 pass (5 new A7 suites, all pass) | `logs/baseline-after/summary.txt` (`a49e1495`) |
| Behaviour pins before / after | 16/16 before; 11/16 after wiring (the 5 predicted); 16/16 after the re-pin | `tests/test_a7_pins.gd`; `logs/test_a7_pins_after_step3_60fps.log`; `logs/test_a7_pins_60fps.log` |
| Read-back, `npc_idle` | 55/55 | `tests/test_npc_idle_readback.gd`, `logs/test_npc_idle_readback_60fps.log` |
| Read-back, `wave_release` rig | 136/136 | `tests/test_wave_rig_readback.gd`, `logs/test_wave_rig_readback_60fps.log` |
| State machine structure + state test | 51/51, identical over three runs | `tests/test_wave_state_machine.gd`, `logs/test_wave_state_machine_60fps.log` |
| Edges (interrupt before / on / after each boundary) | 39/39, identical over three runs | `tests/test_wave_edges.gd`, `logs/test_wave_edges_60fps.log` |
| Mutations (4, each in its own worktree) | m1–m3 exit 1 as required; m4 (fresh cache) passes | `logs/a7_mutations/` (`1dc09f6a`) |
| Headless facts probe | 47/47 | `tests/a7_probe_headless.gd`, `logs/a7_probe_headless_60fps.log` |

## Baseline

Every earlier suite, before (`573e244b`, A7 starting code) and after
(`a49e1495`), each at 60 through `scripts/run-baseline.sh` (12 in parallel).

- **Before: 93 of 103.** Failing: `test_amiya_input`, `test_base_crew`,
  `test_hotbar_input`, `test_loot_input` (timeouts; they need a real
  window), `test_lappland_input`, `test_ui_v1` (also failing in every A6
  baseline), and `test_audio`, `test_loot`, `test_progression`,
  `test_siracusa_enemies`.
- **After: 99 of 108.** The 5 new A7 suites pass. `test_audio`, `test_loot`
  and `test_progression` now pass (A7 did not touch them; read as earlier
  parallel-run flakes). Two flipped to fail in the parallel run, neither
  caused by A7:
  - `test_combat` `wave-spawned` (an enemy spawn wave, not the sword wave),
    `enemy_count 0`: it failed the same way in all four A6 baselines;
    brief r5 (c).
  - `test_recruit_kits`, the Santalla check "icicles fall round the aim"
    (another operator's random icicle scatter): passes 3 of 3 run alone.

## Pins

`tests/test_a7_pins.gd` drives `res://game/main.tscn` with real input
(`Input.parse_input_event`, plus `root.push_input` under `--headless`, the A6
finding). Committed before any clip existed (`573e244b`), 16/16.

| Pin | Before | After wiring | After re-pin | Brief source |
|---|---|---|---|---|
| N0–N3 NPC cells 0→1→2→3→0, 20 frames each | pass | pass (now the `npc_idle` clip) | pass | unchanged |
| S1 state order | attack_1, 2, 3, **wave**, 1 | fail | the sprite plays no "wave"; the release tick is STARTUP | r3 (1) (should have been marked at Step 2: the agent's miss) |
| T1–T5 swing interval 42 ticks, swing lock 0.25 s, dodge 17 ticks, click walk 26 ticks / 2.38 units | pass | pass | pass | unchanged |
| G1 release move lock | 0.25 s | fail (0.6667) | 20/30 s | change 1 |
| G2 release is the 4th swing | pass | pass | pass | unchanged |
| G3 / G4 wave and charge-clear tick after the release swing | 0 | fail (16) | 16 = 12 unfrozen + 4 hitstop | change 1, r3 (3), r5 (b) |
| G5 dodge 2 ticks after a release click | wave out, charge 0 | fail | no wave, charge kept | change 1 |

Each re-pinned suite is its own commit with its reason: `e3a9f825` (pins),
`84ab0ac2` (`test_lappland`), `e04089a4` (`test_builds`), `14403048`
(`test_growth`), `4d76441f` (`test_lappland_input` :78; that suite fails
headless at baseline, so the change cannot be shown passing). No other
expected value changed (diff audited before committing).

## Read-back

- **`npc_idle`** (route: Sprite3D + AnimationPlayer frame track): every track
  resolves (`track_problems`, branched on track type); 4 keys at frames
  0/4/8/12 of 12 fps (tolerance half a frame period, never `==`); length
  16/12 s; `step` 1/12 (also checked exactly, since half a frame cannot tell
  1/12 from 1/30); `loop_mode == LOOP_LINEAR`; `UPDATE_DISCRETE` (asked only
  of a value track); interpolation nearest; every key value inside the sheet
  (< `hframes*vframes` = 4); seam: last value ≠ first, no key at length, gap
  last key → length = key interval; all five NPC sheets 256×64.
- **`wave_release`** (route: cutout rig keyed as resource text): every track
  resolves; 5 tracks × keys at f0/6/10/20 of 30 fps; length 20/30 s; `step`
  1/30; `LOOP_NONE`; no track keys `Billboard` or `Rig.scale`; f0 and f20 equal
  `RESET`; manual clock (process frames do not move it; 6 × `advance(1/30)` →
  0.2 s).

## Mutations

`scripts/a7_mutations.sh`: each mutation in its own sparse git worktree of the
course repository at HEAD, imported from an empty cache, its read-back run
through that worktree's wrapper, the worktree then removed.

| # | Mutation | Read-back | Exit | Caught by |
|---|---|---|---|---|
| m1 | `ArmFront:rotation` → `ArmFront:rotaton` in `wave_release` only | rig | **1** | `track_problems`: "wave_release track 4: ArmFront has no property rotaton" |
| m2 | `npc_idle` `loop_mode` → `LOOP_NONE` | npc | **1** | `loop_mode == LOOP_LINEAR` (0) |
| m3 | `npc_idle` key 3 → 4 (= `hframes*vframes`) | npc | **1** | "key 3 value inside the sheet (0..3)" (4) |
| m4 | delete the cache (fresh worktree), `--import`, no mutation | both | 0 / 0 | the rig is a keyed cutout, not imported, so no importer setting can be lost; 136/136 and 55/55 from an empty cache |

The first run of the script checked out nothing (FRICTIONAL.md) and was
redone after the fix (`5cc51a16`).

## Fresh cache

m4 above: both read-backs pass after a fresh `--import` in an empty cache.
There is no imported rig, so "its loop mode survived" does not apply.

## State machine

`tests/test_wave_state_machine.gd` (51/51): the code's state table
(`WaveState`, `WAVE_CLIPS`, `WAVE_TRANSITIONS`) equals the brief's and exists
in the live rig resource; there is no `AnimationTree` (so the
`advance_expression_base_node` / `advance_mode` checks do not apply, stated in
the output); the rig's clip is read through `current_animation`. Through the
real loop and real input, at r = 1 and r = 1.5: STARTUP → ACTIVE → RECOVERY →
READY at 6/10/20 unfrozen design frames (12/20/40 ticks at r = 1, 8/14/27 at
r = 1.5); the wave and charge clear on the ACTIVE tick only; sprite hidden and
rig shown in every wave state; a dodge in each state returns to READY; a swing
in RECOVERY cuts it. Source scan: the rig's AnimationPlayer is called only
from the Player's state machine; nothing else writes the NPC frame or the
operator sprite's `visible`. Not exercised by a test: death, loss of control,
operator swap and leaving the floor mid-release (they share `_wave_to_ready`).

## Edges

`tests/test_wave_edges.gd` (39/39): a real dodge read on design frame 5/6/7,
9/10/11, 19/20/21 at r = 1, with the release's 4 hitstop ticks counted. f5:
READY, no wave, charge kept (3). f6 and later: the wave is out, charge 0,
READY (on f6 the spawn runs before the dodge in that tick). f20: the release
ends on its own that tick, then an ordinary dodge. f21: already READY. At the
f6 spawn tick the clip position is 0.200 s in every case that reaches it.
Edges at r > 1 are not tested.

## Two clocks

| Clip | Advances on | Gameplay reads |
|---|---|---|
| `npc_idle` | process tick (`ANIMATION_CALLBACK_MODE_PROCESS_IDLE`) | nothing |
| `wave_release` | the player's physics tick (`ANIMATION_CALLBACK_MODE_PROCESS_MANUAL`, `advance(delta*r)` from `Player._physics_process`) | the active window (the wave on frame 6), on the physics tick, from `wave_frame` |
| operator sprite (`AnimatedSprite3D`) | process tick (no such setting) | — |

**Measured largest disagreement: ≤ 1e-4 s** — the state test asserts clip
position = `_wave_time` at every wave tick at both rates, including through
hitstop (both stop together).

## Frame strips (fixture captures)

`captures/wave_release/r0/` (run by the user, 2026-11-22): capture 27 click,
29 first STARTUP, 36/37 the f5/f6 boundary (the wave leaves on 37), 40/41
f9/f10, 49/50 end. One strip, r0; no revision (TUNING.md).

## Human checks

| Check | Result (the user's words) | Source |
|---|---|---|
| The cycle seam (5+ wraps, normal speed) | "All fine" (wired, base store and field squad) — and "same" on the side-by-side fixture | human-checks.md |
| The action in play, interrupt in each phase | "Reads well"; then (translated) "I tried interrupting it during all combat states, during item searching, and while standing still; pass." | human-checks.md |
| Registration | "All fine" covered "no drift in the cell" for the NPCs | human-checks.md |
| Against the background | (translated) "The light/dark contrast is clear; pass." | human-checks.md |
| The final film (watched and listened in full) | (translated) "No problems." | human-checks.md |
| Strip verdict r0 | "I saw the record. everything is nice, we did a good job." then "Keep r0, no revision" | TUNING.md |

## Claude against the user

Claude's r0 strip reading flagged two possible issues (the click's hit flash
landing on the first startup frame; facing possibly away from the enemy). The
user kept r0 without a revision. That is a difference in emphasis, recorded
as such; the user did not report seeing either issue. No other disagreement
occurred.

## Not met / limits

- **No observation-driven tuning revision** (rubric: a prediction, two
  strips, the user's verdict). The user kept r0.
- Death, loss of control, operator swap and leaving the floor mid-release are
  not tested; edges are tested at r = 1 only.
- `test_lappland_input` and the other window-only input suites cannot run
  headless (pre-existing).
