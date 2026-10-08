# Module 6 — Helpful links

## Executive summary

This page collects the readings, Godot documentation, Walker projects and tools for Module 6, Shader foundations. Open it when you want the source behind a claim in the lesson, or when a shader task goes wrong and you need the official reference.

## Read first

- [Chapter 6 — Shader Foundations](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/06-shader-foundations.md) — the long reading behind this module: the full worked run, the agents' mistakes, and the Unity and Unreal comparison.
- [Headless shader findings](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/examples/06-shader-foundations/HEADLESS-SHADER-FINDINGS.md) — the experiment table showing what a `--headless` Godot run can and cannot report about shaders, with real outputs; open it before you trust any headless shader check.
- [How Claude remembers your project](https://code.claude.com/docs/en/memory) — Claude Code's own account of `CLAUDE.md`: how it loads, how long it should be, and the `@` import used on its first line.

## Godot documentation

- [Introduction to shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html) — the shader types and the `vertex()`, `fragment()` and `light()` processor functions.
- [CanvasItem shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html) — the built-ins for 2D shaders, including the exact definitions of `COLOR`, `TEXTURE` and `TIME`.
- [Shading language reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html) — uniforms, hints such as `hint_range` and `source_color`, and the language's types and functions.
- [ShaderMaterial class reference](https://docs.godotengine.org/en/stable/classes/class_shadermaterial.html) — `set_shader_parameter()` and the warning about materials shared between nodes.
- [Visual shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/visual_shaders.html) — the node-graph editor, and how to see the shader code a graph becomes.
- [Overview of debugging tools](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html) — the Remote scene tree you use to set `flash_amount` on a running game.

## Walker projects

- [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd) — the 2D platformer this module's failure flash is built in; open `SOURCES.md` for its provenance and licence notes, `godot/features/player/` for how Clawd is drawn, and `godot/tests/` for the existing suites.
- [walker-compute-post-shader](https://github.com/nikbearbrown/walker-compute-post-shader) — a GLSL compute shader run after the 3D scene renders; open `VERIFICATION.md` for a worked example of stating what a headless run cannot show. It is an adaptation of a Godot demo and keeps the upstream MIT licence.

## Tools

- [Godot download page](https://godotengine.org/download/) — choose the regular editor, not the .NET build; the runs behind this module used Godot 4.7.2, so record your version.
- [Claude Code quickstart](https://code.claude.com/docs/en/quickstart) — installing Claude Code and starting a first session.
- [coreutils on Homebrew](https://formulae.brew.sh/formula/coreutils) — provides the `timeout` command that wraps every headless test run on macOS.

## Going deeper

- [Converting GLSL to Godot shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/converting_glsl_to_godot_shaders.html) — how GLSL-style code, including ShaderToy-style code, maps to Godot's language; open it before porting a shader you found elsewhere.
- [The Book of Shaders](https://thebookofshaders.com/) — a free, engine-neutral introduction to fragment shaders with editable examples.
- [Shadertoy for absolute beginners](https://www.youtube.com/watch?v=u5HAYVHsasc) — a video introduction to writing fragment shaders in the browser, carried over from the course's earlier ShaderToy page.
