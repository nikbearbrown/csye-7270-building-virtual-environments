# FRICTIONAL.md — Assignment 7: two animations

The A6 log is at tag `a6`. This file replaces it. Written by the agent
(Claude Code) on 2026-11-22 from the commits, logs, transcripts and the
user's own words; agent actions are attributed to the agent, human decisions
and observations to the user. Tuning detail is in TUNING.md, results in
TEST-REPORT.md; this file points to them rather than copying them.

## How the work ran

| Who | Did |
|---|---|
| User | Chose where the work lives (a new course-repo folder, as A6), the art source (the game's Sol art), the rig route (2D cutout on a 3D billboard), the attack-speed rule (r4), and accepted or declined every proposal; watched every preview and gave every verdict; ran the Movie Maker capture; kept r0. |
| Agent (main session) | Wrote CHANGE-BRIEF.md and revisions r1–r7, the pins, the probe, the review of every session, the previews, the mutation runner, TUNING/TEST-REPORT/this file, and every commit. |
| Delegated agent sessions | Step 1 CLAUDE.md draft (`sessions/session-1.excerpt.jsonl`); Step 3 `npc_idle` (`session-3.jsonl`); Step 4 rig (`session-4.excerpt.jsonl`); Step 5 plan and six implementation invocations (`session-5-plan.excerpt.jsonl`, `session-5.excerpt.jsonl`). Prompts in `prompts/`. |

The course runs agent steps as `claude -p`. The `claude` CLI is not installed
here, so, as in A5 and A6, each step ran as a delegated agent session given
the prompt verbatim plus written tool rules in place of `--allowedTools`
(the session prompts say which commands were allowed). Step 4 had one extra
allowed command, approved by the user: `python -I tools/a7_cut_rig_parts.py`.

## What was tried and what happened

1. **The art source.** The agent warned that A2's rule for generated sprites
   asks for no copyrighted character; the user answered "ordinary fan
   derivative work, no violation" (translated) and kept the Sol art; later
   gave the model as "gpt sol 6.1" and asked to record only that (brief r7,
   `animations/ATTRIBUTION.md`). Terms and prompts are not recorded because
   the user did not supply them.
2. **The Step 1 draft found two real conflicts** in the agent's brief: a
   second writer to the operator sprite's `visible`, and three existing test
   expectations change 1 would break. The user accepted both fixes (r1,
   `99c9a4a1`).
3. **Headless input.** The pin harness's clicks never reached
   `GameManager._input` under `--headless` (diagnosed with a probe: the press
   registered, the pointer did not). The A6 suite already had the fix
   (`root.push_input`); the pins reuse it (`573e244b`). This is also why
   `test_lappland_input` has always failed headless.
4. **A wrong guess in a pin.** The first draft predicted a 3-unit click walk
   in 31–36 ticks; the game measured 26 ticks and 2.38 units in two identical
   runs, and the pin records the measured value (`tests/test_a7_pins.gd` T5).
5. **The brief was wrong about the sheet.** It said 16 columns; the Step 4
   session measured 14 (896×320) (r2, `9333f4bd`).
6. **A pin the agent should have marked.** Pin S1 expected the sprite's
   "wave" pose, which change 1 removes; the agent had not marked it as one the
   brief changes. The Step 5 plan session stopped on it, with five more test
   expectations r1 had missed (r3, `a38513fb`), and r5 added five more found
   by running (`0b5dda83`).
7. **Transcripts.** The first committed Step 1 transcript was a truncated
   copy of the task output stream (12 records); the full log is 1.2 MB. The
   agent replaced it with a labelled excerpt and the full log's SHA-256
   (`b53bfb70`). The full logs live in the subagent folder, not in the task
   output file.
8. **The mutation runner's first run did nothing.** Git Bash rewrote the
   sparse-checkout pattern `/fall-2026/...` into a Windows path, so every
   worktree was empty and no mutation ran; four empty worktrees were left
   behind. The agent removed them, fixed the pattern (cone mode, no leading
   slash), tested it in one worktree, and reran (`5cc51a16`, `1dc09f6a`).
9. **The strip preview's click missed.** In the window the event's pointer
   landed off the enemy; pushing the same events into the root window fixed
   it, verified by a per-frame log (`e51a4563`). The brief's "trigger at
   capture frame 10" was impossible (loading takes ~17 frames), so the
   frames to read come from the log (r6).
10. **A lost log.** The user's two windowed looks after the capture
    overwrote the r0 per-frame log; the r0 frames still match the agent's
    smoke run exactly (29/37/41/50). The preview now writes one log per run
    (`5ebdda9b`).
11. **Things that worked first time,** and how that was checked: the NPC
    seek-based phases (a probe measured three squad figures at 0.88/1.22/0.22
    s); the plan step 2 attach (nine suites unchanged); the four mutations
    after the runner fix (each failure line read, not only the exit code).

## What was checked, changed or learned in response

- Every session's diff and tests were reread and rerun by the main session
  before commit; three test files were audited for direct calls to the
  transition functions (none).
- The user added the attack-speed rule mid-stream (r4): buffs speed the
  release like every swing, debuffs only lengthen the cooldown.
- The rig's SubViewport rendered every frame while hidden; the agent's
  review added `UPDATE_DISABLED` at rest (`f965840e`).
- RESET was not playing at start; adding it tripped the structure test's S6,
  and the user chose to allow `_build_wave_rig` as a caller (`6648c007`).
- **Unresolved:** death, loss of control, operator swap and leaving the floor
  mid-release are untested; edges at r > 1 are untested; Claude's two strip
  observations (an early hit flash, facing) were not taken up.

## Accepted, modified, rejected (the user)

- **Accepted:** the brief; r1; all five Step 5 stop-item recommendations
  (r3); every plan step; the re-pin; the S6 allowance.
- **Chose:** location, art source, rig route, "scale like today" for attack
  speed, "Keep r0, no revision".
- **Rejected / declined:** using a CC0 or code-made sheet instead of the Sol
  art; a tuning revision after Claude's strip reading.

## Traceability

Commits in the order the work happened: `git log -- .` in this folder (brief
`1d6ec52f` → pins `573e244b` → setups `3c6605eb`, `1722fbbd` → wiring
`b0e69214`, `1f148a98`, `f965840e` → tests `42a78312`, `45cf5845` → re-pins
`e3a9f825`…`4d76441f` → mutations `1dc09f6a` → strip `5ebdda9b`). Human
checks: `evidence/a7/human-checks.md`. Tuning: TUNING.md.
