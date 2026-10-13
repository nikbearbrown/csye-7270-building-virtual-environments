# Brief: Lines and Shine

**What this is.** The content brief for the film that draws a line at any angle from a single rule, gives it a thickness from its distance, and slides it across a sprite as a shine. Slug `lines-and-shine`, folder `claude-liam-lecture-lines-and-shine`, group Fragment techniques, target about 8 to 10 minutes (ceiling 15). Title lines: `["Lines and Shine"]`.
**Why.** The shine sweep is one of the most-wanted sprite effects, and its math (a line as a test, `tan` for slope, a distance formula) is the part people copy without understanding.
**Found.** About 14 minutes of source. A short film is fine. If it grows past 12 minutes, the cut line applies.

## The one idea

A line is a rule: for each pixel, `y - m * x` is 0 on the line, positive on one side, negative on the other. The slope `m` is the tangent of the angle. Divide the test by `sqrt(1 + m*m)` and it becomes the true distance from the line, so thickness is constant at every angle. Move the line by shifting the center.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("A line needs two points.", "two points", "one rule")`.

## Prerequisites for the terms card

**Slope** (how steeply a line rises), **Angle**, **Offset**, **Highlight**. 17 characters or fewer. (As laid out, the terms card is Pixel, UV, Uniform, Slope, Alpha: the viewer cannot be assumed to know UV or uniforms.) The film flips y once, in a named step, so a positive slope climbs to the right; see GLOSSARY "Series conventions". `tan` gets a one-sentence reminder (the trigonometry film defines it).

## Suggested acts

1. **A Line as a Test.** Center the address (`p = UV * 2.0 - 1.0`); the value `p.y - m * p.x`; probes at points above, on and below the line; show it as a signed gradient (grey in the middle).
2. **Slope from an Angle.** `m = tan(angle)`; drag the angle uniform and the line turns; the value blows up near 90 degrees (show it and what to do: use a direction vector, see below).
3. **Distance to the Line.** `abs(p.y - m * p.x) / sqrt(1.0 + m * m)`; without the divide the line gets THINNER as it steepens (corrected 2026-10-13 from the layout's runs: 9.7, 6.9, 2.7, 0.7 percent of the card at 0, 45, 75, 85 degrees, zero at 90); with it, a constant 10 percent. `step(distance, thickness)` makes the band.
4. **Shine (payoff).** Mix a highlight color into the sprite where the band is; an offset uniform slides the line; animate by tween or `TIME`; keep the highlight inside the sprite by multiplying by its alpha.
5. **The Angle-Safe Way (optional).** The same distance from a unit direction: `abs(dot(p - center, normal))`. Show it matches and does not blow up. Only if time allows.

## What the source does (my words)

- Slope-intercept `y = m x + b`; drops `b` by centering; the rewritten test `y - m*x`; plots points to show equal values along a diagonal; computes `slope = tan(angle)`; imports the distance formula from the general line equation and adapts it; `thickness` uniform; `shine_mask = step(distance_to_line, thickness)`; mixes white by the mask; adds a `center` uniform to move the line and notes it only works along one axis at 45 degrees.

## Source claims to check or correct

- The centered-address assumption: the formula as written only passes through the center; the offset needs `p - center`. Check what the source's `center` uniform does at other angles and describe it correctly.
- `tan` near 90 degrees: nothing visibly breaks with the divide in place; what breaks is the SIGN (corrected 2026-10-13 from the layout's runs: on this Mac `tan(radians(90.0))` reads about -22.9 million and warm and cool swap sides between 89.9 and 90 degrees; the divided band stays 10 percent even at 90). The film says "on this Mac".
- That `step(distance, thickness)` gives 1 inside the band: check the argument order with a probe.

## Facts to verify

Docs: `tan`, `sqrt`, `dot`, `abs`. Lab: the signed test on a rect with probes on both sides; the band at 15, 45 and 75 degrees with and without the divide (measure the band width in pixels from PNGs); the shine on the test sprite at several offsets.

## Captures

Lab: angle sweep, offset sweep, the final shine (sprite).

## Cut line

The angle-safe act; the without-divide demonstration shrinks to one beat.

## Other films cover

`tan`, `atan`: trigonometry; `mix`, `step`: math toolkit; sprite textures: textures and color.
