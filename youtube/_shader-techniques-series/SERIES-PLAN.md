# Series plan: shader techniques, in order

**What this is.** The plan for a series of fifteen standalone Godot lecture films (Liam, about ten minutes each, no course name, never numbered) that teach, one technique at a time and in Bear's order, the sixteen lesson shaders now converted to Godot 4.7.2: a flat color and the first lit shader, Lambert, Lambert with ambient, Fresnel, Phong, diffuse maps, spec maps, normal maps, cube maps, vertex animation, UV manipulation, techniques, blend maps, the car shader and the uber shader. Planning only: no beat sheets, no audio, nothing rendered. Written 2026-10-16.
**Why.** Bear asked for the Cg lessons converted to Godot and "a film going through all of those, teaching the various techniques in order", starting with base and super simple together. The conversion is done and every shader was run, so each film below can promise only numbers that were measured (project: `shader_lessons_godot/`, notes: `shader_lessons_godot/CONVERSION-NOTES.md`).
**Found.**
- **The premise of the first film is half true.** `00_superSimple` is a flat color, but `01_base` is already a complete Lambert shader and is the same file as `02_lambert` (the converted pair renders identically: 0 differing pixels in both renderers). So "super simple and base are basically the same" does not hold, and the film Bear wants second ("a Lambert") would repeat the film he wants first unless the two are split by purpose. Recommendation below; it needs Bear's word.
- **Each film has a measured surprise to open or end on.** The base shader's default light lights only the underside; the cube-map lesson shows no reflection on a surface that faces the camera; the spec-map lesson quietly drops a factor the three before it had; the normal-map and uber lessons disagree about the green channel; the same converted shader gives different pixels in Forward+ and Compatibility (a Lambert pixel reads 173 against 107) because only Compatibility does its arithmetic the way the Cg did.
- **Nothing here is blocked except by rights.** The sources are third-party (Eat 3D, "Shader Production DVD", credit "Luiz"); rights are not confirmed by Bear, and the films would show converted code on screen. That is decision 3 below.
- Next step: lay the films out one at a time, a pilot first (see the end).

Nothing viewer-facing carries a number, a count, or the words "part", "episode", "series" or "course". The numbers in the shader file names (`06_diffuse_mapped`) are the original CgFX numbers, kept for traceability only; they never appear in a title, a card or the narration. This document refers to films by working title.

---

## The series at a glance

Order is Bear's. Each film builds on the shader of the one before and says, in a sentence or two, anything it needs from another film (the standalone rule). Working titles are mine.

| Film (working title) | Converted shader | The one idea | Ends on | About |
|---|---|---|---|---|
| The Smallest Shader | `00_super_simple`, `01_base` | A shader is two small programs: one places the corners, one colors the pixels | The flat disc becomes a sphere with three added lines | 10 min |
| Lambert: Light Is a Dot Product | `02_lambert` (same code as `01_base`) | Brightness is how directly a surface faces the light, not how close it is | Dial the light around the sphere; the Cg's own default light lights the underside | 10 min |
| Ambient: The Floor Under the Light | `03_lambert_ambient` | The dark side is not black because something other than the lamp lights it; ambient is a cheat floor | The sphere's dark side gains shape | 9 min |
| Fresnel: Light at the Edge | `04_fresnel` | Surfaces reflect more at a glancing angle; a power makes the rim thin | A lit sphere with a rim that fades on the dark side | 10 min |
| Phong: The Highlight | `05_phong` | A highlight depends on where you stand: mirror the view about the normal and compare with the light | The full lighting model without textures; the highlight moves with the camera | 10 min |
| Diffuse Maps: Paint, Then Light | `06_diffuse_mapped` | A texture multiplies the color before the lighting; rim and highlight are added after | A lit checker sphere | 10 min |
| Spec Maps: Where It Shines | `07_spec_mapped` | A mask in a texture says where the shine is allowed, per pixel; masks are numbers, not colors | The highlight cut off at a mask boundary | 9 min |
| Normal Maps: Lying About the Surface | `08_normal_mapped` | A normal map changes only the normal the light sees; the silhouette stays smooth | A sphere covered in domes that are only lighting | 11 min |
| Cube Maps: Reflecting a World | `09_cube_mapped` | A reflection is a lookup in a picture of the world, in the direction of the mirror ray | A sphere reflecting a sky and a floor, and the surprise that its center reflects nothing | 10 min |
| Vertex Animation: Moving the Corners | `10_vertex_anim` (file `10_vertex_anim.gdshader`) | Offset each vertex by a sine before the matrices; the lighting does not follow | A wobbling sphere whose shading stays that of the round one | 9 min |
| UV Manipulation: Sliding the Picture | `11_uv_manip` | Scale, shift and scroll the address, not the surface; scale 2 tiles, it does not zoom | A scrolling, tiled, normal-mapped sphere | 9 min |
| Techniques: One Shader, Four Behaviors | `12_techniques` | A material is a shader plus render states; Godot picks them at compile time | Four spheres: opaque, blended, tested, added | 10 min |
| Blend Maps: One Texture, Three Colors | `13_blended` | A texture channel can be a selector that picks among colors | A sphere in three paints | 8 min |
| The Car Paint Shader: Tuning the Reflection | `14_car_shader` | Control the reflection with an offset, an intensity, a contrast and a second highlight | A red paint sphere with a sky in it | 9 min |
| The Uber Shader: Everything at Once | `15_uber` | Every earlier idea, recombined, plus a hemisphere ambient and a fake subsurface | The finished shader, line by line, each line named for the film that taught it | 11 min |

Lengths are targets from the series rules (40 to 46 body beats, 1,400 to 1,700 words); the real length is known only after the voice is generated. Nothing is voiced.

## Order and dependencies

Each shader is the previous shader plus one idea (the file diffs are in the notes), so the order is the dependency order:

`The Smallest Shader` to `Lambert` to `Ambient` to `Fresnel` to `Phong` (the full lighting model, no textures) to `Diffuse Maps` to `Spec Maps` to `Normal Maps` (all four texture-free lights now meet textures) to `Cube Maps` (branches off Phong, not off the maps: its shader has no textures) to `Vertex Animation` and `UV Manipulation` (each adds one stage to the Phong or normal-mapped shader) to `Techniques` (needs the rim from Fresnel, because the rim is the alpha) to `Blend Maps` to `The Car Paint Shader` (needs Cube Maps) to `The Uber Shader`, **the payoff: it recombines every earlier idea and the film names which film each of its lines came from, without a number.**

The two cube-map films share one cube map (six code-authored faces); the three normal-map films share one dome map. All films use the same stage: a sphere and a torus, one camera, one light direction, so a viewer who has seen two films recognizes the third.

---

## Decisions about splitting and merging (recommendations only; Bear's order is unchanged)

1. **The first two films.** Bear asked to start with base and combine super simple into it. Reality: `00` is a flat color and `01` is Lambert, the same as `02`. Two ways to honor the order:
   - **A (recommended).** The first film teaches the *skeleton* with `00` (corners and pixels, the matrix line, one uniform color) and then *reveals* `01_base`: the same two programs with a normal and a light direction added, and the flat disc turns into a sphere. It stops at "it works". The second film (`Lambert`) is the film that explains *why*: the dot product, the floor at zero, the sign of the light direction, the two-renderer pixel difference. Same code appears twice, once as a reveal and once as an explanation, which is how the viewer needs it. Both films keep their ten minutes of content without padding.
   - **B.** Make the first film the flat color plus Lambert in full (as Bear described: base is "basically" the starting point) and **drop** the Lambert film: fourteen films, and Ambient follows directly. The first film would carry the dot product, the gamma surprise and the skeleton in ten minutes: too much for a newcomer.
   - Not recommended: pretending `00` and `01` are the same.
2. **Techniques stays one film.** It looks like a grab-bag, but its single idea is "the same shader can behave four ways because of render states", and Godot has no techniques (it uses a compile-time switch), which is itself the film. Splitting it into blend modes and alpha test would give two thin films. Folding it into another film loses its prerequisite (the rim as alpha comes from the Fresnel film). It stays where Bear put it.
3. **Diffuse maps and spec maps stay separate.** The first carries the color-space, repeat and uv lessons; the second carries "data textures are not colors" and the quiet change to the rim. Merged they would run past 15 minutes.
4. **Normal maps is the heaviest film (about 11 minutes, hard cut line).** It carries tangent, binormal, normal, the green-channel convention and the wrong-hint trap. The full treatment of the OpenGL-versus-DirectX choice is deferred to the uber film, so the normal-map film can stay with one convention.
5. **Blend maps is short (about 8 minutes).** Do not pad it. If Bear wants fewer films, it can become the last act of the Spec Maps film ("one texture, several masks"), at the price of moving Bear's order; I do not recommend it.
6. **The car paint film is a small step from cube maps** (offset, intensity, contrast, a second highlight). Keep it short rather than merge it, because the idea ("tune the reflection until it reads as paint") is new.
7. **Two films not in Bear's list that would help, optional:** a short film on reading a normal as a color (`ALBEDO = normal * 0.5 + 0.5`, the debugging view every shader writer uses) and one on moving the same math into Godot's own `light()` function. Neither is planned here; Bear's list stays as is.

## Overlap with the existing Godot shader series (`youtube/_godot-shaders-series/`)

That series (twenty films, all laid out) is mostly 2D fragment work. Where this series touches it: *Shaders in 3D* (a lit sphere, unshaded versus lit, the two renderers), *Vertex Shaders* (a 2D flag), *UV Space* (2D scaling and repeating), *Reflections* (screen-based reflections, not cube maps), *Light Shaders* (2D lights), *Local, World and Screen Space*, *Textures and Color* (sRGB, `source_color`). Rule for these films: none depends on another; where an idea is needed (world space, a uniform, `source_color`), the film says it in one or two sentences or in its terms card. Decision 5.

---

## The fifteen films

Common to every film: Forward+ is the renderer shown unless the film is about a difference; **Compatibility is shown whenever it reads differently** (it does for every lit shader: see the Lambert film). Every number on screen is one of the measured values below, with its renderer; scripted input is labeled; each film opens with the hesitant-writer correction and a terms card of three to six prerequisites; each ends with a recap, a "your turn" prompt that makes the viewer use the idea on their own shader, and the standard spoken outro. All measured values are from `shader_lessons_godot/evidence/logs/` (Forward+ unless marked).

### The Smallest Shader
- **Shader.** `00_super_simple` (flat color) and `01_base` (the reveal).
- **The one idea.** A shader is two small programs. One runs for each corner (`vertex()`), one for each pixel (`fragment()`); the GPU fills in between. Everything else, a color, a normal, a light direction, is data you hand them.
- **The wrong assumption it opens on.** "A shader is one program that paints the whole object." Correction: two programs, at two different rates.
- **Terms.** vertex, pixel (fragment), uniform, matrix, GPU.
- **Real numbers.** A flat teal (sRGB 0.37, 0.64, 0.57) reads the same, (94, 163, 145), at five named places on the sphere and over 21,634 sampled pixels: a flat color has no sphere in it. Writing the matrix line by hand, `PROJECTION_MATRIX * VIEW_MATRIX * MODEL_MATRIX * vec4(VERTEX, 1.0)`, draws exactly what Godot draws for you: 0 of 921,600 pixels differ, on a turned, stretched sphere. Then `01_base`: at the point facing the camera the sphere reads 173 (N.L = 0.42), the lit pole 255, the terminator 5.
- **Demo it ends on.** The teal disc, then the same shader with three added lines (a normal, a light direction, one dot) and the disc becomes a sphere. It stops at "it works" and promises the why.
- **Godot versus Cg worth a beat.** The matrix line is `M * v` in Godot as in Cg's `mul(M, v)` (the order carries over); the Cg technique/pass block and the shader profile names have no Godot equivalent; colors are `source_color`.
- **Cut line.** The hand-written matrix line (keep the sentence, drop the pixel-diff proof); then the second uniform beat.

### Lambert: Light Is a Dot Product
- **Shader.** `02_lambert` (identical code to `01_base`).
- **The one idea.** Brightness is the dot product of two unit vectors: the surface normal and the direction to the light, floored at zero. Distance does not matter here.
- **The wrong assumption.** "The nearer the lamp, the brighter" (or "light is a color you add"). Correction: it is an angle.
- **Terms.** normal, unit vector, dot product, world space, uniform.
- **Real numbers.** N.L = 1.00: 255; 0.70: 218; 0.42: 173; 0.00: 5; -0.50: 0. In Compatibility the same pixels read 255, 179, 107, 0, 0, the numbers the Cg wrote (0.42 x 255 = 107). The Cg's own default light, (0, 1, 0), travels upward: a point on the underside (normal y = -0.8) reads 232 and a point on top reads 0. Two shaders that the original ships as separate files render identically (0 differing pixels): the film can say that a shader and its "next step" are sometimes the same.
- **Demo it ends on.** The sphere with the light direction as a dial; first predict where the lit side goes for (0, 1, 0), then see the underside lit.
- **Godot versus Cg worth a beat.** (1) `saturate` does not exist: the compiler says "No matching function found for: 'saturate'"; `clamp(x, 0.0, 1.0)`. (2) `mul(WorldInverseTranspose, normal)` is `MODEL_NORMAL_MATRIX * NORMAL`, and `NORMAL` means object space in `vertex()` but view space in `fragment()` (measured: (0.01, 1.00, 0.01) against (0.01, 0.00, 1.00) on a sphere turned 90 degrees). (3) **The same number, two pixels**: 173 in Forward+ and 107 in Compatibility, because Forward+ treats the result as linear light and encodes it. This is the beat Bear will want; it is the most important Godot-versus-Cg difference in the series.
- **Cut line.** The default-light prediction; then the world-space beat.

### Ambient: The Floor Under the Light
- **Shader.** `03_lambert_ambient`.
- **The one idea.** Real surfaces are lit by light that bounced; the cheap stand-in is a constant color added before multiplying by the surface color. It is a floor, not a lamp.
- **The wrong assumption.** "With the lamp pointing away, the dark side should be black." Correction: it is only black when nothing else exists.
- **Terms.** ambient, clamp, linear light, sRGB.
- **Real numbers.** Ambient typed 0.15: deep shadow (N.L = -0.75) reads 38 in Forward+ (0.15 x 255 = 38.25) and 36 in Compatibility; terminator 40 and 37; the sphere facing the camera 177 and 145 (against 173 and 107 for Lambert alone). The sum is not clamped: the lit pole of a white surface is 1.15 before the screen clips it to 255.
- **Demo it ends on.** The Lambert sphere with a dial for the floor, dark side gaining shape.
- **Godot versus Cg worth a beat.** What `source_color` does to a typed 0.15 (the shader sees 0.0196 in Forward+ and 0.149 in Compatibility), and that setting a `Color` or a `Vector3` from code behaves differently in Forward+ (a `Color` is converted, a `Vector3` is not, even on a uniform with no hint).
- **Cut line.** The clip beat; then the order-of-operations beat ((lambert + ambient) x color against adding after).

### Fresnel: Light at the Edge
- **Shader.** `04_fresnel`.
- **The one idea.** The more a surface turns away from the viewer, the more it reflects: a rim weight `pow(1 - N.E, power)`, multiplied by the lighting so the rim fades in shadow.
- **The wrong assumption.** "The edges of a sphere are darker because they are further away." Correction: at a glancing angle surfaces reflect more.
- **Terms.** eye vector (surface to camera), power, silhouette.
- **Real numbers.** Rim weight at N.E = 1.0, 0.5, 0.2, 0.0: 0, 0.125, 0.512, 1. A lit rim (N.L = 0.5, N.E = 0.25) reads 223 at power 3 and 205 at power 6. On the dark side (N.L = -0.3, N.E = 0.25) the rim reads 47: nearly nothing, because the rim is multiplied by the lighting.
- **Demo it ends on.** The lit sphere with a thin rim and a power dial.
- **Godot versus Cg worth a beat.** The camera position. The literal port of `ViewInverse[0].w, [1].w, [2].w` reads three zeros (measured length 0.000 against 5.5): Cg indexes rows, Godot indexes columns. `INV_VIEW_MATRIX[3].xyz` is right and equals `CAMERA_POSITION_WORLD` (difference 0.0000). It also compiles silently, which is why the film shows it.
- **Cut line.** The power-6 comparison; then the dark-side beat.

### Phong: The Highlight
- **Shader.** `05_phong`.
- **The one idea.** A highlight is a mirror reflection of the lamp: reflect the surface-to-eye vector about the normal, flip it, compare with the light direction, raise to a power. It depends on where the viewer is.
- **The wrong assumption.** "The highlight is a white spot painted where the light hits." Correction: move the camera and it moves.
- **Terms.** reflect, half vector, specular, power.
- **Real numbers.** The brightest pixel of a specular-only render is (229, 244); the half-vector prediction is (230, 245). Half-height width along that row: 60 px at power 30, 33 px at power 100, exactly as `pow(R.L, power)` predicts.
- **Demo it ends on.** Everything lighting-wise, no textures: Lambert, ambient, rim, highlight, with power dials.
- **Godot versus Cg worth a beat.** `reflect(I, N)` is the same function in both; the Cg passes the surface-to-eye vector and negates the result (`-reflect(e, n)`, the standard mirror direction `2 (N.E) N - E`). Godot would also do this in its own `light()` function; this film does it by hand on purpose.
- **Cut line.** The power-100 comparison; then the half-vector aside.

### Diffuse Maps: Paint, Then Light
- **Shader.** `06_diffuse_mapped`.
- **The one idea.** A texture is a color lookup that multiplies the surface color before the lighting; the rim and the highlight are added after, so they are not tinted by it.
- **The wrong assumption.** "A texture replaces the lighting." Correction: it is one more factor in it.
- **Terms.** UV, texel, sampler, sRGB.
- **Real numbers.** Texel centers through the lighting: the red marker cell reads (147, 40, 33) at N.L = 0.46; a sand cell (193, 171, 121) at N.L = 0.67; a steel cell in shadow (5, 11, 19). A sampler with `source_color` converts an sRGB texel (226, 200, 140) to (0.761, 0.580, 0.263) in Forward+ and reads it raw (0.886, 0.784, 0.549) in Compatibility.
- **Demo it ends on.** A lit checker sphere with four marker cells that show which way U and V run.
- **Godot versus Cg worth a beat.** Colors need `source_color` on the sampler or the lighting runs on the wrong numbers; a sampler with no repeat hint wraps (measured), `repeat_enable` states the intent; UV origin differs from Maya's (Godot's importers flip V); the Cg's own metadata calls the texture a cube.
- **Cut line.** The repeat beat; then the UV-direction markers.

### Spec Maps: Where It Shines
- **Shader.** `07_spec_mapped`.
- **The one idea.** A texture can be a mask: its channels say, per pixel, how much rim and how much highlight are allowed. A mask is a set of numbers, not a color, so it is read without color conversion.
- **The wrong assumption.** "Shininess is one number for the whole object." Correction: it varies by pixel.
- **Terms.** mask, channel, data texture.
- **Real numbers.** The highlight peak lands on a matte cell (mask 0) and reads (68, 104, 140): no highlight. Just below, on a shiny cell (mask 1), the same highlight reads (255, 208, 244). A mask hinted as a color would turn a 0.5 mask into about 0.21 (computed from the sRGB curve; the conversion itself was measured on a texel, so the layout should re-measure before quoting it). **Finding:** this shader's rim no longer has the lighting factor that Fresnel and Phong had; a dark-side point (N.L = -0.4, N.E about 0.2) still glows at 188.
- **Demo it ends on.** The highlight cut off along a mask boundary.
- **Godot versus Cg worth a beat.** `source_color` on colors, none on masks; sampling the red channel for the rim and the green for the highlight.
- **Cut line.** The unhinted-mask warning; then the rim-factor aside (only if the film runs long: it is a real finding).

### Normal Maps: Lying About the Surface
- **Shader.** `08_normal_mapped`.
- **The one idea.** A normal map does not change the shape. It changes only the normal that the lighting uses, so a smooth sphere can look bumpy while its silhouette stays round.
- **The wrong assumption.** "A normal map bends the geometry." Correction: look at the edge.
- **Terms.** tangent, binormal, tangent space, normal map.
- **Real numbers.** A dome in the map: at the right side the normal leans +0.66 along the tangent, at the left -0.68; at the upper side +0.68 along the binormal, lower -0.66. The same dome's upper side reads (193, 83, 77) with an OpenGL-style map and (29, 3, 3) with a DirectX-style one: the same shader, green flipped. A normal map hinted as a color is wrong by 77 percent in Forward+ (decoded x 0.129 against 0.553).
- **Demo it ends on.** A sphere covered in domes that are only lighting; flip the green channel and the domes become dents.
- **Godot versus Cg worth a beat.** `TANGENT` and `BINORMAL` exist and are the right way round on Godot's meshes (959 of 959 sphere vertices tested); no `source_color` on a normal map; the green-channel convention (the next film that uses a normal map flips it).
- **Cut line.** The tangent-versus-model-matrix aside; then the hint trap.

### Cube Maps: Reflecting a World
- **Shader.** `09_cube_mapped`.
- **The one idea.** A reflection is not a rendered mirror. It is a lookup in a picture of the surroundings, in the direction of the mirror ray.
- **The wrong assumption.** "The sphere reflects the scene around it." Correction: it reflects a stored picture; move an object and the reflection does not follow.
- **Terms.** cube map, reflection vector, face.
- **Real numbers.** At a point near the silhouette (N.E about 0.11) the reflection vector is (0.03, 0.30, -0.95); the cube-map texel there is (53, 92, 179) in linear light; the pixel reads (162, 169, 183). **Finding, the surprise:** the pixel that faces the camera reads exactly what a shader with no reflection at all reads (177, 177, 177), because the reflection is multiplied by the rim weight (0, 0.125, 0.512, 1 at N.E 1, 0.5, 0.2, 0). Supplying the picture: `Cubemap.create_from_images` with faces in the order +X, -X, +Y, -Y, +Z, -Z matched a direct lookup in all 14 directions tested, in both renderers.
- **Demo it ends on.** A sphere reflecting a blue sky, a checker floor and four colored wall markers; the viewer sees it reflect only toward the edge, then the film says why.
- **Godot versus Cg worth a beat.** `samplerCUBE`/`texCUBE` become `samplerCube`/`texture`; Godot needs a Cubemap resource; a `source_color` cube is decoded in Forward+ and raw in Compatibility.
- **Cut line.** The six-faces-in-a-cross beat; then the hint beat.

### Vertex Animation: Moving the Corners
- **Shader.** `10_vertex_anim` (`10_vertex_anim.gdshader`).
- **The one idea.** Before the matrices, push every vertex along a vector by `sin(time * speed + x * frequency)`. You can only move corners that exist.
- **The wrong assumption.** "The pixel shader makes it wobble." Correction: `vertex()` moves the corners; the GPU fills in between.
- **Terms.** vertex, object space, TIME.
- **Real numbers.** With `vert_offset = (0, 0.3, 0)`, the top edge of the sphere moves from y = 112 to y = 54 on screen at TIME 1.444, and the whole silhouette matches the formula evaluated on every vertex within 1.0 px; sideways offset 0.4 at TIME 2.891, within 1.4 px. Offset (0, 0, 0), the original's default, is pixel-identical to the Phong shader. **Finding:** the normal is not recomputed and the camera vector uses the undeformed position, so the shading stays that of the round sphere while the shape moves.
- **Demo it ends on.** A wobbling sphere whose lit side does not follow the new shape.
- **Godot versus Cg worth a beat.** Write `VERTEX`, not the clip-space position; Godot's TIME is one global clock and, in Forward+ here, started at 0.14 to 0.17 s on every run, so a film should never quote an absolute TIME.
- **Cut line.** The sideways-offset second run; then the dead-alpha aside.

### UV Manipulation: Sliding the Picture
- **Shader.** `11_uv_manip`.
- **The one idea.** Move the address, not the surface: `uv = ((UV - 0.5) * scale + translate + time * speed) + 0.5`. Scale is about the center, and a bigger scale means more copies, not a closer look.
- **The wrong assumption.** "Scale 2 zooms in." Correction: it tiles.
- **Terms.** UV, wrap, tile.
- **Real numbers.** Scale 1, translate 0, speed 0, the original's defaults, render exactly like the normal-mapped shader (0 differing pixels). Scale 2 with translate (0.25, 0.125) and a scroll of (0.1, 0.05) per second both match the formula on a full image (99.1 and 99.9 percent within 3 bytes, Forward+; cell centers chosen after the transform so the check is about the formula).
- **Demo it ends on.** A scrolling, tiled, normal-mapped sphere.
- **Godot versus Cg worth a beat.** Wrap addressing: a sampler with no repeat hint wraps in 4.7.2 here, `repeat_disable` clamped in Forward+ and not in Compatibility, so say `repeat_enable` when you mean it.
- **Cut line.** The translate-only run; then the center-pivot derivation.

### Techniques: One Shader, Four Behaviors
- **Shader.** `12_techniques`.
- **The one idea.** The same pixel math can be drawn four ways depending on render state: opaque, alpha-blended, alpha-tested, additive. In Godot a state is a `render_mode`, fixed when the shader compiles.
- **The wrong assumption.** "Transparency is a property of the picture." Correction: it is a state plus an alpha value, and here the alpha is the rim.
- **Terms.** alpha, blend mode, render state, culling.
- **Real numbers.** At rim alpha 0.079 over the stage color (217, 213, 202): blended reads (211, 208, 199) in Forward+ and (208, 208, 201) in Compatibility (Forward+ blends in linear light); alpha-tested shows the stage color (alpha below 0.3) and at alpha 1.0 the full color; additive reads (219, 216, 207). A `#define TECHNIQUE` selects the render mode, and all four compile and render.
- **Demo it ends on.** Four spheres side by side.
- **Godot versus Cg worth a beat.** There are no techniques: a `#define` and `#if` choose the `render_mode`; `next_pass` is Godot's answer to a multi-pass technique, but none of these has a second pass. The Cg's blended technique relies on a host default blend function; the film reads it as the usual blend and says that is a reading.
- **Cut line.** The culling beat; then the alpha-test threshold detail.

### Blend Maps: One Texture, Three Colors
- **Shader.** `13_blended`.
- **The one idea.** A channel of a texture can be a selector: red picks the first color, blue the second, green the third, and the result is lit like any other color.
- **The wrong assumption.** "Three colors need three textures or three meshes." Correction: one texture with three channels.
- **Terms.** channel, weight.
- **Real numbers.** Red band (158, 0, 0); blue band (30, 30, 218); a green disc (32, 127, 32); with the three colors swapped to yellow, cyan and magenta the bands show yellow (158, 158, 0) and cyan (30, 218, 218). The channel order is red, blue, green: not RGB order.
- **Demo it ends on.** A sphere in three paints, with the swap.
- **Godot versus Cg worth a beat.** A blend map is data: no `source_color`.
- **Cut line.** The swap run is the proof and stays; the discs go first.

### The Car Paint Shader: Tuning the Reflection
- **Shader.** `14_car_shader`.
- **The one idea.** Take the cube-map shader and give the reflection controls: an offset, an intensity, a contrast (a power on the reflected color), and a second highlight. Paint is not chrome.
- **The wrong assumption.** "Shiny paint reflects everything." Correction: tune how much and where.
- **Terms.** offset, intensity, contrast.
- **Real numbers.** Red paint, the pixel facing the camera reads (96, 13, 13) with no offset and (145, 96, 13) with `fresnel_offset` 0.5: the reflection now shows there. At 10 degrees off the highlight peak only the wide (power 8) highlight reaches: (212, 212, 212).
- **Demo it ends on.** A red paint sphere with a sky in it, offset dial.
- **Godot versus Cg worth a beat.** `pow(vec3, float)` does not compile in Godot (the message says `pow(vec3,float)` is an invalid argument list); widen the exponent with `vec3(reflection_contrast)`.
- **Cut line.** The second-highlight comparison; then the contrast dial.

### The Uber Shader: Everything at Once
- **Shader.** `15_uber`.
- **The one idea.** The earlier shaders were ingredients; this is the recipe. A hemisphere ambient replaces the flat floor, a fake subsurface softens the terminator, the spec map is re-packed (red for the highlight, blue for the reflection), and the normal map's green channel is flipped.
- **The wrong assumption.** "A final shader is a new technique." Correction: it is the earlier ones, recombined; name each line.
- **Terms.** hemisphere, subsurface, channel packing.
- **Real numbers.** With the DirectX-style map and the green flip the sphere is the same picture as with the OpenGL-style map and no flip (51 of 230,400 sampled pixels differ, all on cube-map edges). Subsurface spread 0.5: terminator (179, 171, 146), dark side (155, 140, 113). Subsurface color (0.1, 0, 0) is added inside the clamp, so the red appears only between N.L = -0.1 and 0. Anything whose normal faces down gets the bottom ambient color (default black).
- **Demo it ends on.** The finished shader on the textured sphere, each line labeled with the idea that taught it, by title, never by number.
- **Godot versus Cg worth a beat.** The green-channel convention settled once: Godot's BINORMAL points up the image, so a green-up map works as is and a green-down map needs the flip.
- **Cut line.** The subsurface spread run; then the hemisphere comparison.

---

## What the layouts will need (build facts, not decisions)

- **A 3D capture scene.** The series Lab renders flat quads, rectangles and sprites; it has no camera or mesh mode. `shader_lessons_godot/scripts/rig.gd` and `tools/harness.gd` are the camera, sphere and torus rig and the fixed-step clock; they need wrapping as a scene script for `lab/capture.gd` (the series' `--scene` route, `--native` for the shaders that read window pixels, which none of these do) and a `ShaderLab` layout that shows code beside a sphere.
- **Pronunciation.** `brutalist.art/runtime/pronunciation/liam.json` has no entry for Lambert, Fresnel, Phong, binormal, subsurface or uber: each needs a voice-only respelling and a phoneme check. (Not edited here.)
- **Honesty rules carried over.** Show only what was run and recorded; a pixel value always comes with its renderer; the harness draws at fixed steps and says nothing about real-time speed; the converted code and numbers belong to the project folder's evidence.
- **Glossary.** Reuse `_godot-shaders-series/GLOSSARY.md` wording for terms already defined there; new terms to add (do not edit the shared file): normal map, tangent, binormal, cube map, reflection vector, Fresnel, Phong, hemisphere ambient, subsurface, channel packing.

---

## Decisions for Bear

1. **The first two films** (A or B above). My recommendation is A: the skeleton and a reveal, then a separate Lambert film that explains. This is the only decision that changes the count (fifteen films under A, fourteen under B).
2. **Playlist name.** Not decided. The existing practice is to never type a playlist name in a layout (`series_config.bopen(TITLE, SUMMARY)`), so no card names one. A working label for the folder is "Shader Techniques"; Bear names the real one.
3. **Credit to the DVD's authors, and the rights.** The headers name "Eat 3D - Shader Production DVD" and "Luiz". Rights are not confirmed by Bear and no licence was found. The films show converted code on screen, which is a derivative of third-party code. Options: (a) Bear confirms or obtains permission and the films credit "Eat 3D, Shader Production DVD, Luiz" in the description and in one spoken line; (b) the films teach the same techniques from scratch (Lambert, Fresnel and Phong are standard public ideas; the arithmetic is three or four lines) with newly written shaders and no credit claim beyond "classic lighting models"; (c) wait. Nothing should be published until this is answered.
4. **`shader_lessons/` and `shader_lessons_godot/`.** Both are untracked in the course repo, which goes to a public GitHub repo. Recommended `.gitignore` lines (not applied): `shader_lessons/` and `shader_lessons_godot/`, until the rights decision is made. Bear applies the change.
5. **Overlap with the existing shader series.** Keep every film standalone with a two-sentence retell where the earlier series overlaps (recommended), or tighten this series to avoid retelling the ideas that *Shaders in 3D*, *Vertex Shaders* and *UV Space* already cover.
6. **Renderer policy.** Forward+ is the main picture; Compatibility is shown whenever a pixel reads differently, which is every lit shader. The Lambert film carries the explanation of why (Forward+ encodes linear light, Compatibility passes the numbers through, as the Cg did). Confirm, or choose to show only one.
7. **Optional extra films** (reading a normal as a color; Godot's own `light()`): add, or leave out.
8. **Pilot and build order.** Recommended: settle decision 1, then pilot `The Smallest Shader` (it creates the stage, capture rig and look every later film reuses), then `Lambert` (it carries the two-renderer surprise), then in order.

## Next step

Lay out the films one at a time, the pilot first, under the series rules (`_godot-shaders-series/BUILDER-BRIEF-COMMON.md`): Cowork does the layout (narration, lanes, shot list, fact check, capture plan, `BUILD-PROMPT.md`); a Claude Code session builds. Do not start the audio or the render before Bear answers decision 1. A layout should copy its numbers from the lines of `shader_lessons_godot/evidence/logs/` named in `CONVERSION-NOTES.md`, and re-run the check if it changes a shader.

## Files (absolute paths)

- This plan: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-techniques-series/SERIES-PLAN.md`
- Project: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/shader_lessons_godot/`
- Conversion notes: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/shader_lessons_godot/CONVERSION-NOTES.md`
- Sources and provenance: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/shader_lessons_godot/SOURCES.md`
- Evidence index: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/shader_lessons_godot/evidence/INDEX.md`
- The sixteen shaders: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/shader_lessons_godot/shaders/`
- The originals (untouched by this work): were `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/shader_lessons/`; at the end of the session the folder had been moved to the macOS Trash by something other than this work (`/Users/bear/.Trash/shader_lessons`, all 16 files intact; see `shader_lessons_godot/SOURCES.md`)
- Series rules and Lab: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/BUILDER-BRIEF-COMMON.md`, `.../lab/`
