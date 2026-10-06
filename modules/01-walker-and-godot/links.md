# Module 1 — Helpful links

## Executive summary

This page lists what to open while you work through Module 1: the companion chapter and its run record, the Godot pages behind the vocabulary and the walker-jumpman code, the starter repositories, and the two tools you need installed. Open the chapter after the lesson, and the Godot pages when the lesson sends you to a file or an idea you have not met.

## Read first

- [Chapter 1: Walker and Godot](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/01-walker-and-godot.md) — the long reading behind this module, with the input trace, the run-speed experiment and the Unity and Unreal comparisons.
- [Chapter 1 worked-example record](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/tree/main/examples/01-walker-and-godot) — the prompts, trimmed transcripts, test logs and the predictions written before the run, for checking the chapter's numbers.

## Godot documentation

- [Key concepts overview](https://docs.godotengine.org/en/stable/getting_started/introduction/key_concepts_overview.html) — nodes, scenes, the scene tree and signals, the vocabulary the whole course uses.
- [First look at the editor](https://docs.godotengine.org/en/stable/getting_started/introduction/first_look_at_the_editor.html) — the FileSystem, Scene and Inspector docks and the bottom panel with the debug console, for the Use It step.
- [File system](https://docs.godotengine.org/en/stable/tutorials/scripting/filesystem.html) — what `project.godot` and `res://` mean, and why every command says `--path godot`.
- [TSCN file format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html) — how to read a saved scene as text, the way an agent reads it.
- [GDScript basics](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html) — the language of `player.gd` and `session.gd`, and why it is not Python.
- [Idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html) — `_process` against `_physics_process`, the two clocks, and why every gameplay change lands in 1/60 s steps.
- [Using CharacterBody2D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html) — how `velocity` and `move_and_slide()` move the player.
- [Custom drawing in 2D](https://docs.godotengine.org/en/stable/tutorials/2d/custom_drawing_in_2d.html) — how the starter draws its character in code, separate from its collision shape.

## Walker projects

- [walker-jumpman](https://github.com/nikbearbrown/walker-jumpman) — the starter you clone; it has no license file, so use it as course material and credit it.
- [walker-jumpman BUILD-REPORT](https://github.com/nikbearbrown/walker-jumpman/blob/main/BUILD-REPORT.md) — what the build claims, including the four failures its first test run found.
- [walker-jumpman GDD](https://github.com/nikbearbrown/walker-jumpman/blob/main/GDD.md) — the larger design; read it to find a proposed feature the baseline does not implement.
- [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd) — the semester example, with Clawd as the character; open its `CHANGE-BRIEF.md` and `FRICTIONAL.md` for what an honest log looks like.

## Tools

- [Godot 4.7.2 download](https://godotengine.org/download/archive/4.7.2-stable/) — the regular (non-.NET) editor version the starter was tested with.
- [Claude Code setup](https://code.claude.com/docs/en/setup) — install, `claude --version` and sign-in; it states which account types include Claude Code.

## Going deeper

- [UID changes coming to Godot 4.4](https://godotengine.org/article/uid-changes-coming-to-godot-4-4/) — why scripts have `.uid` files and why you commit them.
- [Claude Code: how Claude remembers your project](https://code.claude.com/docs/en/memory) — `CLAUDE.md` versus `AGENTS.md`, which matters for the Clawd repository's `AGENTS.md`.
