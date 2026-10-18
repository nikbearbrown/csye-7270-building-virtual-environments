# Build notes: Claude mascot (scripted, rigged), by Claude

`1 mesh (9 boxes), 108 triangles, 2 flat-colour materials, 1 armature with 9 bones, 1.36 x 0.495 x 0.86 m, no cameras or lights in the .blend (measured with Blender 5.1.2)`

## What was done
`scripts/build_mascot.py` makes the nine boxes from a table of 2D rectangles (x0, x1, top, bottom) taken from the 2D scene, adds a depth for each, joins them into one mesh, creates the 9-bone armature, skins each box rigidly to its bone (weight 1.0), sets the two materials, saves the .blend and exports the .glb. `render_mascot.py` and `make_sheets.py` produce the renders and contact sheets.

## Measured here
Counts come from `scripts/count_scene.py` (output in `scripts/counts.json`): 1 mesh object, 108 triangles, 2 materials, 1 armature, 9 bones, bounds 1.36 x 0.495 x 0.86 m, 0 cameras, 0 lights, Blender 5.1.2. The .glb was read back: 11 nodes, 1 skin, no images.

## Checks the source reports (not re-run)
Dimensions, 108 triangles and lowest z = 0 from the build log; skin and bounds read from the .glb; Godot 4.7.2 headless import; torso colour (217, 117, 89) rendered against canonical (221, 119, 91).

## Not done
No reference image comparison, no animation clips, no test in Blender 4.2.

## Files not copied
The source folder's build-record, mcp-run and youtube folders belong to other pieces of work. Individual pose renders (about 20 MB) are summarised by `renders/sheet-poses.png`.

## Built by

- **Builder:** Claude (no model or version is recorded in the source files)
- **Method:** Scripted: `build_mascot.py` run with Blender in background mode. Not built through the Blender MCP (the source README says so). Zero render-vs-reference rounds, because there is no image reference; checks were numeric (dimensions, triangle count, torso colour 217,117,89 against canonical 221,119,91), every render looked at, and a Godot import test reported in the source README (not re-run here).
- **Tools:** Blender 5.1.2 (read from the .blend by count_scene.py); Godot 4.7.2 for the import test, as the source README states
- **Build date:** 2026-10-06 (file times and README check date)
- **Human review:** Professor Bear: pending. The source README lists four open decisions for him (scale, spin, MCP or script, next video).

## Known limitations

- Depth, scale (1 pixel = 1 cm) and the raised eyes are invented; the 2D scene only fixes width and height.
- No animation clips exist; the 18 poses are single frames, not tested motion.
- The .blend was saved by Blender 5.1.2 and has never been opened in Blender 4.2; it may not open there.
- No camera or lights are saved in the .blend, so it opens without a ready view.
- The .glb has a skeleton and one skinned mesh node but the model is rigid boxes only; no textures.
- Likeness to the 2D mascot was not compared against an image; it rests on the numbers. Judged by eye, the shape is a plain box creature with the right proportions, but it has no detail beyond that.
