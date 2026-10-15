# Lamp-oil Shrine — MCP build session, 2026-10-14

Route and safeguards as in `lantern_gate-session.md` (mcp-for-blender 2.1.9,
add-on 1.8, Blender 5.2.2 LTS; telemetry off; no generator, library or
trajectory call).

Approval before the first change: Bao chose "批准，开始建 Shrine".

The code of every `execute_blender_code` call is in
`tools/blender/build_oil_shrine.py`, verbatim and in order.

| # | Time (EDT) | Call | Result |
|---:|---|---|---|
| — | 12:02 | `get_scene_info` | live file `supply_stack.blend`, 3 meshes |
| 1 | 12:02 | clear scene through `bpy.data`; metric, unit scale 1.0; 3 materials | open file had no unsaved changes; 0 objects; `OilGlow`, `ShrineBrass`, `ShrineStone` |
| 2 | 12:03 | ShrineBase cube | `get_scene_info`: at (0, 0, 0.12), rot 0, **scale (0.4, 0.4, 0.12)**, size 0.8 × 0.8 × 0.25 |
| 3 | 12:03 | ShrineStem, 8-sided cylinder | at (0, 0, 0.6), scale 1, size 0.24 × 0.24 × 0.7 |
| 4 | 12:03 | OilGem, icosphere subdivision 1 | at (0, 0, 1.15), scale 1, size 0.54 × 0.51 × 0.6, 20 faces |
| 5 | 12:03 | apply rotation and scale to all 3 meshes | every rotation 0 and **scale (1, 1, 1)**; 0 non-manifold edges, 0 loose verts |
| 6 | 12:03 | measure, save `blender/a3/oil_shrine.blend`, write build record | bounds **0.80 × 0.80 × 1.45 m**, min (−0.4, −0.4, 0.0); **3** primitives; **60** triangles |
| — | 12:04 | `look`, material shading, front / back / three-quarter / below | `evidence/a3/mcp/oil_shrine-look.png` |
| 7 | 12:04 | export | `oil_shrine.glb`, 8,064 bytes, SHA-256 `9bdc5867…eb90` |

`get_scene_info` rounds to two decimals, so it lists the base centre as 0.12;
the code and the build record have 0.125.

## Afterwards

- Godot import exit 0; `test_a3_assets.gd` 17/17 PASS, including the four
  shrine checks and the three-asset room checks.
- Running the saved `build_oil_shrine.py` headless in a scratch copy of the
  repository produced a byte-identical GLB.

## What the `look` showed, and what it cannot show

Seen (Claude): plinth, stem and gem read as three stacked pieces from every
side; the gem's facets show; from below the plinth hides the stem and only
the gem's edge is visible.

Not verifiable here: whether the gem reads as glowing lamp oil in Godot, since
the Blender material preview shows the emission as flat pale orange with no
glow.

## After the build: hand edit (not an MCP call)

- 12:19 EDT: `blender/a3/oil_shrine.blend` saved after the mouse edit in
  Blender (`OilGem` rotated 20° about Z, Ctrl+A → Rotation). 12:20 EDT:
  `godot/a3/oil_shrine.glb` re-exported with File > Export (8,064 bytes,
  SHA-256 `e5fb2c65…3f07`). Recorded in commit `7fae834`; described in
  `BLENDER-NOTES.md`.
- 12:23 EDT, read-only `get_scene_info`: `OilGem` at (0, 0, 1.15), rotation 0,
  scale (1, 1, 1), size 0.52 × 0.54 × 0.6 (was 0.54 × 0.51 × 0.6).
- Comparing the two GLBs: the MCP export's gem vertices rotated 20.0° about
  Blender Z match the re-exported gem within 1.84e-8 m. The shrine's
  `build_oil_shrine.py` therefore no longer reproduces the committed GLB.
