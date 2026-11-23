# Main character model and its tablet clips

- **Model and rig:** commissioned for this project (a friend built the rigged character for me from my character sheet); used here with permission. The source `.blend` is not in this repository (over 25 MB).
- **Animation:** keyed in my working copy of that file (`xz_anim.blend`). I posed the one-handed end pose; Claude Code (Claude Opus 5.5) keyed the in-betweens and the fingers in Blender at my request (SOURCES.md: ANIM-TABLET-RAISE-1H-01).
- **Export:** `tools/blender/export_main_character.py`, headless Blender 5.2.2, glTF binary. Clips: `tablet_hold_hip`, `tablet_raise_one_hand`, `tablet_hold_one_hand`. The textures next to the `.glb` are extracted from it by Godot's importer.
- **Licence:** all rights reserved by me as the commissioner; not for reuse outside this project.
- Checked: 2026-11-22.
