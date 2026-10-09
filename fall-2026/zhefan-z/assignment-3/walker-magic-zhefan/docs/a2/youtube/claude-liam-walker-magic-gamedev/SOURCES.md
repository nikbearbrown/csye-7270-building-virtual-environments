# SOURCES — walker-magic gamedev film

## Game evidence

| What | Source | Hash / revision |
|---|---|---|
| Game source shown | `walker-magic-zhefan` at `74c0443` (tree `c931ac05…1ad9`), read from a `git archive` snapshot | per-file sha256 in `gamedev-evidence.json` |
| Capture source | `5266946` (tree `93c13d4d…b6e2`); runtime files identical to 74c0443 | — |
| Takes run-01…run-04 | Godot 4.7.2 Movie Maker, scripted input, gate PASS; AVIs kept out of Git | sha256 in `CAPTURE.md` and `coverage.json` |
| Input logs | `capture/run-0N-inputs.jsonl` | tracked |
| Test output (B22) | `evidence/test_sound_triggers-74c0443.log`, re-run 2026-10-07 on a fresh import of the 74c0443 archive | tracked |
| Media provenance | `evidence/media-provenance.json` (every take interval, sample range and label time) | tracked |
| Images on cards | `design/character/generated/CHAR-IDLE-v1.jpg`, `assets/sprites/mage/mage_idle.png`, `design/checks/mage-palette-revision1-before-after.png`, `design/character/collision.png` | game repo |

Asset models, licenses and prompts for the game itself: the game's `SOURCES.md` (Gemini app / Gemini 3.8 Flash images with SynthID; Lyria music; Stable Audio Open 1.0 effects — **Powered by Stability AI**; "This Stability AI Model is licensed under the Stability AI Community License, Copyright © Stability AI Ltd. All Rights Reserved.").

## Film tools

| Tool | Use | License |
|---|---|---|
| Brutalist toolkit (`brutalist.art`): `godot-gamedev`, `walker`, compile/QC scripts, Remotion compositions (ClaudeComposerAsk, BrutalistHesitantWriter, GodotDesignBoard, GodotDevWorkbench, ClaudeVerdictArtifact, ClaudeTitleOutro) | Structure, cards, master, checks | course-provided |
| Kokoro-82M via kokoro-onnx, voice `am_onyx` | Narration, local | Apache-2.0 |
| Remotion 4 + Node 24 | Composition renders | Remotion license (course toolkit) |
| FFmpeg 9.0.2 (Gyan build) | Cuts, overlays, encode | GPL |
| Pillow | Cards and labels (`scripts/cards.py`) | HPND |
| Fonts: EB Garamond, Inter, PT Mono (bundled in the toolkit) | Cards | SIL OFL |

No generative image, video or music model was used to make the film; every visual is the game, its files, or a labelled card.
