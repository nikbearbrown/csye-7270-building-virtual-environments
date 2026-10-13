# Brief: Drawing Shapes with Math

**What this is.** The content brief for the film that teaches a shape as a question each pixel answers ("am I inside?"), building up to a crosshair with sliders. Slug `drawing-shapes-with-math`, folder `claude-liam-lecture-drawing-shapes-with-math`, group Fragment techniques, target about 10 minutes (ceiling 15). Title lines: `["Drawing Shapes", "with Math"]`.
**Why.** This is the first "think per pixel" workout, and every HUD, ring or cutout effect starts here. It also introduces the idea of a mask that later films combine.
**Found.** The source spends about 30 minutes on the crosshair (the longest chapter of the course). Its habit worth keeping: plug in numbers for one pixel and do the arithmetic by hand. Its aspect-ratio explanation is wrong (see the UV film); this film's shapes assume a square, and says so.

## The one idea

A shape is a rule. For each pixel, measure something (the distance to a center, the distance to a line) and turn it into 1 ("inside") or 0 ("outside"). That 0-or-1 number is a **mask**; masks add, subtract and multiply.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("To draw a circle you need\na circle image.", "a circle image", "a question for each pixel")`.

## Prerequisites for the terms card

**Mask** (a 0-to-1 number per pixel saying how much to show) can be earned in act 1 instead. Candidates: **Distance**, **Radius**, **Center**, **Square** (a shape whose width equals its height). 17 characters or fewer. Use `step` and `distance` with a half-sentence each; the math toolkit film defines them properly.

## Suggested acts

1. **Inside or Outside.** `distance(UV, vec2(0.5))` is a ramp that grows from the center; `step` against a radius makes it 0 or 1; flip the arguments to invert. A radius uniform as a slider. Work one pixel by hand (a pixel at distance 0.2, radius 0.3).
2. **Rings and Cutouts.** Outer circle minus inner circle is a ring. When masks overlap their sum can reach 2, and subtraction can go below 0; `min(..., 1.0)` and `max(..., 0.0)` keep a mask a mask. Show the bug (the cutout vanishes) and the fix, with the numbers.
3. **Lines and Crosses.** A band along one axis is `step(abs(UV.x - 0.5), half_width)`; `abs` mirrors it so one formula draws both sides; the cross is the union of two bands (`max`).
4. **Make It a Tool.** Uniforms normalized to 0 to 1 (a good habit: predictable sliders), scaled inside the shader by constants; a function that returns a mask (`float make_ring(vec2 uv)`), with `uv` passed in because built-ins are not visible inside your own functions (the language film verifies exactly which; cite its result only after you check it yourself in the Lab).
5. **The Crosshair (payoff).** Center dot + ring + four arms, sliders for center size, ring distance, ring width, arm length, arm width, arm gap. Show it as a video sweeping each slider in turn.

## What the source does (my words)

- Builds the center circle from `step(distance(UV, vec2(0.5)), center_size * 0.1)`; the outer ring as `outer_circle - inner_circle` with `circle_distance` and `circle_width`; adds `min`/`max` after finding that the cross cutout subtracts to -1; draws arms as mirrored rectangles (`1.0 - UV.x` for the other side) with width and height steps multiplied; combines with plus. Talks through pixel examples with invented numbers.

## Source claims to check or correct

- "Pixels are always squares" explanation for the oval: wrong, see the UV film; this film just draws on a square.
- That an out-of-range mask "will not be visible": check the exact arithmetic with numbers.
- `step(edge, x)` argument order: say it carefully; the source flips it by hand to invert.

## Facts to verify

Docs: `distance`, `step`, `abs`, `min`, `max` in the built-in function list; Lab: circle at several radii (probes at known distances), ring, the overlap bug (a mask summing to 2) and `min` fix, cross, then the assembled crosshair at defaults and at extremes.

## Captures

All Lab (rect, square 480×480 via `--size 480x480`); a slider-sweep video for the crosshair.

## Cut line

The `min`/`max` act shrinks to one beat; trim two crosshair sliders.

## Other films cover

Soft edges (`smoothstep`): soft-edges film; lines at an angle: lines film; aspect ratio: UV film.
