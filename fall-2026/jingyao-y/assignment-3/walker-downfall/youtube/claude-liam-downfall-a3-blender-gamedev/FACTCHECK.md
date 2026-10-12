# FACTCHECK.md

Each factual claim in the narration, with where it was checked. Source revision: `ceada15`.

| Beat | Claim | Checked against | Status |
|---|---|---|---|
| B00 | The prompt is reconstructed, not a transcript. | Labelled on screen; PROMPTS.md. | OK (disclosed) |
| B01 | Claude built all three assets by MCP, one call per part; every call is in the repo. | `tools/blender/build_*.py` (8 + 7 + 7 calls, plus the clear, join and save calls). | OK |
| B01 | The author made design calls, learned the viewport, moved two kerbs, gave the final look. | `a3/BLENDER-NOTES.md`; CHANGE-BRIEF approvals and R3; TEST-REPORT HUMAN CHECK. | OK |
| B01 | Blender 5.4 Alpha, not 5.1. | `get_addon_status` reported `5.4.0 Alpha`; the course version was given by the author. | OK |
| B02 | The limits per asset. | As the author gave them in chat (`a3/CHANGE-BRIEF.md`, "Assignment limits"). | OK |
| B03 | Level 2.2; run 6.5 per level, under 19°; 2 m aprons; half-width 3.4–5.6; narrowest corridor 6.8. | `continuous_world_map.gd:61-66, 175, 756`. | OK. The snow and city offsets are not mentioned. |
| B04 | Seed 1729 ramp foot; seed 1333 cliff between terraces; the terrain carries shape and collision; Grim Dawn's editor works the same way. | `capture/capture_a3_film.gd` output (`CLIFF seed 1333`); `terrain_surface.gd` (`_cliff_split`, collision walls); Grim Dawn Modding Guide, Terrain Tools (Plateau, Ramp, No Pathing). | OK |
| B05 | Three boxes and one icosphere; one tier + 0.1 above and below; 0.3 in front; call 6 makes the boulder 0.5 tall, on the lip, peak 2.4. | `build_cliff_wall_segment.py` calls 2–6; call 6's printout `z 1.9 2.4`, `y -0.3 0.3`. | OK |
| B06 | Before: a disc; after: it bulges from the face. The rubble's top stone floated and the next call sank it. | `images/blender-cliff-*.png`, `images/blender-rubble-*.png`; `build_cliff_rubble_pile.py` call 5. | OK. The "after" cliff and rubble sheets have three views (no top), as the label says. |
| B07 | One plane edited into a wedge plus two kerbs; slope 2.2/6.5 + 0.02 + a 0.10 crown fading over 0.5 m. | `build_arched_ramp_segment.py:47-51` and calls 2–4. | OK |
| B08 | Edge slope 18.7°; crown 0.1 at y = 0.5; crown barely visible, invisible from the game camera. | Call 5 printout (`edge slope deg 18.7`, `crown … 0.1`); the visibility is Claude's reading of the images (RIFF.md). | OK (observation, not a measurement) |
| B09 | The author moved each kerb 0.1 m outward by hand; the reason; the comment records the steps Claude gave; the author's report was "all done". | Author's message "全部完成"; Claude's step list in the session; verification in B10. | OK |
| B10 | Left kerb −3.5 … −3.2, road unchanged, right kerb mirrored, width 7.0, saved, backup written; git ignores it. | Recorded `get_scene_info` and call 7 output; `.gitignore` `*.blend1`. | OK |
| B11 | Headless, one run per file, glTF binary, Y up, mesh only; +Y → −Z. | `export_glb.py:24-33`; F1 in `test_a3_assets.gd`. | OK |
| B12 | A moment through the game camera, then one full orbit; capsule 1.7 m; the game camera looks from −Z, so the cliff faces away. | `orbit.avi` window 1.34–18.0 s (0.66 s game camera + 16 s orbit); `CapsuleMesh height = 1.7`; `GameManager.CAMERA_OFFSET (0, 16, -10)`. | OK |
| B13 | The check needs the highest ramp vertices past −6 on Z; other checks: bounds ±0.02, transforms, triangles, colours. | `test_a3_assets.gd:114-121` and the rest of the file. | OK |
| B14 | 25 checks pass on a fresh copy of the commit; double-sided materials, so back faces are never culled. | `evidence/test_a3_assets-ceada15.log`; the probe printed `cull 2` (disabled). | OK |
| B15 | `.tscn` lists the basis by rows; Claude wrote columns. | Light direction printed in the re-render: `(-0.353553, 0.707107, 0.612372)` for the first basis, `(-0.5, -0.612372, 0.612372)` corrected. | OK |
| B16 | Re-rendered: the light points up; Claude counted inward faces first (none), then found the transpose. | `light.avi`; the normals probe (0 inward in all 10 islands); TEST-REPORT loop 3. | OK. This is a re-render, disclosed on screen. |
| B17 | Scene statistics on after a second try; the author moved the kerbs and checked in the Godot editor; the report was "everything is correct". | The author's messages "没找到场景统计", then the second screenshot; "全部完成"; "都是对的". | OK |
| B18 | 116 / 68 / 180 triangles; 25 checks; the fixes; the open items. | TEST-REPORT; the Blender counts; the Godot log. | OK |

## Corrections made during the build

- **B12** first said "two seconds through the game camera, then one orbit". The 18 s capture cannot hold both for 16.7 s of narration without retiming, so it now says "a moment … then one full orbit".
- **B09** first said the author "selected each kerb in Edit Mode". The author reported only "全部完成", so the selection steps are Claude's instructions, not the author's report. It now says so.
- **B17** first said the author "orbited the assets". The author's report does not say how they looked, so it now says "checked".
- **B04** first said "then at its top, with the cliff dropping beside it". The ramp-top frame does not clearly show a cliff, so a real cliff frame (seed 1333) was captured and the line changed.

## Visual and audio QC

Recorded after the final render.

### Final export, checked 2026-10-12

`exports/landscape/claude-liam-downfall-a3-blender-gamedev.mp4`:

| Property | Value |
|---|---|
| Resolution | 3840×2160 |
| Frame rate | 30 fps |
| Duration | 338.9 s |
| SHA-256 | `2cd689587a743e521aca43da80f267ab33e64a21a096e5acd682ca08fb403e85` |

- **`./art godot-gamedev --check`:** PASS (21 source files, 7 components, 7 exact excerpts, 7 code→result pairs), against the pristine `ceada15` snapshot, before and after the final build stamp. It checks hashes, lines and associations only.
- **Gate V:** 42 frames, 0 BLOCKER, 0 MAJOR.
- **First render refused** with 4 BLOCKER and 4 MAJOR. Fixes:
  - B10 and B14: the burned labels started at x = 150, outside the 4K title-safe edge (x = 192). They were moved to x = 230.
  - B16: underfill (39–45%) and low contrast in the label region. It became a side-by-side before/after panel, and the declared label region was tightened to the label box.
- **Audio per beat** (volumedetect on the master): every narrated beat sits between −26.5 and −28.2 dB mean. B20 is silent at −91 dB.
- **Outro jingle, limitation:** this is the same as the A2 film. OUTRO-LOCK asks for a stock jingle, but this checkout's `ClaudeTitleOutro` renders no audio, so the card is silent. The shared tool was not changed.
- **Frames inspected** (one per beat, `_qc/final_sheet.png`):
  - B01's correction fired: "course" became "5.4 Alpha".
  - Every engine and Blender frame carries its provenance label.
  - B17 shows the author's screenshot, labelled as the author's.
  - The code excerpts are readable at 4K.
- **No human has watched the film yet.**
