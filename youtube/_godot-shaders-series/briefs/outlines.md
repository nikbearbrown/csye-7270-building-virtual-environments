# Brief: Outlines

**What this is.** The content brief for the film on the sprite outline: each pixel asks its neighbors whether they are opaque. Slug `outlines`, folder `claude-liam-lecture-outlines`, group Fragment techniques, target about 10 minutes (ceiling 15). Title lines: `["Outlines"]`.
**Why.** An outline is the most-requested sprite shader and the best example of a fragment shader reading *other* pixels of a texture. It also shows the cost model (one texture read per neighbor, per pixel) and the padding trap.
**Found.** About 24 minutes of source. The source introduces `if` and `for` here and says ifs should be avoided; check that claim. Its padding fix is a GDScript function that rebuilds the image with a transparent border.

## The one idea

A pixel can read the texture at other addresses. To outline a sprite, a *transparent* pixel looks at its neighbors; if any neighbor is opaque, this pixel is on the outline and gets the line color. The cost is one texture read per neighbor, for every pixel.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("An outline is a bigger copy\nbehind the sprite.", "a bigger copy behind the sprite", "a question about neighbors")` (keep the trigger verbatim in the text and free of end punctuation).

## Prerequisites for the terms card

**Neighbor** (the pixel next to this one), **Opaque** (fully visible), **Alpha**, **Padding** (empty space added around an image). 17 characters or fewer.

## Suggested acts

1. **Ask the Neighbors.** Read the alpha at one offset (a small step left); add the four directions; keep it in range (`min(sum, 1.0)`); subtract the pixel's own alpha so only the outside edge is left; color it with a `vec4` line color via `mix`.
2. **Pixel-Sized Steps.** `TEXTURE_PIXEL_SIZE` is the size of one texel in address units; multiply by a thickness uniform so a step is exactly N pixels at any texture size; add the four diagonals.
3. **Say It with a Loop.** Two nested `for` loops over −1 to 1 replace eight copied lines; count the work (nine reads per pixel here); an `if (thickness > 0.0)` guard; the honest performance note (only `discard`'s cost is in the docs; do not claim ifs are slow without a source).
4. **Room to Draw.** If opaque pixels touch the texture's edge, the outline has nowhere to go: show it on a full-bleed image; fix by padding the image with transparent pixels (the GDScript function: decompress, convert to RGBA8, create a larger `Image`, `fill` transparent, `blit_rect`, make an `ImageTexture`; run it and show the result). Animated sprites work because the shader sees whatever texture is current.
5. **Where It Breaks.** Larger thickness leaves gaps on diagonals with eight samples (show it, measure, and say how a ring of more samples fixes it); `filter_nearest` for pixel art.

## What the source does (my words)

- Starts with a bird sprite with padding and `texture_filter` nearest; uniforms `line_color`, `line_thickness` (0 to 1), `const max_line_thickness = 4.0`; samples the alpha at `UV + vec2(0.005, 0.0)` and so on; notes sampling to the right shows the picture to the left; switches to `TEXTURE_PIXEL_SIZE`; eight directions, then the `if`, then nested `for` loops; mixes `color.rgb` and `line_color.rgb` by `outline - color.a`; adds a GDScript `add_padding_to_texture`; wires a slider to `set_shader_parameter`.

## Source claims to check or correct

- "Ifs inside a shader are not recommended / slow every fragment": find a primary source or drop it.
- "UV moves right, picture moves left": true in effect; show with a probe.
- The `mix(color.rgb, line_color.rgb, outline - color.a)` form: check it handles semi-transparent edges; show what antialiased edges do.

## Facts to verify

Docs: `TEXTURE_PIXEL_SIZE`, loops in the shading language. Lab: the outline on the test sprite at several thicknesses (measure the line width in pixels from PNGs); nine reads per pixel (count in code, say it is by construction); the padding failure and fix (run the GDScript on a scratch texture); the diagonal gap at a large thickness.

## Captures

Lab (sprite kind with the padded blob): a thickness sweep video; a failure still; the fixed still.

## Cut line

The diagonal-gap act; the loop-cost beat.

## Other films cover

`texture()` basics: textures and color; `for` and `if` syntax: the language film (recap only here); sprite animation is not covered.

**Corrections from the layout (2026-10-13):** (a) `mix(color, line, outline - color.a)` goes negative on an opaque pixel with no opaque neighbor (231 of 4,637 sprite pixels turn (126, 255, 99) with one read); multiply by (1 - own alpha) instead. (b) Eight reads leave no diagonal gaps on a disc (diagonal/axis 1.42); four reads pinch (0.63); gaps appear only in thin parts. (c) "Animated sprites work because the shader sees the current texture" holds only for separate frame images; on a sprite sheet `UV` spans the whole sheet and a stray line leaks from the neighbor frame (clamp reads into `REGION_RECT`). (d) `filter_nearest` is a hint for a `sampler2D` uniform; the node's own `TEXTURE` takes the node's Texture Filter or the project default (linear). (e) `Image.create` is deprecated: use `Image.create_empty`. (f) The first draft broke the `BIDEA_TEXT` trigger across the newline.
