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
