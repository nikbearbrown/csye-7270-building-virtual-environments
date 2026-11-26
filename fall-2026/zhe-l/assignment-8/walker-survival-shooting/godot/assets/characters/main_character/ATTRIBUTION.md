# Main character model and tablet animations

- **Model and rig:** commissioned for this project (a friend built a rigged character from my character design) and used with permission. The Blender source file is not in the project (it is over 25 MB); the original stays on my machine.
- **Animation:** keyed in a working copy of the source file (`xz_anim2.blend`). I posed the one-handed hold, the tablet's stowed position and the two-handed hold; Claude Code (Claude Opus 5.5) made the in-between frames, the fingers and the right-hand grip point in Blender at my request.
- **Export:** with `tools/blender/export_main_character.py` from my working folder (headless Blender 5.2.2, glTF binary). Clips: `tablet_hold_hip`, `tablet_raise_one_hand`, `tablet_hold_one_hand`, `tablet_raise_two_hand`, `tablet_hold_two_hand`. The textures next to the `.glb` were extracted from it by Godot's importer.
- **Import settings:** `main_character.glb.import` turns off the `AnimationPlayer` keyframe optimizer (`"nodes"` → `"PATH:AnimationPlayer"` → `"optimizer/enabled": false`); otherwise Godot removes the overshoot-and-settle frames. No clip loops.
- **Licence:** copyright belongs to me (the commissioning party); not for use outside this project.
- Checked: 2026-11-22.
