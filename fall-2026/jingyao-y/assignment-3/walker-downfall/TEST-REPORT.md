# TEST-REPORT.md — A3 Blender assets in Godot

**Date:** 2026-10-12. **Tools:** Blender 5.4.0 Alpha (754ebe3c4b4e), Godot 4.7.2-stable, Windows 11.
**Who ran what:** Claude ran every automated check and Blender measurement below. The author's own check is under "HUMAN CHECK" and is recorded as the author reported it.

## Result

| Check | Result |
|---|---|
| Headless asset check `tests/test_a3_assets.gd` (25 checks) | **PASS, 0 failed** |
| Headless import (`--headless --import`) | **Clean** after loop 2's fix (one error before it) |
| Blender: rotation 0, scale 1, origin (0,0,0), lowest vertex z = 0 for all three | **PASS** (get_scene_info + mesh bounds) |
| Blender: inward-facing faces per mesh island (F7) | **0 of 10 islands** have any |
| HUMAN CHECK in Godot | **PASS, as reported by the author** (see below) |

## Predicted failures (CHANGE-BRIEF F1–F8): what actually happened

| # | Prediction | Check run | Actual result |
|---|---|---|---|
| F1 | Axis flip on export | Godot: Z of the ramp's highest vertices; cliff AABB max z | Ramp high end at z = −6.50 (towards −Z, as predicted). Cliff front at z = +0.30. **Did not happen.** |
| F2 | Unapplied transforms | Blender get_scene_info before save; Godot basis of every node | All rot (0,0,0), scale (1,1,1). Every Godot node basis is identity. **Did not happen.** |
| F3 | Origin in the wrong place | AABB min/max against the brief, ±0.02 | Cliff (−1.47, 0, −0.90)…(1.47, 2.40, 0.30); ramp (−3.5, 0, −6.5)…(3.5, 2.47, 0); rubble (−0.736, 0, −0.627)…(0.736, 0.847, 0.627). **Did not happen.** |
| F4 | Ramp geometry off | Blender: min clearance above slope plane; edge slope. Godot: edge slope | Clearance 0.02 (as designed). Slope 18.70° in Blender and in Godot. Crown 0.10 at y = 0.5. **Did not happen.** |
| F5 | Godot auto-imports `.blend` | Import log | **Happened.** See loop 2. |
| F6 | Over budget | Blender bmesh triangle count; Godot index count / 3 | 116 / 68 / 180, same in both. Primitives 4 / 3 / 3. **Did not happen.** |
| F7 | Flipped normals | Blender: faces pointing towards their island's centre | 0 inward faces. A render *looked* like flipped normals; the cause was the preview light (loop 3). **Did not happen.** |
| F8 | Colour not carried over | Godot `albedo_color` vs brief hex | All six colours exact: 443c31, 5a4f40, 988164, 6e6a60, 6b5e4c, 4f463a. **Did not happen.** |

Not predicted: the exporter marked every material double-sided, so Godot set `cull_mode = 2` (disabled). This is harmless for these closed meshes. It also means that a flipped face would *not* vanish in Godot, so F7's "faces vanish" symptom could never have shown there; the Blender count is the real F7 check.

## Check → problem → fix loops

### Loop 1 — cliff lip boulder buried (Blender, `look`)
- **Check:** `look` from front, right, top and three-quarter views after the four cliff parts were built.
- **Problem:** The 0.35-tall boulder was centred at z 2.225 on the top stratum (top at 2.25), so 0.2 of it was buried. It read as a flat disc.
- **Fix:** Call 6 in `build_cliff_wall_segment.py`. The boulder became 0.8 × 0.6 × 0.5 and moved to the front lip (y −0.30 … 0.30, z 1.90 … 2.40). A second `look` showed it bulging from the face. Brief R2.

### Loop 1b — rubble top stone floating (Blender, `look`)
- **Check:** `look` after the three stones were placed.
- **Problem:** rubble_c's bottom (0.51) cleared the stones under it. The front and right views showed a gap.
- **Fix:** Call 5 in `build_cliff_rubble_pile.py`. The stone was moved over rubble_a's peak and sunk 0.05 into it. The second `look` showed no gap. The pile's height became 0.85 (brief R1).

### Loop 2 — Godot tried to import the `.blend` files (F5)
- **Check:** First `--headless --import`.
- **Problem:** The log lists `arched_ramp_segment.blend`, `cliff_rubble_pile.blend` and `cliff_wall_segment.blend` in `_update_scan_actions`, then `ERROR: Blender path is invalid or not set, check your Editor Settings. Cannot configure blender path in headless mode.` (`editor_scene_importer_blend.cpp:552`). The same scan also picked up the PNGs in `a3/screenshots/`.
- **Fix:** Added an empty `art/blender/.gdignore` and `a3/.gdignore`, and deleted the stray `.import` files. The second import has no errors and no `.blend` lines; the three `.glb.import` files were written.

### Loop 3 — preview scene lit from below (Godot render)
- **Check:** `tests/capture_a3_preview.gd` rendered the preview scene. Claude looked at the PNGs.
- **Problem:** The stone tops were black while their sides and the ramp's end face were lit. It looked like inverted normals. A Blender count (0 inward faces) and a no-shadow close-up ruled that out. The real cause: in a `.tscn`, `Transform3D(...)` lists the basis **by rows**. Claude had written the sun's basis by columns, so the light pointed upward. The camera's basis is symmetric, so it was unaffected.
- **Fix:** The sun's transform in `art/models/asset_preview.tscn` was rewritten as its transpose. The re-render shows lit tops and ground shadows. `test_a3_assets.gd` still passes; the light is not part of what it checks.

## What the headless check proves, and what it does not

It **proves**, for the imported `.glb` as Godot sees it:
- Each asset's bounding box matches the brief within 0.02 m, so origin, orientation (ramp up towards −Z, cliff front towards +Z) and size are right.
- No node carries rotation or scale.
- Triangle counts match Blender and stay under budget.
- Each flat colour arrives exactly.
- The ramp's edge slope is 18.7° (≤ 19°).

It **does not prove**:
- That the assets *look* right; only the renders and the human check speak to that.
- That they fit the real procedural terrain. They are not placed in the game; the brief puts that out of scope.
- That normals face outward, because cull is disabled (see above).
- That the crown and kerbs read from the game's camera.
- Anything about collision: there is none, by design.

The expected numbers in the script come from the brief **and from Claude's own Blender measurements**, so the triangle counts and exact bounds are a consistency check (Blender → glb → Godot), not an independent one.

## Renders (captured by Claude, `tests/capture_a3_preview.gd`)

- `screenshots/claude-godot-preview-gamecam.png`: the game camera (orthographic size 24, offset (0, 16, −10), as `GameManager`).
- `screenshots/claude-godot-preview-front.png`: perspective from +Z, in front of the cliff face.

What Claude saw in them, which is not a human check:
- From the game camera, the cliff's front face (+Z) points **away** from the camera. Only its top and back show.
- The ramp's tall high-end face (z = −6.5) faces the camera. In the game it would be against the upper terrace and hidden.
- The crown shows as a faint centre crease in the perspective view, and not at all from the game camera.
- The capsule (1.7 m, blue) is a scale reference only.

## HUMAN CHECK

**Done by the author, 2026-10-12**, in the Godot 4.7.2 editor on `art/models/asset_preview.tscn`. Claude gave a step list beforehand: orbit, pan and zoom; focus each asset with F; front, rear, side, top and bottom views with the ground hidden; and the game camera's Preview.

**The author's report, verbatim:** "都是对的" ("everything is correct").

The author gave no further detail: not which views they used, nor any per-asset observations. So this records only that the author looked and found nothing wrong. It does not record a judgement on any specific item from the step list, such as whether the crown is readable from the game camera.

| Item | Result |
|---|---|
| HUMAN CHECK | **PASS, as reported by the author** ("都是对的") |
