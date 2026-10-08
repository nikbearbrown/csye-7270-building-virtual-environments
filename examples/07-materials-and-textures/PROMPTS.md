# Prompts — Example 07

## Executive summary

These are the exact prompts and command lines used for Chapter 7's worked run on 2026-09-27. Sessions 1 and 2 ran on Claude Code 2.1.150 (default model `claude-sonnet-4-6`, with `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`). Session 2b ran on Codex CLI 0.153.4 (configured model `gpt-5.6-sol`, reasoning effort `low`) after the Claude account reached its session limit. The attribution facts in prompt 1 were checked on polyhaven.com and api.polyhaven.com before the run.

## Session 1 — audit (Claude Code)

```bash
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude -p "$(cat prompt-1-audit.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot --headless:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(grep:*)" --max-turns 60 --output-format stream-json --verbose < /dev/null > session-1-audit.jsonl
```

The prompt text is `prompts/prompt-1-audit.txt`; it is printed in full in Chapter 7, *Build It*.

Outcome: 30 turns, about 10 minutes. The agent wrote `MATERIALS.md` (167 lines) and `test_materials.gd` (238 lines, 95 checks, all passing). A plain `godot --version` was refused by the scoped permissions. Human review corrected four claims (commit `10512bd`).

## Session 2 — the change (Claude Code), cut off

```bash
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude -p "$(cat prompt-2-ao.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot --headless:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(grep:*)" --max-turns 60 --output-format stream-json --verbose < /dev/null > session-2-ao.jsonl
```

The prompt text is `prompts/prompt-2-ao.txt`, printed in full in Chapter 7.

Outcome: 23 turns, about 14 minutes; final result `You've hit your session limit · resets 6:40pm (America/New_York)`. The partial work was committed unedited (`791a0e8`).

## Session 2b — the same change (Codex), with a handoff paragraph

```bash
codex exec -s workspace-write --json -o session-2b-ao-codex-last.txt "$(cat prompt-2b-ao-codex.txt)" < /dev/null > session-2b-ao-codex.jsonl
```

The prompt is the text of `prompt-2-ao.txt`, preceded by this paragraph:

```text
A previous agent session on this task was cut off by a usage limit. Its
unfinished work is committed as HEAD (see git show HEAD); godot/diag.gd is
its scratch file. Check that work against the task below before building on
it, fix or replace anything that does not meet the task, and delete
godot/diag.gd when you are done. Always run Godot with --headless; never
add --rendering-driver.

The task:
```

Outcome: 20 shell commands; about 1.74 million input tokens (1.66 million cached) and 7,900 output. The external material was wired correctly and the test passed 100 checks, but `ao_enabled` was not set. The human fix is commit `bf86ae3`.

## Our verification (not an agent prompt)

Delete `godot/.godot` (Godot's import cache), then:

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_materials.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://test_settings.gd --fixed-fps 60
```

`probes/probe_hull.gd` was copied into `godot/` temporarily, run the same way, and removed again.
