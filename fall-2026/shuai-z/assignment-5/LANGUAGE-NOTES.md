# LANGUAGE-NOTES — Assignment 5

Written 2026-10-27. Line numbers refer to the current files, including the English comments in the generated shader. The measurements below come from the saved 1920 × 1080 PNGs and capture logs; I also reread the PNG pixels to check the log values.

## File key

- **T** — [game/shaders/invulnerable_tint.gdshader](game/shaders/invulnerable_tint.gdshader)
- **S** — [godot/shaders/weathered_stone.gdshader](godot/shaders/weathered_stone.gdshader)
- **H** — [godot/shaders/hint_experiment.gdshader](godot/shaders/hint_experiment.gdshader)
- **G** — [godot/shaders/standard_generated.gdshader](godot/shaders/standard_generated.gdshader)

For example, **T:8** means line 8 of the tint shader. T, S and H are the three authored shaders discussed in Part B; G is the separate Godot-generated comparison.

## A. Locate the generated code

G was produced by Godot 4.7.2's StandardMaterial3D converter after assigning the Rock 01 albedo, OpenGL normal and roughness textures and enabling Normal Map. The conversion was made in the Inspector's resource menu; English comments were added afterward. The parameter values and texture bindings belonged to the temporary ShaderMaterial, which was not saved with this standalone shader.

| Requested item | Line in G | Exact code |
|---|---:|---|
| Shader type | 5 | `shader_type spatial;` |
| Render modes | 6 | `render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;` |
| Inspector Albedo → Color | 9 | `uniform vec4 albedo : source_color;` |
| Inspector Normal Map → Scale (strength) | 34 | `uniform float normal_scale : hint_range(-16.0, 16.0);` |
| Albedo sampler and hints | 11 | `uniform sampler2D texture_albedo : source_color, filter_linear_mipmap, repeat_enable;` |
| Normal sampler and hints | 32 | `uniform sampler2D texture_normal : hint_roughness_normal, filter_linear_mipmap, repeat_enable;` |
| Write ALBEDO | 54 | `ALBEDO = albedo.rgb * albedo_tex.rgb;` |
| Write ROUGHNESS | 66 | `ROUGHNESS = roughness_tex * roughness;` |
| Write NORMAL_MAP | 70 | `NORMAL_MAP = texture(texture_normal, base_uv).rgb;` |

G:72 applies the normal strength separately: `NORMAL_MAP_DEPTH = normal_scale;`.

## B. Eight questions

### 1. What does shader_type decide?

It selects the kind of object being shaded and the available processor functions, built-ins and render modes. **T:1** selects `canvas_item` for the 2D hearts. **S:1** and **H:1** select `spatial` for 3D meshes: the stone surfaces and the experiment's quads. H remains a spatial shader when **H:2** adds `unshaded`; that mode removes lighting, not the 3D pipeline. These are the two shader types used here. See the official [shader-type overview](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html#shader-types), [CanvasItem reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html) and [spatial reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html).

### 2. Which processor functions did I write, and when do they run? What if the color line moves to vertex()?

The authored shaders define only `fragment()`: **T:7**, **S:16** and **H:8**. Each invocation shades a rasterized fragment, using interpolated inputs. A pixel can involve multiple fragments; it is not exactly one invocation per final screen pixel. G's generated `vertex()` at G:43 runs per vertex and changes UV at G:45. None of T, S or H defines `vertex()` or `light()`. See [processor functions](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html#shaders-in-godot).

At **T:8**, incoming `COLOR` already includes the heart texture multiplied by vertex color and CanvasItem modulation. In `vertex()`, `COLOR` contains the vertex/modulation color before that texture multiplication. Moving the line would therefore tint a multiplier rather than the already textured heart. See [COLOR and TEXTURE](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html#color-and-texture).

Writing RGB componentwise, let `t` be the heart texel, `v` the interpolated vertex/modulation color, `c` the tint color and `w = tint_amount * tint_strength`. The current result is `mix(t * v, c, w)`. Moving the line to `vertex()` and leaving the fragment stage unchanged would give `t * mix(v, c, w)`. The latter also multiplies the tint contribution by the heart texture, so it does not move every visible texel toward the same pale blue. Both versions leave alpha untouched because the assignment targets `.rgb` only.

### 3. Which built-ins do I read and write? Which reads are read-only?

There is a counting limitation in the current source: the three authored shaders explicitly read only **two distinct built-in names**, `COLOR` and `UV`. The third input below is used implicitly by Godot. I cannot claim three explicit built-in reads without changing the shaders.

| Input | Evidence in the authored shaders | Access in the relevant stage |
|---|---|---|
| `COLOR` | **T:8**, right-hand side of `mix()` | CanvasItem fragment `inout`: readable and writable. |
| `UV` | **S:17** and **H:10, H:12** | Spatial fragment `in`: read-only. The local `scaled_uv` can change; the incoming `UV` cannot. |
| `TEXTURE` — implicit only | The incoming `COLOR` consumed by **T:8** already includes the default heart texture. There is no explicit `texture(TEXTURE, UV)` call in T. | Read-only sampler; the engine samples it before the authored fragment color operation. |

Two explicit writes are `COLOR.rgb` at **T:8** and `ALBEDO` at **S:18**. The former is `inout`; spatial `ALBEDO` is `out`. `NORMAL_MAP` at **S:19** is another output, not a third input read. Access qualifiers depend on the stage: spatial `UV` is writable in `vertex()` but read-only in `fragment()`. See the [CanvasItem built-ins](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html#built-ins) and [spatial fragment built-ins](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html#fragment-built-ins).

### 4. Do the hints only change the Inspector, or do they affect shader values?

| Hint used in T, S or H | Source lines | Effect |
|---|---|---|
| `hint_range` | **T:3, T:5; S:9, S:12, S:13** | Inspector range/step controls; no runtime clamp, as measured in question 5. |
| `source_color` | **T:4; S:3, S:8; H:4** | Color controls for vectors and color-space interpretation. For samplers in this Forward+ experiment, it changes the sampled values through sRGB decoding. |
| `hint_normal` | **S:4** | Normal-map handling, including a flat-normal fallback when unbound; not a color-space decode. |
| `filter_linear_mipmap` | **S:3–5** | Sampling behavior; filtering and mip selection can change returned texels. |
| `filter_nearest` | **H:4–5** | Nearest-texel sampling, preserving separate bands here. |
| `repeat_enable` | **S:3–5** | Texture addressing; UVs outside one tile wrap, affecting samples. |

The generated comparison additionally uses `hint_default_white` (G:20), an unbound-texture fallback, and `hint_roughness_r` / `hint_roughness_normal` (G:24, G:32), import-time roughness-limiter metadata. The latter are not sRGB conversion hints. These distinctions follow the [uniform-hint reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#uniform-hints).

**Measured hint experiment.** Both samplers use the same 3 × 1 PNG. **H:6, H:9–12** choose the hinted sampler for Quad A and the plain sampler for Quad B. The run used Metal / Forward+, `unshaded`, Linear tonemapping, exposure 1.0, and no glow, fog or adjustments, as recorded in [the scene probe](logs/probe_hint_scene.log).

| File texel RGB | A: source_color, measured RGB | B: no source_color, measured RGB |
|---|---|---|
| (64, 64, 64) | (64, 64, 64) | (137, 137, 137) |
| (128, 128, 128) | (128, 128, 128) | (188, 188, 188) |
| (192, 192, 192) | (192, 192, 192) | (225, 225, 225) |

Evidence: [hint-experiment.png](evidence/use-it/hint-experiment.png) and [capture_hint.log, lines 7–12](logs/capture_hint.log#L7-L12). Sample x coordinates are 728, 960 and 1192; A uses y = 378 and B uses y = 702. Each surrounding 9 × 9 patch is constant. All six measurements match the brief's predictions exactly.

A's decode followed by display encoding reproduces the file values; B treats those stored values as linear and only applies the display encoding, making the bands brighter. The sampled screen pixels demonstrate that the sampler hint affects rendering, not merely the Inspector. This experiment does not measure every hint independently or establish vector-uniform conversion behavior in the separate Compatibility project.

### 5. Does hint_range clamp a value set from code?

**No, in this measured run.** **T:3** advertises 0.0–1.0, but the capture script sets `tint_amount` to 2.0 and the material reads back 2.0. The driver is stopped first so it cannot overwrite the value: [capture_tint.gd, lines 55–62](game/tests/capture_tint.gd#L55-L62).

| Sample | Measured at 1.0 | Measured at 2.0 | Prediction for unclamped 2.0 |
|---|---|---|---|
| P1, (54, 58) | `#B58086` = (181, 128, 134) | `#A3C1D7` = (163, 193, 215) | `#A2C0D7` = (162, 192, 215) |
| P2, (77, 56) | `#996F7B` = (153, 111, 123) | `#99BBD3` = (153, 187, 211) | `#99BBD3` = (153, 187, 211) |

Evidence: [the 1.0 capture](evidence/use-it/hearts-tint-1.0.png), [the 2.0 capture](evidence/use-it/hearts-tint-2.0.png), and [capture_tint.log, lines 21–30](logs/capture_tint.log#L21-L30). These were rendered with Compatibility, not headlessly.

At **T:8**, the weight becomes `2.0 * 0.4 = 0.8`, rather than the 0.4 weight at 1.0. If the range hint clamped the value, the two captures would match at P1 and P2. They do not. P1 differs from the unclamped prediction by only one 8-bit step in red and green, within the predeclared two-step tolerance; P2 matches exactly. I retain the actual P1 measurement rather than replacing it with the prediction. The transparent control P3 stays `#C8C6CB` in both captures. Where an actual bound is required, **S:21** shows an explicit `clamp()` operation.

### 6. Which lines distinguish color sampling from data sampling?

G:11 declares `texture_albedo` with `source_color`; G:32 declares `texture_normal` with `hint_roughness_normal` and no `source_color`. Their authored counterparts are **S:3**, `albedo_tex : source_color`, and **S:4**, `normal_tex : hint_normal`. **S:18–19** then write the sampled RGB values to `ALBEDO` and `NORMAL_MAP` respectively. The normal hints differ between the two files; they should not be described as identical. Neither normal sampler requests sRGB decoding. The controlled comparison in question 4 shows why this distinction matters for actual sampled values. See [source_color](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#using-source-color).

### 7. Why can a fragment not read its neighbor's ongoing calculation? How does game state arrive?

Fragment invocations can run in parallel, without a guaranteed neighbor-to-neighbor execution order or shared local variables. They do not literally all finish simultaneously. In **S:17**, each invocation has its own `scaled_uv`; **S:18–21** sample existing textures and produce that invocation's outputs. Texture sampling can read nearby texels, but it does not reveal a neighboring invocation's unfinished result. A screen-reading effect needs a defined earlier buffer/pass, not a live peek at a neighbor's work. See [parallel shader execution](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html) and [screen-reading shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/screen-reading_shaders.html).

Rudy's state stays in GDScript. The HUD reads the remaining invulnerability time, divides it by the window duration, and calls `set_shader_parameter("tint_amount", ...)` in [hud.gd:111](game/ui/hud.gd#L111), reached from `_process()` at lines 89–92. **T:3** declares that uniform, and **T:8** reads it. Godot supplies the material value to the draw; fragments do not read the Rudy node or run the game-state countdown themselves.

### 8. What two things does Godot provide beyond plain GLSL?

1. **Inspector metadata in shader source.** **S:7, S:11 and S:14** organize the four numerical uniforms into `surface` and `relief`; **S:9** supplies a range and step. A plain GLSL uniform declaration does not build those Godot Inspector sections or controls. See [uniform groups](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#uniform-groups).
2. **Material outputs connected to an existing renderer.** **S:18–21** supply `ALBEDO`, `NORMAL_MAP`, `NORMAL_MAP_DEPTH` and `ROUGHNESS`. Godot connects them to its material lighting pipeline. In a plain GLSL application I would need to provide the corresponding interfaces and rendering/lighting implementation; those uppercase Godot names are not standard GLSL built-ins. See [spatial fragment outputs](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html#fragment-built-ins).
