# LANGUAGE-NOTES — Assignment 5

Answers are mine, in my own words. claude.ai checked them against my code and added the line references; where it asked me to correct a claim, I rewrote it.

Line references: `hurt_tint` = `walker-magic-zhefan/shaders/hurt_tint.gdshader`, `rock_frost` = `walker-magic-zhefan/shaders/rock_frost.gdshader`, `hint_experiment` = `walker-magic-zhefan/shaders/hint_experiment.gdshader`.

## The generated shader

`walker-magic-zhefan/shaders/standard_generated.gdshader`, made by me in the editor: a StandardMaterial3D on a BoxMesh with `rock_01_diff_1k.png` as albedo texture, Normal Map enabled with `rock_01_nor_gl_1k.png`, and `rock_01_rough_1k.png` as roughness texture, then Material Override > Convert to ShaderMaterial, then Shader > Save As. Nothing in the game uses it. Line numbers in that file (`std` below):

| What | Line | Text |
|---|---|---|
| `shader_type` | `std:3` | `shader_type spatial;` |
| `render_mode` | `std:4` | `blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx` |
| Uniform for the Inspector's albedo colour | `std:6` | `uniform vec4 albedo : source_color;` |
| Uniform for the normal-map strength | `std:20` | `uniform float normal_scale : hint_range(-16.0, 16.0);` |
| Albedo sampler and hints | `std:7` | `texture_albedo : source_color, filter_linear_mipmap, repeat_enable` |
| Normal-map sampler and hints | `std:19` | `texture_normal : hint_roughness_normal, filter_linear_mipmap, repeat_enable` |
| Writes `ALBEDO` | `std:35` | `ALBEDO = albedo.rgb * albedo_tex.rgb;` |
| Writes `ROUGHNESS` | `std:43` | `ROUGHNESS = roughness_tex * roughness;` |
| Writes `NORMAL_MAP` | `std:46` | `NORMAL_MAP = texture(texture_normal, base_uv).rgb;` (and `NORMAL_MAP_DEPTH` at `std:47`) |

Two annotated pairs, generated line beside mine:

- `std:7` `texture_albedo : source_color, ...` and `rock_frost:16` `texture_albedo : source_color, filter_linear_mipmap`: both mark the albedo as sRGB colour, so it is decoded to linear when sampled. The generated one adds `repeat_enable`; mine uses the default repeat.
- `std:19` `texture_normal : hint_roughness_normal, ...` and `rock_frost:17` `texture_normal : hint_normal, filter_linear_mipmap`: neither has `source_color`, so both read the normal map as data. The generated one uses `hint_roughness_normal`, which also links the normal map to the roughness texture (`std:14`, `hint_roughness_r`); mine uses plain `hint_normal`.

Other differences I noticed: the generated shader writes a `vertex()` (`std:27–29`) that scales the UVs, and picks the roughness channel with a `dot` against a channel vector (`std:41–42`), where I read `.r` directly (`rock_frost:24`).

## Questions

**1. What does `shader_type` decide?**
`shader_type` decides whether the shader works on 2D canvas objects or 3D objects, and so which built-in variables and functions exist. `canvas_item` (`hurt_tint:1`) uses the 2D rendering pipeline. `spatial` (`rock_frost:1`, `hint_experiment:1`) uses the 3D rendering pipeline with lighting.

**2. Which processor functions did I write, and when does each run? What would change if the colour line moved into `vertex()`?**
I only wrote `fragment()` (`hurt_tint:6–8`, `rock_frost:21–48`, `hint_experiment:9–15`), which runs for every pixel the object covers. If I moved the colour line (`hurt_tint:7`) into `vertex()`, it would run only at the sprite's four vertices and be interpolated. Also, in `vertex()` `COLOR` is only the vertex colour, before the texture is multiplied in, so the texture colour would be multiplied by red instead of blended with red. For the blue hat (58, 64, 160) at intensity 1.0, blending with red gives (255, 0, 0), while multiplying by red gives (58, 0, 0).

**3. Three built-ins I read, two I wrote; which of the read ones are read-only?**
I read `COLOR` (`hurt_tint:7`) and `UV` (`rock_frost:23–25`, `hint_experiment:11,13`). My shaders read only these two built-ins, because the texture data comes from my own samplers, not the built-in `TEXTURE`. I write `COLOR` (`hurt_tint:7`), `ALBEDO` (`rock_frost:38`, `hint_experiment:11,13`), `ROUGHNESS` (`rock_frost:43`), `NORMAL_MAP` (`rock_frost:46`) and `NORMAL_MAP_DEPTH` (`rock_frost:47`). `UV` is read-only, while `COLOR` can be both read and written in my canvas_item shader.

**4. For each hint I used, does it change only the Inspector, or also the value the shader receives?** *(translated from my Chinese)*
It depends on the hint and on the pipeline (2D or 3D).
- `source_color` on a sampler (`rock_frost:16`, `hint_experiment:4`) changes the value: the sRGB texel is decoded to linear before the shader uses it. In my hint experiment the same stored grey 128 showed as 128 with the hint and as 188 without it (`captures/hint_pixels.json`, `captures/hint_quads.png`).
- `source_color` on a 2D colour uniform (`hurt_tint:3`) did not change the value here: a grey of 0.5 took part in the arithmetic as 127.5, with no linear conversion (`captures/hurt_tint_pixels.json`). It gives the Inspector a colour picker.
- `hint_range` (`hurt_tint:4`, `rock_frost:6,7,12`) only changes the Inspector, a slider: a value of 2.0 set from code reached the shader unchanged (question 5).
- `hint_normal` and `hint_default_white` (`rock_frost:17,18`) only decide the fallback when no texture is bound (a flat normal, or white); with a texture bound, the texture is read as it is.

**5. Does `hint_range` clamp a value set from code?** *(translated from my Chinese)*
No. The limit only exists in the Inspector. With the tint set to grey (0.5) and `intensity` set to 2.0 from code, above the range's maximum, the hair pixel measured (23, 25, 15) and the hat pixel (197, 191, 95) (`captures/hurt_tint_pixels.json`, `captures/hurt_tint_grey_i2.0.png`). These match my prediction for 2.0 not clamped; if it had been clamped to 1.0, both pixels would have been (128, 128, 128). I used grey because with pure red every value of 1.0 or more gives the same pure red, so that test could not tell the two cases apart.

**6. Which line of the generated shader makes the albedo sample as colour and the normal map as data, and what is the equivalent line in my textured shader?** *(translated from my Chinese)*
In the generated shader, `std:7` gives the albedo sampler `source_color`, so it is decoded from sRGB as colour, and `std:19` declares the normal sampler without `source_color` (with `hint_roughness_normal`), so its vector values are read as data with no colour-space conversion. In my shader the equivalents are `rock_frost:16` (`source_color`) and `rock_frost:17` (`hint_normal`, no `source_color`).

**7. Why can't `fragment()` read what the neighbouring pixel's `fragment()` is computing, and how does game state reach it?**
Fragments run in parallel, so one fragment cannot directly read another fragment's result while it is being calculated. My driver code passes game state through uniforms using `set_shader_parameter()` (`features/player/hurt_tint_driver.gd:15`, into the uniform at `hurt_tint:4`), while the engine provides the built-in variables.

**8. Two things the Godot shading language provides that plain GLSL does not.**
Godot provides special uniform hints like `source_color` and `hint_range` (`hurt_tint:3–4`), as well as `group_uniforms` (`rock_frost:4,10,15,19`). These features make it easier to organize shader parameters compared with regular GLSL.
