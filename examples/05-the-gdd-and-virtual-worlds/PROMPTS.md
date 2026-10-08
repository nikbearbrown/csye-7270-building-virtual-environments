# Prompts and commands — Chapter 5 example

## Executive summary

Every prompt given to a coding agent on 2026-09-27 for Chapter 5, in the order it ran, verbatim, with its command line. `<scratch>` stands for the scratch working folder; the project copy was `<scratch>/ch05/walker-3d-platformer`, and `<walker>` is the local Walker framework folder. Nothing here was edited after the run.

## 0. Setup (shell)

Run inside the empty project folder, with `<src>` standing for the local `walker-3d-platformer`:

```bash
rsync -a --exclude='.godot/' --exclude='screenshots/' <src>/godot ./
```

```bash
cp <src>/*.md <src>/.gitignore ./
```

```bash
mkdir -p tests && cp <src>/tests/input_probe.gd <src>/tests/feature_route.gd tests/
```

```bash
git init -q
```

```bash
printf '.godot/\n*.import.tmp\nevidence/\n' >> .gitignore
```

Baseline commit `98fe40a`. Then:

```bash
godot --headless --path godot --import
```

```bash
godot --headless --path godot --fixed-fps 60 --script $PWD/tests/input_probe.gd -- $PWD/evidence/baseline-probe.json
```

```bash
godot --headless --path godot --fixed-fps 60 --script $PWD/tests/feature_route.gd -- $PWD/evidence/baseline-route.json
```

Skill install (commit `3376f55`):

```bash
mkdir -p .claude/skills/gdd && rsync -a --delete --exclude='__pycache__/' <walker>/gdd/ .claude/skills/gdd/
```

```bash
python3 <walker>/scripts/render_dir.py .claude/skills "AGENT_NAME=Claude" "ASSET_GEN_SKILL_DIR=.claude/skills/asset-gen" "ASSET_SKILL_COMMAND=/asset-gen" "GDD_SKILL_DIR=.claude/skills/gdd" "GDD_SKILL_COMMAND=/gdd" "RUNTIME_ASSET_DIR=assets"
```

## 1. Skill load check — Claude Code

```text
/gdd status
```

```bash
claude -p "/gdd status" --permission-mode default --allowedTools "Read,Glob,Grep" --max-turns 15 --output-format stream-json --verbose < /dev/null > session-0-status.jsonl
```

Result: 8 turns; the init event lists `gdd` among skills; Zelda reported no `design/` folder and recommended `reverse`.

## 2. Recover the design — Claude Code

```text
/gdd reverse --path godot silent
```

```bash
claude -p "/gdd reverse --path godot silent" --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep,Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 80 --output-format stream-json --verbose < /dev/null > session-1-reverse.jsonl
```

Result: 48 turns, 20 min 10 s; wrote `design/` (see `recovered-design/`); committed unreviewed as `dfcdfc2`.

## 3. Acceptance criterion (human role, no agent)

`AC-01-checkpoint-pad.md` written and committed as `9585d8e`. `author-prediction.md` written and timestamped (2026-09-27T18:28:19Z) before step 4.

## 4. Build and test — Claude Code (interrupted)

Prompt (verbatim):

```text
Implement design/AC-01-checkpoint-pad.md in this Godot 4.7.2 GDScript project
(walker-3d-platformer). Read that file, design/GDD.md sections M-05 and
06b, and godot/player/player.gd first.

One concern: a checkpoint pad that moves the player's respawn point.
Invariants: do not change any movement, jump, camera, coin, enemy, or
bullet behaviour or constant; do not change godot/project.godot; keep
the existing reset and fall code path, only change where it sends the
player. Allowed edits: godot/player/player.gd (respawn point only),
godot/game.tscn (instance the pad), and new files under godot/checkpoint/
and tests/. The pad needs a visible mesh so a person can see it.

To place the pad you may run read-only Godot probe scripts to find
walkable floor near the start; delete nothing, and put any probe you keep
under tests/. Write tests/test_checkpoint.gd as a SceneTree script that
drives the player with Input.action_press/action_release only, except the
fall check in criterion 5, which must be labelled as a constructed fixture.
It prints one JSON line per criterion and exits 1 if any fails.

Run, from the project root, and read the real output of each:
godot --headless --path godot --import
godot --headless --path godot --fixed-fps 60 --script $PWD/tests/test_checkpoint.gd
godot --headless --path godot --fixed-fps 60 --script $PWD/tests/input_probe.gd -- $PWD/evidence/probe-after.json
godot --headless --path godot --fixed-fps 60 --script $PWD/tests/feature_route.gd -- $PWD/evidence/route-after.json
(The two probes refuse to overwrite an existing report; pick a new file
name if one exists.)

If a criterion cannot be met as written, stop and say which and why; do
not weaken the criterion or the test. Finish with git status, git diff
--stat, and a list of what still needs a person to check in the editor.
```

```bash
claude -p "$(cat prompt-2-implement.txt)" --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 80 --output-format stream-json --verbose < /dev/null > session-2-implement.jsonl
```

Result: 43 turns, 23 min 26 s, CLI exit code 1. Last assistant message: "You've hit your session limit · resets 6:40pm (America/New_York)". Six permission denials: five `python3` commands and one `godot` command containing `$PWD` ("Contains simple_expansion"). Partial work left uncommitted in the working tree; no test had been run.

## 5. Review and finish — Codex

Prompt (verbatim): the five lines below, a blank line, then the whole of the prompt in step 4 unchanged.

```text
A previous agent session (Claude Code) was stopped by an account usage
limit partway through the task below, before it ran any test. Its partial
work is in the working tree: see git status and git diff. Review that
partial work critically against design/AC-01-checkpoint-pad.md, keep or
change it, and finish the task. The task, exactly as it was given:
```

```bash
codex exec --sandbox workspace-write -C <scratch>/ch05/walker-3d-platformer --json -o codex-continue-last.md "$(cat prompt-3-codex-continue.txt)" < /dev/null > session-3-codex-continue.jsonl
```

Result: 2 min 51 s, exit 0. Committed (with the partial work it kept) as `0f45ee6`.

## 6. Our verification (shell)

```bash
godot --headless --path godot --import
```

```bash
godot --headless --path godot --fixed-fps 60 --script $PWD/tests/test_checkpoint.gd
```

```bash
godot --headless --path godot --fixed-fps 60 --script $PWD/tests/input_probe.gd -- $PWD/evidence/verify-probe.json
```

```bash
godot --headless --path godot --fixed-fps 60 --script $PWD/tests/feature_route.gd -- $PWD/evidence/verify-route.json
```

Audit scripts (run from outside the project so no agent saw them):

```bash
godot --headless --script audit/keys.gd
```

```bash
godot --headless --path godot --fixed-fps 60 --script <scratch>/keycheck/ray_default.gd
```

Logs: `logs/verify-*.log`, `audit/*.log`.
