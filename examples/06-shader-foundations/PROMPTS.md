# Prompts — Example 06

## Executive summary

These are the exact prompts and command lines used for Chapter 6's worked run on 2026-09-27: Claude Code 2.1.150, default model `claude-sonnet-4-6`, run in a scratch copy of `walker-jumpman-clawd` at `382f2ba`. The environment variable `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` was set for both sessions, so the agent kept no notes between them. The effect spec inside prompt 1 was written by the human before any code existed.

## Session 1 — write CLAUDE.md

Command (run from the repository root; the prompt text is `prompts/prompt-1-claude-md.txt`):

```bash
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude -p "$(cat prompt-1-claude-md.txt)" --permission-mode acceptEdits --allowedTools "Read,Write,Glob,Grep,Bash(git:*),Bash(ls:*)" --max-turns 40 --output-format stream-json --verbose > session-1-claude-md.jsonl
```

Prompt:

```text
You are working in a scratch copy of walker-jumpman-clawd (Godot 4.7.2,
GDScript, project in godot/). Do not change any file except the one you
create: CLAUDE.md at the repository root.

Read AGENTS.md, README.md, CHANGE-BRIEF.md, godot/project.godot,
godot/game/session.gd, godot/features/player/player.gd,
godot/features/player/clawd_art.gd and the test scripts in godot/tests/.

Write CLAUDE.md, under 120 lines, in this order:
1. The first line is exactly: @AGENTS.md
2. "Project context": engine version, renderer, main scene, how Clawd is
   drawn, which script owns the session state machine and the retry
   countdown, Clawd's collision shape, and the exact headless test commands.
   Give a file reference for every fact. Do not guess.
3. "Effect specification": copy the block between SPEC BEGIN and SPEC END
   below word for word.
4. "Out of scope": what this change must not touch, in your own words,
   consistent with the spec.
5. "Unconfirmed": anything you could not confirm from the files.

Do not write a shader and do not edit any script. Stop after CLAUDE.md.

SPEC BEGIN
Failure flash (Chapter 6)
Visible effect: when a run fails (spikes or a fall), Clawd is tinted toward a
flash color, then fades back to normal by the moment the retry happens.
1. One float uniform, flash_amount, 0.0 to 1.0, drives the effect. It is 1.0
   on the first frame of the failure and reaches 0.0 when the retry starts.
   The fade is linear in time and lasts the same wall-clock time at 30, 60
   and 144 frames per second.
2. Pressing R during the failure ends the flash at once. In every state
   except the failure, flash_amount is 0.0.
3. A second uniform, flash_color, is a color with default #25354a (the
   level's ink). Not white: the background is #f6f3ec, and white against it
   has a contrast ratio of about 1.1 to 1.
4. At flash_amount 0.0 Clawd looks exactly as before: same body color, same
   black eyes, same transparent surroundings. At 1.0 every visible pixel of
   Clawd is flash_color; transparent pixels stay transparent.
5. Only Clawd changes. The level, background, HUD and gallery do not.
6. No change to collision, movement, input, the session state machine, the
   0.55 s retry delay, or any existing test's expectations. Presentation
   code may read session state; it never writes it.
7. It must work in this project's renderer.
8. Evidence: a new headless test proves the shader is accepted by Godot's
   shader parser in a headless run, the two uniforms exist with the right
   types, and flash_amount obeys rules 1 and 2 at 30 and 144 fps. How it
   looks is a human check.
SPEC END
```

Result: 11 turns, about 100 seconds; wrote `CLAUDE.md` (108 lines). Human review corrections are in commit `ea760cd`; compare `files/CLAUDE.agent-draft.md` with `files/CLAUDE.md`.

## Session 2 — build the flash

Command (prompt text is `prompts/prompt-2-build.txt`):

```bash
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude -p "$(cat prompt-2-build.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot --headless:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(grep:*)" --max-turns 60 --output-format stream-json --verbose > session-2-build.jsonl
```

Prompt:

```text
Read CLAUDE.md first. Its effect specification is the contract for this
change; its headless facts describe what a test on this machine can observe.

Implement the failure flash with the smallest change that meets the spec:
- a canvas_item shader file for Clawd,
- the code that gives Clawd a ShaderMaterial with that shader,
- the code that sets flash_amount from session state each frame,
- a new headless test, godot/tests/test_flash.gd.

Rules:
- Do not edit the existing tests or change their expectations.
- Run the three existing test commands from CLAUDE.md, then your new test at
  --fixed-fps 30 and at --fixed-fps 144. Show the real output, including any
  SHADER ERROR lines.
- Say exactly what your test proves and what it cannot prove in a headless
  run, and list the human checks needed to judge the look.
- Do not commit.
```

Result: 25 turns, about 22 minutes (about 15 of them one reasoning step after the first 30 fps failure). Its first `test_flash.gd` failed at `--fixed-fps 30` (`expected 0.6970 got 0.7576, remaining 0.3833`). It then rewrote the test to call `_update_flash()` directly with hand-set countdown values, and both rates passed. The session's final message is at the end of `transcripts/session-2-build.jsonl`.

## Our verification (not an agent prompt)

`tests/verify_flash.gd` was written by hand after session 2, and run as:

```bash
godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 30
```

```bash
godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 60
```

```bash
godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 144
```
