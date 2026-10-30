# textures/cargo_panel — attribution

Rusty Metal Sheet by Amal Kumar, from Poly Haven:
https://polyhaven.com/a/rusty_metal_sheet

License: CC0 1.0 (public domain), https://polyhaven.com/license. No attribution is
required; this file records the source anyway.

Downloaded 2026-10-30 by Claude Code at the student's request, 1K PNG, from
`https://dl.polyhaven.org/file/ph-assets/Textures/png/1k/rusty_metal_sheet/`.
The MD5 of each file matches the value listed by `https://api.polyhaven.com/files/rusty_metal_sheet`.
The files are unchanged from the download.

| File | Bytes | MD5 (matches Poly Haven) | SHA-256 | Source format |
|---|---|---|---|---|
| `rusty_metal_sheet_diff_1k.png` | 5478174 | `635070f22af170e308e225db14c7cd72` | `b8e47f1d84acbe20119a351217d7a9d1139a21ea99a9fe0dd653880c9ee897ba` | 1024×1024, 16-bit RGB |
| `rusty_metal_sheet_rough_1k.png` | 1847486 | `69cf15ca063fd041b7fc33870d2e7e73` | `86ad66e35ae81052886aacbb01a7c3eeb2fadcb906cc3e83805faf77b4182440` | 1024×1024, 16-bit grey |
| `rusty_metal_sheet_nor_gl_1k.png` | 5329963 | `6dda133d0fb9b7801a35c470c8f6191c` | `ad8284e25754f109a46ab418f08a26f7ab8030f9c6cdf60d5b939f441a30b789` | 1024×1024, 16-bit RGBA |
| `rusty_metal_sheet_nor_dx_1k.png` | 5330601 | `5c80ea49bc4ce73b9af99092a84556d4` | `cb4dad32c55b3f5d5893d6cc59537130179f72fc66afb255a9157649daaaeefe` | 1024×1024, 16-bit RGBA |

Import settings (set in each `.import`, reimported, then read back; defaults kept in
`evidence/a5/texture-import/default-import/`):

| File | compress/mode | compress/normal_map | mipmaps/generate | normal_map_invert_y | detect_3d/compress_to | Loads as |
|---|---|---|---|---|---|---|
| diff | 0 (Lossless) | 2 (Disable) | true | false | 0 (Disabled) | RGB8, mipmaps |
| rough | 0 (Lossless) | 2 (Disable) | true | false | 0 (Disabled) | L8, mipmaps |
| nor_gl | 2 (VRAM Compressed) | 1 (Enable) | true | false | 0 (Disabled) | RGTC_RG (BC5), mipmaps |
| nor_dx | 2 (VRAM Compressed) | 1 (Enable) | true | false | 0 (Disabled) | RGTC_RG (BC5), mipmaps |

`detect_3d/compress_to` is off so that first use in 3D does not rewrite these settings.
"Loads as" is from `tests/a5_probe_cargo_textures.gd` (`logs/a5_probe_cargo_textures_60fps.log`).
The 16-bit sources load as 8 bits per channel. The normal maps keep only R and G, and
`NORMAL_MAP` rebuilds Z.
`nor_dx` is only for the curl check; the cargo_panel materials bind `nor_gl`.
