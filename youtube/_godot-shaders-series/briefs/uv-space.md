# Brief: UV Space

**What this is.** The content brief for the film that treats `UV` as a coordinate system you can scale, shift, mirror, center and clip before you look anything up. Slug `uv-space`, folder `claude-liam-lecture-uv-space`, group Fragment techniques, target about 10 minutes (ceiling 15). Title lines: `["UV Space"]`.
**Why.** Almost every effect in the series bends `UV` first. The source course also gives a wrong explanation of why a circle turns oval on a wide shape; this film gives the right one, measured.
**Found.** The source covers this in about 35 minutes across its UV-control, texture, vertex-basics and canvas chapters. The pilot teaches `UV` as an address and uses it as a color and a fade; this film starts from there.

## The one idea

`UV` is the address you look up; change the address before you look and the picture moves, zooms, tiles or mirrors, without the picture itself changing. Moving the address one way moves the picture the other way.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("UV says where a pixel is on\nthe screen.", "the screen", "the shape")`.

## Prerequisites for the terms card

**UV** is recapped (one sentence, not a card entry if you earn it in act 1). Candidates: **Coordinate** (a position given by numbers), **Axis**, **Texture**, **Aspect ratio** (width divided by height). 17 characters or fewer.

## Suggested acts

1. **The Address Book.** `UV` recap; y points down; `texture(TEXTURE, UV)` reads the picture at that address.
2. **Move Where You Look.** Multiply the address by 2 and the picture shrinks to a quarter of the view and tiles or clamps (depending on repeat); subtract 0.25 and the picture moves right and down; add `TIME * 0.1` and it scrolls. Show it with a texture that has an obvious corner. The rule: change the address one way, the picture goes the other. Include the repeat setting (`repeat_enable` on a sampler uniform; `CanvasItem.texture_repeat` for the node's own texture): without repeat the border pixels stretch.
3. **Center and Mirror.** `UV * 2.0 - 1.0` puts zero in the middle (range −1 to 1); `length()` of it is a circle; `abs()` mirrors a shape so one formula draws both sides.
4. **Fixing the Squash.** On a wide rectangle (every ShaderLab capture is 16:9, so the film shows 512 by 288; the 2:1 case, 512 by 256, is measured as evidence) a circle drawn from `distance(UV, vec2(0.5))` comes out as an ellipse. The real cause: `UV` runs 0 to 1 on both axes whatever the shape's proportions. Measure the ellipse from a Lab PNG (width in pixels against height). Fix: scale one axis by the aspect ratio (`TEXTURE_PIXEL_SIZE` or `SCREEN_PIXEL_SIZE` give the proportions: verify which is right for a ColorRect and for a sprite) and show a circle.
5. **Staying Inside the Picture.** Outside 0 to 1 you get repeats or stretched border pixels; mask them with `step` on the address (the source's clip formula multiplies four `step`s); show the border artifact and the fix.

## What the source does (my words)

- Visualizes `UV` as red and green; scales it (`UV * 2` shows only the top-left quarter); offsets with `- vec2(0.4, 0.1)`; explains the inversion with worked numbers; enables texture repeat to see tiles; masks borders with `step(vec2(0.0), scaled_uv)` and `step(scaled_uv, vec2(1.0))`; centers with `2.0 * UV - 1.0` and works three corner examples; uses `abs(UV.x)` to mirror a rectangle; later builds the aspect-ratio correction by multiplying x by a ratio before measuring a distance.
- Its aspect-ratio chapter explains the oval by saying a fragment is a "potential pixel" that can be stretched and "pixels are always squares". That is not the reason.

## Source claims to check or correct

- **Wrong explanation of the oval** (see above): correct it; do not use "fragments can be non-square".
- "Scaling `UV` by 2 shows only the top-left corner": true only when sampling with clamp and the picture occupies the view; describe what you see in the Lab precisely (tiles when repeat is on).
- Verify the claim "moving UV right moves the picture left" with a probe.

## Facts to verify

Docs: `UV` in canvas_item (vertex and fragment), `TEXTURE_PIXEL_SIZE`, `SCREEN_PIXEL_SIZE`, repeat and filter hints, `CanvasItem.texture_repeat`. Lab: sprite with checker texture; `UV * 2.0`, `UV - 0.25`, `UV + vec2(TIME * 0.1, 0.0)` (probes at two times); `2.0 * UV - 1.0` at the corners and center; a 2:1 `ColorRect` (`--size 640x320`) with a circle: measure its width and height in pixels from the PNG; the corrected circle.

## Captures

All Lab: sprite/rect renders; a before/after of the aspect fix; the border stretch and its fix. No editor frames (the `texture_repeat` property is a one-line mention; capture an editor frame only if you show the Inspector).

## Cut line

The mirror beat; the border-mask beat shrinks to one.

## Other films cover

`floor`/`fract` cells and pixelation: patterns film; distance and shapes: shapes film; sine scrolling: time and waves; world and screen coordinates: the space film.
