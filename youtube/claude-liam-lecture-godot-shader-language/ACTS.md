# Acts and coverage map: Godot Shader Language

**What this is.** How this film is built from its brief and from the long third-party shader course the brief describes: which part lands in which act, which parts are left out and why, the cast per act, the opening correction, the terms card, what is added that no source has, and the cut line.
**Why.** Bear split a seven-hour course into films of at most 15 minutes, preferably about 10 (2026-10-13). A split only works if every idea has a home. This file is the record that nothing was dropped silently, and that nothing was copied.
**Found.** Five acts, 41 body beats, about 10.9 minutes by the lint's cautious estimate (1,910 spoken words). Everything in the brief's five suggested acts is covered. Three claims in the brief were checked and changed: custom functions can see four built-ins (TIME, PI, TAU, E), not none; the documentation does say something about branches and speed; and the documentation's own `vec3 + 2` example does not compile. Five things are in the film that the brief did not list (below).

## The sources (both third-party; nothing copied)

- **The brief** (`../_godot-shaders-series/briefs/godot-shader-language.md`), which describes in the brief author's words what a long third-party course says about variables, shader code, functions, outlines and loops. The course's creator is not named in the text Bear gave; its wording is not stored anywhere and none of it is used.
- **The Godot 4.7 documentation and the installed Godot 4.7.2** (the primary sources; see `SOURCES.md`). Every behavior in the film was run, and every engine message on screen is quoted from a run.

## Coverage of the brief

| Brief item | Where it goes | Note |
|---|---|---|
| Act 1 picture: one real 14-line shader as horizontal bands with labels | **Act I**, B01 and B02 | B01 shows the file beside its live result; B02 labels the three bands. The same file returns in Act V, so the film ends by reading what it opened with |
| Header: `shader_type`, optional `render_mode` | **Act I**, B03 | Docs: first line; render mode on the second line. One blend example, run (`blend_add`) |
| Globals: `uniform`, `const`, `varying` | **Act I**, B04 | One sentence each, GLOSSARY wording on screen; declare-above rule run for all three |
| Functions zone and the processor functions | **Act I**, B05 | `vertex`, `fragment`, `light` defined in a table; the film uses `fragment` |
| Statements end in semicolons; braces group | **Act I**, B06 | The engine's own log, including the fact that it points at the next line |
| Indentation is only for people | **Act I**, B07 | One shader in three spellings, pixel-identical (0 of 230,400 pixels differ) |
| `//` and `/* */` comments | **Act I**, B08 | Commenting a line out changes the picture; every pixel differs |
| Names are case-sensitive | **Act I**, B09 | `level` against `Level`, run. Joined with "Godot's names are its own" (`gl_FragColor` is `COLOR`) |
| `float`, `int`, `bool` | **Act II**, B10 | Plus `sampler2D` as the type of a texture, and the shape of a declaration |
| `vec2`, `vec3`, `vec4`; colors are `vec4` | **Act II**, B12 | Also that a texture lookup returns a `vec4` (run) |
| Constructors (`vec4(1.0)`, `vec4(rgb, 1.0)`) | **Act II**, B13 | `vec3(0.5)` is used for the fill rule instead of `vec4(1.0)` (see "Choices") |
| Swizzles (`.rgb`, `.xyz`, `.st`; any order; never mixing sets) | **Act II**, B16 and B17 | `.bgr` on a real picture; the three letter sets named; the mixing error run |
| Component-wise arithmetic (`vec3 * 2.0`, `vec3 * vec3`) | **Act II**, B14 and B15 | Numbers from the Lab; used on `UV` to make a pastel gradient |
| Strict typing: `1` is an int, `1.0` a float; show the real error | **Act II**, B11 (and B18, B30) | The engine's log, twice in one window; a `vec3` into `COLOR` (B18); `float(i)` (B30) |
| Return type, name, parameters | **Act III**, B20 | Signature bracketed; "argument" is a prerequisite term |
| Qualifiers `in`, `out`, `inout`, `const` | **Act III**, B25 | `in`, `inout`, `out` run (a copy, the original, a write-back). The `const` qualifier is **left out** (rare in effects; one extra mode to explain) |
| A function must be defined above its caller | **Act III**, B22 | The engine's message does not mention order; the film says so |
| A function must return what it promises | **Act III**, B21 | Wrong type and missing return both run; one message shown |
| Built-ins inside your own functions (verify which) | **Act III**, B23 and B24 | **Corrected**: UV, COLOR, TEXTURE and others are unknown inside a function; TIME, PI, TAU, E are visible. Eleven built-ins tested |
| `if`/`else`, the ternary | **Act IV**, B28 and B29 | Condition must be a bool (run); scope ends at the closing brace (run); ternary pixel-identical to if/else |
| `for` | **Act IV**, B30 | Five stripes from one loop; the int counter needs `float(i)` (run) |
| `while`, infinite loops freeze the editor | **Act IV**, B31 | Documentation capture; not run (it would freeze the machine) |
| Do not compare floats with `==` | **Act IV**, B32 | `UV.x == 0.5` draws nothing in an even-width frame; a range draws a line; docs example `0.1 + 0.2 == 0.3` came out true here and is not used |
| `discard` has a documented cost; "if statements are slow" | **Act IV**, B33 | **Corrected**: the documentation's preprocessor page does discuss branches (see "Corrections") |
| Act 5: read a 10 to 14 line shader aloud by naming types | **Act V**, B34 to B41 | The 14-line `breathe` file from the opening; a tinted pulse with a function of its own, so every earlier act appears in it. Ends with a one-word change and the engine's refusal |
| Source: code shaders against node-graph (visual) shaders | **LEFT OUT** | The film is about reading text. The documentation says a visual shader graph "is converted to a script shader behind the scene"; that can be one line of the YouTube description |
| Source: `vec4(1.0)` is white | **Left out of the narration** | True (docs: a single scalar fills the whole vector), but a failing shader also shows white in the Lab, which would make the capture ambiguous; `vec3(0.5)` shows the same rule unambiguously |
| Source: red is `vec4(1.0, 0.0, 0.0, 1.0)` | **Left out** | The pilot of this set uses it; here B12 shows a teal `vec4` instead |
| Source: `hint_range(0, 1, 0.1)` start, end, step | **Left out** | Sliders belong to the film on uniforms and dials; B35 covers `source_color` only |
| Source: people write `1.` for a float | **Left out** | Allowed (run), but the shaders style guide asks for a digit on both sides; every shader here writes `1.0` |
| Source: `texture(sampler, UV)` and `TEXTURE` | **Act II**, B12 (one sentence) | A lookup returns a `vec4`; the rest belongs to the film on textures |
| Source: the circle moved into `create_circles(vec2 uv)`, discovering `UV` is unknown there | **Act III**, B23 and B24 | The same discovery with a gradient (`soften`) instead of a circle: circles belong to the shapes film |
| Source: nested `for` loops replace eight copied lines (outline chapter) | **Act IV**, B30 (the idea, on stripes) | The outline itself is another film's subject |
| Not in the brief: arrays, structs, matrices, `uint`/`ivec`/`bvec`, precision qualifiers, `switch`, `do while`, `#define`/`#if`, `instance` and `global` uniforms, uniform groups, documentation comments | **LEFT OUT** | Rare in 2D effects and each needs its own picture; the documentation covers them. Matrices are the one exception to "operators work on every part", and the film says "many", not "every" |

## Added: in the film, in neither the brief nor (as far as the brief says) the source

1. **Godot's names are its own** (B09): `gl_FragColor` is `COLOR`, run, with the documentation's migration table behind it.
2. **Overloading picks by type** (B27): `get_color(1)` and `get_color(1.0)` call different functions; run, from the documentation's own example, with new colors.
3. **Built-in functions have signatures too** (B26): the documentation lists them; `sin` is read as an example.
4. **Mismatches the engine names exactly** (B11, B18, B21, B22, B23, B41): five engine messages shown word for word.
5. **The one-word change** (B41): making `tint` a `vec3` while still reading `tint.a`, caught by reading and confirmed by the engine.

## Corrections to the brief and the docs (full detail in FACTCHECK.md)

| What was said | What the run or the documentation shows | Where it lands |
|---|---|---|
| Custom functions cannot see built-ins | They cannot see the per-pixel ones (UV, COLOR, TEXTURE and others); they can see the four global ones | B23, B24 |
| Only `discard` has a documented cost; do not say "if is slow" | The preprocessor page says modern GPUs handle "static" branching well and that too many branches can slow a shader down significantly | B33 |
| "Based on GLSL 3.0" | "Similar to GLSL ES 3.0" and simplified; Godot has its own names | B09 |
| The documentation's operator table: `vec3(4, 5, 6) + 2` | Godot 4.7.2 refuses `vec3 + int`; the table is shorthand | B11 (not repeated) |
| `in` means "only for reading" | Assigning to an `in` argument compiles; the change stays in the function's copy | B25 |
| The documentation's float-equality example, `0.1 + 0.2 == 0.3` | True on this Mac (the 32-bit sum is exactly 0.3); the film uses `UV.x == 0.5` | B32 |

## Choices

- **Teaching with `UV` and a pastel gradient** (not flat colors): operations on vectors are visible only if different pixels get different numbers. `0.4 + 0.6 * vec3(UV, 0.5)` keeps every channel between 0.41 and 0.99, so there is no near-black field for the type gate to mistake for text.
- **One file twice** (B01 and Act V): the film opens on the 14-line `breathe` shader and ends by reading it, so the promise ("by the end you can read every line") is kept on the same object.
- **Real engine logs, not drawings of errors.** The Lab's `check_shader.sh` prints only the `SHADER ERROR` line; the full log (a source excerpt with the offending line marked) comes from the same engine via `evidence/planning-checks/run-error-logs.sh`.

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I The Shape of a File | the 14-line `breathe` file in the code panel; the pastel gradient (real render); the engine log window |
| II Types and Vectors | the bundle: a row of outlined cells (1 to 4 cells); the pastel gradient and its colors-reversed twin; small type tags |
| III Your Own Functions | the `soften` function box with its signature; three-cell bundle tokens travelling in and out; the wall between `fragment()` and your function |
| IV Choices and Loops | the split picture (teal on the left, pale on the right); the five-stripe picture; the pixel row of the float-equality scene |
| V Read One Aloud | the `breathe` file, line by line (zoomed lines with type tags); the gray-to-teal ramp strip |

## Opening correction and terms

- **BIDEA**: the writer types "A shader line works on one number at a time." and replaces "one number" with "a bundle of numbers". (The brief proposed the break "works on one / number at a time", which splits the trigger phrase across two lines and would fail the checker; the break is moved one word earlier.)
- **BDEFS** (prerequisites only): Shader, Pixel, Type, Function, Argument. The terms the film teaches (uniform, built-in, vector, swizzle, signature, hint, UV, TIME, COLOR, mix, alpha) are defined on screen where first spoken, in `../_godot-shaders-series/GLOSSARY.md` wording.

## Cut line

If the film runs long, cut in this order: the overloading beat (B27), the two-performance-notes beat (B33), the global-built-ins half of B24 (keep the pass-it-in half), and the ternary beat (B29). Together about 47 seconds. The vectors and swizzle beats (B12 to B17), the signature and built-in beats (B20, B23), and the whole reading act (B34 to B41) stay: they are the film. Current estimate: 10.9 minutes by the lint's cautious figure, so no cut is needed.
