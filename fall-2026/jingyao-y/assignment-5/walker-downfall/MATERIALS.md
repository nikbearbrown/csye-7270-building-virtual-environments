# MATERIALS.md — A5 material audit (2026-10-30)

Read-only audit of the textured shader, its two materials, the hint-experiment
shader and its two materials, every texture they bind, and the lights and
Environment of the scenes they appear in. Nothing listed here was changed.
Every table is asserted by `tests/test_materials.gd`
(`./scripts/run-test.sh test_materials.gd 60`, log `logs/test_materials_60fps.log`:
120 PASS, 0 FAIL, exit 0).

## Materials

| Material | Shader | Uniform values it sets | Textures it binds |
|---|---|---|---|
| `res://materials/cargo_panel_mild.tres` (A) | `res://shaders/cargo_panel.gdshader` | `uv_scale` 1.0, `tint_color` Color(1, 1, 1, 1), `roughness_scale` 0.65, `normal_strength` 0.35; `render_priority` 0 | `albedo_tex` = `rusty_metal_sheet_diff_1k.png`, `roughness_tex` = `rusty_metal_sheet_rough_1k.png`, `normal_tex` = `rusty_metal_sheet_nor_gl_1k.png` |
| `res://materials/cargo_panel_weathered.tres` (B) | `res://shaders/cargo_panel.gdshader` | `uv_scale` 1.0, `tint_color` Color(0.8, 0.7, 0.6, 1), `roughness_scale` 1.35, `normal_strength` 1.2; `render_priority` 0 | same three textures as A |
| `res://tests/hint_experiment.tscn::Material_with_hint` (on `QuadWithSourceColor`) | `res://shaders/hint_experiment.gdshader` | `use_source_color` true | `tex_color` = `greys_3x1.png`, `tex_raw` = `greys_3x1.png` |
| `res://tests/hint_experiment.tscn::Material_without_hint` (on `QuadWithoutSourceColor`) | `res://shaders/hint_experiment.gdshader` | `use_source_color` false | `tex_color` = `greys_3x1.png`, `tex_raw` = `greys_3x1.png` |

Texture paths above are under `res://textures/cargo_panel/` and
`res://textures/hint_experiment/`. Evidence: `materials/cargo_panel_mild.tres:3-17`,
`materials/cargo_panel_weathered.tres:3-17`, `tests/hint_experiment.tscn:22-32`.
A and B are separate ShaderMaterial resources that share one Shader resource
(test: "mild and weathered share one Shader resource").

Other users of the textured shader (not among the two materials): three embedded
ShaderMaterials in `tests/normal_map_check.tscn:31-59` (`Material_GL`,
`Material_DX_raw`, `Material_DX_fixed`), all with `uv_scale` 1.0, `tint_color`
white, `roughness_scale` 1.0, `normal_strength` 1.0, the same diffuse and roughness
maps, and `normal_tex` = `nor_gl`, `nor_dx`, `nor_dx_1k_inverty` respectively.

Where A and B appear: `tests/material_review.tscn:46-54` (`PanelA_Mild`,
`PanelB_Weathered`, `material_override`), and in play on the base hall's two
`crate_stack` props, surface 0 only: layout x 98 gets A, x 101.5 gets B
(`world/base_map.gd:64-65`, `world/base_map.gd:231`, `world/base_map.gd:1017-1018`).

## Samplers

Import settings are read from each texture's `.import` `[params]` with ConfigFile.

| Shader | Sampler | Hints as written | Bound texture (per material) | compress/mode | compress/normal_map | mipmaps/generate | Other import settings that matter |
|---|---|---|---|---|---|---|---|
| cargo_panel | `albedo_tex` | `source_color, filter_linear_mipmap, repeat_enable` (`shaders/cargo_panel.gdshader:3`) | A, B: `rusty_metal_sheet_diff_1k.png` | 0 (Lossless) | 2 (Disabled) | true | invert_y false, detect_3d/compress_to 0 |
| cargo_panel | `roughness_tex` | `filter_linear_mipmap, repeat_enable` (`:4`) | A, B: `rusty_metal_sheet_rough_1k.png` | 0 (Lossless) | 2 (Disabled) | true | invert_y false, compress_to 0 |
| cargo_panel | `normal_tex` | `hint_normal, filter_linear_mipmap, repeat_enable` (`:5`) | A, B: `rusty_metal_sheet_nor_gl_1k.png` | 2 (VRAM Compressed) | 1 (Enable) | true | invert_y false, compress_to 0; loads as `get_format()` 21 = `FORMAT_RGTC_RG` (BC5) |
| cargo_panel | `normal_tex` (fixture only) | as above | normal_map_check: `nor_dx_1k.png` / `nor_dx_1k_inverty.png` | 2 / 2 | 1 / 1 | true / true | invert_y false / **true** |
| hint_experiment | `tex_color` | `source_color, filter_nearest, repeat_disable` (`shaders/hint_experiment.gdshader:4`) | both: `greys_3x1.png` | 0 (Lossless) | 2 (Disabled) | false | fix_alpha_border false, compress_to 0 |
| hint_experiment | `tex_raw` | `filter_nearest, repeat_disable` (`:5`) | both: `greys_3x1.png` | 0 (Lossless) | 2 (Disabled) | false | as above |

Non-sampler uniforms, from the source text (defaults are not reported headlessly,
`CLAUDE.md` "Headless facts"):

| Shader | Uniform | Declared | Group |
|---|---|---|---|
| cargo_panel | `uv_scale` | `float : hint_range(0.25, 8.0, 0.25) = 1.0` (`:8`) | Surface |
| cargo_panel | `tint_color` | `vec4 : source_color = vec4(1.0, 1.0, 1.0, 1.0)` (`:9`) | Surface |
| cargo_panel | `roughness_scale` | `float : hint_range(0.0, 2.0, 0.05) = 1.0` (`:12`) | Response |
| cargo_panel | `normal_strength` | `float : hint_range(0.0, 2.0, 0.05) = 1.0` (`:13`) | Response |
| hint_experiment | `use_source_color` | `bool = true` (`:6`) | — |

`get_shader_uniform_list()` order, asserted: cargo_panel = albedo_tex, roughness_tex,
normal_tex, [group Surface], uv_scale, tint_color, [group Response], roughness_scale,
normal_strength; hint_experiment = tex_color, tex_raw, use_source_color.

Source texels (decoded with `Image.load_from_file`): `greys_3x1.png` = 64, 128, 192.
`rusty_metal_sheet_rough_1k.png`: mean R 0.820 (stride-4 sample).

## Lights and environment that change the look

| Scene | Tonemap / exposure | Background | Ambient / reflected | Post-processing | Lights |
|---|---|---|---|---|---|
| `tests/material_review.tscn` (A/B judging) | Linear (0) / 1.0 | colour 0.18 grey | Color(1,1,1) × 0.2 / reflected **disabled** (`reflected_light_source = 1`) | SSR, SSAO, SSIL, SDFGI, glow, fog, volumetric fog, adjustment all off (`:6-22`) | `Sun`: white, energy 1.0, rotation_degrees (-35, -30, 0), direction (0.41, -0.57, -0.71), on. `RakingLight`: white, energy 1.0, rotation_degrees (-75, 0, 0), direction (0, -0.966, -0.259), **off** by default (`:35-44`) |
| `tests/normal_map_check.tscn` | same as above (`:10-26`) | same | same | same | same two lights (`:66-75`) |
| `tests/hint_experiment.tscn` | Linear (0) / 1.0 | black | ambient disabled / reflected disabled | all off (`:6-20`) | none; shader is `render_mode unshaded` |
| Base hall, in play (A/B on crate stacks) | **ACES (3)** / 1.0, white 8.0 | Color(0.02, 0.025, 0.03) | Color(0.62, 0.66, 0.72) × 0.8 | SSAO (r 1.4, i 2.2), SSIL 0.8, glow 0.55 soft-light, fog 0.004, adjustment contrast 1.06 / saturation 1.08 (`game/game_manager.gd:6536-6562`) | sun DirectionalLight3D rotation_degrees (-50, -30, 0), energy `BASE_SUN` 0.15, white, shadows on (`game/game_manager.gd:6494-6497`, `:6528`, `:6621-6623`); hall ceiling OmniLights from `LAMP` Color(0.32, 0.3, 0.24) → light colour (1, 0.94, 0.75), energy 1.92, range 18.7, specular 0.25, nearest 6 cast shadows (`world/base_map.gd:487`, `:589`, `:602-611`); outline pass visible |

Enum values in this file were looked up, not assumed: the Environment and Image
constants from the engine (`tests/a5_review_lookup.gd`, `logs/a5_review_lookup_60fps.log`:
tonemap 0 Linear / 3 ACES / 4 AgX; background 1 Color; ambient 1 Disabled / 2 Color;
reflected 1 Disabled), and the import options from the Godot 4.7.2 source,
`editor/import/resource_importer_texture.cpp:232,241,260`: `compress/mode`
"Lossless,Lossy,VRAM Compressed,VRAM Uncompressed,Basis Universal",
`compress/normal_map` "Detect,Enable,Disabled", `detect_3d/compress_to`
"Disabled,VRAM Compressed,Basis Universal" (values count from 0).

## Findings

1. **B's roughness is almost all clamped to 1.0.** The rough map's mean R is 0.820;
   with `roughness_scale` 1.35, 91.7 % of sampled texels exceed 1 and are clamped
   (`shaders/cargo_panel.gdshader:19`, `materials/cargo_panel_weathered.tres:16`;
   test line `INFO rough source mean R 0.820; texels clamped at 1.0 under roughness_scale 1.35: 91.7%`).
   B therefore shows almost no roughness variation from the texture; the brief's
   "增大后高光变宽、变弱" (`CHANGE-BRIEF.md`, uniform table) saturates well before 1.35.
   A (0.65) keeps the map's variation (mean 0.820 × 0.65 = 0.533, computed, not measured;
   no texel reaches 1.0 because 0.65 × 1.0 < 1).
2. **Environment reflections are off in both fixtures.** `reflected_light_source = 1`
   (`tests/material_review.tscn:12`, `tests/normal_map_check.tscn:16`). Roughness can
   only show through the Sun's (or RakingLight's) direct specular highlight. The brief
   names ambient Color(1,1,1) × 0.2 but does not mention reflected light, so this is a
   choice not recorded there.
3. **`tint_color` is a `source_color` uniform**, so B's Color(0.8, 0.7, 0.6) is decoded
   to linear before the multiply (by the sRGB formula used in the brief, about
   (0.604, 0.448, 0.319)) (`shaders/cargo_panel.gdshader:9`, `:18`). B is darker than the
   literal numbers suggest. Headless cannot confirm what the GPU receives
   (`get_shader_uniform_list()` reports `tint_color` hint 0, the same as a plain vec4).
4. **The "fixed DX" map is a byte-identical second copy.** `rusty_metal_sheet_nor_dx_1k_inverty.png`
   has the same SHA-256 as `nor_dx_1k.png` (`cb4dad32c55b…`; test line
   `PASS nor_dx_1k_inverty.png is byte-identical…`); only its `.import` differs
   (`process/normal_map_invert_y=true`, `.import:37`). That is 5.3 MB more in the repo.
   The brief planned to flip invert_y "仅在单独'修正 DX'分支" and reimport
   (`CHANGE-BRIEF.md:249-250`), not to keep a permanent copy. The brief also speaks of a
   separate "DX sampler" (`CHANGE-BRIEF.md:263`); there is none. The fixture binds the
   DX maps to `normal_tex` in separate materials instead.
5. **curl_ratio separates the conventions, but not near the ideal 0 / 2.** Source GL:
   directx=false 0.5419, directx=true 1.4581; source DX: 1.4584 / 0.5416; the
   imported inverty copy: 0.6088 / 1.3912 (test `CURL_RATIO` lines). The
   `normal_map_check.gd:8-10` legend reads ~0 as a real surface in that convention and
   ~2 as the other convention; 0.54 / 1.46 is in between. A likely reason is the very
   flat map (mean tilt 1.00°, none over 10°, `CHANGE-BRIEF.md` Revisions), where 8-bit
   quantisation is a large share of the slope. The source file of the inverty copy
   gives the raw DX numbers; only the import flips it.
6. **`normal_strength` hardly differs visibly between A and B.** 0.35 against 1.2 on a
   map whose tilt averages 1.00° (`CHANGE-BRIEF.md` Revisions, "法线偏平"). A and B
   differ visibly mainly through `tint_color` and `roughness_scale`, and per finding 1
   B's roughness is mostly the constant 1.0.
7. **Diffuse and roughness maps are uncompressed in VRAM** (`compress/mode=0`, `.import:18`
   for both). This follows the brief's plan (`CHANGE-BRIEF.md:241-242`). Measured image
   data with mipmaps (`get_image().get_data().size()`, `logs/a5_review_lookup_60fps.log`):
   diffuse 4,194,303 bytes (RGB8), roughness 1,398,101 bytes (L8), each normal map
   1,398,128 bytes (RGTC_RG). The 16-bit sources (5.5 MB and 1.8 MB) load as 8 bits per
   channel (`get_format()` 4 = `FORMAT_RGB8`, 0 = `FORMAT_L8`, same log), so the extra
   source precision is not used.
8. **Each hint material binds a texture it never reads.** Both bind `greys_3x1.png` to
   `tex_color` and `tex_raw` (`tests/hint_experiment.tscn:24-25`, `:30-31`), but the
   shader reads only one of them, chosen by `use_source_color`
   (`shaders/hint_experiment.gdshader:9`). It does no harm. Note that the two quads
   differ by the bool as well as by which sampler (with or without the hint) is read.
   The brief's "仅颜色提示不同" (`CHANGE-BRIEF.md:204-206`) holds for the samplers.
9. **In play, A/B are seen under ACES, SSAO, SSIL, glow, fog and adjustment** (base
   environment table above), not under the fixture's Linear look. The brief expects
   this (`CHANGE-BRIEF.md`, Material plan, "In play"). The crate boxes are also not
   dimmed by `room_light()` (brief Revisions).
10. **`material_review.tscn` uses BoxMesh UVs.** The front face shows a 1/3 × 1/2 tile of
    the texture (brief Revisions), so the review panels show the texture magnified.
11. **CLAUDE.md is out of date about these files.** `CLAUDE.md:44` says "`res://tests/material_review.tscn`
    is planned, not yet made", `CLAUDE.md:111` says "`shaders/` does not exist yet", and
    `CLAUDE.md:36-44` still names the `crate` prop as the textured-shader object. The brief's
    Revisions moved that to the hall `crate_stack`s.
12. **`textures/cargo_panel/ATTRIBUTION.md:3-6` adds facts the brief does not contain**:
    an author name and a licence URL. They are left out of the attribution below, which
    uses only the brief. The SHA-256 and MD5 values it lists match the files on disk
    (`sha256sum` / `md5sum` run during this audit).
13. **Nothing in the shaders looks wrong.** The hints match the brief's plan: the colour
    sampler has `source_color`, the data samplers do not, and the normal map has
    `hint_normal`. `NORMAL_MAP = texture(normal_tex, uv).rgb` passes a BC5 (RG-only)
    texture; the brief relies on NORMAL_MAP rebuilding Z (`CHANGE-BRIEF.md:251`). That
    needs a rendered check and was not changed.

## Attribution

From `CHANGE-BRIEF.md` (Material plan), as checked by the student:

- Source: [Poly Haven — Rusty Metal Sheet](https://polyhaven.com/a/rusty_metal_sheet).
- Licence: CC0.
- Resolution: 1K, PNG version.
- Maps used, by Poly Haven map name: Diffuse (`rusty_metal_sheet_diff_1k`),
  Rough (`rusty_metal_sheet_rough_1k`), Normal (OpenGL) (`rusty_metal_sheet_nor_gl_1k`),
  Normal (DirectX) (`rusty_metal_sheet_nor_dx_1k`, curl calibration only).
- `greys_3x1.png` is not from Poly Haven. It was generated by `tests/a5_make_greys_png.gd`.
