# Acts and coverage map: Trigonometry for Shaders

**What this is.** How this film is built from its sources and its brief: which part lands in which act, which parts move to another film in the series, and which are left out, each with a reason. Also the cast per act, the opening correction, the terms card, the additions that are in neither source, and the cut line.
**Why.** Bear split a seven-hour course and a short intro into films of at most 15 minutes, preferably about 10 (2026-10-13). A split only works if every idea has a home. This file is the record that nothing was dropped silently.
**Found.** Five acts, 40 body beats, about 9.9 minutes. Every idea of the brief's five suggested acts has a beat; two brief items are changed on purpose (planet and moon are drawn with plain `if` tests instead of `step` masks and `mix`, and the optional all-in-one screen is left out). Nine things in the film are in neither source (list below). No source claim needed correcting; one draft wording of mine was (FACTCHECK row 60).

## The sources (both third-party; nothing copied)

- **A.** The trigonometry chapter and the orbit chapter of a long third-party course on 2D shaders in Godot (about 27 minutes of it), as described in `../_godot-shaders-series/briefs/trigonometry-for-shaders.md`. The creator is not named there.
- **B.** The clock-hand reveal near the end of a short third-party introduction to Godot shaders (about one minute), as described in the same brief.
- The layout agent saw the sources only through the brief's description, not their transcripts. Every demonstration in the film was rebuilt, run and measured here (`evidence/planning-checks/`).

## Coverage

| Source and part (the brief's wording) | Where it goes | Note |
|---|---|---|
| A: the right triangle, its three sides, SOH-CAH-TOA | **Act I**, B02 to B04 | Taught in new words with a moving triangle and a live ratio readout |
| A: the ratio depends only on the angle (30 degrees: the hypotenuse is twice the opposite side) | **Act I**, B03 | Shown by scaling the triangle; 30 and 50 degrees |
| A: sine, cosine and tangent as those ratios; the by-hand calculator example; `x = cos(angle) * length`, `y = sin(angle) * length` | **Act I** B05 and **Act II** B06, B07, B09, B10 | The brief's two lines become one idea: with a radius of one the legs ARE the numbers; the by-hand example uses new numbers (radius 0.6, 30 degrees) and is checked against a real render later (B19) |
| A: the wave from drawing sin(0), sin(30 degrees), sin(90 degrees) and continuing | **Act II**, B14, B15 | Rebuilt as the trace of the dot's height; cosine shown as the same wave a quarter turn earlier |
| A: "tangent looks different" | **LEFT OUT** | Tangent is used only as a ratio (B04) and, in reverse, as arc tangent (B32). Its own curve is not needed here, and tangent as a slope belongs to *Lines and Shine* |
| A: degrees against radians, learned by trying; `PI`, `TAU` | **Act II**, B11 to B13 | Becomes a taught catch with a measured trap (the shader still compiles, sine of thirty comes out near minus one) |
| A: `vec2 uv = 2.0 * UV - 1.0` | **Act III**, B16 | Called `p` |
| A: the planet mask `step(length(uv), earth_radius)`; the moon mask with `distance`; mixing colors by masks | **Act III**, B17, B18 (changed) | The film writes `if (length(p) < 0.25)` and `if (distance(p, moon) < 0.08)`: the same tests with no `step` argument-order puzzle and no `mix`, so no extra function is needed. `step`, `mix` and masks belong to *The Shader Math Toolkit* and *Drawing Shapes with Math* |
| A: the moon's center from the angle; `a = TIME`; speed | **Act III**, B18 to B22 | The brief's check that "going down means increasing y" becomes two beats, B19 and B20: the moon lands BELOW the middle, and why |
| A: a meteor around the moon with its own faster angle | **Act IV**, B26 to B28 | Planet, moon and meteor are new names and new numbers; the meteor runs at three times the clock |
| A: reversing by negating the angle | **Act IV**, B29 | Shown with the moon unchanged |
| B: the clock-hand sweep from `atan` normalised to 0 to 1, compared with a growing sweep value | **Act V**, B31 to B39 | With the exact mapping `atan(p.y, p.x) / TAU + 0.5` shown, worked for one pixel, probed, and the start moved to twelve |
| B: `smoothstep` softening the hand's edge | **MOVED** to *Soft Edges, Glow and Noise* | The hard edge stays; smoothstep is that film's subject |
| B: noise reveal | **MOVED** to *Soft Edges, Glow and Noise* | |
| Brief: "optional: the dot, the orbit and the clock hand on one screen" | **LEFT OUT** | The orbit and the sweep need two different shaders; one screen would be a bigger shader that teaches nothing new, and the recap carries the link (B31's two arrows are the same idea drawn once) |
| Brief, other films: waves over time (amplitude, frequency, speed, offset) | **MOVED** to *Time and Waves* | B14 and B15 only connect the circle to the wave |
| Brief, other films: matrices for rotation | **MOVED** to *Matrices and Fake 3D* | |
| Brief, other films: aspect ratio in depth | **MOVED** to *UV Space* | B24 states the limit and the fix for circles only |

## Corrections to the sources (full detail in FACTCHECK.md)

None needed: the brief's three "claims to check" all held (a positive angle turns clockwise on a screen, row 33; `atan(y, x) / TAU + 0.5` maps to 0 to 1, rows 49 to 52; `radians()` exists, row 18). One check came out differently from what the brief assumed: `PI`, `TAU` and `E` are documented only in each shader type's own reference (Global built-ins), not in the Shading language page (row 17). One draft wording of mine was corrected: the eight-lobed shape is a flower, not a gear (row 60).

## Added: in neither source (each is checked, FACTCHECK.md)

1. Godot's own manual defines the point at an angle as cosine, sine (`Vector2.from_angle`), shown on its real page (B08, row 11).
2. The degrees-for-radians trap measured: `sin(30.0)` is about -0.99, thirty radians is 4.77 turns (B13, rows 19 to 22).
3. The moon lands below the middle on a screen, and why, with Godot's own sentences on y and rotation (B19, B20, rows 31 to 34).
4. Adding a third of a turn to the angle gives three evenly spaced moons (B23, row 38).
5. On a wide shape circles come out oval, 160 by 90 pixels, and the fix with an aspect uniform (B24, rows 39, 40).
6. The one-argument `atan(y / x)` slip, with Godot's own warning and a render of it (B36, row 54).
7. One pixel worked by hand to its number, one eighth, and a threshold check (B37, row 55).
8. Starting the reveal at twelve with `fract` (B39, row 59).
9. The flower: the pixel's angle fed to cosine again (B40, rows 61, 62).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I One Angle, Two Numbers | the right triangle with its marked 30-degree corner and the live ratio readout; the hook render (teal planet, slate-blue moon, amber meteor) |
| II Angle In, Position Out | the unit circle (paper orientation, y up) with the terracotta dot, the same triangle inside it, and the plot beside it |
| III An Orbit | the centered square p (screen orientation, y down); the Lab renders with the teal planet and slate-blue moon on the warm grey; the code card |
| IV An Orbit Around an Orbit | planet, moon and amber meteor in the same colours as the renders; the two tip-to-tail arrows |
| V Angle from a Position | the circle with the pixel dot (screen orientation); the teal-to-amber angle picture; the teal sprite revealed by the wedge |

## Opening correction and terms

- **BIDEA**: the writer types "Trigonometry is for triangles on paper." and replaces "triangles on paper" with "turning angles into positions". The line break sits before the trigger so the trigger is verbatim (the brief's version broke the trigger across the line, which the checker would reject).
- **BDEFS** (prerequisites only): Angle, Radian, Hypotenuse, Vec2, UV. The brief listed Orbit instead of Vec2 and UV; an orbit is an ordinary word that the film shows rather than defines, while `vec2` and `UV` must be read in the first code. Radian is on the card as a prerequisite word and is then earned (B11) with the radius walked around the edge. The terms the film teaches (sine, cosine, tangent, arc tangent, radian's meaning, `PI`, `TAU`, length, distance, uniform, mix, fract, seam, sweep) are each defined on screen where first spoken (labels and captions listed in the lane entries; wording from `../_godot-shaders-series/GLOSSARY.md` where it has one).

## Cut line

If the film runs long, cut in this order: the flower (B40), the three moons (B23), the arm (B30), the oval limit (B24), then the start at twelve (B39). Each is a bonus that repeats an idea another beat already carries. The brief suggested cutting the meteor and the sweep first; here they stay, because the opening card promises the clock hand and the first picture promises the meteor. Current estimate: about 9.9 minutes, so no cut is needed.
