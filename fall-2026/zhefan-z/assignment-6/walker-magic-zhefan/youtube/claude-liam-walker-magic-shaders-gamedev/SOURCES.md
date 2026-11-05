# SOURCES — walker-magic Assignment 5 gamedev film

## Source revision
Game source as of commit `40c42f5` (`40c42f52b7be9964283057ff778b32714fa06340`) on branch `zhefan-z/assignment-5`; `walker-magic-zhefan` tree `5a45001be6a8c3dbacab531256c0271869383e97`. Excerpts and hashes come from a `git archive` snapshot of that tree (`gamedev-evidence.json`), checked identical to the working tree for every excerpt. Later commits (`d4bf271`, `05316ed`) added documents only, and `walker-magic-zhefan/assets/textures/rock_01/ATTRIBUTION.md`; no game source changed.

## Engine images
Every image of the game is one of the author's in-engine captures, unchanged, in `fall-2026/zhefan-z/assignment-5/captures/` (committed in `40c42f5`): 640×360 PNGs read from the rendered frame by the F9–F12 capture scenes (`tests/capture/`, `f4123db`) in real windowed runs, Forward+ on Vulkan 1.4.312 (TEST-REPORT.md). They are scripted captures: the key press is the author's, the values are set by the capture script. The film crops and enlarges them (factor stated on each card); their SHA-256 hashes are in `evidence/media-provenance.json`. No footage, no new capture, no screenshot of the editor; nothing reconstructed is presented as a screenshot.

## Recorded results
Figures on the test cards (B07, B15, B23, B24) are as recorded in TEST-REPORT.md and its logs (`logs/test_hurt_tint_*fps.log`, `logs/test_materials_60fps.log`, `logs/calibrate_normal_check_60fps.log`, `logs/mutation-*_60fps.log`). No test was re-run for this film.

## Documents the narration draws on
In order of precedence: `CHANGE-BRIEF.md` (with its revisions), `TEST-REPORT.md`, `LANGUAGE-NOTES.md`, `walker-magic-zhefan/MATERIALS.md`, `FRICTIONAL.md`, `SOURCES.md`, the three shaders in `walker-magic-zhefan/shaders/`, `features/player/hurt_tint_driver.gd`, and `captures/*.png`, `*.json`. Also `README.md` (known limitations). FACTCHECK.md maps each sentence and records two discrepancies between sources.

## Texture
Poly Haven "Rock 01", https://polyhaven.com/a/rock_01, Rob Tuytel, CC0 (SOURCES.md; CHANGE-BRIEF.md §4).

## Translations
The Chinese comments in `rock_frost.gdshader` (lines 3, 9, 31, 32, 34) are translated on screen by Claude Code for this film and labelled so. The author's observations quoted from TEST-REPORT.md were already translated there.

## Tools
Brutalist (`E:\7270\brutalist.art`, commit `29ba0e8`, the same installation as the Assignment 3 film, with its one uncommitted local change `runtime/remotion/package-lock.json`): `godot-gamedev` + `walker`, Remotion compositions `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `GodotDevWorkbench`, `ClaudeVerdictArtifact`, `ClaudeTitleOutro`. Kokoro-82M `am_onyx` (local). Pillow cards in the Claude palette (EB Garamond, Inter, PT Mono from the toolkit). FFmpeg 9.0.2. Node for Remotion. No paid service, no generated media, no captions. Nothing published.
