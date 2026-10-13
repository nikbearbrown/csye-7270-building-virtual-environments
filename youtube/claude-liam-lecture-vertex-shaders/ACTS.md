# Acts and coverage map: Vertex Shaders

**What this is.** How this film is built from its brief and the third-party course behind it: which part lands in which act, which parts belong to another film or are left out (each with a reason), the cast per act, the opening correction, the terms the film earns and where each is defined on screen, the additions that are in neither the brief nor the source, and the cut line.
**Why.** Bear split a long third-party course into films of at most 15 minutes, preferably about 10 (2026-10-13). A split only works if every idea has a home; this file is the record that nothing was dropped silently.
**Found.** Five acts, 40 body beats, about 9.8 minutes. Everything the brief asks of this film is covered except the cosine on x and the "incline" term (left out: neither is needed to teach the idea) and the Polygon2D border artifact (moved to the UV film: it is a UV-border problem). Twelve things in the film are in neither the brief nor the source (list below); each was run, not read. No source claim needed correcting; one docs sentence and one brief detail did (below).

## The source (third-party; nothing copied)

A long third-party course on 2D shaders in Godot. About 40 minutes of it bear on this film: basic vertex work, variables (the `varying` chapter), the vertex chapter and the flag. The creator is not named in the material Bear passed on. The brief paraphrases it; nothing was copied; every demonstration was rebuilt and run (see `SOURCES.md`).

## Coverage

| Brief or source item | Where it goes | Note |
|---|---|---|
| The one idea: `vertex()` can only move the vertices that exist; four corners give straight edges | **Act I** B10, **Act II** B11 to B13 | Shown as a real tilt beside a real ripple (B12, B17), not only said |
| Vertex output `VERTEX`; moving it with add and multiply | **Act I** B03 to B07 | Added: VERTEX is local, so a scaled node moves farther (B06) |
| Slanting with `UV.y`; `UV` is 0 to 1, `VERTEX` is pixels | **Act I** B04, B08, B09 | Both numberings on one square (B08) |
| `VERTEX` in the fragment stage means something else | **Act V** B36, B37 | Docs table plus a moving two-square demonstration |
| `Sprite2D` is four vertices | **Act II** B12, B13; **Act V** B40 | Proved with `VERTEX_ID` (0 to 3), FACTCHECK 24 |
| `MeshInstance2D` with a subdivided `QuadMesh` (the brief says about 100 by 100) | **Act II** B15 to B19 | The film cuts the flag 31 by 7 (297 vertices) and shows why rows are not needed (B19) |
| The mesh size trick (negative y in 2D) | **Act V** B35 | Confirmed by a run (FACTCHECK 60) |
| `Polygon2D` with hand-placed points | **Act II** B14, B20; **Act V** B38 | Added: what outline-only points do, and that UV needs a texture |
| Passing `VERTEX` through a `varying` to see the interpolated gradient | **Act IV** B28 to B30 | Shown with four corner colours (exact at the middle of an edge); `VERTEX` through a varying also appears in B37 |
| `VERTEX` in fragment as screen position with `SCREEN_PIXEL_SIZE` | **Act V** B36, B37 | The film uses the window width as a constant; `SCREEN_PIXEL_SIZE` and the other three ways to get a screen position are left to the film on spaces |
| The flag: sine of `UV.x * frequency - TIME * speed` times amplitude times `UV.x`, uniforms for each knob | **Act III** B21 to B26 | Built in the order ripple, travel, pin, dials; the travel step is shown by switching a real flag from static to moving |
| A cosine on x (cloth bunching) | **LEFT OUT** | Aesthetic only; adds no idea; the film needs the room for the pitfalls |
| An "incline" term | **LEFT OUT** | Named in the brief's cut line; not needed to teach the idea |
| Clipping repeated border pixels on a `Polygon2D` with `step` on `UV` | **MOVED** to *UV Space* | The border artifact is a UV-outside-0-to-1 problem, which that film teaches; the flag here never leaves 0 to 1. It exists and the four-step fix works (checked for the record, FACTCHECK 74) |
| Color from the vertex (`COLOR` in `vertex()`) | **Act IV** B31, B33 | Folded in as the shorter way to light the flag; "assigning replaces the tint" is verified (FACTCHECK 75) but not spoken |
| Waves in the fragment stage | **MOVED** to *Time and Waves* | The brief assigns it there |
| Matrices applied to `VERTEX` | **MOVED** to *Matrices and Fake 3D* | The brief assigns it there |
| World position from `MODEL_MATRIX` | **MOVED** to *Local, World and Screen Space* | The brief assigns it there |

## Corrections and findings to report

- **Docs sentence corrected for 2D (FACTCHECK 28).** The class reference words `subdivide_depth` as "along the Z axis"; for a `QuadMesh` drawn in 2D it cuts the vertical direction. The film says "across and down".
- **Brief detail corrected.** The brief's `BIDEA_TEXT` puts a line break inside the trigger phrase (`"A vertex shader changes\npixels."`, trigger `"changes pixels"`), so the trigger is not verbatim in the text and the correction would never fire. The film uses `"A vertex shader\nchanges pixels."` with the same trigger and replacement.
- **A finding the film does not show.** A varying set in `fragment()` and read in `vertex()` is accepted by Godot's own parser and then fails in the generated vertex shader with `'m_v' : undeclared identifier` (FACTCHECK 50). Real, but not a message a viewer should have to read, so the film states the one-way rule from the docs.

## Added: in neither the brief nor the source (each checked, FACTCHECK.md)

1. VERTEX is local: the same forty moves a node scaled to twice its size eighty pixels (B06; row 12).
2. A ripple on four vertices only tilts, as a real run beside the 297-vertex mesh (B12, B17; rows 22, 32).
3. How many pieces a wave needs: worst gap 1 minus cos(pi over pieces per wave), measured on real flags (B18; rows 33, 34).
4. Cut only where it bends: 297 vertices and 66 draw the same picture, pixel for pixel (B19; row 35).
5. What a Polygon2D with outline points only really does: 64 long thin triangles and a twisted picture; a grid with its cell list fixes it (B20; rows 37, 38).
6. `flat` shows that a rectangle is two triangles and that blending happens inside each one (B30; rows 52, 53).
7. A varying is only as detailed as the corners: six stripes vanish on four corners (B34; row 59).
8. A Polygon2D has no UV without a texture (B38; row 64).
9. A vertex shader changes the drawing, not the node: the rectangle and the collision shape stay put (B39; row 66).
10. Count your vertices: the one-line print and the number it gives (B40; row 68).
11. Unpinned against pinned on a real flag, switched live (B21, B22; rows 40, 42).
12. The color shortcut draws the same picture as the explicit varying, pixel for pixel (B33; row 58).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I Corners | the 128 px checker square; its four terracotta corner dots (Manim); the same square as the real Godot sprite in every capture |
| II More Corners | the cream and teal checker flag (384 by 168, 16 by 7 cells), as a four-vertex sprite and as the 297-vertex mesh; the sine curve with its vertex dots; the terracotta dot grid |
| III A Waving Flag | the mesh flag on its grey pole (the same recording serves the hook, the dials and the read-through) |
| IV Passing Data Forward | the four-corner square blended from four colours; the mesh flag on its pole; the three-stage strip (vertex, fill, fragment) |
| V When It Looks Wrong | the blob with two eyes (sprite beside quad mesh); the sprite on its screen frame; the node's grey outline |

## Opening correction and terms

- **BIDEA**: the writer types "A vertex shader changes pixels." and replaces "changes pixels" with "moves corners".
- **BDEFS** (prerequisites only): Shader, Pixel, Vertex, Polygon, Interpolate. The terms this film exists to teach are earned in their acts and defined on screen where first spoken (GLOSSARY wording where the glossary has one):

| Term | Beat | On-screen definition |
|---|---|---|
| `vertex()` | B02 | vertex(): runs once for each vertex; places the corners (GLOSSARY) |
| built-in | B03 | built-in: a value the engine hands to a function (GLOSSARY) |
| `UV` | B08 | UV: a point's address on the shape: 0 to 1 across, 0 to 1 down (GLOSSARY) |
| sine | B12 | sine: a smooth wave between -1 and 1 (not in the GLOSSARY; the math film owns it) |
| mesh | B14 | mesh: the vertices and triangles that make a shape (GLOSSARY) |
| `TIME` | B21 | TIME: seconds on one clock shared by the whole game (GLOSSARY) |
| uniform | B23 | uniform: a value your game sets from outside; every pixel sees the same one (GLOSSARY) |
| amplitude, frequency, speed | B24 | how tall / how many waves fit / how fast (plain words beside each sweep) |
| `fragment()` | B27 | fragment(): runs once for each pixel the shape covers; sets its color (GLOSSARY) |
| varying | B28 | varying: a value set at each corner, blended across the shape for fragment() to read (GLOSSARY) |
| flat | B30 | flat: the value is not blended (docs wording) |
| `COLOR` | B31 | COLOR: the color being drawn (GLOSSARY, shortened) |
| slope | B32 | slope: how steeply a line rises: up divided by across (GLOSSARY, a small math word), plus a cue tag on the code lines: phase: where the wave is, fold: how the cloth slopes |
| texture | B38 | texture: an image a shader can read (GLOSSARY) |
| collision shape | B39 | collision shape: what physics collides with (plain words; a game term, not a shader term) |

## Cut line

If the film runs long, cut in this order: the color-shortcut beat (B33), the flat beat (B30), the wind beat (B25), the polygon-needs-a-texture beat (B38), the upside-down beat (B35). Each repeats a lesson another beat carries or is a trap rather than the main line. The four-corner tilt (B12), the pair (B17), the travelling and pinned flag (B21, B22) and the lit flag (B32) stay: they are the proof and the payoff. Current estimate: about 9.8 minutes, so no cut is needed. (If B33 goes, the opening flag still shows the lit look: the narration there only says the corners move.)
