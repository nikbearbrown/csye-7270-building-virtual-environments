# Acts and coverage map: Soft Edges, Glow and Noise

**What this is.** How the brief for this film (its one idea, five suggested acts, source claims and facts to verify) lands in five acts: which item sits in which act, which is left out and why, what the film adds that the source does not have, the cast per act, the opening correction and terms, and the cut line.
**Why.** Bear split a long course and a short intro into films of at most 15 minutes, preferably about 10 (2026-10-13). A split only works if every idea has a home. This file is the record that nothing was dropped silently.
**Found.** Five acts, 42 body beats, about ten minutes by the lint's ceiling estimate. Every item of the brief is covered except the vertex pulse (left out on purpose, with a measured reason). Two source claims were corrected (smoothstep's arithmetic, what glow needs) and a third is parked (the vertex pulse). Thirteen things in the film are in neither the brief nor the source, all checked (list below); the biggest is that glow in 2D needs the environment's background mode set to Canvas.

## The source (third-party; nothing copied)

A third-party video build of an energy-shield effect in Godot 2D, about 25 minutes of it (the brief's description; the creator is not named in what Bear pasted). The film follows its order of ideas (a main circle, a soft edge with a width control, a highlight, two colors, a glow multiplier, a scrolling noise texture) and rebuilds every demonstration in new words and new, tested shaders: a teal "bubble" on the Lab's stage. The short intro video's noise-texture reveal (named in the brief) is in Act IV.

## Coverage

| Brief item | Where it goes | Note |
|---|---|---|
| The one idea: `smoothstep` is a hard `step` with a defined start and end | **Act I**, B01 to B10 | Same disc, `step` then `smoothstep`; the band is the softness; the S-curve drawn true |
| BIDEA "A soft edge needs a blur." with the correction "a blur" to "a ramp" | **BIDEA** | The writer types it and replaces `a blur` with `a ramp` |
| Terms card: mask, falloff, noise, HDR | **BDEFS and the acts** | Card: ramp, mask, UV, uniform, alpha (prerequisites). Falloff (B11), noise and texture (B24), HDR (B35) are earned in their acts with the definition on screen where first spoken. `step`, `distance` and `smoothstep` get their GLOSSARY or docs wording on screen (B02, B03, B05) |
| Act 1: `step` against `smoothstep(a, b, d)` on `distance`; the band; a width uniform; draw the true S-curve and give one number | **Act I**, B01 to B08 | The one number is 0.028 at ten percent of the way along (the source's 0.1 is the straight-ramp answer) |
| Act 2: `1.0 - distance(UV, spot)`, `pow(spot, 3.0)`, multiply by the main shape | **Act II**, B11 to B15 | Plus a vec2 dial that moves the spot (B16) |
| Act 3: main shape plus highlight; the order-of-operations bug with real numbers; `source_color` colors | **Act III**, B17 to B23 | The bug is `a + b * c` against `(a + b) * c` with a brightness dial: green 0.70 against 0.95 at the highlight's centre, measured. The highlight is added to the body color (`body + highlight * mask`) |
| Act 4: sampler2D noise with `repeat_enable`, seamless NoiseTexture2D, `texture(noise, UV + vec2(TIME * 0.1, 0.0)).r` into the alpha; what happens without repeat and without seamless | **Act IV**, B24 to B30 | Both failures are run, not described: streaks without the hint (B28), a seam without Seamless (B29, B30) |
| Noise-texture reveal from the short intro video | **Act IV**, B31, B32 | A threshold against a uniform; the pace is not linear (measured) |
| Act 5: multiply a color by five; neither on, HDR 2D only, HDR 2D plus glow in a WorldEnvironment; report what each looks like | **Act V**, B33 to B42 | Run all three and found a fourth condition: the environment's background mode must be Canvas (B37); the last beat puts every layer together (B42) |
| Source: "multiply by five and it glows" | **CORRECTED**, B33, B34, B38 | True only when the project holds the number (HDR 2D), the environment turns it into light (glow on, Canvas) and there is dark around the shape |
| Source: smoothstep "limit one 0, limit two 10, value 1 returns 0.1" | **CORRECTED**, B06 | 0.1 is the straight-ramp answer; smoothstep(0, 10, 1) is 0.028 |
| Source: vertex pulse `VERTEX += normalize(VERTEX) * sin(TIME) * amount` | **LEFT OUT** | A vertex-stage idea that belongs in a film about the vertex function. Measured for the record (FACTCHECK 85): it widens a centred Sprite2D outward, but on a ColorRect, whose origin is its corner, `normalize(VERTEX)` of the corner (0, 0) is undefined and the whole rectangle disappeared |
| Source: an inner gradient by multiplying with the distance | **FOLDED** into B15 and B18 | The idea (a mask multiplied by a distance ramp) is exactly "multiply keeps both"; the film's bubble gets its depth from the highlight instead |
| Source: the width halved to cap at 0.5 | **LEFT OUT** | An implementation detail of one rig; the film's width is `0.4 - width` with a `max` guard and a range that ends at 0.4 |
| Other films cover: textures and `source_color` in depth; the `smoothstep` function table; sine scrolling | **Touched, not taught** | `source_color` appears for color uniforms and in the HDR 2D washed-out-color beat (B19, B40); the scroll uses TIME without a sine |

## Corrections to the source (full detail in FACTCHECK.md)

smoothstep 0.1 against 0.028 (rows 12, 14); "multiply by five and it glows" (84); the vertex pulse is not general (85).

## Added: in neither the brief nor the source (each is checked, FACTCHECK.md)

1. `smoothstep` with equal edges, or with swapped edges, is undefined in the docs; on this Mac both "work" in both renderers (B09, B10).
2. A `hint_range` does not stop code from sending a value outside it, so guard with `max` (B09).
3. A power of a negative number is undefined; a fractional power gave NaN on this Mac, an odd whole power did not; the NaN drew as nothing, which is why it hides (B14).
4. The falloff does not stop at the shape's edge until it is multiplied by the shape's mask (B12, B15).
5. A vec2 uniform moves the highlight (B16).
6. Adding to a lookup moves the picture the other way, by exactly the amount added: 0.125 gave a 32 px shift to the left (B27).
7. Without `repeat_enable` a lookup past the edge returns the edge pixel: streaks (B28); a plain `NoiseTexture2D` has a wrap seam 14 times a normal step; Seamless removes it for a small cost in contrast (B29, B30).
8. A reveal driven by noise is not linear: 1 %, 44 %, 93 % at 0.25, 0.5, 0.75 (B32).
9. HDR 2D alone keeps the numbers but the screen still clips them, and the rim picks up a tint because green and blue clip before red (B36).
10. A WorldEnvironment changes nothing in 2D unless its background mode is Canvas (B37).
11. The halo grows with how far above one the color is, and is nearly invisible on a light stage (B39).
12. HDR 2D renders 2D in linear light: a color uniform without `source_color` comes out washed out (B40); and the docs' lower-the-threshold route without HDR 2D gives a faint, colorless halo (B41).
13. The finished bubble: soft edge, highlight, scrolling noise and the glow dial in one shader, run under the three agreements (B42; `lab-shaders/15-bubble-complete.gdshader`).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I From Cut to Ramp | the teal disc (hard, then soft); the plot (axes, a dashed line or two, a terracotta dot riding the curve); the pixel grid (B04) |
| II Falloff and Highlight | the pixel grid with the spot (B11); the teal spot on the square picture; the disc |
| III Layering | the body disc and the pale highlight sheet (B17); the bubble; the two numbers 0.70 and 0.95 |
| IV Noise That Moves | the noise texture (cloud) inside the disc; the strip with a sliding window (B27); the seam |
| V Glow, Honestly | the bubble on the slate stage; the bar through the one-line gate (B33, B38); the halo; the finished bubble with every layer (B42) |

## Opening correction and terms

- **BIDEA**: the writer types "A soft edge needs a blur." and replaces "a blur" with "a ramp".
- **BDEFS** (prerequisites only): Ramp, Mask, UV, Uniform, Alpha. The terms this film exists to teach (step, smoothstep, distance, band, max, falloff, power, clamp, hint, noise, texture, sampler2D, lookup, TIME, repeat, seamless, glow, HDR, linear light, threshold) are earned in their acts, each with its definition on screen where first spoken (GLOSSARY wording where it exists; the new wording is listed in the final report for the GLOSSARY).

## Cut line

If the film runs long, cut in this order: the reveal-pace beat (B32), the beat on what else HDR 2D changes (B40), the swapped-lines beat (B10), the beat on glow without HDR 2D (B41). Each is a true caveat that another beat or the docs already carry. The S-curve pair (B05, B06), the parentheses pair (B21, B22), the seam pair (B29, B30), the two glow runs (B36, B37) and the finale (B42) stay: they are the proof and the payoff. Current estimate: 10.2 minutes by the lint's ceiling formula, so no cut is needed.

## Editor-frame reconciliation 2026-10-13

**What changed.** The picture and capture description of the two editor beats, B19 and B24, and the two OPEN fact-check rows, were reconciled with the real Godot 4.7.2 editor frames recorded by script on 2026-10-13 (`../_godot-shaders-series/editor-capture/README.md`, sections 2.3, 2.7 and 11.5). **Why.** The first plan could not show the Inspector, so two rows were OPEN and two lanes described pictures from convention. No narration changed: no spoken label was wrong. Nothing was voiced, rendered or published.

- **B19 (row 35, now PASS).** The bubble material was recorded in the real editor (the one film-specific driver run; scene, state script and log in `evidence/planning-checks/editor-capture/`): Body Color and Highlight Color are color swatches, Brightness a number box with a slider bar, and a click on a swatch opens the picker. The lane now shows the Inspector crop with a ring on the first swatch, then the picker open. "A color picker in the editor" is true: the Inspector row is a swatch that opens one.
- **B24 and B30 (row 57, now PASS).** The row is labelled exactly "Seamless", a checkbox. The B24 lane's old picture (one Inspector view with the preview, the Noise slot and Seamless together) cannot exist: the NoiseTexture2D view has Width, Height, Noise and Seamless but no preview, and the grey clouds appear one click deeper, in the FastNoiseLite view. The lane now shows those two views in that order, reusing two frames recorded for the Textures and Color film; their ring boxes and timings follow the narration.
- Only 1920x1080 frames exist for B19; the build re-records them at native size (CAPTURE-PLAN section E). `lint_series.py`: no errors, no warnings (the one OPEN-row warning is gone).

Beat ids, beat count (42 body), lane types and acts are unchanged; words unchanged (1,791 by the lint, 10.2 minutes).
