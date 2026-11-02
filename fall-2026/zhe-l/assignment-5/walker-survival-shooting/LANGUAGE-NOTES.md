# LANGUAGE-NOTES — Assignment 5

> Written by me in Chinese and translated to English for this repository. Claude only checked the line references (assignment line 375) and, at my request, added two passages to question 4: the last sentence of the "`source_color`, on a colour uniform" row, and the "What I observed" paragraph (my own words about what I saw, plus the pixel values Claude read from my screenshot).
> My three shaders: `godot/shaders/pad_base_light.gdshader` (the screen), `godot/shaders/crate_wear.gdshader` (the crates), `godot/shaders/hint_experiment.gdshader` (the hint experiment). The generated shader: `godot/shaders/standard_generated.gdshader`.

---

## Part 1: line numbers in the generated shader (`standard_generated.gdshader`)

| What to find | Line | What the line says |
|---|---|---|
| `shader_type` | 4 | `shader_type spatial;` |
| `render_mode` | 7 | `render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;` |
| The uniform for the Inspector's albedo colour | 10 | `uniform vec4 albedo : source_color;` |
| The uniform for the Inspector's normal-map strength | 45 | `uniform float normal_scale : hint_range(-16.0, 16.0);` |
| The albedo sampler and its hints | 13 | `uniform sampler2D texture_albedo : source_color, filter_linear_mipmap, repeat_enable;` |
| The normal-map sampler and its hints | 42 | `uniform sampler2D texture_normal : hint_roughness_normal, filter_linear_mipmap, repeat_enable;` |
| The line that writes `ALBEDO` | 67 | `ALBEDO = albedo.rgb * albedo_tex.rgb;` |
| The line that writes `ROUGHNESS` | 83 | `ROUGHNESS = roughness_tex * roughness;` |
| The line that writes `NORMAL_MAP` | 86 | `NORMAL_MAP = texture(texture_normal, base_uv).rgb;` |

---

## Part 2: questions (each answer cites lines in my three shaders)

### 1. What does `shader_type` decide? (Answer for each type used, citing the first line of each shader)

`shader_type` decides what kind of rendered object the shader is used on, and which processor functions and built-ins it can use.

All of my shaders use `spatial`, which is for 3D objects: the crate shells, the tablet screen and the QuadMeshes of the experiment. A QuadMesh is flat, but it is still a 3D mesh.

Where it is:
- `crate_wear.gdshader`: line 1.
- `hint_experiment.gdshader`: line 1.
- `pad_base_light.gdshader`: line 1.
- `standard_generated.gdshader`: line 4; the three lines before it are a comment and blank lines.

### 2. Which processor functions did I write, and when does each run? What would change if I moved my colour line into `vertex()`, and why?

I used `vertex()` and `fragment()`.

`vertex()` runs while the mesh's vertices are processed, once for each vertex processed. `crate_wear.gdshader` lines 22–32 use it to make UVs from the vertex position and normal; `standard_generated.gdshader` lines 56–59 use it to scale and offset the existing UVs.

`fragment()` runs on the fragments produced by rasterization and computes properties of the surface such as its colour. Where it is:
- `crate_wear.gdshader`: lines 34–42.
- `hint_experiment.gdshader`: lines 8–14.
- `pad_base_light.gdshader`: lines 5–7.
- `standard_generated.gdshader`: lines 61–90.

**The line that writes `ALBEDO` cannot simply be moved into `vertex()`, because `ALBEDO` is not an output available in the vertex stage; it would be a compile error.** If the colour were instead computed in the vertex stage and passed to `fragment()` through a varying, the colour between vertices would be interpolated from the vertex results, and small rust patches or colour bands could be lost.

### 3. Three built-ins I read and two I wrote. Which of the ones I read are read-only?

Taking the crate shader as the example:

| Operation | Built-in | What for, and line |
|---|---|---|
| Read | `NORMAL` | Tells which way the face points, `crate_wear.gdshader` lines 23, 25 |
| Read | `VERTEX` | The vertex position used as projection coordinates, lines 24, 26, 28 |
| Read | `UV` | The sampling coordinates of the two textures, lines 35, 36 |
| Write | `ALBEDO` | Outputs the colour after mixing paint and rust, line 40 |
| Write | `ROUGHNESS` | Outputs the mixed roughness, line 41 |

Whether one is read-only depends on the stage:
- In `vertex()`, `VERTEX`, `NORMAL` and `UV` are all inout and can be read and written.
- In `fragment()`, `UV` is in, read-only.

So not changing `VERTEX` and `NORMAL` was my choice in this implementation, not a sign that they cannot be changed. Also, counting strictly, the crate shader also writes `UV` on lines 24, 26, 28 and 31; the "two" above are the two fragment material outputs.

### 4. For each hint I used: does it change only the Inspector, or also the value the shader receives? (Citing the hint experiment)

| Hint | What it does | Where |
|---|---|---|
| `hint_range(...)` | Sets the Inspector's input range and step; it does not add a `clamp()` to the shader's arithmetic | `crate_wear.gdshader` lines 8, 11, 12, 15 |
| `source_color`, on a colour uniform | Makes the Inspector edit the uniform as a colour and the engine treat it as a colour, not as four separate numbers. It also converts the value from sRGB to linear before the shader gets it: the 0.260 written on `crate_wear.gdshader` line 7 reaches the shader as about 0.055 | `crate_wear.gdshader` line 7; `pad_base_light.gdshader` line 3 |
| `source_color`, on a sampler | In this Forward+ experiment, the sRGB colour texture is decoded to linear values before it is used in the arithmetic | `hint_experiment.gdshader` line 4 |
| `filter_nearest` | Nearest-neighbour sampling, no blending of neighbouring pixels, so it affects the values read | `hint_experiment.gdshader` lines 4, 5 |
| `filter_linear_mipmap` | Linear filtering with mipmaps, which affects the sampled result | `crate_wear.gdshader` lines 3, 4 |
| `repeat_enable` | Coordinates outside 0–1 sample the texture repeated | `crate_wear.gdshader` lines 3, 4 |
| `hint_default_white` | When no texture is bound, a white default texture is used, which affects the sampled result | `standard_generated.gdshader` line 24 |
| `hint_roughness_r`, `hint_roughness_normal` | Give the import-time roughness anti-aliasing information about what the texture is for; not just an Inspector setting | `standard_generated.gdshader` lines 32, 42 |

So hints are not all Inspector hints: some affect how colour is interpreted, how textures are sampled, or how they are processed on import.

In the hint experiment, the two samplers on lines 4 and 5 differ only in having `source_color` or not, and lines 9–12 choose one of them by a bool. Under the experiment's stated conditions, the expected displayed values are:

| Grey in the texture | With `source_color` | Without `source_color` |
|---|---|---|
| 64 | 64 | 137 |
| 128 | 128 | 188 |
| 192 | 192 | 225 |

With the hint, the colour is decoded and then encoded, which restores the original grey; without it, the raw numbers are taken as linear values and become brighter after the display encoding. This table is my hand-computed prediction, made beforehand.

What I observed: I opened `experiments/hint/hint_experiment.tscn` in the editor and saw that only the leftmost colour looked different, and, as an optical effect, the upper quad even looked somewhat darker. The pixel values Claude read from my screenshot (`captures/hint_experiment_editor_view.png`, an OS screenshot of the editor's 3D viewport) are: upper quad (with `source_color`) 64 / 128 / 192, lower quad (without) 137 / 188 / 225, exactly as predicted. All three bands actually differ; the gaps from left to right are 73, 60 and 33 levels, which is why to the eye it looked as if only the leftmost one differed.

### 5. Does `hint_range` clamp a value set from code? (Citing what I observed)

No, `hint_range` does not automatically limit a value passed in from code.
I ran `screen_glow_capture.tscn` from the editor and pressed F9 while holding the tablet in both hands. The capture tool first paused the driver, then set `pad_light_data` from code to 0, 0.39, 1.0 and 2.0 in turn.
According to section 4 of `TEST-REPORT`, at 2.0 the screen centre P1 and the corner P2 both show (255, 255, 255), recorded in the capture `screen_pad_2.00.png`, which matches my prediction B made beforehand.
Although `pad_base_light.gdshader` line 4 declares `hint_range(0.0, 1.0)`, line 6 uses the value directly:

```
ALBEDO = mix(vec3(0.0), cold_white.rgb, pad_light_data);
```

This line has no `clamp()`. With the parameter at 2.0 the result is 2 × `cold_white.rgb`, all three linear colour channels go above 1, and the screen shows pure white.
So the experiment shows that the parameter was not clipped to 1.0 by `hint_range`. The final 255 is the colour output reaching the display's maximum, which is a different matter from whether the parameter was limited.

### 6. Which line of the generated shader makes the albedo sample as colour and the normal map as data, and what is the equivalent line in my textured shader?

In `standard_generated.gdshader`:

* Line 13: `texture_albedo` has `source_color`, so it is treated as sRGB colour.
* Line 42: `texture_normal` has no `source_color`, so the normal data keep their numeric meaning; line 86 writes the sampled result to `NORMAL_MAP`.

In `crate_wear.gdshader`:

* Line 3: `rust_albedo` has `source_color`; it is the rust colour.
* Line 4: `wear_mask` has no `source_color`; it is height data.
* Lines 35 and 36 read the two textures.

What keeps the normal map from being colour-decoded is the absence of `source_color`, not `hint_roughness_normal` doing it automatically.

### 7. My `fragment()` runs for every pixel at once. Why can't it read what the neighbouring pixel's `fragment()` is computing, and how does game state reach it instead?

The GPU processes a large number of fragments in parallel, with no guaranteed order between neighbouring fragments. Each `fragment()` invocation has its own local variables; an ordinary fragment shader has no shared interface to read a neighbour's local variables directly, and does not know whether the neighbour has finished.
For example, `rust`, `height`, `width` and `w` on `crate_wear.gdshader` lines 35–38 all belong to the current fragment, and lines 40 and 41 output the current fragment's material properties. To read other pixels' results, the results usually have to be rendered to a texture first and then sampled in a later rendering step.
Game state can be passed in from GDScript as a uniform with `ShaderMaterial.set_shader_parameter()`. For example, `pad_base_light.gdshader` line 4 declares `pad_light_data` and line 6 uses it to control the screen brightness; `hint_experiment.gdshader` line 6 declares a bool and line 9 uses it to choose a sampler. The shader itself does not access game nodes or GDScript variables directly.

### 8. Two things the Godot shading language provides that plain GLSL does not, or makes you write yourself

First, uniform hints and groups connected to the Inspector.
For example, `crate_wear.gdshader` lines 6, 10, 14 and 17 organize the parameters with `group_uniforms`, and lines 7–15 use colour and range hints. Plain GLSL has uniforms but none of these Godot Inspector features; the application has to build the interface itself.

Second, outputs connected directly to the engine's material and lighting system.
For example, `crate_wear.gdshader` lines 40 and 41 write `ALBEDO` and `ROUGHNESS`, and `standard_generated.gdshader` lines 86 and 89 write the normal map and its strength. Godot goes on to compute lighting from these properties; plain GLSL has no such predefined material outputs, and you have to build the corresponding interface and lighting calculation yourself.
