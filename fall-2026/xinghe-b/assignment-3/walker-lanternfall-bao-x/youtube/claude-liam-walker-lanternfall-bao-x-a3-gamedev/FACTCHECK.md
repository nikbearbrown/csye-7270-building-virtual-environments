# FACTCHECK

Every factual claim in the narration and on screen, with where it was checked. Game source revision:
**c0dba4c** (`FILM-SOURCE-REVISION.txt`). "Take" means a real 4K Movie Maker capture in `capture/` (CAPTURE.md);
"window" means Blender's own screenshot through the MCP (`images/blender/`).

## Corrections made while building the film

| Beat | First draft said | Why it was wrong | Now says |
|---|---|---|---|
| B03 | "On October fourteenth the first status call answered" | the first `get_addon_status` call is logged 2026-10-13 16:30 EDT; the builds were on 10-14 | "The first status call answered straight away … Earlier that day, a different coding session had no MCP tools" |
| B08, B16, B18 | the barrel's base "flickers" | flicker is motion; Claude saw it only in still images (faces showing through each other) | "the two faces show through each other"; "overlapping faces"; Bao later saw it in the running room and called it "一点 z-fighting" |
| B10 | "line sixty-one merges every mesh's bounding box" | merging happens in `_measure` (lines 26–47); line 61 compares the merged box | "takes the merged bounding box of every mesh" |
| B10 | "every node's scale … exactly one" | the test uses `is_equal_approx(Vector3.ONE)` | "every mesh node's scale to be one" |
| B16 | "Godot draws … pale yellow, where Blender showed orange" | Blender's material preview shows a pale orange, not saturated orange | "where Blender's preview showed a pale orange" (draft); final B16 follows Bao's own words |
| B01 | on-screen lines "Claude generated three props / from Blender's basic shapes / the numbers measure, Bao judges" | the third line did not fit at 150 px; at 120 px the final frame check found the beat under-filled (22 % / 44 % of the safe area, minimum 55 %) | "AI generated → scripted the props / from basic shapes / Bao judges the look" at 185 px; one sentence added to the narration ("and every call is kept"; "and he made it"), so the text is typed by the 50 % sample |
| B04 | the plan rendered "−0.22" as a box | the first CJK font (Hiragino Sans GB) has no U+2212 | font changed to STHeiti Light; text unchanged |

## Claims by beat

| Beat | Claim | Checked against |
|---|---|---|
| B00 | three simple 3D props, directed through the Blender MCP, one hand edit, exported, shown in a Godot scene | the Assignment 3 page (executive summary) |
| B00 | 27 build calls through the MCP; code kept in tools/blender/ | `tools/blender/build_lantern_gate.py` (13 calls, one failed), `build_supply_stack.py` (7), `build_oil_shrine.py` (7) |
| B00 | 17 + 14 + 9 headless checks | `capture/test-run-film-build-raw.txt` |
| B00 | the composer prompt is reconstructed | labelled in `beat_sheet.json` role note and PROMPTS.md; not a recorded prompt |
| B01 | no model generated these props; basic shapes; one call per part | build scripts (only `primitive_cube_add`, `primitive_cylinder_add`, `primitive_ico_sphere_add`); `get_addon_status`: every generator off; no `generate_3d` / `search_assets` / `import_asset` call in the session |
| B02 | Lanternfall: 2D survivors game in a fog-bound night market | README.md, CONCEPT.md |
| B02 | names, purposes, sizes, shape and triangle budgets, origin at the centre of the base | CHANGE-BRIEF.md A3-R0 (commit 8a8c778, 2026-10-13 16:01) |
| B02 | built counts 6 · 88, 3 · 68, 3 · 60 | `evidence/a3/*-build.json`; `test_a3_assets.gd` output |
| B02 | "froze their numbers before the build" | A3-R0 is committed before the MCP rebuild (0c11398, 2026-10-14 11:58) and before the script-route builds of the stack and shrine (7e117ce) |
| B03 | MCP for Blender 2.1.9; add-on 1.8; telemetry off; libraries and generators off | `evidence/a3/setup/04-mcp-connect.log` (lines shown verbatim) |
| B03 | a socket on Bao's own machine | `lsof`: Blender PID 42766 listening on 127.0.0.1:9876 (same log) |
| B03 | an earlier session had no MCP tools; first builds were background scripts | FRICTIONAL.md 2026-10-13 entry; `tools/blender/script_route/` |
| B04 | the plan and Bao's two answers | this session's transcript, 2026-10-14 11:59 EDT (Chinese verbatim; English gloss labelled) |
| B05 | call 2 body; location (0, 0, 0.25); dimensions (1.20, 0.80, 0.50) | `tools/blender/build_supply_stack.py` lines 50–60 (verbatim on screen) |
| B05 | the default cube is 2 m, so scale is left behind | `get_scene_info` after call 2: scale (0.6, 0.4, 0.25), size 1.2x0.8x0.5 (`evidence/a3/mcp/supply_stack-session.md`) |
| B06 | film re-run in a scratch file; Scale 0.600 / 0.400 / 0.250; status-bar warning | window `1249-rerun-2-lower-crate.png`; CAPTURE.md |
| B06 | "Godot would receive a scaled node" | glTF stores object scale on the node; `test_a3_assets.gd` checks node scale for this reason (CHANGE-BRIEF "Answers before delegation") |
| B07 | call 5 applies rotation and scale (`transform_apply(location=False, rotation=True, scale=True)`) | `build_supply_stack.py` lines 87–100 |
| B08 | after call 5: scale 1, dimensions 1.2 / 0.8 / 0.5 m | window `1250-rerun-6-sidebar-dimensions.png` |
| B08 | look renders from front, back, three-quarter and below | `evidence/a3/mcp/*-look.png` (2026-10-14 11:56–12:04) |
| B08 | the barrel base and the crate underside share a plane | barrel spans z 0–1.10, lower crate z 0–0.50 (`supply_stack-build.json`); visible in the below tile |
| B09 | Bao selected OilGem in the Outliner, rotated 20° about Z, applied it; his note | BLENDER-NOTES.md (Bao's account); commit 7fae834 |
| B09 | not recorded live | CAPTURE.md; no recording of 12:19 exists |
| B09 | 20.0°, max 1.84e-8 m | TEST-REPORT.md "Blender hand edit"; comparison of the MCP GLB (f7da21f) and the re-export |
| B10 | lines 58–64 of `test_a3_assets.gd`; 0.011 m tolerance; base y ≤ 0.011 | the file at c0dba4c (excerpt hashed in `gamedev-evidence.json`) |
| B11 | 17 checks, 0 failures; sizes; +Y height; scale mutation caught | `capture/test-run-film-build-raw.txt` |
| B11 | Blender column | `evidence/a3/*-build.json` `visual_bounds_blender_xyz_m` |
| B12 | `-convcolonly` boxes become collision-only bodies; layer 3, mask 0 | `a3/lantern_gate.gd` lines 1–11; `lantern_gate.glb.import` (`nodes/use_node_type_suffixes=true`); `test_lantern_gate.gd` (`suffix-created-two-static-bodies`, `prop-layer-and-mask`) |
| B12 | collider sizes; no cross-arm collider | `build_lantern_gate.py` calls 8–9; `test_lantern_gate.gd` `collider-fit` |
| B13 | the stand-in stops at z = 0.667 m, about two thirds of a metre from the gate's centre | `capture/take-a3-block-events.jsonl` (release of `move_up`); base half-depth 0.40 + capsule radius 0.25 |
| B13 | F4 opens the room | `game/session.gd` lines 363–364, 399 |
| B14 | the brief promised a camera behind and below; the room had a fixed camera | CHANGE-BRIEF A3-R0 ("the shared camera can move behind and below"); `lantern_gate_room.tscn` before c0dba4c |
| B14 | lines 51 and 54; floor collider stays | `a3/lantern_gate_room.gd` at c0dba4c; `test_a3_camera.gd` `floor-collider-stays-while-hidden` |
| B15 | front → behind → below (floor hidden) → front → closer, through real input actions | `capture/take-a3-orbit-events.jsonl`; driver `capture/capture_a3_driver.gd` |
| B15 | nine checks, all passing | `capture/test-run-film-build-raw.txt` |
| B16 | Bao's look: front and back normal; colour shift accepted; z-fighting only at very low angles; stand-in stops in front of base and post; passes under the arm | Bao's words, 2026-10-15 (TEST-REPORT.md "HUMAN CHECK — final three-asset room"), verbatim on screen |
| B16 | Claude read the assignment as one prop; an export call failed its own check | CHANGE-BRIEF A3-R0; `build_lantern_gate.py` call 12 (commented, with its error) |
| B16 | next: barrel 0.60 m tall at z = 0.80 | arithmetic: crate top 0.50 m, stack top 1.10 m |
| B17 | who did what | FRICTIONAL.md (2026-10-13, 10-14, 10-15 entries); SOURCES.md "Work split" |
| B17 | source revision c0dba4c | `FILM-SOURCE-REVISION.txt`; `git diff c0dba4c HEAD -- godot/` is empty |
| B18 | verdict lines | the beats above |
| B19 | UpperCrate at y = 0.05 with half-depth 0.34 reaches 0.39 m; the footprint ends at 0.40 m; +0.07 m makes the stack 0.86 m deep | `supply_stack-build.json` parts; test tolerance 0.011 m |

## Not checked by any test

How the props look under the room's light, whether they read as what they are, and whether the collision margin
feels fair: Bao's human check (B16) is the only evidence, and only one person has looked.
