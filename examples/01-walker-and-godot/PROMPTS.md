# Prompts and commands — Chapter 1 example

## Executive summary

The exact prompts given to the coding agents on 2026-09-27, in the order they ran, with the exact command lines. Paths are shortened: `<scratch>` stands for the scratch working folder, and the repository copy was `<scratch>/ch01/walker-jumpman`. Nothing here was edited after the run.

## 0. Setup (human, shell)

Run inside the empty `<scratch>/ch01/walker-jumpman`, with `<src>` standing for the local clone of `walker-jumpman` at `9387542`:

```bash
rsync -a --exclude='.godot/' <src>/godot ./
```

```bash
cp <src>/*.md <src>/DESIGN-STATUS.json <src>/.gitignore ./
```

```bash
git init -q
```

`evidence/` and `youtube/` were not copied. The copy was committed as the local baseline (`05b78d3`).

```bash
godot --headless --path godot --script res://tests/test_game.gd
```

```bash
godot --headless --path godot --script res://tests/test_keyboard.gd
```

```bash
git checkout -b experiment/run-speed-192
```

The example's prediction (`author-prediction.md`, written by the agent drafting the chapter in the student's role) was written and timestamped at this point, before any coding agent ran.

## 1. Trace, no edits — Claude Code

Prompt (verbatim):

```text
Inspect only; do not edit any file. This is the walker-jumpman project
(Godot 4.7.2, GDScript). Trace what happens when the player presses Space
during play, from the key to the jump the player sees on screen. For each
step give the file and line number: where the key is bound to an action,
where the action is read, where the jump velocity is applied, where gravity
and movement are integrated, and where the character is drawn. Then list
which checks in godot/tests/ exercise this path, by check id. Finish with
two short lists: what those tests establish about the jump, and what only
a person playing the game can judge.
```

Command:

```bash
claude -p "$(cat prompt-1-trace.txt)" --permission-mode default --allowedTools "Read,Glob,Grep" --max-turns 40 --output-format stream-json --verbose > session-1-trace.jsonl
```

Result: 10 turns, 1 min 36 s, no files changed. The agent also ran one `find` through Bash (a built-in read-only command in Claude Code; `--allowedTools` pre-approves, it does not restrict). Transcript: `transcripts/claude-session-1-trace.jsonl`.

## 2. One change, prediction first — Claude Code

Prompt (verbatim):

```text
One bounded change in this walker-jumpman project (Godot 4.7.2, GDScript).
The change: in godot/features/player/tuning.gd set speed from 160.0 to 192.0.
Nothing else.

Before you edit anything, write PREDICTION.md. For every check id in
godot/tests/test_game.gd and godot/tests/test_keyboard.gd, say PASS or FAIL
after the change and give the reason from the test code. Then make the one
edit. Do not edit any test, level file, or other script.

Run these two commands and read their real output:
godot --headless --path godot --script res://tests/test_game.gd
godot --headless --path godot --script res://tests/test_keyboard.gd

Report each failing check id with its observed values, compare the results
with PREDICTION.md line by line, and show git diff. Do not try to make a
failing check pass. Tell me what a person should still check by playing.
```

Command:

```bash
claude -p "$(cat prompt-2-tuning.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*)" --max-turns 60 --output-format stream-json --verbose < /dev/null > session-2-tuning.jsonl
```

Result: 13 turns, 4 min 7 s. Files changed: `godot/features/player/tuning.gd` (one line), `PREDICTION.md` (new). No test touched. Transcript: `transcripts/claude-session-2-tuning.jsonl`.

Note: the test commands in this prompt omit `--fixed-fps 60`. walker-jumpman's tests count physics ticks, so the result does not depend on the flag; we verified that by rerunning with it. For your own prompts, include the flag (see Chapter 0, "The time trap").

## 3. Verification (human, shell)

```bash
godot --headless --path godot --script res://tests/test_game.gd
```

```bash
godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

```bash
godot --headless --path godot --script res://tests/test_keyboard.gd --fixed-fps 60
```

```bash
git add godot/features/player/tuning.gd PREDICTION.md
```

```bash
git commit -m "Experiment: run speed 160 -> 192 (speed-cap and neutral-stop fail; route passes in 280 ticks)"
```

```bash
git checkout main
```

```bash
godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

```bash
godot --headless --path godot --script res://tests/test_keyboard.gd --fixed-fps 60
```

Logs: `logs/experiment-speed192-*` and `logs/after-main-*`.

## 4. Trace, no edits — Codex (comparison)

Same prompt text as step 1, run on `main` after step 3:

```bash
codex exec --sandbox read-only -C walker-jumpman --json -o codex-trace-last.md "$(cat prompt-1-trace.txt)" < /dev/null > codex-trace.jsonl
```

Result: 53 s, three shell commands (`rg`, `nl`/`sed` reads), no files changed. Transcript: `transcripts/codex-trace.jsonl`; final message: `transcripts/codex-trace-final-message.md`.

## 5. Instruction-file check — Claude Code (walker-jumpman-clawd copy)

A one-turn question with all tools disabled, in a copy of `walker-jumpman-clawd` that contains `AGENTS.md` and no `CLAUDE.md`:

```bash
claude -p "Do not use any tools. Were you given the contents of a project instruction file named AGENTS.md or CLAUDE.md from this repository at session start? If yes, quote its first line exactly. If not, reply NONE." --tools "" --max-turns 1 --output-format json < /dev/null
```

Result: `NONE`. This is the model's self-report, consistent with the Claude Code documentation that direct `AGENTS.md` reading requires v2.1.277 or later (we ran 2.1.150).
