# Fact check — Walker Survival Shooting: First Props in Blender

Every on-screen number and spoken claim was checked against the submitted revision **b370626** (README,
CHANGE-BRIEF 2026-10-15 entry, BLENDER-NOTES, TEST-REPORT, SOURCES asset log, FRICTIONAL, `godot/`,
`tools/blender/`) or against output re-run for this film (`evidence/a3-check.log`). Narration is the exact text
in `PROMPTS.md`.

## Corrections applied (the film differs from a submitted document)

| Claim in the submitted docs | What the film says | Why |
|---|---|---|
| TEST-REPORT and FRICTIONAL: "56 PASS, 0 FAIL" | **55 PASS**, 0 FAIL, exit 0 | The submitted log `test-logs/a3_check_2026-10-15_v3_latch-fixed.log` and the re-run both contain 55 lines beginning `  PASS  `. 56 is the number of lines containing the word PASS, including the final `== ALL PASS: 0 failure(s) ==` summary. Counted from the script too: Part 1 = 6 assets × 4 + 2 crates × 3 = 30; Part 2 = 5 floor + 4 grid + 1 tablet + 15 overlap pairs = 25. The designer approved using 55. The submitted documents were not changed. |
| SOURCES PROP-TABLET-02 "Where used": "not yet copied into the Godot project" | The tablet is in the Godot scene | `godot/assets/props/tablet.glb` exists at b370626 and `base.tscn` line 146 instances it. The SOURCES cell is out of date. |
| TEST-REPORT §2: small crate Godot box "0.5, 0.500006, 0.5" | B13 shows `(0.5, 0.5, 0.500006)` | Copied from the re-run log line `crate_cube: size (0.5, 0.5, 0.500006)`; the 6 µm is on z, not y. Same magnitude, so the spoken claim (six thousandths of a millimetre) holds. |
| B19 narration draft: test chair re-export "identical" | "came out the same size" | TEST-REPORT §9.4 says only "same size and dimensions"; byte identity was never checked. Changed before the final audio. |
| B11 narration draft named "the desk" | Names the chair, tablet and crates only | The figure crop was moved right (GATE T read the desk legs as overlapping text), so the desk is no longer in frame; the line and the card were changed to match what is shown. |

## Spoken / on-screen claims and their sources

| Beat | Claim | Source |
|---|---|---|
| B00, B20, B21 | Source revision b370626; 55 PASS, exit 0 | `git log` of the course repo; `evidence/a3-check.log` |
| B02 | Game premise; three assets and their game roles; 1 cell = 0.1 m | README.md first paragraph; CHANGE-BRIEF asset table and common rules |
| B03 | MCP vs script route per step; brief written after chair and tablet | SOURCES asset log (ENV-SEAT-02, CRATE-LONG-03 "script route"; build_crate_cube.py call 3 headless); CHANGE-BRIEF "Order, recorded honestly" (quoted exactly, with an ellipsis) |
| B04 | Prompt text; 21 bevelled boxes; 804 triangles | SOURCES PROP-TABLET-01 (translation quoted exactly); TEST-REPORT §8.1, §9.1 |
| B05 | Second prompt; three materials; 804 → 388; 21 shapes kept by decision | SOURCES PROP-TABLET-01/02; CHANGE-BRIEF asset table |
| B06 | 9 boxes / 108 tris → 6 shapes / 72 tris; stretchers removed, slats merged; script route; no viewport capture of v2 | SOURCES ENV-SEAT-TEST-01, ENV-SEAT-02; build_chair.py call 5 header |
| B07 | v1 footprint 0.56 × 0.515 m; grid prompt; v2 exactly 5 × 5 cells; code lines 150–151 | SOURCES CRATE-CUBE-01/02, CRATE-LONG-02; TEST-REPORT §8.2; `tools/blender/build_crate_cube.py` lines 150–151 (whitespace between code and comment compressed on screen). "One cube and one crate twice as long" combines two prompts (CRATE-LONG-01 and -02). |
| B08 | Own screenshot; Edit Mode; median X −0.123, Y −0.2425, Z 0.42553; latch/handle reasons | `design/blender-notes/blender-session-01.png` pixels; BLENDER-NOTES §5; SOURCES CRATE-CUBE-02 |
| B09 | Right latch 0.10 m deep; first fix not saved; "fixed" written unchecked; second fix; duplicate deleted; 6 mm kept | TEST-REPORT §8.4, §9.5; SOURCES CRATE-CUBE-02; FRICTIONAL 2026-10-14/15 |
| B10 | Lines 137–147; scale 1; y = 0.25 = floor top; tablet tilted at y 0.664 | `godot/base.tscn` lines 28–29 (floor size 0.5 high, centred at 0) and 137–147 |
| B11 | Render through a3_asset_camera; recognisable at a glance (human check); one light moved by the designer | capture take `asset_cam`; TEST-REPORT §7 |
| B12 | Script written by Claude; ASSETS table; tablet lowest y −0.081 by design | TEST-REPORT header; `tests/a3_asset_check.gd` lines 12–22; CHANGE-BRIEF origin row |
| B13 | Sizes within 0.002 m; triangles 72 / 388 / 88 / 88 | `evidence/a3-check.log` Part 1 |
| B14–B15 | open → −100°, close → 0°; 15 frames at 24 fps; lid ~8 cm behind footprint | script lines 89–97; log; CHANGE-BRIEF animation row; TEST-REPORT §11 |
| B16–B17 | Floor top from `room/floor`; grid; chair not grid-checked; earlier failing run kept | script lines 104, 112–123; log Part 2; `test-logs/a3_check_2026-10-15_v1_tablet-moved.log` (1 FAIL, exit 1); TEST-REPORT §8.5 |
| B18 | What the check cannot show; human check; no character model; nobody else looked | README "How to run the check"; TEST-REPORT §7, §10 |
| B19 | Claude's errors 1–5 | TEST-REPORT §9 (quoted exactly with an ellipsis) |
| B20 | Contributions; next step | FRICTIONAL contributions (quoted with an ellipsis); SOURCES "Human / AI contributions". The next step (character model, first gameplay, tablet interaction design) is the designer's decision, given for this film. |

## Not claimed

The film does not claim gameplay, a playtest, real-time performance, that the assets look good, or their scale
next to a person. Bounding boxes that do not overlap are not presented as proof that meshes never interpenetrate.
The opening prompt is labeled as a reconstruction.
