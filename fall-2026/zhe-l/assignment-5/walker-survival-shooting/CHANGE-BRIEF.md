# Change brief — Assignment 5: shaders, materials and the Godot shading language

> Version 1 — written 2026-10-29. After this commit version 1 is not rewritten; changes are appended, with dates, under "Revision history" at the end.
> This is the A5 specification (the "contract"): the A5 CLAUDE.md imports it with `@CHANGE-BRIEF.md`, and the agent works to it.
> The A2 / A3 brief is at `../../assignment-3/walker-survival-shooting/CHANGE-BRIEF.md`.
> Paths: `godot/…` in this file is the Godot project folder of this repository.

---

## Part 1: the screen-glow shader (code only, no textures)

### The state

- **What the effect communicates:** whether the tablet screen is on, that is, whether this character is holding the tablet and using it. When the tablet is held in one hand or both hands, the screen glows cold white; when the tablet is stowed on the hip, the screen is dark.
- **Why the player needs it:** the whole tablet is tied to the game's tablet gameplay; the details are in section 5.8 of my original design document (Chinese .docx, not in this repository). The points directly related to this effect: when the tablet is put away, "the tablet switches off and the screen shows nothing"; a power-on sound plays when it is taken out and a power-off sound when it is put away; the game does not pause while the tablet is open (to raise the difficulty, and to prepare for co-op later). So whether the screen is lit shows at a glance whether this tablet is on or off, that is, whether this character is using the tablet right now.
- **Which script and variable hold the state:** `_tablet_hold` in `godot/characters/human/humanoid/humanoid.gd` (type `enum TabletHold { NONE, ONE_HAND, TWO_HAND }`). Read from outside with `get_tablet_hold()`; after the state changes the signal `tablet_hold_changed(old_hold, new_hold)` is emitted. The state is changed only in `_apply_tablet_press()`.
- **Which object:** the screen plate of each tablet, the `Screen` node in `godot/items/tablet/tablet_device.tscn` (`MeshInstance3D`, a 0.18 × 0.108 m `QuadMesh`, 1 mm in front of the model's screen). Path on a character: `Humanoid/Visual/TabletDevice/Screen`. Obtained from outside with `TabletDevice.get_screen()`.

| `TabletHold` | Screen |
|---|---|
| `NONE` (tablet on the hip) | Dark (black) |
| `ONE_HAND` (held in one hand) | Lit once the tablet has moved to the hand slot |
| `TWO_HAND` (held in both hands in front of the eyes) | Lit once the tablet has moved to the slot in front of the eyes |

### The effect specification

**The shader:** `godot/shaders/pad_base_light.gdshader`, `shader_type spatial;`, `render_mode unshaded;` (no lighting is computed: the colour on screen is `ALBEDO`, independent of the scene's lights). Hand-written by me.

**Uniforms:**

| Name | Type | Hint | Default | What sets it |
|---|---|---|---|---|
| `cold_white` | `vec4` | `source_color` | `vec4(0.902, 0.969, 0.969, 1.0)` (= `#E6F7F7` = RGB 230, 247, 247, like the image of a modern night-vision device) | Not set by code; the shader's default is used (it can be tuned in the material's Inspector later) |
| `pad_light_data` | `float` | `hint_range(0.0, 1.0)` | `0.0` (dark) | The driver code, from `TabletHold` (see the rules below). Claude writes the driver and the test in Step 2, after I approve the plan |

**The colour line (inside `fragment()`):**

```glsl
ALBEDO = mix(vec3(0.0), cold_white.rgb, pad_light_data);
```

At `pad_light_data = 0` it is black, `vec3(0.0)`; at `= 1` it is `cold_white`; in between it is the proportional mix in linear space (`cold_white` has `source_color`, so it is converted from sRGB to linear before it reaches the shader).

**Screen-on strength:** I want the screen a little dim, so when the tablet is held `pad_light_data` is not set to 1 but to the screen-on strength **0.39** (as a percentage, 39%). This number is a feel parameter (code rule 1a): it lives in the driver's `@export var light_strength_percentage` (default 0.39) and is tuned in the Inspector, not in the shader.

**When it lights:** not when Tab is pressed and the state changes, but **at the moment the tablet reaches the hand slot**: the tablet comes off the hip, moves for `tablet_move_seconds` (0.35 s, `humanoid.gd`), and on the frame it reaches the hand slot (`TabletOneHandSlot` or `TabletTwoHandSlot`) `pad_light_data` goes straight from 0 to 0.39, with no fade. "Reached" = the tablet's move progress `_tablet_move_progress` in `humanoid.gd` reaching `TABLET_MOVE_DONE`.

**Observable rules:**

| Rule | Specification |
|---|---|
| Value when the state begins | At the moment of switching to `ONE_HAND` or `TWO_HAND`: `pad_light_data` is still 0.0; on the frame the tablet reaches the hand slot: 0.39 |
| Value when the state ends | At the moment of switching to `NONE`: `pad_light_data` becomes 0.0 at once (design document 5.8: "putting the tablet away: the tablet switches off"), without waiting for the tablet to get back to the hip |
| How long the change takes | The change itself is **instant** (from 0 to 0.39 within one frame, no fade). From the state becoming `ONE_HAND` / `TWO_HAND` to the screen lighting: `tablet_move_seconds` = **0.35 s** of game time, with a tolerance of one frame period (1/30 s at 30 fps, 1/60 s at 60 fps, 1/144 s at 144 fps). The same game time at 30 / 60 / 144 fps |
| The state begins again mid-transition | ① `ONE_HAND` ↔ `TWO_HAND`: the tablet is already in the hand and lit; while it moves between the two hand slots it **stays at 0.39, with no frame at 0** (ignore). ② The tablet is being put away (`NONE`) and Tab is pressed again to take it out: the tablet sets off again from where it is, takes the full 0.35 s again, and lights only when it reaches the hand slot (restart) |
| `Engine.time_scale` | The tablet move uses the physics frame's `delta`, which is multiplied by `Engine.time_scale`, so the 0.35 s is **scaled game time**: at time_scale = 0.5 it takes 0.7 s of real time to light |
| While the tree is paused | The game has no pause (design document 5.8: the game does not pause while the tablet is open). If the scene tree were paused (it never is in the game), the value keeps what it had before the pause |
| The state ends before the tablet reaches the hand | Taken out, then put away (back to `NONE`) before reaching the hand slot: the screen **never lights**; it stays 0.0 throughout |
| Several instances, each with its own value | Each tablet's `Screen` material is a `ShaderMaterial` with **`resource_local_to_scene` (Local To Scene)** ticked: every time `tablet_device.tscn` is instanced, Godot makes that instance its own copy of the material. Each character's driver sets only **its own** tablet's screen. When one character takes out its tablet, every other character's screen is unchanged |

**Boundaries (what this change does not touch):** collision, movement, input, the tablet state machine (the switching table in `_next_tablet_hold()`) and its timings (long press 0.4 s, tablet move 0.35 s), the existing test `godot/tests/a3_asset_check.gd` and its expected result (55 PASS), and every object except the tablet screen. Presentation code may read `TabletHold`; it never writes it (code rule 5).

**The evidence split:**

| Rule | Proved by | How |
|---|---|---|
| The shader parses; uniform names and types are right | Headless test | `get_shader_uniform_list()` checks both uniforms' names and types; no `SHADER ERROR` in the log |
| Start / end values, lit only on reaching the hand (0.35 s), no flicker on `ONE_HAND` ↔ `TWO_HAND`, never lit when put away before reaching the hand | Headless test | Switch the state through real key events; read `pad_light_data` every frame at 30 / 60 / 144 fps and record the game time when it first becomes 0.39 |
| Each tablet independent | Headless test | Two humanoid bodies in the scene, only one takes out its tablet: the other's value stays 0, and the two materials are not the same object |
| The screen colour is right | My eyes + captures | One capture per controlled value; sample the pixels below and compare them with my hand-computed predictions |
| In normal play | My eyes | Play normally several times — take out, put away, switch between one and two hands — and check that the boundaries hold |

### Controlled inputs and predicted values

**Three controlled values:** `pad_light_data` = **0.0**, **0.39** (the in-game screen-on value), **1.0** (set directly from code, to check that full strength is exactly `#E6F7F7`).

**Named pixels:**

| Pixel | Where | Expected |
|---|---|---|
| P1 | Centre of the screen | Changes with `pad_light_data` |
| P2 | A corner of the screen (a few pixels in from the edge) | Exactly the same as P1 (shows the whole screen is one even colour) |
| P3 | The bezel outside the screen (the tablet shell) | Unchanged at all three values (shows that only the screen changes) |

**The screen is `unshaded`, so P1 and P2 do not depend on the background or the lights.** The project does not enable HDR 2D; the `WorldEnvironment` in `base.tscn` sets no tonemapper, so it uses the defaults: Linear, exposure 1.0, glow off (confirmed on 2026-10-29 by reading the defaults of `Environment.new()` in a headless script). So the displayed value = `encode(ALBEDO)`, times 255, rounded.

**Hand calculation (done by me, 2026-10-29):** `cold_white` has `source_color`, so it enters the shader as the linear value (0.791, 0.930, 0.930). By the colour line, `ALBEDO = linear value × pad_light_data` (the other end of the `mix` is black). Displayed value = `encode(ALBEDO)` × 255, rounded, with `encode(x) = 1.055 · x^(1/2.4) − 0.055` (x > 0.0031308).
- 0.39: R 0.791 × 0.39 = 0.308 → encode = 0.591 → 151; G 0.930 × 0.39 = 0.363 → encode = 0.636 → 162.
- 1.0: converted there and back, so it is `#E6F7F7` itself.
- 0.0: black.

| `pad_light_data` | P1 / P2 predicted (R, G, B) | P3 |
|---|---|---|
| 0.0 | (0, 0, 0) | Unchanged |
| 0.39 | (151, 162, 162) | Unchanged |
| 1.0 | (230, 247, 247) | Unchanged |

Note: the result at 0.39 is not 230 × 0.39 ≈ 90, because the multiplication happens in linear space and the value is converted back to sRGB before display.

Before the captures, the debug `UpMarker` (the small black box above the tablet) must be deleted or hidden, or it will appear in the picture.

---

## Part 2: the hint experiment (to be added)

A 3×1 PNG (greys 64, 128, 192), sampled with and without `source_color` on `unshaded` quads, Linear tonemap, exposure 1.0. The project uses Forward+, so the predictions are for Forward+.

The predictions (each band's displayed 8-bit value on each quad, and which quad shows the file's values unchanged, and why) **will be added at the end of this file as a dated revision before the hint experiment is built**.

---

## Part 3: the crates' wear shader and its two materials (to be added)

Already decided:
- **Objects:** the two weapon crates `crate_cube` (small crate) and `crate_long` (large crate) in `godot/base.tscn`, models from `godot/assets/furniture/crate_cube.glb` and `crate_long.glb`. The materials go behind the importer's Use External setting so a reimport keeps them. The source model files are not changed.
- **Effect:** wear.
- **Shader:** spatial, in `godot/shaders/`, hand-written by me.

The rest of the material plan (what the wear looks like, the lighting it is judged under, the shader's file name, each texture's role / source / sampling / import settings, each uniform, and what differs between the two materials) **will be added at the end of this file as a dated revision before the crate shader is written**.

---

## Predicted failure cases and the checks that catch them

1. **One character takes out its tablet and every tablet lights up.** Cause: the `Screen` material lives in the prefab, so by default every instance shares the same one (a headless check during the tablet logic work printed `true`); Local To Scene was not ticked, or the driver changed the shared material. Check: a headless test with two humanoid bodies where only one takes out its tablet; the other's `pad_light_data` must stay 0, and the two materials must not be the same object.
2. **`source_color` is left off `cold_white`.** The shader would treat 0.902 as a linear value directly, and at full strength the screen would show about (244, 251, 251), whiter and paler than `#E6F7F7`. Check: a capture at `pad_light_data = 1.0`, where P1 must be (230, 247, 247); the test reads the shader source and checks the hint.
3. **The screen flashes black for a frame on `ONE_HAND` ↔ `TWO_HAND`.** For example, the driver sets 0 and then the screen-on value again, or only sets the value when taking the tablet out of `NONE`. Check: the test reads `pad_light_data` every frame across the switch; it must never be 0.
4. **The crates' data texture is sampled as colour (with `source_color`).** The data would be wrongly converted and the extent of the wear would change. Check: the material test reads the shader source and checks each sampler's hint; the mutation that removes `source_color` must fail.
5. **The screen lights as soon as Tab is pressed (without waiting for the tablet to reach the hand), or lights at different times at different frame rates.** Check: sample every frame at 30 / 60 / 144 fps; the game time at which it first becomes 0.39 must be 0.35 s ± one frame period.
6. **The tablet is put away before it reaches the hand, yet the screen flashes on.** For example, the driver looks only at "which slot the tablet is heading for", not at "whether it has arrived". Check: in the test, take the tablet out and put it away again after 0.1 s, sampling every frame; 0.39 must never appear.
7. **The debug `UpMarker` appears in a capture.** Check: before capturing, confirm it is deleted or hidden.

---

## Short answers

- **Which renderer does project.godot name, and what does it rule out?** Forward+ (`config/features` on line 15 of `project.godot` lists "Forward Plus", and no `rendering_method` is set). Forward+ supports decals, compute shaders, VoxelGI, SDFGI and SSIL, so none of these is ruled out.
- **What colour arrives in my fragment function before I change it, and what would the tempting alternative give me?** White: `COLOR` is the vertex colour, and the `QuadMesh` has no vertex colours, so it is white by default; the black of the old `StandardMaterial3D` does not reach my shader. Mixing from `COLOR` instead of from `vec3(0.0)` would make the screen white when it is off.
- **(The canvas_item question does not apply: both shaders are spatial.)**
- **For spatial: what does ALBEDO hold if I never write it, and what does COLOR hold?** `ALBEDO` is white by default; `COLOR` holds the vertex colour.
- **How long would a frame-counting version of my effect last at 30, 60 and 144 frames per second?** Counting a fixed 21 frames (exactly 0.35 s at 60 fps): 0.7 s at 30 fps, 0.35 s at 60 fps, about 0.146 s at 144 fps. The higher the frame rate the shorter it is, so it must be timed in game time, not counted in frames.
- **Which resource holds my uniform's default, which holds its current value, and what happens if two objects share the material?** The default is written in the shader, which will be at `godot/shaders/pad_base_light.gdshader`. The current value lives in the ShaderMaterial: the driver writes it into the material with `set_shader_parameter()`. Two objects that share one material share the same parameter values. I will tick Local To Scene, so that when there are several tablets in the scene, using the player character's tablet does not light every tablet.
- **Does hint_range clamp a value my driver sets from code? (Predicted now; checked in Use It.)** I predict it does **not** clamp: if the driver sets 2.0, the shader receives 2.0, `ALBEDO` = linear value × 2, all three channels go above 1, and the screen shows (255, 255, 255), pure white.

---

## Revision history

<!-- Append here; do not change version 1 above -->
- **2026-11-01 — Where "0.35 s" starts counting (found while writing the test; version 1 did not say):** Version 1 only says "from the state becoming `ONE_HAND` / `TWO_HAND` to the screen lighting, 0.35 s of game time", without saying which moment the timer starts at. Actual behaviour: the state changes in some physics frame, and the tablet **starts moving in that same physics frame** (`_update_tablet_visual()` in `humanoid.gd` runs after the state change, in the same frame); it takes 21 physics frames (60 per second, 21 × 1/60 = 0.35 s) to reach the hand, and the screen lights on the physics frame it arrives. So the timing rule is made explicit: **count from the physics frame in which the state changes, including that frame, up to the physics frame in which the screen lights**, i.e. (lit physics frame number − change physics frame number + 1) × game time per physics frame (1/60 s × `Engine.time_scale`), which equals 0.35 s ± one frame period. Counting instead "from the frame after the state change is seen" drops one frame and gives 0.333 s, which is outside the tolerance at 144 fps; that is only a different way of measuring, the game behaviour is unchanged. The test `tests/screen_glow_check.gd` times this way in `_lit_delay()`; measured at 30 / 60 / 144 fps: 0.3667 / 0.3500 / 0.3500 s (at 30 fps each rendered frame runs two physics frames, so the sample can read the change one physics frame late). The rule itself (0.35 s, a tolerance of one frame period, lit only on arrival) is unchanged.

### 2026-11-01 revision — Part 3: the material plan for the crate wear shader

> Completes "the rest of the material plan" that Part 3 of version 1 left for later. Written before the crate shader. All values decided by me on 2026-11-01.

**The objects and the surface to replace:** `crate_long` and `crate_cube` in `godot/base.tscn` (already chosen in version 1). Each `.glb` has two materials: the shell `Crate_OliveDrab` (olive drab; the lid uses it too) and the hardware `Crate_Hardware` (handles, latches). **Only the shell is replaced**; the hardware keeps the material it has in the `.glb`.

**What the wear looks like:** the outside of the crate is olive-drab paint; where it is worn, the paint has come off and shows **dark red rust** underneath, with silver metal scratches in the rust (what the Metal041C texture itself looks like).

**Texturing without UVs (found while checking the models on 2026-11-01):** `crate_long.glb` has no UVs at all; in `crate_cube.glb` the body has UVs but the lid does not. The source models are not changed (version 1), so the shader computes its own texture coordinates: in `vertex()`, depending on which axis the normal points along, it takes the other two components of the object-space position `VERTEX` as the UV (normal along X uses `zy`, along Y uses `xz`, along Z uses `xy`), then multiplies by `texture_scale`. All 336 normals of the two models point exactly along X / Y / Z (confirmed on 2026-11-01 by reading the `.glb` files with a script), so each face is projected from one direction only and no three-way blending is needed. Object space rather than world space, so the texture moves with the crate. Because UVs computed this way have no matching tangents, **the crate materials do not use a normal map**.

**The lighting I judge under:** the existing lighting in `godot/base.tscn`: 3 ceiling `OmniLight3D`s (`ceiling_light_1/2/3`), the `WorldEnvironment` ambient light colour (0.45, 0.5, 0.6) at energy 0.35, the default Linear tonemap, exposure 1.0 (version 1, line 85).

**The shader:** `godot/shaders/crate_wear.gdshader`, `shader_type spatial;`, no `render_mode unshaded` (it is lit by the scene). Hand-written by me.

#### Textures

All from one set: **Metal041C from ambientCG** (1K-PNG).

| Item | Content |
|---|---|
| Source URL | https://ambientcg.com/view?id=Metal041C (download: `https://ambientcg.com/get?file=Metal041C_1K-PNG.zip`) |
| Author / role | ambientCG is created and run by Lennart Demes (Münster, Germany; the site's imprint page https://docs.ambientcg.com/legal/); the asset page gives the technique as Procedural (generated procedurally, not a photo scan) |
| Licence | Creative Commons CC0 1.0 Universal (https://docs.ambientcg.com/license/); no credit required. The course requires provenance, so it is recorded in `ATTRIBUTION.md` next to the textures |
| Date checked | 2026-11-01 |
| Normal-map convention | The game uses only `NormalGL` (Godot uses the OpenGL convention); `NormalDX` is used only to calibrate the normal-map check |
| Not AI-generated | No model or prompt involved |

The files go in `godot/assets/shader/metal041c/`, keeping ambientCG's original file names.

| Texture | Used for | What its numbers mean | Sampled as | `compress/mode` | `compress/normal_map` | `mipmaps/generate` |
|---|---|---|---|---|---|---|
| `Metal041C_1K-PNG_Color.png` (RGB 8-bit) | Crate shader: the colour of the rust that shows where the paint has come off; Step 4 albedo | Colour, stored as sRGB | **Colour**, with `source_color` | 2 (VRAM Compressed) | 2 (Disabled) | true |
| `Metal041C_1K-PNG_Displacement.png` (greyscale 16-bit) | Crate shader: the wear mask | Surface height, 0 = lowest, 1 = highest; 8-bit after import | **Data**, without `source_color` | 0 (Lossless) | 2 (Disabled) | true |
| `Metal041C_1K-PNG_Roughness.png` (greyscale 8-bit) | Only in the Step 4 StandardMaterial3D | Roughness, 0 = smooth, 1 = rough | Data | 2 (VRAM Compressed) | 2 (Disabled) | true |
| `Metal041C_1K-PNG_NormalGL.png` (RGB 16-bit) | Step 4 normal map; the normal-map check | Tangent-space normals, OpenGL convention (green = up) | Data (`hint_normal`) | 2 (VRAM Compressed) | 1 (Enable) | true |
| `Metal041C_1K-PNG_NormalDX.png` (RGB 16-bit) | Only to calibrate the normal-map check; not used in the game | Tangent-space normals, DirectX convention (green flipped) | Not sampled by any material | 2 (VRAM Compressed) | 1 (Enable) | true |

Why Displacement is the mask rather than Roughness or Metalness (four maps compared on 2026-11-01): Roughness is almost all bright (107–227, standard deviation 19); Metalness is almost only pure black and pure white (87% of the pixels are 0); Displacement rolls continuously like clouds (0–252, standard deviation 53), so dragging the wear amount grows the worn area smoothly.

#### Parameters (uniforms)

The names are final when I write the shader; the table below is the plan.

| Group (`group_uniforms`) | Name | Type | Hint | Range | Default | What changes on screen across the range |
|---|---|---|---|---|---|---|
| — | `rust_albedo` | `sampler2D` | `source_color, filter_linear_mipmap, repeat_enable` | — | Both materials bind `Metal041C_1K-PNG_Color.png` | — |
| — | `wear_mask` | `sampler2D` | `filter_linear_mipmap, repeat_enable` (no `source_color`) | — | Both materials bind `Metal041C_1K-PNG_Displacement.png` | — |
| `paint` | `paint_color` | `vec4` | `source_color` | Colour | `vec4(0.260, 0.283, 0.190, 1.0)`: the model's current olive drab. The `.glb` stores the linear value (0.055, 0.065, 0.030); with `source_color` the default must be written as sRGB, which converts to RGB (66, 72, 48) | The paint colour where there is no wear |
| `paint` | `paint_roughness` | `float` | `hint_range(0.0, 1.0)` | 0–1 | 0.85 (the same as the model now) | Paint from glossy (0) to matte (1) |
| `wear` | `wear_amount` | `float` | `hint_range(0.0, 1.0)` | 0–1 | 0.1 (neither much nor little, about 10% rust) | 0 = all paint, 1 = all rust; in between the mask decides where rust shows first. Mask statistics: 0.1 → about 10%, 0.2 → about 23%, 0.3 → about 42%, 0.5 → about 75% |
| `wear` | `wear_softness` | `float` | `hint_range(0.0, 0.2)` | 0–0.2 (the mask values are mostly 0–0.6; a wider transition looks like dirt, not chipped paint) | 0.0 (a hard edge: it should feel like paint flaking off) | The boundary between paint and rust goes from a hard edge (0) to a gradual transition |
| `mapping` | `texture_scale` | `float` | `hint_range(0.1, 10.0)` | 0.1–10 (repeats per metre) | 2.0 (medium rust patches: about 12–16 cm, 2 texture repeats across the long crate's front) | How many times the texture repeats per metre: larger means smaller, denser rust patches |

5 non-texture parameters in 3 groups (the assignment requires at least 4 and at least 2 groups).

**The wear calculation (in words; the code is decided by me when I write the shader):** read the mask value, compare it with `wear_amount`, use `wear_softness` for the width of the transition, and get this pixel's wear w (0 = paint, 1 = rust); `ALBEDO` takes a value between `paint_color` and the rust colour by w, and `ROUGHNESS` likewise. **Rust shows in the low places first**: where the mask (height) is below the threshold becomes rust; the larger `wear_amount`, the higher the threshold, and the rust spreads from low to high. Reason: low places move less and rust more easily.

#### The two materials

Both `ShaderMaterial`s use `crate_wear.gdshader`, saved as `.tres` in `godot/assets/furniture/materials/`, and are pointed to from **Use External** on `Crate_OliveDrab` in each `.glb`'s advanced import settings, so a reimport keeps them.

| Material | Used on | `wear_amount` | `paint_roughness` | Other parameters |
|---|---|---|---|---|
| `crate_long_wear.tres` | `crate_long` | 0.2 (heavy, about 23% rust) | 0.95 (more matte) | Defaults (`texture_scale` the same on both crates) |
| `crate_cube_wear.tres` | `crate_cube` | 0.1 (light, about 10% rust) | 0.85 (the default) | Defaults |

Two values differ: `wear_amount` and `paint_roughness`; the textures are the same, and so is `texture_scale` (both crates are the same sheet metal). Why the long crate is more worn: it is bigger, so dragging it chips the paint more and it rusts more. Why its paint is rougher: it is dragged more, so the paint is worn more matte.

#### Evidence split

| Rule | Proved by | How |
|---|---|---|
| The shader parses; parameter names and types are right | Headless test | `get_shader_uniform_list()`; no `SHADER ERROR` in the log |
| The colour texture has `source_color` and the mask does not | Headless test | Read each sampler's hints from the shader source; the mutation that deletes `source_color` must fail (exit 1) |
| Both materials use the same shader, with different values and the right textures | Headless test | Load both `.tres` and compare shader path, parameter values and texture paths |
| The materials sit behind Use External | Headless test | Read `_subresources` in both `.glb.import` files with `ConfigFile` |
| The import settings are the planned values | Headless test | Read each texture's `.import` with `ConfigFile`; run again after deleting `.godot/` and reimporting |
| The normal map has a real surface behind it and the right convention | Headless test | `curl_ratio` in `tests/normal_map_check.gd`, for GL and DX, each under both conventions |

---

### 2026-11-01 revision — Part 2: the hint experiment's plan and predictions

**Files:**
- The script that writes the texture: `godot/tools/make_hint_greys.gd` (written by Claude, committed by me). It writes a 3×1 PNG, `godot/experiments/hint/hint_greys_3x1.png`, whose three pixels are the greys 64, 128 and 192 in that order (R = G = B).
- Import settings: `compress/mode` = 0 (Lossless), `mipmaps/generate` = false, `compress/normal_map` = 2 (Disabled).
- The shader: `godot/shaders/hint_experiment.gdshader`, `shader_type spatial;`, `render_mode unshaded;`, with two samplers both bound to this PNG: one `source_color, filter_nearest`, the other only `filter_nearest`; a `bool` parameter decides which sampler `ALBEDO` uses. Hand-written by me.
- Two materials (the `bool` true and false) on two `QuadMesh`es facing the camera. Scene: `godot/experiments/hint/hint_experiment.tscn`; its `WorldEnvironment` sets the Linear tonemap and exposure 1.0, with glow, fog and adjustments off.
- Renderer: Forward+ (version 1).

**Predictions (computed by me by hand):** displayed value = `encode(sampled value)` × 255, rounded; `encode(x) = 12.92x` (x ≤ 0.0031308), otherwise `1.055·x^(1/2.4) − 0.055`.

| Band (value in the file) | Quad with `source_color` | Quad without `source_color` |
|---|---|---|
| 64 | 64 | 137 |
| 128 | 128 | 188 |
| 192 | 192 | 225 |

Which quad shows the file's values unchanged, and why: **the quad with `source_color`** shows 64, 128, 192 unchanged. `source_color` makes the GPU decode sRGB → linear first, and the engine encodes linear → sRGB again before display; the two conversions are inverses of each other and cancel out. The quad without `source_color` is clearly brighter: the sRGB numbers in the file are wrongly taken as linear brightness and get one more sRGB encode, giving 137, 188, 225 (for example 64/255 = 0.251, `encode(0.251)` = 0.538, × 255 ≈ 137).

---

### 2026-11-01 revision — new failure cases for Part 3

(Version 1's case 4, "a data texture sampled as colour", still applies.)

8. **The colour texture without `source_color`.** The rust colour would be taken as linear values and show too bright and washed out. Check: the material test reads the hint from the shader source; the mutation that deletes `source_color` must exit 1.
9. **The material not behind Use External, or a wrong Use External path.** After a reimport (for example after deleting `.godot/`) the crates fall back to the `.glb`'s original plain material. Check: the test reads `_subresources` in the `.glb.import`; run the test again after clearing the cache and reimporting.
10. **Import settings left on Detect, rewritten by the editor the first time it draws the texture.** For example Displacement changed to another compression, which changes the mask values. Check: the test reads the three keys in the `.import` with `ConfigFile`; run `git status` after first opening the editor to see whether any `.import` was rewritten.
11. **Texture coordinates outside 0–1 without repeat on the sampler.** Most crate faces would show the texture stretched into stripes. Check: the test reads the shader source; both crate samplers must have `repeat_enable`.
12. **A normal map in the wrong convention (DX used as GL).** Check: `curl_ratio` near 2 under the wrong convention.

### 2026-11-01 revision — the rust roughness and the minimum transition width (before writing `fragment()`)

The material plan above says "`ROUGHNESS` likewise", but the parameter table only has the paint's roughness and does not say where the rust's roughness comes from. Two **named constants** are added (`const`, written in `crate_wear.gdshader`; not uniforms, so the parameter table is unchanged and still has 5 entries):

| Constant | Value | What it does | Why it is a constant |
|---|---|---|---|
| `RUST_ROUGHNESS` | 0.79 | The rust's roughness: `ROUGHNESS` takes a value between `paint_roughness` and this by the wear w | My option A: fastest, no extra parameter. 0.79 is the mean of Metal041C's own Roughness map (200.9 / 255, measured with a script on 2026-11-01) |
| Minimum transition width (name chosen by me when writing the shader) | 0.001 | `wear_softness` and this, whichever is larger, is used in `smoothstep` | `wear_softness` defaults to 0, and then the lower and upper edges of `smoothstep` are equal, which GLSL leaves undefined; 0.001 is too small to see, so the effect is still a hard edge. It is a structural constant and is never tuned |
