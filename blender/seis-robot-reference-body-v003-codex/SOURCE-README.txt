SEIS AI LAB — REFERENCE BODY STUDY v003

Purpose
Rebuild the body around Bear's seven supplied armored robot photographs,
using Northeastern colors. The body is the current review decision.
The previous v002 body was rejected as too similar to the original robot.

Files
seis_robot_reference_body_v003.blend — editable native Blender source
exports/seis_robot_reference_body_v003.glb — portable static model
review.html — actual renders beside the supplied front reference
renders/ — six PNG views, 1400 x 1800
scripts/build_body.py — reproducible geometry and materials
scripts/render_views.py — review-camera renders, without saving the source
scripts/export_and_roundtrip.py — Walker-derived Blender GLB round-trip check
references/ — byte-for-byte copies of the supplied photographs
reports/ — inventory, render logs, round-trip and delivery checks

Design
New sculpted body geometry, with an hourglass torso, rounded shoulder armor,
large gauntlets, slim long thighs, visible knee joints, and flared greaves.
Two ordinary hands. A small red Lato 6 on the white chest badge.
Base colors: C8102E red; A4804A and C8A978 golds; 49494D and 9B9C9E grays;
FFFFFF white; 1E2028 cool black. Based on the existing saved NU guidelines.

Deferred
Temporary blank helmet, isolated by body_group=head_placeholder. It is not
the proposed final SEIS face. Final box head, broken antenna, waveform mouth,
engineer connector, six-spool housing and wrist readout are a later pass.
No animation rig, pose controls, speech sync or working agent tools.
Geometry is a high-resolution study, not optimized game geometry.

Technical
Blender 5.1.2 (installed version; Walker notes name 5.2 but were tested on 5.1.2).
163 separate mesh parts; 410800 evaluated triangles. No textures needed.
Forward -Y, up Z; meters; height about 1.89 m.
EXPORT holds original model geometry; PRESENTATION holds only studio elements.
Anatomical groups are in each object's body_group custom property.
Built from scratch using local Blender Python; no MCP invocation or paid API.
No v001/v002 mesh or head reused. Original files retained.

Rebuild
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python scripts/build_body.py
Then run render_views.py with the saved .blend loaded.

Scope of verification
Actual model renders visually inspected; GLB reimport checks mesh count,
triangle count and world dimensions. No game-engine import or animation test.
Technical checks do not establish Bear's approval of the design.
