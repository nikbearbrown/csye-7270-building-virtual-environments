# Checks report (PROOF GATE): Lines and Shine

**What this is.** The lecture skill's whole-sheet checklist for this layout: how many beats are SHOW, HOLD or CARD, the lane histogram, the teaching-arc checks, where every earned term is defined on screen, and the mechanical lint result.
**Why.** The skill requires this file before the first compile, so a punt (a text-only card standing in for a picture) is caught on paper, not after the render.
**Found.** 35 body beats, all SHOW; no HOLD; no text-only card (each act title rides the act's first picture). Lanes: ShaderLab capture 21, Manim 14, library Remotion 0, editor 0. Estimated 9.0 minutes, 1,587 words by the lint's count (which includes the term meanings; the beat sheet holds 1,579). `lint_series.py` is clean with no warnings. Risks the build must watch: the two components and the harness extensions that may not exist yet, the seven two-panel scenes, and the 2 px hairline at 89 degrees.

## Counts

| Class | Beats | Notes |
|---|---|---|
| SHOW | 35 | every body beat has a motion that carries its claim |
| HOLD | 0 | none: no photograph or creator decision is needed |
| CARD | 0 | act titles are labels on each act's first picture; bookends are the mandated cards |
| PUNT | 0 | |

Lane histogram (information, not a quota): capture 21 (all `ShaderLab`) · manim 14 · remotion-library 0 · editor 0. The library's `LectureCodeTrace` and `LectureEvidenceTable` were auditioned as runner-up in 16 rows and lost each time on motion: this film's content is a shader's moving result next to its code, which is what `ShaderLab` is for. Fourteen beats are Manim because their claim is a coordinate system, a triangle, a plot or an equation changing form.

## Teaching arc

- [x] Opens on the newcomer's assumption and corrects it with one phrase (BIDEA: two points, one rule).
- [x] FRAMEWORK before the first example: the test `y - m x` (B05) comes before the three worked points (B06).
- [x] WORKED EXAMPLE: three points with exact numbers (B06), then every pixel at once (B08); then the band, its widths, the offset, the sprite.
- [x] FALSIFIABILITY and edge cases, each a full beat: the radians trap (B12), the seam at ninety (B13, B14), the raw band that thins (B17), the leak (B25), the wide shape (B30).
- [x] Concrete before abstract; predict-then-reveal in four places: the radians trap (B12), the tilting band (B17), the sideways shift of a flat line (B23), the leak (B25).
- [x] Every earned term is defined on screen where first spoken (table below); BDEFS holds prerequisites only.
- [x] A measured claim says machine and renderer: B14 says "on this Mac" and the capture is labelled "Apple M4 Pro · Godot 4.7.2 · Forward+"; widths are a percent of the card, so they do not depend on capture size.
- [x] A thing that surprises is shown by a real run: the band thinning (B17, B21), the swap at ninety (B14, B35), the flat line that ignores a sideways shift (B23), the leak (B25, B26), the tween that fails without a start value (FACTCHECK 52).
- [x] Honest limits: scripted calls are labelled (B28); the card is a square and B30 says what a wide shape does; the shine is hard-edged on purpose; no performance claim.
- [x] SCAFFOLDED viewer task: BHTF is a prompt to paste plus two checks the viewer makes on the result (the band climbs to the right at forty-five degrees; it is as thick at eighty as at ten). The reference solution that passes both is `lab-shaders/10-shine.gdshader` (FACTCHECK 63).
- [x] Payoff uses every earlier idea together: B24 to B29 (address, slope, true distance, step, offset, mix, alpha, clock or tween).
- [x] Standalone: no reference to any other film, book, course or school and no numbering (lint).
- [x] No number on any viewer-facing surface that is not either read from a run here or derived in `evidence/planning-checks/arithmetic.txt`; no digits in the narration (lint).

## Where each earned term is defined on screen

| Term | Beat | Where on screen |
|---|---|---|
| slope | BDEFS card, B02 | the card line; the rise-over-run triangle labelled "slope m: up per step across" |
| U V (address) | BDEFS card, B03 | the card line; the square whose labels morph from 0 to 1 into minus one to one |
| uniform | BDEFS card, B09 | the card line; the highlighted `uniform float slope` line |
| alpha | BDEFS card, B26 | the card line; spoken again where it matters |
| shader_type, canvas_item, fragment() | B08 | labels on the first code beat: "shader_type canvas_item: the first line says this shader is for 2D drawing" on line 1 and "fragment(): runs once for each pixel the shape covers; sets its color" on the function line (spoken: "Fragment runs once for every pixel") |
| vector, COLOR | B08 | caption "vector: a bundle of two to four numbers (vec2, vec4) · COLOR: the color of the pixel being drawn" |
| tangent | B10 | label "tangent of the angle = the slope" with the live height |
| radians | B11 | caption "radians: a full turn is about 6.28" |
| abs, step, band | B15, B16 | labels "abs: drop the sign", "step(a, b): 0 until b reaches a, then 1"; the band is the picture; B16's caption adds "vec3(x): the grey x" |
| sqrt | B19 | label "sqrt: the square root" on the triangle |
| thickness | B20 | caption "thickness is in address units"; the "10% wide" readout |
| offset | B22 | caption "offset: how far the line has been slid" |
| mix | B24 | caption "mix(a, b, t): t = 0 gives a, t = 1 gives b · vec4(1.0) is white" |
| TIME, fract | B27 | caption "TIME: seconds on one clock shared by the whole game"; readout "fract: 0–1" with the repeating ramp |
| tween | B28 | caption "tween: glides a value from one number to another over time" |
| aspect | B30 | the highlighted line `p.x *= aspect;` under the two panels |
| cosine, sine, normal, dot | B31, B32 | labels "cosine: across", "sine: up", "the normal", "dot: across x across + up x up" |

## Risks for the build (not defects of the layout)

1. **Shared pieces.** `ShaderLab`, `shader_kit.py` and the capture harness may not exist yet (`../_godot-shaders-series/COMPONENT-SPECS.md`); this film also needs `caption`, `ramp.period`, a `stack` layout with a short code excerpt, per-panel animation and the two-panel scene (all listed in `BUILD-PROMPT.md`).
2. **Seven two-panel scenes** (C05, C10, C12, C14, C18, C19, C20) come from `evidence/planning-checks/two_panels.gd`, verified as stills only; the animated versions are the build's to make and to compare against the stills.
3. **GATE T and Gate V on the cards.** The grey card is 127, which is 72 from the type gate's MUTE colour (its ink mask tolerance is 48); the smooth warm and cool map is far from ink and mute everywhere; the stage is `#D9D5CA`. The saturated orange and blue fields at ninety degrees (B14, B35) are not near ink. Readout labels need a light backing, not ink on mid-grey.
4. **The hairline.** At 89 degrees the old band is 2 px wide on a 1728 px card (0.12 percent); at 85 degrees 16 px (0.93 percent). It must stay crisp at the recorded size.
5. **Pace.** Ten beats are 39 or 40 words and none is longer (the lint floor is 48); if a voice check runs long, split B27 or B28, not the shorter ones.
6. **Pronunciation to listen for.** "U V", "radians", "tween", "sine", "cosine", "tangent", the single letters in "y equals m x plus b" and "p dot n".

## Lint (mechanical)

`python3 ../_godot-shaders-series/lint_series.py lines-and-shine` prints no errors and no warnings: 41 beats, about 9.0 minutes.
