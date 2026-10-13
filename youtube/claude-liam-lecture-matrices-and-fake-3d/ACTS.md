# Acts and coverage map: Matrices and Fake 3D

**What this is.** How the film is built from its brief (which summarises a third-party video course on matrices and fake 3D in Godot shaders): which brief item lands in which beat, what is left out and why, the cast per act, the opening correction and terms, the additions that are in neither, and the cut line.
**Why.** A film of at most 15 minutes, preferably about 10, only works if every idea has a home. This file is the record that nothing was dropped silently.
**Found.** Five acts, 41 body beats, about 10 minutes (about 1,785 spoken words with the bookends; the lint's ceiling estimate is 10.2). The brief suggested four acts; the "Three Moves" act became two (the three moves, then combining them) so that no act passes ten beats. Every brief item is covered. Three things in the brief were corrected (the order of the product, the 64-pixel edge, the opening line's break) and one source claim ("it looks like 3D") is answered honestly. Ten things in the film are in neither the brief nor the source, each checked.

## The source (third-party; nothing copied)

A video course on matrices and fake 3D in Godot shaders, about 27 minutes of it in the brief's account (matrix arithmetic, then fake 3D). Its creator is not named in anything this session received, and this session received only the brief's description of it, not its transcript. Nothing of it is stored or copied; the brief's account is paraphrased in the table below.

## Coverage

| Brief item | Where it goes | Note |
|---|---|---|
| A 2x2 matrix times a vector: each output number is a row times the vector | **Act I**, B02 | A ring walks down the rows |
| The five-and-six example, result 23 and 34, arithmetic shown | **Act I**, B02, B03 | The table is 1 3 over 2 4, the film's own choice so that the product is 23 and 34; a shader checks it (teal) |
| Identity matrices | **Act I**, B08 (2x2); the 3x3 is shown as the padding in B19 | The 3x3 identity is not named: no beat needs the name |
| In Godot a matrix is built from columns | **Act I**, B04 to B07 | Four beats on purpose: code against paper, the docs, the two wrong answers (17, 39), and why columns make sense |
| Translation needs one more number: a 3x3 and (x, y, 1) | **Act II**, B14 to B16 | The film says first that a 2x2 cannot slide, then the one, then the shader |
| Scale along the diagonal | **Act I** B09 (as arrows), **Act II** B11 (in the shader), B17 (in the table) | |
| Rotation (cos, sin) | **Act II**, B12, B13 | Sine and cosine get one sentence and an on-screen gloss; their own film covers them properly |
| Apply each in `vertex()` to `VERTEX` | **Act II**, B11, B13, B16 | `vertex()` and `VERTEX` are defined where first used (B11) because the viewer may know no other film |
| Combine by multiplying (translate * scale * rotate * v) | **Act III**, B18 to B24 | CORRECTED: the film writes slide * turn * scale (scale nearest the point). With a uniform scale both orders give the same picture (FACTCHECK, B24), with a non-uniform scale they do not |
| Show that swapping the order changes the result | **Act III**, B22, B23 | Two real renders ending in two places, then why (a turn swings round the origin) |
| Rotation about x, y and z (the three 3x3 matrices) | **Act IV**, B28 (y), B30 (x and z), B31 (two at once) | The film also says plainly that one axis alone is only a squeeze of one dimension |
| A full turn is `TAU` | **Act II** B13 (defined), **Act IV** B34 (used) | |
| Apply to `VERTEX` in `vertex()`; a card that flips | **Act I** B01 (hook), **Act IV**, B28, B29, B34 | |
| Be honest: no perspective or depth; right for a card, not for a box | **Act IV**, B32, B33 | Measured: both edges of a turned card stay 128 px tall |
| Pivot: translate by minus the pivot, rotate, translate back | **Act V**, B35 to B37, B40 | B37 shows it as a product of three tables (two-D); B40 as subtract, turn, add (the flip table is three-D) |
| A pivot uniform in pixels (for a 128-pixel sprite, 64 is the right edge) | **Act V**, B39 | CORRECTED: 64 only for a centered sprite; with centered off the right edge is 128 |
| Rotate about a corner | **Act V**, B38 | |
| Source claim: column versus row layout (translation in the third column) | B04 to B06, B15, B16 | PASS (docs and probes) |
| Source claim: y pointing down changes which way a positive rotation turns | B13 | PASS: positive is clockwise on screen; pixel-identical to `Node2D.rotation` |
| Source claim: the result looks like 3D | B32, B33 | CORRECTED: it has no perspective or depth |
| Facts to verify (docs, Lab) | `FACTCHECK.md`, `evidence/planning-checks/` | 76 rows, 61 Lab checks with negative controls |
| Captures | `CAPTURE-PLAN.md` | Fifteen Lab renders and one docs screenshot; no editor frames |
| Cut line: the order-swap beat, z rotation | Named below | |

### Left out, with reasons

- **The named 3x3 identity.** The 2x2 identity carries the idea; B19 shows the 3x3's padding (zeros and a one).
- **Non-uniform scale and shear.** Not in the brief; a non-uniform scale appears only as a FACTCHECK row that justifies the order scale, turn, slide.
- **`MODEL_MATRIX`, world and screen space.** Another film (spaces).
- **Perspective, `mat4`, real three-D.** This film is about the fake; the film says what is missing.
- **A different picture on the back of the card.** Needs a second texture; the film says the back is the front mirrored.
- **Tweening the flip from GDScript.** About uniforms and tweens, not matrices; B34 says only that the game sets the uniform (verified: `set_shader_parameter`).
- **The Inspector and editor frames.** Nothing here depends on the editor; no editor claims are made.
- **Transpose and inverse.** `transpose` appears in the evidence only (a check that rows give (17, 39)).
- **Degrees and `radians()`.** The film uses radians and the 0-to-1 `flip` times `TAU`; the converter exists (docs) and is not needed.
- **Promotional framing of the source.** Nothing to teach.

## Added: in neither the brief nor the source (each checked in FACTCHECK.md)

1. Reading the table as rows and writing the point on the left both give (17, 39): the same plausible wrong answer, no error (B06).
2. The real compiler message for mixed sizes, and `mat3(mat2)` doing the padding (B19).
3. A slide alone is simpler as plain addition; tables pay off when moves combine (B18).
4. The slide stays exactly as long as asked when it goes last in the product (B24).
5. The two ways to be wrong about the third number: the one for sliding and depth for turning cannot be mixed (B26, B40).
6. A card with no thickness draws nothing at a quarter turn, and past it you see the front mirrored (B29).
7. Two turns multiplied make a slanted parallelogram: one turn alone is only a squeeze (B31).
8. The top view: the turn as a shadow on the screen line, and what a box would show (B27, B33).
9. The measured no-perspective test: both edges 128 px at an eighth of a turn (B32).
10. Centered or not: where the origin is, and so which number is the right edge (B39).

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I A Table That Moves Points | the table (a bracketed grid) and the point (a bracketed column); the across arrow (solid) and the down arrow (dashed) on a grid with y pointing down; the unit square; the test rectangle with four terracotta corner dots; in captures, the card (B01) and the teal swatch (B03) |
| II Three Moves | the card in Godot with a grey cross at its origin; the two arrows and the grey circle of radius one (B12); the pinned origin dot (B14); the three-by-three table with the slide in its last column |
| III Moves Together | three small tables merging into one; the card (small, in Manim; real, in the captures) and the origin cross; the token that travels right to left (B21) |
| IV Fake 3D | the flat card with its third number; the top view (screen line, end-on axis marker, a turning segment, shadow dots); three small cards (B30); the real card turning in the captures |
| V The Pivot | the card with the terracotta hinge dot; the origin cross; the two rulers (B39) |

The card, in every capture: a cream card with a warm grey border, a teal arrow pointing right and a small teal square in its top left corner (asymmetric on purpose, so a mirror is visible), drawn at 1024 px so it stays crisp at 4K. It is not on the series' cast list (ramp strip, test rectangle, pixel grid, test sprite) because a flip needs a picture with a front and a back; its colours are the test sprite's (teal and cream) and it sits on the Lab's warm light-grey stage.

## Opening correction and terms

- **BIDEA**: the writer types "A matrix is / advanced math you can skip." and replaces "advanced math you can skip" with "a saved move" (the brief's line break fell inside the trigger, so the text is re-broken; FACTCHECK).
- **BDEFS** (prerequisites only): Vector, Matrix, Vertex, Uniform, Radian (the series glossary's wording for vector, vertex, uniform and radians). The brief suggested Matrix, Vector, Rotation, Pivot. Rotation is plain English; Pivot is the idea Act V earns and is defined on screen there; Vertex, Uniform and Radian are added because the viewer may have seen no other film and the code uses all three. What the film exists to teach (what a matrix does, columns, scale, turn, slide, product, order, the flip, the pivot) arrives in its acts, defined on screen where first spoken.

## Cut line

If the film runs long, cut in this order: the order-swap pair (B22, B23: the render of two orders and the reason), the corner spin (B38), the two-turns beat (B31) and the card-versus-box beat (B33). Each repeats an idea another beat already carries (order: B21 and B36; the pivot: B35 and B41; the honest limit: B32). The columns trio (B04 to B06), the product-order beat (B21), the flip itself (B28, B29) and the door (B35, B41) stay: they are the stumbling blocks and the payoff. Estimated about 10 minutes, so no cut is needed; the four beats together are about a minute.

## Open for Bear

1. **The source course's creator** (and a link, if you want it credited in the description). Nothing in the film names it.
2. **The playlist name** (none yet; the opening card says only the title).
3. **How the voice says "tau"** and the title. The title is "Matrices and Fake 3D" on every screen; the voice reads `SPOKEN_TITLE`, "Matrices and Fake Three D", in the opening beat and the outro. The build session reports how both sound.
