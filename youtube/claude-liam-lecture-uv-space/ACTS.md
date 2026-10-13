# Acts and coverage map: UV Space

**What this is.** How this film is built from its brief and from the third-party course it follows: which part lands in which act, which parts belong to other films, and which are left out, each with a reason. Also the cast per act, the opening correction, the terms card, the additions that are in neither source, and the cut line.
**Why.** Bear split a seven-hour course into films of at most 15 minutes, preferably about 10 (2026-10-13). A split only works if every idea has a home. This file is the record that nothing was dropped silently, and that the one wrong explanation in the source (why a circle turns oval) is corrected on purpose.
**Found.** Five acts, 42 body beats, about 10.3 minutes. Every item of the brief is in an act; nothing the brief asked for is left out. Four things in the film are in neither the brief nor the source (list below), and three source claims were corrected or qualified. No editor frames are needed: every Godot picture is a Shader Lab render of a tested file.

## The source (third-party; nothing copied)

A long third-party course on 2D shaders in Godot (the YouTube cut of a paid course; its creator is not named in the text Bear gave the series). The brief describes what it says about `UV` in about 35 minutes across its UV-control, texture, vertex-basics and canvas chapters. Treated as a claim to check, not a fact. Nothing was stored or reused: every sentence, number and demonstration here is new and was run in Godot 4.7.2 (see `SOURCES.md`).

## Coverage of the brief

| Brief item | Where it goes | Note |
|---|---|---|
| The one idea: `UV` is the address you look up; change it before you look and the picture moves, zooms, tiles or mirrors; the picture goes the other way | **Acts I and II** (B01, B07, B09 to B11); recap line 2 | Shown first as a hook (B01), then measured (B09 to B11) |
| BIDEA: "UV says where a pixel is on the screen" corrected to "the shape" | **Opening** | Exactly the brief's `BIDEA_TEXT` |
| Terms card: Coordinate, Axis, Texture, Aspect ratio | **Opening** (Texture) and **earned in acts** (coordinate = address, B02; aspect ratio, B32) | Axis is not spoken at all. The card also holds Shader, Pixel, Vector and Uniform, because the viewer has seen no other film |
| Act 1: `UV` recap, y points down, `texture(TEXTURE, UV)` reads the picture at that address | **Act I** B02 to B06 | The address map is the Godot tutorial's own example, `vec4(UV, 0.5, 1.0)`, with blue held at half so the top-left corner is not black (GATE T) |
| Act 2: multiply by 2 shrinks to a quarter and tiles or clamps | **Act II** B13 to B15 | The area ratio was measured: 0.2506 |
| Act 2: subtract 0.25 moves right and down | **Act II** B09 to B12 | Probes for U alone and for U and V together |
| Act 2: add `TIME * 0.1` and it scrolls | **Act II** B17 | Speed and direction measured in one process: about 0.10 pictures per second (0.100 on three steps; 0.095 to 0.105 in an earlier run), left |
| Act 2: the rule, change the address one way and the picture goes the other | **Act II** B10, B11, B18 | Worked numbers (B10), both directions (B11), a four-move table (B18) |
| Act 2: repeat (`repeat_enable` on a sampler uniform; `CanvasItem.texture_repeat` for the node's own texture); without repeat the border pixels stretch | **Act II** B15, B16; **Act V** B36, B37 | Defaults, clamp, repeat and mirror all run; the docs wording is quoted in FACTCHECK |
| "Show it with a texture that has an obvious corner" | **Acts I to III** (the sprite: eyes above the middle; the address map) | The red-green gradient as a *texture* has a black corner, a known GATE T risk, so it is used only in probes. The teal sprite with eyes is the picture, and the checker is used where an opaque edge is needed |
| Act 3: `UV * 2.0 - 1.0` puts zero in the middle, range minus one to one | **Act III** B22 | Corners and middle labelled; signs and range measured |
| Act 3: `length()` of it is a circle | **Act III** B23 | A teal disc whose radius sweeps |
| Act 3: `abs()` mirrors a shape so one formula draws both sides | **Act III** B24 to B26 | Drawn with the sprite's own cast: a face with two eyes, one test |
| Act 4: on a 2:1 rectangle a circle from `distance(UV, vec2(0.5))` is an ellipse; the real cause is that `UV` runs 0 to 1 on both axes whatever the proportions; measure the ellipse from a Lab PNG | **Act IV** B28 to B31 | The film's capture is a 16:9 window (512 by 288, ratio 1.78); the 2:1 case (512 by 256) was measured too and is in FACTCHECK |
| Act 4: scale one axis by the aspect ratio; verify `TEXTURE_PIXEL_SIZE` or `SCREEN_PIXEL_SIZE` for a ColorRect and for a sprite; show a circle | **Act IV** B32 to B35 | Four sources of aspect measured on two nodes; only a uniform is right everywhere |
| Act 5: outside 0 to 1 you get repeats or stretched border pixels; mask them with `step` (four `step`s multiplied); show the artifact and the fix | **Act V** B36 to B40 | The mask is written as two vector `step`s whose four components are multiplied |
| Source: visualizes `UV` as red and green | **Act I** B04 | |
| Source: scales it (`UV * 2` shows only the top-left quarter) | **Act II** B13, B14 | CORRECTED / qualified (below) |
| Source: offsets with `- vec2(0.4, 0.1)` | **Act II** B09, B12 | Same idea with 0.25 so the numbers are easy to follow; no source number is reused |
| Source: explains the inversion with worked numbers | **Act II** B10 | New numbers (0.5 reads 0.25) |
| Source: enables texture repeat to see tiles | **Act II** B15, B16 | |
| Source: masks borders with `step(vec2(0.0), scaled_uv)` and `step(scaled_uv, vec2(1.0))` | **Act V** B38 to B40 | Re-derived and run |
| Source: centers with `2.0 * UV - 1.0` and works three corner examples | **Act III** B22 | All four corners and the middle are shown at once |
| Source: `abs(UV.x)` to mirror a rectangle | **Act III** B25, B26 | Face instead of rectangle; `abs` applied to the centered x |
| Source: builds the aspect correction by multiplying x by a ratio before measuring a distance | **Act IV** B32, B33 | |
| Source claim: the oval is because fragments are stretched, non-square "potential pixels" and pixels are always squares | **Act IV** B31 | CORRECTED: not the reason |
| Source claim: moving `UV` right moves the picture left | **Act II** B11 | PASS, with probes in both directions |
| Facts: docs for `UV` in `canvas_item` (vertex and fragment), `TEXTURE_PIXEL_SIZE`, `SCREEN_PIXEL_SIZE`, repeat hints, `CanvasItem.texture_repeat` | FACTCHECK rows | Quoted with URLs, read 2026-10-13 |
| Facts: filter hints | **LEFT OUT** | The docs list `filter[_nearest, _linear][_mipmap][_anisotropic]`; sampling quality belongs with texture and color, not with the address |

## Corrections and qualifications of the source (full detail in FACTCHECK.md)

1. The oval on a wide shape is not caused by stretched fragments: it is the address, which spans 0 to 1 on both sides, so one step covers 64 pixels across and 36 down on a 640 by 360 shape (rows 43 to 46).
2. "Scaling `UV` by 2 shows only the top-left quarter" is true of the address drawn as a colour (the ramp fills the quarter, the rest reads 1.0). For a picture, the whole picture is shown at half size in that quarter and the rest shows edge pixels or repeats (rows 22 to 25).
3. The docs' note that `TextureRect` is not affected by `texture_repeat` is about its own tiling mode: for a shader that reads `TEXTURE` outside 0 to 1, the setting does apply on a `TextureRect` (measured). The film names no node type for this (row 29).

## Added: in neither the brief nor the source (each is checked)

1. Zooming about the corner against zooming about the middle, and the three-step fix (B19 to B21). The brief only says `UV * 2.0 - 1.0` centers; this gives the reason the viewer needs it.
2. A flip by a negative scale on the centered address, on V (seen) and on U (measured) (B27).
3. The measured comparison of four sources of the aspect ratio on a `ColorRect` and a `Sprite2D`, and a script that keeps the uniform in step with a resize (B33 to B35).
4. The opening shader decoded line by line at the end (B41), and a four-row table of the usual causes when a UV effect looks wrong (B42).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I The Address Book | the UV square with its (u, v) dot; the teal test sprite as the picture; the window outline over the picture card |
| II Move Where You Look | the 0 to 1 picture ruler with its teal dot; the sprite inside its fixed square (ringed); the sprite's copies |
| III Center and Mirror | the pivot dot; the centered square with minus one to one labels; the sprite; the teal head with two white eyes |
| IV Fixing the Squash | the wide 16:9 rectangle (the shape); the teal disc, then oval, then circle; the address cell, 64 by 36 pixels |
| V Staying Inside the Picture | the checker picture with its solid edge; the step plot; the gate; the opening shader and its nine copies |

## Opening correction and terms

- **BIDEA**: the writer types "UV says where a pixel is on the screen." and replaces "the screen" with "the shape" (the brief's exact text).
- **BDEFS** (prerequisites only): Shader, Pixel, Texture, Vector, Uniform. Wording from `../_godot-shaders-series/GLOSSARY.md`. Terms this film exists to teach (UV and address, fragment, TIME, mask, step, aspect ratio, absolute value, length) are defined on screen in the beat that first speaks them.

## Left out on purpose

- `floor`, `fract`, tiling cells, pixelation: the patterns film. `smoothstep` edges, shapes other than a disc: the shapes film. Sine and waves: the time-and-waves film. Rotation: the trigonometry film.
- `SCREEN_UV`, world coordinates, matrices: the space films. `REGION_RECT` and sprite regions: not needed for an address on a whole picture.
- Texture filtering and mipmaps: the textures film. Noise: the noise film.
- Editor frames: none are needed (the one editor-adjacent beat, `texture_repeat`, shows the real docs page instead).

## Cut line

If the film runs long, cut in this order: the node-setting beat (B16), the transparent-border beat (B37), the stretched-pixel beat (B31), the fold drawing (B26), and the gate drawing (B39, so the mask takes one beat). Each repeats or decorates an idea another beat carries. The reversal beats (B09 to B11), the centered zoom (B19 to B21), the oval and its fix (B28, B29, B32, B33) and the mask result (B40) stay: they are the proof and the payoff. Current estimate: about 10.3 minutes, so no cut is needed.
