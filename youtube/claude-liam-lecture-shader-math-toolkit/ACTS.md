# Acts and coverage map: The Shader Math Toolkit

**What this is.** How this film is built from its brief and from the third-party course it follows: which function and which idea lands in which act, which parts are left out and why, the cast per act, the opening correction and terms card, what the film adds that no source has, and the cut line.
**Why.** The brief and the course teach about a dozen built-in functions one at a time across hours. A film of at most fifteen minutes (about ten preferred) needs every function and every correction to have a home, and every omission a reason. This file is the record that nothing was dropped silently.
**Found.** Five acts, 41 body beats, about 10.3 minutes (1,808 words). Every function the brief names lands in an act (min and max inside clamp; sine only as a half-beat; cos is left out on purpose). The source's `smoothstep` error is corrected with a measured number, its "swap the arguments" shortcut gets its one exception, the `mod` trap against GDScript is added, and the ring payoff uses `distance`, `step`, `smoothstep` and `mix` together. Seven things in the film are in no source (list below).

## The sources (third-party; nothing copied)

- **A. The brief** (`../_godot-shaders-series/briefs/shader-math-toolkit.md`): suggested acts, the one idea, source claims to check.
- **B. A long third-party course on 2D shaders in Godot** (creator not yet named by Bear; its math functions are taught one at a time between its fragment, color, vertex and shape chapters). Only the order of ideas is followed; the brief's summary of it is the reference here. See `SOURCES.md`.
- **C. Primary:** the Godot 4.7 documentation (built-in shader functions, shading language, canvas item reference, GDScript `fmod`, `fposmod`, `lerp`) and the installed Godot 4.7.2.

## Coverage

| Item (brief or source) | Where it goes | Note |
|---|---|---|
| The one idea: a ramp goes in, a function reshapes it, a ramp-like thing comes out | **Act I**, B02 to B05 | Taught with the series' standard plot (input along the bottom, output up the side, a dot, the strip below) |
| BIDEA: "Shaders need advanced math" corrected to "a dozen small functions" | **Opening** | `BIDEA_TEXT` below |
| Terms card: Function, Input, Output, Float | **BDEFS**: Shader, Pixel, UV, Function, Vector | Input and Output are folded into Function ("numbers go in, one number comes out"); Float is left out (the code reads as a number; `float` is never explained and nothing depends on it); Shader, Pixel, UV and Vector are needed from the first shader on screen |
| Act 1 "Ramps and Plots": a ramp as a gray strip; how to read the plot; one tiny shader per function | **Act I** (B01 to B06) | B03 is the first real shader; each later function gets its tiny shader in `lab-shaders/` or in `evidence/planning-checks/check-shaders/` (probed at x = 0, 0.25, 0.5, 0.75, 1.0 in `quarter-tables.md`) |
| `step(edge, x)`; the equality case | **Act II**, B07 to B08 | At or above the edge gives one (measured at x = 0.5) |
| `smoothstep(a, b, x)`, not linear | **Act II**, B10 to B13 | The correction (B11, FACTCHECK 22) and the docs formula and warning (B12) |
| `mix(a, b, t)` | **Act II**, B14 to B16 | Plus: mix does not pin its weight (B14); any reshaped ramp can be the weight; the word "mask" (B16) |
| `clamp(x, lo, hi)`, `min`, `max` | **Act II**, B09 | One beat: min and max appear as the two halves of clamp (docs formula); no separate beats |
| `abs` | **Act III**, B17 to B18 | Needs a ramp centered on zero first (B17) |
| `fract` | **Act III**, B19 to B20, B22, B23 | "A ramp that restarts"; with `step` it makes stripes (B23) |
| `floor` | **Act III**, B21 to B22 | Defined here; the whole-and-leftover split with `fract` (B22) |
| `mod(x, y)`; negative inputs | **Act III**, B24 to B25 | The brief's "verify, do not assume GDScript's behavior": measured, with the three-row table (B25) |
| `length`, `distance`, `normalize` | **Act IV**, B26 to B31 | `length` (B26), `normalize` (B27), `distance` (B28 to B29), the oval warning (B30), distance as a weight: the soft spot (B31) |
| `pow(x, y)`; the base outside 0 to 1 | **Act IV**, B32 to B33 | Says plainly that a ramp from 0 to 1 is the case taught; a negative base is "undefined" in the docs and the film says so |
| A half-beat preview of sine | **Act IV**, B34 | Sine only; **cos is LEFT OUT**: it is the same curve shifted and adds nothing in half a beat |
| Act 5 "Build a Ring": ring from `distance` and `step`, then soft with `smoothstep` | **Act V**, B35 to B41 | Plus `mix` for color and a radius uniform (the dial) |
| Source: `step` first, as the switch from a gradient to two values | **Act II**, B07 to B08 | Built on `UV.x`, not on the course's circle |
| Source: "swap the arguments to invert it" | **Act V**, B36 | CORRECTED with its one exception (FACTCHECK 65) |
| Source: one-minus to invert | **Act I**, B05 | The first function on the plot |
| Source: `clamp` or `min` to keep TIME from running past one | **LEFT OUT** | TIME is not taught in this film; clamp's purpose is shown with the mix weight instead (B14) |
| Source: `min` and `max` to keep summed masks within 0 to 1 | **LEFT OUT** as its own beat | The ring subtracts two masks that cannot go negative; clamp, min and max are defined in B09 and the idea needs no demo here |
| Source: `abs` on a centered coordinate to mirror a shape | **Partly**, B17 to B18 | The fold is shown on a strip; mirroring a drawn shape is left out (the ring is already symmetric) |
| Source: `floor` and `mod` for grids and checkerboards | **LEFT OUT** | Defined here (B21 to B25) and previewed with stripes (B23); grids and checkerboards need cells in two directions and belong to the film built on `floor` and `fract` |
| Source: `pow` to concentrate a highlight (power two to three) | **Act IV**, B32 to B33 | Shown as the highlight tightening |
| Source: `normalize` for a direction | **Act IV**, B27 | One beat, with the (3, 4) arrow |
| Source's explanation of why a circle goes oval ("fragments are stretched") | **CORRECTED**, B30 | The address runs 0 to 1 on both sides; measured: 384 by 192 px on a 2 to 1 shape (FACTCHECK 53, 54) |
| Vector types and swizzles | **LEFT OUT** | Only `vec3(x)` (three copies) and the `vec4` color are glossed in passing (B03); the language itself is another film's subject |
| `texture()`, `sin`/`cos`/`atan` in depth, grids with `floor`/`fract` | **LEFT OUT** | Other films' subjects; sine gets a half-beat (B34) |
| Captures: a gray ramp strip before and after each function, and the final ring | **Act I to V** | Drawn plots plus 16 Lab captures; no editor frames |

## Corrections to the sources (full detail in FACTCHECK.md)

`smoothstep` is not linear: 0.028, not 0.1 (rows 19, 20, 22). Swapping `step`'s arguments flips the picture except exactly on the edge, where both orders give one (rows 12, 65). A circle turns oval because the address runs 0 to 1 on both axes, not because fragments are "stretched" (rows 53, 54).

## Added: in no source (each is checked, FACTCHECK.md)

1. The measured `smoothstep(0, 10, 1)` = 0.028 against the straight-line 0.1, with the docs formula and the "undefined if a >= b" warning on screen (B11, B12).
2. `mix` does not pin its weight: weight two overshoots to 1.6, so clamp it first (B14).
3. `mod` of a negative number against GDScript's `fmod` and `fposmod`, measured on both sides (B25).
4. The distance picture's two numbers, 0.5 at the middle of an edge and about 0.71 at a corner, and the measured oval (B29, B30).
5. `smoothstep` as a weight for a soft spot of light, `1 - smoothstep(0, 0.5, d)` (B31).
6. The ring, built in five steps with real renders (B35 to B41), ending on the finished shader with its radius dial.
7. A proof that the curves drawn in the film are the curves Godot renders: 21 curves and 10 pictures compared pixel for pixel (`evidence/planning-checks/dense-compare.md`).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I Ramps and Plots | the ring (hook, B01); the ramp strip (a row of narrow tiles) with its terracotta dot; the standard plot frame (axes, curve, dot, drop line, strip) |
| II Cut and Blend | the standard plot frame with the edge line, the guides and the two edges; the teal-to-gold blend strip; the code card beside each real render |
| III Repeat and Fold | the ramp strip with re-labelled ticks; the number line with the dot at 2.75; the standard plot frame |
| IV Distance and Curves | the vector arrow (3, 4) on axes with the origin at the top left (y counts down, as the address does; labelled once in B26, never flipped silently); the UV square with the "middle" dot; the square picture (distance, glow); the standard plot frame |
| V Build a Ring | one square picture at one size and one centre: the disk, the flipped disk, the hard ring, the colored ring, the soft ring, the finished ring (all at radius 0.3); the distance-axis plot for the pulse |

## Opening correction and terms

- **BIDEA**: the writer types "Shaders need advanced math." and replaces "advanced math" with "a dozen small functions".
- **BDEFS** (prerequisites only): Shader, Pixel, UV, Function, Vector. The terms the film earns, each defined on screen where it is first spoken: ramp (B02), fragment, COLOR and alpha (B03), uniform (B08), step, smoothstep, mix, clamp, min, max, abs, fract, floor, mod, length, normalize, distance, pow, sine (each in its beat, with its docs wording) and mask (B16). Wording comes from `../_godot-shaders-series/GLOSSARY.md` where an entry exists (the terms table, and its table of small math words for step, mix, floor, fract, mod, length and alpha), otherwise from the Godot 4.7 docs. The small words the table lists that this film never says (slope, offset, radians, normal, dot, band, tween, TEXTURE) are kept out of the narration on purpose, so none needs a definition here.

## Cut line

If the film runs long, cut in this order: the toolkit map (B06), the sine beat (B34), the normalize beat (B27), the soft-spot beat (B31), the smooth step docs beat (B12) and the floor-only beat (B21; B22 still defines floor). Each repeats or previews an idea another beat carries. The plot-reading pair (B04, B05), the smooth step correction (B11), the whole-and-leftover split (B22), the mod trap (B25) and the whole ring build (Act V) stay: they are the method, the corrections and the payoff. Current estimate: about 10.3 minutes, so no cut is needed; the six cuts together would save about 75 seconds. A cut beat also leaves its name in the recap line (the fourth recap line carries normalize and sine), so that line and its spoken twin must be trimmed too.
