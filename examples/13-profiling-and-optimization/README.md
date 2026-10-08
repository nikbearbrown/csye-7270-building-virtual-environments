# Worked example — Chapter 13: benchmarking nodes against servers in walker-2d-bullet-shower

## Executive summary

**What this is.** The complete record behind Chapter 13's worked example, made on 27 September 2026. Claude Code built a node-based version of the bullet field (the baseline), a parity test showing it behaves like the server-based original (the optimization), and a headless benchmark harness. The instructor then ran the harness ten times per configuration.

**Why look at it.** The agent's code is sound, but the path to it is instructive. In session 1 it could not run Godot (it used the app's absolute path; the allow list said `godot`), tried a sandbox-bypass flag, and then invoked a skill that edits permission settings — the instructor stopped it. In session 2 it fixed two bugs of its own making and ran everything, but described `Performance.TIME_PROCESS` as "last frame" when the engine source shows a one-second maximum — and its own numbers contradict its description. A hung test process it left behind kept the CLI session open for 20 minutes.

**What it found.** On the instructor's Mac (Apple M4 Pro), CPU time per simulated frame, median of ten runs under `--fixed-fps 60`: 500 bullets — nodes 0.331 ms, servers 0.167 ms; 2,000 — 2.845 vs 0.707 ms; 5,000 — 9.854 vs 2.314 ms. Server cost grows about linearly; node cost grows faster than linearly. Run-to-run spread on the shared machine was large (nodes at 5,000: 8.5–39.0 ms).

**What it does not show.** Any GPU or draw cost (headless, dummy renderer), real-time frame pacing, or any mobile or XR device. The decision in the chapter — not justified at the shipped 500 bullets, justified at thousands — rests on CPU numbers only.

---

## Contents

| Path | What it is |
|---|---|
| `PROMPTS.md` | The two prompts, exactly as given, and every command line |
| `changes.diff` | Full change from the scratch baseline (`1cc1478`) to the final commit (`e449968`), `.uid` files excluded. Includes the agent's 82-line `FRICTIONAL.md` entry, kept as written (its `TIME_PROCESS` definition is wrong) |
| `by-session/session1.diff`, `session2.diff` | What each session changed. Session 1 includes the `test_motion.gd` edit that session 2 reverted |
| `bench/` | The agent's `bench.gd`, `bullets_nodes.gd`, `shower_nodes.tscn`, `test_nodes_parity.gd`, and `run_bench.sh` (note its default Godot path is the macOS app path; pass your own) |
| `tests/` | The Walker build's three existing tests (`test_motion.gd`, `test_collision_input.gd`, `test_mouse_input.gd`), needed to reproduce the baseline |
| `walker-adaptation.diff` | The Walker build's changes against the upstream demo: the title and the `BODY_MODE_STATIC` line |
| `sessions/claude-session{1,2}.md` | Readable transcripts (tool results trimmed, paths shortened) |
| `sessions/claude-session{1,2}.jsonl` | Raw transcripts; the Claude Code `init` event reduced to model, working directory and permission mode; scratch paths shortened. Session 1 ends where it was stopped |
| `logs/` | The instructor's runs of the three existing tests and the parity test, in real time and under `--fixed-fps 60` |
| `verification/sweep.sh`, `summarize.py` | The instructor's repeated-measurement runner and summary |
| `verification/sweep1.csv`, `sweep2.csv`, `sweep-combined.csv` and `*-summary.csv` | Every run (5 + 5 per configuration) and the summaries used in the chapter |
| `verification/sweep*-load.txt` | Load averages at the start and end of each sweep |
| `probes/` | The instructor's probes of the `Performance` monitors in headless mode: zero before the first second, a one-second maximum after it, render monitors at zero, and frame pacing with no flag (about 144 FPS) and with `--max-fps 60` |

## How to reproduce

1. Clone `https://github.com/godotengine/godot-demo-projects`, check out `a3b5c113112f77291d5f3d1360f33a882fdc52f7`, and copy `2d/bullet_shower` to a new folder as `godot/`.
2. Apply `walker-adaptation.diff`; copy `tests/*.gd` into `godot/`. Commit.
3. `godot --headless --path godot --import`; then `godot --headless --path godot --script res://test_motion.gd` should print `ALIGNED_BODIES 500/500`.
4. Apply `changes.diff` (or give an agent the prompt in `PROMPTS.md`), import again, and run the verification commands at the end of `PROMPTS.md`. Always use `timeout`: a test that errors before `quit()` never exits.
5. `bash verification/sweep.sh . my-sweep.csv`, then `python3 verification/summarize.py my-sweep.csv`.

Your milliseconds will differ with your machine and its load. Record both. The shape — near-linear server cost, faster-than-linear node cost, a ratio of about 2× at 500 and about 4× at 2,000–5,000 on this machine — is what to compare.

## Licences

The demo code is MIT (Godot Engine contributors). `bullet.png` and the face images are part of the upstream demo and are not included here. The benchmark and parity scripts were written by Claude Code and verified by the instructor; the sweep scripts were written by the instructor.
