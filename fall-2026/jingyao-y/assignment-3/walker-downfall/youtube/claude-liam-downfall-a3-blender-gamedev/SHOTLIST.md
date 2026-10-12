# SHOTLIST.md

| Beat | Act | Visual | Source | Made by |
|---|---|---|---|---|
| B00 | ASK | ClaudeComposerAsk: reconstructed Walker prompt | Remotion | Claude |
| B01 | BLUF | Hesitant writer: "course" → "5.4 Alpha" | Remotion | Claude |
| B02 | SETUP | Assignment limits beside the terraced mine floor | `images/game-terrace-4k.png` (frame 52 of `capture/stills.avi`) | Claude (capture) |
| B03 | MECHANISM | `continuous_world_map.gd:61-66` | GodotDevWorkbench | Claude (reconstruction) |
| B04 | RESULT | Ramp foot (seed 1729), then below a cliff between terraces (seed 1333), game camera | `stills.avi` frames 28 and 98 (labelled holds) | Claude (capture) |
| B05 | MECHANISM | `build_cliff_wall_segment.py:95-107` (call 6) | GodotDevWorkbench | Claude (reconstruction) |
| B06 | RESULT | Blender `look` views: cliff and rubble, before and after | `images/blender-*-{before,after}.png` | Claude (MCP `look`) |
| B07 | MECHANISM | `build_arched_ramp_segment.py:47-51` (`top_z`) | GodotDevWorkbench | Claude (reconstruction) |
| B08 | RESULT | Blender `look` views of the ramp | `images/blender-ramp.png` | Claude (MCP `look`) |
| B09 | MECHANISM | `build_arched_ramp_segment.py:192-196` (the author's edit, comment) | GodotDevWorkbench | Claude (reconstruction) |
| B10 | RESULT | Recorded MCP output after the edit | Text panel of recorded output | Claude (recorded output); **edit by the author** |
| B11 | MECHANISM | `export_glb.py:24-33` | GodotDevWorkbench | Claude (reconstruction) |
| B12 | RESULT | Game camera, then one full orbit of the preview scene | `capture/orbit.avi` 1.34–18.00 s | Claude (Movie Maker) |
| B13 | MECHANISM | `test_a3_assets.gd:114-121` | GodotDevWorkbench | Claude (reconstruction) |
| B14 | RESULT | Recorded PASS lines from a fresh copy of ceada15 | `evidence/test_a3_assets-ceada15.log` | Claude (recorded output) |
| B15 | MECHANISM | `asset_preview.tscn:33-35` (the sun) | GodotDevWorkbench | Claude (reconstruction) |
| B16 | RESULT | Rubble close-up lit by the first basis, then the corrected one | `capture/light.avi` frames 50 and 110 (labelled holds) | Claude (Movie Maker re-render) |
| B17 | HUMAN | The author's Blender screenshot and one-line report | `images/user-01-blender-ui.png` | **The author** (screenshot) |
| B18 | VERDICT | Working / fixed / open / human | ClaudeVerdictArtifact | Claude |
| B19 | HANDOFF | "Your turn" prompt | ClaudeComposerAsk | Claude |
| B20 | OUTRO | Locked title outro | ClaudeTitleOutro | Claude |
