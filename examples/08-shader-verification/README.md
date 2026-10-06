# Example 08 — Shader verification: reviewing a plausible but incorrect flash change

## Executive summary

**What this is.** The worked record behind Chapter 8. A seeded commit changes Chapter 6's failure flash in two plausible ways: a 33-frame counter replaces the game-time countdown, and the shader samples `texture(TEXTURE, UV)` instead of `COLOR`. Then:

- Claude Code and Codex review it blind;
- Codex builds the evidence (a spec-level timing oracle, a CPU colour model, a human test bench);
- we test the oracle against known-good and known-bad code and correct its tolerance;
- Codex fixes the change;
- we verify.

**Why it exists.** Chapter 8's claims must trace to real runs.

**What was found.**

- The seeded commit passes every project check at 60 fps, including Chapter 6's own verification, and fails only at 30 and 144 fps.
- Both reviewers found both bugs without hints.
- The agent's timing oracle rejected the correct Chapter 6 code at 144 fps until its tolerance was corrected.
- Codex credited a named person with work that person did not do, twice.

The shader bug is invisible to every headless check; the claim that it breaks Clawd's colours rests on Godot's documented `COLOR` semantics and has not been observed.

## Contents

| Path | What it is |
|---|---|
| `seeded-change.diff` | The seeded commit (`2473fd8`), written by the book's author for review |
| `changes.diff` | `git diff` from the Chapter 6 end state (`b363a67`) to the final state (`081c7c0`) |
| `git-log.txt` | All commits, including Chapter 6's, each labelled with who made it |
| `prompts/` | `prompt-1-review.txt`, `prompt-2-evidence.txt`, `prompt-3-fix.txt` (also in `PROMPTS.md`) |
| `files/clawd_flash.seeded.gdshader`, `clawd_flash.fixed.gdshader`, `fix.diff` | The shader before and after, and the fix |
| `files/BENCH.md` | The human bench procedure (Codex's, plus one human-added line on rounding) |
| `tests/verify_flash_spec.agent.gd` / `verify_flash_spec.gd` | The agent's spec oracle, and the version with the corrected tolerance |
| `tests/flash_model.gd`, `flash_bench.gd`, `flash_bench.tscn`, `test_flash_bench.gd` | CPU model, bench scene, bench structure test |
| `tests/verify_flash.gd`, `test_flash.gd` | Chapter 6's checks (ours and the agent's), for the matrix |
| `logs/seeded-*.log` | Every check on the seeded commit before any agent ran |
| `logs/oracle-*.log` | The oracle against the known-good Chapter 6 code and the seeded code (v1 and v2) |
| `logs/fixed-*.log` | The full matrix on the fixed commit |
| `transcripts/` | Claude Code review (`stream-json`), the aborted Claude evidence session, and three Codex sessions (`--json` plus final messages). In the Claude transcripts, the init event's lists of installed plugins, skills and commands are replaced with counts. |

## How to reproduce

From `walker-jumpman-clawd` at `382f2ba`, with this course's `examples/` beside it:

```bash
git apply ../examples/06-shader-foundations/changes.diff
```

```bash
git apply ../examples/08-shader-verification/seeded-change.diff
```

Commit each step, then run the prompts in `PROMPTS.md`. To test an oracle both ways, keep a second copy with the Chapter 6 versions of `player.gd` and `clawd_flash.gdshader`.

## Results

| Check | Seeded commit | Fixed commit |
|---|---|---|
| `test_game` / `test_keyboard` / `test_clawd` @60 | pass | pass |
| `SHADER ERROR` lines | 0 | 0 |
| `verify_flash.gd` @30 / @60 / @144 | FAIL / PASS / FAIL | PASS / PASS / PASS |
| `test_flash.gd` (implementation-coupled) | FAIL at every rate | PASS |
| `verify_flash_spec.gd` v2 @30 / @60 / @144 | FAIL (0.515) / PASS (0.0303) / FAIL (0.569) | PASS / PASS / PASS |
| `test_flash_bench.gd` | PASS (it cannot see the shader bug) | PASS |

The oracle checked against known-good Chapter 6 code:

- v1 tolerance `max(delta, tick) / 0.55`: PASS @30 and @60, **FAIL @144** (0.0369 > 0.0303);
- v2 tolerance `(delta + tick) / 0.55`: PASS at all three rates.

## Human checks not performed

- The bench screenshots on the seeded and fixed commits.
- Pixel samples compared with `flash_model.gd`'s table.
- The fade seen at a high refresh rate.

See Chapter 8, *Use It*.

## Incident

The Claude Code evidence session (14:47–14:48) stopped after nine read-only tool calls without a result. It had been started with a shell `&` from a tool call that then exited. By the time it was retried, the Claude account had reached its session limit (`resets 6:40pm (America/New_York)`). The evidence and fix sessions ran on Codex.
