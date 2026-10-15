# SOURCES — Assignment 3, walker-rudy's three 3D props

Credits, tools, versions, and who did what. The dated record is [FRICTIONAL.md](FRICTIONAL.md); every command of the MCP setup is in [evidence/mcp-setup-log.md](evidence/mcp-setup-log.md).

## Starting point

- **My Assignment 2 game, walker-rudy** (course repository, `fall-2026/shuai-z/assignment-2/`, game at commit `9871718`). The three props are 3D versions of its Level 1 waystone, teleport circle and spikes. Their sizes come from the props' pixel sizes in that game, at Rudy = 160 px = 1.2 m; some of their colours come from its code (below). No file of that game is copied here.
- **The Godot project in `godot/` is new**, started on 2026-10-13. It holds only the 3D prop scene.
- **The geometry is my own, built with Claude in Blender** from Blender's basic shapes (cube, cylinder, cone). No downloaded model and no AI-generated mesh is used.
- **The build prompt** follows the assignment's adapted prompt (Walker's Game brief → Build → Playtest → Inspect → Revise → Export, `get_scene_info` first, one `execute_blender_code` call per object, no asset libraries or generators). In practice the prompts were my requests in Chinese in Claude Code, and Claude followed that workflow.

## People

- **Shuai Zhang (me):** the choice of props and the decisions in the brief; my hand edit in Blender; approving, rejecting and changing what Claude built; the steps in Blender's window; my look at the scene in Godot.
- No other collaborators. No one else has looked at the scene.

## Tools

| Tool | Version | Used for |
|---|---|---|
| Claude Code (desktop app), model Claude Opus 5.5 | Claude Code 2.1.296 | Planning; all the Blender code, run through the MCP; the export; the Godot project, scene builder, check and screenshot scripts; drafting the documents |
| Blender | 5.2.2 LTS | Building the three props; my hand edit; the `.blend` sources in `blender/` |
| MCP for Blender, server ([`ahujasid/mcp-for-blender`](https://github.com/ahujasid/mcp-for-blender), PyPI `mcp-for-blender`) | 2.1.9 | The MCP server Claude Code called: `get_addon_status`, `get_scene_info`, `execute_blender_code`, `look`. Registered with `claude mcp add blender -e DISABLE_TELEMETRY=true -- uvx mcp-for-blender`, local scope |
| MCP for Blender, Blender add-on (`blender_mcp.py`, "Interface: MCP for Blender") | 1.8; SHA-256 `eb0facf69781a30e69792532087d8d41c6a14fcd323353250abe7988ee297fa5` | The socket inside Blender, on `localhost:9876`. Poly Haven, Sketchfab, Poly Pizza, Hyper3D Rodin, Hunyuan3D and Tripo were all off throughout (`get_addon_status`), and telemetry consent was off. `generate_3d`, `search_assets` and `import_asset` were never called |
| uv / uvx | 0.10.2, from uv's standalone installer | Running the MCP server and installing the add-on |
| Blender's glTF 2.0 exporter (`io_scene_gltf2`) | 5.2.40 | Exporting `.glb` with +Y Up, run through `execute_blender_code` |
| Godot | 4.7.2.stable.official.ed1daf0bf, the standard build | The 3D scene, the import, the headless check and the screenshots |
| GNU coreutils `timeout` (Homebrew) | 9.12 | Stopping the headless check if it hangs |
| Python | 3.13.5 | One-off reading of the `.glb` files' JSON headers in the terminal, to check axes, transforms and colours before importing |
| Git | 2.51.0 | Version control |

**Not used:** the Blender Lab MCP connector in the Claude app (Blender Lab's `blender_mcp`, 1.0.1). I had it installed before this assignment and turned it off by hand; see FRICTIONAL.md. No paid service was used.

## Colour sources

| Colour | Hex (sRGB) | Source |
|---|---|---|
| Waystone rune, pale blue | `#99E0FF` | walker-rudy `game/content/level_1/waystone.gd`, `GLOW := Color(0.6, 0.88, 1.0)`, the lit rune's glow |
| Teleport circle gold | `#F0A830` | walker-rudy `game/content/level_1/portal.gd`, `LIGHT := Color("#F0A830")` |
| Teleport circle centre, pale gold | `#FFD76E` | walker-rudy `game/content/level_1/portal.gd`, `CORE := Color("#FFD76E")` |
| Stone grey, moss green, dark stone, wood brown, iron grey | `#8C8A80`, `#6E7F3C`, `#4A4440`, `#7A5838`, `#5C6168` | Proposed by Claude in the brief, to match the 2D art and its prompts ("weathered standing stone", "a little moss", "iron spikes set in a weathered wooden base"); accepted by me |
| Scene floor, sky and ambient light | `#8E9A5B`, `#9DB8CF`, `#FFF4E0` | Chosen by Claude in `godot/tools/build_props_room.gd`; not part of the props |

All materials are flat-colour Principled BSDF materials (roughness 0.9), with no textures.

## Human / AI contributions

| Part | Claude | Me |
|---|---|---|
| Choosing the props | Suggested the waystone, teleport circle and spikes from Level 1 | Chose them |
| CHANGE-BRIEF | Drafted revision 1 from the 2D game's pixel sizes and colours; drafted revisions 2 and 3 | Set Rudy = 1.2 m; accepted the depths and colours; chose the lit rune; asked for the changes in revision 2; agreed to revision 3 |
| MCP setup | Checked the package and the README; ran every command; found and fixed the `claude mcp add` argument order; read the add-on's defaults | Enabled the add-on in Blender; checked the panel; turned the other connector off |
| Blender code (`tools/blender/`) | Wrote and ran every `execute_blender_code` body, and measured each step | Approved each plan; moved the waystone's rune up by hand (G, Z); rejected the R; chose the ring, 12 sides and a thinner band; asked for more rune blocks and kept three when the shape limit came up |
| Export and Godot (`godot/`) | Wrote the export code, the project, the scene builder, the check and the screenshot script; tested that the check can fail; found and fixed bugs in the check and the screenshot script | Chose a separate project for the scene; opened it in Godot and judged how the props look |
| Documents | Drafted BLENDER-NOTES' screenshot caption, FRICTIONAL, TEST-REPORT, this file and the README from the conversation | Wrote BLENDER-NOTES' six descriptions; checked the drafts; gave my own observations in my words |
| Film | Structure, narration (Liam, local Kokoro `am_onyx`), stills, the camera-orbit capture, the check re-runs, the after-edit `look` capture and the film's documents, with the Brutalist `godot-gamedev` skill (details in `youtube/claude-liam-walker-rudy-3d-props/SOURCES.md`) | Chose to show the hand edit as before/after stills (option b); asked for the 46 → 44 correction; uploaded the final export to the course Google Drive |
