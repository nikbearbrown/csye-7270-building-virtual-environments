# Brief: Soft Edges, Glow and Noise

**What this is.** The content brief for the film that turns hard cuts into ramps you control (`smoothstep`), shapes falloff (`pow`), layers a highlight, scrolls a noise texture, and tells the truth about glow. Slug `soft-edges-glow-and-noise`, folder `claude-liam-lecture-soft-edges-glow-and-noise`, group Fragment techniques, target about 10 minutes (ceiling 15). Title lines: `["Soft Edges, Glow", "and Noise"]`.
**Why.** The energy-shield build in the source is the series' first "layered" effect. Its smoothstep explanation is wrong and its glow trick needs a setting it never names, so both need testing.
**Found.** About 25 minutes of source. This film is the natural home for the noise-texture reveal in the short intro video too.

## The one idea

`smoothstep` is a hard `step` with a defined start and end, so you decide how soft the edge is. Multiply or add masks to layer effects. Noise gives structure; scrolling it gives motion. A color above 1 only *looks* like glow if the project is set up to show it.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("A soft edge needs a blur.", "a blur", "a ramp")`.

## Prerequisites for the terms card

**Mask**, **Falloff** (how quickly a value fades with distance), **Noise** (a texture of smooth random values), **HDR** (colors allowed to go brighter than 1) — earned or defined in the card; 17 characters or fewer. `step`, `distance` get a half-sentence.

## Suggested acts

1. **From Cut to Ramp.** `step` against `smoothstep(a, b, d)` on `distance` from the center: the same circle with a hard edge and then with a soft one; the band between a and b is the softness; a width uniform. Draw the true S-curve (not a line) and give one number.
2. **Falloff and Highlight.** `1.0 - distance(UV, spot)` makes a bright spot; `pow(spot, 3.0)` tightens it (higher power, smaller spot); multiply by the main shape so it stays inside.
3. **Layering.** main shape + highlight; the order-of-operations bug (multiply happens before add, so wrap the sum in parentheses) with real numbers; colors from `source_color` uniforms: `main_color * main + highlight_color * highlight`.
4. **Noise That Moves.** A `sampler2D` noise uniform with `repeat_enable`, a seamless `NoiseTexture2D`, and `texture(noise, UV + vec2(TIME * 0.1, 0.0)).r` multiplied into the alpha; what happens without repeat (the scroll stops at the edge) and without seamless (a visible seam).
5. **Glow, Honestly.** Multiply a color by 5 and you have a number above 1. Whether you see glow depends on HDR 2D and a glow-enabled environment. Run it three ways: neither on (it clips to white), HDR 2D only, HDR 2D plus glow in a WorldEnvironment. Report what each looks like.

## What the source does (my words)

- Main circle with `step`, an inner gradient by multiplying with the distance, then `smoothstep(min, max, distance)` with a width uniform (halved to cap at 0.5); a highlight spot `1 - distance(UV, highlight_center)` times main shape, then `pow(..., 3.0)`; two `source_color` colors; glow as `color * (1 + glow * 5)`; a noise texture sampler with `repeat_enable` and seamless noise, scrolled by `TIME`; a vertex pulse `VERTEX += normalize(VERTEX) * sin(TIME) * amount`.
- Explains `smoothstep` as "limit one 0, limit two 10, value 1 returns 0.1".

## Source claims to check or correct

- **`smoothstep` is not linear**: 3t² − 2t³. The source's 0.1 is the linear answer; the real one for t = 0.1 is 0.028. Correct it.
- **Glow**: "multiply by five and it glows" is true only with HDR 2D and glow on; find the Godot docs on `hdr_2d`/Environment glow and quote them; verify by experiment (write a scratch scene with and without).
- The vertex pulse needs `normalize(VERTEX)` to scale outward from the center; verify the direction claim, or leave the pulse out.

## Facts to verify

Docs: `smoothstep`, `pow`, `repeat_enable`, NoiseTexture2D seamless, project setting for HDR 2D, Environment glow. Lab: soft circle at known distances (probes), highlight, the parentheses bug as a before/after, noise scroll at two times; scratch scene for the glow experiment (WorldEnvironment is not in the Lab runner).

## Captures

Lab renders; a glow comparison made from a custom scene (three stills).

## Cut line

The vertex pulse (already optional) and the multiply-before-add beat shrink to one.

## Other films cover

Textures in general and `source_color` in depth: textures and color; the `smoothstep` function table entry: math toolkit; sine scrolling: time and waves.

**Added by the layout (2026-10-13):** the source and this brief omit one glow requirement. The HDR route needs the WorldEnvironment background mode set to **Canvas** as well (without it nothing glows; Soft Edges film G4), and a dark surround.
