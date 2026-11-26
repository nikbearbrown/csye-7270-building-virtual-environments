# Texture attribution — Metal041C

| Field | Value |
|---|---|
| Asset | Metal 041 C (`Metal041C`), PBR material, 1K-PNG download |
| Source URL | https://ambientcg.com/view?id=Metal041C (download: https://ambientcg.com/get?file=Metal041C_1K-PNG.zip) |
| Author / role | ambientCG, created and run by Lennart Demes (Münster, Germany; imprint: https://docs.ambientcg.com/legal/). The asset page lists the technique as Procedural |
| Licence | Creative Commons CC0 1.0 Universal (https://docs.ambientcg.com/license/). No credit required; recorded here because the course requires provenance |
| Date checked | 2026-11-01 |
| Downloaded by | Me, from the link above, on 2026-11-01 |
| Changes | None to the image files. Kept 5 of the 11 files in the zip; the `.blend`, `.tres`, `.usdc`, `.mtlx`, Metalness map and preview image were left out of the project |
| Normal-map convention | The game and the Step 4 material use `Metal041C_1K-PNG_NormalGL.png` (OpenGL, the convention Godot expects). `Metal041C_1K-PNG_NormalDX.png` is kept only to calibrate `tests/normal_map_check.gd` |

| File | Used for |
|---|---|
| `Metal041C_1K-PNG_Color.png` | `rust_albedo` in `shaders/crate_wear.gdshader` (colour, `source_color`); albedo of the Step 4 material |
| `Metal041C_1K-PNG_Displacement.png` | `wear_mask` in `shaders/crate_wear.gdshader` (data, no `source_color`) |
| `Metal041C_1K-PNG_Roughness.png` | Roughness of the Step 4 material |
| `Metal041C_1K-PNG_NormalGL.png` | Normal map of the Step 4 material; normal-map check |
| `Metal041C_1K-PNG_NormalDX.png` | Normal-map check calibration only |
