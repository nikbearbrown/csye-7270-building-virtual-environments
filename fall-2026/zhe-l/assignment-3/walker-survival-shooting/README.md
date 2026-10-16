# walker-survival-shooting — Assignment 3

A third-person 3D extraction shooter. The player lives in a subway base, carries a rugged military tablet, goes out to fight monsters, and extracts. In this assignment (Assignment 3) the game got its first 3D assets, built by Claude Code from basic shapes in Blender through the Blender MCP and brought into Godot.

## Versions
| Tool | Version |
|---|---|
| Godot | 4.7.2-stable (Windows, Forward Plus, Jolt Physics, D3D12) |
| Blender | 5.2.2 LTS (Windows, portable build, Simplified Chinese interface) |
| MCP for Blender | server package `mcp-for-blender` 2.1.9 (according to the uv cache), Blender add-on 1.8; started with `uvx blender-mcp`, telemetry off (`DISABLE_TELEMETRY=true`). Asset libraries and generation services (Poly Haven, Sketchfab, Poly Pizza, Hyper3D, Hunyuan3D, Tripo) all switched off |
| Claude Code | Claude Opus 5.5 |
| Operating system | Windows 11 Home |

## What this assignment added
- **The three assignment assets** (each with a `.blend` and a `.glb` in `design/item_resource/<asset>/`):
  - Chair `chair`: the chair the character sits on in the start menu, 0.44 × 0.42 × 0.90 m, 6 shapes, 72 triangles.
  - Tablet `tablet`: the character's rugged military tablet, 0.242 × 0.162 × 0.028 m, 388 triangles (21 shapes, over the course limit; my decision to keep it).
  - Weapon crates: large crate `crate_long` (`big_box`, 1.0 × 0.5 × 0.4 m) and small crate `crate_cube` (`small_box`, a 0.5 m cube): buildable storage furniture with `open` / `close` animations, 88 triangles and 6 shapes each.
- **Extra project assets:** computer desk `computer_desk` (1.5 × 0.5 m) and L-shaped computer desk `computer_desk_l` (1.5 × 1.0 m), tied to the game's computer gameplay.
- **Furniture grid rule:** 1 cell = 0.1 m; furniture footprints are whole cells.
- **Build code:** `tools/blender/build_<asset>.py`, a verbatim record of every `execute_blender_code` body Claude ran (the few parts run as headless scripts say so in the file; local output paths were made relative).
- **Godot:** the assets copied into `godot/assets/` and placed in my subway-base scene `base.tscn`; a camera aimed at the assets, `a3_asset_camera`; the check script `godot/tests/a3_asset_check.gd`.
- **Documents:** CHANGE-BRIEF (revision of 2026-10-15), BLENDER-NOTES, TEST-REPORT, SOURCES, and `../FRICTIONAL.md`.

## How to open the scene
1. Open `godot/project.godot` in Godot 4.7.2.
2. Open `base.tscn`. The assets are by the back wall; from left to right: L-shaped desk, desk, chair, large crate (with the tablet floating beside it), small crate.
3. To view through the asset camera: select `a3_asset_camera` and tick **Current** (the default camera is `preview_camera`).

## How to run the check
```
godot --headless --path godot --import
godot --headless --path godot --script res://tests/a3_asset_check.gd --fixed-fps 60
```
On Windows use `Godot_v4.7.2-stable_win64_console.exe` in place of `godot`. When everything passes the last line is `ALL PASS: 0 failure(s)` and the exit code is 0; any failure gives exit code 1.
What it checks: each asset's size, lowest point, node scales, triangles, and the crate animations; and in `base.tscn`, whether the assets sit on the floor, fit the grid, and overlap each other. It **cannot** show whether the assets look right; that is my human check (see TEST-REPORT).

## Known limitations
- No character model yet, so the scale next to a person is not verified.
- The tablet has 21 shapes, over the course limit of 6 (my decision to keep it).
- An opening crate lid swings out behind its footprint; the chair is not a whole number of cells; the L-shaped desk is recorded as a 15 × 10 rectangle in my item spreadsheet.
- The small crate's right latch is 6 mm off compared with the left one.
- CHANGE-BRIEF was written after the chair and the tablet were made (the brief says so).
- Turn the MCP add-on off in Blender's preferences when it is not in use: its port has no authentication.

## Explainer film
To be added: film link, file name, SHA-256.
