# FRICTIONAL — Assignment 3

My Assignment 2 log is in `../assignment-2/FRICTIONAL.md`.

## Entries

<!-- One entry per work session, newest last. Copy the block below. -->

### 2026-10-07 to 2026-10-12 — First Blender MCP assets: the chair and the tablet (retrospective)

*Written on 2026-10-15 from the Claude Code session transcripts, not at the time.*

- **Date and what I was working on:** 2026-10-07 and 2026-10-12. Trying the Blender MCP route: a simple chair (10-07), then the rugged military tablet from my reference images (10-12).
- **I tried / expected:** Have Claude Code build simple low-poly models from basic shapes in my open Blender 5.2.2 through the Blender MCP, and export them for Godot.
- **What happened:** The MCP connected after I enabled the add-on and started the server in Blender. The chair came out as 9 boxes (54 faces, 108 triangles); the first version floated 6 cm above the ground, and Claude moved the origin to the bottom centre. It was exported as `test_chair.glb` into the Godot project, but no `.blend` was saved. For the tablet I asked for a greybox "blocked out with cubes" where detail could be lost; Claude built 21 bevelled boxes in one light-grey material (804 triangles), and the front and back were hard to tell apart.
- **What I did:** Asked for the tablet's shell in dark green and black with one large black area for the screen; Claude rebuilt it with three materials. I saved `Pad_model.blend` myself.
- **What Claude or another person contributed:** Claude wrote and ran all the Blender Python and exported the chair. I gave the requirements and judged the results.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `walker-survival-shooting/tools/blender/build_chair.py` (calls 1–3), `build_tablet.py` (calls 1–2); asset log rows ENV-SEAT-TEST-01 and PROP-TABLET-01 in `walker-survival-shooting/SOURCES.md`.

### 2026-10-14 to 2026-10-15 — Assignment 3 brief, weapon crates, the furniture grid, my hand edit, computer desks

- **Date and what I was working on:** 2026-10-14 to 2026-10-15. Read the Assignment 3 requirements, gathered my assets into `design/item_resource/`, wrote the brief, made the third asset (two weapon crates), made my hand edit in Blender, and added two computer desks.
- **I tried / expected:** Reuse the chair and the tablet as two of the three assets, bring them within the course limits, and add a crate that opens and closes.
- **What happened:** Claude measured the existing files in headless Blender: the tablet had 804 triangles, over the 500 limit, and the chair (9 boxes) and the tablet (21 boxes) are both over the 6-shape limit. Claude's first brief draft left gaps and marked things as "chosen by Claude" that I had already decided (one cuboid and one cube crate; military green, from the tablet); I corrected that. The tablet went down to 388 triangles by keeping bevels only on the body and the corner bumpers. The first crates were 1.2 × 0.5 × 0.4 m and 0.5 m cubed, and their handles and latches stuck out, so the footprints were 1.26 × 0.515 and 0.56 × 0.515 m. After I set the grid, Claude rebuilt them so the whole crate fits 1.0 × 0.5 and 0.5 × 0.5 exactly. Godot 4.7.2 headless import of every `.glb`: node scale 1, 1, 1; the bottoms at y = 0 (the tablet at −0.081, as intended); the crate lids reach −100° after `open` and 0° after `close`. During one check Claude's script accidentally re-exported `test_chair.glb` over the file in the Godot project; it came out with the same size and dimensions.
- **What I did:** Made the decisions: get every asset under 500 triangles first; keep the tablet's origin in the centre because it does not affect holding it; the character is 1.6 m tall; the chair is the start-menu chair; the crates are buildable furniture that store items (small crate `small_box` 10 × 10, large crate `big_box` 20 × 10); the furniture grid is 1 cell = 0.1 m, so the large crate became 1.0 × 0.5 m. **My hand edit in Blender:** in Edit Mode I raised the small crate's two latches so each sits half on the lid and half on the body, so it reads as a latch that locks the lid, and moved both end handles up, because handles near the top give a lower centre of gravity when the crate is carried. Claude measured the result and found that the right latch had been stretched 0.10 m deep into the lid and the box, and that the two latches were about 2 mm off from each other. I fixed both myself by selecting single faces and typing exact positions that Claude gave me, and saved and exported again; I told Claude not to measure it again. I asked Claude to apply the same edit to the large crate. For the computer desks I chose a 0.7 m desktop, a monitor riser as the computer-desk feature, and dark-grey metal.
- **What Claude or another person contributed:** Claude Code (Claude Opus 5.5) wrote and ran the Blender Python through the MCP (the large crate's last version through the headless script route), ran the Godot headless checks, wrote the brief and the asset log from my decisions, and, when I asked, added the crates and desks to my item spreadsheet and the grid rule to my design document. Claude also taught me the parts of the Blender interface I needed (Edit Mode, selecting linked geometry, typing exact positions instead of dragging).
- **What I understand now / still do not understand:**
- **Evidence and next step:** `walker-survival-shooting/CHANGE-BRIEF.md` (revision 2026-10-15), `walker-survival-shooting/SOURCES.md` (rows PROP-TABLET-02 to COMPUTER-DESK-L-01), `walker-survival-shooting/tools/blender/`, `walker-survival-shooting/design/item_resource/`. Next: a Godot 3D scene with the three assets and a headless check script, BLENDER-NOTES.md, TEST-REPORT.md, and the explainer film.

---

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-10-15 | Add the Assignment 3 brief, Blender assets, and build scripts |
