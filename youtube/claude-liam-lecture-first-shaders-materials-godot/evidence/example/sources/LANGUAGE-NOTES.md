# Godot shading language: instructor example

These explanations and custom shader listings were authored by Codex under Bear's teaching direction. They are an instructor scaffold, not a student's hand-written submission. The authoritative Assignment 5 requires students to write their own shaders and answers. Paths below are relative to `godot/course-series/shaders/`.

## Actual engine-generated code

`standard_generated.gdshader` is the exact shader produced by Godot 4.7.2's Inspector after making the isolated StandardMaterial unique and converting it to ShaderMaterial. The source, saved scratch scene and extraction hash are retained in `evidence/course-assignment-series/shaders/conversion-receipt.json`. It is not loaded by the game. These annotations are separate so the generated code remains unchanged.

| Generated lines | Meaning |
|---|---|
| 3–4 | Spatial pipeline, opaque depth, back-face culling, Burley diffuse and Schlick GGX specular |
| 6, 20 | Albedo color and normal strength from the Inspector |
| 7 | Albedo sampler: color hint, linear/mipmap filtering, repeat |
| 19 | Normal sampler: roughness-normal hint, filtering and repeat; no color hint |
| 27–28 | Vertex processor scales and offsets the incoming UV |
| 34–35 | Sample albedo then multiply it by the material's color |
| 41–43 | Select the red roughness channel and multiply by roughness |
| 46–47 | Write tangent-space normal-map data and its strength |

## Eight language questions

1. `shader_type spatial` selects the 3D processor functions and built-ins. All three custom shaders use this type: `signal.gdshader:1`, `surface.gdshader:1`, `hint.gdshader:1`. The diagnostic hint quads are 3D geometry even though their output is unshaded. No `canvas_item` implementation is claimed here.
2. The custom `fragment()` functions run for fragments being shaded (`signal:7`, `surface:10`, `hint:8`). Godot's generated `vertex()` runs per vertex (`standard_generated:27`). ALBEDO is a fragment output; simply moving `signal:10` into vertex is invalid. A separately calculated varying would interpolate between vertices and would not necessarily preserve fragment-level stripes.
3. The fixture reads UV at `hint:9`, FRAGCOORD and VIEWPORT_SIZE at `hint:10`. These are read-only inputs in the spatial fragment stage. Its optional red screen ruler uses pixel position and viewport width, while UV selects the texture band. The fixture writes ALBEDO at `hint:9,11`; the textured shader writes ROUGHNESS at `surface:12`. UV is instead `inout` in the vertex stage, as the generated assignment at line 28 demonstrates. The screen ruler defaults off during band measurements; its enabled capture is saved separately.
4. `hint_range` shapes the Inspector slider (`signal:3,6`, `surface:6,8,9`); it does not enforce a runtime bound. `source_color` marks color values/samplers (`signal:4–5`, `surface:3,5`, `hint:3`); its decoding behavior is renderer-dependent. Filtering hints select how samples are read (`surface:3–4`). `group_uniforms` organizes the interface (`surface:2,7`), not the sampled values. Generated sampler hints are annotated above; they are engine-selected, not handwritten claims. The actual Compatibility fixture measures all three bands as 64/128/192 with either sampler. The Forward+/Mobile encoding prediction is a different renderer assumption and must not be described as our observation.
5. No. In `signal:3` the displayed range ends at 1. Setting 2 from code reads back 2 and extrapolates the `mix` expression at `signal:10`. The native capture clips negative/overbright output at display limits; it does not become the activation=1 frame. The game driver stays bounded because game charge is bounded, not because of the hint.
6. Generated `standard_generated:7` uses `source_color`; its normal sampler at line 19 does not. Our equivalent color/data distinction is `surface:3–4`. Our custom textured material uses roughness data rather than a normal map. The scratch StandardMaterial and the separate convention calibration do use normal maps.
7. Ordinary fragment invocations have no shared mutable per-fragment state or access to a neighbor's unfinished output. `signal:10` uses uniform inputs set by the CPU-side game, through `signal-garden/garden.gd:253`. A texture is an existing input; reading it is not reading another current fragment's computation.
8. Godot supplies processor entry points and named outputs (`surface:10–13`) and integrates shader uniforms with Inspector hints/groups (`surface:2–9`). Plain GLSL applications must arrange their stages, interfaces and editor controls themselves.

Official references, checked 2026-10-14: [spatial shader built-ins](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html), [shading language and uniform hints](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html).

## Observations and remaining uncertainty

Controlled-pixel predictions were saved before the native capture. At the two named interior pixels, the rendered result differs by up to about five byte values from the simple arithmetic prediction. `controlled-predictions.json` and `material-native-results.json` retain both. The cause has not been isolated; do not silently call this an exact color match. The contrast and perception judgments still require Bear's review. Engine screenshots supply the measured pixels at 3840×2160; a desktop screenshot can add display scaling/color processing and is not the numeric oracle.

A value sweep records min/default/max for the bounded numeric controls. Tint is a color picker with no scalar min/max; black, white and a red sample were used and are labeled as color samples. Under the fixed lighting, roughness spreads the highlight, UV scale increases repetitions, metallic=1 changes diffuse/specular response, and a black tint hides most surface detail. These are image inspections by Codex, not a fabricated human playtest.
