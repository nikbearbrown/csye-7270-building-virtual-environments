# SOURCES — claude-liam-walker-rudy-particles

Claude Code (Claude Opus 5.5) built this film and drafted this file, on 2026-11-07, at shuai-z's request ("接下来按照作业要求做影片", "next, make the film as the assignment asks").

## What the film shows

| Evidence | Source | Identity |
| --- | --- | --- |
| Godot source, every code excerpt | `assignment-6/game/` at `d0ed4152ba4c5dc88ac2d712dbdb5889b07c9f54` (game source unchanged since `d60fb037`) | per-file SHA-256 in `checks/game/gamedev-evidence.json` |
| The game in play | `capture/play-01.mp4`, Godot Movie Maker on an isolated copy with a film-only input driver (`capture/film_driver.gd`) | CAPTURE.md §1 |
| The frame strips | `captures/slash_sparks/` and `captures/run_dust/` in the assignment folder, Movie Maker runs of the two preview scenes, committed with each tuning round | CAPTURE.md §2; `TUNING.md` |
| The Visual Profiler and the paused frames | `evidence/use-it-code/`, recorded by Codex (OpenAI's coding agent) at shuai-z's request on 2026-11-06 | CAPTURE.md §3; that folder's `README.md` |
| Headless results, mutations and the cost table | the committed logs in `logs/` | TEST-REPORT.md, Steps 2, 3, 5, 7 |
| The intent blocks, the settings rows | `CHANGE-BRIEF.md` §§2–3 and its revisions | read by `tools/make_stills.py` |
| The process shader | `game/shaders/particles_generated.gdshader`, generated in the editor by shuai-z (`8b795772`) | TEST-REPORT.md, "The process shader" |
| Who did what, the mistakes caught, what is uncertain | `FRICTIONAL.md`, `TUNING.md`, `TEST-REPORT.md`, `CLAUDE.md` in the assignment folder | FACTCHECK.md |

Every still is composed by `tools/make_stills.py` from these files; it only crops, scales, places and labels. Strip crops are enlarged with nearest-neighbour. The enlarged replays in the gameplay beats are 16:9 regions of the same Movie Maker frames scaled with Lanczos, labelled `ENLARGED` on screen.

## Textures

Neither effect uses an image file. Every texture is a `GradientTexture2D` sub-resource defined inside the effect scenes (`game/effects/slash_sparks.tscn` lines 3–21, `game/effects/run_dust.tscn` lines 3–13), written by the scoped build sessions from the brief's settings. There is no texture asset, licence or generative model to credit for the effects. The game's own art, which the effects play over, dates from Assignment 2 and is not part of this assignment's change.

## Corrections made while building (DOUBLE-CHECK LAW)

- **The second goblin.** The first dry run of the film driver stood Rudy still for 4.5 s while the goblin walked away and back. The take was reordered so the cut comes when the goblin walks towards him; the windowed take then matched the final dry run frame for frame.
- **The game card first showed whole 4K frames**, where the sparks and the dust were too small to read; it now shows 1800 × 960 crops around Rudy, and says so.
- **Gameplay holds.** The first build held the last frame for 6–10 s in every gameplay beat, because the narration outlasted the footage. More real footage was added (1.0× context and labelled replays) instead of retiming anything; the holds are now 1.7–4.6 s, labelled.
- **An enlargement that cut off the trail.** B18's first replay enlarged the region around the screen centre, but at the level's left edge the camera cannot centre Rudy yet, so the trail behind him fell outside it; that replay now enlarges the left edge.
- **Chinese quotations rendered as boxes** on the first stills (the Inter font has no CJK glyphs); they now use Hiragino Sans GB from macOS for those runs only.
- **The r3 card misattributed a quotation**, and B15 and B12 had two imprecise lines; FACTCHECK.md, "Corrections made while building", lists all three.
- **After the first master** (`_qc/FILM-REVIEW.md`): Gate T stopped three code panels' footers at over 12 words; they were shortened. Claude's frame review then found the B13 card's notes overlapping its captions, and that card named the wrong commit for the r0 strip (`017e8a52` instead of `c69523ca`); both were fixed and the master compiled again.

## Tools used to make the film

| Tool | Version | Use |
| --- | --- | --- |
| Brutalist toolkit (`brutalist.art`), skill `godot-gamedev` + `walker` | checkout `a99b5323`; Remotion 4.0.535 as installed (the toolkit reported 4.0.541 as latest; it was not upgraded) | beat-sheet contract, Remotion scenes, Kokoro wrapper, compiler, gates, `./art godot-gamedev --check` |
| Kokoro-82M via kokoro-onnx, voice `am_onyx` ("Liam, in for Bear") | the toolkit's local model | all narration, free and local |
| Godot | 4.7.2.stable.official.ed1daf0bf | the Movie Maker capture on an isolated copy |
| FFmpeg, Python 3 with Pillow and NumPy | Homebrew | encoding, the stills, the per-beat mix |
| Fonts | the toolkit's Inter and PT Mono; macOS Hiragino Sans GB for Chinese quotations | the stills |

The adapted tools in `tools/` started as copies of the Assignment 5 film's (`assignment-5/youtube/claude-liam-walker-rudy-shaders/tools/`). No paid service, image generator or stock media was used. Nothing was uploaded or published by Claude.
