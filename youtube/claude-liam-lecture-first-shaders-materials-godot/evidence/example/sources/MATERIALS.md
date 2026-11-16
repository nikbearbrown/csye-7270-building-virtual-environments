# Course-series material audit

Instructor implementation under Bear's direction. The original Signal Garden resources are unchanged. This audit covers `godot/course-series/`; historical assignment folders retain their original numbering.

| Object/material | Shader | Values |
|---|---|---|
| Signal pad, per-instance ShaderMaterial | `shaders/signal.gdshader` | activation ← charge / 0.6; texture-free |
| MaterialSpecimen0 / matte.tres | `shaders/surface.gdshader` | tint white; roughness .9; scale 1; metallic 0 |
| MaterialSpecimen1 / coated.tres | same | tint (.45,.95,.72); roughness .25; scale 2; metallic .4 |
| ConversionScratch only | exact generated shader embedded in scene | albedo (.85,.8,.7), roughness .65, metallic .2, normal strength 1 |

| Texture | Meaning / shader hint | Explicit import / provenance |
|---|---|---|
| gate-color.png | RGB color; source_color | Lossless mode0, normal disabled2, mipmaps false, Detect compression0 |
| gate-roughness.png | Red-channel roughness data; no source_color | Same explicit import settings |
| analytic-normal-gl.png | Analytic OpenGL normal; scratch conversion only | Same explicit import settings; code-authored source |

Texture source copies derive from this repository's `scripts/garden-textures.py`; no external art grant is inferred. Source images are 64×64. Loaded color/roughness format is enum4, RGB8, as measured by get_image().get_format(); this is not a claim about GPU memory allocation. Enum names follow Godot's Image and texture-import documentation. Normal calibration uses the attributed Poly Haven Stone Floor GL/DX pair in `godot/course-series/normal-calibration/ATTRIBUTION.md`.

The 53-check material test asserts declared names/types, hints, groups, both materials' exact values and texture paths, and ConfigFile import values. Initial source_color vec4 assertions incorrectly expected TYPE_VECTOR4; Godot's uniform list reports TYPE_COLOR. The failing log and repaired log are retained. Analytic normal curl ratio: GL .054465, DX 1.945535. The sourced GL/DX calibration identifies the expected convention, without pretending every valid map yields zero.

Actual native captures use a fixed orthographic camera, Linear tonemap/exposure1, directional light at (-30,-30,0), ambient energy .35, and no SSAO. The baseline shows two distinct resources. A temporary shared shader edit changes both; a temporary tint edit changes only the left. Neither edit mutates the saved game material. Twelve parameter settings are captured, with tint treated as color samples. Exact settings/results are in `evidence/course-assignment-series/shaders/material-native-results.json`.

Three isolated mutations (missing semicolon, renamed activation, missing source_color) exit1. They change temporary shader/source instances, not shared project files. Native pixels, human readability and a person's understanding are outside the headless claims.

[Image format enum](https://docs.godotengine.org/en/stable/classes/class_image.html) · [Texture import](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html)
