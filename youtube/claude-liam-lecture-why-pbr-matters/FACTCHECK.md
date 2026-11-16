# Fact check — Why PBR Matters

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B01 | Painting light into a texture was an older shortcut | Correct (general practice); demonstrated with a code-painted texture | tools/make_textures.py painted_sphere.png; unshaded material in capture.gd | none |
| 2 | B02 | Only the PBR highlight follows a moving light | Correct; shown in the render | capture painted_orbit | none |
| 3 | B03 | Painted sphere ignores time-of-day lighting | Correct; unshaded material ignores lights | capture painted_daynight; Godot SHADING_MODE_UNSHADED | none |
| 4 | B04 | PBR materials look correct regardless of lighting conditions | Correct; attributed source | https://learnopengl.com/PBR/Theory: "these materials will look correct regardless of lighting conditions"; capture three | none |
| 5 | B05 | Energy conservation: outgoing light never exceeds incoming; rougher = wider, dimmer highlight | Correct; measured in Godot | https://learnopengl.com/PBR/Theory: "outgoing light energy should never exceed the incoming light energy"; evidence/profiles.json | none |
| 6 | B06 | Blender material crosses glTF as metallic-roughness and arrives as StandardMaterial3D | Correct; tested in the course worked example | /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/chapters/03-blender-mcp-to-godot.md line 93 | none |
| 7 | B07 | A Godot material saved as text is a list of values | Correct; real output | evidence/materials/gold.tres written by tools/save_materials.gd | none |
| 8 | B08 | With nothing to reflect, a metal looks like dark plastic | Correct; shown in the render | /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/chapters/07-materials-and-textures.md: "A rough metal looks like plastic without something to reflect."; capture metal_sky | none |

Nothing datable (no prices, versions beyond Godot 4.7.2 on the capture label, or dates) is spoken. Sources checked 2026-11-13.
