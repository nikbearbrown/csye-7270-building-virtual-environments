# Worked example — Chapter 9: a death burst and its cost in walker-2d-dodge-the-creeps

## Executive summary

**What this is.** The complete record behind Chapter 9's worked example, made on 27 September 2026. Claude Code added a one-shot `GPUParticles2D` death burst to a scratch copy of `walker-2d-dodge-the-creeps` and wrote a headless test for it; Codex then wrote a script measuring the CPU cost of particle simulation.

**Why look at it.** It shows three agent failures that a reader of the final diff would never see. In session 1 the agent could not run Godot (its allow list said `godot`; it called the absolute path) and printed an "expected output" table instead — two of its three predicted failures were wrong. In session 2 it ran the tests and blamed the one real failure on the headless renderer; the cause was a GDScript lambda that could not change an outer variable in its own test. Codex's benchmark reported 6.90 ms for every case because a headless Godot sleeps toward a 6.9 ms frame unless `--fixed-fps` is set.

**What it found.** The final burst passes 9 of 9 headless checks in real time (three runs), and the original 14-check harness still passes. With `--fixed-fps 60`, `CPUParticles2D` cost 0.035, 0.33 and 1.61 ms per frame at 1,000, 10,000 and 50,000 particles; `GPUParticles2D` cost the same as an empty scene, because the dummy renderer does no GPU work.

**What it does not show.** How the burst looks, whether it reads as a death, or what it costs a GPU. No one looked at a screen; every run was headless.

---

## Contents

| Path | What it is |
|---|---|
| `PROMPTS.md` | The four prompts, exactly as given, and every command line |
| `changes.diff` | Full change from the scratch baseline (`8adaa53`) to the final state (`518c313`), `.uid` files excluded |
| `by-session/session1.diff` | What session 1 wrote: the burst without texture or Disable Z, and the test with the lambda bug |
| `by-session/session2-3.diff` | Session 3's fix: `Dictionary` flag, `GradientTexture2D`, `particle_flag_disable_z`, two new checks |
| `by-session/codex.diff` | Codex's `tests/particle_cost.gd` |
| `tests/test_particles.gd` | The final 9-check burst test |
| `tests/particle_cost.gd` | Codex's cost script, unchanged |
| `tests/test_input.gd` | The Walker build's existing 14-check harness (needed to reproduce the baseline) |
| `walker-adaptation.diff` | The Walker build's changes against the upstream demo: the title, and one `player.gd` line |
| `sessions/claude-session{1,2,3}.md`, `codex-session1.md` | Readable transcripts (tool results trimmed, paths shortened) |
| `sessions/*.jsonl` | Raw transcripts. The Claude Code `init` event was reduced to model, working directory and permission mode (its tool, skill and plugin lists describe the instructor's machine); scratch paths shortened. Otherwise unedited |
| `logs/verify1-*.log` | Instructor's runs after session 1 (6/7 PASS; 14/14) |
| `logs/verify3-*.log` | Instructor's runs of the final state: three real-time runs of the burst test, one of the harness, and both again under `--fixed-fps 60` (assertions pass, audio objects leak at exit), plus the `--verbose` leak list |
| `logs/verify-particle_cost-*.log` | Codex's script run in real time (6.90 ms everywhere) and three times with `--fixed-fps 60` |
| `probes/` | The instructor's pre-task probes: what headless Godot 4.7.2 reports for particles (`probe.gd`), which properties each particle class has (`classes.gd`), whether the dummy renderer compiles particle shaders (`shader_probe*.gd`, `shaders/drift.gdshader`), and how particle time relates to wall time (`delta_probe.gd`), each with its log |

## How to reproduce

1. Clone `https://github.com/godotengine/godot-demo-projects` and check out `a3b5c113112f77291d5f3d1360f33a882fdc52f7`. Copy `2d/dodge_the_creeps` to a new folder as `godot/`.
2. Apply `walker-adaptation.diff` (or make its two edits by hand) and copy `tests/test_input.gd` to `godot/test_input.gd`. Commit this as your baseline.
3. `godot --headless --path godot --import`, then `godot --headless --path godot --script res://test_input.gd` — expect 14 PASS lines.
4. Give an agent the session 1 prompt from `PROMPTS.md`, or apply `changes.diff` to see the final state.
5. Run the three verification commands at the end of `PROMPTS.md`. The burst test and the harness should be run in real time; the cost script with `--fixed-fps 60`.

Engine: Godot 4.7.2 (regular, GDScript). Machine for the recorded numbers: Apple M4 Pro, 14 cores, macOS 26.5.1, load average 19–23 from other jobs during the cost runs. Your milliseconds will differ; the shape (linear CPU cost, flat GPU cost headless, 6.9 ms without `--fixed-fps`) should not.

## Licences

The game code is MIT (Godot Engine contributors; KidsCanCode 2017 for the game). Music: "House In a Forest Loop", HorrorPen, CC-BY 3.0. Images: Kenney, CC0. Font: Xolonium, SIL OFL 1.1. No asset files are included in this folder. The burst's texture is a `GradientTexture2D` defined in the scene file — no image asset. The tests, probes and diffs here were written by Claude Code, Codex and the instructor, as marked in the transcripts.
