# TEST-REPORT — Assignment 5

- **Source revision:** game source as of commit `9995995d` (the screen driver); test `7f53f457`; captures and capture tool `a382422b`. No game source changed after `9995995d`.
- **Godot:** v4.7.2.stable.official.ed1daf0bf (Windows, `Godot_v4.7.2-stable_win64_console.exe`)
- **Renderer:** Forward+, D3D12 12_0, NVIDIA GeForce RTX 5070 Ti Laptop GPU
- **Test entry point:** `scripts/run-test.sh <test file> <fps>`; logs are in `logs/`

This report covers the **first shader (the tablet screen glow, `pad_base_light.gdshader`)** so far. The second shader (crate wear) sections are marked *to do*.

---

## 1. Baseline

| Test | fps | When | Result | Log |
|---|---|---|---|---|
| `a3_asset_check.gd` | 60 | Before (A5 starting point, 2026-10-29) | 55 PASS, 0 FAIL, exit 0 | `logs/a3_asset_check_60fps.log` |
| `a3_asset_check.gd` | 60 | After the screen shader, material and driver (2026-11-01) | 55 PASS, 0 FAIL, exit 0, no SHADER ERROR / SCRIPT ERROR | `logs/a3_asset_check_60fps_after-screen-driver.log` |

`a3_asset_check.gd` and its expectations were not changed in A5. Both counts were also reproduced in this repository's copy of the project after a fresh `--import`.

---

## 2. Shaders parse

### Screen glow shader (`godot/shaders/pad_base_light.gdshader`)

The first five checks in `tests/screen_glow_check.gd`:

| Check | Result (30 / 60 / 144 fps) |
|---|---|
| `cold_white` is in the uniform list and is a colour (`source_color`) | PASS |
| `pad_light_data` is in the uniform list and is a float | PASS |
| `pad_light_data` has `hint_range(0.0, 1.0)` | PASS |
| Source: `cold_white` defaults to `vec4(0.902, 0.969, 0.969, 1.0)` | PASS |
| Source: `pad_light_data` defaults to 0.0 | PASS |

No log at any of the three frame rates contains `SHADER ERROR`.

**Mutations.** After each one the shader was restored; its hash still starts `dbd3fc23…` and `git diff` is empty.

| Mutation | By | SHADER ERROR | Failures | Exit | Log |
|---|---|---|---|---|---|
| Delete a semicolon | me | `Expected a ';'` | 3 FAIL | 1 | `logs/mutation_semicolon_60fps.log` |
| Rename `pad_light_data` to `pad_light_level` in both places (declaration and the use in `fragment()`) | Claude, at my request | none | 3 FAIL (uniform exists / hint / source default) | 1 | `logs/mutation_rename_60fps.log` |
| Rename only the declaration (my first attempt) | me | `Unknown identifier in expression: 'pad_light_data'` | 4 FAIL | 1 | `logs/mutation_rename_declaration_only_60fps.log` |

What the rename shows: the shader still parses, and Godot gives **no error** when the driver writes to a name the shader does not declare. Every behaviour check still passes, because `get_shader_parameter` reads back the value that was just written. Only the "is this name in the uniform list" check catches it.

### Crate wear shader

*To do.*

---

## 3. Driver

`tests/screen_glow_check.gd` drives the game with real Tab key events (`Input.parse_input_event`), records the state and the player tablet's `pad_light_data` every frame, and also records a second humanoid body's value. Time is counted as in the CHANGE-BRIEF revision of 2026-11-01: from the physics frame in which the state changes, including that frame, to the physics frame in which the screen lights.

| fps | First value | Last value | Time to light (game time) | Lit after a retrigger | time_scale 0.5 | Second body | Result | Log |
|---|---|---|---|---|---|---|---|---|
| 30 | 0.0 | 0.0 (put away) | 0.3667 s | 0.3667 s | 0.35 s game time = 0.70 s real time | 0.0 on all 286 frames | 24 PASS, exit 0 | `logs/screen_glow_check_30fps.log` |
| 60 | 0.0 | 0.0 | 0.3500 s | 0.3500 s | same | 0.0 on all 546 frames | 24 PASS, exit 0 | `logs/screen_glow_check_60fps.log` |
| 144 | 0.0 | 0.0 | 0.3500 s | 0.3500 s | same | 0.0 on all 1296 frames | 24 PASS, exit 0 | `logs/screen_glow_check_144fps.log` |

All are within "0.35 s ± one frame". The extra 0.0167 s at 30 fps comes from each rendered frame running two physics frames, so the sample can read the change one physics frame late.

Other boundaries:
- Switching between one hand and two hands: no frame is 0.0 (no flicker).
- Putting it away from one hand: 0.0 on the very frame the state becomes NONE (off at once).
- Taking it out and putting it back before it arrives: never lit.
- The lit value equals `light_strength_percentage` (0.39).

---

## 4. Controlled values

**Method:** run `debug/screen_glow_capture.tscn` from the editor (a real window, not headless), long-press Tab to hold the tablet in both hands, press F9. The tool pauses the player brain's `_physics_process`, sets `pad_light_data` to 0 / 0.39 / 1.0 / 2.0 in turn, saves a PNG of each with `get_viewport().get_texture().get_image()` (viewport 2048 × 1152), then resumes the driver.

**Sample points** (from `unproject_position`, the same in both runs): P1 screen centre (1024, 566), P2 1 cm in from the screen's upper-right corner (1616, 241), P3 the casing below the screen (1024, 1077). `*_marked.png` marks the three points with red boxes.

| `pad_light_data` | P1 | P2 | Predicted (CHANGE-BRIEF) | Difference | P3 casing |
|---|---|---|---|---|---|
| 0.00 | (0, 0, 0) | (0, 0, 0) | (0, 0, 0) | 0 | (7, 17, 14) |
| 0.39 | (151, 162, 162) | (151, 162, 162) | (151, 162, 162) | 0 | (7, 17, 14) |
| 1.00 | (230, 247, 247) | (230, 247, 247) | (230, 247, 247) | 0 | (7, 17, 14) |
| 2.00 | (255, 255, 255) | (255, 255, 255) | (255, 255, 255) | 0 | (7, 17, 14) |

Captures: `captures/screen_pad_{0.00,0.39,1.00,2.00}.png` and the matching `_marked.png`.

**The hint_range question:** setting `pad_light_data` to 2.0 from code turns the screen pure white (255, 255, 255). So `hint_range(0.0, 1.0)` limits only the inspector slider and does **not** clamp a value set from code. The result is `mix(0, cold_white, 2.0)` = 2 × cold_white, and everything above 1 is clipped to 255 on output. This matches my prediction B.

**Casing P3:** the casing uses an ordinary lit material and is the same at all four values, so the screen's `unshaded` material does not light anything next to it. The first time I pressed F9 the console printed P3 as (17, 31, 28). The PNGs here are from the second F9 run, which overwrote the first set; there P3 is (7, 17, 14). The screen values are identical in both runs; the casing differs because it is lit and the character faced a different way.

**Engine capture vs OS screenshot (compared once):**
- The OS screenshot was taken during the second F9 run, while the screen was at 2.0. The copy used is the one I pasted into my chat with Claude (`captures/os_screenshot_f9_chat-copy.webp`, 2000 × 1125).
- With the engine's 2.0 capture scaled to the same size and compared point by point, the per-channel difference has a median of 1, is ≤ 3 for 99% of points and is at most 16, with the largest differences on object edges. The screen is (255, 255, 255) in both; the casing is (8, 17, 14) against (7, 17, 14).
- My display does not support HDR.
- The colours were not changed; the difference comes from scaling (the window was not full screen, so the screenshot is 2000 wide while the viewport is 2048), which moves pixel positions and blurs edges.
- **I trust the engine capture**, because it is the rendered frame at the viewport's own resolution, so its pixel coordinates line up with the ones the predictions were computed for. The OS screenshot went through window scaling, so the same coordinate is not necessarily the same point.
- Claude also ran a temporary diagnostic script (not part of the project) on `base.tscn` in a real window (640 × 360): the image read from the viewport (RGB8 format) and the same image saved as PNG and loaded back differed at 0 points, so saving the PNG does not change pixels.

---

## 5. In play

Played normally in `base.tscn`, taking the tablet out, switching hands and putting it away with short and long Tab presses, about five or six times.

What I saw: **lit only once it reaches the hand, off at once when put away, no flicker when switching.**

---

## 6. Material wiring

*To do (crate wear shader).*

## 7. Texture data

*To do (crate wear shader).*

## 8. Import settings

*To do (crate wear shader).*
