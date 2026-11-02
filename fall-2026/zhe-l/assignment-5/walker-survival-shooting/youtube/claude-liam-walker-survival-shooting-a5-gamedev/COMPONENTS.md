# Components — claude-liam-walker-survival-shooting-a5-gamedev

Game files: `godot/` of the course repository at a84cfa23 (game source last changed in 2d558bba).
43 files inventoried, 15 excluded with reasons, 11 verbatim excerpts, 11 code → result pairs (`gamedev-evidence.json`).

## scene

The saved base scene holds the two crates, the player and the ceiling lights the crates are judged under; project.godot maps Tab to the tablet action.

Beats: B02, B10

Files: `base.tscn`, `project.godot`

## screen-shader

Seven-line unshaded spatial shader: pad_light_data mixes black to cold_white; the colour line matches the specification.

Beats: B03, B04

Files: `assets/props/tablet.glb`, `items/tablet/tablet_device.tscn`, `shaders/pad_base_light.gdshader`

## screen-driver

The body lights the screen only when the tablet has arrived in the hand and darkens it at once when put away; the tablet writes the uniform into its own Local To Scene material.

Beats: B05, B06, B07

Files: `characters/character_intent.gd`, `characters/human/humanoid/humanoid.gd`, `characters/human/humanoid/humanoid.tscn`, `characters/human/player/player.tscn`, `characters/human/player/player_controller.gd`, `items/tablet/tablet_device.gd`, `items/tablet/tablet_device.tscn`

## screen-tests

Headless driver test with real Tab events at 30/60/144 fps, and the F9 capture tool used for the controlled values.

Beats: B04, B08

Files: `debug/screen_glow_capture.gd`, `debug/screen_glow_capture.tscn`, `tests/screen_glow_check.gd`

## crate-shader

Box-projected UVs in vertex(); fragment() compares the height mask with wear_amount; five grouped uniforms.

Beats: B11, B12, B13, B14, B15, B16

Files: `shaders/crate_wear.gdshader`

## crate-materials

Two ShaderMaterials share crate_wear.gdshader and differ in wear_amount and paint_roughness; each crate's .glb import points at its material with Use External.

Beats: B09, B10

Files: `assets/furniture/crate_cube.glb`, `assets/furniture/crate_cube.glb.import`, `assets/furniture/crate_long.glb`, `assets/furniture/crate_long.glb.import`, `assets/furniture/materials/crate_cube_wear.tres`, `assets/furniture/materials/crate_long_wear.tres`

## textures

ambientCG Metal041C (CC0): Color as rust colour with source_color, Displacement as data mask; normal maps only in the Step 4 material and the curl check.

Beats: B11, B22, B26

Files: `assets/shader/metal041c/ATTRIBUTION.md`, `assets/shader/metal041c/Metal041C_1K-PNG_Color.png`, `assets/shader/metal041c/Metal041C_1K-PNG_Color.png.import`, `assets/shader/metal041c/Metal041C_1K-PNG_Displacement.png`, `assets/shader/metal041c/Metal041C_1K-PNG_Displacement.png.import`, `assets/shader/metal041c/Metal041C_1K-PNG_NormalDX.png`, `assets/shader/metal041c/Metal041C_1K-PNG_NormalDX.png.import`, `assets/shader/metal041c/Metal041C_1K-PNG_NormalGL.png`, `assets/shader/metal041c/Metal041C_1K-PNG_NormalGL.png.import`, `assets/shader/metal041c/Metal041C_1K-PNG_Roughness.png`, `assets/shader/metal041c/Metal041C_1K-PNG_Roughness.png.import`, `tests/normal_map_check.gd`

## hint-experiment

One grey PNG sampled with and without source_color on unshaded quads; predicted and measured values match.

Beats: B17, B18

Files: `experiments/hint/hint_experiment.tscn`, `experiments/hint/hint_greys_3x1.png`, `experiments/hint/hint_greys_3x1.png.import`, `experiments/hint/hint_raw.tres`, `experiments/hint/hint_source_color.tres`, `shaders/hint_experiment.gdshader`, `tools/make_hint_greys.gd`

## generated-shader

Shader written by Godot from a StandardMaterial3D, annotated by the user; lines 13 and 42 set colour vs data sampling.

Beats: B19, B21

Files: `shaders/standard_generated.gdshader`

## material-tests

The audit's material test reads hints, values, imports and wiring; the source_color mutation fails it.

Beats: B23, B24, B25

Files: `MATERIALS.md`, `tests/normal_map_check.gd`, `tests/test_materials.gd`

## Excluded files

- `.editorconfig`: Editor formatting defaults from the Godot project template; no runtime effect.
- `.gitattributes`: Git line-ending rules from the project template; no runtime effect.
- `.gitignore`: Git ignore rules; no runtime effect.
- `icon.svg`: Default Godot project icon.
- `icon.svg.import`: Import settings of the default icon.
- `assets/furniture/test_chair.glb`: Assignment 3 test asset, not used by base.tscn.
- `assets/furniture/test_chair.glb.import`: Import settings of the unused test asset.
- `assets/furniture/chair.glb`: Assignment 3 furniture visible in the base; no shader work in this film.
- `assets/furniture/chair.glb.import`: Import settings of Assignment 3 furniture.
- `assets/furniture/computer_desk.glb`: Assignment 3 furniture visible in the base; no shader work in this film.
- `assets/furniture/computer_desk.glb.import`: Import settings of Assignment 3 furniture.
- `assets/furniture/computer_desk_l.glb`: Assignment 3 furniture visible in the base; no shader work in this film.
- `assets/furniture/computer_desk_l.glb.import`: Import settings of Assignment 3 furniture.
- `assets/props/tablet.glb.import`: Import settings of the Assignment 3 tablet model; unchanged in A5.
- `tests/a3_asset_check.gd`: Assignment 3 baseline test; its counts (55 PASS before and after) are in TEST-REPORT, not explained in this film.
