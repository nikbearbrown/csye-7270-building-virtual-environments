# Example record — Chapter 5, The GDD and Virtual Worlds

## Executive summary

**What this is.** The record of Chapter 5's hands-on task, run on September 27, 2026 on a scratch copy of `walker-3d-platformer` (Godot's 3D Platformer demo, renamed): a `/gdd reverse` pass that recovered a GDD from the code, our audit of that GDD, one human-role acceptance criterion for a new 3D interaction (a checkpoint pad), and the implementation and headless verification of that criterion.

**Why it exists.** The chapter reports what the agents did and what they got wrong. Every one of those statements can be checked against the files here.

**What we found.** The recovered GDD (4,777 words, 107 `[OBSERVED]` tags) was mostly right and contained nine wrong or unsupported claims, including the shoot key (it said F9; it is Ctrl) and a measurement cited to a file the agent never opened. The implementation was started by Claude Code, which was stopped by the shared account's usage limit after 43 turns and before any test ran; Codex reviewed the partial work and finished it in under three minutes. Codex strengthened the test and gave a wrong reason for one change (it said a ray hit the pad's own `Area3D`; by default rays ignore areas, which we checked). Our own run of the final checks: all six criteria pass, the input probe reports 4/4, the feature route reports 2 coins and an enemy hit, all exit 0. Our criterion itself had a gap: it let the implementation choose the respawn point that criterion 4 measures against. Nothing here is a human playtest, and no one opened the editor.

"We" in this record, and "author" in `author-prediction.md` and `AC-01-checkpoint-pad.md`, mean the AI agent that drafted Chapter 5 and ran this example, standing in for a student. Professor Bear has not reviewed it.

## Environment

| Item | Value |
|---|---|
| Date | 2026-09-27 |
| Machine | macOS, Apple M4 Pro |
| Godot | 4.7.2.stable.official.ed1daf0bf (regular build, GDScript) |
| Claude Code | 2.1.150; model in transcripts: `claude-sonnet-4-6` (account default) |
| Codex CLI | 0.153.4; model from local config: `gpt-5.6-sol`, reasoning effort low |
| Project source | `walker-3d-platformer` local adaptation of `godot-demo-projects/3d/platformer` at `a3b5c113112f77291d5f3d1360f33a882fdc52f7`; the only difference from upstream is `config/name` |
| Copied | `godot/` (without `.godot/` and `screenshots/`), the root `*.md` files, `.gitignore`, and `tests/input_probe.gd`, `tests/feature_route.gd`; no `evidence/` or `youtube/` |
| Scratch commits | `98fe40a` baseline · `3376f55` gdd skill installed · `dfcdfc2` reverse output · `9585d8e` AC-01 · `0f45ee6` implementation |

**The gdd skill that ran.** The Walker framework's public `main` (`10fedb8`, 2026-09-11) does not contain `gdd/`; it exists in the instructor's local working copy (September 18, untracked). We copied that `gdd/` folder into `.claude/skills/gdd` and filled its tokens with `scripts/render_dir.py` using `publish.sh`'s Claude values. SHA-256 of the key source files as run:

```text
5bc8ca52820ff5fc863050fbc8e53cff4350f0594f8937b469a11c0bd7cd3922  walker/gdd/SKILL.md
1dc8f25b4af424be25e14bae846906ba4c279b310eeb0885fb07020eaa82079e  walker/gdd/persona.md
84ac33f37165d179745fd20dcb1dd1dc8df4ef94dfc1e8fe05fee4edcc718a58  walker/gdd/commands.yaml
5c98175cf9ac87d136c454ff1590380f07249bb7cac9d44f1c38e0428b6589ea  walker/gdd/commands/reverse.md
dd80e89b94955e9698543448213c5f1fee69532c18b984eba80b0891a89c15ce  walker/gdd/commands/draft.md
f9f1c9f329520b23d2ceb9a2aa24b219c5d100fa52d73449002626a76da0de7c  walker/publish.sh (working copy)
9ec45445200012e81117b4ed86b8b81c0888a53513c1ca668e24a613d6587516  walker/scripts/render_dir.py
```

## Files

| Path | What it is |
|---|---|
| `PROMPTS.md` | Every prompt and command, in order, verbatim |
| `author-prediction.md` | Prediction written and timestamped before the implementation run |
| `AC-01-checkpoint-pad.md` | The acceptance criterion, committed before any implementation |
| `recovered-design/` | The `/gdd reverse` output exactly as the agent wrote it (unreviewed): `GDD.md`, `IMPLEMENTATION-MAP.md`, `decisions.md`, `DESIGN-STATUS.json`, `DECK.html`, `diagrams/*.svg` |
| `changes.diff` | `git diff` from the baseline to the final commit, excluding the vendored skill and the deck/diagrams (which are in `recovered-design/`) |
| `changes-implementation-only.diff` | `git diff 9585d8e 0f45ee6`: the pad, the `player.gd` change, the `game.tscn` edit, and the tests |
| `checkpoint/` | `checkpoint_pad.gd` and `checkpoint_pad.tscn` as finished |
| `tests/input_probe.gd`, `tests/feature_route.gd` | The project's two pre-existing probes (from the local `walker-3d-platformer`; not public elsewhere) |
| `tests/test_checkpoint.gd` | The final acceptance test (Claude Code's draft, revised by Codex) |
| `tests/test_checkpoint.claude-partial.gd` | Claude Code's test as it stood when the session was cut off, recovered from the transcript's Write call |
| `tests/floor_probe.gd` | The agent's read-only floor probe |
| `audit/keys.gd`, `audit/keys.log` | Our check of the integer key and joypad codes in `project.godot` |
| `audit/ray_default.gd`, `audit/ray_default.log` | Our check of Codex's "the ray hit the pad" claim |
| `logs/baseline-*.log` | Import and both probes before any change |
| `logs/verify-*.log` | Import, the acceptance test, and both probes, run by us after the implementation |
| `transcripts/claude-session-0-status.jsonl` | `/gdd status` (skill load check) |
| `transcripts/claude-session-1-reverse.jsonl` | `/gdd reverse --path godot silent` |
| `transcripts/claude-session-2-implement-interrupted.jsonl` | Prompt 2 under Claude Code, ending in the usage-limit message |
| `transcripts/codex-session-3-continue.jsonl`, `codex-session-3-final-message.md` | Prompt 3 under Codex |

**Transcript trimming.** As in Chapter 1's example (same `trim_transcript.py`): session-start hook events and the `init` event's listing of locally installed tools, MCP servers, plugins, and skills are removed; thinking-block signatures are removed; the final `result` event is reduced to its outcome fields; the scratch path is replaced with `<scratch>` and the home folder with `~/`. Every assistant message, tool call, and tool result is otherwise verbatim. All transcripts are under 1 MB.

## Results at a glance

| Run | Result |
|---|---|
| Baseline import / input probe / feature route | exit 0 / 4 of 4 true / `coins=2 enemy_hit=true` |
| `/gdd reverse` (Claude Code) | 48 turns, 20 min 10 s; 1 permission denial (`find -exec`) |
| Prompt 2 (Claude Code) | 43 turns, 23 min 26 s; 6 denials (5 `python3`, 1 `$PWD` command); stopped by "You've hit your session limit"; no test run |
| Prompt 3 (Codex) | 2 min 51 s, exit 0; three revisions to the partial work |
| Our verification: `test_checkpoint.gd` | 6 of 6 criteria pass, exit 0 (pad 4.0 m from start, reached in 64 frames, respawn within 0.088 m) |
| Our verification: input probe / feature route | 4 of 4 true / `coins=2 enemy_hit=true`, both exit 0 |

## How to reproduce

You need the upstream folder (`3d/platformer` at `a3b5c11`), the two probes in `tests/`, and a Walker copy that contains `gdd/`. Then follow Chapter 5's Build It section and `PROMPTS.md`. The agents' wording and code will differ; the criterion and the verification commands will not.

## What this record does not show

No one opened the Godot editor, looked at the pad, played the game, or listened to it. Visibility and meaning of the pad, the camera's behavior on respawn, touch and gamepad input, and any export are unverified. The recovered GDD's four gates are unsigned and should stay that way until a person reviews it. No commit or push was made to any public repository.
