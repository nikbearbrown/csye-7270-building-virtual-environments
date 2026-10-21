# Build lesson: Futurama-style toy Enterprise (from images)

Skill: brutalist.art `blender-build` at commit `a187fab`, default **image-based lesson** mode. One possible way to build a *similar* model from the published renders, the concept image and a coding agent. Not a history of how Grok Bot built round 9; it does not use the `.blend`, `.glb` or build scripts.

Images: [SOURCES.md](SOURCES.md). Prompts: [PROMPTS.md](PROMPTS.md). Film: [beat_sheet.md](beat_sheet.md), [SHOTLIST.md](SHOTLIST.md). Narrator: the Liam voice.

## What can be known from the pictures

- **Observed:** round lens saucer with a red edge stripe and porthole rings; glass bridge dome; short neck; fat secondary hull with a cream deflector of nested rings; two nacelles with red domed caps, cream rings and red stripe panels on swept pylons; blue-grey, cream and red palette.
- **Proposed:** working scale (saucer 10 units across), lathed profiles (Screw modifier or Spin) for saucer, hull and nacelles, beveled beams for neck and pylons, radial duplication for portholes, material values.
- **Demonstrated:** nothing. No operation was run in a fresh scratch scene for this lesson. Not learner-tested.

Design choice: match the Futurama-style concept image; use the blueprint comparisons only to check proportions. Do not switch source designs mid-lesson.

## Checkpoints

| # | Goal | Evidence | Blender concept and operation | Expected result | Learner check | If it fails |
|---|---|---|---|---|---|---|
| 0 | Read the images | side, top, front, concept | Axes, working scale, choice of target design | Proportions list | Ratios from side/top/front | Re-measure |
| 1 | Blockout | side, top | Primitives: flattened UV sphere, capsule, cylinders, cube | Four volumes in place | Side and top silhouettes match | Prompt C1 |
| 2 | Saucer and dome | side, detail_bridge | Half profile + Screw modifier (lathe), separate dome with glass material | Lens saucer, red edge, dome | Saucer thickness in side view (round 9's is too thin) | Thicken profile |
| 3 | Secondary hull, nacelles | r9_side_vs_blueprint | Lathed profiles | Hull and nacelles sized to saucer | Hull size vs saucer (round 9's is too small) | Scale hull up only |
| 4 | Neck and pylons | hero, rear34 | Cubes + Bevel modifier, origins at attachment points | Visible neck, swept pylons | Neck reads in side view (round 9's barely shows) | Thicken neck |
| 5 | Portholes | top | One ring, then radial duplication about the saucer centre | Even rings | Flush, evenly spaced | Re-seat one, re-duplicate |
| 6 | Nacelle and deflector detail | detail_nacelle, detail_deflector | Caps (UV sphere halves), rings (torus), curved stripe panels; nested torus rings | Details on surfaces | No floating parts; bumper lights not tile-like | Rounder light shapes |
| 7 | Materials | r9_hero_vs_concept | Material slots, Principled BSDF, glass transmission | Palette under neutral light | Colour vs concept | Adjust materials, not lights |
| 8 | Compare and correct | r9_*_vs_blueprint | Fixed cameras, numbered saves | Same views each round | Biggest mismatch fixed, holds across views | Prompt C8 |
| 9 | Export | hero | glTF 2.0 export, re-import | .glb at right scale | Size, colours survive | Apply scale |

Steps were checked against the reported Blender version (4.2 LTS) by name only; **not executed** for this lesson.

## Review context (reported)

Professor Bear said about the concept image: "I love it. It's fun... you definitely recognize the Enterprise, but it's not the Enterprise." Grok Bot's self-score for round 9 is about 6/10. Professor Bear's verdict on round 9 is pending.

## Practice

Thicken the saucer. Checks: (1) the side view matches the blueprint better; (2) the hero view still reads as the toy.

## Status and assumptions

- Film not rendered; narration not generated. No subtitles or captions. Professor Bear renders with his own tools.
- No scratch-scene demonstration; the film is stills and diagrams and labels its steps as proposed.
- The blueprints appear only inside the published comparison sheets; a learner can use those sheets, or their own reference drawings.
