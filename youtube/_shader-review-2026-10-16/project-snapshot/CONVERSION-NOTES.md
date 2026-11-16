# Conversion notes: sixteen CgFX lessons, hand-converted to Godot 4.7.2

**What this is.** How each of the 16 CgFX lessons in `../shader_lessons/` became one Godot 4.7.2 shader in `shaders/`, what changed on the way, every trap met by running it, and how each shader was checked. Written 2026-10-16. Paths in this file are relative to this project folder.
**Why.** The converted shaders are the demos for a series of Godot lecture films that teach these techniques in order (plan: `../youtube/_shader-techniques-series/SERIES-PLAN.md`). A film may only show a number that was measured, so every shader was run in a real Godot window and compared with a CPU re-implementation of the original Cg arithmetic.
**Found.** All 16 compile in Forward+ and Compatibility (Lab `check_shader.sh`), all 16 render, and 134 numeric checks per renderer pass (0 failures in either; the textured lessons' full-image checks sit at 98.5 to 99.9 percent, explained below). Things the originals do not say, found by running: `01_base` and `02_lambert` are the same shader; the Cg default light lights the underside; `09_cube_mapped` shows no reflection on any surface that faces the camera; `07` quietly drops a factor that `04` to `06` have; `08` and `15` disagree about the normal-map green channel; `13`'s channels do not follow RGB order; and Forward+ and Compatibility give different pixels for the same converted shader because only Compatibility does its arithmetic the way the Cg did (in display values). Nothing was staged, committed or published.

Rights: the sources are third-party teaching material (Eat 3D, "Shader Production DVD", author credit "Luiz"); rights are not confirmed by Bear. See `SOURCES.md`.

---

## 1. Results at a glance

"Compile" is the series Lab's `youtube/_godot-shaders-series/lab/check_shader.sh` (`--kind quad3d`), exit 0 and no `SHADER ERROR`, in both renderers (`evidence/compile/check_shader-*.txt`; a deliberately broken shader fails as it should, `evidence/compile/negative-control.txt`). "Rendered" is a real windowed frame of the test rig, saved in `evidence/renders/`. "Numeric" is checks passed / failed, Forward+ then Compatibility (`evidence/logs/verify-*.txt`).

| CgFX file | Godot shader | Compile F+ / Compat | Rendered | Numeric (F+ / Compat) | Main findings |
|---|---|---|---|---|---|
| `00_superSimple.cgfx` | `shaders/00_super_simple.gdshader` | ok / ok | yes | 6/0 and 6/0 | the "decoder ring" matrix line written by hand renders identically to Godot's own (0 of 921,600 pixels differ) |
| `01_base.cgfx` | `shaders/01_base.gdshader` | ok / ok | yes | 6/0 and 6/0 | F1: it is Lambert, identical to 02 |
| `02_lambert.cgfx` | `shaders/02_lambert.gdshader` | ok / ok | yes | 9/0 and 9/0 | F1 (0 differing pixels vs 01), F2 (Cg default light lights the underside) |
| `03_lambert_ambient.cgfx` | `shaders/03_lambert_ambient.gdshader` | ok / ok | yes | 6/0 and 6/0 | F3 colour space (floor reads 38 in F+, 36 in Compat for typed 0.15); the sum is not clamped (1.15 at the pole) |
| `04_fresnel.cgfx` | `shaders/04_fresnel.gdshader` | ok / ok | yes | 10/0 and 10/0 | rim weights 0, 0.125, 0.512, 1 at N.E 1, 0.5, 0.2, 0; two uniforms of the Cg were never read |
| `05_phong.cgfx` | `shaders/05_phong.gdshader` | ok / ok | yes | 10/0 and 10/0 | highlight peak within 1 px of the half-vector prediction; 60 px wide at power 30, 33 px at power 100, as predicted |
| `06_diffuse_mapped.cgfx` | `shaders/06_diffuse_mapped.gdshader` | ok / ok | yes | 8/0 and 8/0 | the colour texture is labelled "Cube" in the Cg metadata though read as 2D; sRGB decode differs by renderer |
| `07_spec_mapped.cgfx` | `shaders/07_spec_mapped.gdshader` | ok / ok | yes | 8/0 and 8/0 | F8: rim lost its lighting factor between 06 and 07 |
| `08_normal_mapped.cgfx` | `shaders/08_normal_mapped.gdshader` | ok / ok | yes | 7/0 and 7/0 | normal leans along +tangent / +binormal exactly as the map says (+0.66, +0.68); a DirectX-style map lights the wrong side (193 vs 29 in red) |
| `09_cube_mapped.cgfx` | `shaders/09_cube_mapped.gdshader` | ok / ok | yes | 9/0 and 9/0 | F10: no reflection where the surface faces the camera (pixel equals lesson 03 exactly) |
| `10_vertexAnim.cgfx` | `shaders/10_vertex_anim.gdshader` | ok / ok | yes | 3/0 and 3/0 | zero offset is pixel-identical to 05; displaced silhouette matches the CPU within 1.4 px |
| `11_uv_manip.cgfx` | `shaders/11_uv_manip.gdshader` | ok / ok | yes | 7/0 and 7/0 | identity transform is pixel-identical to 08; scale 2 gives MORE tiles, not a zoom |
| `12_techniques.cgfx` | `shaders/12_techniques.gdshader` | ok / ok | yes (4 techniques) | 12/0 and 12/0 | no techniques in Godot: a `#define` picks the render mode; blending is linear in Forward+ |
| `13_blended.cgfx` | `shaders/13_blended.gdshader` | ok / ok | yes | 8/0 and 8/0 | blend map: R picks shader_color, B picks blended_color, G picks third_color |
| `14_carShader.cgfx` | `shaders/14_car_shader.gdshader` | ok / ok | yes | 11/0 and 11/0 | `pow(vec3, float)` does not compile in Godot; fresnel_offset 0.5 lights the reflection on a surface facing the camera |
| `15_uber.cgfx` | `shaders/15_uber.gdshader` | ok / ok | yes | 14/0 and 14/0 | F16: spec map channels re-packed; green flipped; DirectX map plus flip equals OpenGL map without it (51 of 230,400 sampled pixels differ, all on cube-map edges) |

Renderer, always: Godot 4.7.2.stable.official on an Apple M4 Pro, windowed. Forward+ runs on Metal; Compatibility is Godot's OpenGL renderer. Pixel values below are screen bytes (0 to 255) unless a value is marked "linear".

---

## 2. How each shader was checked

- **Test rig** (`scripts/rig.gd`): camera at (0, 0, 5.5) looking down -Z, vertical field of view 30 degrees, window 1280 by 720; a sphere (radius 1, 128 by 64 segments) at (-1.3, 0, 0) and a torus at (1.3, 0, 0) turned 60 degrees about X; stage colour `#D9D5CA`. Y is up, -Z is forward: the same as Maya, so no axis flip was needed. The sphere is about 245 px in radius on screen. The light is `light_direction = (0.5, -0.8, -0.6)`, the direction the light travels.
- **Reference** (`tools/verify.gd`, `shade()`): the Cg arithmetic of each lesson written from the `.cgfx` text, not from the GLSL. For a chosen pixel it finds the exact ray/sphere hit at the pixel centre (true normal, true direction to the camera), evaluates the formula (with bilinear texture and cube-map reads from the same PNG files), and passes the result through the **measured** transfer curve of that renderer (see 4, T6) to get the expected screen value.
- **Named points** (2 to 7 per lesson): lit pole, facing the camera, terminator, dark side, rim, highlight peak, texel and cell centres, dome sides; each prints expected and got. Tolerance: 3 screen bytes (observed worst case at named points: 3, almost always 0 or 1).
- **Full image**: every third pixel in x and y of the sphere against the reference. Non-textured lessons: at least 99 percent within 3 bytes (observed 99.9 to 100). Textured lessons skip the polar cap (|y| > 0.75, where the analytic uv and the mesh's interpolated uv disagree) and a 2-texel band along checker-cell edges, and must reach 98 percent (observed 98.5 to 100; the outliers are sharp edges of the cube map and of the specular masks, where a rounding-sized change in the normal moves a lookup across an edge). Test textures carry no mip chain in these runs so the reference needs only level 0; one informational run with mips on (`evidence/logs/info-mips-forward_plus-L08.txt`) gave 99.92 percent.
- **TIME** is read inside the same frame from a probe quad (`tools/verify.gd`), because Godot's TIME in these runs starts at a different small value each time in Forward+ (see T10).
- **What these checks prove, and what they do not.** They prove the Godot shader computes what the Cg formula says, in the way Godot draws it. They do not prove how the Cg behaved inside Maya: there is no Maya or CgFX runtime here, so host behaviour (what the `Direction` semantic supplies, the units of `Time`, the default blend function of `AlphaBlendEnable`) is inference from the code and is marked as such.

---

## 3. Every place the conversion departed from the original, and why

1. **Names**: lowerCamelCase to snake_case (`shaderColor` to `shader_color`); file names `NN_name.gdshader` keep the original numbers for traceability only. `10_vertexAnim` is `10_vertex_anim.gdshader`.
2. **Colour semantic `: Diffuse` to `: source_color`** (a colour picker, and the engine converts sRGB numbers to linear light in Forward+; see T7, T8).
3. **Maya bookkeeping dropped**: `string description`, `UIWidget`, `UIName`, `UIMin/UIMax/UIStep` (sliders become `hint_range(min, max, step)`), the unused `World` and `ViewInverse` matrices in 01 to 03, the unused `specularPower`/`specularColor` in 04.
4. **Matrices**: Cg `mul(M, v)` is Godot `M * v`. Cg `WorldInverseTranspose` is `MODEL_NORMAL_MATRIX`; `World` is `MODEL_MATRIX`; `WorldViewProjection` is `PROJECTION_MATRIX * VIEW_MATRIX * MODEL_MATRIX` (written out by hand only in 00; Godot does it when POSITION is not written). `ViewInverse[0].w, [1].w, [2].w` is `INV_VIEW_MATRIX[3].xyz` (Cg indexes rows, Godot indexes columns; T1).
5. **`saturate`, `lerp`, `frac`, `float3`, `tex2D`, `texCUBE`, `mul`** do not exist in Godot: `clamp(x, 0.0, 1.0)`, `mix`, `fract`, `vec3`, `texture`, `*` (T14).
6. **Colour space**: the Cg did everything in display values; Godot Forward+ does lighting in linear light and encodes at the end (F3). The conversion takes the Godot-correct route (`source_color` on colours and colour textures, no hint on masks and normal maps) and keeps the Cg's arithmetic untouched. It does not try to reproduce the Cg's display-space look in Forward+. Compatibility, by Godot's design, does arithmetic in display values and so shows the Cg's numbers.
7. **Default light**: the Cg default `lightDirection = (0, 1, 0)` (travels upward, lights only the underside) became `(0.5, -0.8, -0.6)` (from the upper left in front). Same meaning (the direction the light travels, world space, negated in the shader). The Cg default was verified by running it on the converted 02 (F2).
8. **Light space**: the Cg float3 is taken to be a world-space direction (every other vector in the shaders is world space: normal through `WorldInverseTranspose`, camera and surface through `World`/`ViewInverse`). Not verifiable without Maya.
9. **Wrap addressing** `AddressU/V = Wrap` is `repeat_enable` (stated explicitly even though a sampler with no hint wraps in 4.7.2 on this Mac; T11).
10. **Cube map**: `samplerCUBE` to `samplerCube`; the original's `default_cube.dds` was not available, so six code-authored PNG faces are assembled into a `Cubemap` at run time (`scripts/lessons.gd`).
11. **`outColor.a = fresnel`** in 10, 13 (Opaque techniques): dropped, alpha was never used. In 12 it is the heart of three techniques and is kept (`ALPHA = fresnel.x`; the float3-to-float assignment keeps the first component).
12. **Vertex deformation** (10): the Cg writes a deformed clip-space position; Godot writes `VERTEX` (object space) and applies the matrices itself. Same space, same arithmetic (verified by silhouette).
13. **Techniques** (12): Godot has no techniques inside one shader. Nearest honest equivalent: a compile-time `#define TECHNIQUE` (0 to 3) that selects the `render_mode` and the alpha lines. Dropped: nothing; no technique in any file has more than one pass, so `next_pass` was not needed.
14. **12 AlphaBlend**: the Cg writes only `AlphaBlendEnable = True`. It is read as the usual blend (SrcAlpha, OneMinusSrcAlpha), Godot `blend_mix`. **That is an inference**; the original relies on a host default that is not in the file.
15. **12 AlphaTest**: `GREATER 0.3` became `ALPHA_SCISSOR_THRESHOLD = 0.3`, which discards below 0.3 (the two differ only at exactly 0.3).
16. **15 green channel**: the Cg's `* -binormal` is kept as `uniform bool flip_green = true` (default as written); the stage binds `textures/normal_dx.png` to this lesson so it looks right (F9).
17. **Textures** were not available (`default_color.dds` and friends are not in the folder). Everything is generated by `tools/make_textures.py`: code-authored, no outside art (`SOURCES.md`). Nothing about how the DVD's own textures looked is claimed.
18. **Unused outputs**: tangent and binormal in 06, 07 (computed and never read in the Cg): dropped.
19. **Not carried over**: the Cg's commented-out debug line in 15; everything in the technique/pass blocks that named the old shader profiles (`vp30`, `fp30`, `vp40`, `fp40`).

---

## 4. Traps met by running them (T1 to T19)

Each was measured by `tools/traps.gd` (log lines `TRAP-n` in `evidence/logs/traps-forward_plus.txt` and `traps-gl_compatibility.txt`) or by `tools/cg_isms.sh` (`evidence/compile/cg-isms.txt`). "F+" is Forward+, "Compat" is Compatibility.

| # | Trap | What happens | Measured |
|---|---|---|---|
| T1 | Cg indexes a matrix by ROW, Godot by COLUMN | the literal port of `ViewInverse[0].w, [1].w, [2].w` reads three zeros (the 4th row of three columns), so the camera would sit at the origin | length of the naive vector 0.000; camera is 5.5 away; `INV_VIEW_MATRIX[3].xyz` differs from `CAMERA_POSITION_WORLD` by 0.0000. It also compiles silently (`cg-isms.txt`, `mat_row_index`) |
| T2 | Operator order | `M * v` is Cg `mul(M, v)`; `v * M` multiplies by the transpose | `(MODEL * vec4(1,0,0,1)).x` = 0.329 (F+) / 0.298 (Compat), CPU 0.303 (readout resolution about 0.03); the reversed product would be 1.603 |
| T3 | Normal matrix | `MODEL_NORMAL_MATRIX` is the inverse transpose of the model matrix and is NOT normalised; plain `mat3(MODEL_MATRIX)` bends normals on non-uniform scale | difference to `transpose(inverse(mat3(MODEL_MATRIX)))` 0.0000; length 1.208 for scale (2, 0.5, 3) (CPU 1.206); the plain matrix turns the direction by 1.106 (CPU 1.100) |
| T4 | `NORMAL` means two things | in `vertex()` it is the mesh's object-space normal; in `fragment()` it is VIEW space | sphere turned 90 degrees about X, pixel facing the camera: fragment `NORMAL` (0.01, 0.00, 1.00), vertex `NORMAL` (0.01, 1.00, 0.01) |
| T5 | Writing `POSITION` by hand | identical to Godot's own | 0 differing pixels of 921,600 (rotated, non-uniformly scaled sphere), both renderers |
| T6 | ALBEDO to the screen | F+ encodes linear light with the sRGB curve; Compat writes the number as it is, with a slight dip in the darks | ALBEDO 0.5 reads 188 (F+) and 128 (Compat); 16/255 reads 71 (F+) and 11 (Compat); `OUTPUT_IS_SRGB` is false in F+, true in Compat |
| T7 | Colour numbers going in | F+: a `Color` set from code is converted to linear even for a uniform with NO `source_color` hint; a `Vector3` is never converted; a `source_color` default in the shader is converted; a plain default is not. Compat: nothing is converted | typed 0.15: shader sees 0.0196 (F+: default with hint, Color on a hinted vec3, Color on a plain vec3, Color on a vec4) and 0.149 (F+: Vector3 on a hinted vec3, plain default); Compat: 0.149 everywhere |
| T8 | `source_color` on a sampler | F+ decodes the texel to linear; Compat reads it raw | texel (226, 200, 140): F+ source_color sees (0.761, 0.580, 0.263), plain sees (0.890, 0.784, 0.549); Compat both (0.886, 0.784, 0.549) |
| T9 | `source_color` on a NORMAL MAP | in F+ it bends every normal | red byte 198: plain decodes to x 0.553, with the hint x 0.129 (77 percent off). Compat: no difference |
| T10 | TIME with the render loop off | advances exactly by the step given; F+ starts at a small non-zero value that changes per run | F+ starts 0.144 to 0.173 s then moves 0.500, 0.500, 1.000, 0.000, 0.250 exactly; Compat starts at 0.000 |
| T11 | Texture repeat | in 4.7.2 on this Mac a sampler with no repeat hint WRAPS; `repeat_disable` clamps in F+ but did not clamp in Compat in this test | uv.x 1.0625: no hint (0.81, 0.24, 0.20) wrapped; `repeat_disable` F+ (0.75, 0.24, 0.67) clamped, Compat (0.80, 0.24, 0.20) wrapped |
| T12 | Cube map orientation and supply | `Cubemap.create_from_images([+X, -X, +Y, -Y, +Z, -Z])` with faces written to the OpenGL cube-face table matches a CPU lookup exactly; a `source_color` cube decodes in F+ | 14 of 14 directions match in both renderers (axes, the sun, mirrored sun, floor/sky); +X texel raw 0.863: F+ hinted sees 0.718 (decoded 0.716), Compat 0.863 |
| T13 | Built-in meshes | `SphereMesh` and `TorusMesh` carry tangents; sphere tangent runs along +u; `BINORMAL = cross(NORMAL, TANGENT) * tangent.w` points up the image (toward the +Y pole) | 959 of 959 non-polar vertices for both; uv = (atan2(x, z) / 2pi, acos(y / r) / pi) exactly; tangent.w = 1.0 |
| T14 | Compile-time Cg habits | each fails with the compiler's own message | `saturate`, `lerp`, `frac`, `mul`, `tex2D`, `texCUBE`: "No matching function found"; `float3`, `float4x4`: "Unknown identifier"; `pow(vec3, float)`: "Invalid arguments for the built-in function"; `float a = vec3`: "Invalid assignment of 'vec3' to 'float'"; `1 - x` and `* 2 - 1`: "Invalid arguments to operator ... 'int, float'"; `{1.0, 0.0, 0.0}` and `: COLOR`: errors. Full text in `cg-isms.txt` |
| T15 | Preprocessor in a shader | `#define` and `#if` can select a `render_mode`; all four variants of 12 compile and render | `check_shader.sh` exit 0 for the file; four distinct frames in `evidence/renders/12_techniques_*` |
| T16 | Same shader, two renderers, two pictures | Lambert at the pixel facing the camera (N.L = 0.42): F+ 173, Compat 107 (= 0.42 x 255, the number the Cg wrote); terminator N.L = 0: F+ 5, Compat 0 | `verify-*-L0-3.txt` |
| T17 | Blending | F+ blends in linear light, Compat blends display values (like the Cg) | stage (217, 213, 202), rim alpha 0.079, drawn colour (104, 131, 164): F+ 211, 208, 199; Compat 208, 208, 201 (`verify-*-L12-15.txt`) |
| T18 | A renamed shader file fails silently | a wrong path gives an empty shader, a flat grey disc and one easily missed line `Parameter "shader" is null` | met in this build (lesson 10's file name); `tools/run_godot.sh` now reports any line starting `ERROR:` |
| T19 | The Lab renders a failing shader | known (series brief); the negative control proves the compile check can fail | `evidence/compile/negative-control.txt` |

---

## 5. Findings: where the originals do not do what their comments say, or do something their comments do not say

Verdicts are from rendered pixels unless marked **(code reading)**, which means derived from the `.cgfx` text with no run that could contradict it.

- **F1. `01_base` and `02_lambert` are the same shader.** A `diff` of the two `.cgfx` files shows only the header comment, the description string and one blank line moved. The 02 header says it "adds a light direction and passes the normals", but 01 already has both. Converted, the two render identically: 0 differing pixels over the whole frame in both renderers. **Bear's premise that "super simple and base are basically the same" is only half right: `00_superSimple` outputs one flat colour; `01_base` is already a complete Lambert shader.**
- **F2. The Cg default light lights the underside.** Default `lightDirection = (0, 1, 0)`; the shader uses `-lightDirection` as the vector toward the light, so the light travels upward. Run on the converted 02: a point on the underside (normal y = -0.8) reads 232 (F+) / 205 (Compat); a point on top (y = +0.8) reads 0.
- **F3. Colour space.** The Cg wrote N.L straight to the screen. Godot Forward+ treats ALBEDO as linear light and encodes it, so the same converted number is brighter: Lambert at N.L = 0.42 reads 173 (F+) and 107 (Compat, the Cg's own number); the terminator reads 5 (F+) and 0 (Compat); at N.L = 0.70, 218 and 179. The 03 ambient floor for typed 0.15 reads 38 (F+; 0.15 x 255 = 38.25) and 36 (Compat), the lit side facing the camera 177 (F+) and 145 (Compat). A white sphere in Forward+ has a brighter, flatter mid-tone and a lit band that reaches further past the terminator.
- **F4. `03` does not clamp the sum.** At the lit pole lambert + ambient = 1.15 on a white surface; the screen clips it (255), as the original's 8-bit buffer did.
- **F5. `04` declares `specularPower` and `specularColor` but never reads them.** And the rim IS multiplied by (lambert + ambient), so it fades on the dark side: a dark-side point (N.L = -0.3, N.E about 0.25) reads 47 (F+), almost black.
- **F6. `05`'s `-reflect(eye, normal)` is the standard mirror direction** `2 (N.E) N - E`; the highlight peak sits within 1 pixel of the half vector `normalize(L + E)`. Half-height width at power 30: 60 px, at power 100: 33 px, both as pow(R.L, power) predicts.
- **F7. `06` labels its colour texture `TextureType = "Cube"` and `UIName = "Reflection Texture"`** although it is read with `tex2D`. Metadata slip, copied into 07, 08, 11, 12, 15 **(code reading)**. The tangent and binormal it builds are never read.
- **F8. `07` lost a factor.** In `04` to `06` the rim is `pow(1 - N.E, power) * (lambert + ambient)`; in `07` (and 08, 11, 12) it is `pow(1 - N.E, power)` only, so the rim glows on the dark side. A dark-side point (N.L = -0.4, N.E about 0.2) reads 188 in 07 (F+): the rim there is pow(1 - 0.21, 3) = 0.49 in linear light. With the factor 04 to 06 have (lambert 0 plus ambient 0.0196 in linear light) it would be 0.01 (computed, not rendered). The spec map's red channel masks the rim and green masks the highlight.
- **F9. `08` and `15` disagree about the normal map's green channel.** 08 adds `green * binormal`; 15 adds `green * -binormal`. In Godot, BINORMAL points up the image, so 08 expects an OpenGL-style map (green = up) and 15 expects a DirectX-style map (green = down) **(code reading, plus run)**. Run: with the GL map the upper side of a dome reads (193, 83, 77) in 08; the same shader fed the DX map reads (29, 3, 3). Lesson 15 with the DX map and `flip_green` is the same picture as the GL map without it (51 of 230,400 sampled pixels differ, all on cube-map edges).
- **F10. `09`'s cube map shows nothing on a surface that faces the camera.** The reflection is `fresnel * cube`, and the rim weight is 0 at N.E = 1 (0.125 at 0.5, 0.512 at 0.2, 1 at the silhouette), times (lambert + ambient). Run: the pixel facing the camera reads exactly what lesson 03 gives there (177, 177, 177 in F+). The header says "basic phong shader with an added cube map". It is a rim reflection.
- **F11. `10` is an object-space wobble that keeps the original lighting.** Default `vertOffset` is (0,0,0): nothing moves out of the box. The normal is not recomputed and the camera vector uses the undeformed position, so the shading stays that of the original shape. `outColor.a = fresnel` is dead code (Opaque). Run: offset 0 is pixel-identical to lesson 05; with `vert_offset = (0, 0.3, 0)`, frequency 3, speed 2 at TIME 1.444 the top edge of the sphere moved from y = 112 to y = 54 on screen and the whole silhouette matched the CPU's evaluation of the Cg formula on every vertex within 1.0 px; sideways offset 0.4 at TIME 2.891 matched within 1.4 px.
- **F12. `11` scales about the centre and "more" means more tiles.** `uv = ((uv - 0.5) * scale + translate + time * speed) + 0.5`: scale 2 shows the picture twice across, not zoomed in. Identity (scale 1, translate 0, speed 0, the Cg defaults) is pixel-identical to lesson 08.
- **F13. `12` has four techniques and none has a second pass.** In Godot a blend mode is a compile-time `render_mode`. AlphaBlend, AlphaTest and Additive were each checked by pixel value: AlphaBlend rim alpha 0.079 over the stage colour; AlphaTest keeps a pixel only above alpha 0.3 (cells at alpha 0.000 and 0.079 show the stage colour, alpha 1.0 shows the opaque colour); Additive adds colour x alpha to the stage (alpha 0.079: (219, 216, 207) F+, over (217, 213, 202)). Blending is in linear light in Forward+ (T17).
- **F14. `13`'s channels do not follow RGB order.** Red picks `shaderColor`, BLUE picks `blendedColor`, GREEN picks `thirdColor`. Run with swapped colours: the red band shows `shader_color` (yellow), the blue band `blended_color` (cyan), the green disc `third_color`.
- **F15. `14`: `pow(cube, reflectionContrast)` needs the exponent widened in Godot (T14). `fresnelOffset` is a floor on the reflection.** With the demo paint, the pixel facing the camera reads (96, 13, 13) (F+); with `fresnel_offset = 0.5` it reads (145, 96, 13): the reflection now shows there. Two highlights share one R.L: at 10 degrees off the peak only the wide (power 8) one reaches (212, 212, 212).
- **F16. `15` re-packs the spec map.** 07 to 12: red = rim mask, green = highlight mask. 15: RED = highlight mask, BLUE = reflection mask, the rim is unmasked and multiplied by lambert and light colour. The ambient is a hemisphere blend (anything facing down gets `bottomColor`, default black), and `subsurfaceColor` (default (0.1, 0, 0)) is added INSIDE the saturate, so a faint red appears only for N.L between -0.1 and 0.
- **F17. Direction and Time semantics are assumptions** **(code reading)**: `lightDirection : Direction` is assumed to be a world-space vector the host leaves alone; `time : Time` is assumed to count seconds.

---

## 6. Per lesson: what the original did, what changed, what was checked

Each `.gdshader` opens with a header comment that says the same in short (source file, conversion statement, what the original did, what changed).

- **00 `00_super_simple`**: flat colour. `POSITION` written out by hand. Checks: flat teal reads the same at all five named points and over 21,634 sampled pixels (100 percent within 3 bytes); hand-written `POSITION` identical to Godot's.
- **01 `01_base`, 02 `02_lambert`**: Lambert. Checks: lit pole, facing, terminator, dark side, mid-lit point, 21,634 sampled pixels, 100 percent within 3 bytes (F+) and 100 (Compat); 01 and 02 render identically; the Cg default light on 02 (F2).
- **03 `03_lambert_ambient`**: plus ambient colour. Checks: ambient floor in deep shadow (N.L = -0.75) reads 38 (F+) / 36 (Compat), lit pole clips at 255.
- **04 `04_fresnel`**: plus rim. Checks: ten, including rim at N.E 0.25, 0.11, the dark-side rim, and `fresnel_power` 6 at the same point (223 at power 3, 205 at power 6, F+).
- **05 `05_phong`**: plus highlight. Checks: ten, including highlight position (brightest pixel (229, 244) against predicted (230, 245)) and width (60 px at power 30, 33 px at power 100) in a specular-only render (black surface, no ambient, tight rim).
- **06 `06_diffuse_mapped`**: plus colour map. Checks: red, green, yellow, magenta marker cells, sand and steel cells (texel values through lighting); full image 100 percent within 3 bytes (F+).
- **07 `07_spec_mapped`**: plus spec map. Checks: the highlight peak lands on a steel cell whose spec mask is 0 (reads (68, 104, 140), no highlight) and just below it on a sand cell whose mask is 1 (reads (255, 208, 244), highlight); bright and dim rim rows; the dark-side rim (F8).
- **08 `08_normal_mapped`**: plus normal map. Checks: dome centre, right, left, upper, lower sides; perturbation components (+0.66 tangent, -0.68, +0.68 binormal, -0.66); DX map result; full image 99.95 percent.
- **09 `09_cube_mapped`**: plus cube map. Checks: nine, including the reflection lookup at a point near the silhouette (reflection vector (0.03, 0.30, -0.95), cube texel (53, 92, 179) linear, pixel (162, 169, 183) against (163, 170, 183) expected) and equality with lesson 03 where the surface faces the camera; full image 99.98 percent.
- **10 `10_vertex_anim`**: plus vertex wobble. Checks: zero offset equals lesson 05; two silhouette checks against the CPU evaluation of the Cg formula on every vertex.
- **11 `11_uv_manip`**: plus uv transform. Checks: identity equals 08; scale 2 plus translate (0.25, 0.125) and a scroll of (0.1, 0.05) per second at a TIME read from the same frame, with points chosen so the TRANSFORMED uv lands in a cell centre.
- **12 `12_techniques`**: four techniques. Checks: three places (rim alpha 0.000, 0.079, 1.000) times four techniques, each against the expected blended, tested or added value.
- **13 `13_blended`**: blend map. Checks: red band, blue band, blue disc, green disc, and the swapped-colour run.
- **14 `14_car_shader`**: plus fresnel intensity and offset, contrast, second highlight. Checks: eleven, including offset 0.5 and the two-highlight shoulder.
- **15 `15_uber`**: everything. Checks: fourteen, including hemisphere ambient, subsurface spread 0.5 at the terminator (reads (179, 171, 146)) and the DX-plus-flip equality; full image 98.5 percent (F+) and 98.8 percent (Compat).

---

## 7. Not verified, and open

- No Maya or CgFX runtime was available. Everything said about how the Cg behaved in its host is code reading (F7, F17, departure 14).
- The default of `AlphaBlendEnable = True` without a `BlendFunc` is the biggest unknown (departure 14).
- Pixel values are Apple M4 Pro, Godot 4.7.2, windowed, offline fixed steps; they say nothing about real-time speed on any other machine.
- `repeat_disable` did not clamp in Compatibility in the T11 test: a Godot behaviour not explained here.
- The `Texture.hint_normal` decode of RG-compressed normal maps was not tested (the maps here are plain RGB).
- The stage scene (`scenes/stage.tscn`) was not opened in the Godot editor; it was only run through the script harness. Open it and press Left / Right to see the lessons.
