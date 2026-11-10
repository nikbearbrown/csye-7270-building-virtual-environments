# MATERIALS.md — A5 material audit

> 2026-11-01, written by Claude Code (Claude Opus 5.5) from the audit prompt (`prompt-3.txt`); it changed no `.gdshader`, material, scene or `.import` file. Translated from the Chinese original in my working folder; local folder paths adapted to this repository's layout.
> Paths: `res://…` is a path inside the Godot project (the `godot/` folder in this repository).
> Plan source: the 2026-11-01 revisions at the end of `CHANGE-BRIEF.md` (cited below as "CHANGE-BRIEF line N").
> The test that pins these tables: `res://tests/test_materials.gd`, run with `./scripts/run-test.sh test_materials.gd 60`.

---

## 1. Materials (one row per material)

| Material resource | Shader | Uniform values stored in the material | Textures bound | Uniforms not stored (shader default applies) |
|---|---|---|---|---|
| `res://assets/furniture/materials/crate_long_wear.tres` | `res://shaders/crate_wear.gdshader` (lines 3, 9) | `paint_roughness = 0.95`, `wear_amount = 0.2` (lines 12–13) | `rust_albedo` ← `Metal041C_1K-PNG_Color.png`, `wear_mask` ← `Metal041C_1K-PNG_Displacement.png` (lines 4–5, 10–11) | `paint_color`, `wear_softness`, `texture_scale` |
| `res://assets/furniture/materials/crate_cube_wear.tres` | `res://shaders/crate_wear.gdshader` (lines 3, 9) | `paint_roughness = 0.85`, `wear_amount = 0.1` (lines 12–13) | Same as above (lines 4–5, 10–11) | `paint_color`, `wear_softness`, `texture_scale` |
| `res://experiments/hint/hint_source_color.tres` | `res://shaders/hint_experiment.gdshader` (lines 3, 8) | `use_source_color = true` (line 11) | `greys_source_color` and `greys_raw` both ← `hint_greys_3x1.png` (lines 4, 9–10) | none |
| `res://experiments/hint/hint_raw.tres` | `res://shaders/hint_experiment.gdshader` (lines 3, 8) | `use_source_color = false` (line 11) | `greys_source_color` and `greys_raw` both ← `hint_greys_3x1.png` (lines 4, 9–10) | none |

All four materials have `render_priority = 0`, and none has Local To Scene ticked.

**Shader defaults (apply when the material does not store a value), read from the source:**

| Shader | Uniform | Default | Source line |
|---|---|---|---|
| `crate_wear.gdshader` | `paint_color` (`source_color`, group `paint`) | `vec4(0.260, 0.283, 0.190, 1.0)` | line 7 |
| `crate_wear.gdshader` | `paint_roughness` (`hint_range(0.0, 1.0)`, group `paint`) | 0.85 | line 8 |
| `crate_wear.gdshader` | `wear_amount` (`hint_range(0.0, 1.0)`, group `wear`) | 0.1 | line 11 |
| `crate_wear.gdshader` | `wear_softness` (`hint_range(0.0, 0.2)`, group `wear`) | 0.0 | line 12 |
| `crate_wear.gdshader` | `texture_scale` (`hint_range(0.1, 10.0)`, group `mapping`) | 2.0 | line 15 |
| `crate_wear.gdshader` | constants `RUST_ROUGHNESS` / `MIN_WEAR_SOFTNESS` | 0.79 / 0.001 | lines 19–20 |
| `hint_experiment.gdshader` | `use_source_color` | `true` | line 6 |

**Where they are attached (what actually loads in the scene; checked by the test):**
- `crate_long` and `crate_cube` (`res://base.tscn` lines 141–145) are instances of `.glb` files. In the `_subresources` of the two `.glb.import` files only `Crate_OliveDrab` is behind Use External (`crate_long.glb.import` / `crate_cube.glb.import` lines 42–50: `use_external/enabled = true`, `use_external/path` = `uid://cedrurswxh5f2` / `uid://5v6oyvouvy8s`, `fallback_path` pointing to the matching `.tres`). After instancing `base.tscn`: each crate has 2 surfaces with the wear material and 1 surface still using the `.glb`'s `Crate_Hardware` (`StandardMaterial3D`).
- `QuadSourceColor` / `QuadRaw` (`res://experiments/hint/hint_experiment.tscn` lines 23–31) carry `hint_source_color.tres` / `hint_raw.tres` through `material_override`.

---

## 2. Samplers (one row per sampler in each shader)

Import settings are read from each texture's `.import` file. Meaning of the enum values (checked during review against the option lists of the Godot 4.7.2 texture importer: `compress/mode` is "Lossless,Lossy,VRAM Compressed,VRAM Uncompressed,Basis Universal", `compress/normal_map` is "Detect,Enable,Disabled", `detect_3d/compress_to` is "Disabled,VRAM Compressed,Basis Universal"): `compress/mode` 0 = Lossless, 2 = VRAM Compressed; `compress/normal_map` 1 = Enable, 2 = Disabled; `detect_3d/compress_to` 0 = Disabled.

| Shader | Sampler (source line) | Hints as written in the source | Texture each material binds | `compress/mode` | `compress/normal_map` | `mipmaps/generate` | `get_image().get_format()` after import (measured) |
|---|---|---|---|---|---|---|---|
| `crate_wear.gdshader` | `rust_albedo` (line 3) | `source_color, filter_linear_mipmap, repeat_enable` | Both crate materials bind `Metal041C_1K-PNG_Color.png` | 2 (line 19) | 2 (line 25) | true (line 27) | 17 = `FORMAT_DXT1` |
| `crate_wear.gdshader` | `wear_mask` (line 4) | `filter_linear_mipmap, repeat_enable` | Both crate materials bind `Metal041C_1K-PNG_Displacement.png` | 0 (line 18) | 2 (line 24) | true (line 26) | 0 = `FORMAT_L8` |
| `hint_experiment.gdshader` | `greys_source_color` (line 4) | `source_color, filter_nearest` | Both hint materials bind `hint_greys_3x1.png` | 0 (line 18) | 2 (line 24) | false (line 26) | 4 = `FORMAT_RGB8` |
| `hint_experiment.gdshader` | `greys_raw` (line 5) | `filter_nearest` | Both hint materials bind `hint_greys_3x1.png` | 0 (line 18) | 2 (line 24) | false (line 26) | 4 = `FORMAT_RGB8` |

Textures in the plan that no material samples (the same Metal041C set):

| Texture | Planned use (CHANGE-BRIEF) | `compress/mode` | `compress/normal_map` | `mipmaps/generate` | Format after import (measured) |
|---|---|---|---|---|---|
| `Metal041C_1K-PNG_Roughness.png` | The Step 4 StandardMaterial3D (line 185) | 2 (line 19) | 2 (line 25) | true (line 27) | 17 = `FORMAT_DXT1` |
| `Metal041C_1K-PNG_NormalGL.png` | Step 4 normal map; the normal-map check (line 186) | 2 (line 19) | 1 (line 25) | true (line 27) | 21 = `FORMAT_RGTC_RG` |
| `Metal041C_1K-PNG_NormalDX.png` | Normal-map check calibration only (line 187) | 2 (line 19) | 1 (line 25) | true (line 27) | 21 = `FORMAT_RGTC_RG` |

`detect_3d/compress_to` is 0 in all six `.import` files. The formats after import are the `Image` formats read back on the CPU side in a headless run on this Windows computer (the `.import` files' `imported_formats` is `s3tc_bptc`); the format numbers are the `Image.Format` enum, checked during review against the constants printed by the engine (`FORMAT_L8` = 0, `FORMAT_RGB8` = 4, `FORMAT_DXT1` = 17, `FORMAT_RGTC_RG` = 21).

**Formats of the decoded source files (`Image.load_from_file`, measured):** Color, NormalGL and NormalDX are 4 (`FORMAT_RGB8`), Displacement and Roughness are 0 (`FORMAT_L8`), all 1024 × 1024; `hint_greys_3x1.png` is 4 (`FORMAT_RGB8`), 3 × 1.

**curl_ratio of the normal maps (`curl_ratio` in `tests/normal_map_check.gd`, decoded source files, stride 4, measured):**

| Texture | `directx = false` (GL convention) | `directx = true` (DX convention) |
|---|---|---|
| `Metal041C_1K-PNG_NormalGL.png` | 0.1991 | 1.8009 |
| `Metal041C_1K-PNG_NormalDX.png` | 1.8009 | 0.1991 |

Each map is low under its own convention and near 2 under the other, which matches the assignment's description of a wrong convention. No material uses a normal map (the crate shader does not, CHANGE-BRIEF line 160).

---

## 3. Lights and environment that change the look

### `res://base.tscn` (the scene with the crates)

| Item | Value | Evidence |
|---|---|---|
| Lights | 3 `OmniLight3D`s: `ceiling_light_1`, `ceiling_light_2`, `ceiling_light_3`; no other `Light3D` (counted after instancing, including the player and tablet sub-scenes) | lines 156–182; test |
| Light colour / energy / range / shadow | All three are `Color(0.78, 0.86, 1, 1)`, `light_energy = 1.5`, `omni_range = 8.0`, `shadow_enabled = true` | lines 158–161, 165–168, 179–182 |
| Light positions | `ceiling_light_1` (0.02, 2.60, −3.66); `ceiling_light_2` (5.38, 1.71, −3.63); `ceiling_light_3` (−3.08, 2.90, 0) | lines 157, 164, 178 |
| Background | `background_mode = 1` (Custom Color), `background_color = Color(0.03, 0.035, 0.045, 1)` | lines 12–13 |
| Ambient light | `ambient_light_source = 2` (Color), `ambient_light_color = Color(0.45, 0.5, 0.6, 1)`, `ambient_light_energy = 0.35` | lines 14–16 |
| Tonemap / exposure | Linear (`tonemap_mode = 0`) / 1.0. **Not written in the file**; they come from the `Environment` defaults; the test reads the runtime values | lines 11–16 (none of these keys); test |
| Glow, fog, volumetric fog, adjustments, SSAO, SSIL, SDFGI, SSR | All off (also from the defaults) | test |
| Reflected light source | Not written in the file, default; so reflections come from the background (a very dark background colour) | lines 11–16 |
| Project settings | Forward+, HDR 2D off | `config/features` on line 15 of `project.godot` lists "Forward Plus" and the file has no `rendering_method` key (no override); at runtime `ProjectSettings` reads `forward_plus` and `hdr_2d` off (test) |

### `res://experiments/hint/hint_experiment.tscn`

| Item | Value | Evidence |
|---|---|---|
| Lights | None (the shader is `unshaded`, so lights do not affect the result) | whole file; test |
| Background | `background_mode = 1` (Custom Color), default colour | lines 6–7 |
| Tonemap / exposure | Linear / 1.0, **not written in the file**, from the defaults | lines 6–7; test |
| Glow, fog, adjustments | Off (defaults) | test |
| Camera and quads | `Camera3D` at the origin, `current = true`; two 1.2 × 0.4 `QuadMesh`es at z = −2 facing the camera, offset 0.35 up and down | lines 9–13, 20–31; test |

---

## 4. Findings

| # | Kind | Finding | Evidence |
|---|---|---|---|
| 1 | Worded differently from CHANGE-BRIEF | Neither scene **writes** tonemap, exposure, glow, fog or adjustments; Linear / 1.0 / off are the `Environment` defaults. CHANGE-BRIEF line 239 says the hint scene "sets the Linear tonemap and exposure 1.0", and the assignment also says the WorldEnvironment "sets" these values. The runtime values are right (pinned by the test), but if the defaults changed, the predictions would silently stop holding. **Review note:** when Godot saves a scene it does not write properties equal to their defaults, so these values would not appear in the file even if set in the editor; they are pinned by the test reading the runtime values. | `hint_experiment.tscn` lines 6–7 have only `background_mode = 1`; `base.tscn` lines 11–16 have no `tonemap_*` / `glow_*` keys |
| 2 | Not used yet | `Metal041C_1K-PNG_Roughness.png` and `Metal041C_1K-PNG_NormalGL.png` are imported as planned, but no material in the project binds them; the Step 4 material that the plan uses them for does not exist yet. | Searching the project for `NormalGL` / `Roughness.png` finds them only in `assets/shader/metal041c/ATTRIBUTION.md` lines 12, 16–19 and `tests/normal_map_check.gd` line 15 |
| 3 | Waste | `Metal041C_1K-PNG_NormalDX.png` is imported as a VRAM-compressed texture with mipmaps, but nothing reads the import result: the normal-map check reads the source PNG. Likewise the normal-map check does not check NormalGL as imported (after compression to the two-channel `FORMAT_RGTC_RG`). These settings are in the plan (CHANGE-BRIEF line 187), so this is not an inconsistency, only an import result nobody uses. | `Metal041C_1K-PNG_NormalDX.png.import` lines 19, 25, 27; `tests/normal_map_check.gd` lines 27–28 use `Image.load_from_file` |
| 4 | May not match the CHANGE-BRIEF description | The shader never writes `METALLIC`, so the whole crate (rust and scratches included) is shaded as non-metal (`METALLIC` defaults to 0). CHANGE-BRIEF line 158 says the rust has "silver metal scratches" in it; those scratches will show as grey non-metal. The plan says nothing about metallic, so this is a question for you to decide, not an error. **Review decision (2026-11-01, me): recorded as a known limitation; the shader is not changed; the scratches are shaded as non-metal.** | `crate_wear.gdshader` lines 34–42 write only `ALBEDO` and `ROUGHNESS` |
| 5 | Inconsistent (what is stored) | The two crate materials store only `wear_amount` and `paint_roughness`; `paint_color`, `wear_softness` and `texture_scale` use the shader defaults. This matches the plan's "other parameters use the defaults" (CHANGE-BRIEF lines 215–216), but changing a shader default later will change both crates at once. Also, the two values `crate_cube_wear.tres` stores are exactly the defaults (0.85, 0.1), so the small crate pins those two and not the other three. | `crate_cube_wear.tres` lines 12–13; `crate_wear.gdshader` lines 7–15 |
| 6 | Unused (by design) | Each hint material binds the same PNG to both samplers, but `use_source_color` is fixed, so each material reads only one of them. This is the experiment structure the assignment requires; it is listed here only because each material has a sampler that is bound but never read. | `hint_experiment.gdshader` lines 9–13; `hint_raw.tres` / `hint_source_color.tres` lines 9–11 |
| 7 | Minor waste | The two `QuadMesh` sub-resources in the hint scene are identical (both 1.2 × 0.4) and could be one shared resource. | `hint_experiment.tscn` lines 9–13 |
| 8 | Check (consistent) | The shader chooses the projection axis from the normal, which relies on "every normal points straight along an axis" (CHANGE-BRIEF line 160, which counted 336 normals in the `.glb` files). After import, the surfaces using the wear material have 72 normals per crate, all axis-aligned (largest component > 0.99). The counts differ because they were counted differently (here without the hardware, and as Godot's imported vertices), not a contradiction. | Test `base.tscn: crate_long/crate_cube paint-surface normals all axis-aligned`; `crate_wear.gdshader` lines 23–29 |
| 9 | Check (consistent) | CHANGE-BRIEF line 184 says Displacement is 16-bit greyscale and becomes 8-bit after import. Measured: the source file already decodes to `FORMAT_L8` with `Image.load_from_file`, and it is also `FORMAT_L8` after import (lossless). So the precision drops to 8 bits when the PNG is decoded, not because of import compression. The normal maps (16-bit according to lines 186–187) likewise decode to `FORMAT_RGB8`, and the curl is computed on 8-bit data. | The test's `INFO … source file decodes to Image.Format` lines |
| 10 | Check (consistent) | The wear formula "rust shows in low places first": where the height is below `wear_amount`, w is close to 1 (rust). | `crate_wear.gdshader` line 38; CHANGE-BRIEF line 207 |
| 11 | Side note | `ATTRIBUTION.md` lines 10–11 (who downloaded it, which files from the zip were kept) are not in CHANGE-BRIEF, so I did not check them. | `assets/shader/metal041c/ATTRIBUTION.md` lines 10–11 |

Apart from the table above, the import settings, hints, material values and textures, and the Use External wiring all match CHANGE-BRIEF lines 183–187, 197–203, 213–216 and 237–239 (checked item by item by the test).

---

## 5. Attribution (only the facts in CHANGE-BRIEF lines 168–179)

| Item | Content |
|---|---|
| Textures | **Metal041C** (1K-PNG) from ambientCG; all 5 files from the same set |
| Source URL | https://ambientcg.com/view?id=Metal041C (download: `https://ambientcg.com/get?file=Metal041C_1K-PNG.zip`) |
| Author / role | ambientCG is created and run by Lennart Demes (Münster, Germany; the site's imprint page https://docs.ambientcg.com/legal/); the asset page gives the technique as Procedural (generated procedurally, not a photo scan) |
| Licence | Creative Commons CC0 1.0 Universal (https://docs.ambientcg.com/license/); no credit required. The course requires provenance, so it is written in `ATTRIBUTION.md` next to the textures |
| Date checked | 2026-11-01 |
| Normal-map convention | The game uses only `NormalGL` (Godot uses the OpenGL convention); `NormalDX` only calibrates the normal-map check |
| Not AI-generated | No model or prompt involved |
| Location | `res://assets/shader/metal041c/`, keeping ambientCG's original file names |

`hint_greys_3x1.png` is written by the script `res://tools/make_hint_greys.gd` (CHANGE-BRIEF line 236); it is not a sourced asset.

---

## 6. What a headless test cannot establish

- **The colours on screen.** Headless mode uses a dummy renderer that draws nothing: the hint experiment's 64/128/192 predictions, the rust's colour and extent, and the look under the lights must be checked by eye in the editor or in captures.
- **Whether the shader compiles on a real GPU.** The test only proves that Godot's shader parser accepted the source (the uniform list is not empty and the log has no `SHADER ERROR`); no D3D12 shader was generated.
- **The texture format on the GPU.** `get_image().get_format()` reads CPU-side data; how the GPU actually samples (sRGB decoding, BC decompression) cannot be seen. Whether `source_color` really makes the GPU decode sRGB can only be shown by the hint experiment's captures.
- **The effect of sampler hints.** The test reads the source text, which proves the hints are written, not that `repeat_enable` / mipmap filtering work on screen.
- **That the normal map is the "right" surface.** A curl near 0 only says there is a surface behind it, not that it is the correct one.
- **Whether it still holds after a reimport.** This run used the existing `.godot/` cache; after clearing the cache and reimporting it must be run again (the assignment's fresh-cache step).
