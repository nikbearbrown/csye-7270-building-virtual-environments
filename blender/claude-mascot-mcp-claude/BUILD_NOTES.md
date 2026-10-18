# Build notes: Claude mascot (built through the Blender MCP), by Claude

`9 mesh objects, 108 triangles, 3 materials (2 used), 1 armature with 9 bones, 1 camera, 1 light, 1.36 x 0.495 x 0.86 m (measured with Blender 5.1.2)`

## What happened, from the folder's logs
1. **Plan (prompt 1).** The session read the brief, called `get_scene_info` (default cube, light and camera), proposed steps and stopped.
2. **Build (prompt 2).** Approved; 13 tool calls built nine boxes, applied rotation and scale, assigned `ClaudeBody` (#dd775b) and `ClaudeEye` (black). `checks/check_scene.log` shows every part at the brief's size and place, lowest z = 0, 108 triangles.
3. **Save and photograph (prompt 3).** Saved the .blend and rendered an eight-view Workbench turnaround. The session listed what it could not verify (alpha, view transform, outline, light preset).
4. **Colour fix (prompt 4).** The renders were plain grey. The session found that Workbench reads each material's `diffuse_color`, not the Principled BSDF node, set it to the linear value, and re-rendered. Its torso pixel read #C49585 against target #dd775b; it said so and explained it as studio lighting. It also caught and corrected an earlier wrong pixel readout of #8d4d3c.
5. **Rig (prompt 5).** Created `ClaudeMascotRig` with nine bones, bone-parented each part, moved bones to test, saved the .blend and exported the .glb. The session's own note: the skin is not used by the meshes.

## Measured here
`scripts/count_scene.py` (see `scripts/counts.json`): 9 mesh objects, 108 triangles, 3 materials, 1 armature, 9 bones, 1 camera, 1 light, bounds 1.36 x 0.495 x 0.86 m, Blender 5.1.2. The .glb was read back: 19 nodes, 1 skin, no mesh node referencing it.

## Not copied
Session transcripts, add-on and window screenshots, the MCP config and install logs were left out (they hold local paths and setup detail). `gui_mascot.py` is included as the script that took those screenshots; it needs a scratch Blender profile to run and is not needed to use the model.

## Compared with the scripted build
Same dimensions and triangle count. The scripted build skins the parts with weights and has a pose sheet; this one uses bone parenting and has a camera and light but no pose sheet.

## Built by

- **Builder:** Claude, via Claude Code (session logs name the model `claude-sonnet-4-6`, Claude Code 2.1.150)
- **Method:** Driven through the Blender MCP: five prompts, one Claude Code run each, one `execute_blender_code` call per object, each reporting size, location, rotation and scale. One correction round (grey renders, fixed in prompt 4). No reference image, so no render-vs-reference rounds. Who wrote the five prompts is not recorded in the folder.
- **Tools:** Blender 5.1.2; MCP for Blender add-on v1.8 (as the session reported) over `uvx mcp-for-blender`; Claude Code 2.1.150
- **Build date:** 2026-10-07 (log and file times, around 00:03 local); the five prompts ran in the same session window
- **Human review:** Professor Bear: pending. The source records no verdict.

## Known limitations

- The .blend was saved by Blender 5.1.2 and has never been opened in Blender 4.2.
- The parts are bone-parented, not skinned: the .glb has one skin with 9 joints, but no mesh node references it (read back from the file). A game engine that expects weighted skinning will not deform the parts through it; it relies on the node hierarchy.
- The session itself reported it did not verify: that the glb stands upright in a +Y-up viewer, and that the glb coordinates match Blender's. These were not re-checked here.
- The first renders were grey. The fix worked, but the rendered torso reads (196, 149, 133) rather than #dd775b because of Workbench studio lighting.
- The .blend also holds two unused default materials (`Dots Stroke`, `Material`) and its scene contains an unrelated default camera and light.
- No animation clips; the rig was tested by moving a few bones once (Arm.R, Leg.1, Eye.L) in the session's own report.
- No reference image comparison; likeness rests on the brief's numbers and my reading of the renders: a plain box creature with the right proportions.
