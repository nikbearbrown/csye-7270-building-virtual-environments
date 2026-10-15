# SOURCES — claude-liam-walker-rudy-3d-props

## What the film shows

| Evidence | Source | Identity |
| --- | --- | --- |
| Godot source, every code excerpt | `assignment-3/godot/` at `f6f8acf09b1c8e737caa1de08db60f61e28c2a2e` | per-file SHA-256 in `gamedev-evidence.json` |
| The running scene | `capture/orbit-01.mp4`, Godot Movie Maker on an isolated copy with a film-only camera driver | CAPTURE.md §1 |
| Headless numbers, pass and diagnostic fail | `capture/checks-pass.log`, `capture/checks-fail-diagnostic.log` → `stills/headless-numbers.png`, `stills/fail-diagnostic.png` | CAPTURE.md §2 |
| Blender viewport images | `blender-looks/`, the MCP `look` tool's images (Claude's captures), one of them made for this film from the saved hand-edit file | CAPTURE.md §3 |
| shuai-z's own Blender screenshots | `assignment-3/evidence/blender-notes-cube-selected.png`, `evidence/mcp-panel-connected.png` → `stills/blender-own.png` | |
| The prompt and the code it produced | the session transcript (prompt, 20:14 EDT); `assignment-3/tools/blender/build_waystone.py` lines 301–311 → `stills/prompt-code.png` | PROMPTS.md |
| The 2D art, at one scale | `assignment-2/game/content/rudy/frames/CHAR-IDLE.png`, `content/level_1/art/ENV-SPIKES.png`, `ENV-WAYSTONE-LIT.png`, `ENV-PORTAL.png` (generated in Assignment 2 by Gemini, as recorded there) → `stills/game-props.png` | |
| The brief, the revision cycle, the human check, what Claude got wrong | `assignment-3/CHANGE-BRIEF.md`, `FRICTIONAL.md`, `TEST-REPORT.md`, `SOURCES.md` | FACTCHECK.md |

Every still is composed by `tools/make_stills.py` from these files; it only crops, scales, places and labels.

## Corrections made while writing (DOUBLE-CHECK LAW)

- **"46 checks"** in TEST-REPORT.md and FRICTIONAL.md: the recorded log has 44 `ok` lines (12 + 12 + 11 + 9). The film says forty-four, counted from its own re-run; both documents were corrected to 44 at shuai-z's request.
- **The hand edit has no recording and no image of its own.** The film does not claim one: the before still is the 19:58 look image, the after still was captured for the film from the saved file, and the screen says so.
- **"Blender Dimensions"** in the headless-numbers still are the values read through the MCP by code (TEST-REPORT.md), not from a sidebar screenshot; the still says so.
- The student is named `shuai-z`, the course folder's name.

## Tools used to make the film

| Tool | Version | Use |
| --- | --- | --- |
| Brutalist toolkit (`brutalist.art`), skill `godot-gamedev` + `walker` | checkout `519fcbb` | beat-sheet contract, Remotion scenes, Kokoro wrapper, compiler, gates, `./art godot-gamedev --check` |
| Kokoro-82M via kokoro-onnx, voice `am_onyx` ("Liam, in for Bear") | the toolkit's local model | all narration, free and local |
| Remotion | the toolkit's `runtime/remotion` | bookends, editor reconstructions, figures, verdict, outro |
| Godot | 4.7.2.stable.official.ed1daf0bf | the Movie Maker capture and the check runs |
| Blender + MCP for Blender | 5.2.2 LTS · 2.1.9 / add-on 1.8 | one `look` call for the after-edit still (CAPTURE.md §3) |
| FFmpeg, Pillow, NumPy | local | encoding, chips, stills, the per-beat mix (`tools/build_reel.py`) |
| Claude Code, Claude Opus 5.5 | — | wrote the driver, the tools, the beat sheet and the narration; ran everything |

`GodotDevWorkbench` views are **reconstructions** of Godot's editor layout, labelled on screen; their code, paths and line numbers are verbatim. No paid service was used.

## Human / AI

- **shuai-z:** chose option (b) for the hand edit; everything the film reports as shuai-z's (the props, the brief's decisions, the hand edit, the rejections and choices, the human check) is from the project's own records.
- **Claude Code:** the film's structure, narration, stills, capture driver, scripts and documents; the check re-runs; the after-edit look capture.
- shuai-z uploaded the final export to the course Google Drive (README.md); the film is not published on YouTube or elsewhere.
