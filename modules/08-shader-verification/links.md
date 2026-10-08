# Module 8 — Helpful links

## Executive summary

This page collects the readings, Godot documentation, Walker projects and tools for Module 8, Shader verification. Open it when you are reviewing a shader change and need the official reference for a timing, colour or coordinate claim, or the files that rebuild this module's seeded change.

## Read first

- [Chapter 8 — Shader Verification](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/08-shader-verification.md) — the long reading behind this module: the review run, the oracle that rejected correct code, and the Unity and Unreal comparison.
- [The seeded change](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/examples/08-shader-verification/seeded-change.diff) — the plausible but incorrect commit you review; apply it exactly as Build It describes.
- [The human bench procedure (BENCH.md)](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/examples/08-shader-verification/files/BENCH.md) — the step-by-step screenshot and colour-sampling procedure for rung 5 of the evidence ladder.

## Godot documentation

- [CanvasItem shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html) — the definitions of `COLOR`, `TEXTURE` and `TIME`, and the render modes behind the wrong-input and alpha families of bug.
- [Converting GLSL to Godot shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/converting_glsl_to_godot_shaders.html) — the coordinate and UV conventions behind the flip family of bug, for porting ShaderToy-style code.
- [Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) — `--headless`, `--fixed-fps` and the other flags every command in this module uses.
- [Viewport class reference](https://docs.godotengine.org/en/stable/classes/class_viewport.html) — `use_hdr_2d` and what it changes about 2D colour values.
- [SceneTree class reference](https://docs.godotengine.org/en/stable/classes/class_scenetree.html) — the `process_frame` and `physics_frame` signals that decide when a test samples a value.
- [Node class reference](https://docs.godotengine.org/en/stable/classes/class_node.html) — `process_priority`, the property a sampler node uses to run after everything else in the frame.
- [Using compute shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/compute_shaders.html) — the compute pipeline, and the renderer requirement that explains why compiled is not the same as run.

## Walker projects

- [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd) — the project the failure flash lives in; clone it at commit `382f2ba` to rebuild this module's starting point. Its `SOURCES.md` records its provenance and licence notes.
- [walker-compute-post-shader](https://github.com/nikbearbrown/walker-compute-post-shader) — the compute-shader companion; open `VERIFICATION.md` for a model of separating compiled bytecode from executed-shader evidence. It is an adaptation of a Godot demo and keeps the upstream MIT licence.

## Tools

- [Godot download page](https://godotengine.org/download/) — choose the regular editor, not the .NET build; the runs behind this module used Godot 4.7.2, so record your version.
- [Claude Code quickstart](https://code.claude.com/docs/en/quickstart) — installing Claude Code, used for the read-only review in Prompt 1.
- [Codex CLI](https://github.com/openai/codex) — OpenAI's command-line coding agent, used here as the second reviewer and for the `codex exec` runs.

## Going deeper

- [How Claude remembers your project](https://code.claude.com/docs/en/memory) — why the effect spec lives in `CLAUDE.md` and how Claude Code loads it.
- [Unity Graphics Test Framework](https://docs.unity3d.com/Packages/com.unity.testframework.graphics@8.3/manual/index.html) — Unity's image-comparison testing against reference images, the closest counterpart to this module's bench; read it for how reference images are organised by platform.
- [Unreal Screenshot Comparison Tool](https://dev.epicgames.com/documentation/en-us/unreal-engine/screenshot-comparison-tool-in-unreal-engine) — Unreal's built-in screenshot comparison against a Ground Truth image, where a person decides whether a difference is a bug.
