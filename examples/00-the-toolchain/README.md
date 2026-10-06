# Worked example — Chapter 0: adding a score to walker-pong with Claude Code and Codex

## Executive summary

**What this is.** The complete record behind Chapter 0's worked example. On 27 September 2026 the same prompt was given to Claude Code and to Codex, each working in its own fresh clone of [`walker-pong`](https://github.com/nikbearbrown/walker-pong) (commit `c0cbc71`): add a two-player score and prove it with a headless test.

**Why look at it.** It is real. The diffs are what the agents wrote. The transcripts show what they actually ran, including the commands they were refused. The verification files are the outputs of commands the instructor ran afterwards. You can reproduce every number here.

**What it found.** Both agents delivered a working score with a passing test. Both ran the game's existing regression test without `--fixed-fps 60`, saw it fail, and misdiagnosed the cause. A twelve-run experiment on the untouched game shows the cause. The route counts frames while the game moves by seconds, so without a pinned time step the result depends on machine speed. With `--fixed-fps 60`, the original test passes with identical numbers on the untouched game and on both agents' versions.

**What it does not show.** Whether either score is readable or well placed. Nobody looked at a screen: every run here was headless.

---

## Contents

| Path | What it is |
|---|---|
| `PROMPTS.md` | The exact prompt and the exact command lines used |
| `claude/changes.diff` | Claude Code's full change against `c0cbc71` (new files included; its stray `evidence-run/` folder excluded) |
| `claude/score.gd`, `claude/score_check.gd` | Its new score script and test |
| `claude/session.md` | Readable transcript of the Claude Code session (hook/system events omitted; results trimmed; paths shortened) |
| `codex/changes.diff` | Codex's full change against `c0cbc71`, including its edits to README, GAME-BRIEF, GDD and FRICTIONAL |
| `codex/score.gd`, `codex/score_route.gd` | Its new score script and test |
| `codex/session.md` | Readable transcript of the Codex session (reasoning items omitted; output trimmed) |
| `revise/` | The Revise step: the `AGENTS.md` addition and the Codex re-run it produced |
| `verification/route-timing-experiment.sh` | The runner for the fixed-FPS vs real-time experiment |
| `verification/route-reports/*.json` | The route test's own JSON report for each of the twelve experiment runs, and for both agents' versions |
| `verification/verify-*-fixed.json` | The agents' score tests, re-run by the instructor with `--fixed-fps 60` |
| `verification/godot-4.7.2-help.txt` | `godot --help` on the machine used |

## Reproduce

From a fresh clone of `walker-pong`, with Godot 4.7.2 on your `PATH`:

```bash
godot --headless --path godot --import
```

```bash
mkdir -p evidence-local
```

```bash
WALKER_EVIDENCE_DIR="$PWD/evidence-local" godot --headless --path godot --fixed-fps 60 --script "$PWD/tests/input_route.gd"
```

Expected on 4.7.2: exit 0, `"passed":true`, counts Ceiling 5, Floor 4, Left 10, LeftWall 2, Right 8, RightWall 1, `max_speed` 185.67. Drop `--fixed-fps 60` and repeat a few times to see the flakiness for yourself. Each real-time run takes about 35 seconds.

To try an agent's version, apply its diff to a clean clone:

```bash
git apply path/to/claude/changes.diff
```

## Results at a glance

| | Claude Code | Codex |
|---|---|---|
| Time | 14 min | 5 min |
| New score test (instructor re-run, `--fixed-fps 60`) | pass | pass |
| Original route test (instructor re-run, `--fixed-fps 60`) | pass, identical to untouched game | pass, identical to untouched game |
| Ran the original test correctly itself | no | no |
| Its explanation of the failure | import cache / RNG, disproved by the experiment | called the run "deterministic", which it was not |
| Test reads the displayed label text | no | yes |

**Revise.** A `## Checks` section appended to `AGENTS.md` (in `revise/AGENTS-addition.md`) said how to import and how to run the route with `--fixed-fps 60`. With it, the same prompt to Codex ran the checks correctly and passed with the exact baseline numbers: 3.5 minutes, 9 commands. The instructor's re-run matched. Record: `revise/changes.diff`, `revise/session.md`, `revise/verify-*.json`.

## Provenance and limits

- Model identities are as the tools reported them: `claude -p` ran `claude-sonnet-4-6`; Codex ran `gpt-5.6-sol` at reasoning effort `low`, from the instructor's Codex configuration.
- The raw JSONL streams are not published. They contain local hook output and machine paths. The `session.md` files are generated from them and keep every assistant message and tool call in order.
- `walker-pong` is MIT-licensed, adapted from Godot's `2d/pong` demo. The agents' changes keep the license and attribution.
