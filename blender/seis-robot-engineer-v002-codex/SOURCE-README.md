# SEIS engineer — body study v002

A new editable Blender study based on Bear's seven body references. The earlier v001 studies remain intact.

## Files

- `seis_robot_engineer_v002.blend`: editable model, separate mechanical parts, rigid FK skeleton, mouth shape keys and tool controls.
- `exports/seis_robot_engineer_v002.glb`: portable rigged geometry in its exported state. Blender's procedural drivers are not portable glTF logic.
- `review.html`: rendered views, hand/connector comparison and wrist-display study.
- `renders/`: PNGs rendered from the actual model.
- `references/`: supplied photographs, arm design notes and source hashes.
- `scripts/build_engineer.py`: reproducible local Blender build. Assembled from head_helpers.py.txt and body.py.txt.
- `reports/`: build, geometry and export checks.

## This revision

The body has a tapered layered torso, narrow upper legs, substantial flared shin armor and broad, flat feet. It uses white, black, gray, NU red and gold accents. The palette is drawn from the project's saved Northeastern guidelines: red C8102E, bold gold A4804A, light gold C8A978, cool black 1E2028, gray 49494D/9B9C9E, white FFFFFF and canvas F6F6F4. Lighting affects their appearance in renders.

The original box head, raised oval eyes and fine black waveform were retained in form. The antenna now has a bent tip and a broken second mast. The chest numeral is an actual extruded **6 from Lato Bold**, converted to mesh, with no font dependency at playback.

The right arm is an engineering instrument: a narrow **solid audio-style connector**, insulating rings, six spool caps, a wrist display, a split palm and retained folding fingers. The ordinary left hand can gesture and work on designs. The display behaves like a digital quarterback wrist playbook: brief scrolling task text, plus a reading orientation for a raised forearm.

Direct requests override conflicting pasted background notes: this model keeps eyes and the waveform, uses the requested Northeastern palette, and includes wrist text. It does not use the pasted spirit-level face or orange workshop palette. “Jig” remains a name in the supplied notes, not a renamed SEIS mascot.

## Controls in Blender

Select `SEIS_Engineer_Rig`, then Object Properties → Custom Properties:

- `tool_deployed`: 0 is hand mode, 1 exposes the connector. Intermediate values fold fingers in sequence, separate the palm and then extend the plug.
- `screen_orient`: 0 shows the text upright with the arm down; 1 rotates the display toward its wearer for wrist reading.
- Play the timeline to scroll the schematic wrist status text. This is a visual readout, not live agent data.

On `SEIS_Engineer_Waveform_Mouth`:

- `Speaking`: 0 hides the mouth inside the face; 1 shows the black waveform.
- `Emphasis`: increases waveform amplitude. No speech-to-mouth synchronization is attached.

Named shoulder, elbow, wrist, hip, knee and ankle bones provide rigid-part FK posing. The review's wrist pose uses an actual elbow rotation and head tilt, with the connector retracted.

## Scope

This is a visual and mechanical design prototype. The arm's trust/listen/tell bands, spool caps and iris collar represent the supplied design. Cable payout, programmed iris states, quarantine behavior, networked agents and voice-driven facial animation are not implemented. The display is schematic task text. This is not a functional autonomous system or a finished production character.

Built with local Blender Python. No Blender MCP connection was available in this session. No paid generation, source-image edits or external publishing.

