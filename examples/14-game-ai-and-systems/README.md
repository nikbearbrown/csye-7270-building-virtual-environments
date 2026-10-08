# Worked example — Chapter 14, Game AI and Systems

## Executive summary

**What this is.** The record behind Chapter 14 (`../../chapters/14-game-ai-and-systems.md`): every prompt, diff, test, log and agent transcript from the runs of 2026-09-27, plus the audit scripts the chapter author wrote to check the agents' claims.

**Why it exists.** The chapter's evidence standard says an agent's "done" is not evidence. This folder is the evidence: you can rerun each test and compare its output with the logs here.

**What was found.**

- **Main hands-on (guard NPC in `walker-2d-finite-state-machine`).** Three handed-off tasks. Task 1 (navigation, Claude Code) and Task 2 (FSM, Claude Code) passed their own tests; Task 3 (behavior tree) hit the Claude Code usage limit before editing anything and was completed by Codex from the same handoff file, in two runs. Final state: 61 checks pass (4 navigation, 14 shared FSM/BT behavior, 14 BT composite, 18 + 11 original player checks), in both `--fixed-fps 60` and real-time mode, with no script errors, except that the original `test_combo.gd` is flaky (below).
- **What the agents' passing tests missed**, found by the audits in `audit/`: a "never inside the obstacle" check that physics made impossible to fail (the audit measured 17.9 px minimum clearance and 0 obstacle contacts instead); a claim that movement starts "on the next physics tick" (measured over 20 trials: first path on the 2nd to 9th physics frame, varying trial to trial, because navigation map sync runs on a background thread by default; frame 2 or 3 in every trial with async iterations turned off); a hysteresis test that never held the player in the band (the audit held it for 120 physics frames: 0 mode changes, both brains); both brains ignore a player standing 120 px away in plain sight for about 165 physics frames while searching (the spec never said otherwise).
- **Task 3's first Codex run** passed 12 of 12 behavior checks while printing 626 lines of `SCRIPT ERROR`; Codex itself reported the error and stopped, reading "if any test fails, stop" as covering its own new test.
- **The Walker build's own `test_combo.gd` is flaky** on the untouched baseline: 3 of 16 runs failed the same six combo checks (2 of 8 with `--fixed-fps 60`, 1 of 8 without). Cause not diagnosed.
- **Lab A (Q-learning, Codex).** Repeatable from a seed (byte-identical curves); the greedy policy is an optimal 8-step pit-free path, optimal from episode 101 onward for seed 42 (132 for seed 7); the exploring training success rate never held 100% for a 25-episode window.
- **Lab B (PCG, Claude Code).** Validator pass rate 21.5% (43/200). The agent measured the jump on the original level, where the player hit a ceiling, and got 128.3 px; on a flat floor at the same full takeoff speed (200 px/s) the range is 163.3 px. The agent's "landing" check used a hand-built flat row, not a generated level; the author's corrected check landed on all 43 accepted levels. 16 of the 157 rejections are levels that end in a gap.
- **Lab C (networking, Claude Code).** Two loopback processes: connection, one synchronized paddle move (client equal to host), and an authority-mode RPC rejected by the host with a named error. The agent, denied `kill` and `lsof` by its allowlist, put `OS.execute("/bin/kill", …)` inside the Godot test script; the author removed it. A separate audit showed the demo's `any_peer` score RPC accepted 3 of 3 forged points from the client.

**What it does not prove.** No window was opened, no human played any build, and nothing was rendered. Unity and Unreal were not run.

## Environment

macOS on the instructor's Mac; Godot 4.7.2.stable.official.ed1daf0bf (`/opt/homebrew/bin/godot`); Claude Code 2.1.150 (the sessions report model `claude-sonnet-4-6`); Codex CLI 0.153.4 run with `--ignore-user-config` (its session files record model `gpt-6-astra`).

## Starting points

| Part | Walker build (public at `github.com/nikbearbrown/<name>`) | Upstream path at `godot-demo-projects` commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7` |
|---|---|---|
| Main hands-on, Lab A | `walker-2d-finite-state-machine` | `2d/finite_state_machine` |
| Lab B | `walker-2d-dynamic-tilemap-layers` | `2d/dynamic_tilemap_layers` |
| Lab C | `walker-networking-multiplayer-pong` | `networking/multiplayer_pong` |

Only the `godot/` folder and the `.md` files of each build were copied into a scratch directory, `git init`-ed, imported once with `godot --headless --path godot --import`, and committed as a baseline. The Walker adaptations add a title change, their own test scripts (the FSM build's `test_input.gd` and `test_combo.gd` are in `main/tests/`) and, for Pong, the `--walker-loopback` user argument that binds the host to 127.0.0.1. To start from upstream, copy those scripts in and add that argument handling.

## Layout

| Path | Contents |
|---|---|
| `PROMPTS.md` | Exact prompts and commands, in run order |
| `main/changes-task1-navigation.diff` … `changes-task3-bt-correction.diff` | One diff per agent run; `changes.diff` is baseline → final |
| `main/handoffs/` | `HANDOFF.md` as each task left it |
| `main/tests/` | Final test scripts plus the two original Walker tests |
| `main/logs/` | Baseline, per-task verification, final runs in both time modes, audits, the baseline `test_combo` flakiness tally |
| `main/transcripts/` | Claude Code stream-json (sanitized: tool/MCP/skill lists removed from the init line) and Codex JSONL |
| `lab-a/`, `lab-b/`, `lab-c/` | Same pattern per lab; `lab-c/correction-by-author.diff` removes the agent's process-killing block |
| `audit/` | Scripts written by hand by the chapter author, run from outside the project so later agent runs never saw them |

## How to reproduce

From the repository root of your copy (the folder that contains `godot/`), after the agent or you have applied `changes.diff`:

```bash
timeout 120 godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://tests/test_guard_nav.gd
```

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://tests/test_guard_fsm.gd
```

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://tests/test_bt.gd
```

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://test_input.gd
```

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://test_combo.gd
```

Audit scripts run the same way with an absolute path, for example:

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script /absolute/path/to/audit/audit_guard_fsm.gd -- --brain=BT
```

Lab C runs in real time (no `--fixed-fps`), because two processes exchange packets on the wall clock. Start the host first:

```bash
timeout 30 godot --headless --path godot --script res://tests/test_authority.gd -- --walker-loopback --test-host > host.log 2>&1 &
```

```bash
timeout 30 godot --headless --path godot --script res://tests/test_authority.gd -- --walker-loopback > client.log 2>&1
```

Wrap every headless run in `timeout`: a GDScript error does not end a Godot process, and an orphaned host keeps port 8910 bound.

## Time step

Every agent run executed its tests without `--fixed-fps`. The chapter author reran every single-process test both ways. All results matched, with two exceptions that are properties of the project rather than of the flag: the navigation test's same-frame observation (background navigation sync) and the baseline `test_combo.gd` flakiness (present in both modes).
