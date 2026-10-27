# CHANGE-BRIEF — Assignment 5: hurt tint and frosted rock

Author: Zhefan Zhang (zhefan-z). Original version, 2026-10-22. Dated revisions go at the end; this text is not edited in place.

Authorship of this file: every decision, the colour line, all uniform and sampler declarations, and every hand computation below are mine. claude.ai (chat) compiled the file from my answers, looked up the project facts with me, and checked my arithmetic; where it corrected me, the correction is noted. Passages marked *(translated from my Chinese)* are my own explanations, translated.

Paths are relative to `walker-magic-zhefan/` (`res://`) unless they start with `scripts/` or `logs/`.

## 1. The state

**What it communicates.** After a wolf's lunge lands, the mage is invulnerable for 1.0 s. The player needs to see that window: it explains why a second contact does nothing, and it marks the hit as a warning. Red was chosen as an injury warning. This is a deliberate exception to design pillar 1 (warm colours only for fire): a hit is danger, not warmth.

**Where it lives.**

| Fact | Value | Reference |
|---|---|---|
| Variable | `Player.invulnerable`, seconds left | `features/player/player.gd:37` |
| Begins | set to `Tuning.INVULNERABLE_TIME` (1.0) when a hit lands | `player.gd:155`, `features/player/tuning.gd:16` |
| Counts down | `maxf(invulnerable - delta, 0.0)` in `_physics_process` | `player.gd:80` |
| Ignores hits while active | `take_damage` returns if `invulnerable > 0.0` | `player.gd:152` |
| Cleared on win | `invulnerable = 0.0` | `player.gd:142` |
| Frozen on fail | `fail()` disables `_physics_process` without clearing it; the final hit sets it to 1.0 first | `player.gd:155`, `player.gd:170` (`fail`) |
| Existing blink (unchanged) | `sprite.visible` toggles every `BLINK_PERIOD` = 0.1 s while active | `player.gd:81`, `tuning.gd:19` |
| Shaded object | the player's `Sprite2D` child, texture swapped per state | `features/player/player.tscn:15`, `player.gd:51` |
| Pause | `main.gd:57` toggles `tree.paused`; only `UI` and `SessionInput` use `process_mode = 3` | `game/main.tscn:97,117` |
| Physics rate | not set in `project.godot`, so the default 60 ticks per second | `project.godot` |

## 2. Effect specification — the hurt tint

**Shader.** `shaders/hurt_tint.gdshader`, `shader_type canvas_item;`, no `render_mode`. Hand-written by me. On a `ShaderMaterial` assigned to the player's `Sprite2D`.

| Uniform | Type and hint | Default | Set by |
|---|---|---|---|
| `tint_color` | `vec4 : source_color` | `vec4(1.0, 0.0, 0.0, 1.0)` | the shader default; never changed by code |
| `intensity` | `float : hint_range(0.0, 1.0)` | `0.0` | a presentation-only driver script, every frame, from `Player.invulnerable` (script path and wiring proposed by Claude Code in Step 2) |

Declarations as I will write them:

```glsl
uniform vec4 tint_color : source_color = vec4(1.0, 0.0, 0.0, 1.0);
uniform float intensity : hint_range(0.0, 1.0) = 0.0;
```

**The colour line**, inside `fragment()`:

```glsl
COLOR.rgb = mix(COLOR.rgb, tint_color.rgb, intensity);
```

It mixes the sprite's colour toward red by `intensity` and leaves `COLOR.a` untouched, so transparent pixels stay transparent. No samplers of its own; the sprite texture arrives in `COLOR`. No `TIME`.

**Driver mapping.** `intensity = invulnerable / Tuning.INVULNERABLE_TIME` while `invulnerable > 0.0` and the player is neither failing nor cleared; otherwise `0.0`.

### Observable rules

| # | Rule | Expected |
|---|---|---|
| R1 | Value when the state begins | On the first sampled frame after a hit lands, `intensity` is 1.0 minus at most one frame period plus one physics step (≥ 0.95 at 30 fps, because up to two physics ticks run per frame) |
| R2 | Shape | Decreases linearly with game time, never increases until the next landed hit |
| R3 | Value when the state ends | 0.0 on the first frame `invulnerable` is 0.0, and stays 0.0 |
| R4 | Duration | 1.0 s of game time from the first frame with `intensity > 0` to the first frame with `intensity == 0`, at 30, 60 and 144 fps. Tolerance: one frame period, widened to one physics step (1/60 s) at 144 fps, because `invulnerable` only changes on physics ticks. At 144 fps several consecutive frames may sample the same value; that is expected |
| R5 | Retrigger | **Ignore.** A wolf contact while the state holds lands no hit (`player.gd:152`), so `intensity` keeps decreasing and does not return to 1.0. Restart would need a change to game logic, which is out of bounds |
| R6 | Time scale | Scaled time: the countdown uses physics `delta`. Under `Engine.time_scale = 0.5` the effect lasts 1.0 s of game time and 2.0 s of real time |
| R7 | Pause | While the tree is paused, `intensity` holds its value; it resumes counting when unpaused. The driver uses the default pausable process mode |
| R8 | State ends early | If the player fails or clears during the state, `intensity` is 0.0 on that same frame, even though `fail()` leaves `invulnerable` frozen |
| R9 | Instances | One player. The material is unique to the player instance (local to scene), so a reloaded scene starts at the default 0.0 |
| R10 | Blink unchanged | `sprite.visible` still follows `player.gd:81`; the tint shows only on the frames the sprite is visible |

### Boundaries

Unchanged: collision, movement, input, the player state machine and every timing in `tuning.gd`, `take_damage`, `fail`, `win`, the existing blink, every existing test and its expectations, the wolf, the 2D level, the audio, the HUD, and every object other than the player's sprite and the rock. The driver may read `Player` state; it never writes it.

### Evidence split

| Rule | Evidence |
|---|---|
| Uniform names and types | headless: `get_shader_uniform_list()` |
| Defaults (`tint_color`, `intensity = 0.0`) | headless: read from the shader source text (a headless engine does not report them) |
| R1–R5, R8 | headless: drive a real hit through the game loop and scripted input, sample `intensity` every frame from a node with high `process_priority`, at 30, 60 and 144 fps |
| R6, R7 | headless: same test under `Engine.time_scale = 0.5`, and with the tree paused for a known span |
| R9 | headless: reload the scene and read the default |
| R10 and the look | human: in-engine captures and play in the editor |

### Controlled inputs and predicted values

Captured with the driver disabled and `intensity` set from code, so the result is unlit and fixed. `project.godot` sets no `hdr_2d`, so 2D blending happens on the stored sRGB values and the arithmetic below applies directly. Pixels are texture coordinates in `assets/sprites/mage/mage_idle.png` (62×69); both are fully opaque, so the background does not enter the result.

| Pixel | `intensity` 0.0 | 0.5 | 1.0 |
|---|---|---|---|
| Hair (27, 18), stored (232, 230, 240) | (232, 230, 240) | (244, 115, 120) | (255, 0, 0) |
| Hat (24, 7), stored (58, 64, 160) | (58, 64, 160) | (157, 32, 80) | (255, 0, 0) |

Each channel is `stored × (1 − t) + target × t`. At 0.5 the red channel lands on x.5 (243.5 and 156.5); those channels allow ±1.

**Contrast against the background.** Background estimated from the palette's darkest cave colour `#0F1119` (15, 17, 25), not sampled behind the player. WCAG relative luminance:

| | RGB | L | Contrast vs background |
|---|---|---|---|
| Background | (15, 17, 25) | 0.00573 | — |
| Hair at `intensity` 0.0 | (232, 230, 240) | 0.80041 | 15.26 : 1 |
| Pure red at `intensity` 1.0 | (255, 0, 0) | 0.21260 | 4.71 : 1 |

The tint drops the hair's contrast from about 15:1 to about 4.7:1. The mage stays visible against the cave but clearly darkens during the hit. (claude.ai corrected my first-pass hair values, 0.79820 and 15.22:1, which came from imprecise powers.)

## 3. The hint experiment

A committed GDScript writes `assets/textures/hint/greys_3x1.png`: three texels with greys 64, 128, 192. Imported lossless, no mipmaps. A spatial shader with `render_mode unshaded` has two samplers bound to that file, one `source_color, filter_nearest`, one `filter_nearest` only, and a bool uniform picks which one writes `ALBEDO`. Two materials (bool true, bool false) on two quads facing the camera, in their own scene, with a `WorldEnvironment` set explicitly to Linear tonemap, exposure 1.0, glow, fog and adjustments off. Renderer: Forward+.

| Texel | With `source_color` | Without |
|---|---|---|
| 64 | 64 | 137 |
| 128 | 128 | 188 |
| 192 | 192 | 225 (±1; the exact value is 224.9999) |

Without the hint, each value goes through the encode only: `encode(x) = 1.055·x^(1/2.4) − 0.055` for x = 64/255, 128/255, 192/255, giving 0.53807, 0.73665, 0.88235, times 255. (claude.ai corrected my first 128 result, 187, which came from 0.74836 instead of 0.75038.)

**The quad with `source_color` shows the file's values unchanged.** *(translated from my Chinese)* With `source_color`, Godot treats the texture as sRGB colour and decodes it to linear when sampling. Unshaded, with a Linear tonemap at exposure 1.0, the linear value is not changed, and the output is encoded back to sRGB for the screen. Decode and encode cancel, so the screen shows the original numbers. Without the hint, the stored numbers are used as if they were already linear, but the output is still encoded, so the mid-tones are brightened.

## 4. Material plan — the frosted rock

**Object and scenes.** `assets/models/rock.glb`, the rock from Assignment 3. In `showcase3d/prop_room.tscn` it gets the dry material through the importer's per-material Use External setting, so a reimport keeps it; this changes `rock.glb.import`, never `rock.glb`. A new scene `showcase3d/material_compare.tscn` holds two rock instances side by side under a copy of the prop room's lighting: one keeps the dry material from the importer, the other uses a surface material override with the frosted material. Use External applies to every instance of the `.glb`, which is why the second rock needs an override.

**Lighting I will judge under** (`showcase3d/prop_room.tscn:16–30`): one `DirectionalLight3D` "Sun", shadows on, energy at its default 1.0, rotated per its transform at line 29; `Environment` with a solid background colour `#0F1119` and ambient light at its default source. No SSAO, SSIL, glow, fog or SDFGI key is written, so all are at their default (off); tonemap is at its default, Linear at exposure 1.0.

**Shader.** `shaders/rock_frost.gdshader`, `shader_type spatial;`, no `render_mode`. Hand-written by me.

### Textures

Source: Poly Haven "Rock 01", https://polyhaven.com/a/rock_01, author Rob Tuytel, CC0, 1K PNG, downloaded 2026-10-22 from `dl.polyhaven.org`, unmodified. Folder: `assets/textures/rock_01/`.

| File | Role | What its numbers mean | Sampled as | compress/mode | compress/normal_map | mipmaps/generate |
|---|---|---|---|---|---|---|
| `rock_01_diff_1k.png` (8-bit RGB) | albedo | sRGB surface colour | colour, `source_color` | VRAM Compressed | Disabled | true |
| `rock_01_nor_gl_1k.png` (8-bit RGB) | normal map | tangent-space normal, OpenGL green convention, which Godot expects | data, `hint_normal` | VRAM Compressed | Enable | true |
| `rock_01_rough_1k.png` (16-bit greyscale) | roughness, and the frost mask | 0 = smooth, 1 = rough, read as stored | data, no `source_color` | VRAM Compressed | Disabled | true |
| `rock_01_nor_dx_1k.png` (8-bit RGB) | not bound to any material | DirectX green convention | only read by the curl check, to calibrate it | VRAM Compressed | Enable | true |

All four also set `detect_3d/compress_to` explicitly to disabled, so the editor has nothing to change later. Integer values for these enums are looked up in the Godot documentation at import time, not assumed. The roughness file is 16-bit; the format Godot imports it to is checked with `get_image().get_format()`.

Sampler declarations as I will write them:

```glsl
group_uniforms textures;
uniform sampler2D texture_albedo : source_color, filter_linear_mipmap;
uniform sampler2D texture_normal : hint_normal, filter_linear_mipmap;
uniform sampler2D texture_roughness : hint_default_white, filter_linear_mipmap;
group_uniforms;
```

`hint_default_white` only sets what the sampler returns when no texture is bound.

### Non-texture uniforms

```glsl
group_uniforms surface;
uniform vec4 base_tint : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform float normal_scale : hint_range(0.0, 2.0, 0.05) = 1.0;
uniform float roughness_scale : hint_range(0.0, 2.0, 0.05) = 1.0;

group_uniforms frost;
uniform vec4 frost_color : source_color = vec4(0.85, 0.92, 1.0, 1.0);
uniform float frost_amount : hint_range(0.0, 1.0, 0.01) = 0.0;
```

| Group | Uniform | Range | Default | Expected on screen across its range |
|---|---|---|---|---|
| surface | `base_tint` | colour | white | multiplies the albedo; white leaves the texture as it is |
| surface | `normal_scale` | 0.0–2.0 | 1.0 | 0 flattens the surface detail; 2 exaggerates it |
| surface | `roughness_scale` | 0.0–2.0 | 1.0 | multiplies the sampled roughness, and the result is clamped to 0–1 in the shader; low values make the rock glossy, high values make it fully matte |
| frost | `frost_color` | colour | (0.85, 0.92, 1.0) | the colour of the frost layer |
| frost | `frost_amount` | 0.0–1.0 | 0.0 | 0 is no frost; 1 covers the whole surface; in between, areas with low roughness frost first, with a soft edge, and frosted areas get lower roughness |

In a spatial shader the computation is in linear space, so a colour uniform with `source_color` is decoded from sRGB before the shader receives it: `base_tint` (0.92, 0.95, 1.0) does not arrive as those numbers.

### The two materials

| Material | `base_tint` | `frost_amount` | Why |
|---|---|---|---|
| `assets/materials/mat_rock_dry.tres` | (1.0, 1.0, 1.0, 1.0) | 0.0 | the rock as the textures describe it |
| `assets/materials/mat_rock_frosted.tres` | (0.92, 0.95, 1.0, 1.0) | 0.65 | the same rock in a colder part of the cave; the roughness map, read as data, decides where frost settles |

Both reference `shaders/rock_frost.gdshader` and bind the same three textures. They differ in two values.

## 5. Predicted failures

| # | Failure | What it would look like | Check that catches it |
|---|---|---|---|
| F1 | `intensity` default not 0.0, or the driver not wired | the mage is fully red on the first frame, or stays red at rest | headless: the default read from the shader source is 0.0, and `intensity` is 0.0 on frames before any hit; human: first frame of a normal run |
| F2 | the albedo sampler loses `source_color` | the rock looks washed out and too bright in the mid-tones | headless: the material test reads the hint from the source text and fails (the `source_color` mutation); human: side-by-side capture |
| F3 | the normal map imported without `compress/normal_map` Enable, or sampled without `hint_normal` | lighting on the rock looks wrong: blotchy or inverted shading | headless: the material test reads both from the `.import` file and the shader source; human: capture under the stated light |
| F4 | the driver maps `invulnerable` straight to `intensity` and ignores failing | after the hit that takes HP to 0, the kneeling fail image stays fully red, because `fail()` freezes `invulnerable` at 1.0 (`player.gd:155`, `player.gd:170`) | headless: drive a hit that takes HP to 0 and assert `intensity` is 0.0 on that frame and after (R8); a pit fall during the state, same assertion; human: watch one fail in play |

## 6. Short answers, before building

**Renderer.** `project.godot` names no rendering method, so the project uses the default, Forward+. Forward+ rules none of the listed features out: decals and compute shaders need Forward+ or Mobile, and VoxelGI, SDFGI and SSIL are available in Forward+.

*(The answers below are mine, translated from my Chinese.)*

**What colour arrives in `fragment()` before I change it (canvas_item)?** `COLOR` holds the texture's colour at that point multiplied by the vertex colour; the node's modulate reaches the shader through the vertex colour.

**What would `texture(TEXTURE, UV)` give instead of `COLOR`?** Only the texture's colour: the modulate, self-modulate and vertex colour would be lost, so any colour or transparency set on the node in the Inspector would be ignored.

**Spatial: what does `ALBEDO` hold if never written, and what does `COLOR` hold?** `ALBEDO` defaults to white, `vec3(1.0)`, and is still lit. `COLOR` holds the vertex colour, interpolated from the mesh or passed down from `vertex()`.

**How long would a frame-counting version last?** Counting 60 frames: 2.0 s at 30 fps, 1.0 s at 60 fps, about 0.417 s at 144 fps.

**Which resource holds the default, which holds the current value, and what if two objects share the material?** The default is in the shader (`.gdshader`); the current value is in the `ShaderMaterial`. If two objects share one material, a change made through it, including `set_shader_parameter` from code, affects both; to control them separately the material must be unique (local to scene, or duplicated).

**Does `hint_range` clamp a value set from code?** My prediction: no. It only shapes the Inspector slider; `set_shader_parameter(..., 2.0)` passes 2.0 to the shader, and only a `clamp()` in the shader would limit it. To be checked in Use It with a capture at 2.0.

## Revisions

### 2026-10-23 — which rock surface gets the shader

Found while reviewing the CLAUDE.md draft: `rock.glb` has two materials, `Rock_Main` and `Rock_Top`, which section 4 did not account for. Decision: only `Rock_Main` gets the shader material. In the importer, `Rock_Main` uses Use External pointing to `assets/materials/mat_rock_dry.tres`; `Rock_Top` keeps its imported Assignment 3 material. In `showcase3d/material_compare.tscn` the second rock overrides only the `Rock_Main` surface with `mat_rock_frosted.tres`. The two-tone look from Assignment 3 stays.

### 2026-10-23 — R7: measure the paused window in physics ticks

Observed: in `tests/test_hurt_tint.gd`, with a 31-frame pause inside the window, the sum of unpaused frame deltas from the first tinted frame to the first zero frame was 1.0000 s at 30 fps, 0.9833 s at 60 fps and 0.9653 s at 144 fps. The 144 fps value is outside R4's one-physics-step tolerance (`logs/test_hurt_tint_144fps.log`). The value held through the pause and resumed afterwards at all three rates, as R7 requires.

Explanation, not yet confirmed: `invulnerable` only changes on physics ticks (60 per second), and a pause shifts which frames those ticks fall on, so summed frame time is the wrong clock for a window with a pause in it. R4 keeps its frame-time measure for an uninterrupted window.

Revision: R7's duration part is measured in unpaused physics ticks. From the first tinted frame to the first zero frame, the player's `_physics_process` runs 60 times, minus at most the one tick that ran in the hit's own frame: 59 or 60. The summed frame time stays in the test output as an observation, not an assertion. No other rule or tolerance changes.
