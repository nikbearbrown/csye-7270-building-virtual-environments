# Fact check — What Is PBR?

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B01 | Godot StandardMaterial3D holds base colour, metallic, roughness, normal, AO (metallic–roughness model, as glTF 2.0) | Correct | /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/chapters/07-materials-and-textures.md "A PBR material is a set of measurements"; https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html | none |
| 2 | B02 | Albedo is the base colour; highlight and shadow come from the light | Correct; shown in the render | Godot docs: "Albedo is the base color for the material, on which all the other settings operate"; capture albedo | none |
| 3 | B03 | Metallic 0: white highlight over the colour; metallic 1: colour moves into the reflection | Correct; shown in the render | capture metallic (frames 0 vs end); Godot docs Metallic section | none |
| 4 | B04 | Roughness 0 = perfect mirror, 1 = completely blurred reflection | Correct (paraphrase of the docs) | Godot docs: "A value of 0 makes it a perfect mirror while a value of 1 completely blurs the reflection" | none |
| 5 | B05 | Chart: roughness left to right, metallic top to bottom, one albedo | Correct; capture parameters | tools/capture.gd case "grid" | none |
| 6 | B06 | Normal map changes lighting, not geometry; silhouette stays round | Correct | Godot docs Normal map: "This does not modify geometry, only the incident angle for light."; capture normal | none |
| 7 | B07 | AO affects ambient light, not direct light, by default | Correct | Godot docs AO: "it does not affect direct light by default"; chapter: ao_light_affect defaults to 0.0 | none |
| 8 | B08 | The renderer combines the measurements with light and camera per pixel | Correct (conceptual) | /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/chapters/07-materials-and-textures.md: "A light and a camera then turn those quantities into a colour." | none |
| 9 | B09 | Material judged under stated lighting; materials unchanged across presets | Correct; capture keeps materials fixed | /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/chapters/07-materials-and-textures.md consequences list; capture lights | none |
| 10 | B10 | Only base colour is a colour; the rest are data in image files | Correct | /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/chapters/07-materials-and-textures.md: "Only the base colour is a colour. The rest are data that happen to be stored in an image file." | none |

Nothing datable (no prices, versions beyond Godot 4.7.2 on the capture label, or dates) is spoken. Sources checked 2026-11-13.
