# Acts and coverage map: Making Water in Godot

**What this is.** How this film is built from Bear's request and from the progression of a third-party Unity Shader Graph water tutorial that he named as a model of the ORDER of ideas only: which idea lands in which act, which parts are left out and why, the cast per act, the opening correction, the terms the film earns and where each is defined on screen, the additions that are in neither source, and the cut line.
**Why.** A film that borrows a progression must show that nothing was copied and that nothing Bear asked for was dropped silently. This file is that record, and the cut line says what leaves first if the audio runs long.
**Found.** Five acts, 49 body beats, about 11 minutes by the series estimate (12.1 minutes is the lint's deliberately long figure; Liam's real pace is usually about 7 percent faster). Every step Bear named is built: blue, see-through, noise foam, UV manipulation with normal maps, vertex waves, depth-based shore foam, and the Inspector. Left out: METALLIC (water is not metal; the film never touches it), reflections and refraction (further steps in the Unity video; not built), the Unity-specific steps and all sponsor material. Seven things in the film are in neither source; each was run, not read.

## The sources (nothing copied)

- **Bear's request (verbatim in `SOURCES.md`).** The arc: blue, then a little transparent, then noise foam, then UV manipulation and normal maps for waves; vertex wave and depth foam optional if they earn a place. A Godot 4.7.2 text-shader film; every picture real.
- **A third-party Unity Shader Graph water tutorial** (a YouTube video with sponsor reads, creator not named in what Bear passed on). Used only as a model of the progression: a plane, a shader, a material; base colour as a property; a cellular noise whose cell offset moves with time (density and speed as properties); sharpening the cell edges with a power curve; a brighter colour added on top and alpha dropped a little; a second distortion on the noise's UV; a vertex displacement from a scrolled noise multiplied into the up-pointing normal, shown with a floating object bobbing; reflections, refraction and intersection foam named as further steps. Its wording, jokes, sponsor material and Unity steps are not used and its transcript is stored nowhere (see `SOURCES.md`).
- **The Godot 4.7 documentation and the installed Godot 4.7.2** (every number was measured here).

## Coverage

| Item (Bear's request or the model's progression) | Where it goes | Note |
|---|---|---|
| Setup: a plane, a shader, a material on the plane | **Act I** B02, B03 | PlaneMesh, ShaderMaterial, the Material Override slot (real Inspector label); the plane starts as a plain grey plane and the shader is assigned on camera (B03) |
| Set the surface to transparent | **Act I** B06, B07 | In Godot there is no setting: writing `ALPHA` is the switch (docs: it moves the material to the transparent pipeline) |
| A base blue colour as a property wired to albedo | **Act I** B03, B04 | `uniform vec3 : source_color` into `ALBEDO`; the typed numbers read back as typed in Forward+ (25, 115, 178) |
| Roughness (Bear's list: ALBEDO / ALPHA / ROUGHNESS / METALLIC / NORMAL_MAP) | **Act I** B05 | The sun's reflection tightens as roughness falls |
| METALLIC | **LEFT OUT** | Water is not metal; the default is right; no beat would teach anything. Reported to Bear |
| A little transparent (the model: alpha about 0.8) | **Act I** B06 to B09 | Default opacity 0.7 (the rocks stay visible); the blend arithmetic is checked against a rendered pixel in both renderers |
| `render_mode` choices: `blend_mix`, `cull`, `depth_draw` | **Act I** B10 | The three defaults, written out, with the docs' words; `cull_disabled` and depth-write are explained, the cull effect was run (FACTCHECK row) but is not a beat |
| What transparency costs | **Act I** B11, B12 | Draw order and sorting; no shadows; not in the depth or screen textures (docs), plus the measured depth gap |
| The renderer caveat (Forward+ against Compatibility) | **Act I** B09, **Act III** B33, **Act V** B47 | A measured number on every renderer-dependent claim; every capture is labelled with its renderer |
| Noise: ripples from a cellular noise whose points move with time; density and speed as properties | **Act II** B13 to B21 | A hand-written hash-based function; Godot has no Voronoi node and no noise function (counted, not assumed) |
| Sharpen the cell edges with a power curve | **Act II** B22, B23 | As the alternative to the edge-distance line; with its real trap (pow of a negative base) |
| A brighter colour added on top of the base; alpha dropped so the edge is a little see-through | **Act II** B19, B20 | In Godot the foam is opaque (alpha rises) and matte (roughness rises): the opposite of the model's choice, for a reason shown (B20) |
| `NoiseTexture2D` (FastNoiseLite, seamless, `as_normal_map`) as sampler inputs | **Act II** B24, **Act III** B26 to B28 | A cellular texture against the function (B24); the normal map from Godot's own noise (B26, B27) |
| UV scrolling with TIME | **Act III** B29, B30 | One layer, then two layers moving opposite ways |
| UV manipulation (the model: a radial shear on the noise's UV) | **Act III** B32 | The foam's address pushed along the wave slope (the normal map doubles as a flow field) |
| Normal maps for the wavy effect | **Act III** B25 to B31 | Strength, colour-as-direction, seamless, sampler hints, scrolling, and the straight edge that proves they change light, not shape |
| Vertex displacement of a subdivided `PlaneMesh` with a matching `NORMAL` | **Act IV** B34 to B37 | Vertex count (cuts + 2) squared; two sines; the normal from the slope; the glare before and after |
| A floating object bobbing | **Act IV** B38 to B41 | The script mirrors the wave function; one shared clock; the CPU and GPU heights agree to about three millimetres |
| Reflections, refraction | **LEFT OUT** | Named as further steps in the model; not built; the film does not claim them |
| Intersection foam (the model's step 7) | **Act V** B42 to B47 | Built, because it is the one effect a texture cannot do and it needs the depth texture |
| Shader parameters exposed to the Inspector so the viewer can restyle | **Act I** B04, **Act V** B48, B49 | `hint_range`, `source_color`, `group_uniforms`; a real Inspector frame (scripted editor session); three looks from one shader |
| Sponsor reads, jokes, Unity-specific steps (Shader Graph nodes, Sample Gradient, the HDR colour) | **LEFT OUT** | Not part of the progression; none of it is used |

## Added: in neither the request nor the model (each run, FACTCHECK.md)

1. The alpha blend is done in linear light in Forward+ and on the typed numbers in Compatibility: the same water reads 108 against 71 for red (B08, B09).
2. `FastNoiseLite` smears a cellular noise into mush unless its fractal type is None (B24 caption; texture minimum 0.004 against 0.000).
3. `pow` of a negative base is undefined, and the nearest cell distance can pass one: 462 pixels went black in one frame (B23).
4. The sampler's `repeat_enable` is not decoration: without it a scrolled normal map smears into streaks (B28).
5. A built-in that belongs to one processor function (`UV`, `VERTEX`, `SCREEN_UV`, `INV_PROJECTION_MATRIX`) is not visible in a helper function; `TIME` and `TAU` are (B45).
6. The shader's `TIME` and `Time.get_ticks_msec()` start at different moments, differing by about 0.3 s (0.28 to 0.32 s across six logged real-time runs), so a script that must agree with the shader writes its own clock into a uniform (B40).
7. Compatibility counts depth from minus one to one: without one preprocessor line, the depth gap reads 0.000 everywhere and the whole surface turns to foam (B47).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I Blue and Clear | the cove from the 3/4 camera: the 8 by 8 plane, the sand floor and beach, the grey rock above the water and the submerged box, the teal buoy, the cream crate (always the same positions); in the drawings the same buoy, rock and sand slab |
| II Foam | the top view of the bare plane (square window); the grid of squares with one terracotta dot each (drawings use the series' pixel-grid cast) |
| III Ripples | the cove from the 3/4 camera; the real 512 by 512 normal map; the low camera on the bare plane |
| IV Real Waves | the low camera on the bare plane (flat in Act III, waving here); the cove with the buoy and the crate riding the waves |
| V The Shore | the cove from the 3/4 camera with the finished shader; the camera, the water line and the sand line of the depth drawing |

## Opening correction and terms

- **BIDEA**: the writer types "Making water needs a water simulation." and replaces "a water simulation" with "six small tricks".
- **BDEFS** (prerequisites only, wording from the series GLOSSARY): Shader, Vertex, Pixel, Texture, UV, Renderer. The terms this film exists to teach are earned in their acts and defined on screen where first spoken:

| Term | Beat | On-screen definition |
|---|---|---|
| spatial | B03 | spatial: a shader for 3D surfaces (cue label) |
| fragment | B03 | fragment: runs once for each pixel the shape covers (GLOSSARY) |
| built-in | B03 | built-in: a value the engine hands to a function (GLOSSARY, caption) |
| albedo | B03 | albedo: the base color of a 3D surface (GLOSSARY) |
| uniform | B04 | uniform: set from outside; every pixel sees the same one (GLOSSARY) |
| source_color | B04 | the numbers are sRGB; convert to light first (GLOSSARY short form) |
| roughness | B05 | roughness: 0 is a mirror, 1 is fully matte |
| alpha | B06 | alpha: 0 is invisible, 1 is solid (GLOSSARY) |
| dot, sine, fract | B15 | dot: multiply matching parts, add them up; sine: a smooth wave between -1 and 1; fract: the part after the point: x minus floor(x) (GLOSSARY) |
| length | B17 | length: of an offset, the distance (GLOSSARY) |
| smoothstep, mix | B19 | smoothstep: eases from 0 to 1 between two edges; mix: blends from a to b; t of 0 gives a, 1 gives b (GLOSSARY) |
| TIME | B21 | TIME: seconds on one clock shared by the whole game (GLOSSARY) |
| pow, clamp | B22, B23 | pow: x raised to the power y; clamp: pins x inside a range (GLOSSARY) |
| texture | B24 | texture: an image a shader can read by address (GLOSSARY) |
| normal map | B25 | normal map: an image of which way each pixel faces (GLOSSARY) |
| hint_normal, repeat_enable | B28 | the image holds directions, not colors; the address may wrap past 1 (docs: "Used as normalmap."; "Enabled texture repeating.") |
| normal | B37 | normal: a direction at right angles to a surface (GLOSSARY) |
| vertex() | B36 | vertex(): runs once for each vertex; places the corners (GLOSSARY) |
| wave_height, wave_length, wave_speed | B41 | how tall / how long / how fast (cue labels) |
| depth texture | B43 | near is 1, far is 0, and not a distance (docs: reverse-z) |
| CURRENT_RENDERER | B47 | which renderer is running (docs) |

## Cut line

If the film runs long, cut in this order: the renderer-ripples beat (B33: it repeats the renderer lesson of B09), the power-curve pair (B22 and B23: an alternative to the edge line, with its trap), the baked-texture beat (B24), the sorting and cost beats (B11 and B12: docs only, nothing is measured), and the built-ins-in-a-function beat (B45: a compile error, not the main line). The blend arithmetic (B08, B09), the noise net (B14 to B19), the normal map (B25 to B28), the real waves (B35 to B39) and the shore (B42 to B44, B46) stay: they are the arc. Cutting all of the first group saves about 100 seconds. Current estimate: about 11 minutes, so no cut is needed.
