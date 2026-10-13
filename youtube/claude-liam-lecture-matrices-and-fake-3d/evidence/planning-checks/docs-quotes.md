# Godot 4.7 documentation: the sentences this film leans on

**What this is.** Short excerpts from the five Godot documentation pages the film's claims rest on, with the address of each page and the date it was read, so every "the docs say" in `FACTCHECK.md` can be found again.
**Why.** Bear's rule: Godot behaviour is verified against the 4.7 docs or by running it. Where the docs speak, they are quoted here; where they are silent or loose, the claim is checked by a run instead (see `RESULTS.md`).
**Found.** The docs state the column rule, the identity, the clockwise turn, the order rule and `TAU`, but only on the pages named below: `TAU`, `PI` and `E` are in the "Global built-ins" table of each shader type page, not in the shading-language or built-in-functions pages. The docs do not say how a uniform shows in the Inspector (not claimed by this film).

All pages read on **2026-10-13** at `docs.godotengine.org/en/stable` (Godot 4.7). The pages were fetched with the session's fetch tool, which returns a model-assisted extract; the quotes below are the excerpts it returned (each at most one sentence or two short ones, all in the CC BY 3.0 licensed documentation, attribution: Godot Engine documentation). Nothing that matters rests on a quote alone: each claim is also measured (`geometry-summary.txt`, `verify*.gd`).

## Shading language: `tutorials/shaders/shader_reference/shading_language.html`

- Matrix types: "2x2 matrix, in column major order." and "3x3 matrix, in column major order."
- "Construction of matrix types requires vectors of the same dimension as the matrix, interpreted as columns." (section: Data types, Constructing)
- "You can also build a diagonal matrix using `matx(float)` syntax." followed by "Accordingly, `mat4(1.0)` is an identity matrix."
- Building from another size: "Matrices can also be built from a matrix of another dimension." and the rule that "the additional rows and columns are set to the values they would have in an identity matrix."
- Operators: "The exceptions are matrix multiplied by vector, vector multiplied by matrix, and matrix multiplied by matrix." and "These do not operate component-wise, but rather perform the correct linear algebraic multiply."
- Indexing: "For matrices, use the `m[column][row]` indexing syntax to access each scalar," "or `m[column]` to access a vector by column index."
- "Godot uses a shading language similar to GLSL ES 3.0."

## Built-in shader functions: `tutorials/shaders/shader_reference/shader_functions.html`

- radians: "Converts a quantity specified in degrees into radians, with the formula `degrees * (PI / 180)`."
- transpose: "Calculate the transpose of a matrix."
- (The page does not list `PI`, `TAU` or `E`; the formula above uses `PI`.)

## Canvas item shaders: `tutorials/shaders/shader_reference/canvas_item_shader.html`

- "Global built-ins are available everywhere, including custom functions."
- `PI`: "A `PI` constant (`3.141592`)." and "the number of radians in a half turn."
- `TAU`: "A `TAU` constant (`6.283185`). Equivalent to `PI * 2` and the number of radians in a full turn."
- vertex(), `VERTEX` (`inout vec2`): "Vertex position, in local space."
- "Vertex data (`VERTEX`) is presented in local space (pixel coordinates, relative to the Node2D's origin)."
- fragment(), `VERTEX`: "Pixel position in screen space." (a different thing: this film uses `VERTEX` only inside `vertex()`)
- `MODEL_MATRIX` (`in mat4`): "Local space to world space transform." (not used; another film)

## Introduction to shaders: `tutorials/shaders/introduction_to_shaders.html`

- "The `vertex()` function runs over all the vertices in the mesh and sets their positions and some other per-vertex variables."
- "The `fragment()` function runs for every pixel covered by the mesh."

## Matrices and transforms: `tutorials/math/matrices_and_transforms.html`

- "Fun fact: In addition to Y being down in Godot, rotation is represented clockwise."
- "Godot represents all rotations with radians, not degrees."
- "When multiplying matrices, order matters! Don't mix them up."
- "In the image above, we can see that the red X vector is represented by the first column of the matrix, and the green Y vector is likewise represented by the second column."
- "The identity matrix represents a transform with no translation, no rotation, and no scale."
- "Transform2D actually has three Vector2 values: x, y, and origin."
