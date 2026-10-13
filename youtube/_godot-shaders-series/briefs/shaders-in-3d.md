# Brief: Shaders in 3D

**What this is.** The content brief for the film that carries everything from the 2D films into `spatial` shaders and ends by reading a real 3D pad shader line by line. Slug `shaders-in-3d`, folder `claude-liam-lecture-shaders-in-3d`, group Foundations, target about 10 minutes (ceiling 15). Title lines: `["Shaders in 3D"]`.
**Why.** The source course is 2D only, but the shader Bear's Signal Garden game uses is a 3D `spatial` shader (`render_mode unshaded`, `ALBEDO`, `UV` on a quad). The film that explains what the Signal Garden test measured needs this film first.
**Found.** This film is **not** in either source: it is added. Its worked example is a real shader from Bear's game, `walker-claude/godot/signal-garden/signal.gdshader` (copy it into `lab-shaders/` and cite it as "a shader from a small game"). The Lab already renders it (`--kind quad3d`) and reads (0.2588, 0.4392, 0.3059) in the Compatibility renderer and (0.2980, 0.5373, 0.3804) in Forward+ at activation 0.5.

## The one idea

A 3D shader has the same shape as a 2D one (a type line, `vertex()`, `fragment()`, `light()`, uniforms, built-ins); only the outputs and a few built-ins change: you set `ALBEDO` instead of `COLOR`, and `UV` comes from the mesh's own UV map.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("3D shaders are a different,\nharder thing.", "a different, harder thing", "the same shape, new names")` (check the trigger and replacement carry no end punctuation).

## Prerequisites for the terms card

**Mesh** (the points and triangles that make a 3D shape), **Albedo** (the base color of a surface), **Lighting** (how lights change a surface's color), **Renderer**. 17 characters or fewer. `UV` and `uniform` are recapped in one sentence each (standalone).

## Suggested acts

1. **Same Shape, New Names.** `shader_type spatial;`; same three functions; the surface outputs (`ALBEDO`, `ALPHA`, `EMISSION`, `ROUGHNESS`, `METALLIC`: name the few you verify in the docs); there is no `COLOR` here. `UV` follows the mesh's UV map (a `QuadMesh` is a flat rectangle with the same 0 to 1 addresses).
2. **Lit or Unlit.** Default surfaces are lit by lights and the environment; `render_mode unshaded;` skips lighting so `ALBEDO` is the color you get (verify in the Lab with an ambient-lit quad and an unshaded one). A few other render modes by name only (verify: `cull_disabled`, `blend_add`, ...).
3. **A Surface That Changes.** Build up on a quad in the Lab: a UV gradient, stripes (`step(0.5, fract(UV.x * 8.0))`: gloss `step` and `fract` in one phrase each), then two `source_color` colors mixed by an `activation` uniform from 0 to 1.
4. **Read a Real One.** The 8-line pad shader, line by line (header, render mode, three uniforms, the stripe, the base color, `ALBEDO = mix(...)`).
5. **Which Renderer?** The same shader at activation 0.5 in two renderers: two measured pixels. Say what it means: the mix happens on different numbers. Leave the full explanation to the color film; close with "a number read from a pixel is only true for this renderer".

## What the source does

Nothing on 3D. Use: the Godot 4.7 spatial shader reference (built-ins, render modes, outputs), the introduction page, Bear's chapters (`csye-7270-building-virtual-environments/chapters/06`, `07`, `08`) for earlier runs, and the Signal Garden files.

## Source claims to check

None from the sources. Check every built-in or render mode you name in the docs (spatial reference), and that `UV` orientation on a `QuadMesh` matches the 2D picture (top left 0,0 as seen from the front: verify with probes at known corners).

## Facts to verify

Docs: spatial shader reference (processor functions, `ALBEDO`, `ALPHA`, `EMISSION`, `render_mode` list). Lab: `--kind quad3d` renders of each shader you show; the pad shader in both renderers (`--renderer forward_plus` and `gl_compatibility`); lit versus unshaded result of the same `ALBEDO`; stripe positions (`UV.x` probes at 0.0625 and 0.1875 for dark and light stripes: check which is which).

## Captures

All Lab `quad3d`. The pad shader is the film's payoff, so capture its activation sweep 0 to 1 as a video.

## Cut line

The render-modes beat shrinks to a sentence; the stripes build merges with the real-shader reading.

## Other films cover

`step`/`fract`/`mix` in depth: math toolkit; `source_color` and color spaces in depth: textures and color; lighting in 3D (normals, roughness, shadows) is out of scope for the series; vertex displacement in 3D: out of scope (the vertex film is 2D).
