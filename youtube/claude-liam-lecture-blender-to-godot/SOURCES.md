# SOURCES.md

## The source
- `csye-7270-building-virtual-environments/chapters/03-blender-mcp-to-godot.md` — read in full 2026-10-06 (uncommitted course draft; errors in it found by the course's review pass were corrected in the same session before this film was written).
- Evidence record of the chapter's runs (2026-09-27): `csye-7270-building-virtual-environments/examples/03-blender-mcp-to-godot/` — README, PROMPTS, `logs/`, `transcripts/` (Claude Code run 1, Codex run 2), `scripts/agent/`, `scripts/independent/`, `walker-context/`.

## Re-run evidence made for this film (2026-10-06, Blender 5.1.2, Godot 4.7.2.stable.official.ed1daf0bf)
- `evidence/probe/` — the three-column mutation experiment (Blender → three `.glb` → Godot AABB), the stale-dimensions probe, the exit-code probe; outputs match the chapter's recorded lines exactly.
- `evidence/render_post.py` + `evidence/renders/` — Blender's own Workbench renders of the checkpoint post built by the final agent script (`evidence/scratch/tools/blender/build_checkpoint_post.py`, a verbatim copy of `examples/…/scripts/agent/build_checkpoint_post.py`), the collider alone, and a real Blender window screenshot (`gui_shot.py`, run with a scratch `BLENDER_USER_CONFIG` so the user's own Blender config is untouched).
- App icons: the installed `Blender.app` and `Godot.app` icon files, converted to PNG with `sips`.

## Primary documentation (verified by the builders; see FACTCHECK.md)
- Godot docs (stable): Available 3D formats; Model export considerations; Node type customization; Introduction to 3D; Collision shapes (3D); Import process.
- glTF 2.0 specification §3.4 (units: metres).
- Blender 5.1.2 `--help` and the bundled `io_scene_gltf2` 5.1.20 operator properties.
- MCP for Blender (github.com/ahujasid/mcp-for-blender) and Blender Lab's Blender MCP (projects.blender.org/lab/blender_mcp; blender.org/lab/mcp-server): README / documentation pages as read on 2026-09-27 by the chapter; builders re-checked quoted sentences.
- Godot official demo projects, `3d/platformer` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7` (MIT): project.godot, player.tscn, enemy.tscn, enemy.glb.import (read from the public `walker-3d-platformer` copy).

## Credits
- Narration: Liam, in for Bear (Kokoro-82M voice `am_onyx`). Blender and Godot names and icons belong to their projects; shown as the tools they identify.
