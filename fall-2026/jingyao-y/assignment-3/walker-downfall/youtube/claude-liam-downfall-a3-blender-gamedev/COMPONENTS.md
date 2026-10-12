# COMPONENTS.md

Components this film explains. They are hashed in `gamedev-evidence.json` against a pristine clone of `ceada15` (`coldfish432/GodotGame`, local main).

| Component | Beats | What enters → what changes → what is seen | Trade-off |
|---|---|---|---|
| `terrace-dimensions` | B03 → B04 | `TIER` 2.2, `RAMP_RUN` 6.5, `RAMP_APRON` 2.0, half-width 3.4–5.6 → every asset's size → ramps and cliffs on the mine floor. | The terrain keeps the collision, so the assets carry none. |
| `cliff-wall-asset` | B05 → B06 | 8 MCP calls → 3 strata and a lip boulder; call 6 fixes the buried boulder → before/after `look` views. | Boxes read as strata only roughly, and the face points away from the game camera. |
| `rubble-asset` | B06 | 7 MCP calls → 3 icospheres; call 5 sinks the floating stone. | Sized by eye; it ended up 1.47 × 1.25 × 0.85, not about 1.5 × 1.5 × 0.9. |
| `ramp-asset` | B07 → B08, B09 → B10 | `top_z` → a cambered wedge at 18.7°, plus kerbs; **the author's hand edit** moves the kerbs outward → `look` views and the recorded read-back. | Width is fixed at 7.0; a wider corridor needs X scaling, which widens the kerbs. The crown is unreadable from the game camera. |
| `export-import` | B11 → B12 | `export_glb.py` (+Y up) and `.gdignore` → `.glb` in Godot at the right size and facing → the orbit. | Materials come out double-sided, so Godot never culls a back face. |
| `preview-scene` | B12, B15 → B16 | The sun's `Transform3D`, first written by columns → light from below → corrected by rows. | It is a test scene: the light and camera are not the game's lighting. |
| `asset-checks` | B13 → B14 | Imported meshes → bounds, transforms, triangles, colours, ramp direction and slope → 25 PASS. | Expected numbers partly come from Claude's own Blender measurements: a consistency check, not an independent one. |

Everything else in the snapshot is listed under `exclusions` with a reason.
