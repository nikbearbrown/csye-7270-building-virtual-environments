# SOURCES — the Assignment 7 film

## Sources of truth

1. `CHANGE-BRIEF.md`, with its dated revisions (2026-11-10; 2026-11-12 ×3; 2026-11-13, "the brief in the published structure": the two clips, the sheet, the cycle spec, the phase table with "What the player may do / What the game reads", the state machine, two clocks, evidence split, short answers and "The four ideas"); and the author's dated note "2026-11-13 — note on the four ideas" (CHANGE-BRIEF.md:199–201), which is in the working tree after ad7935f and is quoted on B08 with that label
2. `TEST-REPORT.md` (baseline, pins, read-back, mutations, fresh cache, state machine, edges, strips, human checks, two clocks, "Claude against me", "What no headless run shows")
3. `TUNING.md` (first look; lunge and growl cancel; run r0, r1 reverted, r2 kept; visual upgrades r0 → r1)
4. `FRICTIONAL.md` (predictions, the run-cycle struggle and the next test, other entries including process slips, contributions, still open)
5. `README.md`, `SUBMISSION.md` and `SOURCES.md` (Assignment 7); `walker-magic-zhefan/assets/sprites/mage/ATTRIBUTION.md`
6. the clips in the scene files: `features/player/player.tscn`, `features/wolf/wolf.tscn`, `effects/cave_lights.tscn`
7. the tests and probes (`tests/test_pin_behaviour.gd`, `test_anim_edges.gd`, `test_clip_run.gd`, `test_clip_lunge.gd`, `test_clip_flicker.gd`, `test_anim_structure.gd`, `anim_checks.gd`, `probe_two_clocks.gd`) and their logs in `logs/` (including `logs/pin/*.json`, `logs/mutation-a7-M*_60fps.log`, `logs/mutation-a7-1…5-*_60fps.log`, `logs/probe_two_clocks_{30,60,144}fps.log`)
8. `captures/` (look/, lunge/game-r0/, run/game-r2-ticks/, run/analysis/) and `captures/figures/`
9. `git log --oneline` of the assignment

All read at **ad7935f** (game source and documents; the documents' lines on screen are read with `git show ad7935f:`). Where a document disagreed with the logs or the tree, the film shows the logs (FACTCHECK.md, "Corrections").

## Media

| Media | Source | Hash |
|---|---|---|
| Gameplay (B03–B07) and capture crops (B11, B13, B16) | `capture/run-02`, made for this film: scripted input, real engine output, Movie Maker windowed at 60 fps, the game at ad7935f on an isolated copy (CAPTURE.md) | archive `af3cb23b…d09e`; per beat in `evidence/footage-provenance.json` and `evidence/media-provenance.json` |
| Fixture captures (B02, B16, B23) | the author's committed captures, `captures/look`, `captures/lunge/game-r0`, `captures/run/analysis` (capture harnesses that place the characters) | per file in `evidence/media-provenance.json` |
| Figures (B19) | `captures/figures/pin_timeline.png` (drawn from the logs by `tools/make_figures.py`) | `evidence/media-provenance.json` |
| Sprite sheet (B09) | `assets/sprites/mage/mage_run_cycle_sheet.png` (Gemini app, model shown as "4 Hydrogen", 2026-11-12, prompt v3; cleaned by `tools/clean_run_cycle.py`; Google Terms of Service and Generative AI Additional Terms of Service; ATTRIBUTION.md), from the snapshot | `evidence/media-provenance.json` |
| Code, scene and document lines | verbatim from the snapshot of ad7935f (checked equal to the working tree) and from the documents at ad7935f (`git show`) | `gamedev-evidence.json` (workbench excerpts); `evidence/media-provenance.json` (cards) |
| Fonts | EB Garamond, Inter, PT Mono from the Brutalist toolkit (`runtime/fonts/`) | — |
| Voice | Kokoro `am_onyx`, local, free (Liam, in for Bear) | — |

No stock footage, no web images, no game audio.

## Tools

Brutalist toolkit (`brutalist.art`, the same installation as the Assignment 6 film): `godot-gamedev` with the `walker` modifier; `generate_audio_kokoro.py`; Remotion compositions `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `GodotDevWorkbench`, `ClaudeVerdictArtifact`, `ClaudeTitleOutro` through `remotion_scenes.py` (via `scripts/remotion_win.py`); `art godot-gamedev --check`; `art final`. Godot 4.7.2-stable for the capture. FFmpeg 9.0.2. Pillow and NumPy for the cards.
