# Brief: Light Shaders

**What this is.** The content brief for the film on `light()` in 2D: what it replaces, what the `LIGHT_*` built-ins give you, a rotating lighthouse beam and a ring that expands from a light. Slug `light-shaders`, folder `claude-liam-lecture-light-shaders`, group Screen, textures and light, target about 10 to 11 minutes (ceiling 15). Title lines: `["Light Shaders"]`.
**Why.** `light()` is the least-used and least-understood of the three functions. The pilot only names it and states two measured facts: it runs once per light and the results add; an empty `light()` replaces the default lighting.
**Found.** About 28 minutes of source (two chapters). The source says a light shader cannot read `UV`; the 4.7 docs say it can (verified 2026-10-13: "UV from the vertex() function, equivalent to the UV in the fragment() function"). The source's "rebuild the default light" recipe should be tested against the real default.

## The one idea

When you write `light()`, you take over how every light affects that node. Godot hands you the light's color, energy, direction and position; you return the color that light adds to this pixel. Because the results of all lights add, `light()` is where you shape each light's contribution.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("Lighting is built in.\nYou can't touch it.", "You can't touch it", "light() replaces it")` (the first draft broke the trigger across the newline; the layout used this form) (check the trigger's capital and punctuation rules: the trigger must match the text exactly and not end in punctuation; rewrite the text if needed).

## Prerequisites for the terms card

**Light** (a source that brightens nearby things), **Energy** (how strong), **Canvas** (the 2D drawing surface), **Mask** (recap). (As laid out, the terms card is Shader, Pixel, Texture, Canvas, Vector, Mask.) 17 characters or fewer.

## Suggested acts

1. **Lights in 2D.** `PointLight2D` (a texture, scale, color, energy) and `DirectionalLight2D`; a dark `CanvasModulate` makes lights matter; without it the node is already fully lit. Everything in the pilot's measurement (dark canvas; constant `light()`) can be recapped in one beat.
2. **The Light Function.** Writing `light()` replaces the default. Rebuild it: `LIGHT = vec4(COLOR.rgb * LIGHT_COLOR.rgb * LIGHT_ENERGY, LIGHT_COLOR.a);` and check, with a probe, that it matches the default on a simple scene (it may not: normal maps, shadows, light mode; report exactly what it does and does not reproduce). Then change it (invert, pulse the energy with `abs(sin(TIME))`).
3. **Direction.** `LIGHT_DIRECTION` as a mask (`step(x, direction.x)`); both sides with `abs`; a **lighthouse**: rotate `LIGHT_DIRECTION.xy` with a rotation matrix driven by `TIME` so a cone sweeps round.
4. **Position.** `LIGHT_POSITION` (the light's center) and `LIGHT_VERTEX` (the pixel's position) are both in screen space; their difference is a vector from the light; `length` makes rings; a progress uniform expands a ring (outer circle minus inner circle); `mod(LIGHT_VERTEX.x, size)` makes a grid; a left-half grid and right-half dots show combining two.

## What the source does (my words)

- `PointLight2D` with a `GradientTexture2D` radial fill, scale, color; adds a shader and un-comments `light()` (the light disappears); `LIGHT = vec4(…)`; `LIGHT_COLOR`, `LIGHT_ENERGY`; `COLOR`; two lights run the function twice; `LIGHT_DIRECTION` as red/green; `step(progress, LIGHT_DIRECTION.x)`; lighthouse with a rotation matrix; then `LIGHT_POSITION`/`LIGHT_VERTEX` in screen space; `center_position = LIGHT_VERTEX.xy - LIGHT_POSITION.xy`; ring reveal with two `step`s on `length`; grid via `mod`; dots via cell-center distance.

## Source claims to check or correct

- **"Light shaders cannot read UV"**: wrong for 4.7 (docs). Correct it.
- "Runs once for every fragment and every light": verified in the pilot (0.2, 0.4, 0.6); cite.
- The rebuilt default: test it.
- `LIGHT_POSITION` for `DirectionalLight2D` is always (0, 0, 0) (docs): mention.

## Facts to verify

Docs: canvas_item shader reference light built-ins (fetched 2026-10-13: `LIGHT_COLOR`, `LIGHT_ENERGY`, `LIGHT_POSITION`, `LIGHT_VERTEX`, `LIGHT_DIRECTION`, `LIGHT`, `SHADOW_MODULATE`, `UV`); `unshaded` render mode skips `light()`. Scratch scenes (see the pilot's `verify4.gd`): one light, two lights, default vs rebuilt, direction and position values as colors, the lighthouse, the ring and grid.

## Captures

Custom scenes only: dark canvas, a sprite with the shader, one or two lights, scripted rotation/progress.

## Cut line

The grid and dots; the pulse variation.

## Other films cover

`step`, `length`, `mod`: math toolkit and patterns; rotation matrices: matrices film.
