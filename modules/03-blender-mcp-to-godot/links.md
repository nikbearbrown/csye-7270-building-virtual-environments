# Module 3 — Helpful links

## Executive summary

These are the pages to open while you work through Module 3: the companion chapter and its run records, the official Godot documentation behind the import and collision settings, the Walker 3D Platformer, and the tools you need installed. Open the Godot pages when an imported model arrives at the wrong size, axis or collision, and the Blender MCP pages only if you decide to try the live route, which the course has not run.

## Read first

- [Chapter 3 — Blender to Godot: MCP, Scripts, and a Prop You Can Measure](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/03-blender-mcp-to-godot.md) — the long reading behind this lesson, with the Unity and Unreal comparisons and every source.
- [Chapter 3 worked-example record](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/tree/main/examples/03-blender-mcp-to-godot) — the exact prompts, logs, diffs and agent transcripts from the 27 September 2026 runs, plus the probe scripts and the independent post check you copy in Verify.

## Godot documentation

- [Available 3D formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html) — open it to see which 3D formats Godot imports, why glTF 2.0 is the recommended one, and how `.blend` import depends on Blender.
- [Model export considerations](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/model_export_considerations.html) — Godot's axis conventions and the advice to apply transforms before exporting, for when a model arrives lying down or scaled.
- [Node type customization](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/node_type_customization.html) — the `-col`, `-convcol`, `-colonly`, `-convcolonly` and `-noimp` suffixes and the import settings that decide whether they are honoured.
- [Introduction to 3D](https://docs.godotengine.org/en/stable/tutorials/3d/introduction_to_3d.html) — the 3D coordinate system and the rule that one unit is one metre, which every size check in this module relies on.
- [Collision shapes (3D)](https://docs.godotengine.org/en/stable/tutorials/physics/collision_shapes_3d.html) — the 3D collision shape types, the convex versus concave distinction, and the advice not to translate, rotate or scale a collision shape.
- [Import process](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html) — how the `.import` sidecar and the `.godot/imported/` cache work, and which files belong in version control.

## Walker projects

- [walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer) — the project the checkpoint post is placed into: open `godot/player/player.tscn` for the 2.1 m capsule and `godot/enemy/enemy.glb.import` for the import settings that disable collision suffixes.
- [godot-demo-projects, 3d/platformer at the Walker commit](https://github.com/godotengine/godot-demo-projects/tree/a3b5c113112f77291d5f3d1360f33a882fdc52f7/3d/platformer) — the upstream MIT-licensed demo that `walker-3d-platformer` copies, if you would rather start from the original.

## Tools

- [Blender downloads](https://www.blender.org/download/) — the chapter's runs used Blender 5.1.2; install it before the script route and record the version you use.
- [Godot Engine downloads](https://godotengine.org/download/) — install the regular edition, not the .NET one; the chapter's runs used Godot 4.7.2.
- [MCP for Blender (community)](https://github.com/ahujasid/mcp-for-blender) — the README for the project the syllabus names, with its install steps, safety settings and tool list; its socket has no authentication, so keep it on `localhost`.
- [Blender MCP (Blender Lab)](https://www.blender.org/lab/mcp-server/) — Blender's own MCP server page, which requires Blender 5.1+ and warns that it runs generated code without guards.

## Going deeper

- [glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html) — the interchange format itself; section 3.4 gives its units and axes, which explain the +Y Up export option.
- [Blender manual: command line arguments](https://docs.blender.org/manual/en/5.1/advanced/command_line/arguments.html) — every flag for running Blender without a window, including `-b`, `--factory-startup`, `--python` and `--python-exit-code`.
- [Blender Python API: quickstart](https://docs.blender.org/api/5.1/info_quickstart.html) — an introduction to the `bpy` module that an agent's Blender script calls, useful for reading what it wrote.
