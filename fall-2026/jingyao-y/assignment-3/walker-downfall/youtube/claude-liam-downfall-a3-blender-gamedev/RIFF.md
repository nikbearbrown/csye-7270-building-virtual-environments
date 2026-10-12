# RIFF.md — commentary grounded in inspected output

- **"Mostly buried and read as a flat disc."** In call 5 the boulder is 0.35 tall, centred at z 2.225; the top stratum's top is at z 2.25. Claude saw it as a disc in the `look` image (`images/blender-cliff-before.png`).
- **"Its top stone floated."** rubble_c's bottom was at 0.51. The front and right `look` views show a gap (`images/blender-rubble-before.png`).
- **"Barely visible … isn't visible at all."** Claude's own reading of `images/blender-ramp.png` and of the game-camera frames of `orbit.avi`. No human judged the crown.
- **"By default the cliff's face points away from it."** `GameManager.CAMERA_OFFSET = (0, 16, -10)` puts the camera on the −Z side, looking towards +Z. The cliff's front is at +Z (AABB max z 0.30).
- **"Looks like flipped normals."** That was Claude's first hypothesis. The Blender count of inward faces per island was 0 for all ten islands, before the transpose was found.
- **"Everything is correct."** This is the author's whole HUMAN CHECK report, "都是对的". Nothing is inferred beyond it.
