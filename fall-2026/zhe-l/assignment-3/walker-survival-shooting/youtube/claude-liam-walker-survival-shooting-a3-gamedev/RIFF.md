# Riff log — what is visible, and what the narration makes of it

Observations come from the actual frames/stills; interpretations are labeled with their source. Durations and
exact narration are in `PROMPTS.md` and `SHOTLIST.md`.

| Artifact · range | Visible observation | Interpretation (source) | Narration (gist) | Suggested next experiment |
|---|---|---|---|---|
| `inputs/look/2026-10-12_tablet_grey.png` · B04 | Four views of a light-grey slab with bevelled corner bumpers, side rails and buttons | Far more detail than "a greybox from cubes" (SOURCES PROP-TABLET-01: 21 bevelled boxes, 804 triangles) | Claude overbuilt | Ask for a part count before the build |
| `tablet_green-black` / `tablet_388tris` · B05 | Green shell, black bumpers and a black screen; the 388 version looks the same at this size | The triangle cut is invisible at viewing distance (TEST-REPORT §8.1) | The colour came from the designer; the cut kept the look | Compare silhouettes at in-game camera distance |
| `chair_v1` vs `row.png` crop · B06 | Left: chair with two slats and stretchers; right: Godot chair with one backrest board and no stretchers | Shape count met without changing the size (SOURCES ENV-SEAT-02) | Nine to six | Sit a character on it once one exists |
| `crate_cube_v1` vs `v2_grid` · B07 | v1 handles visibly stick out of the box sides; v2 hardware sits flush | Footprint 0.56 × 0.515 → 0.5 × 0.5 (TEST-REPORT §8.2) | The grid rule came from the designer | Grid-check the open lid too |
| `blender-session-01.png` · B08 | Edit Mode, one latch selected on the lid/body seam, sidebar median X −0.123, Y −0.2425, Z 0.42553 | The latch sits across the seam (designer's intent, BLENDER-NOTES, SOURCES) | The designer's own edit | — |
| `latch_close.png` · B09 | Two dark latches across the seam on the small crate front; a handle on the large crate's end | Current saved state after the second fix; the 6 mm asymmetry is not visible at this distance | Inspect, revise, inspect again; first fix never saved | Measure after every save, not after every edit |
| `asset_cam.png` (cropped) · B11 | Chair, floating tilted tablet, both crates against the back wall under cool light (the desk is cropped out of the figure frame) | All read as what they are (designer's human check, TEST-REPORT §7; not established by the frame alone) | Code placement → visible placement | Re-check with a character model in frame |
| `media/B15.mp4` · 0.0–19.87 s | Frames 0–59 closed; from 60 both lids swing open about the back edge to past vertical; from 210 they close; from 420 they open again and stay open | The lids end beyond the back edge (TEST-REPORT §11: about 8 cm behind the footprint) | The check proves end angles; the footage shows the swing | Your Turn: test the lid against the wall |
| `log_part2.png` · B17 | Recorded lines: every bottom 0.250, four grid PASS lines, tablet bottom 0.603 | Placement matches the brief's grid rule (log) | 55 PASS; an earlier run failed and is kept | Keep failing logs for every changed check |
| `tablet_close.png` · B18 | Tablet floating at an angle beside the large crate; screen and green frame readable | A display placement, not a game placement (check-script comment) | What the script cannot judge | A second person's look |

No observation in this table is a playtest. Nothing moves in the scene except the crate lids in B15, driven by
the capture script.
