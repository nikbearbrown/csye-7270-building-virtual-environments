# COMPONENTS — walker-magic Assignment 3 gamedev film

Scope: what Assignment 3 added to `walker-magic-zhefan` at `8d8895c`. The Assignment 2 2D game in the same project is unchanged and explained in the Assignment 2 film (`docs/a2/youtube/claude-liam-walker-magic-gamedev/`); its files are listed as exclusions with that reason in `gamedev-evidence.json`.

| Component | Files | Beats | Code → result |
|---|---|---|---|
| **a3-blender-assets** — the Blender Python Claude Code ran through the MCP, the `.blend` sources, the `.glb` exports and their import settings | `tools/blender/build_rock.py`, `build_crystal.py`, `build_chest.py`, `export_crystal.py`, `rock.blend`, `crystal.blend`, `chest.blend`; `assets/models/{rock,crystal,chest}.glb` + `.import` | B05–B13 | source views B05→B06, B08→B09, B10→B11, B12→B13 (Blender Python, not Godot views) |
| **a3-prop-room** — floor, one light, a camera, WorldEnvironment, the three props at y = 0, the mage Sprite3D | `showcase3d/prop_room.tscn`; `assets/sprites/mage/mage_idle.png` + `.import` | B14–B16 | excerpt B15 (lines 37–44) → B16 (Movie Maker capture) |
| **a3-headless-check** — the size, upright, scale, triangle, colour and scene checks | `tests/test_a3_assets.gd` | B17–B18 | excerpt B17 (lines 78–90) → B18 (recorded output) |

**Why it was built this way, and one trade-off each**
- *Assets:* each part's turns baked into the mesh and its size taken from the real vertex bounds, so the fit factors are 1.000. Trade-off: the stones are sheared icosahedra, and the rock keeps a 0.066 m floor gap.
- *Prop room:* a Sprite3D with Y-billboard as the 1.45 m reference. Trade-off: a flat sprite always shows her front, even from behind.
- *Check:* brief values copied into the script. Trade-off: it would agree with a wrong copy, and it cannot judge looks, light or glow.

**One complete input → state → output trace:** the author's sidebar edit (input: Crystal_Short_B rotation Z = 20°) → `build_crystal.py` call 12 measures the crystal at 0.3228 m wide (state) → J1 lengthens that cone ×1.2125 (lines 472–478) → `crystal.glb` 0.35 × 0.6 × 0.35 m in the headless check (output, B18).

**Tests:** `test_a3_assets.gd` is headless; it proves bounds and settings of the imported files, not appearance (B18).
