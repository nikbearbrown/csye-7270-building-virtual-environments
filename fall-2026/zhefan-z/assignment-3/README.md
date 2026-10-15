# Assignment 3 — Your First 3D Game Assets (walker-magic-zhefan)

CSYE 7270 · Fall 2026 · zhefan-z

This assignment adds three simple 3D assets to my semester game, walker-magic-zhefan, built by directing Claude through the Blender MCP in a running Blender, and shows them together in a small Godot 3D scene with my 1.45 m mage as a size reference. The game itself is still 2D; this scene is a separate 3D prop room, as the assignment allows, and the start of an HD-2D direction (2D pixel character in a 3D environment).

## Versions
- Godot 4.7.2.stable (Windows, Forward+)
- Blender 5.2.2 LTS, glTF exporter 5.2.40
- MCP for Blender: server 2.1.9 (pinned), add-on 1.8
- All three assets were built through the MCP route.

## What this assignment added
| Asset | Role in the game | Size (m) | Triangles |
|---|---|---|---|
| Rock | a roadblock the player jumps over | 1.0 × 0.8 × 0.7 | 60 |
| Crystal | a cold-blue glowing decoration | 0.35 × 0.35 × 0.6 | 30 |
| Treasure chest | the reward at the exit after a cleared level | 0.8 × 0.5 × 0.6 | 76 |

- `walker-magic-zhefan/assets/models/` — `rock.glb`, `crystal.glb`, `chest.glb` and their `.import` files
- `walker-magic-zhefan/tools/blender/` — the `.blend` sources and `build_*.py` (every `execute_blender_code` body, in run order), plus `export_crystal.py`
- `walker-magic-zhefan/showcase3d/prop_room.tscn` — floor, one light, a camera, the three assets side by side and the mage sprite
- `walker-magic-zhefan/tests/test_a3_assets.gd` — the headless check
- This folder: `CHANGE-BRIEF.md`, `BLENDER-NOTES.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, `SOURCES.md`

The Assignment 2 project was copied in unchanged from `zhefan-z/assignment-2` at 946f1f1; one file in the copy was later changed (mage_idle.png.import, in 1bacec8) to keep the 2D sprite lossless; its submission documents are archived in `walker-magic-zhefan/docs/a2/`.

## How to run the check (Windows, Git Bash, from `walker-magic-zhefan/`)
```
"E:/7270/godot/Godot_v4.7.2/Godot_v4.7.2-stable_win64_console.exe" --headless --path . --import
timeout 120 "E:/7270/godot/Godot_v4.7.2/Godot_v4.7.2-stable_win64_console.exe" --headless --path . --script res://tests/test_a3_assets.gd --fixed-fps 60
```
Expected: `A3 ASSET CHECK: 22 checks / 0 failures` and exit code 0. Replace the Godot path with your own.

## How to open the scene
Open `walker-magic-zhefan/` in Godot 4.7.2, then open `res://showcase3d/prop_room.tscn` and press F6. The game's main scene is unchanged (`res://game/main.tscn`).

## Known limitations
See TEST-REPORT.md. In short: the rock has a 0.066 m gap at the floor between its base stones; the chest lid is an 8-sided prism; the build scripts were not re-run on their own; the crystal was exported headlessly from its saved `.blend`; the prop room is not connected to the 2D game yet.

## Film
[final film link, filename and SHA-256 — added after rendering]
