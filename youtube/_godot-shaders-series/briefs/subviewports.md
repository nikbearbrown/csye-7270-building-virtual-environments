# Brief: SubViewports

**What this is.** The content brief for the film on rendering nodes into a texture with a `SubViewport` and shading that texture, so two shaders can work in sequence. Slug `subviewports`, folder `claude-liam-lecture-subviewports`, group Screen, textures and light, target about 10 to 11 minutes (ceiling 15). Title lines: `["SubViewports"]`.
**Why.** A single shader per node limits what you can do. A `SubViewport` lets you shade the content, then shade the *result*, and display it on anything that accepts a texture.
**Found.** About 23 minutes of source (the longest single build after the crosshair), including a rainbow-stripe effect with an HSV function. The HSV function is a good candidate to define properly instead of copying.

## The one idea

A `SubViewport` is a small off-screen picture. Put nodes in it, and the result becomes a texture (`ViewportTexture`) that you can put on a sprite, a mesh or anything else that takes a texture. Each side can have its own shader: the inner one shades the content; the outer one shades the picture of it.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("Each node gets one shader.", "one shader", "two shaders in a row")`.

## Prerequisites for the terms card

**Viewport** (a rectangle the engine draws into), **Texture** (recap), **Off-screen** (drawn but not shown directly), **Transparent** (see-through). 17 characters or fewer.

## Suggested acts

1. **Render to a Texture.** Add a `SubViewport` (size 256 by 256 in the source), put a sprite inside it, add a second sprite whose texture is a `ViewportTexture` pointing at it. The viewport's origin is its top left, and it covers positive x and y from there; "centered" on the sprite shifts what you see; `transparent_bg` keeps empty areas empty.
2. **Two Shaders, One Result.** An inner shader on the content (the source: a vertex scale and rotation matrix) and an outer shader on the displaying sprite (the source: stripes). Both act on the same picture.
3. **Stripes and Hue.** Diagonal stripes from `fract((UV.x + UV.y) * count)` against a width; make them move with `TIME`; color them with a hue cycle: define an `hsv_to_rgb` function and say what hue, saturation and value are, then verify the function you show against a reference (a few known colors).
4. **Wobble the Result (payoff).** Show the viewport on a `MeshInstance2D` with a subdivided `QuadMesh` and a vertex wobble in the outer shader; combine with the inner rotation. Everything a texture can go on, the result can go on.

## What the source does (my words)

- `SubViewport` with 512 then 256 size; `ViewportTexture` on a Sprite2D; explains origin and offset; an inner shader coloring red/green; an outer shader with `COLOR.a = UV.x`; `transparent_bg`; stripes `pattern = fract(diagonal * line_count)`, `is_line = step(pattern, line_width)`, moving with `diagonal - TIME * speed`; the `hsv_to_rgb` function built from `K = vec3(1, 2/3, 1/3)`; pixelates the stripes; the inner vertex shader: `scale_matrix`, `rotation_matrix` (angle = TIME * speed); the final outer vertex wobble on a subdivided `MeshInstance2D`.

## Source claims to check or correct

- The HSV function: write the standard compact form and test red, yellow, green, cyan, blue, magenta at hues 0, 1/6, ..., 5/6 with known RGB results.
- `ViewportTexture` and mesh orientation (negative y size) as in the vertex film: verify.
- That `transparent_bg` is needed to keep the original alpha: verify with and without.

## Facts to verify

Docs: SubViewport and ViewportTexture class pages, `transparent_bg`, render target update mode. Scratch scenes for each step; HSV function probes via the Lab (it is a pure function of a number: render `hsv(UV.x)` as a strip and probe six positions).

## Captures

Custom scenes: viewport content with an inner rotation; the displayed result with stripes; the wobble mesh (video).

## Cut line

The hue act (keep stripes with a constant color); the wobble mesh.

## Other films cover

`hint_screen_texture` post-effects: reading the screen; matrices: matrices film; vertex wobbles: vertex film.
