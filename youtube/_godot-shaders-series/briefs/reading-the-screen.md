# Brief: Reading the Screen

**What this is.** The content brief for the film on the screen texture: a shader reading what has already been drawn, to build full-screen effects and a water distortion. Slug `reading-the-screen`, folder `claude-liam-lecture-reading-the-screen`, group Screen, textures and light, target about 10 to 11 minutes (ceiling 15). Title lines: `["Reading the Screen"]`.
**Why.** Screen-reading shaders are how post-processing, glass, heat haze and water work. They are also where Godot 3 habits break (`SCREEN_TEXTURE` is gone). The short intro video ends with a water shader built on exactly this.
**Found.** About 19 minutes of source (canvas) plus the 8-minute intro's water section, which was held back from the pilot for this film. Bear's chapter on shader foundations already documents the removal of `SCREEN_TEXTURE` and the overlap rule.

## The one idea

Declare `uniform sampler2D screen_texture : hint_screen_texture;` and the engine fills it with everything drawn so far. Read it with `SCREEN_UV` and your shader can recolor, bend or mix what is behind it.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("A shader only knows its own\nsprite.", "its own sprite", "what is already on screen")`.

## Prerequisites for the terms card

**Screen**, **Post-processing** (changing the picture after it is drawn), **Layer** (a drawing order group), **Uniform** (recap). 17 characters or fewer.

## Suggested acts

1. **The Screen Texture.** The declaration; `texture(screen_texture, SCREEN_UV).rgb`; a sprite that is a window onto what is behind it; invert it (`1.0 - rgb`). Note: Godot 4 removed `SCREEN_TEXTURE`; the old tutorials' line fails with a helpful message.
2. **Full-Screen Effects.** A `CanvasLayer` with a `ColorRect` anchored to the full rectangle and a shader on it; grayscale; a grayscale-outside, color-inside circle around the player (centered, aspect-corrected: `x` scaled by the screen's width over height from `SCREEN_PIXEL_SIZE`); pixelate the circle.
3. **Bend What's Behind.** Offset `SCREEN_UV` by a sine wave and sample: the picture wobbles like water seen through glass; mix it with a water texture sampled with *different* UVs (otherwise it looks fixed to the screen); a soft wavy top edge for a pool; a foam line. This is the water shader from the short intro, rebuilt.
4. **What It Can See.** The screen texture holds what was drawn *before* this node (draw order); in 2D, if two screen-reading shaders overlap, the second does not see the first (docs); `repeat_disable, filter_nearest` hints; why full-screen effects belong on a top `CanvasLayer`.

## What the source does (my words)

- A canvas intro scene: reads `SCREEN_UV` and `VERTEX` colors; four ways to get screen position; screen texture with `hint_screen_texture` inverts the background; a full game scene with a top `CanvasLayer` + `ColorRect` (anchors full) that grays out the island except a circle around the player; the circle is an ellipse until corrected with the ratio from `SCREEN_PIXEL_SIZE`; pixelates it with `floor(square_uv * pixel_size) / pixel_size`.
- The short intro: waves added to `SCREEN_UV`, mixing the water texture with different UVs, "overlay" blending for a natural look, a foam line.

## Source claims to check or correct

- That the screen texture holds "everything up to this node": verify with draw order, including inside a `CanvasLayer`.
- "Overlay blend": Godot has no built-in `overlay()` in the shading language; write the formula and verify it (the visual shader has an overlay node; the code form is a few lines): use the standard definition and cite it.
- The ellipse explanation: see the UV film; here only correct the aspect with the ratio.

## Facts to verify

Docs: "Screen-reading shaders" page; `hint_screen_texture`; CanvasLayer/ColorRect anchors; `SCREEN_PIXEL_SIZE`, `SCREEN_UV`. Scratch scenes: a background + a sprite with the shader inverting what is behind; a CanvasLayer full-screen effect; overlap behavior of two screen-reading shaders; the water recipe in steps.

## Captures

Custom scenes (describe each node tree): invert window; full-screen gray vignette with a moving circle (scripted input); the water pool (video). The reflections film uses `BackBufferCopy`; do not duplicate it.

## Cut line

The pixelated vignette; the foam line.

## Other films cover

`BackBufferCopy` and masks: reflections; `SubViewport`: subviewports film; screen coordinates: spaces film; wave math: time and waves.
