# Prompts and command lines — Chapter 0

## Executive summary

**What this is.** The exact text given to both coding agents, and the exact command lines used to run them, for the Chapter 0 worked example (27 September 2026).

**Why it matters.** The chapter prints this prompt for students to paste. The worked example is only honest if it is the same prompt, word for word.

---

## The prompt (identical for both agents)

```text
This is walker-pong, a Walker adaptation of Godot's Pong demo (Godot 4.7, GDScript).
Read AGENTS.md, README.md, GAME-BRIEF.md and GDD.md first. The brief says there is
no score system yet. Add one bounded feature: a score.

Requirements:
- When the ball leaves through the left wall, the right player scores one point;
  when it leaves through the right wall, the left player scores one point.
- Show both scores at the top of the screen, readable in the 640x400 viewport.
- Do not change paddle movement, ball speed, bounce rules, or the reset behavior.
- Keep the upstream license and attribution intact.

Before editing, tell me which files you will change and one way this change could
break existing behavior. Then implement it. Add a headless test under tests/ that
drives the real game with normal input actions only (no direct writes to the score
or the ball) and checks that each score equals the matching wall contacts. Run the
existing tests/input_route.gd and your new test with Godot headless and show me the
real output. Do not open a Godot window. Do not commit.
```

## Claude Code (2.1.150), run from the clone's root

```bash
claude -p "$(cat PROMPT.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot *),Bash(env *),Bash(mkdir *),Bash(ls *),Bash(cat *),Bash(git status *),Bash(git diff *)" --max-turns 60 --output-format stream-json --verbose > session-claude.jsonl
```

`Bash(env *)` was a mistake. `env` can run any program, so this rule approved far more than intended. Leave it out of your own allow list.

## Codex CLI (0.153.4)

```bash
codex exec --sandbox workspace-write -C walker-pong --json -o codex-last.txt "$(cat PROMPT.txt)" > session-codex.jsonl
```

When running `codex exec` from a script or a background job, close its standard input (`< /dev/null`). The Revise re-run sat for five minutes printing `Reading additional input from stdin...` until it was restarted that way.

## The Revise step's addition to AGENTS.md

See `revise/AGENTS-addition.md`. The prompt for the re-run was the same prompt as above, unchanged.
