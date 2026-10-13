# Acts and coverage map: Drawing Shapes with Math

**What this is.** How the content brief for this film (`../_godot-shaders-series/briefs/drawing-shapes-with-math.md`) is covered: which item lands in which act, which items are left out and why, what was added that is not in the brief, the cast per act, the opening correction and terms card, and the cut line.
**Why.** A split of a long course into films of at most 15 minutes, preferably about 10 (Bear, 2026-10-13), only works if every idea has a home. This file is the record that nothing was dropped silently.
**Found.** Five acts, 44 body beats, about 10.8 minutes estimated (the lint's ceiling formula). Every item of the brief has a home. Two things in the brief were corrected or tightened by running them: the "an out-of-range mask will not be visible" claim (true on screen, false in the arithmetic: B14 to B19) and the `step` argument order (B07 to B09, where the swapped order is now spoken as a question: has the distance reached the radius, or the radius the distance). Eight things in the film are not in the brief (list below).

## Coverage of the brief

| Brief item | Where it goes | Note |
|---|---|---|
| The one idea: a shape is a rule; measure, turn it into 1 or 0; that number is a mask; masks add, subtract, multiply | **BIDEA**, B02, B09 (the word mask), Act II (add and subtract), B24 (all three ways) | The film's own phrase is "measure, compare, combine" (B27) |
| Newcomer's assumption: `BIDEA_TEXT` | **BIDEA** | The exact tuple the brief gives |
| Terms card: Distance, Radius, Center, Square; mask earned in act 1 | **BDEFS** holds Function, Shader, fragment(), UV, Vector, Uniform; distance, radius and center are taught in Act I; "square" is said in B33 | The viewer has watched no other film, so fragment, UV and uniform have to be on the card; distance, radius and center are words the viewer already owns |
| Act 1: `distance(UV, vec2(0.5))` as a ramp from the center | B05 (real render), B06 (the V along the middle row) | Shown as alpha (how visible), so the picture keeps its mid-tones |
| Act 1: `step` against a radius; flip the arguments to invert | B07 (step), B08 (the order, the flip), B09 (the circle) | Order stated carefully; flip equals `1 - step(radius, d)` on every pixel (FACTCHECK 18) |
| Act 1: a radius uniform as a slider | B10 | |
| Act 1: work one pixel by hand (distance 0.2, radius 0.3) | B03, B04, B08, B09 | The pixel is (0.62, 0.66): offsets 0.12 and 0.16, a 3-4-5 triangle, distance exactly 0.2 |
| Act 2: outer minus inner is a ring | B11, B12, B13 | Numbers for three pixels in B13 |
| Act 2: overlapping masks sum to 2; subtraction goes below 0; `min` and `max` keep a mask a mask; show the bug (the cutout vanishes) and the fix, with numbers | B14 to B17 (the sum, the vanished hole, the numbers, the `min` fix), B18 and B19 (the mirror image below zero, with a bite cut from a disc; the `max` fix and the rule) | The brief's bug is B15; the below-zero demonstration (B18) is new, and uses only what the viewer has met (circles, step, subtraction), so abs, max and the cross stay in the next act |
| Act 3: a band is `step(abs(UV.x - 0.5), half_width)`; `abs` mirrors; the cross is the union of two bands (`max`) | B20 to B23 | B24 adds the three ways to combine masks |
| Act 3 (implied by the crosshair): arms | B25 to B27 | Multiplied masks; a gap; four arms |
| Act 4: uniforms normalized to 0 to 1 and scaled inside the shader | B28, B29 | Labelled as a habit (design advice), not a rule of the engine |
| Act 4: a function that returns a mask, `uv` passed in because built-ins are not visible inside your own functions | B30, B31, B32 | Checked myself in the Lab: `UV` and `COLOR` fail inside a function, `TIME` works (FACTCHECK 50 to 53) |
| Act 5: center dot, ring, four arms; sliders for center size, ring distance, ring width, arm length, arm width, arm gap; a video sweeping each slider in turn | B35 to B44 | Six dials, three sweep beats, one predict-and-reveal beat, one real-editor beat |
| Source claim: "pixels are always squares" explains the oval | **CORRECTED** in B33 | Not repeated; the real reason is said instead |
| Source claim: an out-of-range mask "will not be visible" | **CHECKED** in B14 to B19 | True on screen, false downstream: it hides on its own and eats the next mask |
| Source claim: `step(edge, x)` argument order, flipped by hand | **SAID CAREFULLY** in B07 to B09 | |
| Captures: Lab rect, square 480 by 480; a slider-sweep video | CAPTURE-PLAN.md (C01 to C24, E1) | |
| Cut line: the min/max act shrinks to one beat; trim two crosshair sliders | `CUT_LINE` below | |
| Other films cover: soft edges, lines at an angle, aspect ratio | **LEFT OUT** | B34 and B33 state the limits only, without naming another film |

## Left out on purpose

- **Soft edges (`smoothstep`).** Another film's job. B34 says only that the edge is hard and that a softer edge needs a different tool.
- **Lines at an angle.** Another film; a cross does not need them.
- **Fixing the oval (aspect ratio).** Another film. B33 says the limit and the correct reason, and offers no fix.
- **Moving the crosshair off the center, giving it a color, drawing it in pixels.** Not needed to teach shapes as questions; every shape is centered at 0.5, 0.5 and teal.
- **Setting the dials from game code.** The film shows the dials moved by a script and, in B44, the Inspector. How a game sets a uniform is a different idea.
- **`length(p)` as another way to write `distance(UV, c)`.** True (the docs say `distance(a, b)` is `length(a - b)`, and calculator cell 5 checks it); not said, to keep the vocabulary small.
- **Anti-aliasing.** The shapes are hard; B34 says so.
- **The source's invented pixel examples.** Replaced by one real pixel, worked once, then reused in B08, B09 and B05's render.

## Added: not in the brief (each is checked, FACTCHECK.md)

1. The 3-4-5 pixel: distance exactly 0.2, reused as the worked example in four beats (B03 to B09).
2. The overlap bug as a real render, a table and a fix with real numbers (B14 to B17).
3. The mirror-image bug below zero: a bite cut from a disc so that it reaches past the disc's edge, a spot added there, and the spot never appears (B18); the `max` fix, introduced as `min`'s mirror, and the rule "after adding, cap at one; after subtracting, floor at zero" (B19).
4. The three ways to combine masks as a picture (B24).
5. The two honest limits as full beats: a square assumption with the measured oval (B33) and the hard edge with its measured two colors (B34).
6. The real compile error for `UV` inside your own function, with the engine's own words (B32).
7. The predict-then-reveal beat at the dials' ends (B43).
8. The backdrop proof that a zero mask is see-through (B39).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I Inside or Outside | the 13-by-13 pixel grid (teal cell = yes); the UV square with the terracotta center cross and the teal pixel at (0.62, 0.66); the V of distances with the terracotta radius line; the teal circle (radius 0.3) in the Lab |
| II Rings and Cutouts | the big teal disc and the small teal disc; the two overlapping circles a (center 0.38, 0.5) and b (0.62, 0.5), radius 0.25, with the small hole (0.08) at the middle; the teal disc with a round bite and the spot in the bite (shaders 08 and 09) |
| III Lines and Crosses | the UV square with its grey middle line; the band; the cross; the thin vertical arm rectangle, the pair of arms with a gap, the four arms (the same three conditions, `far_enough`, `not_too_far`, `near_line`, in the same order the crosshair uses); the pair of circles a and b again in B24 |
| IV Make It a Tool | the vertical-pair line of code, set as three stacked calls, and its three dials (gap, end, width); the three 0 to 1 sliders; the two boxes `fragment()` and `make_ring()` with the wall; the square and the stretched rectangle; the stepped zoomed grid |
| V The Crosshair | the crosshair (dot, ring, four arms) in the Lab; the six uniform lines; the two backdrops; the editor Inspector |

## Opening correction and terms

- **BIDEA**: the writer types "To draw a circle you need a circle image." and replaces "a circle image" with "a question for each pixel".
- **BDEFS** (prerequisites only; the card's wording is the GLOSSARY's, word for word): Function, Shader, fragment(), UV, Vector, Uniform. The terms this film exists to teach (distance, step, mask, abs, min, max, built-in) are earned in their acts, each defined on screen where it is first spoken (wording from `../_godot-shaders-series/GLOSSARY.md`; see the Picture line of each beat in `SCRIPT.md`).

## Cut line

If the film runs long, cut in this order: the ring-in-numbers table (B13), the hard-edge beat (B34), the second numbers table (B16), then one of the three dial-sweep beats (B42: arm width and arm gap move into B41). The min and max act shrinks to the sum bug and its fix (B14, B15, B17) plus one beat for the negative case (B18 and B19 merge). The circle by hand (B04, B08), the cross by max (B23) and the crosshair build (B35 to B38) stay: they are the idea and the payoff. Current estimate: about 10.8 minutes by the lint's ceiling formula, so no cut is needed.
