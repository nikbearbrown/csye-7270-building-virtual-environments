# EVIDENCE-INDEX.md — the real material the film shows

Everything below was produced by real runs on 2026-10-06 (Blender 5.1.2, Godot 4.7.2 stable, macOS) by `evidence/` scripts that can be re-run. Images are in `pantry/` (prefix `ev_`); scripts, logs and notes are in `evidence/<topic>/`. Pixel boxes for every interface part: `evidence/gui/NOTES.md` (read it before cropping). MCP project facts with file and line numbers: `evidence/mcp/README-FACTS.md`.

## What may and may not be claimed
- The three assets were built by a **Blender script run (the script route)** for this film. They were NOT built through the MCP. Never say or show that Claude built them through the MCP.
- The Blender window screenshots were taken by Blender's own screenshot operator under a script (no person at the keyboard). The hand-edit pair is **produced by script: label it "illustrative"**. Never present it as a student's recording.
- The MCP route was **not run** (no `uv`, no MCP server, add-on not installed). Show its commands without output, labelled "documented, not run".
- Paths in the git logs are scratch paths: on screen, show the assignment's command with its `<your-repository>` placeholder and say nothing about the path.

## Assets (script route) — `evidence/assets/`
| asset | dimensions (x y z, m) | triangles | shapes | materials | origin |
|---|---|---|---|---|---|
| Crate | 0.8 × 0.8 × 0.8 | 60 | 5 | CrateWood, CrateBand | centre of the underside at the world origin |
| Lantern | 0.3 × 0.3 × 0.5 | 202 | 5 | DarkIron, WarmGlass, Flame | same |
| Coin | 0.3 × 0.3 × 0.04 | 180 | 3 | CoinGold, CoinFace | same |
All three: rotation 0, scale 1.0 (applied), lowest point z = 0.0 m. Real terminal output of the script route command (`Blender -b --factory-startup --python-exit-code 1 --python build_<asset>.py`): `build_crate.log`, `build_lantern.log`, `build_coin.log` (the last lines print `exported <asset>.glb, +Y Up on`). Sources `build_*.py`, exports `*.glb`, saved `*.blend` and Blender's backups `*.blend1`; the real listing `ls_blend.log` (`ls -la *.blend *.blend1 *.glb`).

## Renders (Blender Workbench, transparent PNG 2400×1350)
`ev_crate_34.png`, `ev_lantern_34.png`, `ev_coin_34.png` (three-quarter views) · `ev_lantern_back.png`, `ev_lantern_below.png` · `ev_three_side_by_side.png` (crate, lantern, coin on a floor plane) · `ev_sphere_default_vs_low.png` (a default UV sphere, 960 triangles, beside a 12 × 6 sphere, 120 triangles, wireframe on).
Primitive triangle counts (Blender 5.1.2, `evidence/primitives/tris.log`): cube 12 · plane 2 · default cylinder 124 · default cone 62 · default UV sphere 960 · sphere 12×6 120 · cylinder with 12 vertices 44.

## Real Blender windows (3456 × 2006; boxes in `evidence/gui/NOTES.md`)
`ev_bl_object_mode.png` all six parts, Item tab open, Dimensions 0.3 / 0.3 / 0.5 m · `ev_bl_object_mode_parts.png` Outliner listing five objects · `ev_bl_edit_mode.png` the crate in Edit Mode · `ev_bl_status_stats.png` status bar "Tris:202" · `ev_bl_export_gltf.png` the glTF export dialog, +Y Up ticked (a second window, 3456 × 2006) · `ev_bl_edit_menu.png` the Edit menu with Preferences · `ev_bl_prefs_addons.png` Preferences on the Add-ons tab · `ev_bl_hand_edit_before.png` / `ev_bl_hand_edit_after.png` (illustrative) · `ev_bl_orbit_1.png` … `_4.png` (same window, four viewport angles). In Blender 5.1.2 an add-on row shows only its name, so the MCP add-on row would read "MCP for Blender" (inference; not installed); the README calls it "Interface: MCP for Blender".

## Real Godot output — `evidence/godot/` (project `tests/check_assets.gd`; the film's headless check)
Commands (real): `godot --headless --path <project> --import` (`import.log`) and `timeout 120 godot --headless --path <project> --script res://tests/check_assets.gd --fixed-fps 60` (`check_good.log`: crate (0.8, 0.8, 0.8), lantern (0.3, 0.5, 0.3), coin (0.3, 0.04, 0.3) m, node scale 1,1,1, gap to floor 0.0, PASS ×3).
Five demonstrations, each a real log with its exit code: `demo_i_lantern_yup_off.log` (+Y Up off: size (0.3, 0.3, 0.5), height on Z, FAIL) · `demo_ii_crate_scale_unapplied.log` (node scale 0.4, mesh size 2.0 m, FAIL) · `demo_iii_crate_origin_centre.log` (centred origin at floor level: lowest point −0.4 m, FAIL: sinks) · `demo_iii_crate_origin_centre_lifted_by_guess.log` (lifted 0.5: +0.1 m, FAIL: floats) · `demo_iii_crate_origin_centre_lifted.log` (lifted exactly 0.4: gap 0.0, PASS, which hides the problem) · `demo_iii_crate_origin_centre_lifted_origin_check.log` (`+origin`: "the origin is 0.4 m above the base: it sits on the floor only because the node was moved", FAIL) · `demo_iv_lantern_x10.log` (every axis ×10: FAIL, a scale error) · `demo_v_check_good_origin_check.log` (good assets with `+origin`: PASS).
`ev_godot_showcase.png` and `ev_godot_showcase_crop.png`: a real Godot window screenshot of the showcase scene (floor, light, camera, the three assets side by side).

## Exit code — `evidence/exitcode/`
`without_flag.log`: `Blender -b --factory-startup --python bad.py`, the script raises ValueError, `echo $?` prints **0**. `with_flag.log`: the same with `--python-exit-code 1`, prints "Error: script failed, file: 'bad.py', exiting." and **1**.

## Git — `evidence/git/` (real output in a scratch repo shaped like a submission)
`git_tag.log` (`git tag a3`) · `git_log.log` (`git log --oneline --decorate`: three commits, the last "(HEAD -> main, tag: a3)") · `git_ls_files.log` (the tracked tree: README, CHANGE-BRIEF.md, BLENDER-NOTES.md, TEST-REPORT.md, FRICTIONAL.md, SOURCES.md, `art/3d/*.blend`, `godot/assets/*.glb` + `.import`, …) · `git_status.log` (clean) · `git_status_ignored.log` (the `.blend1` files ignored) · `git_clone.log`, `git_checkout_a3.log`, `clone_*.log` (clean clone, checkout of `a3`, import and check in the clone).

## MCP project facts — `evidence/mcp/README-FACTS.md` (read it)
Versions: 2.1.1 on 27 Sept 2026, 2.1.9 on 6 Oct 2026 (several releases between). Tool lists: 2.1.1 code has `get_object_info`, `get_viewport_screenshot`, `export_scene` and others; 2.1.9's README lists nine tools (`execute_blender_code`, `look`, `get_scene_info`, `generate_3d`, `search_assets`, `import_asset`, `get_addon_status`, `disable_telemetry`, `record_trajectory_feedback`). Verbatim README sentences (quote ≤ 15 words, attributed, versioned): socket "has no authentication or encryption"; "anyone who can reach that port can run Python inside Blender"; the pip warning; `claude mcp add blender uvx mcp-for-blender` is the README's own line (the `-e DISABLE_TELEMETRY=true … --` form is the course's adaptation); the 2.1.9 README leads with a one-line installer that finds the MCP clients on the machine and lets you pick which to set up. All six service/download checkboxes (Poly Haven, Sketchfab, Poly Pizza, Hyper3D Rodin, Hunyuan3D, Tripo) default to off; the add-on's server auto-starts by default, on localhost port 9876; in a no-window (`-b`) run it never starts the server.

## Also in `pantry/`
`ev_icon_blender.png`, `ev_icon_godot.png` (the real app icons).
