# Example 02 — Prompting game art: one generated image into a checked Godot asset

## Executive summary

**What this is.** The record behind Chapter 2's worked example, run on 2026-09-27. Two coding agents, directed from the command line, turned Professor Bear's AI-generated termite reference (TERM-REF-02, a Gemini image) into a Godot sprite asset in a scratch copy of `walker-jumpman-clawd`, then wired placeholder sounds to real game events.

**Why it matters.** Every test the agents wrote passed. Checks run outside the agents still found four defects: the enemy's collider fits only one of its three sprite variants; the sound test teleported the player, breaking its own "never set state" rule; the sound effects were imported as "detect loop" rather than "no loop"; and the starter's `.gitignore` kept the new `godot/audio/` folder out of Git, so a fresh clone could not load `main.tscn` while every existing test still passed (and `godot` exited 0 on a test it could not parse). A Codex revision fixed the last three. The collider problem is left as the chapter's exercise.

**What it does not show.** Whether the termite reads at game size, whether any collider is fair to the player, or how any sound sounds. No Godot window was opened; those are human checks. The sounds are synthesized test tones, not generated audio, and they do not count toward Assignment 2.

---

## Runs

| Run | Tool | Prompt | Result reported by the agent | What our own checks found |
|---|---|---|---|---|
| Baseline | — | — | — | Import clean; 25/25 mechanics, 9/9 keyboard, 1,950 animation checks / 0 failures (`logs/baseline-*.log`) |
| 1 | Claude Code 2.1.150, claude-sonnet-4-6 | `PROMPTS.md` run 1 (art) | 28/28 on its test; originals pass | Same numbers. Mutation (Linear filter) makes its test fail with exit 1 (`logs/mutation-filter-linear.log`). Collider 20 x 34 covers 77% of the black soldier's opaque pixels and cuts off 7 rows of abdomen; for the yellow soldier 458 of 680 collider pixels are empty (`logs/verify1-collider-vs-alpha.log`) |
| 2 | Claude Code 2.1.150, claude-sonnet-4-6 | run 2 (sound) | 13/13; reports `godot/audio/` ignored by `.gitignore:23: audio/` | Test sets `player.position` and calls `set_paused()`; effects `edit/loop_mode=0`; fresh clone: `main.tscn` loses its `AudioCues` script, `test_audio_cues.gd` fails to parse, exit code 0 (`logs/fresh-clone-*.log`). Real-scene driver: one cue per event, each one physics tick late (`logs/verify2-audio-real-scene.log`) |
| 3 | Codex CLI 0.153.4, gpt-5.6-sol | run 3 (revision) | 17/17; all others pass | Same numbers (`logs/verify3-*.log`). `git check-ignore` now names `!godot/audio/**`. Fresh clone imports, loads `main.tscn` without errors, passes everything (`logs/fresh-clone2-*.log`) |

Claude Code runs: run 1 took 53 turns (19 min), run 2 took 63 turns (22 min, 6 commands refused by the allow list). Codex run 3 took about 4.5 min. A further Claude Code run was refused with "You've hit your session limit"; that is why run 3 used Codex.

## Files

| Path | What it is |
|---|---|
| `PROVENANCE.md` | The provenance note written before the agent saw the image |
| `PROMPTS.md` | The three prompts and command lines, exactly as run |
| `changes.diff` | `git diff` baseline → final, excluding the existing tests' `evidence/*.json` receipts; binary files (PNG, WAV) appear as "Binary files differ" |
| `diffs/run*.diff`, `diffs/git-log.txt` | The same, split by run. Run 2's diff lacks `godot/audio/`: Git ignored it. Run 3's diff adds it |
| `scripts/agent/` | Files the agents wrote, final versions, plus `test_audio_cues.run2-claude.gd` (the version that set state) |
| `scripts/independent/` | Checks written outside the agent sessions: `verify_collider_vs_alpha.py`, `verify_audio_real_scene.gd`, `load_main.gd`, `analyze_reference.py`, `gridslice_check.py` |
| `scripts/probe/` | The Godot 4.7.2 probes behind the chapter's default-setting claims |
| `logs/` | Every headless run's output, paths replaced with `<scratch>` / `<home>`, colour codes stripped |
| `transcripts/` | The three agent sessions (see below) |

The PNG strip, WAV tones and the reference image are not stored here (course rule: no media in examples). `scripts/agent/cut_termites.py` and `make_test_tones.py` regenerate them; the reference is in the course repository at `fall-2026/nik-bear-brown/assignment-2/reference/termite-soldiers-pixel-02.jpg`.

**Transcripts are trimmed, and say so.** They are the `stream-json` (Claude Code) and `--json` (Codex) event streams with these changes only: base64 image data replaced by a placeholder; absolute machine paths replaced; session-start hook events dropped; the `init` event reduced to cwd, model, tools, permission mode and version (the machine's installed skills, plugins and memory paths removed); and Claude Code's `tool_use_result` fields dropped, because each duplicates a tool result already present in the message content.

## Reproduce

Tools: Godot 4.7.2 (regular, not .NET) on `PATH` as `godot`; Python 3 with Pillow, NumPy and SciPy (SciPy only for `analyze_reference.py`); Git; Claude Code or Codex.

```bash
git clone https://github.com/nikbearbrown/walker-jumpman-clawd.git
cd walker-jumpman-clawd
git checkout 382f2ba
mkdir -p source-art
curl -L -o source-art/TERM-REF-02.jpg https://raw.githubusercontent.com/nikbearbrown/csye-7270-building-virtual-environments/main/fall-2026/nik-bear-brown/assignment-2/reference/termite-soldiers-pixel-02.jpg
shasum -a 256 source-art/TERM-REF-02.jpg   # 69f812f079dfd4777855c229a1d8e225f7ffcc46c8dd18b9e1ce1259eb524718
cp <this folder>/PROVENANCE.md source-art/
git add -A && git commit -m "Baseline"
godot --headless --path godot --import
godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

Then run the prompts in `PROMPTS.md` in order, checking and committing after each. Agents are not deterministic: expect different code, and compare it with the same checks:

```bash
timeout 120 godot --headless --path godot --script res://tests/test_termite_art.gd --fixed-fps 60
python3 verify_collider_vs_alpha.py . --overlay overlay-8x.png
timeout 120 godot --headless --path godot --script "$PWD/verify_audio_real_scene.gd" --fixed-fps 60
git check-ignore -v godot/audio/audio_cues.gd
git clone . ../fresh-clone && godot --headless --path ../fresh-clone/godot --import
```

`timeout` is GNU coreutils (on macOS, Homebrew `coreutils`). `verify_collider_vs_alpha.py` assumes the strip is 144 x 48 with three 48 x 48 cells and reads the collider size from `termite.tscn`; adapt it if your agent chose a different layout.

To reproduce the probes, run `scripts/probe/make_probe_files.py` in an empty folder containing a minimal `project.godot` (`config_version=5`), then `godot --headless --path . --import` and each `probe*.gd` with `--script`. `probe3.gd` expects you to change `edit/loop_mode` in `s.wav.import` and reimport between runs (1 to 4).

## Human checks still open

- Does each soldier read at 48 px in the 640 x 360 view, next to Clawd? (`godot/art_lab/termite_lab.tscn`)
- Which collider is fair for which soldier, and should a top-down creature appear in a side-view level at all?
- Do the cues sound right when they fire, and does the (real, generated) music loop without a click?
