# SOURCES.md — tools, versions, references, AI contribution

## Tools and versions

| Tool | Version | Notes |
|---|---|---|
| Blender | **5.4.0 Alpha**, build hash 754ebe3c4b4e (`blender-5.4.0-alpha+main.754ebe3c4b4e-windows.amd64-release`) | **The course uses 5.1.2.** Everything here was done in the 5.4 Alpha. No 5.4-specific API was knowingly used, but nothing was tested in 5.1.2. The UI language was Simplified Chinese. |
| Blender MCP add-on (`blender_mcp.py`) | 1.8, protocol 13 (from `get_addon_status`) | Listens on localhost:9876. Asset libraries and 3D generators reported **off**, telemetry consent false. |
| MCP server `mcp-for-blender` | 2.1.9 (the version `uvx` resolved on 2026-10-12) | Registered with `claude mcp add -s user blender -e DISABLE_TELEMETRY=true -- uvx mcp-for-blender` |
| Claude Code | 2.1.295, Claude desktop app (Code tab), Windows | — |
| Claude model | Claude Opus 5.5 (`claude-opus-5-5`) | — |
| Godot | 4.7.2.stable.official.ed1daf0bf | Console build for the headless import, check and capture runs |
| uv | 0.12.9 | Runs the MCP server |
| OS | Windows 11 Home China 10.0.22631 | — |

**MCP tools used:** `get_addon_status`, `get_scene_info`, `execute_blender_code` and `look`.
**Not used** (assignment rule): `generate_3d`, `search_assets` and `import_asset`. No Poly Haven, Sketchfab, Poly Pizza, Hyper3D, Hunyuan3D or Tripo.

## Third-party assets

None. All geometry was built from Blender's own primitives (cube, plane, icosphere) by the scripts in `tools/blender/`. All materials are single flat colours.

## References consulted

The **game's own code and design note** is where every dimension comes from:
- `world/continuous_world_map.gd`: `TIER`, `RAMP_RUN`, `RAMP_APRON`, `CLIFF_STEP`, `_corridor_width()` and `_link_height()`;
- `world/terrain_surface.gd`: the cliff split and the region colours;
- `地图场景改造.md`, section "立体分层与出口随机".

**Grim Dawn's approach**, researched at the author's request:
- *Grim Dawn Modding Guide* (Crate Entertainment, official PDF), "Terrain Tools": Plateau, Raise Plateau, Ramp, Brush and No Pathing tools. https://www.grimdawn.com/downloads/Grim%20Dawn%20Modding%20Guide.pdf
- Titan Quest developer blog #9, on heightmaps not representing overhangs or caves. https://gamebanshee.com/kucdp
- Titan Quest Wiki, World Editor (terrain vs grid levels). https://titanquest.fandom.com/wiki/World_Editor
- GamingTrend, Grim Dawn developer on fixed terrain with randomized setpieces. https://gamingtrend.com/news/grim-dawn-dev-talks-dynamic-level-design-more-rewards

These only informed the decision to treat the assets as dressing over terrain that keeps the collision. Nothing was copied from them. Claude also gave its own impressions of Grim Dawn's cliff rocks and ramps; it said in chat that these were unverified, and nothing in the brief depends on them.

## AI contribution

| Work | By |
|---|---|
| Asset concept: which three assets, and that they match the terraces | The author (the assignment prompt) |
| Design decisions (origins, one ramp per whole tier, overlay role, repos, `!a3/*.md` rule) | The author, choosing from options Claude laid out |
| CHANGE-BRIEF, revisions, TEST-REPORT, README, SOURCES, FRICTIONAL, SUBMISSION | Claude, approved by the author |
| BLENDER-NOTES, the six UI part descriptions | Dictated by the author in Chinese; Claude translated |
| Every Blender modelling step (22 `execute_blender_code` calls: 8 cliff, 7 ramp including one read-only check, 7 rubble; `tools/blender/build_*.py`) | Claude |
| Moving both kerbs 0.1 m outward, then saving | **The author, by hand in Blender** |
| Export, import, preview scene, `test_a3_assets.gd`, `capture_a3_preview.gd` | Claude |
| UI screenshots `user-00`, `user-01` | The author |
| Godot renders `claude-godot-preview-*` | Claude (capture script) |
| HUMAN CHECK in the Godot editor | The author |
