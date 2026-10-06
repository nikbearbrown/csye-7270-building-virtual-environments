# Example 06 — Shader foundations: a failure flash in walker-jumpman-clawd

## Executive summary

**What this is.** The worked record behind Chapter 6. It has three parts:

1. A headless experiment on what Godot 4.7.2 can check about shaders without a window.
2. Two Claude Code sessions: one wrote `CLAUDE.md` with a student-authored effect spec, the other built a `canvas_item` failure flash for Clawd.
3. Our own verification of that work.

**Why it exists.** The chapter's claims about the agent's work, and about headless verification, must trace to runs that happened. This folder is where they trace to.

**What was found.**

- The agent's shader was right: it started from `COLOR` and kept alpha.
- Its driver was frame-rate independent: it derived the flash from the session's `retry_remaining`.
- Its `CLAUDE.md` draft had wrong line citations and one false claim that a headless test could confirm the look.
- Its test stopped exercising frame timing after a 30 fps failure. With the shader deliberately broken, the test still passed 11 of 11.
- Our own `verify_flash.gd` passed at 30, 60 and 144 fps and failed on the broken shader.

No window was opened for the build or its verification, so nothing here shows what the flash looks like. The look is the student's human check.

## Contents

| Path | What it is |
|---|---|
| `HEADLESS-SHADER-FINDINGS.md` | The experiment: what a headless run reports about shaders, materials and textures, with real outputs |
| `headless-probe/` | The probe project (shaders, scripts, scenes) and its logs |
| `prompts/` | The two prompts exactly as given to Claude Code (also in `PROMPTS.md`) |
| `PROMPTS.md` | Prompts and the exact command lines used |
| `changes.diff` | `git diff` from the baseline (`0c7679b`) to the final state (`b363a67`), all commits |
| `git-log.txt` | The scratch repository's commits, in order, with who made each change |
| `files/CLAUDE.agent-draft.md` | `CLAUDE.md` exactly as session 1 wrote it |
| `files/CLAUDE.md` | `CLAUDE.md` after human review (commit `ea760cd`) |
| `files/clawd_flash.gdshader`, `files/player.gd.diff` | The agent's shader and its change to `player.gd` |
| `tests/test_flash.gd` | The agent's test (session 2, final version) |
| `tests/verify_flash.gd` | Our verification script (student-written, not the agent's) |
| `logs/` | Baseline, after-change, verification and mutation logs (ANSI colour codes stripped) |
| `transcripts/` | Both sessions' `stream-json` transcripts (112 KB and 651 KB). The init event's lists of the instructor's installed plugins, skills and slash commands are replaced with counts; nothing else is edited. |

## Starting point

- Public repository `https://github.com/nikbearbrown/walker-jumpman-clawd`, commit `382f2baa5ee5e90a5afc083d82a5337845157f34`.
- Only `godot/` and the root `.md` files were copied. The local checkout had an uncommitted `README.md` edit; the committed version was used.
- `test_clawd.gd.uid` did not exist at that commit. Godot generated it on the first baseline test run, and it was committed separately (`a8e9550`) so the diffs show only authored changes.
- `test_clawd.gd` writes a report to `../evidence/clawd/`. That folder was excluded from Git in the scratch copy.

## How to reproduce

From a clone of the public repository at the commit above, with Godot 4.7.2 on your `PATH`:

```bash
git checkout -b ch06-failure-flash 382f2baa5ee5e90a5afc083d82a5337845157f34
```

```bash
godot --headless --path godot --import
```

```bash
godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

Then run the two prompts in `PROMPTS.md`, review `CLAUDE.md` against `files/CLAUDE.md`, copy `tests/verify_flash.gd` into `godot/tests/`, and run:

```bash
godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 30
```

Repeat with `--fixed-fps 60` and `--fixed-fps 144`, then grep each log for `SHADER ERROR`. An agent run will not reproduce this transcript word for word. Compare your agent's result with the spec, not with ours.

## Results (from `logs/`)

| Check | Result |
|---|---|
| `test_game.gd` @60, baseline and after | 25 PASS, 0 FAIL |
| `test_keyboard.gd` @60, baseline and after | 9 PASS |
| `test_clawd.gd` @60, baseline and after | `"checks":1950,"failures":0` |
| `test_flash.gd` (agent) @30/60/144 | exit 0, 11 checks |
| `verify_flash.gd` (ours) @30 / @60 / @144 | 12 PASS each; failure lasted 17 / 34 / 82 frames = 0.567 / 0.567 / 0.571 s of game time; flash equalled the countdown on every frame |
| Mutation: one `;` removed from the shader | `test_flash.gd` exit 0 (11 checks pass); `test_game.gd` 25 PASS; `verify_flash.gd` exit 1 (3 FAIL); every log shows `SHADER ERROR: Expected a ';'.` |

## Human checks not performed

These are the student's checks, listed in Chapter 6, *Use It*:

- Clawd's colours at `flash_amount` 0.0.
- The tint at 0.5 and 1.0 against the predicted values.
- The level and HUD staying untouched.
- The flash reading well against the cream background.

## Incident

During the headless experiment, four probe runs (about one second each) used `--display-driver headless` or `--headless --rendering-driver …`. Godot fell back to the macOS display server, so a window may have appeared briefly. See `HEADLESS-SHADER-FINDINGS.md`. The runs were not repeated.
