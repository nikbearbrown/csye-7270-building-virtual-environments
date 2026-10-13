# Brief: Matrices and Fake 3D

**What this is.** The content brief for the film that treats a matrix as a saved move (translate, scale, rotate), combines moves by multiplying, and uses rotation matrices to flip a 2D sprite like a card. Slug `matrices-and-fake-3d`, folder `claude-liam-lecture-matrices-and-fake-3d`, group Vertex and space, target about 10 to 11 minutes (ceiling 15). Title lines: `["Matrices and", "Fake 3D"]`.
**Why.** Matrices are the part newcomers skip and then meet in every transform. The source makes them approachable ("just a lot of simple arithmetic"); the series keeps that tone and adds a picture of what each matrix does.
**Found.** About 27 minutes of source (matrix math, then fake 3D). Godot builds matrices from **columns**, which is the usual stumbling block; the docs say so.

## The one idea

A matrix is a table that moves a point. Multiply the matrix by a vector and you apply the move. Multiply two matrices and you get one move that does both. The identity matrix is "do nothing". Order matters.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("A matrix is\nadvanced math you can skip.", "advanced math you can skip", "a saved move")` (the first draft broke a line inside its own trigger; the layout used this form).

## Prerequisites for the terms card

**Matrix**, **Vector** (recap), **Rotation**, **Pivot** (the point something turns around). 17 characters or fewer.

## Suggested acts

1. **A Table That Moves Points.** A 2×2 matrix times a vector: each output number is a row times the vector; work the source's 5 and 6 example (result 23 and 34) with the arithmetic shown; the identity matrix changes nothing. In Godot a matrix is built from **columns**: `mat2(vec2 col0, vec2 col1)` (docs).
2. **Three Moves.** Translation needs one more number: use a `mat3` and a vector `(x, y, 1)`; scale; rotation (`cos`, `sin`); apply each in `vertex()` to `VERTEX`; combine by multiplying (`translate * scale * rotate * v`); show that swapping the order changes the result.
3. **Fake 3D.** Rotation about x, y and z (the three 3×3 matrices); full turn is `TAU`; apply to `VERTEX` in `vertex()`; a card that flips. Be honest: it is a rotation of a flat shape with no perspective or depth, so it looks right for a card, not for a box.
4. **Pivot (payoff).** Translate by minus the pivot, rotate, translate back; a pivot uniform in pixels (for a 128-pixel sprite, 64 is the right edge); rotate about a corner.

## What the source does (my words)

- Introduces matrix-vector multiplication on a `2×2`, identity matrices for 2 and 3, translation by embedding in a 3×3 with the vector `(x, y, 1)` and the offset in the last column, scale along the diagonal, the rotation matrix; builds `mat3(vec3(1,0,0), vec3(0,1,0), vec3(x_offset, y_offset, 1))`; says each `vec3` is a column; combines `translation * scale * rotation`; for fake 3D builds the three rotation matrices, multiplies by `TAU` for full turns, and the pivot (translate–rotate–translate) with a `pivot` uniform.

## Source claims to check or correct

- Column versus row layout: confirm with the docs and a probe that the translation lives in the third *column*.
- That the 2D y axis points down changes which way a positive rotation turns: verify in the Lab.
- That the result "looks like 3D": it has no perspective; say so.

## Facts to verify

Docs: matrix types and constructors (column-major), `mat3 * vec3`, `TAU`. Lab: the 5-and-6 example evaluated in a shader (render the result as a color, probe it); translate/scale/rotate on the test sprite (measure the corner positions in the PNG); the order-swap difference (two renders); a flip about the y axis and a pivot rotation.

## Captures

Lab sprite renders in `vertex()`: a translate/scale/rotate sweep video; the card flip; the pivot demo.

## Cut line

The order-swap beat; z rotation.

## Other films cover

Spaces and `MODEL_MATRIX`: spaces film; `sin`/`cos`: trigonometry film; vertices: vertex film.
