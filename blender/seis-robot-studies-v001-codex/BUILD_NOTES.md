# Build notes: SEIS AI Lab robot, design studies v001: compact and slim

`2 models · 135 meshes each · 51,536 (compact) and 51,984 (slim) triangles · 7 materials in the GLB · 17 bones each · 1.68 m (compact) and 2.08 m (slim) tall with antenna · Blender 5.1.2`

## What it is

Two robots built in one pass from one script, `scripts/build_robot.py`: **compact** (lead design) and **slim** (comparison). The compact version follows a boxy-body reference; the slim keeps the longer limbs of the earlier white mascot (the source's wording). Both share the face, materials and rig.

## What I measured

From `scripts/count_scene.py` run on each .blend (Blender 5.1.2): compact 136 mesh objects, 51,538 triangles, 8 materials, 1 armature, 17 bones, 1 camera, 3 lights. Slim 136 mesh objects, 51,986 triangles, 8 materials, 1 armature, 17 bones, 1 camera, 3 lights. Raw output is in `reports/scene-counts-*.json`. The two extra triangles and one extra mesh over the source's figures are the studio floor plane.

Glb inspection (read from the glTF JSON): 0 images, 0 textures, 7 materials, 1 skin and 0 animations in each GLB.

## What the source reports (not re-run by me)

- Compact: 135 meshes, 51,536 triangles, 7 materials, 0 textures, 17 bones, one root, size 0.878 x 0.619 x 1.6815 m. Slim: 135 meshes, 51,984 triangles, 7 materials, 17 bones, size 0.838 x 0.599 x 2.0765 m. Design-study budget 60,000 triangles per robot.
- Walker validator: zero errors and zero warnings for both. GLB export and re-import: mesh, triangle, bone counts and bounds match.
- Godot 4.7.2 import test: both pass (one 17-bone skeleton, 135 meshes, Speaking/Emphasis morphs reachable).
- Logs and JSON in `reports/` (paths made relative for this repository).

## Controls

Select `SEIS_Compact_Rig` (or `SEIS_Slim_Rig`) and enter Pose Mode: head, torso, arms, wrists, hips, knees and feet can be posed. On the mouth object, `Speaking` 0 hides the waveform and 1 shows it; `Emphasis` adds amplitude. The model opens in a speaking state.

## Method notes

Built headless with the installed Blender; no live Blender MCP connection and no paid generation services were used (the source says so). The scripts were copied with absolute paths replaced by placeholders. `scripts/build_robot.py` loads the Lato Bold font from a path outside this repository to make the 6; edit that path to rebuild.

## Files copied from the source

Both .blend files, both GLBs, 16 renders (PNG), the build, render, validator and round-trip reports, the scripts, and the two supplied reference images in `references/`. Not copied: the Godot verification project, `.blend1` backups, review.html.

## Built by

- **Builder:** Codex (OpenAI). Builder identified from Codex session logs on this machine dated 2026-10-18, not from a label in the folder; no product or model version is stated in the files.
- **Method:** Scripted: one Blender Python script (scripts/build_robot.py) builds either variant from primitives in a fresh background Blender. No sculpting and no AI image-to-3D. The source lists no numbered render-versus-reference rounds; it records one headless build per variant, a render pass, and mechanical checks. The compare images in this folder were made afterwards for this page, by eye.
- **Tools:** Blender 5.1.2 (confirmed by my scene count); Khronos glTF Blender I/O v5.1.20; the source's own validator (zero errors, zero warnings, both variants); Godot 4.7.2 import test recorded by the source (both pass). The source says the guide named Blender 5.2 LTS but 5.1.2 was what was installed.
- **Build date:** 2026-10-17 (file times 16:21 to 16:25 and START-HERE.txt; the folder's own note says October 17, 2026)
- **Human review:** Professor Bear: pending. The source START-HERE.txt says: "these first design studies still need Bear's aesthetic review."

## Known limitations

- This is a design study, not a final model.
- The compact is the source's "lead design" label, not a human decision recorded in the folder.
- Proportions differ from the supplied drawing (huge head on a squat body in the compact); the drawing's distressed ink texture, rounded shoes and open gesturing hand are not reproduced.
- Fingers are rigid parts of each hand, not rigged individually. No IK, control rig, walk cycle or animation; the rig is simple FK with every part fully weighted to one bone.
- The mouth uses two discrete shape-key controls; no speech sync, no sound is attached.
- Counts: my count_scene run on the .blend files reports 136 mesh objects and 51,538 / 51,986 triangles, which is the source's 135 meshes and 51,536 / 51,984 triangles plus a 2-triangle floor plane; the .blend also shows 8 materials against 7 in the GLB (the extra is presentation-only).
- Height figures (1.6815 m and 2.0765 m with antenna) come from the source's own audit; my count cannot give them because of the large floor plane.
- Verification of Godot import and the GLB round-trip is as recorded by the source; I did not re-run it.
