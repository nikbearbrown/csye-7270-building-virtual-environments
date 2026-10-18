# MASCOT-BRIEF.md — the Claude mascot, written before building

**Name:** ClaudeMascot.
**What it is:** the Claude mascot, a pixel-art creature made of nine boxes: a torso, two arms, two eyes, four legs.
**Where it appears:** the end of a video series now; next, as a character in a game, animated (idle, walk, jump, wave and others), so each part must stay a separate, named object that can follow its own bone later.

## Size and place, in metres (1 Blender unit = 1 m, Z up, the front faces -Y)
Each part is ONE box. Size is X (width) x Y (depth) x Z (height); position is the centre.

| Object | Size (m) | Centre (m) |
|---|---|---|
| Torso | 0.96 x 0.48 x 0.60 | (0, 0, 0.56) |
| ArmL | 0.20 x 0.20 x 0.20 | (-0.58, 0, 0.56) |
| ArmR | 0.20 x 0.20 x 0.20 | (0.58, 0, 0.56) |
| EyeL | 0.11 x 0.03 x 0.10 | (-0.315, -0.24, 0.71) |
| EyeR | 0.11 x 0.03 x 0.10 | (0.315, -0.24, 0.71) |
| Leg1 | 0.11 x 0.11 x 0.26 | (-0.315, 0, 0.13) |
| Leg2 | 0.11 x 0.11 x 0.26 | (-0.105, 0, 0.13) |
| Leg3 | 0.11 x 0.11 x 0.26 | (0.215, 0, 0.13) |
| Leg4 | 0.11 x 0.11 x 0.26 | (0.425, 0, 0.13) |

The whole mascot is 1.36 m wide with the arms, 0.495 m deep, 0.86 m tall.

## Origin
The world origin is the centre of the underside of the feet, so the feet stand at z = 0. Every object keeps its own origin at its centre (the rig comes later).

## Look
Flat colours, no textures. Torso, arms and legs: material ClaudeBody, colour #dd775b. Eyes: material ClaudeEye, colour #000000.

## Budget
Nine boxes, 12 triangles each: 108 triangles. Never more than 500.

## Predicted failures, and the check that catches each
1. A part ten times too big or in the wrong place: print every object's dimensions and location and compare with the table.
2. The feet not on the floor: the lowest point of the legs must be z = 0.0000.
3. Rotation or scale not applied: every object must report rotation 0 and scale 1.
4. A wrong colour: read the two material colours back.
5. The tool silently not doing what it says: look at the viewport yourself after every part.
