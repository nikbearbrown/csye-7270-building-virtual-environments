# CHANGE-BRIEF.md — Downfall, Assignment 3: first Blender assets

**Written:** 2026-10-12, before any modelling. This brief predicts; it is not a retrospective.
**Author:** Yuan Jingya, drafted with Claude Code (Claude Opus 5.5). The design decisions marked "user's decision" were made by the author in chat.
**Rule:** After approval this text is never edited. Corrections go under "Revisions" at the end, dated.

## Context

Downfall's field maps were recently changed to terraced levels. The source is `world/continuous_world_map.gd` and the design note `地图场景改造.md`, section "立体分层与出口随机" (2026-10-12). Every geometric number below comes from those two files:

| Game constant | Value | Meaning |
|---|---|---|
| `TIER` | 2.2 | Height of one terrace level (levels at 0 / 2.2 / 4.4) |
| `RAMP_RUN` | 6.5 | Minimum horizontal run per tier of ramp. 2.2 / 6.5 → atan = **18.7°** |
| `RAMP_APRON` | 2.0 | Flat stretch at each end of a ramp, part of the room floor |
| `CLIFF_STEP` | 0.9 | Rise over 1.5 m above which ground counts as cliff |
| `_corridor_width()` | 3.4–5.6 | Corridor **half**-width (distance from centre line; see `continuous_world_map.gd:756`). Full width 6.8–11.2 m; snow +0.5, city +0.3 per side |

The ramp height profile is a linear `lerpf` between the two tiers (`_link_height`). The terrain mesh is sampled on a 1.5 m grid.

**Reference: how Grim Dawn does it.** The official modding guide documents heightmap terrain, built with the Plateau, Raise Plateau and Ramp tools, and No Pathing painting. Rocks and bridges are placed as decorations on top. Downfall works the same way: the terrain mesh already provides each ramp's and cliff's shape and collision. **These assets are therefore visual dressing.** They are laid onto that terrain and carry no collision of their own. This round they appear in a test scene only; placing them along real cliff lines and ramps in the generator is out of scope.

**Axes.** Blender is Z-up. Export is glTF with +Y Up, so Blender +Y becomes Godot −Z and Blender −Y becomes Godot +Z.

**Colours.** They follow the mine region (`terrain_surface.gd`): floor `#615646`, road `#988164`, cliff face 0.7 × floor. Every material is a single flat base colour in a Principled BSDF, with no textures.

## Assignment limits (all three assets)

- At most 6 primitives per asset and **under 500 triangles** each.
- Flat-colour materials only. No sculpting, texture painting, rigging or animation.
- One `.blend` per asset in `art/blender/`. Modelled around the world origin, with the bottom on the ground (lowest vertex at z = 0).
- Rotation and scale are applied before saving (rotation 0, scale 1).
- Every line of Blender code is kept verbatim in `tools/blender/build_<asset>.py`.

---

## Asset 1 — `cliff_wall_segment`

- **Purpose:** It covers the vertical rock face that `TerrainSurface._cliff_split` creates where two terraces meet with no ramp between them. It breaks up that flat face, and hides the two seams: low floor to face, and face to upper rim.
- **Where it appears:** Repeated along a cliff line on the low side. Each segment is rotated to the local direction of the line. Neighbouring segments **overlap** about 0.2 m rather than tiling seamlessly, as Grim Dawn's cliff rocks do. The line is curved, so a seamless tile would open gaps.
- **Size (m):** 3.0 wide (X) × 1.2 deep (Y) × 2.4 tall (Z).
  - Height 2.4 = one `TIER` (2.2), plus 0.1 sunk below the low floor, plus 0.1 standing above the upper rim. Both seams are covered.
  - Depth 1.2: at most **0.3 in front** of the face line (towards the low floor), and 0.9 behind it, buried in the upper terrace. The collision wall stands at the face line, so anything further forward would be rock the player visibly walks into.
  - Width 3.0: two segments cover a typical 1.5 m-sampled cliff edge run with overlap. This is a judgement call, not a game constant.
- **Origin (user's decision):** On the bottom, at the midpoint of the **face line**: x = 0, y = 0, z = 0. The rock occupies y ∈ [−0.3, +0.9]. The front faces −Y in Blender, which is +Z in Godot. Placement puts the origin on the cliff line at low-floor height − 0.1.
- **Look:** Three stacked, slightly mis-rotated rock strata (boxes, ±3° about Z, leaning back about 4°). The top stratum steps back from the bottom one. One low-subdivision icosphere boulder sits on the top lip. Colours: strata `#443C31`, a darker cliff-face brown; boulder `#5A4F40`.
- **Primitives:** 4 (3 cubes + 1 icosphere).
- **Triangle budget:** ≤ 300 (estimate about 36 + 80 = 116).

## Asset 2 — `arched_ramp_segment`

- **Purpose:** A visual overlay that sits on the terrain's ramp. It reads as a built road with a cambered surface and kerbstones, instead of bare sloped ground. Collision stays with the terrain.
- **Where it appears:** On the sloped middle stretch of a corridor that joins rooms of different tiers, between the two 2.0 m aprons.
- **Size (m):** 6.8 wide (X) × 6.5 run (Y) × 2.2 rise, plus a 0.10 crown and 0.25 kerbs.
  - Rise 2.2 = one `TIER` (user's decision: one segment per whole tier).
  - Run 6.5 = `RAMP_RUN`, so slope = **18.7°**, inside the 19° limit. In the game a ramp's run is *at least* 6.5. A longer ramp is matched by scaling the segment along its length. The kerbs run lengthwise, so this does not distort them.
  - Width 6.8 = the narrowest corridor's full width (2 × 3.4). **Known limit:** a wider corridor (up to 11.2) needs X scaling, which also widens the kerbs (0.3 → up to about 0.5). Accepted for this round.
  - Crown 0.10: the cross-slope over 3.4 m is about 1.7°, which is purely visual.
- **Origin:** Bottom, at the midpoint of the **low-end edge** (0, 0, 0). The ramp rises towards +Y in Blender, which is −Z in Godot.
- **Shape:**
  - **Road body (1 primitive):** a plane, edited into a solid wedge. The flat bottom is at z = 0; the bottom is hidden inside the terrain in the game.
  - **Top surface:** follows the slope `z = 2.2 · y / 6.5`, plus a camber. The camber is 0 at the side edges and 0.10 on the centre line. It tapers from 0 to full over the first and last 0.5 m, so both ends meet the flat apron with no lip. The side-edge top sits **0.02** above the slope plane, so the overlay never z-fights the terrain.
  - **Kerbs (2 primitives):** one per side, as a box edited so its bottom lies on the slope and its ends are vertical. Each is 0.3 wide × 0.25 tall × 6.5 run, centred at x = ±3.25, so the outer edge is at ±3.4, the corridor's carved edge.
- **Colours:** road `#988164` (the mine road colour); kerbs `#6E6A60`, grey stone.
- **Primitives:** 3.
- **Triangle budget:** ≤ 200 (estimate about 70).

## Asset 3 — `cliff_rubble_pile`

- **Purpose:** Scatter at the foot of a cliff. It breaks the straight line where the cliff face meets the low floor, as Grim Dawn's cliff-foot debris does.
- **Where it appears:** On the low floor against `cliff_wall_segment`, every few segments, within the 0.3 m front zone plus about 1 m. It is decoration only and must not narrow a corridor below its walkable width.
- **Size (m):** about 1.5 × 1.5 × 0.9. That is about half a cliff segment wide, and under the 0.9 `CLIFF_STEP`, so it reads as debris, not as a new step.
- **Origin:** Bottom centre (0, 0, 0). The lowest vertex is at z = 0.
- **Look:** Three flattened icospheres: two of about 0.9 m and one of about 0.5 m, leaning into each other. Colours: `#6B5E4C`, plus one stone in `#4F463A` so the pile does not read as one blob.
- **Primitives:** 3 icospheres (subdivisions 2, 2, 1).
- **Triangle budget:** ≤ 250 (estimate 80 + 80 + 20 = 180).

---

## Predicted failures and how each will be checked

| # | Prediction | Check |
|---|---|---|
| F1 | **Axis flip on export.** The ramp rises towards Godot +Z instead of −Z, or the cliff's front faces into the upper terrace. | The headless Godot script prints each mesh's AABB and the Z of the ramp's highest vertices, and checks the sign against this brief. |
| F2 | **Unapplied transforms.** Rotation or scale left on the object, so Godot reports scale ≠ 1, or the bounding box differs from the mesh data. | Before each save, `get_scene_info` shows rotation (0,0,0) and scale (1,1,1). The Godot script prints every node's scale and basis. |
| F3 | **Origin in the wrong place.** For example the AABB min z ≠ 0, the ramp's low edge not at y = 0, or the cliff's face not at y = 0. | Blender: print the bounding box per axis. Godot: compare the AABB min/max with the expected ranges (tolerance 0.02 m). |
| F4 | **Ramp geometry off.** The slope is over 19°, or the crown or kerbs pass below the slope plane. | Print the slope from the vertex data, max(z)/max(y) for the edge rows. Assert that every top vertex is ≥ the slope plane + 0.02. |
| F5 | **Godot auto-imports the `.blend` files.** Godot 4 has a Blender importer, so it may try to run Blender on `art/blender/*.blend` during `--import`. | Read the `--headless --import` log. If it happens, add `art/blender/.gdignore`. |
| F6 | **Over budget.** A higher icosphere subdivision or an extra loop cut pushes an asset past 500 triangles or 6 primitives. | Blender: count triangles after triangulating, in the script. Godot: count `surface_get_arrays` indices / 3. |
| F7 | **Flipped normals** on the hand-edited meshes (wedge, kerbs). Godot culls back faces, so faces vanish or turn black. | Recalculate normals outside, then `look` from all sides in Blender. Human check in Godot, including the back and the underside. |
| F8 | **The material colour does not carry over.** The colour was set on the viewport colour instead of the Principled node, so the glb arrives white. | The Godot script prints each surface's `albedo_color` and compares it with the hex values above. |

## Approval

- [x] Approved by the author in chat on 2026-10-12 ("同意"), with the docs folder `a3/`. From here on, only revisions are appended.

## Revisions

(none yet)
