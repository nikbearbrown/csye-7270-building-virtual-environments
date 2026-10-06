# Example 11 — A state machine that follows the player, and its edge cases

## Executive summary

**What this is.** The worked example behind Chapter 11 (`chapters/11-animation-and-interaction.md`). In a scratch copy of `walker-3d-platformer`, the `AnimationTree`'s hard ground/air switch (a Blend2 set to 0 or 1 each physics tick) was replaced by an `AnimationNodeStateMachine` named `motion` (ground, jump, fall) driven by advance expressions on the player's physics. A scripted-input test checks normal play and three edge cases: jump held through landing, direction reversal, and interrupts (reset mid-jump, shot mid-jump). All runs were on 2026-09-27 with Godot 4.7.2.stable.official.ed1daf0bf, headless, on the instructor's Mac.

**What was found.** The new machine had a real, timing-dependent bug. With jump held, the robot can land at the end of one physics tick and take off in the next tick of the same rendered frame (120 ticks per second, test at 60 fps). The tree, updating once per frame, never saw the landing and stayed in `fall` while the robot rose. Whether a given hop hits that case depends on tick parity, which is why the check passed or failed as unrelated parts of the test changed.

**What happened with the agents.** Claude Code 2.1.150 (`claude-sonnet-4-6`) built the state machine and the test (49 turns, 44 minutes of session time). Along the way it invented a nonexistent `start_node` property, left an orphaned Godot process running after a script error, fixed a missing `Start → ground` transition and transitions left at the default Enabled mode instead of Auto, and then classified the parity failure as a test problem. It stopped on the account's session limit with 9 of 11 checks passing. Codex CLI 0.153.4 (configured `gpt-5.6-sol`, low reasoning effort, `--sandbox workspace-write`) then added the one missing `fall → jump` transition (43 s) and made the test run the hop sequence at both tick offsets (51 s).

**What it establishes, and what it does not.** Final: 14 of 14 at `--fixed-fps 60` (three runs). The strengthened test fails 2a and 2b at both offsets on the pre-fix scene (a mutation check). The Walker build's original input probe still reports movement, jump, projectile and reset all true. It does **not** establish the feel. Traces show that on one tick parity the machine reports `ground`, fading from `fall`, while the robot is already rising after a held-jump landing; `jump` starts 12 ticks (0.1 s, the landing cross-fade) after the landing. On the other parity it goes straight to `jump`. An experiment with the tree processing in physics frames made both parities identical (and kept the test green) but was not applied. Whether that 0.1 s is acceptable is a human play decision, still **open**. No human has played this build.

## Starting point

- Upstream: `github.com/godotengine/godot-demo-projects` at `a3b5c113112f77291d5f3d1360f33a882fdc52f7`, folder `3d/platformer`, MIT. The Walker copy differs only in the project name (checked with `diff -rq`).
- Scratch baseline commit `221f0a4` (Walker `godot/` + its Markdown files; `youtube/`, `evidence/` and `tests/` not copied).

## Files

| Path | What it is |
|---|---|
| `PROMPTS.md` | The three prompts, exactly as sent, and which CLI ran each |
| `changes.diff` | `git diff` from the scratch baseline to the final commit |
| `diffs/01-claude-state-machine-and-test.diff` | Claude Code run 1 (state machine, `player.gd` path updates, test), as left at the session limit |
| `diffs/02-codex-fall-to-jump.diff` | The one-transition fix |
| `diffs/03-codex-both-parities.diff` | Check 2 at tick offsets 0 and 1 |
| `tests/test_motion_states.gd` | The final test |
| `reviewer/` | Our own probes and traces, not given to the agents: baseline blend parameters, held-jump traces (fresh start, both offsets), the traced copy of run 1's check 2, the FSM mid-air attack probe, and the animation inventory |
| `tools/run-codex.sh` | Wrapper used for the Codex runs (`codex exec … < /dev/null`) |
| `logs/` | Every run cited in the chapter |
| `sessions/` | Claude Code as a trimmed excerpt (raw transcript 1.2 MB, over the ~1 MB limit); Codex JSONL in full |

Key logs: `01-inspect-anims.log` (clip list, tree nodes, empty `root_motion_track`); `02-reviewer-probe-baseline.log` (one-tick `state` cut at takeoff and landing); `10-after-claude-run1-test.log` (9/11); `12-reviewer-trace-check2.log` (stuck in `fall` while rising); `13-verify-after-codex2-run1..3` (11/11); `14-mutation-prefix-scene-new-test.log` (pre-fix scene fails 2a/2b at both offsets); `15-regression-input-probe-final.*` (4/4 true); `16-reviewer-trace-final-hops.log` (the two parities); `17-reviewer-experiment-physics-callback.log` (physics-callback experiment, not applied); `20-final-fixed60-run1..3` (14/14); `21-final-realtime-run1..3` (no `--fixed-fps`: 13, 13, 14 of 14); `03-reviewer-probe-fsm-jump-attack.log` (FSM demo: body hangs at 79.3 px during a mid-air attack); `jc-*` (`walker-jumpman-clawd` tests on a scratch copy: 25/0, nine keyboard checks, 1,950 checks over 162 samples).

## Known issues in the final test (not fixed here)

- `XFADE_FRAMES := 8` is commented "Worst-case xfade is 0.1 s = 6 frames; +2 buffer", but the loops count physics ticks (12 per 0.1 s at 120 Hz).
- No check forbids `ground` while the robot is rising, so the 0.1 s landing-fade lag passes.
- The test calls `quit()` without freeing the game scene. Shutdown warnings (`13 ObjectDB instances were leaked`, `5 resources still in use`) appear in some runs and not others.

## Reproduce

```bash
git clone https://github.com/godotengine/godot-demo-projects.git
```

```bash
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

```bash
mkdir -p motion-states && cp -R godot-demo-projects/3d/platformer motion-states/godot
```

Inside `motion-states`: `git init`, import, commit, then run the prompts in `PROMPTS.md` or `git apply` `changes.diff`, and:

```bash
godot --headless --path godot --import
```

```bash
godot --headless --path godot --fixed-fps 60 --script res://tests/test_motion_states.gd
```

Expected: 14 `PASS` lines and `RESULT: PASS`. To run the traces: `godot --headless --path godot --fixed-fps 60 --script /absolute/path/to/reviewer/probe_held_jump_offsets.gd -- 0` (and `-- 1`).

## Scratch commit history

```text
38ac2a4 agent run 3 (Codex): run check 2 at two physics-tick offsets
32179b4 agent run 2 (Codex): add fall->jump Auto transition for the missed one-tick floor contact
0cf366f agent run 1 (Claude Code, claude-sonnet-4-6): motion state machine + tests/test_motion_states.gd; stopped on session limit with 2a/2b failing
221f0a4 baseline: walker-3d-platformer godot/ + md (copied 2026-09-27)
```

No commit was made in the course repository or any `walker-*` folder. No window was opened; no paid generation was used.
