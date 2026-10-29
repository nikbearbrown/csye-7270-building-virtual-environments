# SOURCES — claude-liam-walker-rudy-shaders

Claude Code (Claude Opus 5.5) built this film and drafted this file, on 2026-10-28, at shuai-z's request ("接下来按照作业要求做影片", "next, make the film as the assignment requires").

## What the film shows

| Evidence | Source | Identity |
| --- | --- | --- |
| Godot source, every code excerpt | `assignment-5/game/` and `assignment-5/godot/` at `a2a3a77d50c5c9d8a65663d21898b7de54096604` | per-file SHA-256 in `checks/game/gamedev-evidence.json` and `checks/godot/gamedev-evidence.json` |
| The game in play | `capture/play-01.mp4` and its inset version, Godot Movie Maker on an isolated copy with a film-only input driver | CAPTURE.md §1 |
| The props scene running | `capture/stone-01.mp4`, Movie Maker on an isolated copy with a film-only camera driver | CAPTURE.md §2 |
| Controlled values, sweep, hint experiment, two materials, OS screenshot | the windowed captures in `evidence/use-it/` and their logs, made on 2026-10-27 | CAPTURE.md §3; TEST-REPORT.md §§4, 6–8, 12 |
| Headless results and mutations | the committed logs in `logs/` | TEST-REPORT.md §§1–3, 9–10 |
| The brief, the uniform table, the colour line | `CHANGE-BRIEF.md` §2 | read by `tools/make_stills.py` |
| The textures | `godot/assets/textures/rock_01/`: Rock 01 by Rob Tuytel, Poly Haven, CC0, https://polyhaven.com/a/rock_01 | `ATTRIBUTION.md` beside them |
| Who did what, the mistakes caught, what is uncertain | `SOURCES.md`, `FRICTIONAL.md`, `TEST-REPORT.md`, `CLAUDE.md` in the assignment folder | FACTCHECK.md |

Every still is composed by `tools/make_stills.py` from these files; it only crops, scales, places and labels. The 16-bit roughness map is shown scaled to 8 bits, not clipped.

## Corrections made while building (DOUBLE-CHECK LAW)

- **The hint predictions are not "by hand".** An early draft of B15 said so. Claude's script computed them (CHANGE-BRIEF.md header); shuai-z recomputed quad B's left band by hand afterwards (TEST-REPORT.md §4). The narration now says both.
- **The controlled values were set from code, not by hand.** B06's first draft said "by hand"; `capture_tint.gd` sets them.
- **The capture values are not an eye check.** The verdict first called the pixel matches "checked by eye"; they are measured from windowed captures by the tool. The verdict now separates the captures from the playtest.
- **"Glossier" is the material's intent.** B14 says the circle's material makes the disc glossier; B12 and TEST-REPORT.md §7 say roughness_offset barely shows under this light, and the film keeps both.
- **The respawn's jump** in the film's own take is from 0.041667 to 0.972222 (`capture/play-01-run.log`), not the test's 0.027778 or 0.055556; the narration uses the take's numbers.
- **The roughness map first rendered white** in the textures figure: PIL clipped its 16-bit values when converting to RGB. Fixed before the render.
- **Code ranges were narrowed to fit the editor view** after a pilot render cut off the last lines: `weathered_stone.gdshader` 3–13 (line 1, `shader_type spatial`, is named in the panel's footer; Gate T also had the two panels' footers shortened to 12 words or fewer), `hint_experiment.gdshader` 2–13, `invulnerable_tint_checks.gd` 347–354.

## Tools used to make the film

| Tool | Version | Use |
| --- | --- | --- |
| Brutalist toolkit (`brutalist.art`), skill `godot-gamedev` + `walker` | checkout `a99b5323`; Remotion dependencies reinstalled with `npm ci` from its own lock file (4.0.535) on 2026-10-28, because the installed `node_modules` predated its last update and lacked `@remotion/transitions` | beat-sheet contract, Remotion scenes, Kokoro wrapper, compiler, gates, `./art godot-gamedev --check` |
| Kokoro-82M via kokoro-onnx, voice `am_onyx` ("Liam, in for Bear") | the toolkit's local model | all narration, free and local |
| Godot | 4.7.2.stable.official.ed1daf0bf | Movie Maker captures on isolated copies |
| FFmpeg, Python 3 with Pillow and NumPy | Homebrew; Python 3.13.5, Pillow 10.4.0 | encoding, the inset, the stills, the per-beat mix |

No paid service, image generator or stock media was used. Nothing was uploaded or published by Claude. shuai-z uploaded the master to Google Drive on 2026-10-29 (https://drive.google.com/file/d/1Cx9urHkUlUhYBZ6EGtCq6PX-BPRnuqhX/view?usp=drive_link).
