# Lantern Gate — MCP build session, 2026-10-14

Route: Claude Code → `mcp-for-blender` 2.1.9 (add-on 1.8, protocol 13) → Bao's
running Blender 5.2.2 LTS (PID 42766, 127.0.0.1:9876). Telemetry consent
`false`; every asset library and generator `off`. No `generate_3d`,
`search_assets`, `import_asset` or `record_trajectory_feedback` call was made.

Approval before the first change: Bao chose "批准，开始建 Gate" for the
proposed plan, and "只是选择/视角，可以丢" for the unsaved `*` in the open
`supply_stack.blend` (a read-only comparison had shown its objects, meshes and
materials identical to the saved file).

The code of every `execute_blender_code` call is in
`tools/blender/build_lantern_gate.py`, verbatim and in order.

| # | Time (EDT) | Call | Result |
|---:|---|---|---|
| — | 11:53 | `get_scene_info` | live file still `supply_stack.blend`, 3 meshes, unchanged since 2026-10-13 |
| 1 | 11:53 | clear scene through `bpy.data`; metric, unit scale 1.0; 3 materials | 0 objects, 0 meshes; `AgedBrass`, `DarkWood`, `EmberGlass`; UI language `en_US` |
| 2 | 11:54 | GateBase cube | `get_scene_info`: at (0, 0, 0.09), rot 0, **scale (0.4, 0.4, 0.09)**, size 0.8 × 0.8 × 0.18 |
| 3 | 11:54 | GatePost, 8-sided cylinder | at (0, 0, 1.37), scale 1, size 0.24 × 0.24 × 2.37 |
| 4 | 11:54 | GateCrossArm cube | at (0, 0, 2.55), scale (0.6, 0.08, 0.08), size 1.2 × 0.16 × 0.16 |
| 5 | 11:55 | GateFinial cube | at (0, 0, 2.7), scale (0.08, 0.08, 0.15), size 0.16 × 0.16 × 0.3 |
| 6 | 11:55 | LeftLantern cube | at (−0.38, 0, 2.18), scale (0.22, 0.2, 0.24), size 0.44 × 0.4 × 0.48 |
| 7 | 11:55 | RightLantern cube | at (0.38, 0, 2.18), same size |
| 8 | 11:55 | BaseCollider-convcolonly, wire display | at (0, 0, 0.16), scale (0.4, 0.4, 0.16), size 0.8 × 0.8 × 0.32, no material |
| 9 | 11:55 | PostCollider-convcolonly, wire display | at (0, 0, 1.27), scale (0.21, 0.21, 1.27), size 0.42 × 0.42 × 2.55 |
| 10 | 11:56 | apply rotation and scale to all 8 meshes | `get_scene_info`: every rotation 0 and **scale (1, 1, 1)**; sizes unchanged; 0 non-manifold edges, 0 loose verts on every part |
| 11 | 11:56 | measure, save `blender/a3/lantern_gate.blend`, write build record | visual bounds **1.20 × 0.80 × 2.85 m**, min (−0.6, −0.4, 0.0); **6** visible primitives; **88** triangles |
| — | 11:56 | `look`, material shading, front / back / three-quarter / below | `evidence/a3/mcp/lantern_gate-look.png` |
| 12 | 11:56 | export (first attempt) | **failed**: `AssertionError: []`. The check read the exporter's `export_format` items, which are generated at run time and read back empty. Nothing was exported. |
| 13 | 11:56 | export without that check | `lantern_gate.glb`, 14,160 bytes, SHA-256 `2ac507f8…eea0`; 8 primitives exported, including both colliders |

## Afterwards

- Godot import exit 0; `test_lantern_gate.gd` 14/14 and `test_a3_assets.gd`
  17/17 PASS (11:57 EDT, from the suites' own UTC stamps).
- Running the saved `build_lantern_gate.py` headless in a scratch copy of the
  repository produced a byte-identical GLB (same SHA-256).

## What the `look` showed, and what it cannot show

Seen (Claude, from the four tiles): both lantern blocks stay separate from the
post from the front and from behind; the cross-arm and finial read as one
brass cross; the underside is the flat dark base.

Not verifiable here: how bright the EmberGlass emission looks in Godot's
lighting (Blender's material preview draws it as pale orange with no glow); how
the gate reads at game-camera distance; whether the collision margin feels
fair to a player. Those need Bao's look in the F4 room.
