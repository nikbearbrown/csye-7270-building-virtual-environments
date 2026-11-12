# CHANGE-BRIEF — Assignment 6: landing dust + dust under the ceiling light

> Translated from the Chinese original in my working folder. This file replaces my Assignment 5 brief; the A5 version stays in history at tag `zhe-l-a5`.
> This file is committed before the first agent prompt. After that the original text is not changed; dated revisions go in "Revision history" at the end.
> Who wrote what: the intent, the rules, the evidence split, the predicted failures and the short answers are mine. The initial values were proposed by Claude from my intent; I checked them and adopted them (2026-11-09, "use this version first"). Claude assembled my answers into this file.

## Shared facts

| Item | Value | Source |
|---|---|---|
| Godot version / renderer | 4.7.2-stable, Forward Plus, D3D12, Jolt Physics | `godot/project.godot` |
| Window size | 2048 × 1152 | `godot/project.godot` |
| Main character | 1.6 m tall, capsule diameter 0.6 m, origin at the feet | `godot/characters/human/humanoid/humanoid.tscn` |
| Jump | Take-off speed 4.5 m/s, gravity 9.8 m/s²; one standing jump is about 0.92 s in the air | `godot/characters/human/humanoid/humanoid.gd` |
| Base floor | The floor surface is at world Y ≈ 0.25 m | `godot/base.tscn` |
| Base lighting | Background colour (0.03, 0.035, 0.045); ambient light (0.45, 0.5, 0.6), energy 0.35; 3 ceiling lights, OmniLight3D (0.78, 0.86, 1.0), energy 1.5, range 8 m; light 1 at (0, 2.6, -3.7) | `godot/base.tscn` |
| Ceiling-light switch | `CeilingLights`: signal `lights_changed(lights_on)`, query `is_lights_on()`; the wall switch is pressed with F; the lights are on at scene load | `godot/world/lights/ceiling_lights.gd`, `godot/world/light_switch/light_switch.gd` |

---

## Effect A: landing dust

### The job
- What it tells the player: it clearly signals that the character has touched the ground, helps the player judge when the jump has ended, and adds weight to the landing.
- Event: the player lands (the frame the body comes back to the floor from the air). Owned by `humanoid.gd`: a new signal `landed`, emitted once on the frame `is_on_floor()` changes from false to true. It only notifies; it changes no movement, velocity or other state.

### Intent
- **Timing phases:**
  - the dust is clearly visible within 0.10 s of landing and at its strongest at about 0.15 s;
  - then it fades slowly, the second half is mostly a very faint remainder, and it is completely gone at 1.60 s;
  - the ground wave spreads to its final size in 0.30 s and is completely gone at 0.45 s.
- **Contrast against the background:**
  - first check the bright background on the open floor near ceiling light 1, then the dark background at the front of the room, near the shadows of the furniture.
  - These are only candidate places to check. I cannot claim they are the brightest and darkest places in the whole scene; that has to be confirmed in the real picture.
- **Scale against the character:**
  - including the quads, the height stays within 0.10 m above the floor (ankle height only);
  - the dust's final overall diameter is about 0.90 m, 1.5 times the character's capsule diameter;
  - the ground wave's final outer diameter is 0.90 m, and it stays very thin and very faint.
- **Change over life:**
  - the dust's hue stays essentially the same; it appears quickly, then fades slowly, and each quad grows gradually;
  - the ground wave grows from a small ring while its opacity keeps falling.
- **Colour:** the dust is a low-saturation grey-brown, base RGB (0.48, 0.45, 0.40); the ground wave is a lighter grey-brown, (0.62, 0.59, 0.53).
- **Variation:**
  - the dust's spawn position, horizontal spread direction, speed, size and initial rotation are random; the colour stays the same;
  - the ground wave's size and timing are fixed, so the landing cue is steady.
- **Layering:** two emitters under one root node:
  1. `Dust`: the dust;
  2. `GroundRing`: a ring lying flat on the floor. It does not spread far (this is not an explosion); it only stresses "you have landed".

### Settings (scene file `godot/effects/landing_dust.tscn`)
- **Node type:**
  - root node `Node3D`, with two `GPUParticles3D` under it;
  - reason for GPU: neither effect is hard to compute.
- **Placement:** the effect lives in the world, not under the player, at the landing point. The ground wave is raised about 0.01 m above the landing point so it does not z-fight with the floor.

**`Dust`**
| Part | Setting | Value |
|---|---|---|
| Emission | amount / one_shot / explosiveness | 24 / true / 1.0 |
| Emission | lifetime / lifetime_randomness | 1.6 / 0.2 |
| Emission | emission_shape | RING: emission_ring_axis (0,1,0), emission_ring_radius 0.2, emission_ring_inner_radius 0.05, emission_ring_height 0 |
| Process | direction / spread / flatness | (1,0,0) / 180 / 1.0 |
| Process | initial_velocity_min / max | 0.6 / 0.9 |
| Process | damping_min / max | 1.4 / 1.8 |
| Process | gravity | (0, 0, 0) |
| Process | angle_min / max | 0 / 360 |
| Process | scale_min / max; scale_curve | 0.8 / 1.2; 0.6 → 1.0 |
| Process | color; opacity (color_ramp) | (0.48, 0.45, 0.40); 0 s → 0, 0.15 s → 0.6, 0.8 s → 0.15, 1.6 s → 0 |
| Draw | draw_pass_1 | QuadMesh 0.08 × 0.08 m; the emitter sits 0.04 m above the landing point |
| Draw | Material | StandardMaterial3D: shading_mode unshaded, transparency alpha, vertex_color_use_as_albedo on, billboard_mode PARTICLES, albedo_texture a round soft-edged GradientTexture2D; the node casts no shadow |
| Coordinates | local_coords | false: when the player walks off after landing, the dust stays at the landing point and keeps fading |
| Visibility | visibility_aabb | set by hand to position (-0.6, -0.1, -0.6), size (1.2, 0.3, 1.2), then checked |
| Preprocess | preprocess | 0 (a landing effect does not need to run in advance) |

**`GroundRing`**
| Part | Setting | Value |
|---|---|---|
| Emission | amount / one_shot / explosiveness | 1 / true / 1.0 |
| Emission | lifetime / lifetime_randomness | 0.45 / 0 |
| Process | initial_velocity / gravity | 0 / (0, 0, 0) |
| Process | scale_curve | 0 s → 0.2, 0.30 s → 1.0, then stays at 1.0 |
| Process | color; opacity | (0.62, 0.59, 0.53); 0.35 → 0, falling linearly the whole time |
| Draw | draw_pass_1 | QuadMesh 0.9 × 0.9 m, orientation FACE_Y (lying flat), 0.01 m above the landing point |
| Draw | Material | StandardMaterial3D: unshaded, transparency alpha, vertex_color_use_as_albedo on, billboard off, albedo_texture a ring GradientTexture2D (transparent centre, one thin bright band near the outer edge); the node casts no shadow |
| Coordinates | local_coords | false |
| Visibility | visibility_aabb | set by hand to position (-0.5, -0.05, -0.5), size (1.0, 0.1, 1.0), then checked |
| Preprocess | preprocess | 0 |

### Observable rules
- It fires on every landing and never otherwise (including on scene load), at the landing point.
- **Retrigger rule: restart.** If the player lands again before the old effect has finished, the second landing clears the old effect and plays again at the new landing point; both emitters replay. So at most 1 burst is alive at once, and the peak particle count = 24 + 1 = 25. The code must use `restart()`, not just set `emitting = true`.
- If the node Effect A would follow is freed: not applicable. The effect lives in the world, not under the player, and the player is not freed on landing.

### Frame strip
- Preview background: the open floor near ceiling light 1 in the base (bright), and the front of the room, near the shadows of the furniture (dark).
- 30 fps, trigger at frame 10; read frames 10, 12, 15, 20, 30 and 50. The lifetime of 1.6 s is longer than 1.3 s, so frames 58 and 60 are read as well.
- Retrigger: a second landing at frame 25 (inside the first burst's lifetime), about 0.5 m away from the first so the old and new bursts can be told apart. Read frames 25, 27, 30 and 35. `--quit-after 80`.
- The two are captured separately, once each: with the preview's retrigger switch off, it triggers only at frame 10, and I read frames 10–60 in the table below; with it on, it triggers at frames 10 and 25, and I read the last 4 rows of the table. If both were captured in one run, the first burst would be cleared at frame 25, and frames 30–60 would not show the first burst. So one capture shows the whole fade, and one shows the retrigger.
- What each frame should show (the "state worked out from the values" column was converted from the values above by Claude; the "my prediction" column is mine):

| Frame | Since trigger | State worked out from the values (dust / ground wave) | My prediction of what the picture shows |
|---|---|---|---|
| 10 | 0 s | Trigger frame; the particles may not appear until frame 11 | The dust is just starting at the feet; it may not be visible on this frame and may only appear on the next one. |
| 12 | 0.067 s | Dust opacity about 0.27, spread out by about 0.05 m / wave diameter about 0.34 m, opacity about 0.30 | A little faint dust comes up beside the feet and spreads outward along the floor; a small ring can be seen on the floor. |
| 15 | 0.167 s | Dust near its strongest (about 0.59), spread about halfway / wave diameter about 0.58 m, opacity about 0.22 | The dust beside the feet is at its most visible, gathered into a small cloud, only up to the ankle. The ring on the floor has grown too, but it is fainter than the dust. |
| 20 | 0.333 s | Dust about 0.47, spread almost to its full range / wave at its final outer diameter of 0.90 m, opacity about 0.09 | The dust has spread out and is not as thick beside the feet as before. The ring on the floor has reached its largest size, and only a very faint edge is left. |
| 30 | 0.667 s | Dust about 0.24, no longer spreading, overall diameter about 0.9 m, quads about 25% larger than at birth / wave already gone (at 0.45 s) | The ring on the floor can no longer be seen; only a thin layer of dust is left near the landing point, and it has not spread any further. |
| 50 | 1.333 s | Dust about 0.05, only a very faint remainder; the particles whose lifetime was shortened at random are gone / — | Only a few specks of dust are left; you can hardly see them unless you look closely. |
| 58 | 1.6 s | The dust has just all gone / — | The dust has all gone, and the floor looks as it did before. |
| 60 | 1.667 s | Nothing / — | There is no dust and no ring on the floor, and no new cloud comes up. |
| 25 (retrigger) | new 0 s, old 0.5 s | The old burst (opacity about 0.36 at this point) is cleared; the new burst is triggered at the new position | The old cloud is cleared before it has finished fading. Dust starts again at the new landing point next to it; the new cloud may only be visible on the next frame. |
| 27 | new 0.067 s | Same as frame 12, but at the new position; no dust at the old position | Faint dust and a small ring appear at the new landing point; the old cloud does not stay behind to fade slowly. |
| 30 | new 0.167 s | Same as frame 15, at the new position | The dust at the new landing point is at its most visible, and the small ring on the floor is growing; there is only the new cloud in the picture. |
| 35 | new 0.333 s | Same as frame 20, at the new position | The new cloud has spread out, and the ring on the floor has reached its largest size and is almost invisible; the old cloud has not come back. |

---

## Effect B: dust under the ceiling light

### The job
- Job: ambience.
- What it tells the player: it shows dust hanging in the air of the base, adds to the sense of an old, worn space, and makes the area lit by the ceiling light easier to notice once the light is on.
- Condition: the ceiling lights are on. Owned by `CeilingLights`:
  - signal `lights_changed(lights_on)`;
  - at scene load, `is_lights_on()` is queried once for the initial state (the lights are on at the start).
- **Features Effect A doesn't use:**
  - a box emission shape;
  - light turbulence;
  - an opacity ramp with several rises and falls, combined with random lifetimes;
  - additive blending (ADD).
- The "reflection" here is a visual simulation: the ramp makes each particle brighten and darken several times in its life, and the differences in lifetime and birth time keep them out of step. It does not compute each speck's real reflection angle.
- In the first version the draw material is not lit; showing and hiding the effect is controlled entirely by the light state.

### Intent
- **Where:** in the first version, only under ceiling light 1, with one emitter. The emission box's full size is 1.80 × 1.60 × 1.20 m, centred for now at world position (0, 1.45, -3.20).
- **Timing phases:**
  - at the start and whenever the light is switched on again, preprocess runs, so the first visible rendered frame already shows a steady distribution;
  - when the light is switched off, the effect becomes invisible at once and stops emitting. Because this layer shows dust lit by the lamp, it does not keep glowing after the light is off.
- **Contrast against the background:**
  - first check it against the wall behind ceiling light 1, then turn to a brighter, lit wall;
  - the specks should be recognisable against both the dark and the bright background; against the bright background they may be less noticeable;
  - the exact darkest and brightest places are confirmed in the running game.
- **Scale against the character:** quad diameter 0.006–0.012 m, about 1/267 to 1/133 of the main character's height.
- **Colour:** a fixed cool white, base RGB (0.78, 0.86, 1.0); only brightness and opacity change.
- **Variation:** everything except the colour is random: spawn position, direction, speed, size, lifetime and drifting path.
- **Layering:** one emitter, because there is only one thing here: dust.

### Settings (scene file `godot/effects/light_dust.tscn`)
- **Node type:** one `GPUParticles3D`, for the same reason as Effect A; also, only GPU nodes have turbulence.

| Part | Setting | Value |
|---|---|---|
| Emission | amount / one_shot / explosiveness | 150 / false / 0 |
| Emission | lifetime / lifetime_randomness | 6.0 / 0.5 |
| Emission | emission_shape | BOX: emission_box_extents (0.9, 0.8, 0.6) |
| Process | direction / spread | random / 180 |
| Process | initial_velocity_min / max | 0.01 / 0.04 |
| Process | gravity | (0, 0, 0) |
| Process | turbulence | turbulence_enabled on; turbulence_noise_strength 1.0; turbulence_noise_scale 4.0; turbulence_influence_min / max 0.02 / 0.06 |
| Process | scale_min / max | 0.5 / 1.0 (quads 0.006–0.012 m) |
| Process | color; opacity (as a fraction of life) | (0.78, 0.86, 1.0); 0 → 0, 0.10 → 0.6, 0.25 → 0.15, 0.40 → 0.9, 0.55 → 0.2, 0.70 → 0.7, 0.85 → 0.1, 1.0 → 0 |
| Draw | draw_pass_1 | QuadMesh 0.012 × 0.012 m |
| Draw | Material | StandardMaterial3D: unshaded, blend_mode ADD, transparency alpha, vertex_color_use_as_albedo on, billboard_mode PARTICLES, albedo_texture a round soft-edged GradientTexture2D; the node casts no shadow |
| Coordinates | local_coords | false: the dust belongs to this space in the world and does not follow anything |
| Visibility | visibility_aabb | set by hand to position (-1.1, -1.0, -0.8), size (2.2, 2.0, 1.6), one size larger than the emission box because turbulence carries specks out of it; checked after setting |
| Preprocess | preprocess | 6.0 |

### Observable rules
- It starts when the light is on and stops when the light is off (invisible at once after the light goes off, and it stops emitting).
- The lights are on at scene load, so Effect B already shows a steady distribution on its first visible frame; it must not start empty.
- While the tree is paused: the specks' positions, ages and brightness changes are frozen. The game has no pause feature yet, so the test sets `get_tree().paused = true` directly to check it.
- While the node is hidden: it stops and its old progress is thrown away; when it is shown again with the light on, it preprocesses again.
- It is not a feedback loop, so amount_ratio does not apply.
- Peak particle count = 150.

### Frame strip
- Preview background: the wall behind ceiling light 1 (dark), and a brighter, lit wall (bright).
- 30 fps. The evidence split says "Effect B's start-up preprocess, the paused freeze, and the picture after hiding and showing again" are checked by frame strip, so the strip also includes pausing and hiding. The timing:
  - frame 10: light on;
  - frame 45: pause; frame 55: unpause;
  - frame 60: hide; frame 65: show again;
  - frame 70: light off;
  - `--quit-after 100`.
- Note: the preview scene starts with the light off. This is a test fixture; in the game the light is on when the scene loads. "A steady distribution on the first frame after scene load" is checked by eye in the running game. The preview starts with the light off so the change before and after switching it on is easy to see.
- What each frame should show (the "expected state from the settings" column was worked out by Claude from the rules above; the "my prediction" column is mine):

| Frame | What happens | Expected state from the settings | My prediction of what the picture shows |
|---|---|---|---|
| 9 | Light still off | No dust | No dust can be seen under the light. |
| 10 / 11 | Light switched on | After 6 s of preprocess, the first visible frame already shows a steady distribution (not filling up slowly from empty) | As soon as the light comes on, some tiny cool-white specks of dust can be seen scattered in the air, some bright and some dark, without waiting for them to build up. |
| 40 | 1 s after the light came on | Steady: about as many as on frame 11, but the specks' positions and brightness have changed | The dust is still sparse and scattered; some specks have brightened a little, some have dimmed, and they have moved slightly; it has not kept building up. |
| 46 / 54 | Paused | The two frames are identical: positions and brightness are frozen | The dust seems to hang still in mid-air. Comparing the two frames, each speck's position and brightness are unchanged. |
| 57 | After unpausing | Drifting and twinkling again | The dust starts drifting slowly again, and its brightness keeps changing; it no longer stays where it was. |
| 61 | Hidden | No dust | The light is still on, but the dust can no longer be seen at all. |
| 66 | Shown again | Preprocessed again, a steady distribution at once | As soon as it is shown, the dust is already spread out under the light; it does not build up from a few specks, and it does not carry on drifting from where it was before it was hidden. |
| 69 | The frame before the light goes off | Steady distribution | There are still tiny specks of dust under the light, drifting sparsely; some a little brighter, some almost invisible. |
| 71 | After the light goes off | Invisible at once | The light goes out, and the glowing specks disappear with it; no bright points are left fading slowly. |
| 90 | 0.67 s after the light went off | Still no dust | Still no dust can be seen under the light, and no leftover bright points come back. |

---

## Boundaries
- Collision, movement, input, the state machine and its timings, the expected values of the existing tests, my Assignment 5 shaders (`godot/shaders/`), and every other object stay unchanged. The light switch and `CeilingLights` stay unchanged too.
- Presentation code may read game state; it never writes it.
- The only game-script change allowed: a notify-only `landed` signal added to `humanoid.gd` (agreed by me, 2026-11-10).
- Effect settings live in scene files in `godot/effects/`, not in code.

## Baseline (before A6)
- Results through `scripts/run-test.sh` (the A6 version): `a3_asset_check.gd` at 60 fps, 55 passed; `screen_glow_check.gd` at 30 / 60 / 144 fps, 24 passed each; `normal_map_check.gd` at 60 fps, 2 passed; `test_materials.gd` at 60 fps, **168 passed, 1 failed** (exit code 1). No log contains `SHADER ERROR` or `SCRIPT ERROR`. Logs: `logs/`.
- The reason for that one failure: `test_materials.gd` counts every Light3D in `base.tscn` and expects 3. The extra one is `ScreenTabletLight`, which I added after A5 inside the on-screen tablet's SubViewport (in `player.tscn`). The checks on the three ceiling lights themselves all pass.
- A6 agrees not to change the expected values of existing tests, so this existing failure stays, with its reason noted. When A6 is finished, I check that there are no new failures, and I still report "168 passed, 1 failed" honestly, never as all passing.

## Evidence split

| Rule to check | How it is checked |
|---|---|
| Configuration: node types, amounts, lifetimes, material switches | Headless configuration test |
| Fires only on landing, no false trigger at the start, one notification per landing | Headless event test |
| Light-state connection, initial-state query, control state after hiding | Headless logic test |
| Dust height, spread size, colour, opacity, duration | Rendered frame strip |
| The second landing really clears the old effect and plays again | Event test + rendered retrigger frame strip |
| Effect B's start-up preprocess, the paused freeze, the picture after hiding and showing again | Rendered frame strip |
| Whether it reads clearly from the normal view, whether it covers the character, whether it is too bright | Checked by eye in the running game |
| Whether the performance meets the budget | Frame time measured on a real GPU render |

A headless test can prove the configuration and the control logic; it cannot prove the final GPU picture is right.

## Predicted failures

| Predicted failure | How it is caught |
|---|---|
| A wrong or outdated property name is used, and the setting does not take effect | Load-error log + reading the properties back |
| vertex_color_use_as_albedo is left off, so the colour ramp has no effect | Configuration test + frame strip |
| The draw material does not handle transparency correctly, so the fade has no effect | Configuration test + frame strip at the end of the lifetime |
| visibility_aabb is too small, so the particles suddenly vanish when the camera turns | Moving and turning the camera in the running game |
| Effect B's preprocess does not take effect, so it starts empty | Screenshot of the first frame |
| Effect A only sets emitting = true, so the second landing does not replay | Two-landing event test + retrigger frame strip |

## Price predictions and budget

| Effect | Peak particle count | Predicted headless CPU price | Predicted GPU time | Budget (compared on) |
|---|---|---|---|---|
| A landing dust | 25 | Almost the same as the empty-scene control, within 0.05 ms | about 0.05 ms | ≤ 0.2 ms (GPU time) |
| B dust under the light | 150 | Almost the same as the empty-scene control, within 0.05 ms | about 0.1 ms | ≤ 0.3 ms (GPU time) |

Both effects are GPU nodes, so their headless CPU price is near zero by construction, and their budgets are compared on GPU time. GPU used for the GPU price: NVIDIA GeForce RTX 5070 Ti Laptop GPU (the laptop's discrete GPU; before measuring, I confirm in Godot's start-up output that it is this GPU and not the integrated one).

## Short answers

1. **Node types, and the features they lack:**
   - Both effects use `GPUParticles3D`; Effect A has two emitters, Effect B has one.
   - The node itself knows nothing of "the character landed", "the ceiling-light switch" or "how to recover after being hidden"; presentation code has to listen to the events and control it.
   - Movement and lifecycle are configured by the `ParticleProcessMaterial`; the look is configured by the draw mesh, the texture and the material.
2. **`local_coords` and the player walking off:** both of Effect A's emitters are set to `false`. When the player walks off after landing, the dust stays at the landing point and keeps fading; on the next landing, the old effect is cleared and the new effect plays at the new position.
3. **How many bursts at once:** under restart, at most 1 burst at once; peak particle count = 24 + 1 = 25.
4. **Headless price and VSync:**
   - An ordinary headless run does not do real GPU drawing, so GPU time may read 0 or be unavailable; that does not mean the effect is free in a real run. The CPU still runs the related scripts.
   - With ordinary VSync on, on a 60 Hz display, and if both cases can reach the refresh rate, both effect off and effect on may read about 60 FPS. So GPU time should be compared, not FPS alone.
5. **Effect B on the first frame, while paused, while hidden:**
   - With 6 s of preprocess: on the first visible frame the distribution is already steady. Without it: it starts empty or with very few particles, and the distribution builds up gradually.
   - While paused: positions, ages and brightness changes are frozen.
   - While hidden: it stops as defined above and its old progress is thrown away; when it is shown again with the light on, it preprocesses again.
6. **Which settings belong to emission, process and draw:**

| Part | Settings in this brief |
|---|---|
| Emission | Amount, one-shot or continuous emission, how concentrated the emission is, spawn region, initial velocity and lifetime |
| Process | Gravity, turbulence, motion changes, the scale curve, colour and opacity over life |
| Draw | Quads, round or ring textures, facing the camera, transparent or additive blending, lighting, shadows |

preprocess is a simulation start-up setting, and `local_coords` is a coordinate-space setting; `visibility_aabb` decides when the effect counts as inside the visible range.

## Unconfirmed (handed to the "Unconfirmed" section of CLAUDE.md and to checks in the running game)
- Whether `restart()` runs preprocess again (this decides whether Effect B is full at once when the light is switched on again or the node is shown again).
- Whether a hidden `GPUParticles3D` keeps simulating in 4.7.2.
- 4.7.2's `ParticleProcessMaterial` still has a property named `initial_velocity` (found with ClassDB on 2026-11-09), so the "rename to the Godot 3 property name" mutation may not fail; the reason has to be found.
- Effect B's specks are only about 3 pixels across at 4 m from the camera; they may be too small to see.

---

## Revision history

### 2026-11-11 — Effect A intent changed to "grey cloud puffs" (before Step 4)
- **Why:** in the r0 frame strips and in the game, the dust I saw was a scatter of small dots and did not read clearly. What I want is puffs of dust that look like small grey clouds (see the r0 section of TUNING.md). The old intent capped the dust at "0.10 m including the quads (ankle height only)" and used 5–10 cm quads, which cannot make cloud puffs, so the intent changes first and the tuning starts after.
- **These intent items are replaced (the rest of the intent is unchanged):**
  - **Height:** at most about 0.30 m, mid-calf, measured to the **visible top edge** of the dust cloud. Replaces "including the quads, the height stays within 0.10 m above the floor (ankle height only)".
  - **Size of one puff:** about 0.18–0.25 m across when it is most visible, a little bigger than a fist, with a soft outline.
  - **Number of puffs:** about 6–8 per landing. Neighbouring puffs may partly overlap, with small gaps between puffs.
  - **Colour:** neutral grey, without the clearly warm brown it has now. On the base's grey-blue floor, it is enough that the outline of the puffs can be seen. Replaces the dust's "low-saturation grey-brown, base RGB (0.48, 0.45, 0.40)".
  - **Timing:** still most visible at about 0.15 s and fully gone at 1.6 s. New: at 0.7 s a few faint grey puffs can still be seen, and after that they slowly clear away.
  - **Ground ring:** keep its current size and spread timing; it stays a thin, faint ring. If on screen it draws the eye more than the dust cloud, make it fainter.
- **Unchanged:** the overall diameter of about 0.90 m, the two layers (`Dust` + `GroundRing`), the ground ring's colour, the restart retrigger rule, `local_coords`, the event and every testable rule.
- **The settings tables:** the values in the "Settings" tables above stay as they are for now. Step 4 changes one setting at a time; each change that is kept gets its own dated revision here, with that setting's old and new value, and the matching expected value in the configuration test changes with it.
- **Configuration check affected:** "Dust top including quads = 0.088 m <= 0.10 m" was written from the old intent. It is changed to the new 0.30 m limit only once the first revision that changes the height or the quad size is kept; it is not loosened in advance to make a test pass.

### 2026-11-12 — Effect A, kept revision r1: `Dust` quad size
- **Setting:** `Dust` `draw_pass_1` QuadMesh `size` (0.08, 0.08) → **(0.32, 0.32)**, in the `Dust` settings table above. Kept by me after r1 (see TUNING.md, revision r1).
- **Height check:** with this change the configuration test's height limit becomes the revised intent's 0.30 m (was 0.10 m), as the 2026-11-11 revision said. The quad top is now 0.04 + 0.32 × 1.2 / 2 = 0.232 m. The test measures the quad top, which is an upper bound on the visible top edge.
- **Not changed yet:** amount, emission ring radius, colour, opacity ramp, emitter height. Each is a later revision of its own.

### 2026-11-12 — Effect A colour intent back to "low-saturation, slightly warm grey"
- **Replaces** "Colour: neutral grey, without the clearly warm brown it has now" in the 2026-11-11 revision. The dust colour's intent is back to a low-saturation grey with a slight warmth, base RGB still (0.48, 0.45, 0.40), so the scene and the configuration test do not change.
- **Why:** in the game I cannot see much difference between the beige and a neutral grey. Claude adds: in the r1 comparison the agent said the dust is seen mainly through this slight warmth, not through a difference in brightness; a neutral grey of the same brightness might be harder to see on the grey-blue floor (not verified with a capture).

### 2026-11-12 — Effect B intent changed to "dust through the whole room, lit by the lights" (before Step 4)
- **Why:** after Effect B was wired into the game I saw in the game that I have to get close to the light to see any particles; I want the effect to be wider and bigger, so that the dust does not catch the light only right under the lamp. I also looked at an amount of 90 (my words are in TUNING.md, Effect B r0): "At 150, anyone would think a nuclear war had broken out. Make it 90; dust that dense makes the air feel strange."
- **These intent items are replaced (the rest is unchanged):**
  - **Where:** was "the first version is only under ceiling light 1, emission box 1.80 × 1.60 × 1.20 m". Now the dust fills **the whole room**, with an emission box covering roughly the room's interior (Claude's estimate from `base.tscn`: centre about (0, 1.6, 0), full size about 14 × 2.6 × 9 m). Still one emitter.
  - **Brightness:** was "the first version's draw material is not lit". Now the dust is **lit by the lights**: it takes light from the three ceiling lights, bright near a light where the light is strong, fainter farther away, and nearly invisible in the dark. I chose "lit by the lights", not "brighter in the dark".
  - **Density:** sparser than now. I looked at 90 particles in the small box under light 1 (about 26 per cubic metre) and found it right; how many the whole room needs is to be decided while tuning, by looking in the game.
  - **Size:** the specks vary in size, over 0.003–0.03 m (my words: "I mean 0.003–0.03"). Replaces "quad diameter 0.006–0.012 m".
- **Unchanged:** the condition is still "the ceiling lights are on" (all three lights go on and off together from one switch); after the lights go off the dust is invisible at once and stops emitting; preprocess at start and on every lights-on, so the first visible frame is a settled spread; frozen while paused; stopped when hidden and preprocessed again when shown; cool white (0.78, 0.86, 1.0); the opacity ramp that rises and falls; turbulence; ADD blending.
- **The settings table:** its values stay as they are for now. Step 4 changes one setting at a time; each change that is kept gets its own dated revision here, and the matching expected value in the configuration test changes with it. Expected order (Claude's suggestion): amount 150 → 90; lit material; a larger emission box (with the amount raised to match); a larger `visibility_aabb`; speck size.
- **What this affects (Claude's notes):**
  - The particle peak and the cost prediction (150, ≤ 0.3 ms) need a new estimate; Step 7 measures it.
  - The emission box centre moves from under light 1 to the middle of the room, so the position of `LightDust` in `base.tscn` (now (0, 1.45, −3.2)) has to follow, or an emission offset in the process material is used; this is decided in that round.
  - The strip's backgrounds and preview camera need choosing again, since the dust is no longer only under light 1.

### 2026-11-12 — Effect B, kept revision r1: `amount`
- **Setting:** `LightDust` `amount` 150 → **90**, in the Effect B settings table above. Kept by me after r1 (see TUNING.md, Effect B revision r1). The particle peak is now 90.

### 2026-11-12 — Effect B redesign: settings for "the whole room, lit by the lights"
- **Why:** the Effect B intent revision above (whole room, lit, sparser, specks 0.003–0.03 m). I am fairly sure of these changes and asked for them to be made at once rather than one setting per tuning round; if the result is bad in the game, they are reverted. So this is a redesign of the settings table, not a tuning revision. Applied by Claude Code (the review session), not by a prompted agent.
- **Settings changed in the Effect B table** (old → new):
  - `amount`: 90 → **3000** (about 9 per cubic metre over the 330 m³ box; a first value, to be judged in the game; the lit material makes far specks faint, so it is sparser than the 26 per cubic metre of the small box);
  - `emission_box_extents`: (0.9, 0.8, 0.6) → **(7, 1.3, 4.5)**, so the full box is 14 × 2.6 × 9 m;
  - new: `emission_shape_offset` **(0, 0.15, 3.2)**, which moves the box from the `LightDust` node at (0, 1.45, −3.2) in `base.tscn` to the room centre (0, 1.6, 0); the node itself does not move, so `base.tscn` and the state test do not change;
  - `scale_min` / `scale_max`: 0.5 / 1.0 → **0.1 / 1.0**;
  - `draw_pass_1` QuadMesh size: 0.012 → **0.03** m, so the specks are 0.003–0.03 m;
  - draw material `shading_mode`: unshaded → **per-pixel (lit)**; blend stays ADD;
  - `visibility_aabb`: (−1.1, −1, −0.8, 2.2, 2, 1.6) → **(−7.3, −1.45, −1.6, 14.6, 3.2, 9.6)**, the offset box plus 0.3 m on every side for turbulence.
- **Unchanged:** lifetime 6 s, lifetime_randomness 0.5, preprocess 6 s, velocity, turbulence, colour, the opacity ramp, ADD, billboard, the round texture, `local_coords` off, no shadow.
- **Tests:** the configuration test's expected values follow this table (110 passed, one new check for the offset); the state test reads `amount` at load, so it did not change (41 passed). Every other test kept its baseline count.
- **Particle peak and price:** the peak is now 3000, not 150; the brief's price prediction (≤ 0.3 ms GPU) is for the old effect and is re-measured in Step 7 and Use It.

### 2026-11-12 — Effect B redesign, second pass after my look in the game: `amount` and `color`
- **Why:** with the redesign above I looked at the strip and in the game: "still too dense" and "too bright, halve the brightness". I asked for 900 particles and half the brightness, looked at them in the game, and approved ("OK, go do the records").
- **Settings changed in the Effect B table** (old → new):
  - `amount`: 3000 → **900** (about 2.7 per cubic metre over the 330 m³ box); the particle peak is now 900;
  - `color`: (0.78, 0.86, 1.0) → **(0.39, 0.43, 0.5)**, the same cool white at half brightness. With ADD blending, half the colour adds half the light. This replaces the intent's "fixed cool white (0.78, 0.86, 1.0)"; the hue does not change.
- **Tests:** the configuration test's expected values follow (110 passed); the state test reads `amount` at load (41 passed); every other test kept its baseline count.

### 2026-11-12 — Effect B redesign, third pass: `amount` 900 → 1300
- **Why:** after the second pass I decided: "Let's make it 1300 after all."
- **Setting:** `amount` 900 → **1300** (about 3.9 per cubic metre over the 330 m³ box); the particle peak is now 1300. The colour stays at half brightness.
- **Tests:** the configuration test's expected value follows (110 passed); state test 41 passed; every other test kept its baseline count.
