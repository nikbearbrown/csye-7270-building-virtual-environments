# Acts and coverage map: Patterns and Pixelation

**What this is.** How this film is built from its brief: which item lands in which act, which items are left out and why, the cast per act, the opening correction, the terms card, the additions that are not in the source, and the cut line.
**Why.** The film replaces about thirty minutes of a longer third-party course with one film of about ten minutes. A split only works if every idea has a home; this file is the record that nothing was dropped silently.
**Found.** Five acts, 43 body beats, about ten minutes (1,790 words by the series checker). The one idea (floor says which cell, fract says where inside it) carries every effect. The source's pixelate half-fix was tested and is not a centering fix at all: it removes the drift and halves the edge blocks (measured). One source claim is corrected and three more are sharpened, and nine things in the film are in neither source, each measured.

## The source (third-party; nothing copied)

**A.** A long third-party course on 2D shaders in Godot, covering this material across four chapters (pixel grid and checkerboard in the UV chapter, a "pixelate" chapter, stripes in the viewport chapter, grid and dots in the light chapter), about thirty minutes in all. The creator is not named in the material Bear supplied. What the course says is summarised in `../_godot-shaders-series/briefs/patterns-and-pixelation.md` in the brief's words; none of the course's sentences, code or examples are reused here.
**B.** The Godot 4.7 documentation (read 2026-10-13) and the installed Godot 4.7.2, which are the primary sources for every fact in the film.

## Coverage

| Item in the brief | Where it goes | Note |
|---|---|---|
| The one idea: scale the address, then `floor` says which cell and `fract` says where inside | **Act I**, B02 to B09 | Taught as a stretched ramp (B02 to B04), then both numbers in two dimensions (B05), then drawn as colors in a real shader (B06, B07) |
| The cells picture: a grid with cell numbers, a moving dot with both values | **Act I**, B05 | Manim grid, dot at (2.3, 1.7): cell (2, 1), inside (0.3, 0.7) |
| `fract` as a repeating address (tile) | **Act I**, B08 | Two lines; the brief lists "tile" in the one idea but gives it no beat, so it gets one |
| `floor(UV * n) / n` snaps to the cell's top left; the picture drifts toward the bottom right | **Act II**, B10 to B14 | Shown (a jump against a fixed ring), measured (3.5 px right and down at 8-pixel blocks) and explained (a one-dimensional staircase) |
| Better: `(floor(UV * n) + 0.5) / n`, the cell's center | **Act II**, B15, B16 | Measured: the sprite does not move (less than one pixel); worked example with real arithmetic |
| The source's `floor(UV * n + 0.5) / n` "rounding": test what it does | **Act II**, B17 to B19 | CORRECTED: it is a lookup at the nearest grid line, not centering; it removes the drift but halves the first and last blocks (measured 4 px against 8 px) |
| Measure that the corner blocks match in size for the fixed version | **Act II**, B18, B19 | All sixteen blocks are 8 px in the middle-lookup version; the rounding version has 17 blocks (4, eight fifteen times, 4) |
| `n` from the texture's size with `1.0 / TEXTURE_PIXEL_SIZE`; a block-size uniform (float, then int, to 32) | **Act III**, B20 to B25 | Docs shown (B21); an int uniform with `hint_range(1, 32)`; blocks counted in picture pixels; the short last block when the size does not divide the picture |
| A slider for block size (a uniform) | **Act III**, B23 | A scripted sweep in the Lab; the Inspector is not shown (no editor frames; the docs say a uniform appears as an editable parameter, which is as far as the film goes) |
| Checkerboard `mod(floor(p.x) + floor(p.y), 2.0)`; why adding two cell numbers alternates; verify at four cells | **Act IV**, B26 to B29 | Sums grid, remainder, why diagonal neighbours match; Lab: 64 of 64 cells match the formula; `mod` explained as the remainder with 3 mod 2 = 1 |
| Stripes `fract(diagonal * count)` against a width | **Act IV**, B30 to B32 | Diagonal ramp, sawtooth, `step`; Lab: the gold share equals the width |
| A moving version with `TIME` | **Act IV**, B33 | Subtract `TIME * speed` inside the `fract`; `fract` of a negative number stays in 0 to 1 |
| Dots: `length(fract(UV * n) - 0.5)` and `step(radius, ...)` | **Act V**, B35 to B38 | Cell space centered, length, step, radius sweep (they touch at 0.5 and fill the cell at 0.71) |
| (not in the brief) the dots turn oval on a wide shape | **Act V**, B39, B40 | Measured: 49 to 50 by 28 pixels on a 640 by 360 shape; the fix is a count for each direction |
| (not in the brief) pixelate and dots together | **Act V**, B41 to B43 | A dot screen: floor picks the cell and the lookup, fract draws the dot; the rounding trap again, in dots |
| Optional: HSV-to-RGB from `fract`, `abs`, `clamp`, to color moving stripes | **LEFT OUT** | Color conversion belongs with color, not with cells; the stripes need two colors only |
| The light chapter's `mod(LIGHT_VERTEX.x, size)` grid and dots | **LEFT OUT** | The same math is taught here in `UV`; the light-shader inputs belong with light shaders |
| Source claim: GLSL `mod` against GDScript `%` on negatives | **Act IV**, B29, B33 (only what is used) | Lab: `%` on decimals is a shader error; `mod` and `fract` of negatives land in 0 to 1. The GDScript side is not claimed |
| Definitions of `floor`, `fract`, `mod` | **Acts I and IV** | Each is defined on screen in the beat that first speaks it (the film is standalone); the full tour of math functions is left to others |
| Stripe angle and scale beyond the diagonal; sprite sheets and regions (docs: `UV` spans the whole texture when a region is enabled) | **LEFT OUT** | Not in the brief; the region caveat is recorded in FACTCHECK row 67 for whoever teaches sprite sheets |

## Corrections and sharpenings (full detail in FACTCHECK.md)

- The `+ 0.5` inside the `floor` is not centering: it looks up the nearest grid line, so the drift goes away but the edge blocks halve (row 29).
- The drift has a size: half a block, less the half pixel of the measurement (rows 22, 24, 25).
- Percent is not mod: in a shader `%` is an error on decimals (row 44); `mod` is the remainder and stays in range for negatives (rows 41, 50).
- `TEXTURE_PIXEL_SIZE` only means something on a node with a texture; on a Color Rect it reads 1 (row 34).

## Added: in neither source (each is measured, FACTCHECK.md)

1. The size of the drift, at three block sizes (B13, B14).
2. The first and last blocks of each variant, and what picture pixel each shows (evidence only).
3. The worked example with real arithmetic (B16).
4. The short last block (B25) and blocks that scale with the sprite (B24).
5. Percent on decimals fails; `fract` of negatives is fine (B29, B33).
6. The coverage of a dot against its radius, and the two thresholds (B38).
7. The wide-shape oval measured, and the fix (B39, B40).
8. The dot screen and its edge check (B41, B42), validated against a reference answer and two wrong answers (`evidence/planning-checks/verify-bhtf.gd`).
9. The smooth filter against the nearest filter (FACTCHECK row 64; the captures say "nearest filter").

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I Which Cell, and Where in It | the ramp strip (0 to 1, stretched to 0 to 4), the terracotta dot, the four by four cell grid; the teal test sprite in the real renders |
| II Pixelate Without the Drift | the test sprite with a terracotta ring on its original silhouette; a cell of pixel dots over a picture strip; the row of blocks |
| III Blocks of Any Size | the picture's pixel grid with a block outlined; the 128 pixel strip of blocks; the sprite |
| IV Checkerboards and Stripes | the grid of sums (the same grid in B26 to B28), the checkerboard, the diagonal ramp square, the sawtooth plot |
| V Dots, and Both Numbers at Once | the unit cell with its origin in the middle, the circle, the dot grid; the sprite as a dot screen |

## Opening correction and terms

- **BIDEA**: the writer types "Patterns need a pattern image." and replaces "a pattern image" with "math on the address".
- **BDEFS** (prerequisites only): Shader, UV, Texture, Uniform, Cell, Remainder. The terms this film teaches (floor, fract, mod, mix, step, length, TIME, pixelate, ramp, sawtooth) are defined on screen where first spoken, in the cue labels of the code cards or in the Manim beats (wording from `../_godot-shaders-series/GLOSSARY.md` where the glossary has the term; the glossary has none of `floor`, `fract`, `mod`, `mix`, `step`, `length`, so those definitions use the Godot 4.7 docs' own words).

## Cut line

If the film runs long, cut in this order: the scale beat (B24), the worked example (B16), the diagonal-step beat (B28), then merge the moving stripes (B33) into the stripes beat (B32). Each repeats an idea another beat carries. The drift pair (B13, B14), the rounding pair (B17, B18), the wide-shape trap (B39, B40) and the dot screen with its edge check (B41, B42) stay: they are the proof and the payoff. Current estimate: about 10.2 minutes, so no cut is needed.
