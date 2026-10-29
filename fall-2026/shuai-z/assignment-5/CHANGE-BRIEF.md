# CHANGE-BRIEF — Assignment 5: the hearts' safe tint, and weathered stone for the waystone and the circle

**Revision 1 — 2026-10-24, committed before either shader is written.** Later changes are added as dated revisions at the end; this revision stays as it is.

**How this brief was made:** Claude Code (Claude Opus 5.5) drafted all of it from the assignment and this folder's files: the design, the rules, the colour line, the predicted values and the short answers. I reviewed it on 2026-10-24. The colour line is Claude's suggestion; I type it into the shader myself and record it in SOURCES.md and FRICTIONAL.md, as the assignment asks for any suggestion I adopt. Claude computed the predicted values with a short script; section 3 shows the arithmetic, so each value can be checked by hand.

`CLAUDE.md` imports this file (`@CHANGE-BRIEF.md`), so it is the contract the agent works to.

This folder holds two Godot 4.7.2 projects copied from tag `a3`: `game/`, the 2D game (GL Compatibility), and `godot/`, the Assignment 3 props scene (Forward Plus). The game is 2D, so the shader from code is in `game/`, and the textured shader, its materials, the hint experiment and the generated shader are in `godot/`.

## 1. The state

**Rudy is invulnerable:** the window after a hit, or after he gets back up at a checkpoint, in which hits are ignored.

- **What the effect says.** The hearts take on the pale blue of the lit waystone's glow, strongest when the window opens and fading to nothing as it runs out. It says that a hit just landed, and how much of the safe window is left.
- **Why the player needs it.** A hit already shows: Rudy is knocked back and flickers see-through, and a heart empties. Neither shows how long he is safe. The flicker is on Rudy, who moves; the hearts stay in the corner where the player looks to count them. With the tint, the player can tell when walking back into a hazard will cost again.
- **Where it lives.** `game/content/rudy/rudy.gd`:
  - `_invulnerable_left` (line 88), in seconds;
  - set to `invulnerable_time` (line 75, 1.2 s) by `take_hit()` (line 144) and by `respawn_at()` (line 188);
  - counted down by `_count_down()` (lines 263–264), once per physics tick;
  - `is_invulnerable()` (line 112) is `_invulnerable_left > 0.0`; while it is true, `take_hit()` returns false (line 129).

## 2. The effect specification

### The shader and its material

- **Shader:** `game/shaders/invulnerable_tint.gdshader`, `shader_type canvas_item;`, with no `render_mode` (the default `blend_mix`). The game has no `Light2D` or `CanvasModulate`, so nothing lights the hearts. It has no sampler uniforms: the heart textures, which `hearts.gd` draws with `draw_texture_rect()` (line 24), arrive in `COLOR`. It does not use `TIME`.
- **Object:** `Hud/Hearts` (`game/ui/hud.tscn` line 10), the one `Control` that draws all three hearts. Its material is a `ShaderMaterial` saved as `game/ui/hearts_tint.tres` and used by nothing else.
- **Why the hearts, not Rudy:** two existing checks rule out a new material on the obvious objects:
  - `game/tests/checks.gd` lines 871–877 require Rudy's `Look/Sprite` to keep the outline material;
  - lines 1056–1061 require that only the spikes and the goblin have a material, so the waystone, the circle and the pickup have none.

  Either change would alter an existing test's expectation.

### Uniforms

| Name | Type | Hint | Default | Set by |
|---|---|---|---|---|
| `tint_amount` | `float` | `hint_range(0.0, 1.0)` | `0.0` | the driver, every frame: Rudy's `_invulnerable_left / invulnerable_time` |
| `tint_color` | `vec4` | `source_color` | `vec4(0.6, 0.88, 1.0, 1.0)` (`#99E0FF` in 8 bits) | the material only, never code. It is the lit waystone's glow, `waystone.gd` line 19 (`GLOW`): the game's colour for a safe place |
| `tint_strength` | `float` | `hint_range(0.0, 1.0)` | `0.4` | the material only, never code. It sets how far toward `tint_color` a pixel moves at `tint_amount` 1.0. It is no more than 0.4 because at 0.6 the heart's outline would fall to 2.1:1 against the sky beside it, under rule 9's 3:1; at 0.4 it is 3.5:1 (section 3) |

### The colour line

The one line inside `fragment()` that changes the colour. I write the shader from it, and every prediction below is computed from it.

```glsl
COLOR.rgb = mix(COLOR.rgb, tint_color.rgb, tint_amount * tint_strength);
```

How it meets rules 7 to 9:
- At `tint_amount` 0.0 the weight is 0, so `COLOR.rgb` is unchanged (rule 7).
- It writes `.rgb` only, so alpha, the transparent pixels and the fade-in are untouched (rule 8).
- At 1.0 the weight is `tint_strength`, 0.4, so each pixel moves 40% of the way to `tint_color` (rule 9).
- The driver never sets more than 1.0, so the line has no clamp. Leaving the clamp out also lets the 2.0 capture show whether `hint_range` clamps (short answer 7).

### Observable rules

Game time is the `delta` Godot passes to `_physics_process()` and `_process()`. `game/project.godot` sets no `physics_ticks_per_second`, so physics runs at the default 60 ticks a second, and the window changes only on a physics tick.

1. **Begin.** On the first frame of a window, `tint_amount` is at least 70/72 = 0.972. After a hit it is 71/72 = 0.986 at 60 and 144 fps, and 71/72 or 70/72 at 30 fps. It is not 1.0 for this reason: the spikes (`spikes.gd` line 18) and the goblins (`goblin.gd` line 60) call `take_hit()` in their own `_physics_process()`, which runs before Rudy's in `main.tscn`'s tree order. Rudy's countdown therefore removes one tick (1/60 s) before any frame is drawn, and at 30 fps a second tick can pass in the same frame.
2. **Fade.** On every frame of the window, `tint_amount` = `_invulnerable_left / invulnerable_time`, which is linear in game time.
3. **End.** `tint_amount` is 0.0 on the first frame in which Rudy is not invulnerable, and on every frame in which he is not.
4. **Duration.**
   - The window is 72 physics ticks: 1.2 s of game time from the tick of the hit.
   - The first of those ticks passes before the first frame. So the frames that show `tint_amount` above zero span 71 ticks: **1.183 s ± one frame period** (1/30, 1/60 or 1/144 s), the same at 30, 60 and 144 fps.
   - In 64-bit floats, 72 steps of 1/60 from 1.2 reach exactly 0.0 (checked in Python), so rounding adds no tick.
5. **Retrigger.**
   - **A hit is ignored.** While the window is open, `take_hit()` returns false, so touching the spikes or a goblin again changes nothing. `tint_amount` keeps falling without a jump.
   - **A respawn restarts it.** `respawn_at()` opens a new window, and `tint_amount` jumps back up to that window's value (rule 1). This happens in normal play. A hit that takes the last heart opens a window, and the respawn comes about 1.15 s later (`DEFEAT_HOLD` 0.8 s + `FADE_TIME` 0.35 s, `main.gd` lines 41–42), usually before that window has run out.

   The tint follows the window, not the hit.
6. **Time scale and pause.**
   - The window runs on scaled game time: `Engine.time_scale` scales the `delta` that counts it down. At 0.5 the tint shows for 2.4 s of real time: 145 steps of 1/120 s reach zero (one more than exact arithmetic, because 1.2 is not exact in binary), minus the first.
   - While the tree is paused (Esc, `main.gd` line 159), Rudy and the driver are paused too; only `system_keys.gd` and `music.gd` use `PROCESS_MODE_ALWAYS`. So `tint_amount` holds its value, and continues from it on resume.
7. **At 0.0** the hearts are exactly as before: every pixel matches a capture taken without the shader.
8. **Alpha.** The tint never changes alpha.
   - Transparent pixels (the inside of an empty heart, the gaps between hearts) stay transparent, so the sky shows through unchanged.
   - The hearts' fade-in when play starts (`hud.gd` line 61, `modulate.a`) still works.
9. **At 1.0** every visible heart pixel has moved `tint_strength` of the way toward `tint_color`, and no further. The heart's dark outline keeps at least 3:1 contrast against the sky beside it (B in section 3), WCAG 2's minimum for parts of an interface, so each heart stays readable and a full heart still reads as full.
10. **Ending early.** The tint cannot outlast the window, because it follows the window. A window is cut short only by a scene reload (Enter on the end card, `main.gd` line 209), and the new `Hearts` starts at the shader's default, 0.0.
11. **Instances.** There is one `Hearts` node and one material, shared with nothing. If another `Hearts` were added, it would need its own material (a duplicate, or `resource_local_to_scene`); otherwise the two would tint together.
12. **Renderer.** It works in GL Compatibility, the 2D game's renderer.

### Boundaries

These do not change:
- collision, movement and input;
- `rudy.gd`, byte for byte. The driver reads `_invulnerable_left` and `invulnerable_time` and never assigns either; GDScript's underscore is a convention, not access control;
- the state machine and its timings in `rudy.gd` and `main.gd`: the 1.2 s window, the 0.35 s hurt time, Rudy's 0.12 s see-through flicker;
- the outline material and where it is used;
- every other HUD element (the title, the debug line, the fade, the end card, "Paused") and every other object;
- every existing test and its expectations: 141 checks in `game/`, 44 in `godot/`.

Presentation code may read game state; it never writes it.

### Evidence split

| Rule | Machine (headless, through `scripts/run-test.sh`) | My eyes |
|---|---|---|
| The shader parses; uniform names and types | New test: `get_shader_uniform_list()` holds exactly the three names with their types; no `SHADER ERROR` line in the log | — |
| Defaults | Read from the shader's source text; a headless engine does not report them | — |
| 1–4: begin, fade, end, duration | New test, through real play: the `restart` action starts play and `move_right` walks Rudy into the first spikes. `tint_amount` is sampled every frame from a node with a high `process_priority`, at 30, 60 and 144 fps | — |
| 5: retrigger | Same test: Rudy walks back into the spikes while the window is open (no jump), then loses his last heart (restart after the respawn) | — |
| 6: time scale and pause | Same test: one run with `Engine.time_scale` at 0.5, and one pause through the `pause` action in mid-window | — |
| 7–9: look | — | Captures at 0.0, 0.5 and 1.0, with sampled pixels beside the table below |
| `hint_range` from code (short answer 7) | — | A capture with `tint_amount` set to 2.0 from code |
| 10–11 | Test: the shader is on `Hud/Hearts` only, and a reload starts it at 0.0 | — |
| 12 | Every run uses the game's renderer | A windowed run |
| Boundaries | All 141 existing checks pass at 60 fps; `git diff --stat` on `rudy.gd`, `main.gd` and the existing tests is empty | In play, Rudy, the goblins, the spikes, the title and the rest of the HUD look as before |

## 3. Controlled inputs and predicted values

**Inputs.**
- `tint_color` = (0.6, 0.88, 1.0) and `tint_strength` = 0.4.
- `tint_amount` = 0.0, 0.5 and 1.0, and 2.0 from code in Use It.

**Why I compute on the values as written** (8-bit ÷ 255, rounded back to 8 bits):
- `game/project.godot` does not enable HDR 2D (`rendering/viewport/hdr_2d` is absent);
- the hearts are unlit;
- the Compatibility renderer uploads canvas uniforms without sRGB conversion.

The last point is Chapter 6's reading of the 4.7.2 source, not an observation, so a difference of more than a step or two per channel is a finding.

**Capture.**
- Taken in-engine, with `get_viewport().get_texture().get_image()` and the driver stopped.
- Taken after one hit at the first spikes, once that window has run out, so two hearts are full and one is empty.
- The coordinates below use the 1920 × 1080 layout. I record the capture's real size and scale them to it.

**Named pixels.** Both full-heart pixels sit in flat, opaque regions, so mipmapping does not change them. P3 sits in a 13 × 13-texel region with alpha 0.

| Pixel | Where (1920 × 1080) | Texel | Colour at 0.0 |
|---|---|---|---|
| P1, a full heart's red | heart 1, (54, 58) | `UI-HEART-FULL.png` (44, 68); 9 × 9 spread ≤ 2/255 | `#C84035` (200, 64, 53) |
| P2, a full heart's shadow | heart 1, (77, 56) | `UI-HEART-FULL.png` (90, 64); 9 × 9 spread ≤ 4/255 | `#992323` (153, 35, 35) |
| P3, a control: inside the empty heart | heart 3, (183, 49) | `UI-HEART-EMPTY.png` (62, 50), alpha 0 | the sky behind it |
| B, the sky beside the hearts | (222, 52) | — | about `#D1CBC9` (209, 203, 201). Read from Assignment 2's `evidence/2c/2c-hit-hearts.jpg`, a JPEG taken right after a hit at the first spikes; the 0.0 capture gives the exact value |

**Predicted values.** Each channel is c + w × (t − c) on the 0–255 scale, where c is the pixel, t is `tint_color` × 255 = (153, 224.4, 255), and w = `tint_amount` × 0.4. The result is rounded to the nearest step, and the capture may differ by one step. For example, P1's green at 1.0 is 64 + 0.4 × (224.4 − 64) = 128.2, so 128.

| `tint_amount` | P1 | P2 | P3 |
|---|---|---|---|
| 0.0 | `#C84035` (200, 64, 53) | `#992323` (153, 35, 35) | the sky, as captured |
| 0.5 | `#BF605D` (191, 96, 93) | `#99494F` (153, 73, 79) | unchanged |
| 1.0 | `#B58086` (181, 128, 134) | `#996F7B` (153, 111, 123) | unchanged |
| 2.0, from code | `#A2C0D7` (162, 192, 215) if `hint_range` does not clamp; `#B58086` if it does | `#99BBD3` (153, 187, 211), or `#996F7B` if it clamps | unchanged |

P3 is unchanged at every value: its alpha is 0, and `blend_mix` keeps the sky whatever the line does to the colour.

**Contrast** (WCAG 2, against B ≈ `#D1CBC9`):
- P1, the red fill: 3.09:1 at 0.0, 2.05:1 at 1.0. The fill is not what separates a heart from the sky; the outline is.
- The outline, `#3F170E` (texel (16, 34) of `UI-HEART-FULL.png`): 9.77:1 at 0.0, 3.51:1 at 1.0, above rule 9's 3:1.

## 4. The hint experiment

**Setup:**
- **The texture.** `godot/tools/write_grey_strip.gd` writes `godot/assets/hint_experiment/grey_strip_3x1.png`: three opaque texels, (64, 64, 64), (128, 128, 128) and (192, 192, 192).
- **Its import settings.** `compress/mode` 0 Lossless, `mipmaps/generate` false, `compress/normal_map` 2 Disabled, and `detect_3d/compress_to` 0 Disabled. Without the last one, the editor would switch it to VRAM compression the first time it draws it in 3D.
- **The shader.** `godot/shaders/hint_experiment.gdshader` is a spatial shader with `render_mode unshaded`. Two samplers are bound to that same file, one `source_color, filter_nearest` and one `filter_nearest` only. A `bool` uniform picks which one writes `ALBEDO`.
- **The materials.** `godot/materials/hint_source_color.tres` (`true`) and `godot/materials/hint_plain.tres` (`false`) sit on two quads facing the camera in `godot/scenes/hint_experiment.tscn`.
- **The environment.** A WorldEnvironment with `tonemap_mode` 0 (Linear), `tonemap_exposure` 1.0, and glow, fog and adjustments off.
- **The renderer.** Forward+ (`godot/project.godot` line 16), as the predictions assume.

To predict the displayed 8-bit value, use encode(x) = 12.92x for x ≤ 0.0031308, and 1.055·x^(1/2.4) − 0.055 otherwise.

| Band | File value | Quad A (`source_color`) | Quad B (no hint) |
|---|---|---|---|
| left | 64 | 64 | 137 (255 × encode(64/255) = 137.2) |
| middle | 128 | 128 | 188 (187.8) |
| right | 192 | 192 | 225 (225.0) |

**Quad A shows the file's values unchanged.**
- `source_color` tells Godot the texels are sRGB-encoded colour, so the sampler decodes them to linear for the renderer.
- The final sRGB encode on the way to the screen undoes that decode exactly: encode(decode(v)) = v.
- Quad B's texels are taken as linear already, so they are only encoded, once, on the way out, and come out lighter.
- In between, `unshaded` and the Linear tonemap at exposure 1.0 leave the values alone.

## 5. The material plan

### Objects and lighting

- **Objects** (in `godot/scenes/props_room.tscn`):
  - the waystone's **Stone** surface: surface 0 of the mesh `Waystone`;
  - the teleport circle's **DarkStone** surface: surface 1 of the mesh `TeleportCircle`.

  The Moss, Rune, Gold and PaleGold surfaces and the spikes keep their imported flat colours.
- **How the materials attach.** They are surface material overrides on the two instanced meshes (Editable Children), not the importer's per-material *Use External*.
  - Why: `godot/tests/check_props.gd` lines 85–89 load each `.glb` on its own and check every imported material's albedo colour by name (`Stone` `#8C8A80`, `DarkStone` `#4A4440`). With Use External those surfaces would load as `ShaderMaterial`, and that existing check would fail.
  - An override lives in `props_room.tscn`, so a reimport keeps it too. The `.glb` files and their `.import` files do not change.
  - `props_room.tscn` was written by Assignment 3's `godot/tools/build_props_room.gd`. Once the overrides are in, I do not run that builder again, because it would write the scene without them.
- **Lighting I judge under:** `props_room.tscn` as it is (lines 7–13 and 40–43):
  - one DirectionalLight3D, `Sun`, energy 1.1, shadows on;
  - background colour `#9DB8CF` (`background_mode` 1, Custom Color);
  - ambient light from the colour (1, 0.957, 0.878) at energy 0.45 (`ambient_light_source` 2, Color);
  - `tonemap_mode` 2 (Filmic), exposure 1.0 (the default).

  SSAO, SSIL, SSR, SDFGI, glow and fog are not set, so they are off, and nothing screen-space can be mistaken for the normal or roughness map. I view from the scene's `Camera`, and orbit for the sweep.

### Textures

All the textures come from Poly Haven's **Rock 01** (`rock_01`):
- by Rob Tuytel (role "All" in the API), released 2018-08-09;
- licence CC0. Poly Haven's licence page says "Our assets are all licensed as CC0", and no credit is required; the course requires provenance anyway;
- real-world width 1.5 m;
- page: https://polyhaven.com/a/rock_01.

I use the 1k PNGs, kept in `godot/assets/textures/rock_01/` with an `ATTRIBUTION.md` that records the URL, the author and role, the licence, the date checked, and the normal-map convention I use (`_nor_gl`). The files:
- https://dl.polyhaven.org/file/ph-assets/Textures/png/1k/rock_01/rock_01_diff_1k.png
- https://dl.polyhaven.org/file/ph-assets/Textures/png/1k/rock_01/rock_01_nor_gl_1k.png
- https://dl.polyhaven.org/file/ph-assets/Textures/png/1k/rock_01/rock_01_nor_dx_1k.png
- https://dl.polyhaven.org/file/ph-assets/Textures/png/1k/rock_01/rock_01_rough_1k.png

| File | Role | What its numbers mean | Sampled as | `compress/mode` | `compress/normal_map` | `mipmaps/generate` | Also set |
|---|---|---|---|---|---|---|---|
| `rock_01_diff_1k.png` | albedo | the rock's colour, sRGB-encoded | colour: `source_color` | 2 VRAM Compressed | 2 Disabled | true | `detect_3d/compress_to` 0 |
| `rock_01_nor_gl_1k.png` | normal map, OpenGL (Y+), which Godot expects | tangent-space surface directions in R and G, stored as plain numbers | data: `hint_normal` | 2 VRAM Compressed | 1 Enable | true | `detect_3d/compress_to` 0; `process/normal_map_invert_y` false |
| `rock_01_rough_1k.png` | roughness | 0 = mirror-smooth, 1 = fully rough, stored as plain numbers | data: no colour hint | 2 VRAM Compressed | 2 Disabled | true | `detect_3d/compress_to` 0; `roughness/mode` 1 Disabled |
| `rock_01_nor_dx_1k.png` | the curl check's calibration pair only; bound to no material | the same slopes with green flipped (DirectX, Y−) | not sampled | 0 Lossless | 2 Disabled | false | `detect_3d/compress_to` 0 |

**Why the last column.** The editor rewrites an `.import` file the first time it draws the texture in 3D (compression), as a normal map, or as roughness beside a normal map. The language step draws all three in a StandardMaterial3D in a real editor. So I set every value the editor would otherwise detect, and leave it nothing to change.

### The textured shader

`godot/shaders/weathered_stone.gdshader`, `shader_type spatial;`, with the default render modes. Its samplers:
- `albedo_tex`: `source_color, filter_linear_mipmap, repeat_enable`;
- `normal_tex`: `hint_normal, filter_linear_mipmap, repeat_enable`;
- `roughness_tex`: `filter_linear_mipmap, repeat_enable`, with no colour hint.

| Group | Name | Type | Hint and range | Default | Across its range on screen |
|---|---|---|---|---|---|
| `surface` | `albedo_tint` | `vec4` | `source_color` | `vec4(1.0)`: white, the photo as it is | Multiplies the photo's colour. White leaves it as photographed; darker values darken and tint the stone |
| `surface` | `uv_scale` | `float` | `hint_range(0.25, 4.0, 0.05)` | `1.0` | How many times the 1.5 m photo repeats across the UVs. High values give finer grain and visible repeats; low values stretch it soft |
| `relief` | `normal_strength` | `float` | `hint_range(0.0, 2.0, 0.05)` | `1.0` | How deep the normal map's relief reads. At 0 the surface is lit as flat; at 2 the cracks and bumps are exaggerated, with possible artefacts at grazing light |
| `relief` | `roughness_offset` | `float` | `hint_range(-0.5, 0.5, 0.01)` | `0.0` | Added to the roughness map, then kept within 0–1. Negative values make the stone glossier, with a tighter highlight from the Sun; positive values make it matte |

### The two materials

| | `godot/materials/waystone_stone.tres` (waystone, Stone) | `godot/materials/circle_darkstone.tres` (circle, DarkStone) |
|---|---|---|
| Textures | the three above | the same three |
| `albedo_tint` | `#FFFFFF` | `#8F857D`: a starting value, aimed at an average near A3's DarkStone `#4A4440`; set in the sweep and recorded as a revision |
| `uv_scale` | 1.0 | 1.0 |
| `normal_strength` | 1.0 | 0.35 |
| `roughness_offset` | 0.0 | −0.25 |

**Why they differ:**
- The waystone stands in a field and is weathered: the photo as taken, full relief, rough.
- The circle's inner disc is where travellers step. It is darker, as Assignment 3 made it; it is worn flatter, so it has less relief; and it is polished by feet, so it is glossier.

They differ in three values and share their textures. A change to the shader therefore changes both, and a change to one material changes only that one.

## 6. Predicted failures and how each is caught

| # | Prediction | Check |
|---|---|---|
| 1 | The tint shows on something else: the material is shared, or set on the HUD instead of `Hearts`. | The new test asserts that the shader is on `Hud/Hearts` only, and the outline checks in `checks.gd` still pass. In play, nothing but the hearts changes. |
| 2 | The duration depends on the frame rate: the driver counts frames, or runs its own clock in real time. | The new test measures 1.183 s ± one frame at each of 30, 60 and 144 fps. |
| 3 | The driver follows the hit, not the window: walking back into the spikes restarts the tint, or a respawn does not. | The new test's retrigger steps (rule 5), through real input. |
| 4 | The tint keeps fading while paused, because the driver uses `PROCESS_MODE_ALWAYS` and its own clock. | The new test pauses mid-window with the `pause` action. |
| 5 | The colour line writes alpha, so the inside of the empty heart turns blue. | P3 in the 0.5 and 1.0 captures. |
| 6 | Rudy is standing on the spikes when a window ends. The next tick hits him again (`spikes.gd` checks every tick), so `tint_amount` is 0.0 for one tick only; at 30 fps that tick can fall inside one frame, so no frame shows 0.0. | This is the game's rule, not a broken rule 3: the test measures a window's end with Rudy off the spikes. |
| 7 | A data texture is sampled with `source_color`, or the colour texture without it. | `test_materials.gd` reads each sampler's hints from the source text, and the mutation that deletes `source_color` from `albedo_tex` must exit 1. |
| 8 | The editor rewrites an import setting the first time it draws a texture. | `git status` after my first editor session, and `test_materials.gd` asserting the settings above from the `.import` files. |
| 9 | The materials go on through Use External, and `check_props.gd` loses its `Stone` and `DarkStone` colours. | `check_props.gd` stays at 44 of 44, and `test_materials.gd` asserts the two overrides in `props_room.tscn`. |
| 10 | The normal map uses the wrong convention. | The curl ratio of `rock_01_nor_gl_1k.png` is near 0 with `directx = false` and near 2 with `true`, after calibrating on the GL/DX pair. |
| 11 | The tinted hearts lose contrast against the pale clouds. | My contrast ratios in section 3, and the 1.0 capture. |

## 7. Short answers

1. **Which renderer project.godot names, and what it rules out.**
   - `game/project.godot` lines 95–96 name `gl_compatibility` for desktop and mobile. That rules out decals, compute shaders, VoxelGI, SDFGI and SSIL.
   - `godot/project.godot` line 16 lists the feature `Forward Plus` and sets no other method, so the 3D project uses Forward+, which rules out none of them.
2. **What colour arrives in my `fragment()` before I change it, and what the tempting alternative would give.**
   - `COLOR` arrives holding the heart's texel colour multiplied by the vertex colour, and the vertex colour already carries `Hearts`' `modulate` and `self_modulate`. Godot's canvas_item reference: "COLOR from the vertex() function multiplied by the TEXTURE color".
   - For the hearts, that is the art's colour, with the art's alpha times the title fade (`hud.gd` lines 54 and 61).
   - The tempting alternative, `texture(TEXTURE, UV)`, gives the texel alone. The colours here would be the same, but `modulate` would be gone, so the hearts would show on the title screen, where `hud.gd` line 54 hides them with `modulate.a = 0.0`.
3. **For `canvas_item`, what `texture(TEXTURE, UV)` would give instead of `COLOR`.** The colour stored in the heart texture at that UV, filtered, before any vertex colour or `modulate` is applied. On something drawn without a texture, such as Chapter 6's Clawd drawn with `draw_rect()`, the colour lives only in the vertex colour, which `texture(TEXTURE, UV)` throws away; `TEXTURE` is then Godot's default texture, which is white.
4. **For `spatial`, what `ALBEDO` holds if I never write it, and what `COLOR` holds.**
   - `ALBEDO` is white by default (Godot's spatial reference: "Albedo (default white)"), so an untextured stone would light as plain white.
   - `COLOR` holds the vertex colour passed on from `vertex()`. The props' `.glb` meshes have no vertex-colour attribute (only `POSITION`, `NORMAL` and `TEXCOORD_0`), and neither do the quads, so I expect it to be white; I will check that rather than assume it. Neither of my spatial shaders reads it.
5. **How long a frame-counting version would last.** Counting 72 frames, the window's length at 60 fps, it would last 72/30 = 2.4 s at 30 fps, 1.2 s at 60 and 72/144 = 0.5 s at 144. The window itself, and the hits it ignores, would still last 1.2 s at every rate, so the tint and the safety would disagree.
6. **Which resource holds the default and which the current value, and what happens if two objects share the material.**
   - The default lives in the `Shader` resource: `= 0.0` in the uniform's declaration in `invulnerable_tint.gdshader`.
   - The current value lives in the `ShaderMaterial`, `game/ui/hearts_tint.tres`: the value saved there at load, and the driver's `set_shader_parameter()` value after that. A uniform the material never sets uses the shader's default.
   - Two objects that share a material share one value, so tinting one tints both. The game already shares one material: `systems/art/outline.tres` is on Rudy, the goblin and the spikes (`rudy.tscn`, `goblin.tscn`, `spikes.tscn`), so changing its `width` changes all three.
7. **Does `hint_range` clamp a value my driver sets from code? My prediction: no.**
   - The shading-language reference describes `hint_range` only as "Restricted to values in a range (with min/max/step)", and says nothing about values set from code. I expect it to shape only the Inspector's slider.
   - So `tint_amount` set to 2.0 from code should reach the shader as 2.0. The colour line would then move P1 to `#A2C0D7`, past the 1.0 value `#B58086` (section 3).
   - If the capture shows `#B58086`, something clamped it, and I find out what.

## Revisions

### Revision 2 — 2026-10-27: the circle's `albedo_tint` is `#A4A7B4`

Section 5 gave `circle_darkstone.tres` the `albedo_tint` `#8F857D` as a starting value, aimed at an average near Assignment 3's DarkStone `#4A4440`, to be set in the sweep and recorded here. It is now `#A4A7B4`.

- **Why.** Rock 01's colour map, averaged in linear light, is `#776C5E`, a warm grey. Multiplied by `#8F857D`, which is warm too, it averages `#40352A`: darker and browner than `#4A4440`, by 10, 15 and 22 steps in red, green and blue.
- **The new value.** `#A4A7B4` is the tint that puts the average at `#4A4440`, computed the same way. It is slightly cool, so it cancels the photo's warmth.
- **How it was computed.** Each texel is decoded from sRGB to linear, the texels are averaged, and the average is multiplied by the tint, also decoded to linear, then encoded back to sRGB. This is the colour of the texture alone, before lighting and the Filmic tonemap; the look on screen is my check in the editor.
- **Who.** Claude computed both averages and the new tint. I chose to change it.
- **Unchanged:** everything else in section 5, including the circle's other values and the waystone's material.

### Revision 3 — 2026-10-27: line numbers in section 5

The surface overrides added two `ext_resource` lines to `props_room.tscn`, so the lines section 5 cites for the lighting moved. The Environment is now lines 9–15 and `Sun` lines 42–45, not 7–13 and 40–43. The values are unchanged. The audit found this (`godot/MATERIALS.md`, finding 4).

### Revision 4 — 2026-10-28: line numbers for `hud.gd` and `hud.tscn`

The driver (`bd797945`) added a line to the comment at the top of `game/ui/hud.gd`, and an `ext_resource` line and a `material` line to `game/ui/hud.tscn`, so lines this brief cites moved. In section 2, `Hud/Hearts` is now `hud.tscn` line 11, not 10, and its material is line 18. In rule 8 and short answer 2, the title's `modulate.a = 0.0` is now `hud.gd` line 55, not 54, and the hearts' fade-in is line 62, not 61. The code they point to is unchanged. Claude found this while checking CLAUDE.md's references, which had moved the same way.
