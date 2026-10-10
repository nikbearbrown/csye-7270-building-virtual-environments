# SOURCES — the film

`claude-liam-walker-lanternfall-bao-x-gamedev` · godot-gamedev skill with the walker modifier (brutalist.art toolkit, local clone).

## The game shown

- Repository: https://github.com/yanxlh/walker-lanternfall-bao-x · project folder `godot/`
- Source revision shown in the film: **8a6f9881e0e2858e523d22bb09f1a423695f04e1** (every code panel and every main/lose/props take). One comparison shot (B17, left) comes from **40102ab**, the build of Bao's first playtest, captured with the same driver.
- Engine: Godot 4.7.2.stable.official.ed1daf0bf (GL Compatibility), macOS 26, Apple M4 Pro.
- File inventory and hashes: `gamedev-evidence.json` (75 files: 72 explained, 3 excluded with reasons).

## Engine captures

| File | SHA-256 |
|---|---|
| `capture/take-main-seed11.avi` | `23f8f6d9aa4b868c1fa35ddd9f9ccacabcb37920dd8f78a0b050ed193fc630c7` |
| `capture/take-lose-seed3.avi` | `029ad163a853a96d0920c4fa60e531275d271f8ecfc6292cec67ae44fefe9551` |
| `capture/clean/take-lose-seed3.mov` (stale frames removed) | `fbcbc1f87f547b04dc7bf0062131e05123e3f7976f090e70333ff0abedd7000d` |
| `capture/take-props-seed11.avi` | `3fb120507b918761f0e20e46afcaf1c78f28de9b5e2cdf85dce8910718b43e1c` |
| `capture/take-before-40102ab-seed14.avi` | `60170d6a5fc35d4025c739ccf9a754d419310068b8a9e497727a78af3c959449` |

Method, seeds, dry runs and rejected takes: CAPTURE.md. The takes are not in git (size); the driver, scene, commands and logs that regenerate them are.

## Repository files shown on screen

All from this repository at the commit the film was built from (the game folder at 8a6f988):

- Design: `CONCEPT.md` (excerpt and pillars), `CHARACTER-SHEET.md` (rules, palette), `design/character/blockout-poses-x8.png`, `design/character/sheet-vs-game.png`.
- Generation: `gen/raw/ART-PC-01/ART-PC-01-20260929T202956Z-s11.png` (rejected first batch), `gen/accepted/ART-PC-01/ART-PC-01-20260929T210117Z-s11-walk_contact.png` (raw output used), the sidecars `gen/log/ART-PC-01/*.json` (prompts verbatim, settings, decisions), `gen/mappings/ART-PC-01.json`.
- Edits: stage images re-run with `gen/art_process.py` by `tools/asset_trace_stages.py` → `images/trace/` (last stage equal to `godot/assets/art/pc_sheet.png` frame 3).
- Sprites: `godot/assets/art/pc_sheet.png`, `godot/assets/art/env_stall.png`.
- Evidence: `evidence/playtest/2026-10-01-runs-A-B.md` (Bao's quotes), TEST-REPORT.md, FRICTIONAL.md (roles), SOURCES.md (models and revisions).
- Recorded test output: `capture/test-run-film-build-raw.txt` (fresh copy of 8a6f988).

## Models that made the game's assets (not the film)

FLUX.1-schnell @ 741f7c3 (Apache-2.0) · Stable Audio Open 1.0 @ f21265c (Stability AI Community License) · MusicGen-medium @ d3bd7b0 and MusicGen-melody @ 68d653a (CC-BY-NC-4.0 weights). Details: the repository's SOURCES.md.

## Film tooling

- Narration: Kokoro-82M (kokoro-onnx, Apache-2.0), voice `am_onyx`, run locally. "Liam, in for Bear" is a named stand-in voice, not a clone.
- Scenes: Remotion compositions from the toolkit — `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `GodotDesignBoard`, `GodotDevWorkbench` (labelled "Godot editor reconstruction"), `ClaudeVerdictArtifact`, `ClaudeTitleOutro` (stock jingle).
- Evidence beats: composed by `tools/compose.py` (PIL + ffmpeg) from the captures and files above; fonts EB Garamond, Inter, PT Mono (OFL, bundled with the toolkit) and Hiragino Sans GB (macOS system font) for Bao's words in Chinese.
- Loudness: the Kokoro narration (about −24.7 LUFS, spiky peaks) is normalised per beat with EBU R128 `loudnorm=I=-16:TP=-1.5:LRA=11` (result −17 to −19 LUFS; the Kokoro mp3s are kept, the beats use the levelled WAVs). The five game-sound-only beats get one constant gain of −5.5 dB — no compression or EQ, so their relative levels and the game's own mix are unchanged (−16 to −21 LUFS). The outro jingle is untouched. Measurements: `audio-levels.json` (tools/level_audio.py).
- Outro jingle: `logos/bear-brown/bear-brown-6.mp3` from the toolkit's @NikBearBrown pool, chosen with the same slug seed the outro card uses (character sum 4283, mod 6), played whole with 1 s of silence after it.
- No paid service, API key, stock footage, image search or upload was used.

## Upstream documentation consulted

None beyond the toolkit's own skill files (`godot-gamedev`, `ai-explainer`) and the project's documents.
