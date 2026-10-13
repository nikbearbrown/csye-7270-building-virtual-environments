# Brief: The Shader Math Toolkit

**What this is.** The content brief for the film that teaches the dozen or so built-in functions almost every effect uses, each as a reshaping of a 0-to-1 ramp. Slug `shader-math-toolkit`, folder `claude-liam-lecture-shader-math-toolkit`, group Foundations, target about 10 minutes (ceiling 15). Title lines: `["The Shader Math", "Toolkit"]`.
**Why.** Every later film uses these functions (`step`, `mix`, `smoothstep`, `fract`, `distance`...). The source course introduces them one at a time across seven hours; the series teaches them once, with plots, so later films can use them with a half-sentence reminder.
**Found.** The source gets one function wrong in a way that matters (it describes `smoothstep` as if it were a straight line). A "ramp in, function, ramp out" picture covers all of them. Also useful: the pad shader in the 3D film uses `step`, `fract` and `mix`, so this film is a prerequisite for reading it.

## The one idea

A ramp (a smooth run from 0 to 1, such as `UV.x`) goes in; a function reshapes it; a ramp-like thing comes out. About twelve functions cover most effects. Learn what each does to a ramp and you can predict a shader.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("Shaders need advanced math.", "advanced math", "a dozen small functions")`.

## Prerequisites for the terms card

**Ramp** is the film's word but is earned in act 1. Candidates: **Function**, **Input**, **Output**, **Float** (a number with a decimal point). Keep to 17 characters.

## Suggested acts

1. **Ramps and Plots.** What a ramp is (show `UV.x` as a grey strip, 0 at the left, 1 at the right). How to read the series' standard plot: input along the bottom, output up the side, a dot travelling, the strip below showing the result. One tiny shader per function renders `COLOR = vec4(vec3(f(UV.x)), 1.0)` in the Lab.
2. **Cut and Blend.** `step(edge, x)` (0 below the edge, 1 at or above), `smoothstep(a, b, x)` (a smooth S between a and b; not a straight line), `mix(a, b, t)` (blend), `clamp(x, lo, hi)`, `min`, `max`.
3. **Repeat and Fold.** `abs` (mirror about zero), `fract` (the part after the decimal point: a ramp that restarts), `floor`, `mod(x, y)` (remainder; the GLSL form).
4. **Distance and Curves.** `length`, `distance`, `normalize`, `pow` (reshapes a 0-to-1 ramp: higher power squeezes toward the edge), and a half-beat preview of `sin`/`cos` as repeating curves (taught in the time and trigonometry films).
5. **Build a Ring (payoff).** A ring from `distance` and `step` (outer minus inner), then a soft ring with `smoothstep`. Three functions, one picture.

## What the source course does (my words)

- `step` first, as the switch from a gradient to two values (with `UV` and with `distance` to build a circle); "swap the arguments to invert it".
- `mix` to blend two colors by a 0-or-1 or 0-to-1 weight; one-minus to invert; `clamp` or `min` to keep time from running past one; `min`/`max` to keep summed masks within 0 to 1 (overlap sums to 2) or above 0 (subtraction goes negative).
- `smoothstep` for a gradient with a defined start and end; `pow` to concentrate a highlight (2 to 3); `normalize` for a direction of length one.
- `abs` on a centered coordinate to mirror a shape; `floor` and `mod` for grids and checkerboards; `fract` for a repeating pattern.

## Source claims to check or correct

- **`smoothstep` is not linear.** The source explains it as "if limit one is 0, limit two is 10 and the value is 1, it returns 0.1". That is linear interpolation. The real `smoothstep` returns 3t² − 2t³ with t = (x − a)/(b − a), so 0.028 for that input. Show the true S-curve and the number (verify in the Lab).
- `mod` semantics for negative inputs (GLSL's `mod(x, y) = x − y·floor(x/y)`): verify; do not assume GDScript's `%` behavior.
- The source's description of `pow(x, y)` as "concentrates a gradient" is fine for a 0-to-1 ramp; say so (a base outside 0 to 1 behaves differently).
- `step(edge, x)` returns 1 when `x >= edge`; check the equality case.

## Facts to verify

Docs: the shading language reference's built-in function list and descriptions (step, smoothstep, mix, clamp, min, max, abs, fract, floor, mod, pow, length, distance, normalize). Lab: one tiny shader per function with probes at x = 0, 0.25, 0.5, 0.75, 1.0 (record the output values); the `smoothstep(0.0, 10.0, 1.0)` number; `mod(-0.25, 1.0)`.

## Captures

All Lab: a grey ramp strip before and after each function, and the final ring (sprite or rect). No editor frames.

## Cut line

Drop `clamp`/`min`/`max` to a one-line mention; drop the `pow` and `normalize` beats to one.

## Other films cover

`sin`/`cos`/`atan`: time and trigonometry films; `texture()`: the textures film; `floor`/`fract` for grids: the patterns film (this film defines them, that one uses them); vector types and swizzles: the language film.
