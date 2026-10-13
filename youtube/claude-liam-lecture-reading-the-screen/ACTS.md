# Acts and coverage map: Reading the Screen

**What this is.** How the film is built from its brief and the two third-party sources the brief describes: which part lands in which act, which parts move to another film of the series or are left out, each with a reason. Also the cast per act, the opening correction, the terms card, what the film adds that no source has, and the cut line.
**Why.** Bear split a seven-hour course and a short intro into films of at most 15 minutes, preferably about 10 (2026-10-13). A split only works if every idea has a home; this file is the record that nothing was dropped silently.
**Found.** Four acts, 38 body beats, about 9.6 minutes by the lint's formula (1,685 words). Everything in the brief's four suggested acts is covered except two items the brief itself marks as the cut line (the pixelated circle, the foam line) and the overlay blend, which does not exist in Godot's shading language. Five source claims were corrected, and eight things in the film are in neither source (list below), all run on Godot 4.7.2 before they were written down.

## The two sources (third party; nothing copied)

- **A. The canvas part of a long course on 2D shaders in Godot** (about 19 minutes in the brief's account; creator not named in the text Bear pasted). The brief's description, not the transcript, is what this layout worked from.
- **B. The water section of the short introduction to Godot shaders** (about 2 minutes of its 8; creator not named). Held back from the first film of the series for this one.
- Primary sources for every claim: the Godot 4.7 documentation (pages in `SOURCES.md`) and runs on Godot 4.7.2.

## Coverage

| Source and part (the brief's wording) | Where it goes | Note |
|---|---|---|
| Canvas intro: a scene that reads `SCREEN_UV` and `VERTEX` colours | **Act I**, B07 to B09 (`SCREEN_UV`); `VERTEX` in the fragment stage **LEFT OUT** | The film teaches the screen address; `VERTEX` as a screen position belongs with the coordinate spaces |
| "Four ways to get a pixel's screen position" | **MOVED** to *Local, World and Screen Space* | Its brief tests the four against each other with a moving camera |
| Screen texture with `hint_screen_texture` inverts the background | **Act I**, B03 to B09 | The invert (B09) is exactly this; B03 is the smaller "vanishing rectangle" that comes first |
| A full game scene: top `CanvasLayer` + `ColorRect` with full-rect anchors | **Act II**, B11 to B13 | Verified; adds the mouse-filter catch (B13) |
| Grays out the island except a circle round the player | **Act II**, B14 to B20 | Rebuilt on the film's own meadow; weights for gray sourced (B14) |
| The circle is an ellipse until corrected with the ratio from `SCREEN_PIXEL_SIZE` | **Act II**, B18 and B19 | The explanation is CORRECTED: addresses run 0 to 1 on both axes whatever the proportions (measured 320 px against 180 px); the source's "fragments are stretched" idea is not used |
| Pixelates the circle with `floor(square_uv * pixel_size) / pixel_size` | **LEFT OUT** | The brief's own cut line; snapping coordinates is the subject of the film on patterns and pixelation |
| Short intro: waves added to `SCREEN_UV` | **Act III**, B21 to B24 and B29 | Built in steps: shift, sine of the row, time, amount |
| Mixing a water texture sampled with *different* UVs (or it looks fixed to the screen) | **Act III**, B26 | Same insight, shown without a texture: whichever address drives the waves decides whether they ride with the pool or stay on the screen (measured) |
| "Overlay" blending for a natural look | **LEFT OUT** | CORRECTED: Godot's shading language has no `overlay()`; a call fails with "No matching function found for: 'overlay'" (verify6 R3). The film tints with `mix` (B27) |
| A soft wavy top edge for the pool | **Act III**, B28 | `discard` above a sine of the pool's own address |
| A foam line | **LEFT OUT** | The brief's own cut line; it is the same trick as the top edge shifted down |
| Act 4 of the brief: the screen texture holds what was drawn before this node | **Act IV**, B30 and B31 | CORRECTED: it holds what was drawn before the **first reading node on the layer**; later readers on that layer reuse it (B30 to B33) |
| Overlapping screen-reading shaders: the second does not see the first (docs) | **Act IV**, B32 and B33 | Shown with two flipping windows, then fixed with `BackBufferCopy` (copy mode Viewport) |
| `repeat_disable`, `filter_nearest` hints | **Act IV**, B36 (and the mipmap filter in **Act III**, B25) | `repeat_disable` clamps to the edge pixel in both renderers; `filter_nearest` is obeyed in Forward+ and ignored for the screen texture in Compatibility, so B36 says which renderer obeys (a first draft claimed it for both: FACTCHECK row 76) |
| Why full-screen effects belong on a top `CanvasLayer` | **Act IV**, B34 and B35 | A layer takes its own copy (CORRECTED against the docs' blanket statement), and a higher layer is untouched |
| `SCREEN_TEXTURE` is gone in Godot 4 | **Act I**, B10 | The engine's real message is the picture |
| `BackBufferCopy` masks, a reflection under a character | **MOVED** to *Reflections* | Not duplicated: here `BackBufferCopy` is only the fix for a stale copy |
| `SubViewport` | **MOVED** to *SubViewports* | The capture route uses one, but the film never teaches it |

## Corrections to the sources (full detail in FACTCHECK.md)

1. The screen texture holds "everything up to this node": it holds everything drawn before the first reading node **on that layer**, and later readers on that layer reuse it (rows 55, 58, 59 and 73).
2. "Overlay" blend: there is no built-in `overlay()` (row 70).
3. The oval: not about fragments against pixels; addresses run 0 to 1 on both axes (rows 37 and 71).
4. A new `CanvasLayer` starts with a fresh copy, so a full-screen filter above a shader-drawn pool needs no `BackBufferCopy` (rows 61 and 73). The docs' text, and Bear's chapter that quotes it, say the second shader never sees the first without qualification.
5. The game-side line: plain `position / screen size` puts the circle on the world position, not the screen position, once a `Camera2D` has moved (rows 41 and 74). The film shows the canvas-transform form.

## Added: in neither source (each is checked, FACTCHECK.md)

1. The miniature (`UV` against `SCREEN_UV`) as a picture of the wrong address (B08) and as an X-ray lens of what the copy holds (B31).
2. A full-screen color rect swallows mouse clicks unless its mouse filter is Ignore (B13).
3. The oval measured in pixels, and the fix measured (B18, B19).
4. Frosted glass from a mipmap filter and `textureLod` (B25).
5. Ripples that ride with a window or stay on the screen, measured (B26).
6. Back Buffer Copy: Viewport mode fixes the overlap; the default Rect mode does not (B33).
7. A layer takes its own copy; a layer above the filter is untouched (B34, B35).
8. Four renderer facts found by running both renderers, so that nothing is claimed for both that holds in one: repeat enable wraps in Forward+ and not in Compatibility; filter nearest gives a hard edge in Forward+ and is ignored for the screen texture in Compatibility (the one difference B36 says aloud); a texture read with no filter hint is blurred at a higher level in Compatibility and not in Forward+; the blur at the same level is stronger in Forward+; everything else in the film behaved the same in both.

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I A Copy of the Screen | the meadow (green checker, sand path, flowers, trees); **the window**: a 16:9 rectangle in a cream frame; the screen texture drawn as a copy of the meadow |
| II Full-Screen Effects | the meadow; the teal player (the series' test sprite); the full-window filter; the layer stack (two panes) |
| III Bend What Is Behind | the meadow; windows in cream frames; the pool (blue, wavy top edge) |
| IV What It Can See | the meadow; the same windows; the lens (a miniature window); the mustard and violet blocks; the player, the pool, the filter and the health bar together |

## Opening correction and terms

- **BIDEA**: the writer types "A shader only knows its own sprite." and replaces "its own sprite" with "what is already on screen".
- **BDEFS** (prerequisites only): Texture, UV, Uniform, fragment(), Draw order, Post-processing. The terms this film exists to teach (screen texture, hint, sampler2D, screen UV, swizzle, canvas layer, Full Rect, mix, dot, distance, screen pixel size, sine, mipmap, Back Buffer Copy) are earned in their acts, each defined on screen where first spoken, in the GLOSSARY's wording where it has one (new wording is listed in the report).

## Cut line

If the film runs long, cut in this order: the symptom table (B38), the finale (B37), the mouse-filter beat (B13), the edge-and-filter beat (B36) and the frosted-glass beat (B25). The window (B03 to B09), the spotlight with its oval fix (B16 to B20), the pool (B27 to B29) and the overlap with its fix (B32, B33) stay: they carry the idea. Current estimate about 9.4 minutes, so no cut is needed.
