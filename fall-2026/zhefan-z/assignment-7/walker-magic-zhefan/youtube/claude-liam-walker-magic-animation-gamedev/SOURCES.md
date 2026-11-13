# SOURCES — the Assignment 7 film

## Sources of truth

1. `CHANGE-BRIEF.md`, with its dated revisions (2026-11-10; 2026-11-12 ×2)
2. `TUNING.md` (first look; lunge and growl cancel; run r0, r1 reverted, r2 kept; visual upgrades r0 → r1)
3. `TEST-REPORT.md` (pin first, read-backs and structure, edges, mutations, earlier suites, two clocks, strips and play, human checks)
4. `FRICTIONAL.md` (predictions, the run-cycle struggle, other entries, contributions, still open)
5. `README.md` and `SOURCES.md` (Assignment 7)
6. the clips in the scene files: `features/player/player.tscn`, `features/wolf/wolf.tscn`, `effects/cave_lights.tscn`, `effects/embers.tscn`
7. the tests (`tests/test_pin_behaviour.gd`, `test_anim_edges.gd`, `test_clip_run.gd`, `test_clip_lunge.gd`, `test_clip_flicker.gd`, `test_anim_structure.gd`, `test_afterimage.gd`, `anim_checks.gd`) and their logs in `logs/` (including `logs/pin/*.json`, `logs/mutation-a7-*_60fps.log`, `logs/probe_growl_cancel_60fps.log`)
8. `captures/` (look/, lunge/game-r0/, run/game-r0, game-r1, game-r2-ticks, run/analysis/) and `captures/figures/`
9. `git log --oneline` of the assignment

All read at **f860fed** (game source and documents). Where a document disagreed with the logs or the tree, the film shows the logs (FACTCHECK.md, "Corrections").

## Media

| Media | Source | Hash |
|---|---|---|
| Gameplay (B03, B04, B05) and capture crops (B11, B13, B24, B25) | `capture/run-01`, made for this film: scripted input, real engine output, Movie Maker windowed at 60 fps, the game at f860fed on an isolated copy (CAPTURE.md) | archive `355e10a8…ee82`; per beat in `evidence/footage-provenance.json` and `evidence/media-provenance.json` |
| Fixture captures (B02, B08, B21, B22) | the author's committed captures, `captures/look`, `captures/lunge`, `captures/run` (capture harnesses and preview scenes that place the characters) | per file in `evidence/media-provenance.json` |
| Figures (B08, B16, B20, B21, B22) | `captures/figures/` (drawn from the logs by `tools/make_figures.py`) | per file in `evidence/media-provenance.json` |
| Sprites (B06, B09) | `assets/sprites/wolf/wolf_lunge.png` (A2, unchanged) and `assets/sprites/mage/mage_run_cycle_sheet.png` (Gemini, cleaned; SOURCES.md), from the snapshot | per file in `evidence/media-provenance.json` |
| Motion reference (B06, B09) | Eadweard Muybridge, *Animal Locomotion* (1887), plate 707 (dog galloping) and plate 60 (man running), public domain, from Wikimedia Commons; `design/a7/reference/` with its SOURCES.md | per file in `evidence/media-provenance.json` |
| Code and source views | verbatim from the snapshot of f860fed (checked equal to the working tree) | `gamedev-evidence.json` |
| Fonts | EB Garamond, Inter, PT Mono from the Brutalist toolkit (`runtime/fonts/`) | — |
| Voice | Kokoro `am_onyx`, local, free (Liam, in for Bear) | — |

No stock footage, no web images other than the two public-domain Muybridge plates already committed by the author, no game audio.

## Tools

Brutalist toolkit (`brutalist.art`, the same installation as the Assignment 6 film): `godot-gamedev` with the `walker` modifier; `generate_audio_kokoro.py`; Remotion compositions `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `GodotDevWorkbench`, `ClaudeVerdictArtifact`, `ClaudeTitleOutro` through `remotion_scenes.py` (via `scripts/remotion_win.py`); `art godot-gamedev --check`; `art final`. Godot 4.7.2-stable for the capture. FFmpeg 9.0.2. Pillow and NumPy for the cards and the torch measurement.
