# Brief: Vertex Shaders

**What this is.** The content brief for the film that goes deep on `vertex()`: moving corners, getting more corners, passing values forward with `varying`, and a waving flag. Slug `vertex-shaders`, folder `claude-liam-lecture-vertex-shaders`, group Vertex and space, target about 10 to 11 minutes (ceiling 15). Title lines: `["Vertex Shaders"]`.
**Why.** The pilot proves with a measured lean that `vertex()` moves only corners and the GPU fills in between. This film turns that into a toolkit: how to get enough vertices to bend a shape, how to hand a value to `fragment()`, and how to animate a flag.
**Found.** About 40 minutes of source across vertex basics, variables (varying), the vertex chapter and the flag. The source warns that `VERTEX` means different things in the vertex and fragment stages; the docs agree. Its `MeshInstance2D` size trick (invert the y size) needs checking.

## The one idea

`vertex()` can only move the vertices that exist. A plain rectangle has four, so its edges stay straight. Give it more vertices (a Polygon2D with many points, or a subdivided mesh) and the same line of code can bend it. Whatever `vertex()` computes can be passed to `fragment()` as a `varying`, which the GPU blends smoothly across the shape.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("A vertex shader\nchanges pixels.", "changes pixels", "moves corners")` (the first draft of this brief broke the trigger across the newline, so the correction would never fire; keep the trigger on one line).

## Prerequisites for the terms card

**Vertex**, **Polygon** (a shape made of straight edges between points), **Pixel**, **Interpolate** (blend smoothly between two known values). 17 characters or fewer. Recap in one beat that `vertex()` runs once per corner.

## Suggested acts

1. **Corners.** `VERTEX` is the corner's position in *pixels*, relative to the node's center (a 128-pixel sprite has corners at ±64). Add a vector (slide), multiply (squash), use `UV.y` to lean the top differently from the bottom. `UV` is 0 to 1; `VERTEX` is pixels: two coordinate systems, one shape.
2. **More Corners.** A `Sprite2D` is a four-corner rectangle. A `Polygon2D` with many points, or a `MeshInstance2D` with a `QuadMesh` subdivided (for example 100 by 100), gives the vertex stage something to work with. Count the vertices in a scratch scene to prove it. Check the mesh size sign (the source says the y size must be negative in 2D).
3. **Passing Data Forward.** `varying vec2 v;` assigned in `vertex()`, read in `fragment()`; the GPU interpolates between corners (show the four-corner gradient). The flow is one way. In `fragment()`, `VERTEX` is *not* the same thing: it is the pixel's position in screen space (docs).
4. **A Flag (payoff).** `VERTEX.y += sin(UV.x * frequency - TIME * speed) * amplitude * UV.x` (multiplying by `UV.x` pins the left edge); add a cosine on `x` and an incline; uniforms for each knob. On a `Polygon2D`, clip the repeated border pixels in `fragment()` with `step` on `UV`.
5. **Color from the Vertex.** `COLOR` in `vertex()` multiplies the node's modulate; assigning it replaces the tint. A short beat, optional.

## What the source does (my words)

- Vertex output `VERTEX`; moves with add/multiply nodes; slant with `UV.y`; shows that `vertex.y` in the fragment stage refers to something else; Sprite2D = four vertices, `MeshInstance2D` + `QuadMesh` (size 128 by −128, subdivide 100 by 100) and `Polygon2D` (hand-placed points) as ways to get more; passes `VERTEX` through a `varying` and shows the interpolated gradient; explains `VERTEX` in the fragment stage as screen position with `SCREEN_PIXEL_SIZE`; the flag: sine of `(UV.x - TIME*speed)*frequency` times `amplitude` times `UV.x`, cosine for x, an incline term, uniforms; clips repeated border pixels with four `step`s on `UV`.

## Source claims to check or correct

- "Vertex positions are pixels, UV is 0 to 1": fine; confirm with a Lab probe.
- QuadMesh size and orientation in `MeshInstance2D` (negative y): verify in a scratch scene.
- That colors from `vertex()`'s `COLOR` replace modulate and self-modulate: verify.
- The pilot's claim ("four corners can only make straight edges") should be consistent here.

## Facts to verify

Docs: canvas_item `VERTEX` (vertex vs fragment tables), `varying`, interpolation qualifiers (`flat`, `smooth`). Scratch scenes: Sprite2D vs Polygon2D vs subdivided QuadMesh (count vertices by a debug counter such as drawing a dot at each `VERTEX` via a `varying` or by measuring the flag's shape); the Polygon2D border artifact and its fix.

## Captures

Lab sprite lean/ripple on the four-corner sprite (no ripple) against a subdivided mesh (ripple); the flag on a Polygon2D or mesh (custom scenes; describe the node setup exactly); the four-corner varying gradient.

## Cut line

The color-from-vertex beat; the incline term.

## Other films cover

Waves in the fragment stage: time and waves; matrices applied to `VERTEX`: matrices film; world position from `MODEL_MATRIX`: spaces film.
