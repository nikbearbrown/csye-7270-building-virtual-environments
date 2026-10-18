# Ultron-style armoured robot, v4 (Blender 4.2.3, headless)

v1, v2 and v3 are untouched (/workspace/robot, /workspace/robot/v2, /workspace/robot/v3). v4 is in /workspace/robot/v4.
v4 refines the face and shoulders on top of v3. The round-by-round log is in PROGRESS.md.

## Deliverables
| File | Size | Notes |
|---|---|---|
| robot_standing.blend | 25.30 MB | Standing pose active, no plinth |
| robot_seated.blend | 25.30 MB | Thinker pose on the stepped stone plinth |
| robot_build.blend | 25.30 MB | Build output (= v4r5.blend) with both actions and all cameras |
| v4r1.blend ... v4r5.blend | about 24 MB each | Milestone build of every round (for the build-breakdown film) |
| robot_v4.glb | 4.07 MB | Full geometry (1,481,252 tris), Draco level 7, skinned rig with 50 joints, actions Standing and Thinker, **flat PBR colours** + emissive eyes |
| audit_standing.json / audit_seated.json | 1 KB | Both PASS |
| renders/final/gallery/ | | 11 images (same set as v3) |
| renders/prev/rN_*.png, compare/v4rN_*.png, compare/v4final_*.png | | Per-round previews and side-by-sides against the reference crops |

Fixed compare cameras (identical in every round): Cam_HeadFront, Cam_Head34, Cam_HeadSide, Cam_Shoulder34, Cam_Stand_34 (Standing) and Cam_Front (Thinker).
v4r0 = the v3 state. Not every camera was rendered every round; see renders/prev/.

Gallery: 01_seated_front_2400x3000 (24 samples); at 1200x1500 / 40 samples: 02_seated_front, 03_seated_three_quarter, 04_seated_side,
05_seated_back_three_quarter, 06_standing_front, 07_standing_three_quarter, 08_head_closeup_front, 09_head_closeup_side,
10_chest_six_closeup, 12_shoulder_three_quarter. Cycles CPU + OIDN, AgX Medium High Contrast (exposure -0.5), compositor Fog Glow on the eye cores.

## What changed from v3
- **Face, layered plates:** the brow/forehead mask, cheek plates, muzzle and new jaw side plates now stand off the skull at stepped
  depths with real thickness (brow 6.8 mm + 5.5 mm thick, cheek 4.6 + 5, muzzle 3.4 + 5.5, jaw 2.8 + 4.5). The brow overlaps the cheeks
  and the cheeks overlap the muzzle and jaw. Black gap strips run along every plate border.
- **Cut pattern:** six angled grooves per side sweep from the keystone edge back over the dome; grooves run from the brow corners up to the temples;
  diagonal cuts on the cheek plates; lines on the brow plates.
- **Eyes:** orbs about 25% larger (white-hot core scaled with them); the socket glow is larger and about 3x stronger.
- **Lower face:** wider, squarer jaw silhouette (lower skull rows widened); wide flat muzzle with a straight bottom (no V tab) and a long horizontal black mouth line.
- **C-frames:** stand 18 mm off the skull with a black gap strip underneath; round hinge discs (dark disc, silver ring, black hub) at the cheek/jaw hinge.
- **Shoulders:** the three stacked cowl shells (which made the 3/4 ledge) are replaced by one big smooth hood per side that follows the shoulder
  and wraps down over the deltoid, with a rolled lip along its lower edge, a thick front rim, bronze trims and a mid groove.
  Three long inner arcs per side run from the top of the shoulder in toward the neck and down onto the chest V plates,
  each with a bronze outer-edge trim and a black gap strip beneath.

## Technical record
- 1,179 separately named mesh parts. 1,481,252 evaluated triangles (same in both poses).
- 50-bone FK armature including finger and thumb bones; parts are rigidly bone-parented.
- Height 2.21 m standing. Metric units, Z up, front is -Y.
- 14 procedural materials (Armor_Gunmetal, Armor_Gunmetal_B, Armor_Gunmetal_Flat, Bronze_Worn, Decal_White, Eye_Core, Eye_Glow,
  Eye_SocketGlow, Face_Silver, Mech_Dark, Muscle_Red, Paint_Red, Panel_Groove, Socket_Black) plus the plinth stone.
  Distressed procedural finish (edge wear, scratches, grime, dents, chipped paint) in the .blend files and renders.
- Legible white "6" (DejaVu Sans Bold text mesh) on the sternum plate.
- Thinker pose: torso grid search plus two-bone IK baked to FK; left hand drooping over the left knee.
- Audit (naming, materials, non-manifold, zero-area faces, parenting): PASS for both files.

## Scripts
- build_v4.py (about 40 s; `BUILD_NAME=x.blend` writes a milestone file instead of robot_build.blend), lib.py, materials.py, poses.py.
- save_variants.py, audit.py, render.py, render_gallery_v4.sh, prev.sh, compare.py, export_flat.py (`-- full`), glbinfo.py.

## Honest limitations
- **No baked textures in the GLB:** flat PBR colours, metallic/roughness and emissive eyes only. The distressed look is only in the .blend files and renders.
  The eye bloom is a compositor effect and does not exist in a glTF viewer.
- No lite (uncompressed) GLB was made for v4 (not requested this round); v3's export script supports `-- lite`.
- Shoulder hood: the ledge is gone, but the hood still reads as a fairly round dome in the 3/4 view. The ref hood is a longer,
  more sculpted curved plate, and its rolled lip is more pronounced than ours (ours is mostly hidden behind the arm in front views).
- The inner arcs lie on the chest and over the hood's inner edge; they are swept bands, not overlapping solid shells, and they do not continue down the back.
- Face plates are projected shells with uniform thickness (rounded by subdivision), not hand-sculpted forms; the plate pattern is simpler than the ref.
- Gaps between plates are black strips under the plate edges, not true cut-throughs.
- Mesh count 1,179 (below the original ~1,500 target).
- Plain grey studio, no environment.
