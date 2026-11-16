# Fact check — PBR Textures Are Data, Not Pictures

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B01 | A PBR material is a set of maps, one per measurement | Correct | /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/chapters/07-materials-and-textures.md; capture stack | none |
| 2 | B02 | Only the base colour map is a colour | Correct | /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/chapters/07-materials-and-textures.md: "Only the base colour is a colour." | none |
| 3 | B03 | Tiles hold about 0.3 roughness, grout 0.9 | Correct; read from the file | textures/tiles_roughness.png via textures.json | none |
| 4 | B04 | Roughness map makes the shine vary across the surface | Correct; shown in the render | capture roughmap | none |
| 5 | B05 | Lighting depends on the angle between normal and light | Correct (Lambert N·L) | /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/chapters/07-materials-and-textures.md N·L worked example | none |
| 6 | B06 | Normal map RGB = XYZ; flat texel (128,128,255); normal maps pale blue | Correct | glTF 2.0 normal texture rule quoted in /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/chapters/07-materials-and-textures.md; chapter flat texel (128,128,255) | none |
| 7 | B07 | Normal map changes lighting, not geometry | Correct | Godot docs: "This does not modify geometry, only the incident angle for light." | none |
| 8 | B08 | Poly Haven ARM: R=AO, G=roughness, B=metallic; ORMMaterial3D reads the same order | Correct | /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/chapters/07-materials-and-textures.md ORM channel order (material.cpp at 4.7.2) | none |
| 9 | B09 | 128/255 = 0.502 decodes to 0.216; flat normal tilts 38.8° | Correct; recomputed | /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/chapters/07-materials-and-textures.md "Colour versus data"; evidence/decode-check.txt | none |
| 10 | B10 | Same flat normal map read as colour lights the sphere off-centre | Correct; shown in the render | capture decode (two ShaderMaterials differing only in hint_normal vs source_color) | none |

Nothing datable (no prices, versions beyond Godot 4.7.2 on the capture label, or dates) is spoken. Sources checked 2026-11-13.
