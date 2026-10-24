# CHANGE-BRIEF — Assignment 3: three 3D assets

> Version 1, committed before any asset is built. Later revisions are appended below with a date; this original is not rewritten.
> Drafted by Claude (claude.ai chat) from my decisions; sizes, colours and budgets reviewed and approved by me. Triangle counts in "Measured in my Blender session" are my own readings (see BLENDER-NOTES.md).

## Scale reference
- 1 Blender unit = 1 metre = 1 Godot 3D unit. No unit conversion anywhere.
- The player character (the fire mage) counts as **1.45 m** tall in 3D. Every size below is justified against that height.
- Tolerance: each measured dimension must be within **±0.02 m** of this brief.

## Axes and origin (all three assets)
- Built in Blender (Z-up) around the world origin, base resting on Z = 0, one asset per .blend file.
- Origin: **centre of the underside**, at the world origin. Reason: Godot places an imported scene at its node position, so a node at floor height puts the asset on the floor, not half inside it.
- Rotation and scale applied before export: the Blender sidebar must show rotation 0, 0, 0 and scale 1, 1, 1.
- Front faces Blender −Y. Prediction to check: after glTF export with +Y Up, the front faces Godot +Z (toward a default camera placed in front).
- Export: binary glTF (.glb), +Y Up on.

## Measured in my Blender session (Blender 5.2.2 LTS, Scene Statistics)
| Shape | Settings | Triangles |
|---|---|---|
| Cube | default | 12 |
| UV sphere | default (32 segments, 16 rings) | 960 |
| Ico sphere | default (subdivisions 2) | 80 |
| Ico sphere | subdivisions 1 | 20 |
| Cone | default (32 vertices) | 62 |
| Cone | 6 vertices | 10 |
| Cylinder | default (32 vertices) | 124 |
| Cylinder | 8 vertices | 28 |

A default UV sphere alone is almost twice the course limit of 500, and one default cylinder is a quarter of it, so every curved part below uses the reduced settings.

Also observed: these shapes are not equally wide in every direction. An ico sphere at subdivisions 1 measured 1.79 × 1.70 × 2.00 m, and a 6-vertex cone 1.73 × 2.00 × 2.00 m, both created with a 1 m radius. Sizes must therefore be checked against the measured dimensions, not set from the radius.

## Asset 1 — Rock
- **Role in game:** a roadblock on the path that the player has to jump over. Its gameplay collision will be a simple box (added in a later assignment, not here).
- **Size (W × D × H):** 1.0 × 0.8 × 0.7 m. Below the mage's waist: it blocks walking, she can see past it, and it reads as something to jump over rather than a wall. Whether 0.7 m is jumpable depends on the 3D jump height, which is not designed yet; that check belongs to a later assignment.
- **Shape constraint from the collision box:** the silhouette should stay close to its bounding box (no long spikes sticking out), so a box collider will match what the player sees.
- **Build:** 3 ico spheres at subdivisions 1, scaled, overlapped and slightly rotated so the silhouette is irregular and angular.
- **Look:** main colour **#343539** (the grey top surface of my Assignment 2 cave ground tile); the top stone in **#797069** (the tile's top-edge highlight, a warm grey-brown). Both are sampled from assets/sprites/env/cave_ground_tile.png. I chose these lit-rock colours rather than the tile's main fill #1A1C25 because a 3D material is shaded again by the scene light, and a near-black base would lose its shape.
- **Triangle budget:** 200 (measured basis: 3 × 20 = 60).

## Asset 2 — Crystal
- **Role in game:** decoration; a cold glow in the cave scenery. Not collectible, no collision.
- **Size (W × D × H):** 0.35 × 0.35 × 0.6 m. About thigh height: easy to spot, clearly smaller than the mage.
- **Build:** 3 cones with 6 vertices each, one tall and two short, leaning in different directions from a shared base.
- **Look:** deep cold blue **#3558C8** with a weak emission in the same colour, chosen for a mysterious feel. It is brighter and more saturated than every rock colour, so it stays readable against the dark cave (background mostly #0F1119 to #272A31). Cold on purpose: warm colour is reserved for fire (see the palette rule below).
- **Triangle budget:** 100 (measured basis: 3 × 10 = 30).

## Asset 3 — Treasure chest
- **Role in game:** appears at the exit after the level is cleared, as the reward.
- **Size (W × D × H):** 0.8 × 0.5 × 0.6 m (body 0.35 m + rounded lid 0.25 m). A classic RPG chest proportion, about thigh height on the mage.
- **Build (5 shapes):** cube body; 8-vertex cylinder laid along X as the rounded lid, half sunk into the body; small cube lock on the front; two thin cube metal bands.
- **Look:** deliberately warm: wood **#8A5A2B** for the body and lid, gold **#D4A73A** for the bands and lock. The chest marks the rest point after a cleared section, and later a torch or campfire will stand beside it, so its warmth belongs to the fire's warmth (see the palette rule below).
- **Triangle budget:** 150 (measured basis: 12 + 28 + 12 + 12 + 12 = 76).

## Palette rule (carried from Assignment 2, refined)
The cave is cold and low-saturation (slate blue-grey, grey-brown). **Fire is the only warmth.** Saturated warm colour appears only on fire and on what fire makes safe: the fireball and staff gem from Assignment 2, and from now on rest points such as this chest, with a torch or campfire beside it in a later assignment. The crystal stays cold so it never competes with fire.

## Why these budgets
Low-poly shapes suit the pixel-art character and keep each asset far below the course limit of 500. The budget leaves room to correct mistakes (for example a 12-vertex lid if 8 looks too coarse), and the measured basis makes it obvious if Claude builds more detail than asked: a chest at 172 triangles would mean a default 32-vertex lid.

## Predicted failure cases and checks
1. **Transforms not applied.** Rotated parts arrive with a node scale or rotation that is not clean. *Check:* Blender sidebar shows scale 1, 1, 1 and rotation 0 after applying; the Godot headless script prints each node's scale.
2. **Wrong way up.** An asset arrives lying on its side after the Z-up to Y-up conversion. *Check:* the headless script reports the bounding-box size per axis; height must be on Godot Y. Visual check in the scene.
3. **Origin in the wrong place.** Origin left at the centre, so the asset floats or sinks into the floor. *Check:* bounding-box minimum Y ≈ 0 in Godot; the asset placed on the floor visibly touches it.
4. **Wrong size by a factor.** For example 10× or 100× from a unit slip. *Check:* Blender sidebar dimensions and Godot bounding box both within ±0.02 m of this brief.
5. **Claude overbuilds.** More than six shapes, or default segment counts. *Check:* object count in the Outliner and the triangle count in Scene Statistics against the measured basis above.
6. **Crystal emission lost or changed in export.** *Check:* compare the Blender viewport with the Godot scene; inspect the imported material's emission.
7. **Chest lid misaligned.** Visible gap or overlap between lid and body. *Check:* orbit the camera to the side, back and below in both Blender and Godot.
8. **Sizes set from radius instead of dimensions.** Ico spheres and 6-vertex cones are narrower on some axes than their radius suggests (measured above), so a size computed from radius will miss the brief. *Check:* compare the sidebar dimensions, not the creation radius, with this brief.
9. **Colours drift between Blender and Godot.** Hex values typed into Blender may look different after export and under Godot lighting. *Check:* compare each material's base colour in Godot's inspector with the hex values above, and look at the assets in the Godot scene.

## Out of scope
Textures, sculpting, rigging, animation (the chest does not open), collision, the torch or campfire next to the chest, and placing the assets into the 2D game.

## Revision 2026-10-14 (after building; the original above is unchanged)
- **Chest:** the body/lid split came out 0.376 + 0.224 m instead of 0.35 + 0.25 m, because an 8-sided lid as deep as the body (lid 0.448 m, body 0.450 m) rises about half its depth, 0.224 m; a 0.25 m rise would need a 0.50 m deep lid, and the bands and lock would then push the chest past 0.5 m deep. The total height is still 0.600 m.
- **Chest gold:** metallic 0.3, roughness 0.5. Fully metallic gold read dark olive with a single light. Wood: metallic 0, roughness 0.8.
- **Rock:** roughness 0.9 (Claude Code's proposal, approved). Known limitation: a 0.066 m gap at the floor between the two base stones, accepted after my look.
- **Crystal:** emission strength 0.5, roughness 0.3. My hand edit rotated one short cone to Z = 20°; that cone was then lengthened ×1.2125 along its own axis to keep the 0.35 m width.
- All three assets matched the size, origin, rotation, scale and triangle predictions above; see TEST-REPORT.md.
