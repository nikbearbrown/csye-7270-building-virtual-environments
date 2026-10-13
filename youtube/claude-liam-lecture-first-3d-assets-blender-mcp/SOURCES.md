# SOURCES.md — Your First 3D Game Assets with Claude and Blender

## Source
The film is built from one document: **Assignment 3, "Your First 3D Game Assets with Claude, the Blender MCP, and Blender"** for CSYE 7270 (Virtual Environments and Real-Time 3D, Nik Bear Brown, Northeastern University), `../../assignments/03-first-3d-assets-with-blender-mcp.md`. Nik Bear Brown pasted the full text with the request "Use the lecture skill, Liam persona, to make a film on this." The whole document is covered; what the film leaves out, and why, is in `ACTS.md`.

## Primary sources checked
- MCP for Blender README and add-on/server code, 27 Sept 2026 (version 2.1.1) and 6 Oct 2026 (version 2.1.9): `evidence/mcp/` (`README-FACTS.md` has file and line numbers). Public page captured without sign-in for B31 (`evidence/act4/capture_readme.py`).
- PyPI release list for `mcp-for-blender` (`evidence/mcp/pypi*.json`): the 7 releases after 2.1.1.
- Blender 5.1.2 (Blender's own screenshot operator and Python API) and Godot 4.7.2: every number and every window picture in the film comes from a run recorded under `evidence/`.
- The course's AI policy video (B14): public YouTube page, captured without sign-in (`evidence/act1/capture_policy_video.py`).

## Real runs and captures (all re-runnable; commands in each act's folder under `evidence/`)
- Script route: `build_crate.py`, `build_lantern.py`, `build_coin.py` (crate 60, lantern 202, coin 180 triangles); Workbench renders; primitive triangle counts (cube 12, default cylinder 124, default cone 62, default UV sphere 960, 12×6 sphere 120).
- Blender window screenshots taken with Blender's own screenshot operator under a script, scratch preferences only (no person at the keyboard). The hand-edit before/after pair is produced by script and labelled "illustrative" on screen.
- Godot headless import and check script, with five demonstrations (axis, unapplied scale, origin, ×10, colour).
- Exit codes of a failing Blender script with and without `--python-exit-code 1` (0 and 1).
- A scratch git repository shaped like a submission: `git ls-files`, `git tag a3`, `git log --oneline --decorate`, a clean clone and `git checkout a3`.

## What was NOT run
- The MCP route (uv, `claude mcp add`, the add-on, any MCP session) was never run, by the course or for this film. Its commands appear without output, labelled "documented, not run". The prompt in Act V is shown as the assignment's adapted prompt, "not run".
- The three assets in the film were built by a Blender script, not through the MCP, and the film says so.

## Credits
Narration: Liam, in for Bear (Kokoro, `am_onyx`). Drawings and layouts: Manim and Remotion from the Brutalist toolkit (Claude palette). Blender and Godot icons are the apps' own. Blender is GPL; Godot is MIT. No third-party footage, audio or models.
