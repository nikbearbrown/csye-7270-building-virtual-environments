# Brief: Trigonometry for Shaders

**What this is.** The content brief for the film that uses trigonometry as "angle in, position out": a point on a circle, an orbit, an orbit around an orbit, and the angle of a pixel. Slug `trigonometry-for-shaders`, folder `claude-liam-lecture-trigonometry-for-shaders`, group Fragment techniques, target about 10 minutes (ceiling 15). Title lines: `["Trigonometry", "for Shaders"]`.
**Why.** Sine and cosine appear everywhere in shaders but are rarely explained as what they are: the coordinates of a point on a circle. The source course builds the whole idea from a right triangle before using it; the series does it with a moving dot.
**Found.** About 27 minutes of source (the trigonometry chapter and the orbit). The short intro video also uses `atan` for a clock-hand reveal. In Godot's 2D the vertical axis points down, so a positive angle turns clockwise on screen: verify.

## The one idea

`(cos a, sin a)` is the point at angle `a` on a circle of radius 1. Multiply by a radius, add a center, and you can place a thing anywhere on a circle around anything. Sine's wave is just that point's height as the angle grows.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("Trigonometry is for triangles\non paper.", "triangles on paper", "turning angles into positions")`.

## Prerequisites for the terms card

**Angle**, **Radian** (an angle measured so a full turn is about 6.28), **Hypotenuse**, **Orbit**. 17 characters or fewer.

## Suggested acts

1. **A Triangle with a Right Angle.** The three sides; an angle fixes the ratio of the sides whatever the size (30 degrees: the hypotenuse is twice the opposite side); sine, cosine and tangent are those ratios; SOH-CAH-TOA as a memory aid.
2. **Angle In, Position Out.** `x = cos(a) * r`, `y = sin(a) * r`; the dot goes round a circle as `a` grows; the same dot's height over time *is* the sine wave (plot both); radians: 45 degrees is `PI / 4.0`, a full turn is `TAU` (check that Godot shaders have `PI`, `TAU`, `E`).
3. **An Orbit.** Center the address (`UV * 2.0 - 1.0`); a planet mask with `step(length(p), radius)`; the moon's center `vec2(cos(a), sin(a)) * moon_distance`, its mask with `distance(p, moon_center)`; `a = TIME`; mix colors by masks.
4. **An Orbit Around an Orbit.** A meteor at `moon_center + vec2(cos(b), sin(b)) * meteor_distance` with its own faster angle; reverse by negating the angle.
5. **Angle from a Position (payoff).** `atan(p.y, p.x)` gives a pixel's angle; compared with a growing sweep it makes a clock-hand reveal. Optional: the dot, the orbit and the clock hand on one screen.

## What the source does (my words)

- Defines the right triangle, SOH-CAH-TOA, and that the ratio depends only on the angle (30 degrees gives twice); works `y = sin(30°) · 20 = 10` and `x = cos(30°) · 20 ≈ 17.32` by calculator; rewrites as `x = cos(angle) · length`, `y = sin(angle) · length`; explains the wave by drawing sin(0) = 0, sin(30°) = 0.5, sin(90°) = 1 and continuing; notes tangent looks different.
- Orbit: `vec2 uv = 2.0 * UV - 1.0`; `earth_mask = step(length(uv), earth_radius)`; `moon_x = cos(PI/4) * moon_distance`; `moon_mask = step(distance(uv, moon_center), moon_radius)`; learns that sin and cos need radians; animates the angle with `TIME`; a meteor around the moon at `TIME * 2.0`.
- Intro video: clock-hand sweep from `atan` normalized to 0 to 1 compared with a growing sweep value; `smoothstep` softens it.

## Source claims to check or correct

- Direction: the source says "going down means increasing y"; confirm that increasing angle moves clockwise on screen in `canvas_item`.
- Normalizing `atan(y, x)` to 0 to 1: the range is −PI to PI; show the exact mapping you use (`atan(y, x) / TAU + 0.5`) and probe it.
- Degrees to radians: say it once and show `radians()` if Godot has it (check).

## Facts to verify

Docs: built-in constants and functions (`PI`, `TAU`, `sin`, `cos`, `tan`, `atan` two-argument form, `radians`). Lab: a dot at several angles (probes at the computed positions), the planet/moon/meteor scene at two times, the sweep at several sweep values.

## Captures

Lab videos: orbit (`TIME`), the sweep (uniform `sweep` swept 0 to 1).

## Cut line

The meteor beat; the sweep act.

## Other films cover

Waves over time: time and waves; the line at an angle (`tan` as slope): lines and shine; matrices for rotation: matrices film.
