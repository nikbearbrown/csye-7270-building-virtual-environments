# MATERIALS — audit of the Assignment 5 materials

Audit of 2026-10-28, covering CHANGE-BRIEF.md section 3 (the hint experiment), section 4 and its revisions (the frosted rock). Paths are relative to `walker-magic-zhefan/` (`res://`). Every value below is pinned by `tests/test_materials.gd`, which runs with `./scripts/run-test.sh test_materials.gd 60` from `fall-2026/zhefan-z/assignment-5/`. Nothing here was checked on screen: the headless run uses a dummy renderer.

## Materials

| Material | Shader | Uniform values it sets | Textures it binds |
|---|---|---|---|
| `assets/materials/mat_rock_dry.tres` | `shaders/rock_frost.gdshader` | `base_tint = Color(1, 1, 1, 1)`, `normal_scale = 1.0`, `roughness_scale = 1.0`, `frost_color = Color(0.85, 0.92, 1, 1)`, `frost_amount = 0.0` (lines 10–14) | `texture_albedo` = `rock_01_diff_1k.png`, `texture_normal` = `rock_01_nor_gl_1k.png`, `texture_roughness` = `rock_01_rough_1k.png` (lines 15–17) |
| `assets/materials/mat_rock_frosted.tres` | `shaders/rock_frost.gdshader` | `base_tint = Color(0.92, 0.95, 1, 1)`, `normal_scale = 1.0`, `roughness_scale = 1.0`, `frost_color = Color(0.85, 0.92, 1, 1)`, `frost_amount = 0.65` (lines 10–14) | same three as the dry material (lines 15–17) |
| `assets/materials/mat_hint_source_color.tres` | `shaders/hint_experiment.gdshader` | `use_source_color = true` (line 10) | `source_color_tex` = `greys_3x1.png`, `raw_data_tex` = `greys_3x1.png` (lines 8–9) |
| `assets/materials/mat_hint_raw_data.tres` | `shaders/hint_experiment.gdshader` | `use_source_color = false` (line 10) | same two as above (lines 8–9) |

- Each material sets every uniform its shader declares; none is left at the shader default.
- The two rock materials differ only in `base_tint` and `frost_amount`, as section 4 says. The two hint materials differ only in `use_source_color`.
- Texture paths are under `assets/textures/rock_01/` and `assets/textures/hint/`.
- Where they are used:
  - `showcase3d/material_compare.tscn:28–29, 34–35`: `surface_material_override/0` on `RockDry/Rock` (dry) and `RockFrosted/Rock` (frosted). Surface 0 is `Rock_Main`, and surface 1, `Rock_Top`, has no override and keeps its imported `StandardMaterial3D`.
  - `showcase3d/hint_experiment.tscn:28, 33`: the `QuadSourceColor` quad at x = −0.6 and the `QuadRawData` quad at x = +0.6.

## Samplers

The hints are as written in the source; the import settings come from each texture's `.import` file, `[params]` section.

| Shader : sampler | Hints as written | Bound texture (both materials) | `compress/mode` | `compress/normal_map` | `mipmaps/generate` | Imported format |
|---|---|---|---|---|---|---|
| `rock_frost.gdshader:16` `texture_albedo` | `source_color, filter_linear_mipmap` | `rock_01_diff_1k.png` | 2, VRAM Compressed | 2, Disabled | true | `FORMAT_DXT1` (17), 1024², mipmaps |
| `rock_frost.gdshader:17` `texture_normal` | `hint_normal, filter_linear_mipmap` | `rock_01_nor_gl_1k.png` | 2, VRAM Compressed | 1, Enable | true | `FORMAT_RGTC_RG` (21), 1024², mipmaps |
| `rock_frost.gdshader:18` `texture_roughness` | `hint_default_white, filter_linear_mipmap` | `rock_01_rough_1k.png` | 2, VRAM Compressed | 2, Disabled | true | `FORMAT_DXT1` (17), 1024², mipmaps |
| `hint_experiment.gdshader:4` `source_color_tex` | `source_color, filter_nearest` | `greys_3x1.png` | 0, Lossless | 2, Disabled | false | `FORMAT_RGB8` (4), 3×1, no mipmaps, texels 64/128/192 |
| `hint_experiment.gdshader:5` `raw_data_tex` | `filter_nearest` | `greys_3x1.png` | 0, Lossless | 2, Disabled | false | as above |
| (no sampler) | — | `rock_01_nor_dx_1k.png`, bound by no material | 2, VRAM Compressed | 1, Enable | true | `FORMAT_RGTC_RG` (21), 1024², mipmaps |

- **Where the settings are in each `.import` file:**
  - rock_01 files: line 19 (`compress/mode`), 25 (`compress/normal_map`), 27 (`mipmaps/generate`) and 41 (`detect_3d/compress_to`).
  - `greys_3x1.png.import`: lines 18, 24, 26 and 40.
- **`detect_3d/compress_to`:** all five files set it to 0, Disabled, as section 4 asks.
- **Imported format:** these are the formats on this machine (`imported_formats: ["s3tc_bptc"]`, rock_01 `.import` line 8). Another platform's VRAM format would differ. The test compares them with the engine's own `Image.FORMAT_*` constants.

**Meaning of the integers.**
- **`compress/mode`:** 0 Lossless, 1 Lossy, 2 VRAM Compressed, 3 VRAM Uncompressed, 4 Basis Universal. Source: the documentation page for ResourceImporterTexture lists the options in that order ([docs.godotengine.org/en/4.7/classes/class_resourceimportertexture.html](https://docs.godotengine.org/en/4.7/classes/class_resourceimportertexture.html), "Godot Engine 4.7 documentation"). The same order is in the engine's enum string `"Lossless,Lossy,VRAM Compressed,VRAM Uncompressed,Basis Universal"` (`editor/import/resource_importer_texture.cpp`, tag `4.7.2-stable`).
- **`compress/normal_map`:** 0 Detect, 1 Enable, 2 Disabled.
  - The documentation gives only the default, `0`, which is Detect ("By default, it's set to Detect"). It does not number Enable or Disabled.
  - Those two come from the engine source at the same tag: `PROPERTY_HINT_ENUM, "Detect,Enable,Disabled"`.
- **`mipmaps/generate`:** a bool, not an integer (documentation: default `false`; "If true, smaller versions of the texture are generated on import").
- **`detect_3d/compress_to`:** 0 Disabled, 1 VRAM Compressed, 2 Basis Universal. The documentation names these options but does not number them, so the integers come from the engine source: `"Disabled,VRAM Compressed,Basis Universal"`.

**Uniform lists.** `get_shader_uniform_list()`, read after the main loop has started, reports:
- `rock_frost`:
  - `base_tint` Color and `frost_color` Color;
  - `normal_scale` float, range `0,2,0.05`; `roughness_scale` float, range `0,2,0.05`; `frost_amount` float, range `0,1,0.01`;
  - three `Texture2D` objects.
- `hint_experiment`: two `Texture2D` objects and `use_source_color` bool.

**Normal-map convention** (`tests/normal_map_check.gd`, run on each source PNG, stride 4):

| File | `curl_ratio`, OpenGL | `curl_ratio`, DirectX |
|---|---|---|
| `rock_01_nor_gl_1k.png` (bound) | 0.1444 | 1.8556 |
| `rock_01_nor_dx_1k.png` (unbound) | 1.8556 | 0.1444 |

The thresholds come from `logs/calibrate_normal_check_60fps.log:7–8, 13–14`: the bound map must be below 0.5 in OpenGL and above 1.5 in DirectX. The bound map reads as a real surface in the OpenGL convention, which Godot expects.

## Lights and environment

| Scene | Setting | Value | Evidence |
|---|---|---|---|
| `material_compare.tscn` | Light | One `DirectionalLight3D` "Sun". Energy 1.0 and colour white (defaults), shadows on. It comes from above (45° elevation) at the camera's left (the light's +Z axis is (−0.35, 0.71, 0.61)) | `material_compare.tscn:16–18` |
| | Background | `background_mode = 1` (Color), `#0F1119` | `:7–9` |
| | Ambient light | source 0, Background (default), so ambient light is the dark background colour | not written; read back by the test |
| | Tonemap | `tonemap_mode` 0 = Linear, `tonemap_exposure` 1.0 (defaults) | not written; read back by the test |
| | Off (defaults) | glow, fog, volumetric fog, SSAO, SSIL, SSR, SDFGI, adjustments | not written; read back by the test |
| | Same as the prop room? | Environment and light read back identical to `prop_room.tscn:16–18, 28–30` | test check `compare-scene-environment`, `compare-scene-lights` |
| | Floor | none, so the rocks cast no visible ground shadow | user's instruction for this scene |
| `hint_experiment.tscn` | Light | none; both quads are `render_mode unshaded` | `hint_experiment.gdshader:2` |
| | Tonemap | `tonemap_mode = 0` (Linear), `tonemap_exposure = 1.0`, written explicitly | `hint_experiment.tscn:10–11` |
| | Off | `glow_enabled`, `fog_enabled`, `adjustment_enabled` = false, written explicitly | `hint_experiment.tscn:12–14` |
| | Background | `background_mode` 0 (Clear Color, default); it does not reach the quads | not written |
| | Camera | at (0, 0, 2), default fov, facing the quads | `hint_experiment.tscn:21–23` |

## Findings

1. **Roughness precision (possible visible artefact, unconfirmed).**
   - **Evidence:** `rock_01_rough_1k.png.import:19` `compress/mode=2`; the imported format is `FORMAT_DXT1`.
   - **What happens:** the source is 16-bit greyscale. `Image.load_from_file` reads it as `FORMAT_L8` (0), and the import stores it as DXT1, a colour format with 5-bit red and 6-bit green endpoints.
   - **Measured** (test observation `roughness-import-error-in-8bit-steps`, every 2nd texel, 262,144 samples), the imported texture against the 8-bit source:
     - red channel: mean error 3.0, max 13 steps of 255;
     - green channel: mean 2.72, max 11.
   - **Why it matters:** the shader reads `.r` (`rock_frost.gdshader:24`), and the frost mask's transition band is only ±0.1 wide (`:35`). A 13/255 ≈ 0.05 error is a quarter of that band, so the frost edge may show 4×4 block steps.
   - **Next step:** a human should look at it at `frost_amount` 0.65. If it shows, options are a non-VRAM `compress/mode` for this one file (a change to section 4's table) or reading `.g`. Both are your call; nothing was changed.
2. **Unused import (wasteful, by design).**
   - **Evidence:** `rock_01_nor_dx_1k.png.import:19, 25, 27`.
   - `rock_01_nor_dx_1k.png` is imported VRAM-compressed with mipmaps, but no material binds it: the test's `bound_to` is `[]`, and outside the tests only `tests/calibrate_normal_check.gd:8` names it.
   - Both readers decode the source PNG with `Image.load_from_file`, never the imported texture. So the `.ctex` is never used, and an export of all resources would ship it.
   - Section 4 states that it is "not bound to any material"; the import itself is what goes unused.
3. **Alpha unused.** `base_tint` and `frost_color` are `vec4`, but only `.rgb` is used (`rock_frost.gdshader:28, 38`), and `ALPHA` is never written. Harmless: both materials set alpha 1.
4. **The ice roughness is a constant, not a uniform.** `rock_frost.gdshader:42` `float ice_roughness = 0.15;`. Section 4 says "frosted areas get lower roughness" without a value, so this is consistent, but it cannot be tuned from a material.
5. **`roughness_scale` does not move the frost.** The mask uses the unscaled `rough_tex` (`rock_frost.gdshader:35`); only the base roughness is scaled (`:41`). This agrees with section 4 ("the roughness map, read as data, decides where frost settles"). It is noted because the uniform table could suggest otherwise.
6. **Checked, not a problem: normal map `.rgb` from RGTC_RG.**
   - **The concern:** the documentation warns that RGTC (`compress/normal_map` Enable) affects the blue channel, and the shader passes `.rgb` to `NORMAL_MAP` (`rock_frost.gdshader:25, 46`).
   - **Why it is fine:** the engine's 4.7.2 scene shader (`scene_forward_clustered.glsl`, tag `4.7.2-stable`) rebuilds Z from XY (`normal_map.z = sqrt(max(0.0, 1.0 - dot(normal_map.xy, normal_map.xy)))`) and says "always ignore Z, as it can be RG packed". So the blue channel is never used.
   - **Tangents:** the rock mesh has them on surface 0 (`rock.glb.import:26` `meshes/ensure_tangents=true`; the test's `tangents_0` is true).
7. **Materials referenced without a UID.**
   - **Evidence:** `material_compare.tscn:4–5`, `hint_experiment.tscn:3–4`, and line 1 of each `.tres`.
   - The four `.tres` files have no `uid=` in their header, and both scenes reference them without `uid=`. Godot writes one on its own saves, so the first editor save may rewrite these lines.
8. **CLAUDE.md is out of date in five places** (it's your file, so I left it unchanged):
   - `CLAUDE.md:34–38` describes the prop room as the place for the textured shader. After revision 2026-10-27 the shader is only in `material_compare.tscn`.
   - `CLAUDE.md:97` says `rock.glb.import` may change. Revision 2026-10-27 keeps it as in Assignment 3.
   - `CLAUDE.md:108–109` says the surface index of `Rock_Main` is still to be confirmed. It is surface 0, confirmed headlessly (revision 2026-10-27; test `compare-scene-rock:*`).
   - `CLAUDE.md:110–113` lists the materials, scenes, hint folder and driver as not created; they all exist.
   - `CLAUDE.md:114–115` says the rock_01 PNGs have no `.import` files and the roughness format is unknown. They do have `.import` files, and the format is `FORMAT_DXT1`.
9. **Section 4's scene paragraph is superseded.** It still describes Use External in the prop room. Revision 2026-10-27 already marks it as superseded, and the files follow the revision. Nothing is inconsistent; it is noted so the table above is read against the revision.

## Attribution

From CHANGE-BRIEF.md only:

- **Author** of CHANGE-BRIEF.md: Zhefan Zhang (zhefan-z). Original version 2026-10-22, with dated revisions at the end.
- **Mine, per the brief:** "every decision, the colour line, all uniform and sampler declarations, and every hand computation".
  - This covers the sampler and uniform declarations of `rock_frost.gdshader` audited above.
  - It also covers the hint-experiment predictions (64/128/192 with `source_color`; 137/188/225 without).
- **claude.ai (chat):** compiled the file from those answers, looked up the project facts with the author, and checked the arithmetic.
  - It corrected the first 128 result in section 3: 187, which came from 0.74836 instead of 0.75038.
- **Translations:** passages marked *(translated from my Chinese)* are the author's own explanations, translated.
  - In the parts audited here, that is section 3's explanation of why the `source_color` quad shows the file's values unchanged.
- **`shaders/rock_frost.gdshader`:** "Hand-written by me" (section 4).
- **Textures:** Poly Haven "Rock 01", https://polyhaven.com/a/rock_01, author Rob Tuytel, CC0, 1K PNG. Downloaded 2026-10-22 from `dl.polyhaven.org`, unmodified.

Not recorded in CHANGE-BRIEF.md, so not attributed here:
- who wrote `shaders/hint_experiment.gdshader`;
- who wrote the four `.tres` materials, the two scenes, `tools/write_hint_png.gd` and `greys_3x1.png`;
- who wrote `tests/normal_map_check.gd`, this file and `tests/test_materials.gd`.
