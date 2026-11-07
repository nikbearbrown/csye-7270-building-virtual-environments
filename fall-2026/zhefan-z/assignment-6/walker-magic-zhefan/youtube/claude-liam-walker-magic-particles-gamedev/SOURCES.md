# SOURCES — the Assignment 6 film

## Sources of truth, in the order the author gave them

1. `CHANGE-BRIEF.md`, with its dated revisions (2026-11-05 ×3, 2026-11-06 ×2)
2. `TUNING.md` (r0, r0b, r1 for Effect A; r0, r1 for Effect B)
3. `TEST-REPORT.md` (machine checks, mutations, human checks, price, the process shader)
4. `FRICTIONAL.md` (entries 1–16, contributions, still open)
5. `SOURCES.md` and `walker-magic-zhefan/assets/textures/fx/ATTRIBUTION.md`
6. `walker-magic-zhefan/effects/` (the two effect scenes)
7. `walker-magic-zhefan/shaders/particles_generated.gdshader`
8. the tests and their logs in `logs/`
9. the strips in `captures/fireball_impact/` and `captures/fireball_trail/`

All read at **3c37fe0** (game source and documents). `CLAUDE.md` "Headless facts" is used for B06.

## Media

| Media | Source | Hash |
|---|---|---|
| Gameplay (B04, B13, B19; B02 frames 25 and 32) | `capture/run-01`, made for this film: scripted input, real engine output, Movie Maker windowed, the game at 3c37fe0 on an isolated copy (CAPTURE.md) | archive `81f20704…2e80`; per beat in `evidence/footage-provenance.json` |
| Strips (B09, B10, B12, B16, B18) | the author's committed fixture captures, `captures/` (Movie Maker, preview scenes, 640×360, 30 fps) | per file in `evidence/media-provenance.json` |
| Code and document views | verbatim from the snapshot of 3c37fe0 (checked equal to the working tree) | `gamedev-evidence.json` |
| Fonts | EB Garamond, Inter, PT Mono from the Brutalist toolkit (`runtime/fonts/`) | — |
| Voice | Kokoro `am_onyx`, local, free (Liam, in for Bear) | — |

No sourced or model-generated textures appear in the game or the film: `spark.png` and `smoke.png` are written by `tools/write_fx_textures.gd` (ATTRIBUTION.md). No stock footage, no web images, no game audio.

## Tools

Brutalist toolkit (`brutalist.art`, the same installation as the Assignment 5 film): `godot-gamedev` with the `walker` modifier; `generate_audio_kokoro.py`; Remotion compositions `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `GodotDevWorkbench`, `ClaudeVerdictArtifact`, `ClaudeTitleOutro` through `remotion_scenes.py` (via `scripts/remotion_win.py`); `art final`. Godot 4.7.2-stable for the capture. FFmpeg 9.0.2. Pillow for the cards.

## Corrections made while building (DOUBLE-CHECK)

- Narration first said the rapid casts were "one every point three five seconds"; the driver clicked every 11 frames (0.367 s), so the line now says "about every point three seven seconds, just over the cooldown".
- "A four-pixel texture" → "a four-by-four pixel texture" (`spark.png` is 4×4).
- The verdict first said "after one tuning step each"; Effect A had two steps, one of them a preview fix, so it says "after one change to each effect".
- B04's narration was reordered so "quarter speed" is said when the replay starts.
- Code excerpts B03, B08 and B15 were narrowed after the pilot render showed lines past the panel's end (the component does not scroll); the rest of those blocks is in labelled source notes.
