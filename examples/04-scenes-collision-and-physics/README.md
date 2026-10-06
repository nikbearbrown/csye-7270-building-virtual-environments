# Worked example — Chapter 4: a shield pickup in walker-2d-dodge-the-creeps

## Executive summary

**What this is.** The complete record behind Chapter 4's hands-on. On 27 September 2026 the same prompt was given to Claude Code (2.1.150, `claude-sonnet-4-6`) and to Codex (0.153.4, `gpt-5.6-sol`), each working in its own scratch copy of `walker-2d-dodge-the-creeps` at baseline `03da9b0`. The task was to add a shield pickup as its own scene, on its own named physics layer, and prove it with a headless test that steps physics frames.

**Why look at it.** Every file is real. The diffs are what the agents wrote, and the transcripts are what they ran. The logs are the outputs of commands the reviewer ran afterwards, not the agents' reports.

**What it found.** Both agents handled the hard case correctly: when the shield ends while a creep still overlaps the player, the player is hit, because both re-check `get_overlapping_bodies()`. Both tests passed, and both still pass three times in a row under `--fixed-fps 60`. But when the shield was shortened from 3.0 s to 0.5 s on purpose, **Claude Code's own test still passed 7/7**. Its "within 10 physics frames" check starts counting after a fixed wait, not at expiry. The reviewer's 11-check script (`reviewer/verify_shield_timing.gd`) pins the hit at 181 physics ticks after collection, fails the mutant at 31 ticks, and passes both agents' real versions. Claude Code also hand-wrote engine identifiers (`uid://…`, `unique_id=123456789`). One was rejected by Godot at load time.

**What it does not show.** Anything visual. No run opened a window. The shield tint or ring, the pickup drawing, spawn fairness and feel are human checks.

---

## Contents

| Path | What it is |
|---|---|
| `PROMPTS.md` | The exact prompt and command lines |
| `starting-point/walker-adaptation.diff` | Upstream `2d/dodge_the_creeps` → Walker adaptation (title + one-line rotation fix). Apply with `patch -p1` inside the upstream folder |
| `starting-point/test_input.gd` | The Walker adaptation's 14-check harness (MIT, from `walker-2d-dodge-the-creeps/godot/`) |
| `claude/changes.diff` | Claude Code's full change against baseline `03da9b0`, new files included |
| `claude/test_shield.gd` | Its test (7 checks) |
| `claude/session.jsonl`, `claude/session.md` | Raw stream-json transcript (447 KB) and a readable excerpt |
| `codex/changes.diff`, `codex/test_shield.gd` | Codex's change and its test (6 checks) |
| `codex/session.jsonl`, `codex/last-message.md` | Codex's JSONL event stream and final message |
| `reviewer/verify_shield_timing.gd` | The human-written check: layer/mask contract, shield duration in physics ticks, a naturally spawned pickup |
| `logs/` | Every verification run quoted in the chapter (numbered; `MUTANT` in a name means the code was deliberately broken for that run and restored afterwards) |

`godot/test_input.gd.uid` appears in both diffs. The reviewer's baseline `--import` generated it. Neither agent wrote it.

## Reproduce

1. Get Godot's demo collection at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7` and copy `2d/dodge_the_creeps` to a new folder. Inside it:

```bash
patch -p1 < walker-adaptation.diff
```

2. Copy `starting-point/test_input.gd` into the folder. Put the project in a `godot/` subfolder, as the Walker layout does, then from the parent folder:

```bash
godot --headless --path godot --import
```

```bash
godot --headless --path godot --script res://test_input.gd --fixed-fps 60
```

Expect `RESULT failures=0`. Without the patch, expect 13/14, failing `horizontal movement resets orientation` (see `logs/02-upstream-demo-with-walker-harness.log`).

3. Apply an agent's change from a git repository of that folder:

```bash
git apply path/to/claude/changes.diff
```

4. Import again, so the new `.tscn` and script files register, then run the three checks:

```bash
godot --headless --path godot --import
```

```bash
godot --headless --path godot --script res://tests/test_shield.gd --fixed-fps 60
```

```bash
godot --headless --path godot --script /absolute/path/to/reviewer/verify_shield_timing.gd --fixed-fps 60
```

Expected for both agents' versions: `RESULT failures=0` and `SHIELD_TICKS … elapsed_ticks=181`.

## Results at a glance

| | Claude Code | Codex |
|---|---|---|
| Wall time | 16 min (33 turns) | about 2.5 min |
| Pickup layer / player mask | layer 3 (value 4) / 5 | layer 2 (value 2) / 3 |
| Shield timer | float countdown in `_physics_process` | one-shot `ShieldTimer` node |
| Expiry with overlap | `get_overlapping_bodies()` → hit | `get_overlapping_bodies()` → hit |
| Engine identifiers | invented `uid://` and `unique_id`; one rejected with a warning | omitted; Godot's import assigned them |
| Agent test, real code | 7/7 | 6/6 |
| Agent test, 0.5 s mutant | **7/7 (missed)** | 2 failures (caught) |
| Reviewer check, real code | 11/11, 181 ticks | 11/11, 181 ticks |
| Reviewer check, 0.5 s mutant | fails, 31 ticks | fails, 31 ticks |

Every result in this table comes from a run with `--fixed-fps 60` (logs `13`–`18` and `22`–`25`). Logs `10`–`12`, `20` and `21` are the same tests run without the flag, the way both agents ran them. They pass too.

Clean-clone note: running `test_shield.gd` in a fresh clone **before** `--import` printed 7 PASS lines and exited 0. The same log holds 55 `ERROR` lines for textures and audio that could not load (`logs/30-…`). After importing: zero errors.
