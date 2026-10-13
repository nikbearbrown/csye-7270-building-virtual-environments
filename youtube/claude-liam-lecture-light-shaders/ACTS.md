# Acts and coverage map: Light Shaders

**What this is.** How this film is built from its brief and its source: which part of each lands in which act, which parts are left out, each with a reason. Also the cast per act, the opening correction, the terms card, the things the film adds that the source does not have, and the cut line.
**Why.** The lecture skill requires a coverage map so that nothing is dropped silently, and the brief says the source is loose in places. This is the record that every idea has a home and that every source claim was checked.
**Found.** Five acts, 40 body beats, about 10.3 minutes. Everything in the brief's four suggested acts is covered; the "invert" variation and the dots are left out with reasons. The source's claim that a light function cannot read U V is wrong for Godot 4.7 and is corrected (FACTCHECK row 23). Fourteen things in the film are in neither the brief nor the source (list below), several found by measuring rather than reading. One finding changes how the series must record captures: screen-space shader numbers are physical pixels (FACTCHECK row 75).

## The source (third-party; nothing copied)

A long third-party course on 2D shaders in Godot; two of its chapters (about 28 minutes) are about the light function. Its creator is not named in the text Bear gave us (open question for Bear, see SOURCES.md). The film follows the course's order of ideas for `light()` and teaches each idea in new words with new, measured demonstrations on new scenes. No sentence, example scene or image is reused, and nothing from it is stored here.

## Coverage

| Brief or source part | Where it goes | Note |
|---|---|---|
| `PointLight2D` with a radial `GradientTexture2D`, scale, color, energy | **Act I**, B02 to B05 | B04 shows the Godot docs' own recipe as the evidence |
| A dark `CanvasModulate` makes lights matter | **Act I**, B03 | measured: without it a light can only brighten a scene that is already lit |
| Lights add; the ambient stays | **Act I**, B06, B07 | the measured arithmetic 0.5 x (0.2 + 0.4 + 0.4) = 0.5 |
| Adds a shader and writes `light()`: the light disappears | **Act II**, B09 | with an empty `light()`; the lamp still lights the other sprite |
| `LIGHT = vec4(…)`, `LIGHT_COLOR`, `LIGHT_ENERGY`, `COLOR` | **Act II**, B10, B11, B13 | B10 is a flat answer, B13 the three-line rebuild |
| Two lights run the function twice | **Act II** B10 (flat answers add) and **Act IV** B29 (two beams) | measured |
| Rebuild the default and test it | **Act II**, B13 and B18 | exact match on a plain sprite, shadows included; not with a normal map; the docs' fix shown |
| Change it: invert | **LEFT OUT** | a "negative" light is Godot's Subtract blend mode, a lamp property, not a `light()` idea; bands (B15) show reshaping better |
| Change it: pulse the energy with `abs(sin(TIME))` | **Act II**, B16 | on the cut line |
| `LIGHT_DIRECTION` painted as red and green | **Act III**, B19, B20 | the arrow is drawn in Manim (B19) and used as brightness on the lamp (B20) instead of a red-green wheel: on the dusk floor a painted color clips against the ambient and hides the ramp |
| `step(progress, LIGHT_DIRECTION.x)` | **Act III**, B21 | an edge of zero; a moving edge is replaced by aiming a wedge in Act IV |
| Both sides with `abs` | **Act III**, B22 | |
| A lighthouse by a rotation matrix driven by `TIME` | **Act IV**, B24 to B26 | built from cosine, sine and a dot product: the same rotation without a matrix (matrices belong to a later film in the shader series) |
| `LIGHT_POSITION`, `LIGHT_VERTEX` in screen space | **Act V**, B31 | measured: window pixels, top left origin, y down; the lamp's position exact, the pixel's at its centre |
| `LIGHT_POSITION` of a `DirectionalLight2D` is always zero | **Act III**, B23 | docs and measured |
| `center_position = LIGHT_VERTEX.xy - LIGHT_POSITION.xy`, `length` | **Act V**, B32, B33 | |
| Ring reveal with two `step`s on `length`; a progress uniform expands it | **Act V**, B34 to B36 | B36 is a tween driven by the game |
| A grid with `mod(LIGHT_VERTEX.x, size)` | **Act V**, B38, B39 | on the cut line |
| Dots with a cell-center distance | **LEFT OUT** | the same `mod` cell idea in another shape; belongs to the series' pattern film (grid and dots in `UV`), and the grid beat is already on the cut line |
| "Light shaders cannot read `UV`" (source) | **CORRECTED** in B11 | the docs sentence and the corner colors, FACTCHECK row 23 |
| "Runs for every fragment and every light" | **Act I** B08, **Act II** B10, B12 | docs and measured |
| `unshaded` skips `light()` | **Act II**, B17 | also ignores the ambient tint (measured) |
| `DirectionalLight2D` | **Act I** B02, **Act III** B23 | |
| Never in the brief and left out on purpose | **LEFT OUT** | shadows and `LightOccluder2D` (B18 only says the copy keeps them), light blend modes (Add, Subtract, Mix), light masks and layers, SDF functions, specular, `light_only`, `SHADOW_MODULATE`, lamp height. Normal maps are named in B18 with the docs' fix, not taught: they need art assets and a film of their own |

## Corrections (full detail in FACTCHECK.md)

- `UV` is available in `light()` (row 23); the source said it is not.
- The docs word `LIGHT_DIRECTION` loosely ("Direction of the Light2D in screen space"). Measured: an arrow from the pixel toward the lamp, three numbers of length one (row 42). For a directional light it points toward the sun, the same everywhere (row 50).
- The one-line rebuild of the default is exact (row 28) but only without a normal map (row 39); the docs' version with `NORMAL` is the fix and is only for sprites that have a normal map (row 41).
- Screen-space numbers are physical pixels (row 75). The series' capture convention (a 4K SubViewport over a 1280 x 720 canvas) would draw every ring and stripe here three times too small, so this film's captures are 1920 x 1080 at scale 1 (CAPTURE-PLAN.md).
- With the film's dusk ambient an empty `light()` leaves the ambient look (row 17); with a black ambient it is black.

## Added: in neither the brief nor the source

1. The Godot docs' own recipe for a soft lamp as the evidence for "the soft edge is the texture's alpha" (B04, B14).
2. The measured pixel arithmetic: surface times the total of ambient and lights (B06, B07).
3. A flat `light()` to prove "once per lamp, and the answers add" (B10).
4. The order of work: fragment first, its color arrives in light, one run per lamp, the sum (B12).
5. Alpha is the soft edge; forced to one the glow becomes the texture's hard square (B14).
6. Bands: reshaping the fade (B15).
7. `unshaded` for the lamp's own bulb (B17).
8. What the copy misses (normal maps) and the docs' fix, with measured pixel counts (B18).
9. The dot product explained as agreement between two arrows (B25).
10. The cutoff as a uniform, and a soft beam edge with `smoothstep` (B27, B28).
11. The reach caution: light is never called outside the lamp's texture (B30).
12. Screen-space numbers do not follow the camera (B37).
13. Stripes belong to the screen, not the sprite (B38).
14. "Where each job belongs", the closing table (B40).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I Lights in 2D | the dusk tiled floor (blue-grey, mid-tone on purpose); the warm lamp with a pale bulb disc marking it; the teal blob |
| II The Light Function | the same floor and lamp; the blob as the control that stays on default lighting; the grey card for the flat answers; two pale bulb discs for `unshaded` |
| III Which Way Is the Light? | the lamp at the centre of a ring of pixel dots with arrows (Manim); the floor and lamp (captures) |
| IV A Lighthouse | the lamp and its turning wedge; the unit circle and the two arrows (Manim); the blob |
| V Where Is the Light? | the window frame with its origin dot and a DOWN-pointing y axis; the lamp and the pixel dot; the ring; the floor tiles |

## Opening correction and terms

- **BIDEA**: the writer types "Lighting is built in. You can't touch it." and replaces "You can't touch it" with "A shader can replace it". (The brief's suggested text broke the trigger across a line, which the verbatim rule forbids; this text keeps the trigger on one line and the corrected sentence reads as true.)
- **BDEFS** (prerequisites only): Shader, Pixel, Texture, Canvas, Vector, Mask. The brief suggested Light, Energy, Canvas, Mask; a viewer who is making a game knows what a light is, and energy is earned in B05, while `vec2`, `vec3` and `vec4` fill the code cards, so Vector replaces Light and Energy. Texture is added because B04 says a soft glow is a texture and B14 and B30 lean on the lamp's texture; Shader and Pixel are the two words every shader film needs. Terms the film teaches (light function, ambient light, built-in, alpha, uniform, step, smoothstep, mod, tween, screen space, normal map, unshaded, dot product) are defined on screen where first spoken, in captions or labels; the wording comes from `../_godot-shaders-series/GLOSSARY.md` where it has the term (light(), built-in, uniform, TIME, alpha, floor, abs, step, dot, length, mod, tween, mask, vector, pixel, texture, shader); the GLOSSARY has no row yet for ambient light, smoothstep, max, screen space, normal map or unshaded, so those use this film's own plain wording (FACTCHECK).

## Cut line

If the film runs long, cut in this order: the grid beat (B39), the stripes beat (B38), the pulse beat (B16), then the limits beat (B18). Each repeats an idea another beat carries (rings already show distance patterns; bands already show reshaping) or sits outside the film's one idea. The rebuild (B13), the lighthouse (B26) and the expanding ring (B36) stay: they are the proof and the two payoffs. Current estimate: about 10.3 minutes (the lint's), so no cut is needed; removing all four would give about 9.4 minutes.
