# Acts and coverage map: Local, World and Screen Space

**What this is.** How this film is built from its brief: which part of the source lands in which act, which parts are left out and why, the cast per act, the opening correction, the terms card, the additions that are in no source, and the cut line.
**Why.** A film cut from a long source only works if every idea has a home. This file is the record that nothing was dropped silently, and that what was added was checked.
**Found.** Five acts, 40 body beats, about 10.1 minutes (1,770 spoken words, 1,456 of them in the body). The source slice (about 27 minutes of a long third-party course: the model matrix, then the canvas coordinates) is covered end to end except the clip-space matrix and the 3D equivalents. Eleven things in the film are in no source (listed below); three source or documentation claims were corrected (the zero and one in the vec4, the texture-pixel-size shortcut, the docs' range for FRAGCOORD).

The source is a third-party work whose creator is not named in the brief; its ideas are followed, nothing is copied (see `SOURCES.md`).

## Coverage

| Source or brief item | Where it goes | Note |
|---|---|---|
| The one idea: a position is numbers relative to something; the three zeros | **Act I**, B02 and B03 | B02 is new: the same dot, the zero moves, the numbers change |
| The same corner of a sprite: local, world, screen; a moved sprite keeps its local numbers and changes its world numbers | **Act I**, B04 to B07 | numbers chosen and measured: (-64,-64), (536,336), (286,236), then (186,236) after a pan |
| The source draws three spaces on a picture of the project | **Act I**, B03 | rebuilt as one diagram: world rectangle, window frame, sprite |
| `MODEL_MATRIX` and `CANVAS_MATRIX` are mat4 and vertex-only | **Act II**, B10, B14 and **Act IV**, B27 | "vertex-only" is shown by the real compile error, "mat4" by the 4 by 4 table |
| `world = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy`; why a vec4 with 0 and 1 | **Act II**, B12 and B13 | the source says to include them without a reason: CORRECTED, the reason is the matrix's last column and it is tested (w = 0 gives a direction) |
| `world_position` as a vec2 varying | **Act II**, B14 and B15 | |
| Colour by world position to show it differs from local when the node is moved | **Act II**, B16 | |
| Texture lookup by `world_position * TEXTURE_PIXEL_SIZE * scale` with a repeating second texture | **Act III**, B17 to B22 teach a tile size you choose; B23 shows the shortcut as a pitfall | the brief's pitfall: the shortcut only makes sense for a 128 px sprite; measured: the pattern halves when 128 px art becomes 64 px art |
| A circle cutout at world coordinates with `distance` and `discard` | **Act III**, B24 | rebuilt as a hole of radius 60 that stays put while the sprite crosses it (brief cut line) |
| `amount` animated with a tween: the "spacing out" payoff | **Act III**, B25 | the tween needs its start value set from code first (a known trap, checked again) |
| Canvas chapter: `VERTEX` in `fragment()` is the screen position; times `SCREEN_PIXEL_SIZE` gives 0 to 1 | **Act IV**, B30 and B32 | |
| The varying form `CANVAS_MATRIX * MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)` | **Act IV**, B27 to B29 | order tested against the swapped order |
| `SCREEN_UV`, `FRAGCOORD` | **Act IV**, B31 and B32 | the docs' range for FRAGCOORD is wrong for the engine: CORRECTED |
| "The four methods give the same result" | **Act IV**, B33 | tested in five setups (plain, camera panned, zoomed, rect turned, window stretched): they agree; the real differences are units and the window size (B32, B34) |
| Effects fixed to the world against effects that follow the screen (the brief's why) | **Act V**, B35 to B40 | new: three striped sprites and a two-move test (slide the sprite, pan the camera) |

## LEFT OUT (with reasons)

- **`SCREEN_MATRIX`** (canvas space to clip space): no effect in this film needs it; naming a third matrix without a picture would only add a term.
- **Spatial (3D) shaders**: their built-ins differ (`VIEW_MATRIX` and others); the film is canvas item only and does not claim the 3D names.
- **Building matrices** (translate, rotate, scale, pivots): the film uses `MODEL_MATRIX` as a given; constructing matrices belongs to the film on matrices.
- **Reading the screen texture** (post-processing, water): belongs to the film on reading the screen; B26 only says why a screen address is needed.
- **`CanvasLayer` transforms, `SubViewport` spaces**: they change what "screen" is measured against; verified (a layer's own transform is what `CANVAS_MATRIX` holds, `verify2.gd` case e) but not taught, to stay inside ten minutes.
- **Camera rotation, smoothing and limits**: pan and zoom are enough for the idea.
- **Vertex displacement interacting with varyings**: belongs to the film on vertex shaders.
- **The source's promotion and sign-up material**: none in this slice.

## Added: in no source (each is checked, FACTCHECK.md)

1. The same dot with a moving zero (B02): the whole film's idea in one picture.
2. The model matrix includes the node's parents; the editor's position is relative to the parent, with worked numbers (B10, B11).
3. The last-column explanation of the zero and the one, with the direction demonstration (B13).
4. The real compile error for the matrix read in `fragment()` (B14).
5. UV as local space squeezed to zero to one, measured at both corners (B17).
6. A sampler with no repeat hint clamps; the smear is shown on the real sky (B20).
7. The sky stays put under a turn and a stretch (B22).
8. The docs say (1.0, 1.0) for the far corner of FRAGCOORD; the engine counts pixels (B31).
9. Four tiles, four methods, one seamless gradient, tested in five setups (B33).
10. Screen pixels are real window pixels under stretch mode; a fraction of the screen is not (B34).
11. Three anchored stripe sprites and the two-move test (B36, B37), which also separates world from screen.

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I Three Addresses | the test sprite (a square outline with the teal blob), the three zero markers, the window frame, the world rectangle, the terracotta corner dot; in captures the blob over the star sky and its faint copy |
| II From Local to World | the same sprite and corner dot; the 4 by 4 matrix table; the vec4 token; the world-field colors |
| III Locked to the World | the blob over the star sky, its faint copy and the ringed planet; the white square only for the turn-and-stretch beat; the checker only for the texture-pixel-size beat; the hole ring |
| IV Where Is the Screen? | the window frame, the corner token, the two matrix boxes; the four tiles and their gradient |
| V Choosing a Space | the three striped blobs; the pin on three things |

## Opening correction and terms

- **BIDEA**: the writer types "A position is just a position." and replaces "just a position" with "an address in some space".
- **BDEFS** (prerequisites only, six): Shader, Pixel, Origin, Space, Vertex, Texture, in the GLOSSARY wording. The terms this film exists to teach (local space, world space, screen space, matrix, model matrix, canvas matrix, vector, vertex(), fragment(), built-in, varying, UV, tile size, repeat enable, discard, mix, distance) are earned in their acts, each defined on screen where first spoken in the GLOSSARY wording where it exists: screen space (B03), built-in and vertex() (B08), matrix (B09), vector (B12), fragment() (B14, a line the broken-shader script prints), varying (B15), UV (B17), `texture()` (B18), `repeat_enable` and `repeat_disable` (B20), `TEXTURE_PIXEL_SIZE` (B23), `distance` and `discard` (B24), `amount` and `mix` (B25). The new ones (local space, world space, model matrix, canvas matrix, tile size) are in the report to the series lead.

## Cut line

If the film runs long, cut in this order: the hole beat (B24), the wrong-order beat (B29), the turn-and-stretch beat (B22) and the parents warning (B11); each repeats an idea another beat carries and none leans on its neighbours. Only if that is not enough, drop the frag coord beat (B31) and its tile in capture C10, and change "four" to "three" in B26 and B33 and the counting words in B30 to B32 (re-voice those beats). The sky window (B21), the world colors (B16), the four-tile agreement (B33) and the two-move test (B36, B37) stay: they are the proof and the payoff. Current estimate: about 10.1 minutes, so no cut is needed.

## Editor-frame reconciliation 2026-10-13

**What changed.** Beat B11's picture and capture description, and FACTCHECK row 23's evidence, were reconciled with the real Godot 4.7.2 editor frames recorded by script on 2026-10-13 (`../_godot-shaders-series/editor-capture/README.md`, section 2.5). **Why.** The first plan could not show the Inspector, so the lane described a picture from the property list (`verify11.gd`) and had a Manim fallback. No narration changed: the real Inspector reads Node2D, Transform, Position with fields x and y, exactly what the line says. Nothing was voiced, rendered or published.

- **B11.** The lane now uses the clean-root pair (Child selected: Position 50.0 px, 0.0 px; Parent selected: 500.0 px, 300.0 px; the Scene dock reads Scene, Parent, Child), whole frames, cross-dissolved, with measured ring boxes. The plan-exact scene (the root node itself is the transformed Parent) shows an editor warning triangle on the root, so it is not used. The dissolve moved from 0.42 to 0.58 of the beat so the parent's numbers appear when the voice reaches "a parent at five hundred, three hundred" (it fell before "a child at fifty, zero" was spoken). Row 23 is PASS with the frames as evidence; the Manim fallback is no longer needed.
- Beat ids, beat count (40 body), lane types and acts are unchanged; words unchanged (1,770 by the lint's count, 10.1 minutes). `lint_series.py`: no errors, no warnings.
