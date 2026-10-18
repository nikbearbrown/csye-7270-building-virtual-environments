# Build notes: SEIS AI Lab reference body, study v003

`163 meshes · 410,800 triangles · 8 materials in the GLB · no rig · about 1.9 m tall · Blender 5.1.2`

## What it is

A body-only study built by `scripts/build_body.py`: an hourglass torso, rounded shoulder shells, large gauntlets, slim long thighs, visible knee joints and flared greaves, in the saved Northeastern palette (C8102E red, A4804A and C8A978 golds, 49494D and 9B9C9E grays, FFFFFF white, 1E2028 cool black). Each part carries a `body_group` custom property (arm_l, arm_r, body, head_placeholder, leg_l, leg_r).

## What I measured

`scripts/count_scene.py` on the .blend (Blender 5.1.2): 164 mesh objects, 410,802 triangles, 10 materials, 0 armatures, 0 bones, 1 camera, 3 lights (`reports/scene-counts-seis_robot_reference_body_v003.json`). The floor plane accounts for one mesh and two triangles over the source's 163 meshes and 410,800 triangles.

GLB inspection: 0 images, 0 textures, 8 materials, 0 skins, 0 animations.

## What the source reports (not re-run by me)

- Geometry checks PASS: finite geometry, applied transforms, materials, anatomical group inventory; chest 6 present. Not a topology, rig, engine or design-approval check.
- GLB re-import in Blender: 163 meshes, 410,800 triangles and dimensions match.
- Six renders at 1400 x 1800. The supplied reference copies match their originals byte for byte (delivery.json).

## Scope

The source's own words: the body is the current review decision; the helmet is a temporary blank placeholder isolated by `body_group=head_placeholder`; no rig or controls. Rebuild with `scripts/build_body.py` in a fresh background Blender; the Lato Bold font path points outside this repository.

## Not copied

review.html, the `.blend1` backup, anything else outside the list above.

## Built by

- **Builder:** Codex (OpenAI). Builder identified from Codex session logs on this machine dated 2026-10-18, not from a label in the folder; no product or model version is stated in the files.
- **Method:** Scripted: Blender Python (scripts/build_body.py), built from scratch; the source says no geometry from v001 or v002 was reused and no MCP invocation or paid API was used. The source records one inspect-and-fix pass on the rendered views (the raised calf vent positions were corrected) and a six-view render pass; it does not log numbered render-versus-reference rounds. review.html in the source puts the front photograph beside the render for human judgment. The compare images in this folder were made afterwards for this page, by eye.
- **Tools:** Blender 5.1.2 (confirmed by my scene count); Lato Bold for the 6; the source's GLB re-import check in Blender (163 meshes, 410,800 triangles and dimensions match). No game-engine import or animation test.
- **Build date:** 2026-10-17 (file times 18:13 for the .blend and 18:15 for the GLB; delivery.json is dated 2026-10-17)
- **Human review:** Professor Bear: pending. The source README.txt says: "The body is the current review decision." and "The previous v002 body was rejected as too similar to the original robot." delivery.json says: "Awaiting Bear review; static body study; final head and wrist deferred", and README.txt says: "Technical checks do not establish Bear's approval of the design." The files do not say who rejected v002 or when.

## Known limitations

- This is a design study, not a final model.
- The helmet is a temporary placeholder, not the proposed SEIS face; the box head, antenna, waveform mouth, engineer connector, spool housing and wrist display are deferred.
- Static: no animation rig, no pose controls, no speech sync, no working tools. The source says it is a high-resolution visual study, not game-optimised geometry.
- At 410,800 triangles it is about eight times heavier than the v001 robots and not a game-ready asset.
- The photographs are of a black-and-gold figure; the model is deliberately red, gold, gray, white and black in Northeastern colours, so colour is not comparable. Shape likeness is moderate and cruder; see Compare.
- No reference photograph shows a true side view, so there is no side comparison.
- Counts: my count_scene run reports 164 mesh objects and 410,802 triangles, which is the source's 163 meshes and 410,800 triangles plus a 2-triangle floor plane; 10 materials in the .blend against 8 in the GLB. Height about 1.9 m (the source's audit says about 1.89 m; my count gives 1.905 m including the floor plane's offset).
