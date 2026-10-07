# SUBMISSION.md

| Field | Value |
|---|---|
| Assignment | Assignment 2 - Generate Art, Sound, and Music for Your Game |
| Student | Yuan Jingya (yuan.jingya@northeastern.edu) |
| Project name | `downfall-godot`. **It does not start with `walker-` as required.** The author chose to keep the existing repository. |
| Game concept in one sentence | A top-down extraction ARPG where Lappland fights down one-way floors and keeps deciding whether to push deeper or extract with her loot. |
| GitHub repository/folder URL | Assignment folder: https://github.com/nikbearbrown/csye-7270-building-virtual-environments/tree/Jingyao_Y/fall-2026/jingyao-y/assignment-2 (documents, design images, generated audio, film sources). The game source it describes is https://github.com/coldfish432/GodotGame at `100dce3`; the full game is not copied into the course repo. |
| Started from | The author's own earlier Downfall project (Unity prototype → Godot port). Not walker-jumpman, not Assignment 1. |
| Submitted commit SHA | Course repo branch `Jingyao_Y`: **see the Canvas submission note**, since this file cannot name the commit that contains it. Game repo: `coldfish432/GodotGame` `main` at `100dce3`. |
| Source revision shown in the film | `111bf6e` (local tag `a2-film-source`). GitHub's `100dce3` contains **byte-identical game files**: `git diff --stat a2-film-source 100dce3 -- . ':!*.md' ':!design' ':!youtube' ':!.gitignore'` is empty. It is the same game history rebuilt without the documents, so the hashes differ. |
| Godot version and OS | Godot 4.7.2.stable.official.ed1daf0bf, GL Compatibility, Windows 11 |
| Generative models used | See the table below. |
| Final film URL and filename | **To be added after upload.** Filename: `claude-liam-downfall-gamedev.mp4` (3840×2160, 30 fps, 6:23). It is kept out of GitHub per the course rule. |
| Final film SHA-256 | `144dbfe4412d5c2ed2e18e42c9d881dc126e31d2b264f101d7d502a1c59cc943` |

## Generative models used

| Model | How it was run | Terms | What it made |
|---|---|---|---|
| OpenAI gpt-image | Through the author's Codex agent ("Sol") | OpenAI Terms of Use | Every image |
| Google Gemini (music mode) | Gemini app | Google Generative AI terms | 2 music loops, 2 stings, 2 event sounds |
| Kokoro (`am_onyx`) | Local | Free, for the film's narration only | Narration |

Full details are in [SOURCES.md](SOURCES.md).

## Summary of my work

**Game.** A playable Godot 4.7.2 extraction ARPG: three regions, the Rhodes base, real-time combo/dodge combat, telegraphed enemies, relics, loot, insurance and saves.

**Art (gpt-image, reduced to pixel art by scripts).**

| Asset | State |
|---|---|
| Lappland | 7 distinct states, 8-direction facing |
| Field | Three region surfaces and prop groups |
| Enemies | Generated |
| Equipment icons | 51 |
| Relic icons | 96 |
| Rhodes base | Generated |

**Audio (Gemini).**

- A base loop and a field loop, each with a logged loop point.
- A fail sting and an extract sting.
- Two warehouse event sounds (lights on, lights off). Two more warehouse events (hatch, shelf) are wired and counted but silent.
- Pause freezes the field music; the base music ducks.
- A mute switch in Settings.

**Tests.** `tests/test_audio.gd` (26 checks) counts one sound per event and checks the loop points, pause, stings and mute. On a fresh `git clone` of `111bf6e`, every test suite passes, headless and windowed.

**Defects found by the fresh-copy run and fixed:**

1. The suites needed a `../evidence` folder that a clone does not have (`f770e26`).
2. An ignore rule had kept all the music out of git (`111bf6e`).

**Film.** A Brutalist godot-gamedev film, walker mode, 6:23 at 4K (`youtube/claude-liam-downfall-gamedev/`).

- Real 4K gameplay captures, scripted input.
- Two labelled segments with the slice's own audio and no narration.
- One asset traced from brief to engine.
- The `.gitignore` cause-and-effect.
- The test evidence.
- A verdict.
- `verify_gamedev.py` passes, and Gate V is clean.

## Known limitations

- **Rights:** uses the Arknights IP (character, setting, relic names) and fed official PRTS images to the image model as references.
- **Design order:** most art was generated before the design documents existed. The documents are retrospective and say so.
- **Character sheet:** 7 distinct poses, not 10. No turnaround.
- **Event sounds:** the hatch and shelf sounds were not generated.
- **Mute:** no separate music/SFX toggles; the buses exist but share one mute.
- **Human playtest:** none recorded yet, with sound on or muted.
- **Flaky capture:** `capture_v1` failed once on a random map and passed on reruns.
- **Reproducibility:** no seeds are recorded for the image generations, and some early prompts are lost.
- **Film outro:** silent; this pipeline's outro card has no jingle.
- **Repository name:** not a `walker-` repository.
