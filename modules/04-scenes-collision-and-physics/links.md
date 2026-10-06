# Module 4 — Helpful links

## Executive summary

This page collects what to open while you work through Module 4: the companion chapter, the Godot manual pages behind each idea, and the public Walker builds the lesson takes apart. Open the documentation page that matches whichever idea you are stuck on, and open a Walker project when you want to read the real files rather than a description of them.

## Read first

- [Chapter 4 — Scenes, Collision and Physics](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/04-scenes-collision-and-physics.md) — the long reading behind this lesson, including the full Unity and Unreal comparisons.
- [Worked-example record for Chapter 4](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/examples/04-scenes-collision-and-physics/README.md) — the prompt, both agents' diffs and tests, the reviewer's timing check, and every log from the 27 September 2026 runs.

## Godot documentation

- [Physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html) — the four collision-object types and the exact meaning of collision layers and masks.
- [Area2D](https://docs.godotengine.org/en/stable/classes/class_area2d.html) — open it to see when `get_overlapping_bodies()` is updated and which signals an `Area2D` emits.
- [Creating instances](https://docs.godotengine.org/en/stable/getting_started/step_by_step/instancing.html) — how a saved scene is reused, and how an instance's overrides interact with the source scene.
- [Using signals](https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html) — the observer pattern that wires Dodge the Creeps together.
- [Idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html) — which of `_process` and `_physics_process` to use, and why the physics rate matters to a test.
- [TSCN file format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html) — the text format an agent edits; read it before trusting a hand-written scene or UID.
- [Overview of debugging tools](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html) — where Visible Collision Shapes lives, for the Use It checks.

## Walker projects

All are public, and each keeps the upstream MIT license.

- [walker-2d-dodge-the-creeps](https://github.com/nikbearbrown/walker-2d-dodge-the-creeps) — the build you extend with the shield pickup; open `godot/test_input.gd` for its 14 checks.
- [walker-pong](https://github.com/nikbearbrown/walker-pong) — every object is an `Area2D` reacting through `area_entered`; open it for scripted-input tests at 30 and 60 FPS.
- [walker-2d-bullet-shower](https://github.com/nikbearbrown/walker-2d-bullet-shower) — 500 server-side bodies and the failed check where physics bodies fell away from their drawings.
- [walker-2d-dynamic-tilemap-layers](https://github.com/nikbearbrown/walker-2d-dynamic-tilemap-layers) — art and collision separated on purpose, so the player walks through a fake wall.
- [walker-loading-autoload](https://github.com/nikbearbrown/walker-loading-autoload) — a persistent autoload that changes scenes with a deferred call.
- [walker-loading-scene-changer](https://github.com/nikbearbrown/walker-loading-scene-changer) — the same job done with the engine's own change-scene helpers.

## Tools

- [Godot Engine downloads](https://godotengine.org/download/) — install the regular (not .NET) build; the chapter's runs used Godot 4.7.2.

## Going deeper

- [Using CharacterBody2D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html) — open it when you need a body you move yourself with `move_and_slide()`, as jumpman's Clawd does.
- [Optimization using Servers](https://docs.godotengine.org/en/stable/tutorials/performance/using_servers.html) — the trade behind the bullet shower: lower per-object overhead in exchange for managing handles yourself.
