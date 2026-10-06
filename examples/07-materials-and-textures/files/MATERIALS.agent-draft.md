# Dutch Ship Medium — Material & Texture Audit

## 1. Texture slots

The GLTF defines three materials (indices 0–2) and nine images (indices 0–8).
Each material uses three texture slots in glTF 2.0 PBR: normal, baseColor, and
metallicRoughness. No `occlusionTexture` slot is declared for any material.

### Material 0 — `dutch_ship_medium_rigging`

| Slot | Texture file | Channel(s) | Color space | compress/mode | compress/normal_map | mipmaps/generate | detect_3d/compress_to |
|------|-------------|-----------|-------------|:---:|:---:|:---:|:---:|
| Normal (`normalTexture`) | `dutch_ship_medium_rigging_nor_gl_1k.jpg` | RGB → XYZ tangent-space | Linear | 0 | 1 | true | 0 |
| Base Color (`baseColorTexture`) | `dutch_ship_medium_rigging_diff_1k.jpg` | RGB | sRGB | 0 | 0 | true | 0 |
| Metallic/Roughness (`metallicRoughnessTexture`) | `dutch_ship_medium_rigging_arm_1k.jpg` | B = metallic, G = roughness, R = AO (unused — see Findings §1) | Linear | 0 | 0 | true | 0 |

### Material 1 — `dutch_ship_medium_hull`

| Slot | Texture file | Channel(s) | Color space | compress/mode | compress/normal_map | mipmaps/generate | detect_3d/compress_to |
|------|-------------|-----------|-------------|:---:|:---:|:---:|:---:|
| Normal | `dutch_ship_medium_hull_nor_gl_1k.jpg` | RGB → XYZ tangent-space | Linear | 0 | 1 | true | 0 |
| Base Color | `dutch_ship_medium_hull_diff_1k.jpg` | RGB | sRGB | 0 | 0 | true | 0 |
| Metallic/Roughness | `dutch_ship_medium_hull_arm_1k.jpg` | B = metallic, G = roughness, R = AO (unused) | Linear | 0 | 0 | true | 0 |

### Material 2 — `dutch_ship_medium_sails`

| Slot | Texture file | Channel(s) | Color space | compress/mode | compress/normal_map | mipmaps/generate | detect_3d/compress_to |
|------|-------------|-----------|-------------|:---:|:---:|:---:|:---:|
| Normal | `dutch_ship_medium_sails_nor_gl_1k.jpg` | RGB → XYZ tangent-space | Linear | 0 | 1 | true | 0 |
| Base Color + alpha mask | `dutch_ship_medium_sails_diff_1k.jpg` | RGB + alpha channel (JPEG: no alpha — see Findings §2) | sRGB | 0 | 0 | true | 0 |
| Metallic/Roughness | `dutch_ship_medium_sails_arm_1k.jpg` | B = metallic, G = roughness, R = AO (unused) | Linear | 0 | 0 | true | 0 |

**compress/mode** key: `0` = Lossless (decoded to uncompressed RGBA at runtime; not GPU-native).
**compress/normal_map** key: `0` = off, `1` = on (stored in two-channel RG normal format).
**detect_3d/compress_to** key: `0` = Disabled (no automatic upgrade to VRAM-compressed format).

---

## 2. Material flags that change appearance

| Material | Transparency | Alpha Scissor Threshold | Cull Mode | Metallic (scalar) | Roughness (scalar) |
|----------|:-----------:|:---:|:---------:|:-----------------:|:------------------:|
| rigging | DISABLED (opaque) | — | CULL_DISABLED (double-sided) | 1.0 (glTF default) | 1.0 (glTF default) |
| hull | DISABLED (opaque) | — | CULL_DISABLED (double-sided) | 1.0 (glTF default) | 1.0 (glTF default) |
| sails | ALPHA_SCISSOR | 0.5 | CULL_DISABLED (double-sided) | 0.0 (`metallicFactor: 0`) | 1.0 (glTF default) |

All three materials have `doubleSided: true` in the GLTF, which Godot maps to
`BaseMaterial3D.CULL_DISABLED`. The metallic and roughness **scalars** multiply the
corresponding texture channels (B and G of the ARM map). A scalar of 1.0 means the
texture drives the value entirely; the ship hull and rigging are not visually
all-metallic because the ARM texture's blue channel encodes metallic ≈ 0 for wood
and rope and metallic ≈ 1 for iron fittings.

---

## 3. Lights and environment that light the ship

### Lights (3d_scene.tscn)

| Node | Type | Color | Energy | Shadows | Notes |
|------|------|-------|:------:|:-------:|-------|
| `DirectionalLight3D` | Directional | white (default) | 1.0 | enabled; bias 0.05; PSSM-1 (parallel split); max distance 17 m | Main sun |
| `OmniLight3D` | Point/omni | white (default) | 1.0 | enabled; bias 0.04 | Low fill light at (−1.03, 0, 0.71) |
| `SpotLight3D` | Spot | Color(1, 0.816, 0) (gold) | 5.0 | enabled | Lamp fixture above the scene |

No `WorldEnvironment` is in 3d_scene.tscn; it lives in control.tscn.

### Environment (control.tscn `WorldEnvironment` sub-resource)

| Effect | Default state | Notes |
|--------|:------------:|-------|
| Background | Color(0.6, 0.6, 0.6, 1) (grey) | `background_mode = 1` |
| Tonemapper | ACES Fitted (`tonemap_mode = 4`) | Always active |
| Glow / bloom | Disabled | Configured: `intensity=1.0`, `hdr_threshold=0.5`, `hdr_scale=0.2` |
| SDFGI (GI) | Disabled | Configured: `cascades=2`, `min_cell_size=0.1`, `y_scale=0` (75%) |
| Volumetric Fog | Disabled | `density=0.0` |
| Color Adjustments | Enabled | Brightness/Contrast/Saturation all 1.0 (identity) |

### What the settings UI can switch

From **settings.gd**:

- **Video** — Resolution scale (3D), Display filter (Bilinear / FSR 1.0 / FSR 2.2), TAA, MSAA 2–8×, Screen-Space AA (FXAA / SMAA), V-Sync, FPS limit, FOV, Fullscreen mode.
- **Quality** — Shadow resolution (directional + positional, 512–16384), Shadow filtering quality (6 levels), Mesh LOD threshold (4 levels).
- **Effects** — SDFGI (off / low / high), Bloom/Glow (off / low / high bicubic), SSAO (off + 5 quality levels), SSIL (off + 5 quality levels), Screen-Space Reflections (off / low / medium / high), Volumetric Fog (off / low / high filtered).
- **Adjustments** — Brightness (0.5–2.0), Contrast (0.5–2.0), Saturation (0.01–2.0).

In **compatibility mode** (detected at runtime in `settings.gd:27`), the script
additionally halves OmniLight and SpotLight energy (to 0.5) and duplicates
DirectionalLight3D into a sky-only copy + a 0.35-energy light-only copy, compensating
for sRGB blending differences. This is not exposed as a UI toggle.

---

## 4. Findings

### F-1: AO channel discarded — no `occlusionTexture` on any material

**Evidence:** `dutch_ship_medium_1k.gltf` lines 31–79 (`materials` array). Every
material contains `pbrMetallicRoughness.metallicRoughnessTexture` pointing to an
`_arm_` image (AO in R, Roughness in G, Metallic in B per Poly Haven convention), but
none declares an `occlusionTexture` entry. glTF 2.0 §3.9.3 specifies that
`occlusionTexture.index` is the designated slot for the R-channel AO data. Without
it, Godot's GLTF importer does not populate `StandardMaterial3D.ao_texture`, and the
red channel of every `_arm_` texture is permanently ignored. Disk space carrying AO
data is wasted for all three materials.

### F-2: Sails alpha mask is inoperative — JPEG has no alpha channel

**Evidence:** GLTF material 2 (`dutch_ship_medium_sails`, line 62–79) sets
`alphaMode: "MASK"` and `alphaCutoff: 0.5`. The alpha for MASK mode is read from the
**alpha channel of the baseColorTexture**. Image index 7 (`lines 197–202`) resolves
to `textures/dutch_ship_medium_sails_diff_1k.jpg`, a JPEG file. JPEG does not encode
an alpha channel; the decoded alpha is always 1.0. Every texel therefore exceeds the
0.5 threshold, and no geometry is ever discarded. The sail outline cutout — the visual
reason for using MASK mode — does not work. A PNG (or any format with an alpha channel)
carrying the opacity mask is required. The GLTF image name `dutch_ship_medium_sails_diff-dutch_ship_medium_sails_alpha` (line 202) confirms that Blender intended an alpha channel to be present.

### F-3: All nine textures use software (lossless) compression, not GPU-native compression

**Evidence:** All nine `.import` files set `compress/mode=0` (Lossless) and
`detect_3d/compress_to=0` (Disabled). The resulting `.ctex` metadata confirms this
with `"vram_texture": false`. At 1024 × 1024 RGBA, each texture occupies
approximately 4 MB of GPU VRAM without compression. With BC7 (desktop) or ETC2 (mobile)
the same texture would occupy ≈ 0.5–1 MB. Nine textures: ≈ 36 MB actual vs
≈ 4.5–9 MB with VRAM compression. Setting `compress/mode=2` (VRAM Compressed) and
`detect_3d/compress_to=1` on the diff and ARM textures, and relying on the existing
`compress/normal_map=1` for the nor_gl textures, would reduce GPU memory significantly.

### F-4: Sails metallicRoughness image mislabelled in GLTF

**Evidence:** `dutch_ship_medium_1k.gltf` line 207: image index 8 has the `name`
field `dutch_ship_medium_sails_rough`, but the `uri` is
`textures/dutch_ship_medium_sails_arm_1k.jpg`. Every other mesh (rigging image 2,
hull image 5) uses the `_arm_` convention in both the name and uri fields. The
`_arm_` file for sails packs AO+Roughness+Metallic identically to the others. The
name `_rough` implies a single-channel roughness map, which conflicts with the file
name, the other materials' naming pattern, and the file's actual R and B channel content.
This is a Blender GLTF-export artefact but can mislead tooling that reads glTF names.

### F-5: Mesh LOD handler applies "Very Low" threshold only briefly before overwriting it

**Evidence:** `settings.gd` lines 253–264 (`_on_mesh_lod_option_button_item_selected`):

```gdscript
if index == 0: # Very Low
    get_viewport().mesh_lod_threshold = 8.0
if index == 0: # Low          ← duplicate; runs immediately after for index=0
    get_viewport().mesh_lod_threshold = 4.0
if index == 1: # Medium
    get_viewport().mesh_lod_threshold = 2.0
```

Both the "Very Low" and "Low" branches are guarded by `if index == 0`. GDScript
executes sequential `if` statements without short-circuiting, so selecting index 0
first sets 8.0 then immediately overwrites it with 4.0. The effective mapping is:
index 0 → 4.0 (Low), index 1 → 2.0 (Medium), index 2 → 1.0 (High), index 3 → 0.0
(Ultra). The "Very Low" (8.0) threshold is unreachable. The fix is to change the
second `if index == 0` to `if index == 1` and cascade the rest by one.

---

## 5. Attribution

"Dutch Ship Medium" from Poly Haven. Model, textures, and cleanup: James Ray Cock.
Sails model and textures: Rico Cilliers. Original model: Nicolò Zubbini. License:
CC0 1.0. Published 2022-05-25.
