# Capture plan: Outlines

**What this is.** Every Godot render and screenshot the build session must record for this film: the scene spec to play, the shader files, the values over time, the length, the renderer, what is on screen at the 50 and 85 percent marks, the route used and the result already verified. Nothing is recorded yet; every number comes from planning runs in `evidence/planning-checks/`.
**Why.** Films show only what was really done and recorded. This is the list of things to really do, written so a medium-effort session can do them without further judgment, and without the editor.
**Found.** 27 Godot captures (26 clips, 1 still) and 1 docs screenshot. None needs the editor and none reads window pixels, so **every capture uses the SubViewport native-size route** (a 3840 by 2160 SubViewport over the 1280 by 720 canvas): `route-summary.txt` renders all 27 specs both ways and finds 0 differing pixels in 55 frame pairs. Each capture is a small JSON spec played by a reference scene player (`scene_player.gd`), so the build needs one harness option, not 27 scripts.

## Conventions for all captures

- **Route.** Native-size SubViewport (3840 by 2160 over the 1280 by 720 logical canvas, `size_2d_override` with stretch). The other route in the series (1920 by 1080 at scale 1) is for shaders that read window pixels (`FRAGCOORD`, `SCREEN_PIXEL_SIZE`, `LIGHT_POSITION`); **no shader in this film does**: every neighbor offset is in texture units (`TEXTURE_PIXEL_SIZE`, `UV`). `evidence/planning-checks/route_check.gd` is a working example of the route with the scene player, scripted key events included.
- 30 fps, Forward+ (Apple M4 Pro, Godot 4.7.2), stage color `#D9D5CA`, nearest filter on every sprite except the linear ones in C39 (its left sprite is linear until 9.86 s, then nearest). Offline at a fixed tick rate: nothing here says anything about real-time frame rate. Label scripted input (C26) "scripted input".
- Output to `runtime/remotion/public/godot-outlines/` as `<spec id>.mp4` (clips) or `<spec id>.png` (stills), the names the lanes use. A still is one frame at 50 percent of the spec's duration.
- **Timing.** Spec times are planned from the narration at 0.34 s per word. The build voices first, then plays every clip stretched to its beat's measured audio: `scene_time = audio_time x spec.duration / measured_audio`, so a change planned on a word stays on that word whatever the real pace. Keyframes are never edited by hand.
- **The scene player is a pure function of time**: `player.setup(spec)` once, then `player.at(t)` for any t, any order (scripted key events in C26 fire once, in the first `at(t)` that reaches them, so render that clip in one pass from t = 0).
- Environment: `OUTLINE_FILM_DIR` must be the film's absolute folder; the player reads shaders from `lab-shaders/`, then `evidence/planning-checks/shaders/`.

## The contract: spec files and the player

`evidence/planning-checks/scenes/<ID>.json`: `id`, `beat`, `canvas` [1280, 720], `duration` (seconds), `fps` 30, `still`, `note`, `sprites[]`, optionally `script` (a GDScript file attached to a holder node, C26) and `input[]` (`{t, key}`).

A sprite: `texture` (`kind` blob, blob_soft, mascot, crate, plus, sheet; `crop`, `pad`, `cut` [x, y, w, h], `white`), `scale`, `center` (canvas pixels), `filter` (nearest, linear, default; or a stepped list of them), `shader` or `shader_at` (a stepped list of shader names; null = no material), `uniforms` (a constant or `{"keys": [[t, v], ...], "interp": "step" or "linear"}`; colors as [r, g, b, a] floats), `modulate`, `visible`, `hframes` and `frame`, `region`, `frames` (separate frame images), `share_with` and `own_from` (two nodes on one material until a time), `instance_uniforms` and `instance_from` (per-node values on a shared material).

Files the build needs, all in `evidence/planning-checks/`: `scene_player.gd`, `ol_lib.gd` (texture and material factory), `padding_snippet.gd` and `select_snippet.gd` (the exact code shown on screen), the shaders in `lab-shaders/`, and the 27 specs.

**One harness addition, about 40 lines (`S/lab/capture_spec.gd` if `S/lab/capture.gd` cannot already drive a scene player):** load the spec, build a `SubViewport` 3840 by 2160 with `size_2d_override` 1280 by 720 and stretch on, add `scene_player.gd` inside it, set `player.input_viewport` to the SubViewport (scripted keys must be pushed into it, not into the root window), call `setup(spec)`, then for frame i call `player.at(i / 30.0 x spec.duration / clip_seconds)`, `await process_frame`, `RenderingServer.force_draw(false)`, save the SubViewport texture as PNG; `ffmpeg` joins the PNGs into the MP4 the way the series' harness does. Do not await `frame_post_draw` (it can stall). Stills: one frame at `0.5 x duration`. The same traps as in `COMPONENT-SPECS.md` apply (a SubViewport needs its own size override; keys released between runs).

## Godot captures

"Steps" below means the value holds until the next time, then jumps. Times are spec seconds (before stretching). 50 and 85 percent are fractions of the spec's duration.

| ID | Beat | Shader (in `lab-shaders/`) | Sprites and values over time | Length | On screen at 50 % / 85 % | Verified result to reproduce (canvas px = image px x scale) |
|---|---|---|---|---|---|---|
| C01 | B01 | `08-loop` | the sprite at 4x; no material until 3.74 s, then the shader at thickness 3 | 11.6 s | line on / line on | 0 outline px before the switch; a 12 px line (3 x 4) after |
| C02 | B02 | none | a plus sign at 6x; a white copy, modulated indigo (0.25, 0.25, 0.75), behind it grows from 6x to 7.2x between 4.08 s and 6.46 s | 13.9 s | copy settled / copy settled | border 29 px at an arm's tip, 9 px along its side (ratio 3.2); at 2x and 2.4x 10 px and 3 px |
| C07 | B07 | `02-paints-the-sprite` | the sprite at 4x; no material until 6.12 s, then the first try switches on | 13.6 s | the whole sprite blue except its right edge / the same | 0 outline px before the switch; then 71,112 of 74,192 sprite px line coloured (95.8 percent; 4,406 of 4,637 = 95.0 at 1:1) |
| C08 | B08 | `02-paints-the-sprite`, then `03-one-question` from 2.72 s | the sprite at 4x; the blue sprite of the first try, then the fix switches on | 13.3 s | a line on the left of the sprite only / the same | before the switch 71,112 of 74,192 sprite px line coloured; after it 3,080 outline px, all left of the centre, none on the sprite (231 at 1:1) |
| C09 | B09 | `03-one-question`, then `04-lighter-diagonals` from 0.68 s | the sprite at 4x; the one-sided line, then the four reads switch on | 11.6 s | a ring with lighter diagonal stretches / the same | before: 3,080 px, all left; after: ring 8,992 px, 3,328 of them (37.0 percent) (128, 128, 255) (252 of 672 at 1:1) |
| C10 | B10 | `04-lighter-diagonals`, then `05-four-questions` from 5.78 s | the sprite at 4x; the ring with lighter stretches, then the cap switches on | 13.6 s | a ring of one blue / the same | wrong-colour px 3,328 of 8,992 before, 0 after |
| C13 | B13 | `06-pixel-steps` | 4x; thickness steps 1 (0 s), 2 (6.8 s), 3 (7.14 s), 4 (7.48 s) | 12.9 s | thickness 1 / thickness 4 | line widths 4, 8, 12, 16 canvas px (thickness x 4) |
| C14 | B14 | `06-pixel-steps` | 4x, thickness 3; `line_color` steps indigo (0.25, 0.25, 0.75) at 0 s, magenta (0.8, 0.25, 0.55) at 8.5 s, amber (0.95, 0.7, 0.1) at 9.52 s | 12.9 s | indigo / amber | ring colours (64, 64, 191), (204, 64, 140), (242, 178, 26) |
| C16 | B16 | `06-pixel-steps` | thickness 2; scale steps 1 (0 s), 2 (4.76 s), 3 (8.16 s) | 13.9 s | 2x / 3x | line widths 2, 4, 6 canvas px |
| C17 | B17 | `06-pixel-steps` (left), `07-eight-reads` (right) | the square sprite at 4x at x = 340 and 940; thickness steps 1 (0 s), 2 (1.7 s), 3 (4.76 s) | 11.9 s | thickness 3 / thickness 3 | the eight-read ring has 64, 256, 576 more canvas px than the four-read ring at thickness 1, 2, 3 (4 x t x t x 16); the corners of the left one are empty |
| C18 | B18 | `06-pixel-steps`, then `07-eight-reads` from 2.72 s | the square sprite at 4x, thickness 3; four reads, then the eight reads switch on | 8.8 s | a complete frame / the same | 12,288 line px before, 12,864 after: 576 more (4 x 3 x 3 x 16), the four corner holes |
| C19 | B19 | `08-loop` | the square sprite at 4x, thickness 3 | still | a complete frame | 12,864 line px, 0 pixels different from C18's final frame |
| C21 | B21 | `07-eight-reads` (left), `08-loop` (right) | the sprite at 3x at x = 340 and 940; thickness steps 1 (0 s), 2 (2.72 s), 3 (3.06 s), 4 (3.4 s), 8 (4.08 s) | 11.2 s | thickness 8 / thickness 8 | 0 pixels differ between the two sprites at 1, 2, 3, 4 and 8 |
| C25 | B25 | `08-loop` (left, no guard), `09-guard` (right) | the soft-edged sprite at 4x; thickness steps 2 (0 s), 0 (3.4 s) | 11.9 s | thickness 0 / thickness 0 | at thickness 2 the two draw the same; at 0 the left keeps a tinted rim: 3,584 canvas px differ (224 x 16), the right none |
| C26 | B26 | `09-guard` | the sprite at 4x with `select_snippet.gd` on a holder node; scripted key (SPACE) at 3.06 s and 5.78 s | 13.3 s | plain sprite (after both keys) / plain sprite | outline px 0 at 0.05 s, 10,112 at 3.36 s, 0 at 6.08 s; thickness reads back 0.0 |
| C27 | B27 | `09-guard`, then `13-instance` from 9.18 s | two sprites at 3x (x = 340 and 940) on one shared material; left thickness 0, then 2 at 6.46 s (both outlined); from 9.18 s an instance uniform: left 2, right 0 | 14.3 s | both outlined / only the left | outline px left and right: 0 and 0 at 0.3 s; 5,688 and 5,688 at 6.76 s; 5,688 and 0 at 9.48 s |
| C28 | B28 | `01-look-right` | the sprite at 4x; `look` rises 0 to 0.4 between 0.8 s and 8.28 s | 13.9 s | look 0.33, cut flat / look 0.4 | the left-most solid column is x = 416 at look 0.14, then x = 384 (the rectangle's left edge) at 0.28 and 0.42, where the uncut sprite would start at 343 and 273 |
| C29 | B29 | `08-loop` | the sprite trimmed to its shape (77 x 77) at 4x; thickness 0 to 6.12 s, rising to 4 at 8.02 s | 13.3 s | thickness about 1 / thickness 4 | axis widths 0, 0, 0, 0 at the end (nothing where the shape touches the edge) |
| C31 | B31 | `08-loop` | three trimmed sprites at 3x (x = 240, 640, 1040), padded 0, 2 and 4 by the `add_padding` function; thickness 0 to 0.6 s, rising to 4 at 1.8 s | 14.3 s | thickness 4 / thickness 4 | line widths 0, 6, 12 canvas px (padding x 3) |
| C32 | B32 | `08-loop` on the right panel | left: the whole two-frame sheet at 3x, no shader; right: frame 1 at 4x; thickness 0 to 8.84 s, rising to 4 at 13.22 s | 16.0 s | no outline yet / stray line on frame 1's left edge | the strip of line pixels at the frame's left edge: 0 before, 4,096 (16 x 256) after; the ring in the frame 14,080 px |
| C33 | B33 | `08-loop`, then `12-sheet-safe` from 6.62 s | the same two panels; thickness 4 throughout | 13.9 s | clamp on, strip gone / the same | stray strip 4,096 px before, 0 after; the disc's own ring 9,984 px before and after |
| C34 | B34 | `06-pixel-steps`, `07-eight-reads`, `10-ring` | the sprite at 3x three times (x = 215, 640, 1065); thickness 1 to 8 between 0 and 2.16 s | 9.9 s | thickness 8 / thickness 8 | axis 24.0 px each; diagonal 15.3, 34.2, 24.2 px (ratios 0.64, 1.42, 1.01) |
| C36 | B36 | `10-ring` | the sprite at 4x; thickness 1 to 8 between 0 and 4.06 s | 13.9 s | thickness 8 / thickness 8 | axis widths 32 px (8 x 4) |
| C37 | B37 | `08-loop` (left), `10-ring` (right) | the stem sprite (disc, 3 px stem, ball) at 4x at x = 330 and 950; thickness 1 until 3.74 s, rising to 8 at 6.42 s | 11.9 s | thickness about 6.8 / thickness 8 | on image row 17 at thickness 8: left `.....................###.....SSS.....###....................` (five empty px each side), right `....................#########SSS##########..................` |
| C38 | B38 | `06-pixel-steps` (left), `06-pixel-steps` then `11-soft-edges` from 10.54 s (right) | a 12x look at a 32 x 32 piece of the soft sprite's rim (crop at 20, 20); thickness 1 | 13.3 s | both pale and see-through / the right solid, the left still pale | 7,056 canvas px of the right panel change at the switch, none of the left; alpha 0.75 to 0.95 (mean 0.82) on all 224 rim px with plain mix, 1.00 with the composite (`soft-summary.txt` B1) |
| C39 | B39 | `08-loop` | a 12x look at the hard sprite's rim, thickness 1; both on the default linear filter, the left switches to nearest at 9.86 s | 13.9 s | both blurred / the left crisp, the right blurred | blurred px in the left panel 10,342 before and 0 after, the right 10,342 throughout; half-transparent px over the whole sprite at 2x: 0 with nearest, 2,008 with linear (`filter-summary.txt`) |
| C40 | B40 | `06-pixel-steps` (left), `14-modulate` (right) | the sprite at 4x twice, thickness 2; the node's modulate alpha 1 until 4.76 s, falling to 0.5 at 8.9 s | 13.3 s | alpha about 0.77, both fading / alpha 0.5 | before the fade both have 74,192 sprite px and 7,104 line px; after it the left centre pixel is (95, 163, 145), unchanged, the right (156, 188, 173), half-faded teal on the stage |

Notes the build must keep: the 12x close-ups (C38, C39) are crops of the texture drawn at 12x with nearest filtering, except C39, where both sprites start on the node's default linear filter on purpose (the left one switches to nearest, the right one stays linear). C39's counts are for the whole sprite at 2x, not for the crop (the on-screen label says so). The gaps of the thin-part clip (C37) depend on the row: row 17 shows them, row 21 does not (the diagonal reads reach the ball and the disc).

## Screenshot

| ID | Beat | What | How |
|---|---|---|---|
| D1 | B12 | The Godot "Canvas item shaders" page (`https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html`), scrolled to the **fragment** built-ins table, 1600 x 900 at device scale 2.4; the camera pushes in on the `TEXTURE_PIXEL_SIZE` row (the page lists it in the vertex, fragment and light tables: use the fragment one, next to `REGION_RECT` and `UV`) | Playwright (the `BrowserCapture` convention); caption with the capture date |

## Editor frames

None. Every beat is shown with a render, a diagram, the real code, or the docs page.

## Not captured on purpose

No GPU timing (the engine's counter reads 0.0 here, FACTCHECK F37). The stress-test bars in B22 are drawn by Manim from `cost-summary.txt`, not recorded. No real-time frame-rate claim anywhere.

## What could not be verified before the build

- No frame has been rendered at 3840 by 2160 yet; the route was verified by sampling the big frame at the centre of every 3 by 3 block against the 1280 by 720 render (identical), and the 4K look at the end (edges of 12x sprites) is the build's first visual check.
- The stretch to measured audio is arithmetic on the spec's times; the build confirms each cue still lands on its word.
- Gate T on real captures was not run (the build owns it); the sprite is teal on a warm grey stage on purpose, and the ring is indigo, mid-tone and not near ink.
