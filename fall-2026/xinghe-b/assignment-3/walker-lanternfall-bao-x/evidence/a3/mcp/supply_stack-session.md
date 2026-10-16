# Supply Stack — MCP build session, 2026-10-14

Route and safeguards as in `lantern_gate-session.md` (mcp-for-blender 2.1.9,
add-on 1.8, Blender 5.2.2 LTS; telemetry off; no generator, library or
trajectory call).

Approval before the first change: Bao chose "批准，开始建 Stack". For the barrel,
offered either the script route's floor-to-top cylinder or one sitting on the
lower crate, Bao chose "和旧版一样".

The code of every `execute_blender_code` call is in
`tools/blender/build_supply_stack.py`, verbatim and in order.

| # | Time (EDT) | Call | Result |
|---:|---|---|---|
| — | 11:59 | `get_scene_info` | live file `lantern_gate.blend`, 8 meshes |
| 1 | 11:59 | clear scene through `bpy.data`; metric, unit scale 1.0; 2 materials | open file had no unsaved changes; 0 objects; `CrateBrass`, `MarketTimber` |
| 2 | 11:59 | LowerCrate cube | `get_scene_info`: at (0, 0, 0.25), rot 0, **scale (0.6, 0.4, 0.25)**, size 1.2 × 0.8 × 0.5 |
| 3 | 12:00 | UpperCrate cube | at (−0.22, 0.05, 0.75), scale (0.36, 0.34, 0.25), size 0.72 × 0.68 × 0.5 |
| 4 | 12:00 | OilBarrel, 12-sided cylinder | at (0.32, 0, 0.55), scale 1, size 0.44 × 0.44 × 1.1 |
| 5 | 12:00 | apply rotation and scale to all 3 meshes | every rotation 0 and **scale (1, 1, 1)**; 0 non-manifold edges, 0 loose verts |
| 6 | 12:00 | measure, save `blender/a3/supply_stack.blend`, write build record | bounds **1.20 × 0.80 × 1.10 m**, min (−0.6, −0.4, 0.0); **3** primitives; **68** triangles; part locations recorded as the hand-edit baseline |
| — | 12:00 | `look`, material shading, front / back / three-quarter / below | `evidence/a3/mcp/supply_stack-look.png` |
| 7 | 12:01 | export | `supply_stack.glb`, 7,168 bytes, SHA-256 `399ac223…a904` |

## Afterwards

- Godot import exit 0; `test_a3_assets.gd` 17/17 PASS, including the four
  Supply Stack checks (1.2 × 1.1 × 0.8 in Godot, unit scale, 3 / 68, materials).
- Running the saved `build_supply_stack.py` headless in a scratch copy of the
  repository produced a byte-identical GLB.

## What the `look` showed, and what it cannot show

Seen (Claude): the two crates and the barrel read as separate pieces from the
front, back and three-quarter views. From below, the barrel's bottom cap lies
in the same plane as the crate's underside, and a faint circle shows through:
two coplanar faces flickering against each other (z-fighting). This follows
from keeping the barrel floor-to-top, as chosen; on the floor in Godot the
underside should be hidden, but that is for Bao's look from below to confirm.

Not verifiable here: how the brass and timber separate under the room's moon
and practical lights, and whether the stack reads as "supplies" at game-camera
distance.
