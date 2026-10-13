# Brief: Godot Shader Language

**What this is.** The content brief for the film that teaches the *language* of a Godot shader: how to read any shader line by line. Slug `godot-shader-language`, folder `claude-liam-lecture-godot-shader-language`, group Foundations, target about 10 minutes (ceiling 15). Title lines: `["Godot Shader", "Language"]`.
**Why.** Bear asked for two opening films: one on what a shader is (the pilot, already laid out) and one on the language itself. A viewer who can read the types and the shape of a file can read what an AI writes.
**Found.** The source course spends about 45 minutes across its variables, shader-code and function chapters on this. Two of its claims need checking before they are repeated (custom functions and built-ins; "if statements are slow"). The pilot teaches `uniform` and hints for sliders, so this film only recaps them.

## The one idea

Every line of a shader is an expression with a **type**, and most types are **vectors** (bundles of two to four numbers). Operations act on all the parts at once, which is why shader code looks so short. If you can say the type of each expression, you can read the file.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("A shader line works on\none number at a time.", "one number", "a bundle of numbers")`. The film's framing: shader code looks like GDScript but is stricter, and its basic unit is a bundle of numbers.

## Prerequisites for the terms card (3 to 6; the film earns vector, swizzle, uniform)

Candidates: **Variable** (a named value), **Type** (what kind of value a variable holds), **Function** (a named block of code you can call), **Argument** (a value you pass into a function). Terms of 17 characters or fewer.

## Suggested acts (change within the rules; 4 to 10 beats each)

1. **The Shape of a File.** Header (`shader_type`, optional `render_mode`), then globals (`uniform`, `const`, `varying`), then functions. Statements end in semicolons; braces group; indentation is only for people; `//` and `/* */` comments; names are case-sensitive. Picture: one real 14-line shader as horizontal bands with labels.
2. **Types and Vectors.** `float`, `int`, `bool`; `vec2`, `vec3`, `vec4`; constructors (`vec4(1.0)` fills all four; `vec4(rgb, 1.0)`); swizzles (`.rgb`, `.xyz`, `.st`, any order, never mixing sets); component-wise arithmetic (`vec3 * 2.0`, `vec3 * vec3`). **Strict typing**: `1` is an int, `1.0` a float, and the compiler refuses to mix them (show the real error text from the Lab).
3. **Your Own Functions.** Return type, name, parameters; qualifiers `in`, `out`, `inout`, `const`; a function must be defined above the function that calls it; a function must return what it promises. **Built-ins inside your functions:** the source says `UV` and `COLOR` are not visible inside a function you write and must be passed in; verify exactly which built-ins are and are not (is `TIME`, a global built-in, visible?).
4. **Choices and Loops.** `if`/`else`, the ternary `?:`, `for`, `while`. Keep to what the docs say: infinite loops can freeze the editor; do not compare floats with `==` (use a small range); `discard` has a documented performance cost. Do **not** repeat "if statements are slow in shaders" unless you can source it.
5. **Read One Aloud (payoff).** A neutral 10 to 14 line `canvas_item` shader (for example a tinted pulse: `uniform vec4 tint : source_color; ... vec3 base = tint.rgb * (0.5 + 0.5 * sin(TIME)); COLOR = vec4(base, tint.a);`) read line by line by naming each expression's type. Do not use the Signal Garden pad shader here (another film reads it).

## What the source course does (in my words, for orientation only)

- Contrasts code shaders with the node-graph (visual) kind: equally powerful; the graph is friendly to start and becomes hard to read at scale; online shader sites and AI assistants hand you code, so code is the one to read. (The film may say one sentence: Godot generates the same code from a graph.)
- Says the language is based on GLSL 3.0, C-like; semicolons everywhere; types are strict; no int plus float; indentation does not matter; `void fragment()` is called automatically; `vec4(1.0)` is white; red is `vec4(1.0, 0.0, 0.0, 1.0)`; `color.rgb` and `color.xyz` are the same parts; people write `1.` for a float.
- Declares variables with a type first; `const` exists but is rare; `uniform` is the exposed kind (a "parameter" in the graph editor); `hint_range(0, 1, 0.1)` gives start, end, step; `source_color` turns a vec3/vec4 into a color picker; a `sampler2D` uniform is a texture and `texture(sampler, UV)` returns a vec4; the built-in `TEXTURE` is the node's own texture.
- In the function chapter: the circle code moved into `create_circles(vec2 uv)` and the source discovered `UV` was unknown there, so it passes `uv` in; a function must have a `return`.
- In the outline chapter: `if (line_thickness > 0.0) { ... }`, then nested `for` loops replace eight copied lines; it says ifs should be avoided for performance.

## Source claims to check or correct

- "Based on GLSL 3.0": the docs say **similar to GLSL ES 3.0** (and "simplified"). Say "similar to".
- "Custom functions cannot see built-ins": verify which, with a Lab shader that uses `UV`, `COLOR`, `TIME` and `TEXTURE` inside a user function; the docs do not state it directly.
- "If statements are slow": not in the docs; only `discard` has a documented cost. Either leave it out or source it properly.
- "1. is how you write a float": it is allowed shorthand; `1.0` is clearer on screen.

## Facts to verify

Docs: Shading language reference (types, casting, swizzling, flow control, functions, uniforms, varyings, constants). Lab/scripts: the exact compiler message for `float a = 2;`, for `1 + 1.0`, for a swizzle that mixes sets (`c.rx` against `c.xg`), for calling a function defined later, for `UV` inside a user function, for a missing `return`; that `vec4(1.0)` is white; that `vec3 * float` works and `vec3 * int` does not.

## Captures

Mostly Lab stills and real compiler messages shown on `CCPlainShell`/`ClaudeCodeBeat` (the Lab prints `SHADER ERROR` text). No editor interaction needed, except possibly one editor frame of the shader editor's error panel (optional).

## Cut line

Act 4 shrinks to two beats; the three compiler-error beats in act 2 merge into one.

## Other films cover (do not teach here)

Uniform sliders and `set_shader_parameter` (the pilot); the math functions (`step`, `mix`, ...): the math toolkit film; `varying` in depth: vertex shaders; `texture()` in depth: textures and color; `render_mode` options: the 3D film.
