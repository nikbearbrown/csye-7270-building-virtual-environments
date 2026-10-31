# LANGUAGE-NOTES — A5

2026-10-30

These are my notes on how the shaders work and what I found in the code and experiment results. The line numbers refer to the current files, so I will need to check them again if the code changes. The Use It measurements are now recorded in evidence/a5/use-it/measurement.json.

## A. Lines in the generated StandardMaterial3D shader

For this step, I used Godot 4.7.2 with Forward+ and D3D12. I assigned the albedo, roughness, and GL normal textures to a StandardMaterial3D on a BoxMesh, enabled Normal Map, converted it to a ShaderMaterial, and saved the generated Shader as `shaders/standard_generated.gdshader`. I did not save the temporary scene or change the three existing shaders.

The file has 48 lines. Its SHA-256 is:

`ca1c191c44fb614ae64a258fce3efbc13b77fdc82f480e98ac4582e30805650d`

| What I looked for | Location in the generated file |
|---|---|
| shader_type | `shaders/standard_generated.gdshader:3`: `shader_type spatial;` |
| render_mode | `shaders/standard_generated.gdshader:4`: `blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx`; normal scene lighting is used. |
| Albedo color in the Inspector | `shaders/standard_generated.gdshader:6`: `uniform vec4 albedo : source_color;` |
| Normal strength in the Inspector | `shaders/standard_generated.gdshader:20`: `uniform float normal_scale : hint_range(-16.0, 16.0);` |
| Albedo sampler and hints | `shaders/standard_generated.gdshader:7`: `texture_albedo : source_color, filter_linear_mipmap, repeat_enable` |
| Normal sampler and hints | `shaders/standard_generated.gdshader:19`: `texture_normal : hint_roughness_normal, filter_linear_mipmap, repeat_enable`; no source_color. |
| Roughness sampler and hints | `shaders/standard_generated.gdshader:14`: `texture_roughness : hint_roughness_r, filter_linear_mipmap, repeat_enable`; no source_color. |
| ALBEDO | `shaders/standard_generated.gdshader:35`: `ALBEDO = albedo.rgb * albedo_tex.rgb;` |
| ROUGHNESS | `shaders/standard_generated.gdshader:43`: `ROUGHNESS = roughness_tex * roughness;` |
| NORMAL_MAP | `shaders/standard_generated.gdshader:46`: `NORMAL_MAP = texture(texture_normal, base_uv).rgb;` |
| NORMAL_MAP_DEPTH | `shaders/standard_generated.gdshader:47`: `NORMAL_MAP_DEPTH = normal_scale;` |

One difference I noticed is that the generated version also has vertex() on lines 27–29 to handle UV1 scale and offset. The other three shaders only define fragment().

The generated declarations for uniforms such as albedo and normal_scale do not include default values. The values used during conversion are stored in the ShaderMaterial: albedo_color was white and normal_scale was 1.0. Saving only the Shader does not also save the material's texture bindings and parameter values. I kept this file for comparison and did not connect it to the game.

I checked that the file parses and ran a separate BoxMesh render with Forward+ / D3D12. There were no SHADER ERROR or SCRIPT ERROR messages. No game scenes or materials reference the generated shader. The SHA-256 hashes of the three texture `.import` files and the three existing shaders also stayed the same.

The editor still reported scan interruption, settings-file write errors, and resource cleanup errors on exit. This check passed for the generated shader, but it does not mean the whole project ran without errors.

## B. Eight questions

### 1. What does shader_type decide?

My understanding is that shader_type tells Godot which kind of rendering the shader is for. It also determines which processor functions, built-in variables, and render modes I can use.

All three files start with `shader_type spatial;` on line 1 because they work with surfaces in a 3D scene. This gives fragment() access to outputs such as ALBEDO and ROUGHNESS. Here, spatial is the shader type; Forward+ and D3D12 are the project's renderer and rendering driver.

Code: `shaders/burning_bottle_fire.gdshader:1`, `shaders/cargo_panel.gdshader:1`,
`shaders/hint_experiment.gdshader:1`.
Reference: [Godot Introduction to shaders — Shader types](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html#shader-types).

### 2. Which processor functions did I write, when do they run, and what would happen if I moved the color line into vertex()?

All three shaders only define fragment(): line 10 in the flame shader, line 16 in cargo, and line 8 in hint. It runs on fragments after rasterization, using UV values interpolated between vertices. It does not run just once per object, and its execution count cannot be calculated directly from the CPU frame count. vertex() processes mesh vertices. Godot handles the stages I have not customized.

The flame shader assigns ALBEDO on line 17. ALBEDO is a fragment-stage output, so I cannot move that whole statement directly into vertex(). To calculate a color earlier, I would need to store it in a custom variable in vertex() and pass it to fragment() through a varying.

I also need to separate the color calculation from the shape calculation. The mix expression only depends on uniforms, so it gives the same color across one object. Moving just that calculation earlier would not create a color gradient. The flame shape depends on UV, though. Calculating it only at a few vertices and interpolating between them would give a different outline from calculating it per fragment.

Code: `shaders/burning_bottle_fire.gdshader:10`, `:11`, `:14`, `:17`;
`shaders/cargo_panel.gdshader:16`; `shaders/hint_experiment.gdshader:8`.
Reference: [Godot Introduction to shaders — Processor functions](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html#shaders-in-godot).

### 3. Which three built-ins are read, which two are written, and which are read-only?

When I counted them in the actual code, these three shaders only explicitly read two different built-ins: UV and TIME. Lines 11, 13, and 15 in the flame shader are three reading locations, with some repeated use of the same variables:

| Code location | What it reads | Can I change it in this stage? |
|---|---|---|
| `shaders/burning_bottle_fire.gdshader:11` | UV | No; it is a read-only fragment input. |
| `shaders/burning_bottle_fire.gdshader:13` | UV, TIME | Both are read-only. |
| `shaders/burning_bottle_fire.gdshader:15` | TIME | No; it is a read-only global time input. |

The flame shader writes ALBEDO on line 17 and ALPHA on line 18. Cargo also writes ROUGHNESS on line 19, NORMAL_MAP on line 20, and NORMAL_MAP_DEPTH on line 21. These set the fragment outputs without changing UV or TIME.

fire_remaining and tint_color are uniforms I declared, so they do not count as built-ins. p and shape are local variables inside the function and do not count either.

Code: `shaders/burning_bottle_fire.gdshader:17`, `:18`;
`shaders/cargo_panel.gdshader:19`, `:20`, `:21`.
Reference: [Godot Spatial shaders — Built-ins](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html#built-ins).

### 4. Do the hints only affect the Inspector, or do they also change the values the shader receives?

| Hint | Where I used it | My understanding |
|---|---|---|
| source_color | `shaders/hint_experiment.gdshader:4`; `shaders/cargo_panel.gdshader:3`, `:9` | A color uniform gets a color control. For a color sampler, Forward+ decodes sRGB into linear values, so this affects the sampled values. |
| hint_range | `shaders/cargo_panel.gdshader:8`, `:12`, `:13` | It gives the Inspector a range and step size. It does not clamp values assigned from code. |
| hint_normal | `shaders/cargo_panel.gdshader:5` | It marks the texture as a normal map for the engine's texture handling. It does not decode the map as sRGB or automatically change DX's Y direction to GL's. After I write the encoded sample to NORMAL_MAP, the built-in normal-map path handles its interpretation and reconstruction. |
| filter_nearest / filter_linear_mipmap | `shaders/hint_experiment.gdshader:4`, `:5`; `shaders/cargo_panel.gdshader:3` | These change GPU texture filtering. The first uses the nearest texel; the second uses linear filtering and mipmaps. They affect sampling, beyond how a control looks in the Inspector. |
| repeat_disable / repeat_enable | Same locations as above | These control sampling outside the 0–1 UV range. Repeating is disabled in the hint experiment and enabled in cargo so uv_scale can exceed 1. |

I compared this with the rendered results in `evidence/a5/hint-experiment/measurement.json`. That capture used Godot 4.7.2, Forward+, D3D12, and an AMD Radeon(TM) 610M. Tonemapping was Linear, exposure was 1, and post-processing was disabled.

| File gray | With source_color: predicted / measured RGB | Without source_color: predicted / measured RGB |
|---|---|---|
| 64 | 64 / (64,64,64) | 137 / (137,137,137) |
| 128 | 128 / (128,128,128) | 188 / (188,188,188) |
| 192 | 192 / (192,192,192) | 225 / (225,225,225) |

All six within_2 values are true, and the center samples match the predictions exactly. I also looked at hint-experiment.png in the same folder. The bottom row, without source_color, is visibly brighter.

The RGB values in the table come from the measurements; I did not estimate them by looking at the screenshot or rerun the capture while writing these notes. With the hint, the value is decoded first and encoded again at output, returning to the file's original gray. Without the hint, that first decoding step is missing, so encoding the raw value makes the displayed result brighter.

Reference: [Godot Shading language — Uniform hints](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#uniform-hints).

### 5. Does hint_range clamp a value set from code?

No. In `logs/a5_probe_headless_60fps.log:9`, I found:
`FACT hint_range value set 2.0 from code, read back: 2.0`.

Setting 2.0 and reading back 2.0 shows that hint_range did not automatically limit the material parameter to 1.0. This was a headless test, though, so it only tells me about the stored value, not the color displayed on screen.

The flame shader's hint on line 4 has a range of 0–1, but the mix on line 17 has no clamp. The alpha calculation on line 18 explicitly uses clamp. The normal driver also limits the state ratio to 0–1 in `entities/fire_flame.gd:43`.

I therefore need to separate whether the material can store 2.0 from what the shader does after receiving 2.0. Question 6 in the brief predicts that center pixel A will be (210,255,67). The real rendered capture now measures exactly (210,255,67), and the material reads back 2.0. At r=1 the same point is (210,210,67). Both results match the original predictions.

Code: `shaders/burning_bottle_fire.gdshader:4`, `:17`, `:18`.

### 6. Which lines in the generated shader sample albedo as color and normals as data, and where are the matching lines in my shader?

I found texture_albedo on line 7 of the generated file. It has source_color, so it is treated as color. texture_normal on line 19 has hint_roughness_normal and no source_color, so the normal sample is not decoded as sRGB color. Lines 34 and 35 sample and combine albedo. Line 46 sends the normal sample to NORMAL_MAP, and line 47 sets its strength.

In my cargo shader, the matching declarations are albedo_tex on line 3 and normal_tex on line 5. The first has source_color. The second has hint_normal and no source_color. Line 18 multiplies the color sample by tint_color.rgb and writes ALBEDO. Line 20 sends the normal sample straight to NORMAL_MAP, without applying `*2-1` or writing NORMAL directly.

The normal hints have different names: the generated shader uses hint_roughness_normal, while cargo uses hint_normal. The shared point for this question is that neither marks the normal texture as source_color.

Code: `shaders/standard_generated.gdshader:7`, `:19`, `:34`, `:35`, `:46`, `:47`;
`shaders/cargo_panel.gdshader:3`, `:5`, `:18`, `:20`.

### 7. Why can't fragment() read what a neighboring pixel is currently calculating, and how does game state reach the shader?

My understanding is that each fragment calculates its own result. I cannot assume a neighboring fragment has already finished, and there is no variable here that gives me the ALBEDO it is currently writing. texture() reads a supplied texture, not another fragment's current output. For an effect that needs neighboring pixels, I would first render a result into a texture and sample it in a later rendering step.

Game state comes from the CPU through uniforms. The flame shader declares fire_remaining on line 4 and uses it for color and alpha on lines 17 and 18. In `entities/fire_flame.gd`, line 24 stores the initial lasting value, line 34 creates a separate material for each fire, and line 36 sets its initial value to 1.0. Line 43 then uses set_shader_parameter to write the clamped lasting/initial_lasting ratio. During a pause, line 42 skips that update.

This lets several fires share one Shader while keeping separate material values. The shader handles their appearance without changing damage or burning duration.

Code: `shaders/burning_bottle_fire.gdshader:4`, `:17`, `:18`.
Reference: [Godot Introduction to shaders — Parallel execution](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html).

### 8. What are two things Godot's shading language provides that ordinary GLSL does not, or that I would otherwise need to connect myself?

The two I used most directly were color hints and Inspector parameters.

The first is source_color. Adding it on cargo line 3 tells the engine that the sampler reads a color texture. Lines 4, 5, and 9 of the hint experiment show the difference using the same PNG. A regular GLSL application can also do sRGB sampling, but the application usually needs to configure the texture format and bindings. It does not get that connection from a source_color hint on a uniform declaration.

The second is group_uniforms and hint_range. Cargo lines 7, 11, and 14 organize the parameters into Surface and Response. Lines 8, 12, and 13 define the sliders' ranges and steps. Ordinary GLSL uniform declarations do not automatically create those Inspector controls; the application needs its own interface code.

TIME on flame lines 13 and 15 is another input Godot provides. Ordinary GLSL has no standard TIME variable that automatically follows the game, so the application normally passes time in itself. The rendered R5 test advances 120 frames at fixed 60 fps: TIME advances 2.0, 1.0, 4.0, and 0.0 seconds at time_scale 1, 0.5, 2, and 0. It follows the engine time scale. These are simulation intervals; fixed-fps runs finish faster than real time on this machine.

Code: `shaders/cargo_panel.gdshader:3`, `:7`, `:8`, `:11`, `:12`, `:13`, `:14`;
`shaders/hint_experiment.gdshader:4`, `:5`, `:9`; `shaders/burning_bottle_fire.gdshader:13`.
Reference: [Godot Shading language — Uniform groups](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#uniform-groups).
