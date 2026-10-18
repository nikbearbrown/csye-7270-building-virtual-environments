# Build notes: Coin (teaching prop), built by Claude

`3 basic shapes · 180 triangles · 2 materials · 0.30 x 0.30 x 0.04 m · Blender 5.1.2`

**Source.** `youtube/claude-liam-lecture-first-3d-assets-blender-mcp/evidence/assets (build_*.py, build_*.log, ASSETS.md, save_blend_demo.py)` in this repo's `youtube/claude-liam-lecture-first-3d-assets-blender-mcp/evidence/assets/`. `coin.blend`, `coin.glb`, `build_coin.py` and `build_coin.log` are copied unchanged. `.blend1` backups were not copied.

**How it was built (quoted).** ASSETS.md: "Each asset is built from basic shapes only, joined into ONE object ... Command (run from this folder, exactly as the film shows it): `Blender -b --factory-startup --python-exit-code 1 --python build_coin.py`. Exit code 0 for all three." The lecture's BUILD-LOG.md: "The MCP route is not shown running, because nobody has run it ... The three assets in the film were built by a Blender script (the assignment's fallback route)." So this is a scripted build, not an MCP session. Rounds: one script run per asset; the log has a single run. The "hand edit" images in the source's evidence/gui are produced by script and labelled illustrative there; no human modelling is recorded.

**Numbers.** From my own `count_scene.py` run on `coin.blend` (Blender 5.1.2): 3 shapes by ASSETS.md (the file holds 1 joined mesh object), 180 triangles, materials CoinGold, CoinFace, size 0.30 x 0.30 x 0.04 m, 0 cameras, 0 lights. These match ASSETS.md's table. Colours (flat sRGB): CoinGold #FFC20A, CoinFace #E39A00; all materials metallic 0, roughness 0.9, taken from ASSETS.md.

**Renders.** Made 2026-10-18 with `scripts/render_props.py` in Blender 5.1.2 (EEVEE, 1200 x 900, sun plus area fill on a plain floor, exposure -1). The source folder only has transparent Workbench stills, so these were rendered fresh. Run: `Blender -b coin.blend --python scripts/render_props.py -- --out-dir renders --tag coin`.

**References.** None exist; see Compare section.

**Not done.** No hand review by Professor Bear, no opening in Blender 4.2, no texture or UV work (none intended).

## Built by

- **Builder:** Claude (no model version is recorded in the source files)
- **Method:** Scripted: build_coin.py was run once in background Blender (`Blender -b --factory-startup --python-exit-code 1 --python build_coin.py`), as ASSETS.md and build_coin.log record. It was NOT built through the Blender MCP: the lecture's BUILD-LOG.md says 'The three assets in the film were built by a Blender script (the assignment's fallback route)' and that nobody has run the MCP route. No render-versus-reference rounds and no hand-modelling rounds: one scripted build, no references. The five renders here were made on 2026-10-18 by scripts/render_props.py (one pass, plus two layout adjustments of the cameras).
- **Tools:** Blender 5.1.2 (read from the .blend by count_scene.py and from the build log); glTF exporter bundled with Blender; Godot 4.7.2 was used by the source film for an import check (evidence/godot logs, not copied here).
- **Build date:** 2026-10-06 (build logs at 12:59, .blend saved 13:27); renders 2026-10-18
- **Human review:** Professor Bear: pending (no verdict is recorded in the source folder).

## Known limitations

- There is no emblem or lettering; the face is a flat plain medallion. The rim is a 24-sided polygon and visibly faceted.
- The coin is metallic gold in colour only: all materials are metallic 0, roughness 0.9, so it looks matte, not shiny.
- The .blend was saved by Blender 5.1.2 (save_blend_demo.py) and has never been opened in Blender 4.2; Blender 4.2 may refuse or warn.
- The .blend has no camera and no light; the renders use a stage (floor and lights) added at render time, which is not in the file.
- The source folder's own note: the glass, flame and colours are flat Principled base colours, not textured; the .glb is small because there are no textures.
