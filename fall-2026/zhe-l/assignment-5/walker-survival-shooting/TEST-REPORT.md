# TEST-REPORT — Assignment 5

- **Source revision:**
  - First shader: game source as of commit `9995995d` (the screen driver); test `7f53f457`; captures and capture tool `a382422b`.
  - Second shader: crate shader `6cf61748`, hint-experiment shader `b9be0617`, textures, materials and hint scene `2d558bba`, material test `f722f2d7`. No game source changed after `2d558bba` (only tests, documents and `standard_generated.gdshader`, which the game does not use, were added later).
- **Godot:** v4.7.2.stable.official.ed1daf0bf (Windows, `Godot_v4.7.2-stable_win64_console.exe`)
- **Renderer:** Forward+, D3D12 12_0, NVIDIA GeForce RTX 5070 Ti Laptop GPU
- **Test entry point:** `scripts/run-test.sh <test file> <fps>`; logs are in `logs/`

This report covers both shaders, the tablet screen glow (`pad_base_light.gdshader`) and the crate wear (`crate_wear.gdshader`), plus the hint experiment and the shader generated in Step 4. The look of the crate shader and the hint experiment is checked in section 9: the captures were taken by Claude with scripts in a real window, and I looked at them.

---

## 1. Baseline

| Test | fps | When | Result | Log |
|---|---|---|---|---|
| `a3_asset_check.gd` | 60 | Before (A5 starting point, 2026-10-29) | 55 PASS, 0 FAIL, exit 0 | `logs/a3_asset_check_60fps.log` |
| `a3_asset_check.gd` | 60 | After the screen shader, material and driver (2026-11-01) | 55 PASS, 0 FAIL, exit 0, no SHADER ERROR / SCRIPT ERROR | `logs/a3_asset_check_60fps_after-screen-driver.log` |
| `a3_asset_check.gd` | 60 | After the crates got the wear materials (2026-11-01) | 55 PASS, 0 FAIL, exit 0, no SHADER ERROR / SCRIPT ERROR | `logs/a3_asset_check_60fps_after-crate-materials.log` |
| `screen_glow_check.gd` | 60 | After the crates got the wear materials (2026-11-01) | 24 PASS, exit 0; the log is identical to the earlier one | `logs/screen_glow_check_60fps.log` |
| `a3_asset_check.gd` | 60 | After all changes (2026-11-01, commit `4473d512`) | 55 PASS, 0 FAIL, exit 0, no SHADER ERROR / SCRIPT ERROR | `logs/a3_asset_check_60fps_final.log` |

`a3_asset_check.gd` and its expectations were not changed in A5.

**Every test run again after all changes (2026-11-01, commit `4473d512`, all through `scripts/run-test.sh`):**

| Test | fps | Result | Log |
|---|---|---|---|
| `a3_asset_check.gd` | 60 | 55 PASS, exit 0 | `logs/a3_asset_check_60fps_final.log` |
| `screen_glow_check.gd` | 30 / 60 / 144 | 24 PASS each, exit 0 | `logs/screen_glow_check_{30,60,144}fps_final.log` |
| `normal_map_check.gd` | 60 | 2 PASS, exit 0 | `logs/normal_map_check_60fps_final.log` |
| `test_materials.gd` | 60 | 169 PASS, exit 0 | `logs/test_materials_60fps_final.log` |

None of the six logs contains `SHADER ERROR` or `SCRIPT ERROR`. The same counts were reproduced in this repository's copy of the project after deleting `godot/.godot/` and running `--import` again.

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

### Crate wear shader (`godot/shaders/crate_wear.gdshader`)

Checked by `tests/test_materials.gd` (written by the audit session, see section 6):

| Check | Result |
|---|---|
| `get_shader_uniform_list()` has 7 entries: `rust_albedo`, `wear_mask` (Texture2D), `paint_color` (Color), `paint_roughness`, `wear_amount`, `wear_softness`, `texture_scale` (float) | PASS |
| Groups: `paint_color` / `paint_roughness` in `paint`, `wear_amount` / `wear_softness` in `wear`, `texture_scale` in `mapping`, the two samplers in no group | PASS |
| `hint_range`: 0.0–1.0, 0.0–1.0, 0.0–0.2, 0.1–10.0 | PASS |
| Source: the five defaults, `RUST_ROUGHNESS = 0.79`, `MIN_WEAR_SOFTNESS = 0.001`, no `render_mode unshaded` | PASS |
| Source: `rust_albedo` hints are `source_color, filter_linear_mipmap, repeat_enable`; `wear_mask` hints are `filter_linear_mipmap, repeat_enable` (no `source_color`) | PASS |

No `SHADER ERROR` in the log. The hint-experiment shader (`hint_experiment.gdshader`) is checked by the same test: 3 uniforms, both samplers' hints, `unshaded`, all PASS.

The shader generated in Step 4 (`standard_generated.gdshader`) parses when loaded headlessly (exit 0); the game does not use it.

### Crate shader mutation

| Mutation | By | SHADER ERROR | Result | Exit | Log |
|---|---|---|---|---|---|
| Delete `source_color` from `rust_albedo` (line 3) | me | none (deleting a hint is not a syntax error) | 168 PASS, **1 FAIL**: `rust_albedo hints are source_color, filter_linear_mipmap, repeat_enable (source: filter_linear_mipmap, repeat_enable)` | **1** | `logs/mutation_source_color_60fps.log` |

After restoring, `git diff godot/shaders/` is empty, the file hash equals the one in commit `6cf61748` (`e254ae3b…`), and the test is back to 169 PASS, exit 0. On my first attempt the edit was not saved to disk (the file time was still 21:12 and `git diff` was empty); that run gave the usual 169 PASS, did not count, and its log was deleted.

Only the "read the hints from the source" check catches it: a sampler's `source_color` does not show in `get_shader_uniform_list()`, where both samplers appear only as Texture2D.

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

**Audit (assignment lines 304–348):** I opened a separate interactive Claude Code session with `prompt-3.txt` (the assignment's audit prompt, with a note about my local paths added at the top). It wrote `godot/MATERIALS.md` and `godot/tests/test_materials.gd` and ended normally (its last event is `end_turn`, no permission denials); its output was committed unedited as `f722f2d7`. After the audit, `git diff --stat godot/shaders/` and the diff of `scripts/run-test.sh` printed nothing.

**Review (me and Claude; corrections committed separately as `2e6de3f8`):**
- The integer enums were checked against the option lists of the Godot 4.7.2 texture importer; `compress/normal_map` 2 had been written "Disable" and became "Disabled".
- The format numbers were checked against the `Image.FORMAT_*` constants printed by the engine (L8 = 0, RGB8 = 4, DXT1 = 17, RGTC_RG = 21).
- The renderer evidence was wrong: the audit wrote "`rendering_method = forward_plus`, `project.godot` line 15", but the file has no such key; line 15 is the "Forward Plus" entry in `config/features`. Corrected.
- The "distance from the lights to the crates" row was deleted: its numbers were computed from coordinates, not measured.
- The audit found that the shader never writes `METALLIC`, so the silver scratches in the rust are shaded as non-metal. I decided to record this as a known limitation and not change the shader.

**Test results:**

| Run | Result | Exit | Log |
|---|---|---|---|
| In the audit session | First run 1 FAIL, caused by the test itself (it compared the `hint_range` minimum 0.1 as text, which reads back from a 32-bit float as `0.10000000149012`); after the audit session changed it to a numeric comparison, 169 PASS | 0 | The audit session's own log was later overwritten; see `session-3-audit-excerpt.md` |
| After deleting the `godot/.godot/` cache and reimporting | 169 PASS | 0 | `logs/test_materials_60fps_fresh-cache.log` (the import log stays on my computer: the editor prints its progress in my interface language, Chinese; it has no error or warning lines) |
| With `source_color` deleted (mutation, see section 2) | 168 PASS, 1 FAIL | **1** | `logs/mutation_source_color_60fps.log` |
| After restoring `source_color` | 169 PASS | 0 | `logs/test_materials_60fps.log` |
| After all changes | 169 PASS | 0 | `logs/test_materials_60fps_final.log` |

What the test checks: both crate materials use the same shader; the values each material stores (long crate `wear_amount` 0.2 / `paint_roughness` 0.95, small crate 0.1 / 0.85) and the textures it binds; each sampler's hints (read from the source); the uniform list; the import settings of the 6 `.import` files (`ConfigFile`); Use External in both `.glb.import` files pointing to the matching `.tres`; after instancing `base.tscn`, the shell and lid of both crates use the wear material and the hardware keeps its original material; the lights and environment of both scenes (runtime values).

**What the headless test cannot prove:** the colours on screen, the look of the rust, whether the shader compiles on a GPU, whether `source_color` really makes the GPU decode sRGB, and the on-screen effect of the sampler hints (see section 6 of `godot/MATERIALS.md`).

## 7. Texture data

`curl_ratio` from `tests/normal_map_check.gd` (function body copied from the assignment), reading the source files (`Image.load_from_file`; the 16-bit PNGs decode to `FORMAT_RGB8`), stride 4:

| Texture | `directx = false` (GL convention) | `directx = true` (DX convention) |
|---|---|---|
| `Metal041C_1K-PNG_NormalGL.png` | **0.1991** | 1.8009 |
| `Metal041C_1K-PNG_NormalDX.png` | 1.8009 | **0.1991** |

- Calibration pair (GL and DX of the same Metal041C set): each map is low under its own convention and near 2 under the other, **not reversed**, so the sign s did not need flipping.
- 0.199 is not 0: 8-bit quantization noise moves the ratio away from 0 (assignment line 300 says compressed or flat maps drift toward 1). The threshold is read from this pair's measured values: about 0.2 under the right convention, about 1.8 under the wrong one.
- No material in the game uses a normal map (the crate shader does not); NormalGL is used only in the Step 4 StandardMaterial3D.
- Logs: `logs/normal_map_check_60fps.log`, `logs/normal_map_check_60fps_final.log`; `test_materials.gd` prints the same four numbers.

## 8. Import settings

The plan is in the CHANGE-BRIEF revision of 2026-11-01. A first headless import generated the `.import` files, the keys were then set to the planned values, and the textures were reimported:

| Texture | `compress/mode` | `compress/normal_map` | `mipmaps/generate` | Format after import (`get_image().get_format()`) |
|---|---|---|---|---|
| `Metal041C_1K-PNG_Color.png` | 2 (VRAM Compressed) | 2 (Disabled) | true | 17 `FORMAT_DXT1` |
| `Metal041C_1K-PNG_Displacement.png` | 0 (Lossless) | 2 | true | 0 `FORMAT_L8` |
| `Metal041C_1K-PNG_Roughness.png` | 2 | 2 | true | 17 `FORMAT_DXT1` |
| `Metal041C_1K-PNG_NormalGL.png` | 2 | 1 (Enable) | true | 21 `FORMAT_RGTC_RG` |
| `Metal041C_1K-PNG_NormalDX.png` | 2 | 1 | true | 21 `FORMAT_RGTC_RG` |
| `hint_greys_3x1.png` | 0 | 2 | false | 4 `FORMAT_RGB8`; after import the three pixels are still 64 / 128 / 192 |

**Two keys set beyond the plan (in all six files):** `detect_3d/compress_to = 0` (Disabled) and `roughness/mode = 1` (Disabled). Reason: with the defaults, the first time the editor draws a texture in 3D it switches it to VRAM compression by itself (which would change the lossless Displacement), and a roughness texture may also be rewritten by detection. With both off, the editor has nothing left to change.

**Did the editor rewrite any `.import`:** the first time these textures were used in the editor was Step 4 (the StandardMaterial3D used Color, Roughness and NormalGL). Afterwards `git status` showed no change to any committed `.import`, and none changed after clearing `.godot/` and reimporting either. **No `.import` was rewritten, so there is no diff to explain.**

Displacement is 16-bit greyscale in the file; it becomes 8-bit when the PNG is decoded (`Image.load_from_file` already returns `FORMAT_L8`), not because of import compression.

---

## 9. The crate shader and the hint experiment on screen (engine captures)

**How the captures were made:** Claude took them with capture scripts in the film-preparation session (the scripts `hint_capture.gd` and `crate_capture.gd` live in my film working folder, not in the project). They ran in a copy of the project in a real window (not headless), on D3D12, and read the engine's frame with `get_texture().get_image()`, not an OS screenshot. Parameters were changed only at runtime with `set_shader_parameter()`; nothing was written back to any file. **I looked at all the captures on 2026-11-01 and found nothing wrong.**

### Hint experiment

`experiments/hint/hint_experiment.tscn`, Linear tonemap, exposure 1.0 (defaults, see section 6). The sample points are the centres of the bands computed with the scene camera's `unproject_position()`; the 3 × 3 pixels around each point are identical. The window viewport (1152 × 648) and a 4K `SubViewport` (3840 × 2160) read the same values.

| Band (value in the file) | With `source_color` (upper quad), predicted → measured | Without (lower quad), predicted → measured |
|---|---|---|
| 64 | 64 → (64, 64, 64) | 137 → (137, 137, 137) |
| 128 | 128 → (128, 128, 128) | 188 → (188, 188, 188) |
| 192 | 192 → (192, 192, 192) | 225 → (225, 225, 225) |

The difference from the predictions in Part 2 of CHANGE-BRIEF is 0. The quad with `source_color` shows the file's values unchanged, because the sRGB → linear decode when sampling and the linear → sRGB encode before display cancel out; the quad without it is encoded once more, so it is brighter.

I also looked at it myself once in the editor's 3D viewport: the upper quad is darker, and the leftmost band differs the most. The values read from my screenshot are the same as in the table (`captures/hint_experiment_editor_view.png`, an OS screenshot of the editor viewport, with the camera icon and guides on it, not an engine export). The gap is largest on the left (73 levels) and smallest on the right (33 levels), because the sRGB encoding curve is steepest in the darks.

Captures: `captures/hint/hint_window_1152x648.png`, `captures/hint/hint_4k_3840x2160.png`.

### One shader, two materials

`captures/crate/pair.png`: the original lighting of `base.tscn` (3 ceiling lights + ambient light), no light added; the camera was added by the capture script. The long crate (`crate_long_wear.tres`, `wear_amount` 0.2, `paint_roughness` 0.95) is more rusted than the small crate (`crate_cube_wear.tres`, 0.1, 0.85).

- **Editing one material:** the sweep changes only `crate_cube`'s material, and `crate_long` next to it is unchanged in every sweep capture.
- **Editing one line of the shader so both crates change:** **not done.** Only I may edit the shader, and I did not do this check.

### Interface sweep

Only `crate_cube` was changed. The "what changed" column is Claude's description of the captures; I looked at the captures and agree with it.

| Uniform | Minimum | Default | Maximum | What changed on screen |
|---|---|---|---|---|
| `paint_color` | (0, 0, 0, 1) | (0.26, 0.283, 0.19, 1) | (1, 1, 1, 1) | The paint turns entirely black / white; the rust patches keep their place and colour |
| `paint_roughness` | 0.0 | 0.85 | 1.0 | Almost no difference from the first camera angle (largest pixel difference 2). From an angle with a highlight (`captures/crate-glint/`): at 0 the top is darker and greener, at 0.85 there is a greyish sheen, and 1 differs very little from 0.85 |
| `wear_amount` | 0.0 | 0.1 | 1.0 | 0: no rust visible; 1: the whole crate is rust (with silver scratches) |
| `wear_softness` | 0.0 (= default) | 0.0 | 0.2 | At 0.2 the edge between paint and rust turns into a blur that looks like dirt, not chipped paint |
| `texture_scale` | 0.1 | 2.0 | 10.0 | 0.1: the rust patches become large blocks; 10: they become fine dots |

**Settings that break the look:** near 0.2, `wear_softness` no longer looks like chipped paint; at `wear_amount` = 1 the whole crate is rust and no longer reads as a painted crate. The five "default" captures have identical file hashes, so the same values draw the same pixels every time.

Captures: `captures/crate/crate_cube_<uniform>_<value>.png` (15 images, 4K), `captures/crate-glint/` (5 images, from the angle with a highlight).
