# Components — claude-liam-walker-survival-shooting-a6-gamedev

Game files: `godot/` of the course repository at 1828bb6b.
27 files inventoried, 51 excluded with reasons, 9 verbatim excerpts, 9 code → result pairs (`gamedev-evidence.json`).

## scene

The saved base scene holds the player, the three ceiling lights, the wall switch and one instance of each effect; project.godot maps Space, WASD and F.

Beats: B02, B08, B16

Files: `base.tscn`, `characters/human/player/screen_tablet.gd`, `project.godot`

## effect-a

Landing dust: Dust (24 one-shot billboard puffs, ring spawn, damping, scale curve, opacity ramp, 0.32 m quads) and GroundRing (one flat ring quad that grows and fades).

Beats: B03, B04, B05, B06

Files: `effects/landing_dust.tscn`

## effect-a-trigger

humanoid.gd emits landed once per landing (not on load); the trigger moves to the feet and restart()s both emitters, so a second landing clears the first burst.

Beats: B07, B08, B09, B10

Files: `base.tscn`, `characters/character_intent.gd`, `characters/human/humanoid/humanoid.gd`, `characters/human/humanoid/humanoid.tscn`, `characters/human/player/player.tscn`, `characters/human/player/player_controller.gd`, `effects/landing_dust_trigger.gd`

## effect-b

Light dust: 1300 specks in a 14 x 2.6 x 9 m box via emission_shape_offset, turbulence, a multi-peak opacity ramp, additive lit quads 0.003-0.03 m, 6 s preprocess.

Beats: B11, B12, B13, B14

Files: `effects/light_dust.tscn`

## effect-b-condition

The listener follows CeilingLights.lights_changed (queried once at start): on = show and one restart(); off = hidden, no births; hide/show handled via visibility_changed.

Beats: B15, B16

Files: `base.tscn`, `effects/light_dust_listener.gd`, `world/light_switch/light_switch.gd`, `world/light_switch/light_switch.tscn`, `world/lights/ceiling_lights.gd`

## strips

Preview scenes replay each effect on a fixed timeline for the Movie Maker fixture strips.

Beats: B05, B06, B10, B13, B14, B18, B20

Files: `previews/landing_dust_preview.gd`, `previews/landing_dust_preview.tscn`, `previews/light_dust_preview.gd`, `previews/light_dust_preview.tscn`

## process-shader

Godot's generated particles shader for Effect B: lines 261/263 emission box and offset; line 253 colour ramp; lines 397/410 gravity.

Beats: B17, B18, B19, B20

Files: `shaders/particles_generated.gdshader`

## tests

Read-back tests check ClassDB names then every brief value; state tests drive real keys and check landing count, retrigger, lights on/off, pause and hide.

Beats: B21, B22, B23

Files: `tests/test_landing_dust_config.gd`, `tests/test_landing_dust_events.gd`, `tests/test_light_dust_config.gd`, `tests/test_light_dust_state.gd`

## price

Headless cost script with controls; windowed GPU-time helper and vsync key for the GPU price.

Beats: B24, B25, B26

Files: `debug/gpu_price.gd`, `debug/vsync_toggle.gd`, `tests/cost_effects.gd`

## Excluded files

- `.editorconfig`: Editor formatting defaults from the Godot project template; no runtime effect.
- `.gitattributes`: Git line-ending rules from the project template; no runtime effect.
- `.gitignore`: Git ignore rules; no runtime effect.
- `icon.svg`: Default Godot project icon.
- `icon.svg.import`: Import settings of the default icon.
- `MATERIALS.md`: Assignment 5 material audit; not part of the particle work.
- `tests/a3_asset_check.gd`: Assignment 3 baseline test; counts in TEST-REPORT, not explained here.
- `tests/screen_glow_check.gd`: Assignment 5 baseline test; counts in TEST-REPORT, not explained here.
- `tests/normal_map_check.gd`: Assignment 5 baseline test; counts in TEST-REPORT, not explained here.
- `tests/test_materials.gd`: Assignment 5 baseline test (168 passed, 1 known failure); not explained here.
- `debug/screen_glow_capture.gd`: Assignment 5 capture tool.
- `debug/screen_glow_capture.tscn`: Assignment 5 capture scene.
- `items/tablet/tablet_device.gd`: Assignment 5 tablet script; not part of the particle work.
- `items/tablet/tablet_device.tscn`: Assignment 5 tablet prefab; not part of the particle work.
- `tools/make_hint_greys.gd`: Assignment 5 hint-experiment tool.
- `shaders/crate_wear.gdshader`: Assignment 5 crate shader; visible in the base, not explained here.
- `shaders/hint_experiment.gdshader`: Assignment 5 hint experiment shader.
- `shaders/pad_base_light.gdshader`: Assignment 5 tablet screen shader.
- `shaders/standard_generated.gdshader`: Assignment 5 generated StandardMaterial3D shader.
- `assets/props/tablet.glb`: Assignment 3 tablet model; not part of the particle work.
- `assets/props/tablet.glb.import`: Import settings of the tablet model.
- `assets/shader/metal041c/ATTRIBUTION.md`: Assignment 5 texture credits (crates); the particles use no outside texture.
- `experiments/hint/hint_experiment.tscn`: Assignment 5 hint experiment; not part of the particle work.
- `experiments/hint/hint_greys_3x1.png`: Assignment 5 hint experiment; not part of the particle work.
- `experiments/hint/hint_greys_3x1.png.import`: Assignment 5 hint experiment; not part of the particle work.
- `experiments/hint/hint_raw.tres`: Assignment 5 hint experiment; not part of the particle work.
- `experiments/hint/hint_source_color.tres`: Assignment 5 hint experiment; not part of the particle work.
- `assets/furniture/chair.glb`: Assignment 3 furniture model; background in the captures only.
- `assets/furniture/chair.glb.import`: Import settings of Assignment 3 furniture.
- `assets/furniture/computer_desk.glb`: Assignment 3 furniture model; background in the captures only.
- `assets/furniture/computer_desk.glb.import`: Import settings of Assignment 3 furniture.
- `assets/furniture/computer_desk_l.glb`: Assignment 3 furniture model; background in the captures only.
- `assets/furniture/computer_desk_l.glb.import`: Import settings of Assignment 3 furniture.
- `assets/furniture/crate_cube.glb`: Assignment 3 furniture model; background in the captures only.
- `assets/furniture/crate_cube.glb.import`: Import settings of Assignment 3 furniture.
- `assets/furniture/crate_long.glb`: Assignment 3 furniture model; background in the captures only.
- `assets/furniture/crate_long.glb.import`: Import settings of Assignment 3 furniture.
- `assets/furniture/test_chair.glb`: Assignment 3 furniture model; background in the captures only.
- `assets/furniture/test_chair.glb.import`: Import settings of Assignment 3 furniture.
- `assets/furniture/materials/crate_cube_wear.tres`: Assignment 5 crate material; background only.
- `assets/furniture/materials/crate_long_wear.tres`: Assignment 5 crate material; background only.
- `assets/shader/metal041c/Metal041C_1K-PNG_Color.png`: Assignment 5 crate texture (ambientCG, CC0); not used by the particles.
- `assets/shader/metal041c/Metal041C_1K-PNG_Color.png.import`: Import settings of an Assignment 5 crate texture.
- `assets/shader/metal041c/Metal041C_1K-PNG_Displacement.png`: Assignment 5 crate texture (ambientCG, CC0); not used by the particles.
- `assets/shader/metal041c/Metal041C_1K-PNG_Displacement.png.import`: Import settings of an Assignment 5 crate texture.
- `assets/shader/metal041c/Metal041C_1K-PNG_Roughness.png`: Assignment 5 crate texture (ambientCG, CC0); not used by the particles.
- `assets/shader/metal041c/Metal041C_1K-PNG_Roughness.png.import`: Import settings of an Assignment 5 crate texture.
- `assets/shader/metal041c/Metal041C_1K-PNG_NormalGL.png`: Assignment 5 crate texture (ambientCG, CC0); not used by the particles.
- `assets/shader/metal041c/Metal041C_1K-PNG_NormalGL.png.import`: Import settings of an Assignment 5 crate texture.
- `assets/shader/metal041c/Metal041C_1K-PNG_NormalDX.png`: Assignment 5 crate texture (ambientCG, CC0); not used by the particles.
- `assets/shader/metal041c/Metal041C_1K-PNG_NormalDX.png.import`: Import settings of an Assignment 5 crate texture.
