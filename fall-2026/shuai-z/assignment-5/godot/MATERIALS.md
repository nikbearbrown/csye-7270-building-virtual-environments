# MATERIALS — audit of the textured shader, the hint experiment and their textures

Audited on 2026-10-27 against `CHANGE-BRIEF.md`, revision 1 with revision 2 (the circle's `albedo_tint` is `#A4A7B4`). Every value below was read from the file named beside it. `godot/tests/test_materials.gd` asserts these tables: run it from `assignment-5/` with `scripts/run-test.sh godot test_materials.gd 60` (log: `logs/godot_test_materials_60fps.log`, 125 PASS, 0 FAIL, `all checks passed`).

Claude Code (Claude Opus 5.5) did this audit and drafted this file and the test; nothing in a `.gdshader`, material, scene or `.import` file was changed.

## Materials

| Resource | Shader | Uniform values it sets | Textures it binds | On |
|---|---|---|---|---|
| `res://materials/waystone_stone.tres` | `res://shaders/weathered_stone.gdshader` (`waystone_stone.tres:3`) | `albedo_tint` `Color(1, 1, 1, 1)` = `#FFFFFF`; `uv_scale` 1.0; `normal_strength` 1.0; `roughness_offset` 0.0 (lines 13–16) | `albedo_tex` ← `rock_01_diff_1k.png`; `normal_tex` ← `rock_01_nor_gl_1k.png`; `roughness_tex` ← `rock_01_rough_1k.png` (lines 4–6, 10–12) | `surface_material_override/0` of `Waystone/Waystone`, the imported surface `Stone` (`props_room.tscn:53-54`) |
| `res://materials/circle_darkstone.tres` | `res://shaders/weathered_stone.gdshader` (`circle_darkstone.tres:3`) | `albedo_tint` `Color(0.6431373, 0.654902, 0.7058824, 1)` = `#A4A7B4`; `uv_scale` 1.0; `normal_strength` 0.35; `roughness_offset` −0.25 (lines 13–16) | the same three (lines 4–6, 10–12) | `surface_material_override/1` of `TeleportCircle/TeleportCircle`, the imported surface `DarkStone` (`props_room.tscn:59-60`) |
| `res://materials/hint_source_color.tres` | `res://shaders/hint_experiment.gdshader` (`hint_source_color.tres:3`) | `use_source_color` true (line 10) | `source_color_tex` and `plain_tex` ← `grey_strip_3x1.png` (lines 4, 8–9) | `material_override` of `QuadA` (`hint_experiment.tscn:21-24`) |
| `res://materials/hint_plain.tres` | `res://shaders/hint_experiment.gdshader` (`hint_plain.tres:3`) | `use_source_color` false (line 10) | `source_color_tex` and `plain_tex` ← `grey_strip_3x1.png` (lines 4, 8–9) | `material_override` of `QuadB` (`hint_experiment.tscn:32-35`) |

Both stone materials load the same `Shader` resource, so a change to the shader changes both. Each material sets every uniform its shader declares, and nothing else. The other four surfaces of the two meshes (`Moss`, `Rune`, `Gold`, `PaleGold`) have no override and keep their imported `StandardMaterial3D`. No other mesh in `props_room.tscn` uses the textured shader.

The shaders' own defaults, from the source text (the dummy renderer reports none):

| Shader | Uniform | Type and hint | Default |
|---|---|---|---|
| `weathered_stone.gdshader` | `albedo_tint` (group `surface`) | `vec4 : source_color` (line 8) | `vec4(1.0)` |
| | `uv_scale` (group `surface`) | `float : hint_range(0.25, 4.0, 0.05)` (line 9) | `1.0` |
| | `normal_strength` (group `relief`) | `float : hint_range(0.0, 2.0, 0.05)` (line 12) | `1.0` |
| | `roughness_offset` (group `relief`) | `float : hint_range(-0.5, 0.5, 0.01)` (line 13) | `0.0` |
| `hint_experiment.gdshader` | `use_source_color` | `bool` (line 6) | `false` |

`get_shader_uniform_list(true)` reports, in order: `albedo_tex`, `normal_tex`, `roughness_tex` (Object, `Texture2D`), group `surface`, `albedo_tint` (Color), `uv_scale` (float, range), group `relief`, `normal_strength`, `roughness_offset` (float, range): nine entries. For the hint shader: `source_color_tex`, `plain_tex` (Object, `Texture2D`), `use_source_color` (bool).

## Samplers

The hints are as written in the source. The import settings are from each texture's `.import` file, `[params]`.

| Shader | Sampler | Hints (source) | Bound by | Texture | `compress/mode` | `compress/normal_map` | `mipmaps/generate` | Other settings the brief sets |
|---|---|---|---|---|---|---|---|---|
| `weathered_stone` | `albedo_tex` | `source_color, filter_linear_mipmap, repeat_enable` (line 3) | both stone materials | `rock_01_diff_1k.png` | 2 VRAM Compressed (`.import:19`) | 2 Disabled (`:25`) | true (`:27`) | `detect_3d/compress_to` 0 Disabled (`:41`) |
| `weathered_stone` | `normal_tex` | `hint_normal, filter_linear_mipmap, repeat_enable` (line 4) | both stone materials | `rock_01_nor_gl_1k.png` | 2 VRAM Compressed (`:19`) | 1 Enable (`:25`) | true (`:27`) | `detect_3d/compress_to` 0 Disabled (`:41`); `process/normal_map_invert_y` false (`:37`) |
| `weathered_stone` | `roughness_tex` | `filter_linear_mipmap, repeat_enable` (line 5) | both stone materials | `rock_01_rough_1k.png` | 2 VRAM Compressed (`:19`) | 2 Disabled (`:25`) | true (`:27`) | `detect_3d/compress_to` 0 Disabled (`:41`); `roughness/mode` 1 Disabled (`:29`) |
| `hint_experiment` | `source_color_tex` | `source_color, filter_nearest` (line 4) | both hint materials | `grey_strip_3x1.png` | 0 Lossless (`:18`) | 2 Disabled (`:24`) | false (`:26`) | `detect_3d/compress_to` 0 Disabled (`:40`) |
| `hint_experiment` | `plain_tex` | `filter_nearest` (line 5) | both hint materials | `grey_strip_3x1.png` | 0 Lossless (`:18`) | 2 Disabled (`:24`) | false (`:26`) | `detect_3d/compress_to` 0 Disabled (`:40`) |
| — | (no sampler) | — | no material | `rock_01_nor_dx_1k.png` | 0 Lossless (`:18`) | 2 Disabled (`:24`) | false (`:26`) | `detect_3d/compress_to` 0 Disabled (`:40`) |

The integers are the importer's enums, from Godot 4.7.2's `editor/import/resource_importer_texture.cpp`: `compress/mode` 0 Lossless, 1 Lossy, 2 VRAM Compressed; `compress/normal_map` 0 Detect, 1 Enable, 2 Disabled; `compress/channel_pack` 0 sRGB Friendly, 1 Optimized; `roughness/mode` 0 Detect, 1 Disabled; `detect_3d/compress_to` 0 Disabled, 1 VRAM Compressed.

All of these match the brief, sections 4 and 5. What the import produced on this machine (Godot 4.7.2, macOS; `get_image()`, printed as INFO by the test): the colour and roughness maps are format 17 (DXT1) and the GL normal map format 21 (RGTC_RG), each 1024 × 1024 with 10 mipmap levels; the DX normal map is format 4 (RGB8) with none; the strip is 3 × 1, RGB8, with none.

Normal-map convention, from `normal_map_check.gd`'s curl ratio of each source file (decoded with `Image.load_from_file`, not the import):

| File | `directx = false` | `directx = true` | Reads as |
|---|---|---|---|
| `rock_01_nor_gl_1k.png` (bound) | 0.1444 | 1.8556 | OpenGL (Y+), which Godot expects |
| `rock_01_nor_dx_1k.png` (calibration only) | 1.8556 | 0.1444 | DirectX (Y−) |

The same numbers as the calibration run (`logs/godot_calibrate_normal_map_check_60fps.log`).

## Lights and environment

**`scenes/props_room.tscn`** (the stone materials):

| Setting | Value | Where |
|---|---|---|
| Light | one `DirectionalLight3D`, `Sun`, `light_energy` 1.1, `shadow_enabled` true, colour white (default) | `props_room.tscn:42-45` |
| Background | `background_mode` 1 Custom Color, `#9DB8CF` | `:10-11` |
| Ambient | `ambient_light_source` 2 Color, `Color(1, 0.957, 0.878)`, energy 0.45 | `:12-14` |
| Tonemap | `tonemap_mode` 2 Filmic | `:15` |
| Exposure and white | `tonemap_exposure` 1.0, `tonemap_white` 1.0 (defaults; not in the file) | read from the loaded Environment |
| Post effects | glow, fog, volumetric fog, adjustments, SSAO, SSIL, SSR, SDFGI all off (defaults; not in the file) | read from the loaded Environment |
| Camera | `Camera`, FOV 50, 22.97° down toward the props (computed from its transform) | `:66-69` |

**`scenes/hint_experiment.tscn`** (the hint materials):

| Setting | Value | Where |
|---|---|---|
| Lights | none; both quads are `unshaded` (`hint_experiment.gdshader:2`) | whole scene |
| Background | `background_mode` 1 Custom Color, `Color(0.125, 0.157, 0.188)` | `hint_experiment.tscn:7-8` |
| Tonemap | `tonemap_mode` 0 Linear, `tonemap_exposure` 1.0, `tonemap_white` 1.0 (defaults; not in the file) | read from the loaded Environment |
| Post effects | glow, fog, volumetric fog, adjustments, SSAO, SSIL, SSR, SDFGI all off (defaults) | read from the loaded Environment |
| Camera | `Camera`, no rotation, 2.5 m in front of the quads, FOV 50 | `:43-46` |

## Findings

Nothing contradicts the brief's tables. These are the things that look wasteful, unused, stale or unchecked.

1. **The roughness map is stored as three compressed channels of 8-bit data, and the shader reads one.** The source is 16-bit greyscale (`ATTRIBUTION.md:24`). The shader reads only `.r` (`weathered_stone.gdshader:21`). It imports as VRAM Compressed (`rock_01_rough_1k.png.import:19`) with `compress/channel_pack=0`, sRGB Friendly (`:26`), and comes out as DXT1 (format 17, test INFO line): 8-bit, block-compressed RGB. That costs both the 16-bit precision and DXT1's block error on a data map, for a channel the shader then throws two-thirds of away. It is what the brief asks for (section 5: `compress/mode` 2), so it is not a mismatch; whether a single-channel format would serve better is a question for a brief revision, and I have not tested one.
2. **`rock_01_nor_dx_1k.png` is imported though nothing binds it.** It is the curl check's calibration file only (`ATTRIBUTION.md:13`), imported Lossless with no mipmaps (`rock_01_nor_dx_1k.png.import:18`, `:26`), which comes out as RGB8 at 1024 × 1024 (test INFO line). Its file in `.godot/imported/` is 1,908,496 bytes, because a lossless import is stored compressed; decoded, the image is 3,145,728 bytes. Harmless in the editor; it would also ship in an export unless it is excluded there.
3. **Each hint material binds the strip to a sampler it never reads.** `hint_experiment.gdshader:9-13` reads `source_color_tex` or `plain_tex`, never both, but both materials bind the strip to both (`hint_source_color.tres:8-9`, `hint_plain.tres:8-9`). This is the brief's design (section 4: "Two samplers are bound to that same file"), so the two materials differ only in the bool; the unused binding changes nothing on screen. Also, `hint_plain.tres:10` sets `use_source_color = false`, which is already the shader's default (`hint_experiment.gdshader:6`): redundant, but explicit.
4. **The brief's line numbers for the props room's lighting are stale.** Section 5 cites `props_room.tscn` "lines 7–13 and 40–43". The two `ext_resource` lines for the materials (`props_room.tscn:5`, `:7`) pushed them down: the Environment is now lines 9–15 and `Sun` lines 42–45. `CLAUDE.md` already cites the current lines. The values themselves are unchanged.
5. **The circle is seen at a low angle with no anisotropic filtering.** All three stone samplers use `filter_linear_mipmap` (`weathered_stone.gdshader:3-5`), and the camera looks down at 22.97° (computed from its transform, `props_room.tscn:67`) onto the circle's flat disc. Trilinear filtering at that angle usually blurs the far side of the disc; `filter_linear_mipmap_anisotropic` usually keeps it sharp. This is a look question for the human sweep, not a mismatch; the brief names `filter_linear_mipmap`.
6. **The material ext_resources in `props_room.tscn` have no `uid`.** Lines 5 and 7 reference the two `.tres` files by path only (so do the `.glb` lines, 3, 4 and 6, written by `build_props_room.gd`), while the `.tres` files reference their shader and textures by uid and path. The scene loads correctly, but the editor may add `uid=` to these lines the first time it saves the scene, which would show as a diff in `git status`.
7. **Not checked: how big the photo is on the props.** The brief describes `uv_scale` as "how many times the 1.5 m photo repeats across the UVs". Whether `uv_scale` 1.0 shows the rock at its real size depends on the UV layout inside each `.glb`, which this audit did not read.
8. **Not done here: brief section 6, prediction 7's mutation.** The brief says deleting `source_color` from `albedo_tex` must make `test_materials.gd` exit 1. The test compares each sampler's hint list exactly (the `albedo_tex hints are …` line), so that mutation should fail it, but the shader is hand-written and an agent does not edit it (`CLAUDE.md`, Ownership); the mutation run is yours.

## Attribution

All four textures in `godot/assets/textures/rock_01/` are Poly Haven's **Rock 01** (`rock_01`), recorded in `godot/assets/textures/rock_01/ATTRIBUTION.md`.

| | |
|---|---|
| Page | https://polyhaven.com/a/rock_01 |
| Author and role | Rob Tuytel, role "All" (Poly Haven's API, https://api.polyhaven.com/info/rock_01) |
| Published | 2018-08-09 |
| Real-world size | 1500 × 1500 mm (the brief: width 1.5 m) |
| Licence | CC0 1.0, https://creativecommons.org/publicdomain/zero/1.0/. Poly Haven's licence page, https://polyhaven.com/license, says "Our assets are all licensed as CC0" and that no credit is required. The course requires this record anyway. |
| Downloaded | 2026-10-27, as 1k PNGs |
| Checked | 2026-10-27: the author, role, date and size in the API, and the licence page |
| Normal-map convention | `_nor_gl`, OpenGL (Y+), which Godot expects. `_nor_dx` is here only to calibrate `godot/tests/normal_map_check.gd`; no material binds it. |

| File | Source URL | Bytes | MD5 | Format |
|---|---|---|---|---|
| `rock_01_diff_1k.png` | https://dl.polyhaven.org/file/ph-assets/Textures/png/1k/rock_01/rock_01_diff_1k.png | 2,324,722 | `c29597dec4148d5ebaba69a237e382de` | 1024 × 1024, 8-bit RGB |
| `rock_01_nor_gl_1k.png` | https://dl.polyhaven.org/file/ph-assets/Textures/png/1k/rock_01/rock_01_nor_gl_1k.png | 1,913,482 | `74a313abbc4720f0bd413d7d88801fc1` | 1024 × 1024, 8-bit RGB |
| `rock_01_nor_dx_1k.png` | https://dl.polyhaven.org/file/ph-assets/Textures/png/1k/rock_01/rock_01_nor_dx_1k.png | 1,913,469 | `d6932416ebfd5e3a4e52543f5df55e58` | 1024 × 1024, 8-bit RGB |
| `rock_01_rough_1k.png` | https://dl.polyhaven.org/file/ph-assets/Textures/png/1k/rock_01/rock_01_rough_1k.png | 1,881,279 | `0ced2505764d992f4743eb651e8feab5` | 1024 × 1024, 16-bit greyscale |

The sizes and MD5 sums are the ones Poly Haven's API lists (https://api.polyhaven.com/files/rock_01).

`grey_strip_3x1.png` is not a download: `godot/tools/write_grey_strip.gd` writes it.

## What the test cannot establish headlessly

- **Anything drawn.** `--headless` uses the dummy renderer, which draws nothing and cannot read a frame back. So the hint experiment's displayed values (brief section 4: 64/128/192 on quad A, 137/188/225 on quad B) and the stone's look under the Sun (section 5) are not tested.
- **That the sampler hints do what they say.** The engine reports no sampler hints, so the test reads them from the source text. It proves they are written, not that the GPU decodes `albedo_tex` from sRGB.
- **That the shaders compile for the GPU.** The parser runs, and the uniform lists come back full (an empty list means a parse failure), with no `SHADER ERROR` in the log, but the dummy renderer compiles no GPU code.
- **That the editor leaves the `.import` files alone.** The test reads them as they are on disk. Whether the editor rewrites one the first time it draws the texture (brief section 6, prediction 8) shows only in `git status` after an editor session.
- **The import's GPU format on other platforms.** The DXT1 and RGTC_RG formats are this machine's (`s3tc_bptc` in the `.import` metadata), so the test prints them and does not assert them.
- **The normal map in the renderer.** The curl ratio is computed from the source PNG, not from the RGTC_RG import or from what the shader does with it.

## Review

The audit above was committed unedited (`cd1e71a3`) and then reviewed on 2026-10-27. Claude Code did the review at my request.

- **Integer enums.** Each one was looked up: the importer's in Godot 4.7.2's `editor/import/resource_importer_texture.cpp`, and those of `Environment` and `Image.Format` in the engine's `ClassDB`. Every name the audit gave was right. Two values had no name, `detect_3d/compress_to` 0 and `compress/channel_pack` 0, and now do.
- **Formats.** `get_image().get_format()` reads 17 (DXT1), 21 (RGTC_RG) and 4 (RGB8), as the audit says (the test's INFO lines; `logs/probe_textures.log`). The `.import` metadata does say `"imported_formats": ["s3tc_bptc"]`.
- **Numbers nobody measured.** "About 3 MB" for the DirectX map's import was wrong: its file is 1,908,496 bytes, and 3,145,728 bytes is the decoded image. "About 23°" is now 22.97°, computed from the camera's transform.
- **Findings.** All eight stand. The stale line numbers of finding 4 are corrected in the brief's revision 3. Finding 8, the mutation, is next.
- **The test** is unchanged apart from a comment that names the importer enums it compares.
