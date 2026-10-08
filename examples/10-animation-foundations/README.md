# Example 10 — Pin the sword's timing, then change it

## Executive summary

**What this is.** The worked example behind Chapter 10 (`chapters/10-animation-foundations.md`): a frame-stepped headless check that pins the sword timing in `walker-2d-finite-state-machine`, followed by one animation change, the fix the check forced, and a deliberate re-pin. All runs were on 2026-09-27 with Godot 4.7.2.stable.official.ed1daf0bf on the instructor's Mac, in a scratch copy.

**Why it matters.** The build's existing combo test (11 checks) passes while the second combo swing never moves on screen: `sword.gd` re-plays `attack_fast` while it is already playing, and Godot's `play()` does not restart it. The new check pins that. When the hitbox window was then moved from code into animation keys, the check failed the invariant "every swing has at least one hitbox-on frame" for swing two. The two older tests still passed. One line (`$AnimationPlayer.seek(0.0)`) fixed it.

**What happened with the agents.** Claude Code (2.1.150, `claude-sonnet-4-6`) ran prompt 1 for 59 minutes (20 turns, 13 extended-reasoning blocks of about 248,000 characters in total) and stopped on the account's session limit before writing the test. Codex CLI (0.153.4, configured model `gpt-5.6-sol`, low reasoning effort, `--sandbox workspace-write`) then ran prompts 1–4 in about five minutes, 77 s, 67 s and 69 s.

**What it establishes, and what it does not.** Under three scripted F-key sequences at `--fixed-fps 120`, the final build passes 20/20 pinned checks (three runs), and the Walker tests still pass 18/18 and 11/11. Without `--fixed-fps` the same test failed 7, 9 and 9 of 20 checks, all of them frame-number pins; the seven invariants held every time. Nothing here establishes that the swing looks right, that the hitbox matches the art, or that any target is hit (the scene has no target). The human play check in the chapter's Use It step has **not** been done for this example; the approval in prompt 4 was given on the numbers and the probe alone, and a person still has to play it.

## Starting point

- Upstream: `github.com/godotengine/godot-demo-projects` at `a3b5c113112f77291d5f3d1360f33a882fdc52f7`, folder `2d/finite_state_machine`, MIT. The Walker copy differs only in the project name and two added tests (checked with `diff -rq` on 2026-09-27).
- Scratch baseline commit `980dee1` (Walker `godot/` + its Markdown files).

## Files

| Path | What it is |
|---|---|
| `PROMPTS.md` | The four prompts, exactly as sent, and which CLI ran each |
| `changes.diff` | `git diff` from the scratch baseline to the final commit |
| `diffs/01-pin-test.diff` … `04-repin.diff` | One diff per agent run |
| `tests/test_sword_timing.gd` | The final pinned check (Codex-written, re-pinned in run 4) |
| `tests/walker-harness/test_input.gd`, `test_combo.gd` | The Walker build's two existing tests, needed when starting from upstream |
| `reviewer/probe_sword_frames.gd` | Our own frame-by-frame probe, written before any agent ran, not shown to the agents |
| `tools/run-codex.sh` | The wrapper used for every Codex run (`codex exec … < /dev/null`) |
| `logs/` | Every headless run cited in the chapter (see below) |
| `sessions/` | Agent transcripts: Codex JSONL in full; Claude Code as a trimmed excerpt |

Key logs: `01/02-baseline-*` (18/18, 11/11); `03-reviewer-probe-baseline.log` (swing two holds at 75°); `10-verify-pin-run1..3` (20/20); `20-after-hitbox-window-*` (3 failures, 18/18, 11/11); `30-after-restart-*` (10 timing failures, invariants pass); `31-reviewer-probe-after-restart.log` (swing two moves); `40-final-pin-fixed120-run1..3` (20/20); `41-final-pin-realtime-run1..3` (no `--fixed-fps`: 7, 9, 9 failures); `42-final-*` (18/18, 11/11); `ik-0*` (the `walker-3d-ik` reproduction: `--raw` 10/12, evaluated 12/12, headless mouse mode reads back 0). The reviewer probe numbers the first processed frame after the key press as frame 0; the test numbers it frame 1.

The Claude Code raw transcript was 1.3 MB, over this book's ~1 MB limit, so `sessions/claude-run1-excerpt.md` keeps every assistant message, tool call and truncated tool result, and replaces each reasoning block with its length. `sessions/codex-check*.jsonl` are the two sandbox checks described in the chapter: an un-imported copy that printed 11/11 PASS while textures and the font failed to load, and an imported one.

## Reproduce

From an empty folder, with Godot 4.7.2 on your `PATH` as `godot`:

```bash
git clone https://github.com/godotengine/godot-demo-projects.git
```

```bash
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

```bash
mkdir -p sword-timing && cp -R godot-demo-projects/2d/finite_state_machine sword-timing/godot
```

Copy `tests/walker-harness/*.gd` into `sword-timing/godot/`, `git init` inside `sword-timing`, import, and commit the baseline:

```bash
godot --headless --path godot --import
```

Then either run the prompts in `PROMPTS.md` yourself, or apply `changes.diff` (`git apply`) and run the checks:

```bash
godot --headless --path godot --script res://tests/test_sword_timing.gd --fixed-fps 120
```

```bash
godot --headless --path godot --script res://test_input.gd --fixed-fps 120
```

```bash
godot --headless --path godot --script res://test_combo.gd --fixed-fps 120
```

Expected: `RESULT 20 checks; 0 failures`, `RESULT 18 checks; 0 failures`, `RESULT 11 checks; 0 failures`. If your agent writes its own pin test, its frame numbers may be counted differently; what must match is the behavior (swing two at position 0.25 and 0° travel on the baseline).

## Scratch commit history

```text
9b174cf agent run 4 (Codex): re-pin TIMING constants after approval; invariants unchanged
2422163 agent run 3 (Codex): every swing restarts its animation (seek(0.0)); invariants pass, 10 timing pins moved
917c521 agent run 2 (Codex): monitoring window keyed in attack_fast/attack_medium; pin test 17/20 (swing 2 invariant broken)
9d42df2 agent run 1b (Codex): tests/test_sword_timing.gd pins baseline timing (20 checks)
980dee1 baseline: walker-2d-finite-state-machine godot/ + md (copied 2026-09-27; includes import-generated test_combo.gd.uid)
```

No commit was made in the course repository or any `walker-*` folder. No window was opened; no paid generation was used.
