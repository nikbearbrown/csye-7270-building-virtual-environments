# Test report — Assignment 3

**Environment:** Blender 5.2.2 LTS (Windows, portable build, Simplified Chinese interface); Godot 4.7.2-stable (Windows, Forward Plus, Jolt Physics); Windows 11 Home; MCP for Blender: server package `mcp-for-blender` 2.1.9 (according to the uv cache), Blender add-on version 1.8. All checks were run on 2026-10-15.

**The three assignment assets:** the chair (ENV-SEAT), the tablet (PROP-TABLET), and the weapon crates (large crate CRATE-LONG `big_box` + small crate CRATE-CUBE `small_box`). The two computer desks are extra project assets and were checked too.

**Check commands (headless; the script `tests/a3_asset_check.gd` was written by Claude):**
```
godot --headless --path godot --import
godot --headless --path godot --script res://tests/a3_asset_check.gd --fixed-fps 60
```
(The assignment's commands are written for macOS. On Windows I used `Godot_v4.7.2-stable_win64_console.exe` in place of `godot`, and wrapped the second command in Git Bash's own `timeout 120`.)
Final result: **56 PASS, 0 FAIL, exit code 0** (`test-logs/a3_check_2026-10-15_v3_latch-fixed.log`).

---

## 1. Interface notes
The six parts of the interface are described in my own words in `BLENDER-NOTES.md`; the screenshot is from my own Blender session: `design/blender-notes/blender-session-01.png` (Edit Mode, one latch of the small crate selected, the sidebar showing its median coordinates).

## 2. Size: brief / Blender / Godot

The Blender column was read by Claude in headless Blender from `object.dimensions` (the same value the sidebar's Dimensions shows); I did not copy it from the sidebar by hand. Blender is Z-up and Godot is Y-up, so in the Godot column the height is the second number.

| Asset | Brief (width × depth × height, m) | Blender dimensions (X × Y × Z) | Godot bounding box (X, Y, Z) | Result |
|---|---|---|---|---|
| Chair | 0.44 × 0.42 × 0.90 | 0.44 × 0.42 × 0.90 | 0.44, 0.90, 0.42 | Match |
| Tablet | 0.242 × 0.028 × 0.162 | 0.242 × 0.028 × 0.162 | 0.242, 0.162, 0.028 | Match |
| Large crate | 1.0 × 0.5 × 0.4 | Overall 1.0 × 0.5 × 0.4 (body 1.0 × 0.5 × 0.355, lid 0.94 × 0.485 × 0.08) | 1.0, 0.4, 0.5 | Match |
| Small crate | 0.5 × 0.5 × 0.5 | Overall 0.5 × 0.5 × 0.5 (body 0.5 × 0.5 × 0.454, lid 0.44 × 0.485 × 0.08) | 0.5, 0.500006, 0.5 | Match (0.006 mm off) |
| Computer desk | 1.5 × 0.5 × 0.78 | 1.5 × 0.5 × 0.78 | 1.5, 0.78, 0.5 | Match |
| L-shaped computer desk | 1.5 × 1.0 × 0.78 | 1.5 × 1.0 × 0.78 | 1.5, 0.78, 1.0 | Match |

(The crate body's size includes the handles and latches, which is why the body is 0.5 wide and the lid 0.44 wide.)

## 3. Upright and scale
- Every asset has its height on Godot's Y axis (see the table), so it stands upright.
- Every node scale is 1, 1, 1 (the check script checks each node). In Blender every object has rotation 0 and scale 1 (transforms applied before export).

## 4. Origin
- Chair, both crates, both desks: origin at the bottom centre; loaded on their own, their lowest point is y = 0.
- Tablet: origin at the geometric centre, lowest point y = −0.081, kept on purpose in the brief (so it can later be attached to the hand).
- Placed in `base.tscn`: the floor top is y = 0.250 (the check script reads it from the floor node `room/floor` itself, not from an asset). The bottoms of the chair, both crates and both desks are at y = 0.250: **they sit on the floor and do not float**.
- Crate lids: origin on the back hinge; after `open` the lid is at −100°, after `close` back at 0°.

## 5. Triangles and shape count
| Asset | Triangles (budget ≤ 500) | Shapes (course limit 6) |
|---|---|---|
| Chair | 72 | 6 |
| Tablet | 388 | **21 (over; I decided to keep it)** |
| Large crate | 88 | 6 |
| Small crate | 88 | 6 |
| Computer desk | 72 | 6 |
| L-shaped computer desk | 72 | 6 |

The check script computes the triangles from the imported meshes, and Claude also counted them in Blender with a script. I also turned on Scene Statistics in Blender's status bar, and the numbers match.

## 6. Imports and appears in the scene
- `--import` printed no errors or warnings. All six `.glb` files got their `.import` files.
- All are placed in `base.tscn` (my indoor subway-base scene): the chair in its old place by the back wall; the two crates to the right of the chair; the two desks to the left of the chair, against the back wall; the tablet floating beside the large crate (see section 8).
- The check script confirms: the footprint edges of every piece of furniture except the chair sit on the 0.1 m grid, and no two assets' bounding boxes overlap.

## 7. HUMAN CHECK (what I saw myself)
- In Godot I could **recognise at a glance** the chair and the two crates, and the tablet too (at that time it was lying flat on one of the crates). The two desks also look normal.
- Under the original lights the objects were hard to see, so **I moved one light** to shine on them.
- **I moved the tablet into the air and tilted it** to make it easier to look at.
- The sizes of the objects relative to each other look right. But **there is no character model yet**, so I am not sure yet about their scale next to a person.
- From behind and from below: I looked at those too.
- Missing faces or wrong colours: I found nothing to report.
- Nobody else has looked at the scene.

## 8. Inspect-and-revise cycles (evidence)
1. **Tablet triangle cut:** the 2026-10-12 version had 804 triangles, over 500. Keeping bevels only on the body and the four corner bumpers brought it to 388 (PROP-TABLET-02).
2. **Crates onto the grid:** the first crates' handles and latches stuck out, so their footprints were 1.26 × 0.515 and 0.56 × 0.515 m, off the 0.1 m grid. After I set "1 cell = 0.1 m, large crate 1.0 × 0.5", the second version moved the handles and latches inside the footprint: exactly 1.0 × 0.5 and 0.5 × 0.5 (confirmed by the headless bounding boxes).
3. **Chair shape cut:** 9 boxes was over 6; removing the two stretchers and merging the two backrest slats into one board made it 6 (ENV-SEAT-02).
4. **Small-crate latches (my hand edit):** I raised the latches onto the seam between the lid and the body and moved the handles up. Claude measured that the right latch had been stretched to 0.10 m deep, into the box, and that left and right were 2 mm apart. I said it was fixed, but **my first fix never reached the saved files**: when the numbers for this report were collected, the `.blend` and `.glb` still had the 0.10 m latch. On my second try I deleted the right latch, duplicated the left one, saved and exported. Measured again: 0.015 m deep and the same height on both sides; the right latch centre is at X +0.129 against −0.123 on the left, 6 mm off (fine for the design, so I kept it); and the duplicate had left an extra latch on top of the left one, which Claude deleted at my request, bringing the shape count back to 6.
5. **Tablet placement and the check script:** the check script used to check "the tablet lies on the large crate's lid". After I moved the tablet into the air, that check **failed** (`test-logs/a3_check_2026-10-15_v1_tablet-moved.log`, exit code 1). Because the placement itself had changed, the check became "the tablet is above the floor and touches no other asset", with the reason written in the script. This was not deleting a failing assertion to turn the report green; the failing run is kept.

## 9. What Claude got wrong
1. **Built more than I asked for:** for the tablet I asked for "a greybox blocked out with cubes"; Claude built 21 bevelled parts and 804 triangles.
2. **First brief draft:** it marked things I had already decided (one long and one square crate, military green) as "chosen by Claude" or left them blank; I corrected it.
3. **First crates off the grid:** the handles and latches stuck out of the footprint (section 8, item 2).
4. **Overwrote a file by accident:** while extracting the build code, Claude's script tried to point the export path at a temporary folder, the replacement did not take effect, and the re-export overwrote `test_chair.glb` in the Godot project (same size and dimensions).
5. **Wrote "fixed" without checking:** after my first latch fix I told Claude not to measure again, and Claude wrote "fixed" into SOURCES and FRICTIONAL and pushed that to the course repo in commit `ce90608`, while the files were in fact not fixed yet (section 8, item 4). This upload corrects it.
6. **Small slips Claude caught and fixed itself:** the first extraction of code from the session transcript used the wrong call numbers; the first chair rebuild split the file on the wrong marker and raised an AttributeError.

## 10. What the check does and does not show
- **It shows:** the assets reached Godot at the size, orientation and scale I measured; where the origins are; that triangles are within budget; that the crate animations exist and turn to the right angles; that placed assets sit on the floor, fit the grid and do not overlap.
- **It does not show:** whether the assets look right, whether their colours can be told apart under the game's lighting, whether they read as what they are, or whether they suit the style. That is my own check (section 7). Also, "on the floor" only means the assets are where we put them, not that that is a sensible place; and non-overlapping bounding boxes do not prove the meshes never interpenetrate (the L-shaped desk's bounding box is the whole rectangle).

## 11. Known limitations
- No character model yet, so the scale next to a person is not verified.
- The tablet has 21 shapes, over the course limit (my decision to keep it).
- When a crate opens, the lid swings about 8 cm behind its footprint; placed against a wall it would pass through the wall.
- The chair is 0.44 × 0.42 m, not a whole number of grid cells.
- In my item spreadsheet the L-shaped desk can only be recorded as a 15 × 10 rectangle, though it really covers 100 cells in an L.
- The small crate's right latch is 6 mm off compared with the left one.
- The brief was written after the chair and the tablet were made (the brief says so).
