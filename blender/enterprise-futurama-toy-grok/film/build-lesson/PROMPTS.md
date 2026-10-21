# Prompts: build a Futurama-style toy Enterprise from images

For a fresh coding-agent chat. Attach from the gallery in SOURCES.md: `hero.jpg`, `side.jpg` (left side), `top.jpg`, `front.jpg`, `rear34.jpg`, `concept_grok_bot.jpg` (the style target), the close-ups `detail_bridge.jpg`, `detail_nacelle.jpg`, `detail_deflector.jpg`, and the comparison sheets `r9_side_vs_blueprint.jpg`, `r9_top_vs_blueprint.jpg`, `r9_front_vs_blueprint.jpg`. Your agent needs Blender control or the ability to write a script for Blender's Scripting workspace.

## Starter

> Help me learn Blender by building a chunky toy-style starship from the attached images: concept_grok_bot.jpg (the style I want), hero.jpg, side.jpg (left side), top.jpg and front.jpg. These images are all I have; do not assume any original model, blueprints file or scripts. Describe the visible major forms and any perspective uncertainty. Propose short modeling checkpoints with the Blender concept for each. Use X width, Y length, Z height and a working scale of 10 units across the saucer, labelled as an assumption. Start with only four blockout volumes: saucer, secondary hull, two nacelles, neck. If you can control Blender, work in a new scene and save `toy_c1.blend`; otherwise give me a Scripting-workspace script and a manual alternative. Render side, top and hero-angle views. Tell me what you executed and what is still a proposal.

## C1: blockout

> Change only the four volumes. Match their sizes and positions to side.jpg and top.jpg. Render side and top from fixed cameras and list the remaining disagreement.

## C2: saucer and dome

> Replace the saucer with a lathed lens: draw half its profile and use a Screw modifier (or Spin). Add the red edge band and a separate glass dome from detail_bridge.jpg. Success: saucer thickness in the side view matches side.jpg and is not thinner.

## C3: secondary hull and nacelles

> Lathe the secondary hull and both nacelles from profiles. Size the hull against the saucer using r9_side_vs_blueprint.jpg; err larger rather than smaller. Render side and top.

## C4: neck and pylons

> Add the neck and the two pylons as beveled beams, each with its origin at its attachment point. Make the neck thick enough to read clearly in the side view. Show hero and rear views.

## C5: one porthole, then a ring

> Make one cream porthole ring seated on the saucer surface; explain its local axes. Wait for my check. Then repeat it around the saucer at the spacing in top.jpg.

## C6: nacelle and deflector detail

> From detail_nacelle.jpg and detail_deflector.jpg add the red caps, cream rings, the curved red stripe panels and the deflector's nested rings. Keep the bumper lights round, not tile-like. Exterior only.

## C7: materials

> Under neutral lights add blue-grey plastic, cream, red and clear glass. Compare with concept_grok_bot.jpg. Explain your choices without claiming they were the original method.

## C8: correction

> Show my side, top and front views beside the comparison sheets. Fix only the largest mismatch (likely saucer thickness or secondary hull size). Keep nacelle positions. Save a new checkpoint and re-render the same views without moving cameras. Tell me what changed and why.

## C9: export

> Save a numbered .blend, apply scale, export glTF 2.0 (.glb), re-import in a new scene and confirm size and colours.

These prompts have not been run by a learner or tested for this lesson.
