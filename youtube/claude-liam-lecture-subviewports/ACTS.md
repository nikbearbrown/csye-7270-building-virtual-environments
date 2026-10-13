# Acts and coverage map: SubViewports

**What this is.** How this film is built from its brief and its one third-party source: which part lands in which act, which parts are left out and why, the cast per act, the opening correction and terms card, the additions that are in neither the brief nor the source, the source claims that were corrected, and the cut line.
**Why.** The film must teach one idea (a picture drawn off to the side, then shaded a second time) in about ten minutes and no more than fifteen. That only works if every item has a home. This file is the record that nothing was dropped silently.
**Found.** Four acts, 40 body beats, about 10.5 minutes at Liam's pace (1,840 words, lint figure; the real length is known after the voice). All four acts the brief suggested are used. One thing the source does (a fade written as `COLOR.a = UV.x`) is corrected: on a transparent picture it turns the empty parts into a dark haze. Three things are in neither brief nor source and were found by running Godot: a transparent picture stores half-transparent pixels premultiplied, so a plain display darkens soft edges; a shader's UV belongs to the thing it draws; and the outer shader works in display pixels while the inner works in picture pixels.

## The source (third-party; nothing copied)

A long third-party course on 2D shaders in Godot (the SubViewport chapter is about 23 minutes). The creator is not named in the text Bear pasted. Only the ideas, in the order the brief lists them, are followed; every sentence is new, every demonstration was rebuilt and run (`SOURCES.md`).

## Coverage

| Source or brief item | Where it goes | Note |
|---|---|---|
| `SubViewport` with a size (512, then 256), a `ViewportTexture` on a `Sprite2D` | **Act I**, B02 to B06 | The default size 512 is the film's picture size (docs: `size = Vector2i(512, 512)`); the editor path, the five-line code path and "size is resolution" are all run |
| the origin, "centered" shifts what you see | **Act I**, B07, B08 | A centred sprite at (0, 0) shows a quarter of itself and no eyes (14,187 of 55,202 teal pixels, 0 eye pixels) |
| `transparent_bg` keeps empty areas empty | **Act I**, B09, B10 | Verified with and without; B10 adds what the source does not say: the picture stores premultiplied colour |
| an inner shader colouring the sprite (red and green in the source) | **Act II**, B13 | Rebuilt as a teal-to-gold gradient by the sprite's own UV; tested against the formula |
| an outer shader on the displaying sprite with `COLOR.a = UV.x` | **Act II**, B14, B15 | **CORRECTED**: whole colour times `UV.x` with `render_mode blend_premul_alpha` (FACTCHECK rows 35 and 36) |
| stripes: `pattern = fract(diagonal * line_count)`, `is_line = step(pattern, line_width)` | **Act III**, B21 to B24 | Rebuilt as diagonal, saw, stripe (`1.0 - step(width, saw)`), mask, with `count` and `width` as uniforms |
| moving with `diagonal - TIME * speed` | **Act III**, B25 | The formula with the `TIME` the shader saw predicts every probe |
| the `hsv_to_rgb` function from `K = vec3(1, 2/3, 1/3)` | **Act III**, B26 to B29, B30 | Written from the definition (a plateau pushed by thirds), not copied; checked against the engine's `Color.from_hsv` over 131,072 pixels (largest difference 0.002) and Python's `colorsys` over 640 columns (0.0019); the six pure colours are exact |
| pixelating the stripes | **LEFT OUT** | The pixelate function belongs to the Patterns film; the per-pixel idea behind it is B20 |
| the inner vertex shader: `scale_matrix`, `rotation_matrix` (angle = TIME * speed) | **LEFT OUT** | Matrices belong to the Matrices film. The sprite inside turns by a scripted rotation (always labelled "scripted"); the film's inner shader is a fragment gradient |
| the final outer vertex wobble on a subdivided `MeshInstance2D` | **Act IV**, B31 to B35 | With the upside-down catch and its fix (source claim confirmed: a negative height) |
| Brief: "Everything a texture can go on, the result can go on" | **Act IV**, B40 | Sprite, interface panel, 3D plane and a shader's sampler: one picture, four places, all run |
| Brief cut line: the hue act, the wobble mesh | the film's cut line (below) | The hue beats are cut first after the three small ones |

Left out on purpose (not in the source's SubViewport chapter or not needed for the idea): `SubViewportContainer` beyond its one job in B39 (passing input in); cameras and `Camera2D` inside a viewport (verified: a `Camera2D` at (0, 0) makes (0, 0) the middle of the picture, `verify1` X2, a good tip but one beat too many); the clear mode, `size_2d_override` and stretch, HDR 2D, MSAA and debug draw; the `ViewportTexture` local-to-scene rule and `viewport_path`; the rule to wait for `frame_post_draw` before reading the picture's image; 3D worlds inside viewports beyond the one 3D plane in B40; any speed claim (nothing about cost was measured, so B38 says only what the docs say).

## Corrections to the source (full detail in FACTCHECK.md)

- `COLOR.a = UV.x` on a transparent picture: the empty parts come out as a dark haze; multiplying fixes the empty parts, and under premultiplied storage the right form is the whole colour times the mask with premultiplied blending (rows 35, 36).
- "`transparent_bg` is needed to keep the original alpha": true, with a nuance the source misses: it also decides what the empty parts hold (alpha 1 of the clear colour, or alpha 0).
- The mesh orientation claim (negative y size) is **confirmed** in both renderers, with the mechanism: the quad's vertex that carries UV (0, 0) sits at y = +1, which is up in 3D and down on a 2D screen (row 57).

## Added: in neither the brief nor the source (each is checked, FACTCHECK.md)

1. Premultiplied alpha: a transparent picture stores half-transparent pixels already multiplied by their alpha; Mix darkens soft edges; Premultiplied Alpha is right (B10).
2. A shader's UV belongs to the thing it draws: the gradient turns with the sprite, the fade does not; the same stripe shader on the sprite itself turns with it (B16, B17, B25).
3. One fade across a group against a fade on each sprite (B18).
4. The inner shader works in the picture's pixels, the outer shader in the display's pixels (B20).
5. A picture inside another viewport can take a third shader (B37).
6. A standalone viewport receives no input; a container forwards it (B39).
7. Update Mode Once, and the default (B38).
8. A viewport has to be drawn to render: a hidden display stops it (run, not spoken).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I A Picture Off to the Side | the teal test sprite (blob with two cream eyes); the picture box (an outline square with its top-left origin); the screen frame; the display sprite |
| II Two Shaders, One Result | the same sprite and picture, now with an "inner shader" tag and an "outer shader" tag; the gradient (teal to gold) and the fade (0 to 1) as two thin ramp strips |
| III Stripes and Hue | the ramp strip (0 to 1) and the UV square; the saw plot; the colour wheel; the stripes on the same gradient blob |
| IV Wobble the Result | the rectangle with four terracotta corner dots; the grid mesh; the cream card with a teal frame carrying the blob; the chain token (the blob thumbnail) |

## Opening correction and terms

- **BIDEA**: the writer types "Shaders cannot see each other's work." and replaces "cannot see" with "can build on". (The brief proposed "Each node gets one shader." with "two shaders in a row"; that sentence reads wrongly once corrected and is not literally true, because each node still has one material. See CHECKS-REPORT.md.)
- **BDEFS** (prerequisites only, five): Shader, Texture, Viewport, UV, Alpha. The brief's Off-screen and Transparent are defined where the film teaches them (B02, B09); the terms the film exists to teach (SubViewport, ViewportTexture, premultiplied alpha, fract, step, hue, vertex, mesh, uniform, TIME, TEXTURE) are defined on screen in the beat that first speaks them, in GLOSSARY wording.

## Cut line

If the film runs long, cut in this order: the input beat (B39), the update-mode beat (B38), the three-in-a-row beat (B37), the per-pixel beat (B20), then the hue beats (B26 to B29), keeping the stripes at one colour. The origin and cut-off pair (B07, B08), the dark-edges beat (B10), the predict-and-reveal pair (B16, B17) and the wobble beats (B33 to B35) stay: they are the proof and the payoff. Cutting all of those saves about 1 minute 45 seconds at Liam's pace (B39, B38 and B37 about 37 s, B20 about 15 s, B26 to B29 about 53 s; B30 stays, with the stripes at one colour). Current estimate: about 10.5 minutes, so no cut is needed.
