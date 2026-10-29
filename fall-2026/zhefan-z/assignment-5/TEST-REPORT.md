# TEST-REPORT — Assignment 5

- **Source revision:** game source as of `40c42f5` (captures and generated shader); the documents were added after it without changing game source.
- **Godot:** 4.7.2-stable, official build `ed1daf0bf`.
- **Renderer:** Forward+, Vulkan 1.4.312, NVIDIA GeForce RTX 5060 Laptop GPU (printed by every windowed run). `project.godot` names no rendering method, so this is the default. No `hdr_2d`.
- **OS:** Windows, Git Bash. Every test ran through `./scripts/run-test.sh`, which pins `--fixed-fps`, keeps a log, and fails on `SHADER ERROR` / `SCRIPT ERROR`.

Human checks were done by me; their observations are in my words *(translated from my Chinese)*. A headless run uses a dummy renderer and draws nothing, so no headless result below says anything about the look.

## Machine checks

| Check | Result | Evidence |
|---|---|---|
| Baseline before | 7 suites at 60 fps: a3_assets 22, audio 13, cast 11, flow 14, player 11, sound_triggers 11, wolf 13; 95 checks / 0 failures. Each 2D suite prints one engine "resources still in use at exit" line on shutdown (pre-existing, not a failure) | `logs/baseline-before/`, `7767726` |
| Baseline after | Same 95 checks / 0 failures, every check line identical to the baseline, after the driver (`be44384`), after the 3D build (`e7b4766`) and in the committed logs. Shutdown leak counts vary run to run | `logs/test_*_60fps.log` |
| Hurt-tint shader parses, names and types | `get_shader_uniform_list()` lists exactly `tint_color` (Color) and `intensity` (float, range 0–1); defaults read from the source text | `test_hurt_tint.gd`, `logs/test_hurt_tint_*fps.log` |
| Parse mutation (semicolon deleted) | `SHADER ERROR: Expected a ';'.`, empty uniform list, exit 1 | `logs/mutation-1-semicolon_60fps.log`, `9e5894d` |
| Rename mutation (`intensity` renamed in the shader only) | no `SHADER ERROR`; uniform-list and source-default checks fail, the other 15 pass; exit 1 | `logs/mutation-2-rename_60fps.log` |
| Driver at 30 / 60 / 144 fps, real game loop, real key events and real wolf lunges | 17 checks / 0 failures at each rate | `logs/test_hurt_tint_30fps.log`, `_60fps`, `_144fps` |
| R1 first value | 0.9833 at all three rates (minimum allowed 0.95 / 0.9667 / 0.9764) | same logs |
| R4 duration (game time) | 1.0000 s / 0.9833 s / 0.9861 s, within one frame (one physics step at 144) | same logs |
| R5 retrigger | a second wolf's lunge reached her during the state; hit ignored, `intensity` kept falling | same logs |
| R6 time scale 0.5 | 1.0 s game time, 2.0 s frame time | same logs |
| R7 pause | value held through 31 paused frames and resumed; 60 / 59 / 59 unpaused physics ticks from first tint to zero (summed frame time 1.0000 / 0.9833 / 0.9653 s, observation only; see below) | same logs, `b81bad4` |
| R8 / F4 | `intensity` 0.0 from the frame of an HP-0 fail (with `invulnerable` frozen at 1.0), a pit fall during the state, and a clear during the state | same logs |
| R9 | a reloaded scene starts at 0.0 with a different material object | same logs |
| Material wiring | `test_materials.gd`: 32 checks / 0 failures (shader paths, uniform values, texture paths, sampler hints from the source, import settings via ConfigFile, imported formats via `get_format()`, scene lights and environment) | `logs/test_materials_60fps.log`, `b6663b2` |
| Fresh import | deleted `walker-magic-zhefan/.godot`, reimported: 32 / 0, no `.import` file rewritten | `logs/test_materials_fresh-cache_60fps.log`, `5ebfa15` |
| `source_color` mutation (removed from `rock_frost.gdshader:16`) | `sampler-hints:...:texture_albedo` fails, exit 1; shader restored | `logs/mutation-3-source-color_60fps.log` |
| Texture data: curl ratio | `nor_gl` 0.1444 (OpenGL) / 1.8556 (DirectX); `nor_dx` 1.8556 / 0.1444. Bound map below 0.5 in OpenGL and above 1.5 in DirectX, thresholds from this calibration | `logs/calibrate_normal_check_60fps.log` |
| Import settings | explicit for all five textures (`d568b80`, hint PNG in `e7b4766`): rock maps `compress/mode=2`, normals `compress/normal_map=1`, others 2, mipmaps on, `detect_3d/compress_to=0`; hint PNG lossless, no mipmaps. Imported formats: DXT1 (albedo, roughness), RGTC_RG (normals), RGB8 (hint) | `MATERIALS.md` |

## Human checks

All captures were taken in-engine with the F9–F12 capture scenes in real windowed runs (`tests/capture/`, `f4123db`), from the rendered frame at viewport resolution (640×360). They are scripted captures: the key press is mine, the values are set by the capture script.

### Controlled values (hurt tint)

Driver disabled, values set from code, pixels sampled under the sprite's texture pixels (`captures/hurt_tint_pixels.json`, PNGs `hurt_tint_i0.0/0.5/1.0.png`):

| Pixel | `intensity` | Predicted | Measured |
|---|---|---|---|
| Hair (27, 18) | 0.0 | (232, 230, 240) | (232, 230, 240) |
| Hat (24, 7) | 0.0 | (58, 64, 160) | (58, 64, 160) |
| Hair | 0.5 | (244, 115, 120) | (243, 115, 120) |
| Hat | 0.5 | (157, 32, 80) | (156, 32, 80) |
| Hair | 1.0 | (255, 0, 0) | (255, 0, 0) |
| Hat | 1.0 | (255, 0, 0) | (255, 0, 0) |

The two red channels at 0.5 land exactly on .5 (243.5, 156.5); the GPU wrote both one step lower than my round-half-up. Within the ±1 the brief allowed for x.5 channels. Cause not investigated.

**`hint_range` and a value from code.** With pure red, every `intensity` of 1.0 or more gives (255, 0, 0), so a capture at 2.0 cannot tell clamped from unclamped. I captured 2.0 with `tint_color` set to grey (0.5) from code (`hurt_tint_grey_i2.0.png`): hair (23, 25, 15), hat (197, 191, 95). Prediction if not clamped (2 × 127.5 − stored): (23, 25, 15) and (197, 191, 95); if clamped: (128, 128, 128). (The capture script's own prediction field in the JSON uses the grey rounded to 128 and so says (24, 26, 16) and (198, 192, 96); the tint is 0.5, i.e. 127.5, which matches the measured pixels exactly.) So `hint_range` does not clamp a value set from code, and the 2D `source_color` colour uniform is used as stored (0.5 → 127.5), which the brief assumed.

**In-engine capture against an OS screenshot.** My Win+Shift+S screenshot of the same run is 1285×724: the window border plus 2× integer scaling. At the in-engine hair coordinate scaled by 2, the screenshot shows the hat colour (58, 64, 160), not the hair; the exact hair colour (232, 230, 240) is a few pixels away. Colours were not altered, coordinates were. I trust the in-engine capture, because its coordinates are the viewport's own and its pixels need no scaling or border offset. (The OS screenshot was compared during the session; it is not committed.)

### In play

Played the main scene (F5) and took wolf hits. *(translated from my Chinese)* The hurt effect in the game looked correct. After the hit that took HP to 0, the kneeling fail image was not red. The boundaries (collision, movement, the existing blink) are confirmed headlessly by the seven earlier suites, unchanged. A pit fall during the tint was checked headlessly only (R8).

### Hint experiment

`captures/hint_quads.png`, `captures/hint_pixels.json`; Linear tonemap, exposure 1.0, unshaded quads, Forward+:

| Texel | With `source_color`: predicted / measured | Without: predicted / measured |
|---|---|---|
| 64 | 64 / 64 | 137 / 137 |
| 128 | 128 / 128 | 188 / 188 |
| 192 | 192 / 192 | 225 / 225 |

All six as predicted. The quad with `source_color` shows the file's values, because the sRGB decode on sampling and the sRGB encode on output cancel.

### Interface sweep (frosted rock)

`captures/rock_sweep_<uniform>_<min|default|max>.png`, on `mat_rock_frosted` (default = the material's value). *(translated from my Chinese)*

| Uniform | Minimum | Maximum |
|---|---|---|
| `base_tint` (black / white) | the rock's base turns black; only the white frost patches float on a dark base | the natural grey-brown rock, brightest |
| `normal_scale` (0 / 2) | surface relief flattened; facets stay sharp but look smooth, like plastic | pits and grain much stronger, harder and deeper shading |
| `roughness_scale` (0 / 2) | very smooth; lit faces show a sharp white highlight | fully matte; the highlight spreads out and flattens |
| `frost_color` (black / white) | frost areas turn dark grey-black, like soot deposits | clean bright white snow, strongest contrast |
| `frost_amount` (0 / 1) | frost gone; the right rock matches the bare left rock | the whole rock covered in a white crust; the rock texture is almost gone and the bright parts are close to blown out |

Nothing broke the rendering (no missing-material pink, no black holes). `frost_amount = 1.0` loses almost all rock detail and becomes a near-white block, which hurts readability.

The audit predicted that the DXT1 roughness map (error up to 13 of 255) might show 4×4 blocks at the frost edge. Looking at `rock_sweep_frost_amount_default.png` (0.65) I saw a frost layer and no blocks, at 640×360.

### One shader, two materials

Measured from the captures (mean brightness of the non-background pixels, and pixels changed against the default capture):

| Capture | Dry rock (left) | Frosted rock (right) | Pixels changed, left / right |
|---|---|---|---|
| `rock_compare_default.png` | 67.9 | 84.0 | — |
| `rock_one_material_changed.png` (`normal_scale` 0 on the dry material only) | 66.1 | 84.0 | 6031 / 0 |
| `rock_compare_after_shader_edit.png` (my edit of `rock_frost.gdshader:28`, `* 0.5`) | 54.7 | 73.7 | 8225 / 8103 |

Editing one value in one material changed only that rock; editing one line of the shader changed both. Neither halved, because `Rock_Top` keeps its imported material and the frost colour is mixed in after line 28. The running shader's hash matched the edited file (`36f8bfdf…`); I reverted the edit afterwards (hash back to `f94674a8…`).

### Editor rewrites

On first opening the editor, `project.godot` lost two keys equal to their defaults (`audio/buses/default_bus_layout`, `window/stretch/aspect`). No behaviour changed; I restored the file with `git checkout` after closing the editor. No `.import` file was rewritten by the editor. The editor's normal-map preview showed "1024×1024 RGTC RedGreen8, 10 Mipmap", matching the audit.

## Inspect-and-revise cycles

1. **R7 at 144 fps** failed on summed frame time (0.9653 s). Revised the brief to measure unpaused physics ticks (`b81bad4`), then the test (`9072f67`): 59 ticks, no ticks missing.
2. **Use External** would have broken `test_a3_assets`. Revised the brief to scene overrides in a new scene (`47ce061`); earlier suites stayed at baseline.

## What no headless run shows

The look of either shader, whether red appears on screen, whether transparent pixels stay transparent, how the frost settles, whether the normal map lights the rock correctly, and real (not simulated) frame timing. Those are the human checks above.
