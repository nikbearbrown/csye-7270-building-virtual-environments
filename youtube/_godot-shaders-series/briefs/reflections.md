# Brief: Reflections

**What this is.** The content brief for the film that uses `BackBufferCopy` to control when the screen is captured, and a hidden mask layer, to build a water reflection under a character. Slug `reflections`, folder `claude-liam-lecture-reflections`, group Screen, textures and light, target about 9 to 10 minutes (ceiling 15). Title lines: `["Reflections"]`.
**Why.** It is the clearest example of using the screen texture as *data* rather than as a picture: a mask drawn on the screen that the player never sees.
**Found.** About 13 minutes of source. The source compares a screen color to pure red or green with `==`; the docs warn against exact float comparisons, so the film should use a tolerance.

## The one idea

A shader that reads the screen sees everything drawn before it. `BackBufferCopy` decides *when* the screen is captured; place it between a hidden mask layer and the visible layers, and the shader can read the mask without the mask ever appearing in the game.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("A reflection needs a second\ndrawing of the scene.", "a second drawing of the scene", "a mask the shader can read")`.

## Prerequisites for the terms card

**Screen texture** (recap), **Mask**, **Draw order** (which things are drawn first), **Reflection**. 17 characters or fewer.

## Suggested acts

1. **The Hidden Mask Problem.** A map with water: you want to know, per pixel, "is this water?" The cleanest answer is a layer painted in flat colors (red for water, green for coast); but you do not want it visible.
2. **BackBufferCopy.** Three colored sprites and an overlay shader that reads the screen: with the node after all three you see all three; move `BackBufferCopy` between sprites and the shader sees only what was drawn before it. Copy mode: viewport, rectangle, disabled (docs).
3. **A Reflection.** A copy of the animated character, flipped vertically, below the original and kept in step with a `RemoteTransform2D`; its shader reads the screen at its own position: if the mask there is red, show it (alpha 1), else hide it.
4. **Polish.** Compare colors with a small tolerance (`distance(screen_rgb, vec3(1.0, 0.0, 0.0)) < 0.1`), not `==`; a coast value with lower alpha; a blue tint with `mix`.

## What the source does (my words)

- Three tinted sprites and an overlay shader; `BackBufferCopy` with copy mode viewport; moving it down the draw order hides nodes from the screen texture; the game scene has a visible tile layer and a mask layer painted in Photoshop (red water, green coast); `RemoteTransform2D` keeps the flipped reflection under the player; the reflection's shader reads `screen_texture`, `water_alpha = float(screen_color == vec3(1,0,0))`, multiplies `COLOR.a`; adds `coast_alpha` with 0.3 and water with 0.5; tints with a `source_color` uniform and `mix(…, 0.2)`.

## Source claims to check or correct

- Exact `==` on floats: the docs warn; test whether it works anyway for 8-bit colors in this renderer and say why you prefer the tolerance.
- Whether the mask layer (drawn before the copy) is hidden from the visible result: the source does it with draw order; verify there is no flicker or ordering surprise in a scratch scene.
- `BackBufferCopy` modes and the "viewport" mode requirement: quote the docs.

## Facts to verify

Docs: BackBufferCopy class reference and the screen-reading shaders page; `RemoteTransform2D`; comparison guidance. Scratch scene: the three-sprite demo with the copy node in each position (record which sprites the overlay sees); the mask-driven reflection with a moving character.

## Captures

Custom scenes only (describe the node trees exactly and the scripted movement).

## Cut line

The coast/tint polish.

## Other films cover

The basics of `hint_screen_texture` and full-screen effects: reading the screen; masks as math: shapes film.
