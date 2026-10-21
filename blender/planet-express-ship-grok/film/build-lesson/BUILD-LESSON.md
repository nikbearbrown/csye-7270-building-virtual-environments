# Build lesson: Planet Express ship (from images)

Skill: brutalist.art `blender-build` at commit `a187fab`, default **image-based lesson** mode. This lesson teaches one possible way to build a *similar* model from the published renders and a coding agent. It is **not** a history of how Grok Bot built round 15, and it does not use the `.blend`, `.glb`, STL kit or build scripts.

Images: see [SOURCES.md](SOURCES.md). Prompts to copy: [PROMPTS.md](PROMPTS.md). Film: [beat_sheet.md](beat_sheet.md), shot list [SHOTLIST.md](SHOTLIST.md). The narrator is the Liam voice.

## What can be known from the pictures

- **Observed:** long rounded teal hull rising to a turret and falling to the engine; rounded nose wrapped by a red lip; low flat dark-teal visor; cream portholes along both sides; cream ribbed vent, hatch and ladder; swept fin with a round logo (mirrored on the right side); short wings with rings; cream engine bell with a cluster of dark nozzles; turret dome with barrel and antenna.
- **Proposed:** working scale (hull about 12 units long, about a quarter as wide and as tall), lofted or sculpted hull, Solidify fin, mirrored wings, radial nozzle duplication, image-texture logo, material values.
- **Demonstrated:** nothing yet. No operation in this lesson has been run in a fresh scratch scene for the lesson; every checkpoint is a proposal with a visible check. Not learner-tested.

The source model's stats (206 objects, 109,004 triangles, 13 materials) describe that asset only; a learner need not match them.

## Checkpoints

Each has goal, evidence, Blender concept, operation, prompt (in PROMPTS.md), expected result, learner check, correction.

| # | Goal | Evidence | Blender concept and operation | Expected result | Learner check | If it fails |
|---|---|---|---|---|---|---|
| 0 | Read the images | side, top, front | Axes (X width, Y length, Z height), working scale, perspective | Written proportions and a list of parts | Ratios read from side/top/front, not the quarter view | Re-measure from orthographic-looking views only |
| 1 | Hull blockout | side, front | UV sphere (low res), Scale in Object Mode; or a lofted profile mesh | One smooth hull, no detail | Side render overlays top line and belly; front width/height match | Prompt C1: change only hull scale/profile |
| 2 | Nose and lip | front34, front | Loop cuts, proportional editing (O), separate lip object following the edge (curve with bevel profile is one option) | Rounded tapered nose with a red band | Nose not too pointed in front view | Prompt C2: widen nose, keep length |
| 3 | Visor | detail_cockpit, front | Separate object, Inset Faces for panes, origin on the hull surface | Low flat frame seated on hull | Front view: not sunk, not floating | Re-seat along hull normal |
| 4 | Fin, wings, turret | top, rear34, detail_turret | Named objects, Solidify modifier, Mirror modifier, Spin/Screw for the dome | Parts attached at visible roots | Roots line up in top and rear views | Move origins, not cameras |
| 5 | Portholes | side | One ring + pane, local axes, then duplicate along the side | Evenly spaced flush portholes | No floating or buried rings | Fix one, re-duplicate |
| 6 | Engine | detail_engine, rear34 | Revolved bell; one nozzle + radial duplication (Array with empty, or Spin duplicate) about a set center | Bell with nozzle cluster | Bell size vs hull in side view (round 15's is too big) | Scale bell down only |
| 7 | Materials | detail_fin_logo, detail_vent_wing | Material slots, Principled BSDF roughness, image texture + UV for the logo | Teal/dark teal/cream/red under neutral lights | Colour boundaries match | Adjust slots, not lights |
| 8 | Compare and correct | r15_ref06, before_after | Fixed comparison cameras, incremental saves | Same views each round | Largest mismatch named and fixed; holds across views | Prompt C8 (front too narrow, bell too big) |
| 9 | Save and export | front34 | Numbered .blend saves, File > Export > glTF 2.0 | .glb re-opens at the right scale | Scale and colours survive re-import | Apply scale before export |

Version-sensitive steps (glTF exporter, Solidify, Mirror, proportional editing) exist in Blender 4.2 LTS, the version the source model reports; they were **not executed** for this lesson.

## Review context (reported)

Round 12: Grok Bot self-score 4/10; Professor Bear said "pretty good, maybe a six out of ten, but it could use another round." Round 13 skipped the chunkier hull because of Grok Bot's own instruction. Round 15: self-score 5.5/10 (side 6, front 5, rear 4, top 5.5). Professor Bear's verdict on round 15 is pending.

## Practice

Widen the nose of your hull. Checks: (1) the front view matches the front-on toy reference better; (2) the side view still matches.

## Status and assumptions

- Film not rendered and narration not generated; Professor Bear renders with his own tools. No subtitles or captions.
- No scratch-scene Blender demonstration was made, so the film is stills and diagrams and says its steps are proposed.
- Assumes the published renders are close to orthographic for side/top/front; they are rendered views of the model and are treated as reference images, not measured drawings.
