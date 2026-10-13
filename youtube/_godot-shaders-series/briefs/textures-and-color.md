# Brief: Textures and Color

**What this is.** The content brief for the film on reading textures and doing math on color, including why a color number is not the color you see. Slug `textures-and-color`, folder `claude-liam-lecture-textures-and-color`, group Foundations, target about 10 minutes (ceiling 15). Title lines: `["Textures and Color"]`.
**Why.** Color is where shader results and shader tests disagree most. The same shader reads different pixels in different renderers (measured 2026-10-13), which is exactly what a headless test cannot see.
**Found.** The source course covers textures in two chapters (about 28 minutes) and does not mention color spaces at all. The Shader Lab already measured the key fact: the pad shader at activation 0.5 reads (0.2588, 0.4392, 0.3059) in the Compatibility renderer and (0.2980, 0.5373, 0.3804) in Forward+. This film should reproduce that on a small canvas-item shader and explain it.

## The one idea

A texture is a table you look things up in by address; a color is four numbers; and "the number I wrote" and "the color on screen" are only the same thing if you know which color space and which renderer you are in.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("A texture is a picture\npasted onto a shape.", "pasted onto a shape", "looked up by address")` (the first draft broke the trigger across the newline).

## Prerequisites for the terms card

**Texture** (an image a shader can read), **Channel** (one of red, green, blue, alpha), **Alpha** (how see-through), **Renderer** (the part of Godot that draws). 17 characters or fewer.

## Suggested acts

1. **Reading a Texture.** A `sampler2D` uniform; `texture(tex, UV)` returns a `vec4`; `TEXTURE` is the node's own texture; filter and repeat hints (`filter_nearest`, `repeat_enable`); where textures come from (an image file, `GradientTexture`, `NoiseTexture2D`). Show reading the same texture with different UVs (the UV film goes deeper).
2. **Color Is Math.** Channels; tint = multiply; invert = one minus; grayscale by one channel or by a weighted sum (say which; verify the weights you use); `mix` between two colors by a mask; alpha as a fade.
3. **Noise as a Mask.** A noise texture plus `step` makes a dissolve; a gradient texture as a color ramp for the edge. Payoff beat: a dissolve that burns away with a colored edge.
4. **The Color You Set Is Not the Color You See.** `source_color`: what it does and why it exists (color pickers are sRGB; math is cleaner in linear light). Run the same `mix` in both renderers (`--renderer forward_plus` and `gl_compatibility`) in **both** a canvas-item and a spatial shader and report each pixel. Explain the difference in one picture. State plainly what a pixel probe measures: this renderer's output for this shader.
5. Optional: **Hue.** Skip unless there is room (the patterns film has the HSV function).

## What the source course does (my words)

- Texture work in the node editor: a `Texture2D` node with `sampler2D`, UV by default; gradient and noise textures made in the Inspector; `one minus` to invert; `step` on noise for dots; `mix` with the original color; the rule that an assigned texture is scaled to the original texture's UV (aspect ratio matters; squares are easiest).
- Color: float to vec3 gives grey (the value is copied to all three); vec4 to vec3 drops alpha; vec2 to vec3 pads blue with zero; grayscale by taking the red, green or blue channel (source admits it favors a channel).
- Time-based exercise: fade blue in with `clamp`/`min` of time.
- In code: `uniform sampler2D tex;`, `texture(tex, UV)`; in the shield chapter, a `sampler2D` noise uniform needs `repeat_enable` and a seamless `NoiseTexture2D` to scroll.

## Source claims to check or correct

- The source never mentions sRGB versus linear; add it, with measured numbers.
- Grayscale "by picking a channel" is a simplification; if you show the weighted version, give the weights and a source.
- Bear's own chapter notes (from reading the 4.7.2 source, not from a pixel) that the Compatibility renderer does no sRGB-to-linear conversion on 2D uniforms and Forward+/Mobile convert a `source_color` uniform in 2D only when the viewport renders in HDR. **Test it** and report what you find in 2D and in 3D separately.

## Facts to verify

Docs: `source_color`, filter and repeat hints, `hint_default_*`; color spaces in Godot's rendering docs (find the page and quote it). Lab: pad-style shader in both renderers (done once in 3D: Compatibility (0.2588, 0.4392, 0.3059), Forward+ (0.2980, 0.5373, 0.3804)); the canvas-item equivalent; `mix` midpoint of two `source_color` colors in each renderer; whether the Inspector's color picker shows the value you typed.

## Captures

Lab renders for the dissolve (noise + gradient; sprite kind), the two-renderer comparison (two stills, side by side), tint/invert/gray on the test sprite. Editor frame E3 (a `source_color` uniform shows a color picker) is shared with the pilot's evidence; capture it here if it is not done.

## Cut line

Drop the dissolve to a single beat; drop grayscale.

## Other films cover

UV bending (UV film); noise scrolling and glow (soft-edges film); `varying` color (vertex film); HSV hue cycling (patterns film).
