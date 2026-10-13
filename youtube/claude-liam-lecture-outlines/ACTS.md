# Acts and coverage map: Outlines

**What this is.** How the brief for this film lands in five acts: which item goes where, what was corrected, what was left out and why, plus the cast per act, the opening correction and terms card, the additions that are in neither the brief nor its source, and the cut line.
**Why.** Bear asked for films of at most 15 minutes, preferably about 10 (2026-10-13). A cut only works if every idea has a home, and a film is only as honest as its list of what it left out. This file is the record that nothing was dropped silently.
**Found.** Five acts, 41 body beats, 1,562 body words, about 10.7 minutes by the lint's deliberately pessimistic estimate. Every item of the brief has a home or a reason below. Six claims in the brief or its source were corrected (F14, F45, F54, F60, F63, F73 in `FACTCHECK.md`), and fifteen things in the film are in neither: the biggest is the second half of Act IV (sprite sheets), found by running the brief's claim that animated sprites just work.

## The source (third-party; nothing copied)

A long video course on 2D shaders in Godot (creator not named in the brief): about 24 minutes of it build an outline on a bird sprite. Bear's brief gives its content in his own words. This film follows its order of ideas (one offset, four directions, a pixel-size step, diagonals, a loop, a guard, padding) and teaches each in new words, with a different sprite and new, tested demonstrations. Nothing was copied or stored (`SOURCES.md`).

## Coverage of the brief

| Brief item | Where it goes | Note |
|---|---|---|
| The one idea: a pixel reads the texture at other addresses; a transparent pixel looks at its neighbors; the cost is one read per neighbor, per pixel | **Acts I and III**: the idea B03 to B05, the cost B22 | The cost is counted by construction and then timed in a labelled stress test |
| The newcomer's assumption (BIDEA) | **BIDEA** | Trigger kept verbatim; the line break sits before the trigger (a break inside it fails the lint's trigger check) |
| Terms card: neighbor, opaque, alpha, padding | **BDEFS** | Plus shader and texture (six terms). Wording for shader, texture and alpha is the GLOSSARY's; the other three are not in it |
| Act 1: read the alpha at one offset | **Act I**, B04 to B07 | The film steps to the right: the pixel reads the pixel on its right, which is also the first sign that the picture slides left (B28) |
| Add the four directions; keep it in range with `min(sum, 1.0)` | **Act I**, B09 and B10 | The light diagonals (sum of two) are shown first, so `min` is earned |
| Subtract the pixel's own alpha so only the outside edge is left | **Act I**, B08, reworked | **CORRECTED** (F14): multiply by one minus the pixel's own alpha. The subtraction form goes negative on a pixel with no opaque neighbor |
| Color it with a `vec4` line color via `mix` | **Act I**, B06 to B10; the uniform in B14 | `mix` has its own beat (B06) before the first shader |
| Act 2: `TEXTURE_PIXEL_SIZE` | **Act II**, B11 and B12 | B11 first shows why a fraction of the picture is the wrong unit; B12 shows the docs page |
| A thickness uniform: a step is exactly N pixels at any texture size | **Act II**, B13 and B16 | Measured widths 1, 2, 3, 4 and 8; B16 adds the sprite's own scale |
| Add the four diagonals | **Act II**, B17 | With the exact corner hole: t by t pixels per corner |
| Act 3: two nested `for` loops over -1 to 1 replace the copied lines | **Act III**, B18 to B21 | B21 is the proof: zero pixels differ at five thicknesses |
| Count the work: nine reads per pixel here | **Act III**, B22 | Nine in the loop plus one for the pixel itself: ten; the stress test is labelled wall-clock because the card's own timer is unreadable here |
| An `if (thickness > 0.0)` guard | **Act III**, B23 to B25 | `return` is not allowed in `fragment`; B25 shows what the guard does beyond saving work |
| The honest performance note: only `discard`'s cost is in the docs | **Act III**, B24 | **CORRECTED** (F45): the docs warn about `discard` and endless loops, nothing about `if`; a 2005 graphics book says a branch costs when neighbors disagree, and here they agree |
| Act 4: with opaque pixels at the texture's edge the outline has nowhere to go (a full-bleed image) | **Act IV**, B28 and B29 | B28 is the slide-and-cut probe that shows why a shader paints only inside its rectangle |
| The fix: pad the image (the GDScript: decompress, RGBA8, a larger `Image`, `fill`, `blit_rect`, an `ImageTexture`; run it and show the result) | **Act IV**, B30 and B31 | The function shown is the file that was run. **CORRECTED** (F54): `Image.create_empty`, not the deprecated `create` |
| Animated sprites work because the shader sees whatever texture is current | **Act IV**, B32 and B33 | **CORRECTED** (F60): true for separate frame images, false for a sprite sheet (UV spans the whole sheet); the fix is `REGION_RECT` |
| Act 5: larger thickness leaves gaps on diagonals with eight samples; show it, measure it, fix it with a ring | **Act V**, B34 to B37 | **CORRECTED** (F63): four reads pinch, eight reads bulge into a rounded square, and gaps appear only in thin parts; the ring of sixteen is the fix |
| `filter_nearest` for pixel art | **Act V**, B39 | **CORRECTED** (F73): that hint is for a sampler uniform; the node's own texture takes the node's filter, and the default is linear |
| Source: a bird sprite with padding and a nearest filter; uniforms `line_color` and `line_thickness` (0 to 1) with `const max_line_thickness = 4.0` | **LEFT OUT** | The film uses the series' own test sprite, and a thickness that is directly a count of image pixels (0 to 8, and 0 to 4 in the viewer's prompt): a 0 to 1 slider scaled by a constant adds a second unit to explain |
| Source: samples at `UV + vec2(0.005, 0.0)` | **Act I**, B07 uses 0.02 | 0.005 of a 128 px image is 0.64 px, too small to see; 0.02 is 2.56 px |
| Source: sampling to the right shows the picture to the left | **Act IV**, B28; the ghost-copy picture in B15 | Measured: reading 0.125 slides the picture 16.00 px |
| Source: switches to `TEXTURE_PIXEL_SIZE`; eight directions, then the `if`, then loops | **Acts II and III** | In the same order, with the loop and the guard each earning their place |
| Source: mixes `color.rgb` and `line_color.rgb` by `outline - color.a` | **B08 and B38** | The film mixes all four channels and shows what that does to a soft rim (B38) |
| Source: a slider wired to `set_shader_parameter` | **Act III**, B26 | **LEFT OUT** as a slider: the film shows the selected-unit key toggle and the call, which is the same call and the real use |
| Facts to verify: docs, loops, the padding failure and fix, the diagonal gap, nine reads | **FACTCHECK.md** | Every one is a row; the padding and gap were run |
| Captures: a thickness sweep video, a failure still, the fixed still | **CAPTURE-PLAN.md** C13, C29, C31 | Each is a short clip from a data-driven scene spec rather than a still, so the picture moves with the words |
| Cut line: the diagonal-gap act, the loop-cost beat | **Cut line** below | Act V also carries soft edges, the filter, modulate and the checks, which matter more to a working outline than the brush numbers, so the cut takes the brush beats and the loop-cost beat after three lighter ones |
| Other films cover: `texture()` basics, `for` and `if` syntax, sprite animation | **Recap only** | `texture` gets two beats (B04, B05); `for` and `if` are explained in one line each on screen (B19, B23); sprite animation is touched only for the sheet trap |

## Corrections to the brief and its source (full detail in FACTCHECK.md)

The subtraction form of the line color (F14); "ifs inside a shader are slow" (F45); the deprecated `Image.create` (F54); "animated sprites work because the shader sees whatever texture is current" (F60); "gaps on diagonals with eight samples" (F63); `filter_nearest` for the node's own texture (F73).

## Added: in neither the brief nor its source (each is checked in FACTCHECK.md)

1. The bigger-copy trick, measured: border 10 px at a tip, 3 px at a side (B02).
2. Each read as the whole picture slid by the step, the model behind thickness, brush shape and thin-part gaps (B15).
3. The step counts image pixels, so the line grows with the sprite (B16).
4. The exact corner hole of four reads: t by t pixels, four times (B17).
5. Godot refuses a `vec2` built from two whole numbers, with the real message (B20).
6. The loop and the eight reads compared pixel by pixel at five thicknesses (B21).
7. The labelled wall-clock stress test, and the honest note that the card's own timer is unreadable (B22).
8. Thickness zero is only zero with the guard on a soft-edged sprite: 224 pixels change without it (B25).
9. A selected-unit toggle from GDScript, the shared-material trap and the instance-uniform fix (B26, B27).
10. A shader paints only inside its rectangle: the slide-and-cut probe (B28).
11. Sprite sheets: UV spans the whole sheet, the stray line, and the `REGION_RECT` clamp (B32, B33).
12. Thin parts come apart into floating copies; the ring holds them (B37).
13. Soft edges: plain `mix` leaves the rim see-through, alpha 0.75 at worst (B38).
14. A shader that assigns color from the texture ignores the node's modulate (B40).
15. The five-item check list for any outline shader, the viewer's or an AI's (B41).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I Ask the Neighbors | the teal test sprite (a disc with two cream eyes) on the warm stage; the pixel grid (B03); the teal-to-indigo color strip (B06); the one shader's code card (B07 to B10) |
| II Pixel-Sized Steps | the strips of 32, 64 and 128 cells (B11); the test sprite at 1x, 2x and 3x (B16); the square sprite with two eyes (B17); the four-read code card (B13, B14) |
| III Say It with a Loop | the code card as it grows (eight reads, loop, guard); the square sprite from the end of Act II for the eight reads and the loop (B18, B19), the disc for the comparison (B21) and the soft disc for the guard (B25); the three-by-three block (B20); the bar chart (B22); the pairs of pixel grids with arrows (B23, B24); two units side by side (B26, B27) |
| IV Room to Draw | the trimmed round sprite and its padded copies (B29 to B31); the two-frame sheet and its frame 1 (B32, B33) |
| V Where It Breaks | three sprites, each with its own shader (B34); the stem sprite (B37); the soft rim close-up (B38, B39); the two faded sprites (B40); the checks table (B41) |

## Opening correction and terms

- **BIDEA**: the writer types "An outline is a bigger copy behind the sprite." and replaces "a bigger copy behind the sprite" with "a question about neighbors".
- **BDEFS** (prerequisites only): Shader, Texture, Alpha, Opaque, Neighbor, Padding. The terms this film exists to teach (mix, min, uniform, hint, texture pixel size, offset, for, instance uniform, region rect, clamp, varying, modulate) are earned in their beats, each defined on screen where it is first spoken, in the GLOSSARY's wording where it has one.

## Cut line

If the film runs long, cut in this order: the line-color beat (B14), the loop-cost beat (B22), the branch beat (B24), the modulate beat (B40), then the thin-part beat (B37) and the brush-number beat (B35). The corner beat (B17), the padding beats (B29 to B31) and the checks table (B41) stay: they are the proof and the payoff. Cutting all six removes 237 words, about 1.3 minutes; the current estimate is about 10.7 minutes, so no cut is needed.
