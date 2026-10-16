# Sources — Walker Survival Shooting: First Props in Blender

## Game source shown
- **Revision:** `b370626` of the course repository, folder `fall-2026/zhe-l/assignment-3/walker-survival-shooting/`
  ("Add the Godot scene with the assets, the check script, the test report, README, and Blender notes; correct
  the latch-fix record").
- **Exported copies:** two `git archive b370626` exports: one is the checker's `--game` folder (never opened by
  Godot), the other the capture copy where `--import`, the check script and `capture/capture_driver.gd` ran.
- **Engine:** Godot v4.7.2.stable.official.ed1daf0bf (Windows 11, Forward Plus, D3D12, Jolt Physics).
- **Per-file hashes:** `gamedev-evidence.json` (every authored file under `godot/`) and
  `evidence/MANIFEST.sha256` (every figure, still, capture and input image used by the film).

## Media in the film and where each comes from

| Media | Origin | Label on screen |
|---|---|---|
| `inputs/own/blender-session-01.png` (= `design/blender-notes/blender-session-01.png` at b370626) | The designer's own screenshot of their Blender 5.2.2 session (Simplified Chinese interface) | "MY OWN SCREENSHOT", title bar cropped (it shows a local path), insets are enlargements of the same pixels |
| `inputs/look/*.png` (9 files, 2026-10-07 to 2026-10-15) | Captured by Claude Code through the MCP for Blender `look` tool from the designer's open Blender; saved by the designer from the session for this film | "viewport capture by Claude through the MCP look tool" |
| `capture/stills/*.png`, `media/B15.mp4` | Native 3840 × 2160 Godot renders of the unmodified `base.tscn` (see `CAPTURE.md`) | "Native Godot 4.7.2 render … film camera added by capture script" |
| `figures/*.png` | Built by `scripts/make_figures.py` only from the items above, the re-run log and text from the submitted docs | Each figure names its inputs |
| Godot editor views (B10, B12, B14, B16) | `GodotDevWorkbench` reconstruction with exact file lines (hash-checked) | "Godot editor reconstruction" by component design; path and line numbers shown |
| Prompts in B04, B05, B07 | SOURCES.md asset log rows PROP-TABLET-01 and CRATE-LONG-02 (English translations of the designer's Chinese) | "my prompt, translated from Chinese" |
| B07 code line | `tools/blender/build_crate_cube.py` lines 150–151 | Path and lines in the excerpt; spacing compressed |

## Tools and models used to make the film
| Tool | Use | Cost |
|---|---|---|
| Brutalist toolkit (`godot-gamedev` walker, `ai-explainer`, `riff`) | Beat sheet, Remotion scenes, compositor, checks | Free, local |
| Kokoro (`kokoro-onnx`, voice `am_onyx`, "Liam, in for Bear") | All narration | Free, local |
| Remotion | Rendering the scenes at 4K (`--scale=2`) | Free, local |
| FFmpeg / ffprobe | Encoding, probing, frame sampling | Free |
| Pillow | Figures | Free |
| Godot 4.7.2 | Headless check re-run and engine captures | Free |
| Claude Code (Claude Opus 5.5) | Wrote the beat sheet, narration, scripts and these documents from the submitted sources; ran every step | — |

No paid service, no image or video generation, no voice cloning. No music, no jingle, no game sound.

## Toolkit change made for this film
`runtime/remotion/src/scenes/GodotDesignBoard.tsx` gained an optional `excerptLabel` prop (default
`"GDD · DOCUMENT EXCERPT"`, so existing reels render unchanged). This film quotes the README, CHANGE-BRIEF,
TEST-REPORT and FRICTIONAL, which are not a GDD, so each board names its real source.

## Corrections
See `FACTCHECK.md` ("Corrections applied"), in particular 55 PASS instead of the submitted "56 PASS".
