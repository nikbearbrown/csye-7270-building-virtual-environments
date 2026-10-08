# Example record — Chapter 1, Walker and Godot

## Executive summary

**What this is.** The record of the hands-on task in Chapter 1, run on September 27, 2026: a coding agent traced the Space key through `walker-jumpman`, then changed one tuning number (run speed 160 → 192) after writing a prediction for every automated check.

**Why it exists.** The chapter's evidence standard says a step is only described as run if it was run. Everything the chapter reports about this task can be checked against the files here.

**What we found.** The read-only trace (Claude Code) cited the right lines for the input path and every test, and made four wrong or unsupported claims (a wrong line for gravity, a jump "rise of exactly ~53.3 px over 13 ticks" when the measured rise is 56.07 px over about 20 ticks, an overclaim about the buffer fixtures, an overclaim about the route test). Codex, on the same prompt, got the gravity line right and made a different mistake. After the speed change, 2 of 25 mechanics checks failed (`speed-cap` observed 170.67, `neutral-stop` observed 10.67); the scripted route still passed (280 ticks, 0 deaths); all 9 keyboard checks passed. The agent predicted the two failures exactly and wrongly predicted that the route would fail. `main` was unchanged and still passed 25/25 and 9/9. Nothing here is a human playtest.

## Environment

| Item | Value |
|---|---|
| Date | 2026-09-27 |
| Machine | macOS, Apple M4 Pro |
| Godot | 4.7.2.stable.official.ed1daf0bf (regular build, GDScript) |
| Claude Code | 2.1.150; model recorded in the transcript: `claude-sonnet-4-6` (account default, no `--model` passed) |
| Codex CLI | 0.153.4; model from the local Codex config: `gpt-5.6-sol`, reasoning effort low |
| Starting revision | `nikbearbrown/walker-jumpman` `9387542ca473b0a252c43bfe6d4fd39b61f8d439` |
| Workspace | A scratch copy of `godot/` and the Markdown files only, `git init`, baseline commit `05b78d3`; experiment branch `experiment/run-speed-192`, commit `ed4ec86` |

## Files

| File | What it is |
|---|---|
| `PROMPTS.md` | The exact prompts and the exact commands, in order |
| `author-prediction.md` | The prediction written for this example before any agent run, by the AI agent that drafted Chapter 1, standing in for a student (not by Professor Bear) |
| `agent-prediction.md` | The `PREDICTION.md` the agent wrote before editing (copied from the experiment branch) |
| `changes.diff` | `git diff main experiment/run-speed-192`: the new `PREDICTION.md` and the one-line `tuning.gd` change |
| `logs/baseline-*.log` | Both test scripts before any change (real-time, no `--fixed-fps`) |
| `logs/experiment-speed192-*.log` | Both scripts on the experiment branch, without and with `--fixed-fps 60` |
| `logs/after-main-*.log` | Both scripts on `main` after the experiment, without and with `--fixed-fps 60` |
| `logs/clawd-*.log` | The three test scripts of `walker-jumpman-clawd` at `382f2ba`, run with `--fixed-fps 60`, for the chapter's description of that project |
| `transcripts/claude-session-1-trace.jsonl` | Prompt 1 under Claude Code (trimmed, see below) |
| `transcripts/claude-session-2-tuning.jsonl` | Prompt 2 under Claude Code (trimmed) |
| `transcripts/codex-trace.jsonl`, `codex-trace-final-message.md` | Prompt 1 under Codex, read-only sandbox (trimmed) |
| `trim_transcript.py` | The script used to trim the transcripts |
| `audit/err_before_quit.gd`, `audit/err_before_quit.log` | A deliberate script error before `quit()`: headless Godot kept running until `timeout 15` killed it (exit 124). Supports the chapter's advice to wrap test runs in `timeout` |

**Transcript trimming.** The original Claude Code stream-json files were 130–135 KB each and the Codex JSONL 95 KB. We removed the session-start hook events and the `init` event's listing of locally installed tools, MCP servers, plugins, and skills (the instructor's machine configuration, not part of the task), removed thinking-block signatures, reduced the final `result` event to its outcome fields (turn count, duration, result text, permission denials; usage and cost fields dropped), and replaced the scratch path with `<scratch>` and the home folder with `~/`. Every assistant message, tool call, and tool result is otherwise verbatim. The script that did this is `trim_transcript.py` in this folder; it only deletes whole events or fields and rewrites the path prefix.

## Results at a glance

| Run | Mechanics (25) | Keyboard (9) | Notes |
|---|---|---|---|
| Baseline, real time | 25 pass | 9 pass | 22.4 s wall time; rise 56.07 px; route 325 ticks |
| Baseline, `--fixed-fps 60` | 25 pass | 9 pass | 0.34 s; identical values |
| Speed 192, real time (agent and us) | 23 pass, 2 fail | 9 pass | `speed-cap` 170.67, `neutral-stop` 10.67, route 280 ticks |
| Speed 192, `--fixed-fps 60` (us) | 23 pass, 2 fail | 9 pass | identical values |
| `main` afterwards, both modes | 25 pass | 9 pass | |
| Clawd, `--fixed-fps 60` | 25 pass | 9 pass | `test_clawd.gd`: 162 samples, 1,950 checks, 0 failures |

## How to reproduce

From a fresh clone of `walker-jumpman` at `9387542`:

```bash
godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

```bash
godot --headless --path godot --script res://tests/test_keyboard.gd --fixed-fps 60
```

Then follow `PROMPTS.md`. The agents' wording will differ from ours; the test results should not.

## What this record does not show

No one opened the Godot editor or played either speed. Readability of landings at 192 px/s, the feel of the jump, and whether the faster run is better are human judgments this record leaves open. No export was made. No commit or push was made to any public repository.
