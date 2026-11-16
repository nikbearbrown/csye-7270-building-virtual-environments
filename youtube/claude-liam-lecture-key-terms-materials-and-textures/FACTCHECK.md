# FACTCHECK - Key Terms: Materials and Textures

Status: 2026-11-13, checked by Claude. Figures: every spoken figure machine-checked against the words on the slide at that step. Explanations: an independent second pass compared every beat with its slide and the chapter; no beat needed rewording. No human sign-off.

The film teaches from the deck; the deck's numbers are computed in the page or labelled illustrative or simulated on the slide itself (the badge at top right). This file checks that the narration says only what the slide and the chapter support.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | BOPEN | Playlist name, film title, what the film covers | PASS | Playlist name follows the Computational Skepticism one (course name, Exam Prep); summary restates the deck's map slide | none |
| 2 | BDEFS | What each tag and badge means: In the book text, In the glossary, Video only, Computed, Simulation, Illustrative data, Conceptual | PASS | Deck slide 1 speaker note (tags); the badges are the deck's own evidence labels; seeded = the deck's `rng(seed)` | none |
| 3 | B0101 | Figures spoken: `34` | PASS | Each figure is printed on slide 2 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 4 | B0101 | Explanation of: GROUP; TERMS; WHAT IT IS ABOUT; What a material holds | PASS | Second-pass check against slide 2 step 1 and 07-materials-and-textures.md | none |
| 5 | B0102 | Explanation of: Maps are data; What each image means and how to read it | PASS | Second-pass check against slide 2 step 2 and 07-materials-and-textures.md | none |
| 6 | B0103 | Explanation of: Packing and engines; How maps share one file, and why engines differ | PASS | Second-pass check against slide 2 step 3 and 07-materials-and-textures.md | none |
| 7 | B0104 | Explanation of: Fitting textures to a mesh; Where a texture lands, how sharp it is, how it is lit | PASS | Second-pass check against slide 2 step 4 and 07-materials-and-textures.md | none |
| 8 | B0201 | Figures spoken: `0.00`, `0.50` | PASS | Each figure is printed on slide 3 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 9 | B0201 | Explanation of: Material; in the book text; TELL THESE APART; Albedo | PASS | Second-pass check against slide 3 step 1 and 07-materials-and-textures.md | none |
| 10 | B0202 | Explanation of: PBR; in the book text; THE SAME MATERIAL UNDER THREE LIGHTS; light A | PASS | Second-pass check against slide 3 step 2 and 07-materials-and-textures.md | none |
| 11 | B0203 | Explanation of: Lighting; in the book text; LIGHT ORBITS; THE MARKED POINT CHANGES COLOUR; ambient | PASS | Second-pass check against slide 3 step 3 and 07-materials-and-textures.md | none |
| 12 | B0301 | Explanation of: Albedo; in the book text; also: base colour; The colour the surface reflects, before any lighting. | PASS | Second-pass check against slide 4 step 1 and 07-materials-and-textures.md | none |
| 13 | B0302 | Figures spoken: `0.10`, `0.90`, `2°`, `45°` | PASS | Each figure is printed on slide 4 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 14 | B0302 | Explanation of: in the book text; Roughness; ROUGHNESS 0.10 TO 0.90, METALLIC 0; 0.10 | PASS | Second-pass check against slide 4 step 2 and 07-materials-and-textures.md | none |
| 15 | B0303 | Figures spoken: `0.30`, `diffuse 0.26`, `diffuse 0.00` | PASS | Each figure is printed on slide 4 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 16 | B0303 | Explanation of: Metallic; in the book text; METALLIC 0 TO 1, ROUGHNESS 0.30; 0.00 | PASS | Second-pass check against slide 4 step 3 and 07-materials-and-textures.md | none |
| 17 | B0401 | Explanation of: Colour texture; in the book text; Data texture; in the book text | PASS | Second-pass check against slide 5 step 1 and 07-materials-and-textures.md | none |
| 18 | B0402 | Figures spoken: `0`, `255`, `146`, `0.29` | PASS | Each figure is printed on slide 5 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 19 | B0402 | Explanation of: sRGB; in the book text; EIGHT EVEN sRGB STEPS AND THE LIGHT THEY STAND FOR; 0 | PASS | Second-pass check against slide 5 step 2 and 07-materials-and-textures.md | none |
| 20 | B0403 | Figures spoken: `0.502`, `0.216` | PASS | Each figure is printed on slide 5 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 21 | B0403 | Explanation of: Linear and decoding; in the book text; DECODE CURVE: STORED VALUE TO LINEAR; 128/255 = 0.502 becomes 0.216 | PASS | Second-pass check against slide 5 step 3 and 07-materials-and-textures.md | none |
| 22 | B0404 | Figures spoken: `128, 128, 255`, `value 0.502`, `value 0.216`, `tilt 38.8°`, `22%` | PASS | Each figure is printed on slide 5 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 23 | B0404 | Explanation of: FLAT NORMAL TEXEL (128, 128, 255), READ TWO WAYS; read as linear data; value 0.502; unpacked +0.004 | PASS | Second-pass check against slide 5 step 4 and 07-materials-and-textures.md | none |
| 24 | B0501 | Explanation of: Normal map; in the book text; TELL THESE APART; Normal map | PASS | Second-pass check against slide 6 step 1 and 07-materials-and-textures.md | none |
| 25 | B0502 | Figures spoken: `26.6°` | PASS | Each figure is printed on slide 6 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 26 | B0502 | Explanation of: Tangent space; in the glossary; THE SAME TEXEL ON THREE SURFACES; flat | PASS | Second-pass check against slide 6 step 2 and 07-materials-and-textures.md | none |
| 27 | B0503 | Explanation of: Green channel convention; in the book text; Whether green points up (OpenGL, Godot) or down (DirectX).; A DOME, LIT FROM ABOVE: GREEN UP OR GREEN DOWN | PASS | Second-pass check against slide 6 step 3 and 07-materials-and-textures.md | none |
| 28 | B0601 | Figures spoken: `0.50`, `AO = 0.72` | PASS | Each figure is printed on slide 7 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 29 | B0601 | Explanation of: Ambient occlusion; in the book text; TELL THESE APART; Texture AO | PASS | Second-pass check against slide 7 step 1 and 07-materials-and-textures.md | none |
| 30 | B0602 | Figures spoken: `AMBIENT 0.05`, `output 0.04`, `emission 0.60`, `output 0.64` | PASS | Each figure is printed on slide 7 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 31 | B0602 | Explanation of: Emission; in the glossary; Light the surface gives off itself.; A SURFACE IN A DARK ROOM: AMBIENT 0.05, ALBEDO 0.80 | PASS | Second-pass check against slide 7 step 2 and 07-materials-and-textures.md | none |
| 32 | B0603 | Figures spoken: `0.85`, `0.94`, `0.82` | PASS | Each figure is printed on slide 7 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 33 | B0603 | Explanation of: in the book text; SSAO; BRIGHTNESS = AMBIENT × AO + DIRECT; no AO | PASS | Second-pass check against slide 7 step 3 and 07-materials-and-textures.md | none |
| 34 | B0701 | Explanation of: ORM; in the book text; TELL THESE APART; ORM | PASS | Second-pass check against slide 8 step 1 and 07-materials-and-textures.md | none |
| 35 | B0702 | Figures spoken: `0.65 = 165`, `0.82 = 210`, `0.00 = 0` | PASS | Each figure is printed on slide 8 at step 2 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 36 | B0702 | Explanation of: Channel packing; in the glossary; ONE TEXEL, THREE VALUES; R channel = AO | PASS | Second-pass check against slide 8 step 2 and 07-materials-and-textures.md | none |
| 37 | B0703 | Explanation of: Map slot naming; in the glossary; FILE NAMES TO SLOTS, AS IN THE SHIP; …hull_diff | PASS | Second-pass check against slide 8 step 3 and 07-materials-and-textures.md | none |
| 38 | B0801 | Figures spoken: `roughness 0.10`, `smoothness 0.90`, `roughness 0.30`, `smoothness 0.70` | PASS | Each figure is printed on slide 9 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 39 | B0801 | Explanation of: Smoothness; in the glossary; The inverse of roughness: how mirror-like a surface is.; TELL THESE APART | PASS | Second-pass check against slide 9 step 1 and 07-materials-and-textures.md | none |
| 40 | B0802 | Figures spoken: `roughness 0.60`, `smoothness 0.40` | PASS | Each figure is printed on slide 9 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 41 | B0802 | Explanation of: HDRP mask map; in the book text; REPACK ONE TEXEL: GODOT ORM TO HDRP MASK MAP; Godot ORM | PASS | Second-pass check against slide 9 step 2 and 07-materials-and-textures.md | none |
| 42 | B0803 | Explanation of: URP Lit maps; in the book text; SLOT BY SLOT; Godot | PASS | Second-pass check against slide 9 step 3 and 07-materials-and-textures.md | none |
| 43 | B0901 | Figures spoken: `4 × 4`, `0.58, 0.26` | PASS | Each figure is printed on slide 10 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 44 | B0901 | Explanation of: UV; in the book text; TELL THESE APART; UV map | PASS | Second-pass check against slide 10 step 1 and 07-materials-and-textures.md | none |
| 45 | B0902 | Figures spoken: `6 FACES`, `12 EDGES`, `5 as folds`, `7 edges are cut` | PASS | Each figure is printed on slide 10 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 46 | B0902 | Explanation of: Unwrapping; in the glossary; Cutting a mesh along seams and flattening it into a UV map.; A CUBE CUT OPEN: 6 FACES, 12 EDGES | PASS | Second-pass check against slide 10 step 2 and 07-materials-and-textures.md | none |
| 47 | B0903 | Figures spoken: `185 vertices`, `2 vertices`, `0.46` | PASS | Each figure is printed on slide 10 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 48 | B0903 | Explanation of: video only; Texture baking; HIGH-POLY DETAIL BAKED INTO A NORMAL MAP; high-poly: 185 vertices on this line | PASS | Second-pass check against slide 10 step 3 and 07-materials-and-textures.md | none |
| 49 | B1001 | Figures spoken: `8 × 8`, `64 texels`, `16 × 16`, `256 texels`, `32 × 32`, `1,024 texels`, `1024 × 1024`, `a million texels` | PASS | Each figure is printed on slide 11 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 50 | B1001 | Explanation of: Resolution; in the glossary; Width and height of a texture in pixels.; TELL THESE APART | PASS | Second-pass check against slide 11 step 1 and 07-materials-and-textures.md | none |
| 51 | B1002 | Figures spoken: `1024`, `2 m wall`, `8 m wall`, `512 px/m`, `128 px/m`, `four times coarser` | PASS | Each figure is printed on slide 11 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 52 | B1002 | Explanation of: in the glossary; Texel density; ONE 1024 TEXTURE ON TWO WALLS; 2 m wall | PASS | Second-pass check against slide 11 step 2 and 07-materials-and-textures.md | none |
| 53 | B1003 | Figures spoken: `UV scale 4`, `8 m`, `512 px/m` | PASS | Each figure is printed on slide 11 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 54 | B1003 | Explanation of: UV scale; in the glossary; A multiplier on UVs that sets how often a texture repeats.; UV SCALE 4 ON THE LONG WALL | PASS | Second-pass check against slide 11 step 3 and 07-materials-and-textures.md | none |
| 55 | B1101 | Explanation of: Tiling; in the glossary; TELL THESE APART; Repeat | PASS | Second-pass check against slide 12 step 1 and 07-materials-and-textures.md | none |
| 56 | B1102 | Figures spoken: `1.6`, `0.60` | PASS | Each figure is printed on slide 12 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 57 | B1102 | Explanation of: Wrap mode; in the glossary; SAMPLING PAST THE EDGE: u FROM 0 TO 1.6; repeat | PASS | Second-pass check against slide 12 step 2 and 07-materials-and-textures.md | none |
| 58 | B1103 | Figures spoken: `1024`, `1 × 1`, `11 levels` | PASS | Each figure is printed on slide 12 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 59 | B1103 | Explanation of: Mipmap; in the book text; A 1024 TEXTURE AND ITS MIP LEVELS; levels 0 to 6: 1024, 512, 256, 128, 64, 32, 16 pixels wide | PASS | Second-pass check against slide 12 step 3 and 07-materials-and-textures.md | none |
| 60 | B1104 | Figures spoken: `4 BYTES`, `level 0: 4.00 MiB`, `5.33 MiB`, `+33.3%`, `64 pixels`, `level 4 is used (64 × 64)` | PASS | Each figure is printed on slide 12 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 61 | B1104 | Explanation of: MEMORY (RGBA, 4 BYTES A TEXEL) AND WHICH LEVEL IS USED; level 0: 4.00 MiB; all levels: 5.33 MiB (+33.3%); drawn 64 pixels wide on screen: | PASS | Second-pass check against slide 12 step 4 and 07-materials-and-textures.md | none |
| 62 | B1201 | Explanation of: Baked lighting; in the glossary; TELL THESE APART; Baked lighting | PASS | Second-pass check against slide 13 step 1 and 07-materials-and-textures.md | none |
| 63 | B1202 | Figures spoken: `direct light 0.00`, `0.40` | PASS | Each figure is printed on slide 13 at step 2 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 64 | B1202 | Explanation of: Global illumination; in the book text; BOUNCE LIGHT: A RED FLOOR TINTS A WHITE WALL; sun | PASS | Second-pass check against slide 13 step 2 and 07-materials-and-textures.md | none |
| 65 | B1203 | Explanation of: Reflection probe; in the book text; A PROBE'S SAMPLES; A MIRROR SPHERE SHOWS THEM; the probe | PASS | Second-pass check against slide 13 step 3 and 07-materials-and-textures.md | none |
| 66 | B1301 | Figures spoken: `smoothness 0.85`, `roughness 0.15` | PASS | Each figure is printed on slide 14 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 67 | B1301 | Explanation of: PAIR 1 · LEFT; Roughness; 0 is mirror, 1 is dull.; roughness 0.85 | PASS | Second-pass check against slide 14 step 1 and 07-materials-and-textures.md | none |
| 68 | B1302 | Figures spoken: `0.30`, `0.15`, `0.24` | PASS | Each figure is printed on slide 14 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 69 | B1302 | Explanation of: PAIR 2 · LEFT; Texture AO; baked into a map, ambient only.; texture AO 0.50 | PASS | Second-pass check against slide 14 step 2 and 07-materials-and-textures.md | none |
| 70 | B1303 | Figures spoken: `0.502`, `0.22`, `0.50` | PASS | Each figure is printed on slide 14 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 71 | B1303 | Explanation of: PAIR 3 · LEFT; Colour texture; decode sRGB before lighting.; sRGB 0.502 | PASS | Second-pass check against slide 14 step 3 and 07-materials-and-textures.md | none |
| 72 | B1304 | Figures spoken: `1024`, `8.0 m`, `128 px/m` | PASS | Each figure is printed on slide 14 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 73 | B1304 | Explanation of: PAIR 4 · LEFT; Resolution; how many pixels in the image.; same 1024 × 1024 file | PASS | Second-pass check against slide 14 step 4 and 07-materials-and-textures.md | none |
| 74 | B1401 | Figures spoken: `1.0`, `0.3`, `diffuse 0.00` | PASS | Each figure is printed on slide 15 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 75 | B1401 | Explanation of: “make it look like metal”; WHAT THE INSTRUCTION DOES; metallic 0, roughness 0.8; diffuse 0.26 | PASS | Second-pass check against slide 15 step 1 and 07-materials-and-textures.md | none |
| 76 | B1402 | Figures spoken: `128`, `0.502`, `0.216`, `0°`, `38.8°` | PASS | Each figure is printed on slide 15 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 77 | B1402 | Explanation of: “the normal map looks wrong”; linear data: 0.502; tilt 0.3°; sRGB-decoded: 0.216 | PASS | Second-pass check against slide 15 step 2 and 07-materials-and-textures.md | none |
| 78 | B1403 | Figures spoken: `1024 px`, `2 m`, `512 px/m`, `8 m wall`, `UV scale 4` | PASS | Each figure is printed on slide 15 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 79 | B1403 | Explanation of: “make the wall texture sharper”; 2 m wall, scale 1; 512 px/m; 8 m wall, scale 1 | PASS | Second-pass check against slide 15 step 3 and 07-materials-and-textures.md | none |
| 80 | B1404 | Figures spoken: `1024`, `4.00`, `5.33 MiB` | PASS | Each figure is printed on slide 15 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 81 | B1404 | Explanation of: “stop the shimmer in the distance”; no mipmaps: 4.00 MiB; with mipmaps: 5.33 MiB; about a third more memory | PASS | Second-pass check against slide 15 step 4 and 07-materials-and-textures.md | none |
| 82 | B1405 | Figures spoken: `0.60`, `0.40` | PASS | Each figure is printed on slide 15 at step 5 (machine check, check_narration.py). Badge: Computed. | none |
| 83 | B1405 | Explanation of: “use the Poly Haven arm file in Unity HDRP”; R metallic; 0.00; G AO | PASS | Second-pass check against slide 15 step 5 and 07-materials-and-textures.md | none |
| 84 | B1501 | Explanation of: Is each map colour or data, and decoded that way?; Is the normal map tangent space, green up for Godot?; Which channel does each packed map read: R, G, B?; Is texel density the same on neighbouring objects? | PASS | Second-pass check against slide 16 step 1 and 07-materials-and-textures.md | none |
| 85 | B1502 | Explanation of: Before you trust a material | PASS | Second-pass check against slide 16 step 2 and 07-materials-and-textures.md | none |
| 86 | B1503 | Explanation of: Before you trust a material | PASS | Second-pass check against slide 16 step 3 and 07-materials-and-textures.md | none |
| 87 | B1504 | Explanation of: Before you trust a material | PASS | Second-pass check against slide 16 step 4 and 07-materials-and-textures.md | none |
| 88 | B1505 | Explanation of: Before you trust a material | PASS | Second-pass check against slide 16 step 5 and 07-materials-and-textures.md | none |
| 89 | B1506 | Figures spoken: `1.0`, `0.3` | PASS | Each figure is printed on slide 16 at step 6 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 90 | B1506 | Explanation of: Before you trust a material | PASS | Second-pass check against slide 16 step 6 and 07-materials-and-textures.md | none |
| 91 | BVDT | Six recap lines | PASS | Each restates a body beat; nothing new | none |
| 92 | BHTF | Practice prompt | EXEMPT | A viewer exercise composed from the film's terms; not presented as a run | none |

## Things noticed on the deck itself (not changed; for Bear)

- Slide 11 step 4: '16 texels share a pixel (minification)'. A 1024 texture drawn 64 pixels wide puts 16 texels per pixel along each axis, so 256 texels share each screen pixel. The code uses tpp = 1024 / 64. The narration says 'many texels'.
- Slide 14 step 1: the chart for the exact instruction 'metallic 1.0, roughness 0.3' shows specular 0.00 as well as diffuse 0.00, so the fix looks like a black surface. The sampled normal [0.3, 0.3, 0.9] lies outside the narrow roughness-0.3 highlight. Slide 3 step 3 shows the metallic-1 sphere with a highlight. The narration speaks only the diffuse drop.
- Slide 14 step 2 says 'tilt must be 0°', while its own chart and slide 4 step 4 give 0.3° for the correct linear read (unpacked +0.004). The narration says 'about zero'.
- Slide 9 step 1: 'texel column 2, row 2 from the top' counts from zero, but the dot sits visibly in the third column and third row of the 4 × 4 checker. Nothing says the count starts at 0. The narration does not speak it.
- Slide 6 carries the badge 'Computed' while its note says the SSAO bars use illustrative inputs. The same SSAO 0.80 case is reused on slide 13 pair 2, also under 'Computed'. The narration calls both a made-up example.
- Slide 13 pair 1 says 'highlight 45° wide' for roughness 0.85, while slide 3 step 2 calls 45° the half-width and gives it for roughness 0.90. In halfWidth() the exponent clamps at 2 from about roughness 0.84 up, so 0.85 and 0.90 both give 45°.
- Slide 12 step 1: the box moves out and back (kf 0, 1, 0), so the step ends with both rows identical and the baked-versus-real-time difference shows only mid-animation. The step sits under the badge 'Illustrative data', though its shadow is computed per cell and only step 2's bounce factor is illustrative.
- Slide 10: step 2 draws the 8 m wall four times taller as well as longer than the 2 m wall, so its checker squares look the same size. Step 3 then draws the same wall as a thin strip the height of the 2 m wall. The caption 'four times coarser' is not visible in step 2's picture.
- Slide 13 pair 2, left: the remaining ambient part is drawn in the same dark ink as the direct part, so the bar reads dark, grey, dark and looks like a gap, not a dimmed ambient part. The right bar uses red for it.
- Term names differ between the map and the slides: the map lists 'linear' and 'green channel', and the slides title them 'Linear and decoding' and 'Green channel convention'. Slide 8 step 3 puts the 'ORM texture → HDRP Mask Map' row under the heading 'Unity URP Lit / HDRP', though that row is HDRP only.
