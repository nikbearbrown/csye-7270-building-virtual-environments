# Technical checks — engineer v002

2026-10-17. Ready for design review; this is not human approval of the design.

- Saved Blender model: 230 meshes, 67,496 triangles, 24 bones.
- Every mechanical vertex has exactly one full-weight bone.
- Six spool caps and both mouth morph targets are present.
- Connector deployment was evaluated at 0, .25, .5, .75 and 1. Fingers fold first; the palm separates; the solid plug then travels 0.24 m. These are prototype proportions, not manufacturing dimensions.
- Digital text moves between timeline frames. Display lettering is flat and emissive; a four-second silent preview demonstrates the readout.
- Twelve actual model views rendered. Inspected front, side, back, top, hero, silent face, hand mode, wrist reading, wrist detail, connector detail, hand detail and wireframe. Side review prompted bringing the chest numeral/calibration marks and leg trim back onto their supporting surfaces.
- GLB exported and reimported in Blender with matching mesh count, triangle count, bone count and dimensions. The first export used the rest pose; export_rest_position_armature=False corrected the mismatch. Mouth morph names survived; no external buffers are required.
- Export preserves the displayed pose and rigged geometry. Blender drivers and scrolling logic are not portable glTF behavior. No game-engine runtime import was tested.
- The previous v001 model and seven supplied image copies match their recorded source hashes.
- Local review links resolve. File hashes are recorded in delivery-manifest.json.

The right arm remains a visual/mechanical concept. Cable payout, live agent connections, iris/quarantine state logic and voice-synchronized mouth animation are future work.
