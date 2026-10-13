# Acts and coverage map: Lines and Shine

**What this is.** How the film is built from its one source: which idea lands in which act, which are corrected, which are left out, each with a reason. Also the cast per act, the opening correction, the terms card, the additions that are not in the source, and the cut line.
**Why.** The film is short (about nine minutes) and every idea must have a home or a reason for having none. This file is the record that nothing was dropped silently, and that every change to the source's claims is deliberate.
**Found.** Five acts, 35 body beats, about 9.0 minutes. The source's whole chain is covered (a line as a test, slope from `tan`, a distance formula, `step` into a band, a mix, a way to move the line). Three of its claims are corrected by measurement (the band thins, not thickens, when the line steepens; a centre shift moves the line by an angle-dependent amount; the divide rescues the band even at ninety degrees, and what actually breaks there is the sign). Eight things in the film are in neither the source nor the brief (list below).

## The source (third-party; nothing copied)

One third-party video of about 14 minutes about drawing a line with a rule in a shader and using it as a shine on a sprite (length and content as given in the content brief, `../_godot-shaders-series/briefs/lines-and-shine.md`). Its creator is not named in the brief. **I worked from the brief's paraphrase of it; I did not see the video.** The film follows its order of ideas and teaches them in new words with new demonstrations, each run in Godot 4.7.2.

## Coverage

| Source idea (as the brief describes it) | Where it goes | Note |
|---|---|---|
| The line `y = m x + b`; `b` dropped by centering the address | **Act I**, B02 to B04 | The address is centred and also flipped, so that a positive slope climbs to the right (the brief's `p = UV * 2.0 - 1.0` alone leaves `y` pointing down) |
| The rewritten test `y - m*x` (zero on the line, positive one side, negative the other) | **Act I**, B05, B06 | Three worked points with exact numbers (0, +0.6, -0.6) |
| Plotting points to show equal values along a diagonal | **Act I**, B07 | A dot slides along a parallel line and its number stays |
| The test as a signed picture (grey in the middle) | **Act I**, B08, B09 | Warm and cool around a grey strip; real Lab render |
| `slope = tan(angle)` | **Act II**, B10 to B12 | With the radians trap (`tan(30.0)` is -6.4), measured on the GPU |
| The value blows up near ninety degrees: show it and say what to do | **Act II**, B13, B14; **Act V** | What the brief expected to see fail (a thick or broken line) does not happen with the divide; what does happen is the sign swap. CORRECTED (FACTCHECK rows 20 to 25) |
| The distance formula, imported from the general line equation and adapted | **Act III**, B18 to B20 | Derived instead from one right triangle (a step along the line is `sqrt(1 + m*m)` long), so nothing is imported on trust |
| `thickness` uniform; `step(distance, thickness)` makes the band | **Act III**, B15, B16, B20 | Argument order checked with probes |
| Without the divide the line changes thickness with angle | **Act III**, B17, B21 | CORRECTED: it gets **thinner** (width = full width x cos(angle)), not thicker (FACTCHECK rows 30 and 31) |
| Mix white into the sprite by the mask | **Act IV**, B24 to B26 | The first attempt leaks onto transparent pixels; multiplying by alpha fixes it (brief's "keep the highlight inside the sprite") |
| A `center` uniform moves the line; it only works along one axis at 45 degrees | **Act IV**, B22, B23 | CORRECTED: a centre shift moves the line by shift x sin(angle) or x cos(angle); an offset added to the true distance slides it straight across at any angle (FACTCHECK rows 39 to 42) |
| Animate by tween or by `TIME` | **Act IV**, B27, B28 | `TIME` is one global clock; a tween needs its start value set from code first (a failed run is kept) |
| The angle-safe way: `abs(dot(p - center, normal))` | **Act V**, B31 to B35 | Shown equal to the slope form pixel for pixel; B33 shows the divide was a disguised cosine; the `- center` part is left out (see below) |

## LEFT OUT, with reasons

- **Soft-edged shine (`smoothstep`).** The shine here is hard-edged on purpose: a hard `step` is what makes the band width exactly measurable and the leak visible. A soft edge is a one-word swap and belongs with the other soft-edge techniques.
- **`abs(dot(p - center, normal))` with a centre.** The act teaches the direction form through the origin; moving the line is already done by the offset in Act IV and the same `+ offset` applies to the direction form.
- **Editor setup of the material and the uniform sliders.** The viewer is assumed to have a shader attached; no editor captures are needed, so this film has no editor frames.
- **Why a circle goes oval, aspect ratio in general.** Only the one consequence for lines is shown (B30), with its fix.
- **Angle from a position (`atan`), sprite sheets, textures beyond the sprite's own color.** Not needed for a line and a shine.
- **Performance claims.** None are made; no timing was measured for this film.

## Added: in neither the source nor the brief (each is checked, FACTCHECK.md)

1. The y flip, so that angles behave as taught in school (B04).
2. The radians trap, measured on the GPU: `tan(30.0)` = -6.405 (B12).
3. The seam at ninety, measured: the sign flips between 89.9 and 90 degrees in both renderers; at exactly ninety Godot's tangent on this Mac is -22,877,334 (B13, B14).
4. The raw band vanishes at ninety (0 px at 90 degrees, a hairline at 89), the divided band does not (B17, B21).
5. The alpha leak and its fix (B24 to B26), including the pixel that proves it.
6. A wide shape bends the angle (45 shows as 29 on 16:9) and drifts the thickness; the fix, `p.x *= aspect`, is verified (B30).
7. The divide is a disguised cosine, so the direction form is the same distance without the tangent (B33).
8. A tween on a uniform never set from code fails with "does not exist" (B28; the run that must fail is kept in `run-1-verify1.log`, test T2).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I A Line as a Test | the test square with centred axes (y up) and the line m = 0.5; the three terracotta dots; the real card (square, warm and cool around grey) |
| II Slope from an Angle | the turning line with its one-step-across height; the real card holding the same warm and cool picture; the paired cards for the radians trap |
| III Distance to the Line | the tilted line with its two gaps; the grey card with the white band; the old and new bands side by side |
| IV Shine | the teal test sprite with the white band; the paired panels (offset and centre; leak and fix; wide and fixed) |
| V The Angle-Safe Way | the unit arrow and its normal; the paired cards (slope form and direction form) |

Stage colours as in the series: Lab stage `#D9D5CA`, cream `#FAF9F5`, ink `#3D3929`, terracotta only as dots and rings.

## Opening correction and terms

- **BIDEA**: the writer types "A line needs two points." and replaces "two points" with "one rule".
- **BDEFS** (prerequisites only): Pixel, UV, Uniform, Slope, Alpha. The brief suggested Slope, Angle, Offset, Highlight, assuming the viewer already knows `UV` and uniforms from an earlier film; this film is standalone, so the two terms it needs from outside (`UV`, uniform) are on the card, plus Alpha, and Angle and Highlight (plain words) are left to the picture. Offset is earned in Act IV, tangent in Act II, band and distance in Act III, normal, dot, sine and cosine in Act V, each defined on screen where first spoken (wording from `../_godot-shaders-series/GLOSSARY.md` where it has one).

## Cut line

If the film runs long, cut in this order: **Act V** (B31 to B35), and with it the last sentence of B14, which promises it; then the centre-shift beat (B23); then fold B16 and B17 into one beat (the band, then the tilt). The wide-shape limit (B30) stays unless the film is far over, because it is the honest edge of the whole method. The shine itself (B01, B22, B24 to B29) never goes. Current estimate: about 9.0 minutes, so no cut is needed.
