# Texture credits — assets/textures/rock_01/

| Field | Value |
|---|---|
| Asset | Rock 01 |
| Source | https://polyhaven.com/a/rock_01 (files from `dl.polyhaven.org`, 1K PNG) |
| Author and role | Rob Tuytel, texture author |
| Licence | CC0 (Poly Haven requires no credit; the course requires provenance) |
| Date downloaded and checked | 2026-10-22 |
| Modified | No; the committed PNGs are the downloaded files |
| Normal-map convention used | OpenGL (`_nor_gl`), the one Godot expects. `_nor_dx` is kept only to calibrate `tests/normal_map_check.gd` and is bound to no material |

| File | Use | SHA-256 |
|---|---|---|
| `rock_01_diff_1k.png` | albedo (colour, `source_color`) | `60404f5c3e505db17fc6501b3d0045e7aa6516e0baf08e81487f9a008a9c1dac` |
| `rock_01_nor_gl_1k.png` | normal map (data, `hint_normal`) | `28ed28b8109590352fce645896390fdff75aeb827ec41841fab94400e59238e5` |
| `rock_01_nor_dx_1k.png` | calibration only | `3f553c334f4c71479c11cac05086759dbb8250f5b1247ccbf403a188e31e6329` |
| `rock_01_rough_1k.png` | roughness and frost mask (data) | `6a99d084b3137ead2f6b76872d71148a8a912de9b7cf4f0509d7dc2515f9f938` |

Curl check (`logs/calibrate_normal_check_60fps.log`): `nor_gl` 0.1444 under OpenGL, 1.8556 under DirectX; `nor_dx` the reverse.

The hint-experiment texture `assets/textures/hint/greys_3x1.png` is written by code (`tools/write_hint_png.gd`) and needs no credit.
