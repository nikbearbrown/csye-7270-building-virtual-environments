# Brief: Local, World and Screen Space

**What this is.** The content brief for the film on coordinate spaces: the same point has different numbers relative to the node, to the world and to the screen, and matrices convert between them. Slug `local-world-and-screen-space`, folder `claude-liam-lecture-local-world-and-screen-space`, group Vertex and space, target about 10 to 11 minutes (ceiling 15). Title lines: `["Local, World and", "Screen Space"]`.
**Why.** Effects that must stay fixed in the world (a texture that does not move with its sprite), or follow the screen (a vignette), need the right space. The pilot's source video touches world-space UVs; this film does them properly.
**Found.** About 27 minutes of source (model matrix, then the canvas coordinates). The source lists four ways to get a pixel's screen position and says they are interchangeable; they can be tested against each other.

## The one idea

A position is only a pair of numbers relative to something. Local space is relative to the node's origin, world space to the world's origin, screen (canvas) space to the window's top left. `MODEL_MATRIX` turns local into world; multiplying `CANVAS_MATRIX` too turns it into screen.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("A position is just a position.", "just a position", "an address in some space")`.

## Prerequisites for the terms card

**Origin** (the point where the numbers are zero), **Space** (a way of measuring positions), **Matrix**, **Transform**. 17 characters or fewer.

## Suggested acts

1. **Three Addresses.** The same corner of a sprite: (−64, −64) local, (some numbers) world, (other numbers) screen. A sprite moved to (300, 200) keeps its local numbers and changes its world numbers. Picture: three origins on one scene.
2. **Converting.** In `vertex()`: `world = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy`; why `vec4` with 0 and 1 (the source says "just include them"; give the real reason in one line if you can source it, else leave it as a rule); pass it to `fragment()` through a `varying`; screen/canvas: `CANVAS_MATRIX * MODEL_MATRIX * vec4(...)`, in that order.
3. **A Texture Locked to the World.** Sample a second texture by `world_position * TEXTURE_PIXEL_SIZE * scale` with `repeat_enable` instead of `UV`; move the sprite and the sprite reveals a different part of a fixed pattern; a cutout at world coordinates (a circle at (100, 150), radius 200) that hides the sprite inside it. Payoff: a character "spacing out" into a fixed starfield with a tween.
4. **Where Is the Screen?** Four ways to get the screen position of a pixel: `VERTEX` in `fragment()`, a `varying` built from the matrices, `SCREEN_UV`, and `FRAGCOORD.xy`; `SCREEN_PIXEL_SIZE` turns pixels into 0 to 1 addresses. Render all four to color and show they agree (and where they would differ, if any: test with a camera that moves and zooms).

## What the source does (my words)

- Draws three spaces on a picture of the project; states `MODEL_MATRIX` and `CANVAS_MATRIX` are `mat4` and vertex-only; gets `world_position` as a `vec2` varying; colors by world position to show it differs from local when the node is moved; builds the world-space circle cutout with `distance(world_position, circle_center)`; locks a space texture with `world_position * TEXTURE_PIXEL_SIZE * 0.1`; animates `amount` with a tween for the "spacing out" effect; in the canvas chapter: `VERTEX` in the fragment stage gives screen pixels, times `SCREEN_PIXEL_SIZE` gives 0 to 1; the varying form `CANVAS_MATRIX * MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)`; `SCREEN_UV`; `FRAGCOORD`.

## Source claims to check or correct

- "The four methods give the same result": test with a moving camera and with the node rotated or scaled.
- The 8-minute intro's world-space UV divides by sprite size 128: that only makes sense for a 128-pixel sprite; mention it as a pitfall.
- Order of matrix multiplication (canvas, model, vertex): verify by trying the other order.

## Facts to verify

Docs: `MODEL_MATRIX`, `CANVAS_MATRIX`, `SCREEN_MATRIX`, `VERTEX` (fragment), `FRAGCOORD`, `SCREEN_PIXEL_SIZE`, `SCREEN_UV`, `TEXTURE_PIXEL_SIZE` (the canvas_item reference you can fetch and quote). Scratch scenes for world position under a moved node, camera moves and rotation.

## Captures

Custom scenes: the world-locked texture (sprite moves, pattern stays); the world-space cutout; the four-methods comparison as four panels.

## Cut line

The cutout beat; the fourth method.

## Other films cover

Post-processing with the screen texture: reading the screen; matrices: matrices film; vertices: vertex film.
