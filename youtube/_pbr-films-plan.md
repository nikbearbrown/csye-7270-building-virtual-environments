# PBR films: built (2026-11-13; Bear: "Build all three")

**Executive summary:** Three short CSYE 7270 teaching films on PBR (physically based rendering), built with the `lecture` skill in its topic-film form (the same format as the Godot shader-technique films already in this folder: Liam voice, claude-liam channel, BOPEN title card with series title only, no numbers). PBR is OFF the exam (Bear, 11-13); these are class material. Godot only, no shading-language code. Every material shown on screen is a real Godot 4.7.2 render made for the film (Godot is installed here), not a stand-in.

Series title on the card: planned as "Materials and PBR in Godot"; built with the existing course playlist "CSYE 7270 Building Virtual Environments" instead (no video numbers).

| Working title | One line | Main source |
|---|---|---|
| What Is PBR? | A material is a set of measurements, not a picture: base colour, metallic, roughness, normal and ambient occlusion, which a light and a camera turn into colour. Shown on a real Godot grid of spheres (roughness left to right, metallic top to bottom). | Ch 7, "A PBR material is a set of measurements, not a picture"; deck 12 slides 3 and 4 |
| Why PBR Matters | One material, any light: the same measurements stay believable under noon sun, sunset and a dim room, while a texture with the lighting painted in breaks as soon as the light moves. Plus: one shared model (glTF metallic–roughness) means a model made in Blender arrives in Godot looking the same, and you always judge a material under stated lighting. | Ch 7 (consequences list; lighting and GI section); Godot Standard Material 3D docs; glTF 2.0 spec |
| PBR Textures Are Data, Not Pictures (optional) | Only the base colour map is a colour; roughness, metallic, AO and normal maps are numbers stored in image files. Packed ORM/ARM files (red AO, green roughness, blue metallic), and what goes wrong when data is read as colour (a flat normal tilted 38.8°). Covers what a normal is, which Bear called fair game for the exam. | Ch 7, "Colour versus data"; ORMMaterial3D section; deck 12 slides 5 and 6 |

Length: as long as each needs (likely 3 to 5 minutes each), no padding.

Risks before rendering:
- Disk: 2.3 GB free on 11-13 (`df -h`). A 4K lecture build writes per-beat clips and a master; space must be freed first or the render will fail part-way.
- "Why" claims beyond the chapter (painted-in lighting, cross-tool consistency) get sourced to Godot docs and the glTF spec in FACTCHECK.md; anything unsourced is cut.

Status (2026-11-13, evening): all three masters built, every gate passing, not published. Playlist on the card is the existing "CSYE 7270 Building Virtual Environments" (not a new series name).
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-what-is-pbr/exports/landscape/claude-liam-lecture-what-is-pbr.mp4 (3:07)
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-why-pbr-matters/exports/landscape/claude-liam-lecture-why-pbr-matters.mp4 (2:42)
- /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-pbr-textures-are-data/exports/landscape/claude-liam-lecture-pbr-textures-are-data.mp4 (3:12)
Evidence rig: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_pbr-evidence
