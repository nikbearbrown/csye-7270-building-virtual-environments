# SOURCES — Assignment 3

## Tools and versions
| Tool | Version | Used for |
|---|---|---|
| Blender | 5.2.2 LTS (Windows) | Building the three assets |
| glTF 2.0 exporter (built into Blender) | 5.2.40 | `.glb` export, +Y Up on (the default in 5.2.2) |
| MCP for Blender (community project) | server 2.1.9, pinned; add-on 1.8 | Claude driving Blender. All three assets used the MCP route |
| uv / uvx | 0.11.19 | Running the MCP server |
| Godot | 4.7.2.stable.official.ed1daf0bf | 3D scene, import and headless check |
| Claude Code | 2.1.220, model Claude Opus 5.5 | Blender code, exports, Godot scene and check, git |
| Claude (claude.ai chat) | Claude Opus 5.5 | Planning, review of Claude Code's plans, document drafts |
| Brutalist godot-gamedev + walker | commit 29ba0e8 of E:\7270\brutalist.art, with one uncommitted local change (runtime/remotion/package-lock.json) | Explainer film |

## Remote services
All of the add-on's asset and generation services stayed off for the whole assignment, as `get_addon_status` reported each time: Poly Haven, Sketchfab, Poly Pizza, Hyper3D Rodin, Hunyuan3D, Tripo. No downloaded or AI-generated meshes are used; every mesh was built from Blender's basic shapes by code run through the MCP. Telemetry: off (`DISABLE_TELEMETRY=true` and add-on consent false).

## Colours
Rock colours #343539 and #797069 are sampled from my own Assignment 2 tile `assets/sprites/env/cave_ground_tile.png`. The crystal (#3558C8) and chest (#8A5A2B, #D4A73A) colours were proposed by Claude (claude.ai chat) to fit my Assignment 2 palette and approved by me.

## Starting point
My Assignment 2 project, walker-magic-zhefan, copied from branch `zhefan-z/assignment-2` at 946f1f1. Its existing sprites, sounds and music keep their provenance in `walker-magic-zhefan/SOURCES.md`. The prop room's mage sprite is `assets/sprites/mage/mage_idle.png` from that project.

## Human and AI contributions
- **Blender code:** written and run by Claude Code through the MCP; I approved each plan, asked for the rock revision and the gold change, made the hand edit on the crystal, and judged each asset in the viewport.
- **Godot scene and check:** written by Claude Code; I checked the scene myself in the editor and with F6, and asked for the background, floor and billboard fixes.
- **Film:** made with Brutalist godot-gamedev + walker (commit 29ba0e8, with the local change noted above) and local Kokoro narration (voice am_onyx, "Liam"); no paid media. Claude Code wrote the script, beat sheet, cards, capture and render; Claude in my claude.ai chat reviewed the script against my documents and suggested wording fixes; I approved the beat sheet and the fixes, provided my screenshots, and watched and listened to the final film.
- **Documents:** drafted by Claude (claude.ai chat) and Claude Code from the session records; the decisions, observations and my own statements (marked as translated from Chinese) are mine.

No collaborators.
