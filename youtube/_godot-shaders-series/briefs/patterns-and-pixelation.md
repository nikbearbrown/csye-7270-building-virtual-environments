# Brief: Patterns and Pixelation

**What this is.** The content brief for the film on turning smooth coordinates into cells with `floor` and `fract`, and using cells to pixelate, tile, checker, stripe and dot. Slug `patterns-and-pixelation`, folder `claude-liam-lecture-patterns-and-pixelation`, group Fragment techniques, target about 10 minutes (ceiling 15). Title lines: `["Patterns and", "Pixelation"]`.
**Why.** Pixelation, checkerboards, stripes and dot grids are common effects that all come from one trick. The source course scatters them across four chapters and, in its pixelate chapter, applies a half-fix that is worth testing.
**Found.** About 30 minutes of source. The pixelate formula has a real drift problem (the picture shifts toward the bottom right); the film should show the drift, then the fix, then measure that the corners agree.

## The one idea

Multiply the address by n and cut it in two: `floor` says which cell you are in, `fract` says where inside the cell. Cells are enough to pixelate (look up the cell's center), tile, make checkerboards, stripes and dots.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("Patterns need a pattern image.", "a pattern image", "math on the address")`.

## Prerequisites for the terms card

**Cell** (one square of a grid), **Grid**, **Remainder** (what is left after dividing), **Pixelate** (show an image as big blocks). 17 characters or fewer. (`floor` and `fract` are defined in the math toolkit film; give each a half-sentence here.)

## Suggested acts

1. **Cells.** `floor(UV * n)` is the cell number; `fract(UV * n)` is the position inside the cell (0 to 1 again). Picture: a grid with cell numbers, a moving dot with both values.
2. **Pixelate.** `floor(UV * n) / n` snaps the address to the cell's top left corner, so each block shows what sits at its own top left corner and the whole picture reads as shifted toward the bottom right (corrected 2026-10-13 from the layout's runs: the jump is half a block). Better: sample the cell's center, `(floor(UV * n) + 0.5) / n`. Compare with the source's `floor(UV * n + 0.5) / n` (corrected by the layout's runs: it is a nearest-grid-line lookup, not centering; it removes the drift but gives 17 blocks, the two end blocks half size). Make n come from the texture's size: `1.0 / TEXTURE_PIXEL_SIZE`. A slider for block size (a uniform). Measure the fixed version: 16 equal blocks, no drift. (In the rounded variant the two corner blocks match each other, 4 px each, but are half the size of the rest.)
3. **Checkerboard and Stripes.** Checker: `mod(floor(p.x) + floor(p.y), 2.0)`. Stripes: `fract(diagonal * count)` against a width. A moving version with `TIME`.
4. **Dots.** In `fract(UV * n) - 0.5` space, `length(...)` is the distance to the cell's center; `step(radius, ...)` makes a dot per cell.
5. **Optional: cycle the hue.** The source builds an HSV-to-RGB function from `fract`, `abs` and `clamp` to color moving stripes. Include only if there is room; otherwise cut.

## What the source does (my words)

- Pixel grid: `floor(UV * grid) / grid` with grid (4, 3), then 24 by 4 on the sprite; admits the picture is pushed down and right and promises a fix; checkerboard via `mod(floor(UV*4.0).x + floor(UV*4.0).y, 2.0)` with a worked example of odd and even; mod explained as the remainder with 3 mod 2 = 1.
- Pixelate chapter: a `pixel_size` uniform (float then int, range up to 32), adds 0.5 inside the `floor` to "round" and says "not perfect"; computes the texture's size as `1.0 / TEXTURE_PIXEL_SIZE`.
- Stripes in the viewport chapter: `fract(diagonal * line_count)` compared with a width, then a moving offset with `TIME * speed`; an HSV-to-RGB function.
- Light chapter: grid and dots with `mod(LIGHT_VERTEX.x, size)` against a gap and a cell-center distance. (Same math in `UV`.)

## Source claims to check or correct

- The `+ 0.5` inside `floor` is rounding, not centering: test and show what each variant does to the corners.
- GLSL `mod` versus GDScript `%` on negatives (belongs to the math toolkit; verify only what you use).
- The checkerboard works because adding two cell numbers and taking the remainder after 2 alternates; verify at four cells.

## Facts to verify

Docs: `floor`, `fract`, `mod`, `TEXTURE_PIXEL_SIZE`. Lab: pixelate variants on the checker or sprite texture with probes at the top-left and bottom-right blocks; compare block sizes from PNGs (Pillow); checkerboard probes at four cells; dots (probe a center and a corner of a cell).

## Captures

All Lab (sprite and rect). A block-size sweep video for the pixelate slider.

## Cut line

Drop the optional hue act; merge stripes into the checkerboard beat.

## Other films cover

`floor`, `fract`, `mod` definitions: math toolkit; UV scaling/centering: UV space; trig: trig film.
