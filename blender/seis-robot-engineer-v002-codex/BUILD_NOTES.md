# Build notes: SEIS AI Lab engineer robot, body study v002

`230 meshes · 67,496 triangles · 12 materials in the GLB · 24 bones · mouth shape keys Speaking and Emphasis · 6 spool caps · 2.84 m tall with antenna in the source's audit · Blender 5.1.2`

## What it is

A second body for the SEIS robot with an instrument arm, built by `scripts/build_engineer.py`. The supplied pasted design notes (an agent-orchestrating engineer called "Jig", kept in `references/engineer-arm-notes.txt`) were treated as background only: the source says direct requests override conflicting pasted notes, so the model keeps the eyes and waveform and the Northeastern palette, includes wrist text, and does not use the notes' spirit-level face or orange palette.

## What I measured

`scripts/count_scene.py` on the .blend (Blender 5.1.2): 231 mesh objects, 67,498 triangles, 13 materials, 1 armature, 24 bones, 1 camera, 3 lights (`reports/scene-counts-seis_robot_engineer_v002.json`). The floor plane accounts for one mesh and two triangles over the source's 230 meshes and 67,496 triangles.

GLB inspection: 0 images, 0 textures, 12 materials, 1 skin, 0 animations.

## What the source reports (not re-run by me)

- 230 meshes, 67,496 triangles, 24 bones, every vertex weighted to one bone, six spool caps, both mouth morph targets present.
- Connector deployment evaluated at five states: fingers fold first, the palm separates, the plug then travels 0.24 m.
- GLB re-import in Blender matched mesh, triangle and bone counts and dimensions. The first export used the rest pose; setting `export_rest_position_armature=False` corrected it.

## Controls

On `SEIS_Engineer_Rig` (Object Properties, Custom Properties): `tool_deployed` 0 to 1 folds the fingers, separates the palm, then extends the plug; `screen_orient` 0 to 1 turns the display toward its wearer. On `SEIS_Engineer_Waveform_Mouth`: `Speaking` and `Emphasis` shape keys. Play the timeline to scroll the wrist text.

## Notes

Palette from the project's saved Northeastern guidelines: red C8102E, bold gold A4804A, light gold C8A978, cool black 1E2028, grays 49494D and 9B9C9E, white and canvas F6F6F4. Paths in copied scripts and logs were replaced with placeholders; the Lato font path in `build_engineer.py` points outside this repository.

## Not copied

review.html, the 24 readout frame PNGs, `.blend1` backups.

## Built by

- **Builder:** Codex (OpenAI). Builder identified from Codex session logs on this machine dated 2026-10-18, not from a label in the folder; no product or model version is stated in the files.
- **Method:** Scripted: local Blender Python (scripts/build_engineer.py, assembled from head_helpers.py.txt and body.py.txt); the source says no Blender MCP connection and no paid generation. Recorded checks (reports/CHECKS.md): connector deployment evaluated at 0, .25, .5, .75 and 1; twelve views rendered and inspected; one visible inspect-and-fix pass (the side review moved the chest numeral and leg trim onto their surfaces). No numbered render-versus-reference rounds are logged; the supplied photographs were used for body proportions and armour cues only. The compare images here were made afterwards for this page, by eye.
- **Tools:** Blender 5.1.2 (confirmed by my scene count); Lato Bold font converted to mesh for the 6; the source's own Blender export and re-import check. No game engine import was run.
- **Build date:** 2026-10-17 (file times 17:25; the source's CHECKS.md is dated 2026-10-17)
- **Human review:** Professor Bear: pending. The source CHECKS.md says: "Ready for design review; this is not human approval of the design." A later source file (the v003 README.txt, in this repository's sibling folder) states: "The previous v002 body was rejected as too similar to the original robot." The files do not say who made that call or when.

## Known limitations

- This is a design study, not a final model.
- Likeness to the supplied photographs is weak; the body is still close to the original SEIS robot (the v003 README says so in its own words).
- The right arm is a visual concept only: cable payout, programmed iris states, quarantine behaviour, live agent connections and voice-driven face animation are not implemented. The wrist display is schematic text, not live agent data.
- The source's own prototype proportions are not manufacturing dimensions; the connector travels 0.24 m in the audit.
- Rigid FK posing only; no IK, no animation clips in the GLB, no engine import test.
- Counts: my count_scene run reports 231 mesh objects and 67,498 triangles, which is the source's 230 meshes and 67,496 triangles plus a 2-triangle floor plane; 13 materials in the .blend against 12 in the GLB.
- The 2.84 m height (with antenna) is from the source's own audit; my count cannot give it because of the large floor plane. At this height the robot is large compared with the 1.68 m of v001.
- I did not copy the 24 readout frame PNGs or the review.html; the 4-second mp4 is included.
