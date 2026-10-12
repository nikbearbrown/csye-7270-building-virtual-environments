# Downfall — Assignment 3: first 3D assets with Claude, Blender MCP and Blender

**Author:** Yuan Jingya, with Claude Code (Claude Opus 5.5). **Date:** 2026-10-12.
**Game:** *Downfall*, a top-down extraction ARPG in Godot 4.7.2, project `downfall-godot`. Its field maps were just changed to three terrace levels with ramps and cliffs (`world/continuous_world_map.gd`). This assignment makes the first three Blender assets to dress those terraces.

## The three assets

| Asset | Size (m, Blender x × y × z) | Triangles | Primitives | Origin |
|---|---|---|---|---|
| `cliff_wall_segment` | 2.94 × 1.20 × 2.40 | 116 | 4 (3 cubes, 1 icosphere) | bottom, midpoint of the cliff's face line |
| `arched_ramp_segment` | 7.00 × 6.50 × 2.47 (rise 2.2, 18.7°) | 68 | 3 (1 plane, 2 cubes) | bottom, midpoint of the low-end edge |
| `cliff_rubble_pile` | 1.47 × 1.25 × 0.85 | 180 | 3 icospheres | bottom centre |

All three use flat-colour materials only: no textures, sculpting, rigging or animation. Every number traces to the game's `TIER = 2.2`, `RAMP_RUN = 6.5` and corridor half-width 3.4 — see [CHANGE-BRIEF.md](CHANGE-BRIEF.md). The assets are **visual dressing** laid on the game's terrain, which keeps the collision, as in Grim Dawn. They are shown in a preview scene and are **not yet placed by the map generator**.

## Where things are (paths relative to `downfall-godot/`)

| Path | What |
|---|---|
| `a3/CHANGE-BRIEF.md` | Predictions written before modelling, with appended revisions R1–R4 |
| `a3/TEST-REPORT.md` | Every check's actual result, four check → problem → fix loops, and the HUMAN CHECK |
| `a3/BLENDER-NOTES.md` | The author's first Blender session; the six UI parts were dictated by the author and translated by Claude |
| `a3/FRICTIONAL.md`, `a3/SOURCES.md`, `a3/SUBMISSION.md` | What went wrong, tools and versions, submission fields |
| `a3/screenshots/` | `user-*` were taken by the author; `claude-*` were rendered by Claude's capture script |
| `art/blender/*.blend` | One file per asset |
| `tools/blender/build_*.py` | Every `execute_blender_code` call, verbatim and in order, plus the author's manual edit noted where it happened |
| `tools/blender/export_glb.py` | Headless glTF (+Y up) export |
| `art/models/*.glb`, `asset_preview.tscn` | Imported assets and the preview scene: ground, sun, game-style camera, 1.7 m scale capsule |
| `tests/test_a3_assets.gd` | Headless check: bounds, node transforms, triangles, colours, ramp slope and direction |
| `tests/capture_a3_preview.gd` | Renders the preview scene to `a3/screenshots/claude-godot-preview-*.png` (needs a window) |

## Run the checks

```powershell
& 'Godot_v4.7.2-stable_win64_console.exe' --headless --path downfall-godot --import
& 'Godot_v4.7.2-stable_win64_console.exe' --headless --path downfall-godot --script res://tests/test_a3_assets.gd
```

Re-export a `.blend` after editing it:

```powershell
& 'blender.exe' -b --factory-startup downfall-godot/art/blender/arched_ramp_segment.blend --python downfall-godot/tools/blender/export_glb.py
```

## Who did what

- **The author** made the design decisions in chat:
  - origin placement, and one ramp segment per whole tier treated as a terrain overlay;
  - which repositories to use.

  They also did these by hand in Blender and Godot:
  - learned the viewport;
  - took the UI screenshots;
  - **moved both ramp kerbs 0.1 m outward and saved**;
  - did the HUMAN CHECK in the Godot editor.
- **Claude** drafted the brief, wrote and ran every Blender script through Blender MCP, exported and imported the assets, wrote the preview scene and the checks, and wrote these documents.
