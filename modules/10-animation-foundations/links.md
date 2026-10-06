# Module 10 — Helpful links

## Executive summary

This page collects the readings, documentation, Walker projects and tools behind Module 10, Animation foundations. Open it when you start the sword-timing exercise, when an agent makes a claim about animation timing that needs checking against the documentation, or when you begin Assignment 8.

## Read first

- [Chapter 10 — Animation Foundations](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/10-animation-foundations.md) — the long reading behind this lesson: the full run of 27 September 2026, the frame-by-frame measurements, and the Unity and Unreal comparisons.
- [Worked-example record for Chapter 10](../../examples/10-animation-foundations/README.md) — open it for the four prompts as sent, one diff per agent run, the final pinned test, and every headless log.
- [walker-2d-finite-state-machine](https://github.com/nikbearbrown/walker-2d-finite-state-machine) — the demo whose sword timing you pin; its `godot/` folder holds `test_input.gd` and `test_combo.gd`, and it keeps the upstream MIT license.

## Godot documentation

- [Animation class reference](https://docs.godotengine.org/en/stable/classes/class_animation.html) — tracks, keys, `length`, update modes and loop modes, in the engine's own words.
- [AnimationPlayer class reference](https://docs.godotengine.org/en/stable/classes/class_animationplayer.html) — what `play()` does when the same animation name is already assigned.
- [AnimationMixer class reference](https://docs.godotengine.org/en/stable/classes/class_animationmixer.html) — the shared base class that owns the process and method callback modes.
- [Introduction to the animation features](https://docs.godotengine.org/en/stable/tutorials/animation/introduction.html) — interpolation, easing and update mode between keys.
- [Animation track types](https://docs.godotengine.org/en/stable/tutorials/animation/animation_track_types.html) — what each track type does, including why method tracks do not fire when you scrub in the editor.
- [2D sprite animation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html) — the two routes for a sprite sheet: `AnimatedSprite2D` with `SpriteFrames`, or `Sprite2D` frames keyed in an `AnimationPlayer`.
- [Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) — the exact meaning of `--headless`, `--script` and `--fixed-fps`, which every check in this module uses.

## Walker projects

- [walker-3d-ik](https://github.com/nikbearbrown/walker-3d-ik) — open `test_modes.gd` and `test_navigation.gd` for a scheduling regression check and the `skeleton_updated` sampling fix; its `FRICTIONAL.md` records the headless mouse-capture limit.
- [Godot demo `2d/finite_state_machine`, pinned commit](https://github.com/godotengine/godot-demo-projects/tree/a3b5c113112f77291d5f3d1360f33a882fdc52f7/2d/finite_state_machine) — the upstream demo the chapter's Build It starts from, before the Walker tests were added.
- [Godot demo `3d/ik`, pinned commit](https://github.com/godotengine/godot-demo-projects/tree/a3b5c113112f77291d5f3d1360f33a882fdc52f7/3d/ik) — the upstream Battle Bot IK scenes behind `walker-3d-ik`.

## Tools

- [Godot Engine downloads](https://godotengine.org/download/) — install the regular, non-.NET build; the recorded runs used Godot 4.7.2.
- [Claude Code documentation](https://code.claude.com/docs/en/overview) — the official overview for running Claude Code; access through Northeastern is set up as in Module 1.
- [Codex CLI](https://developers.openai.com/codex/cli) — the chapter's record used it for four of the five agent runs, where `codex exec` runs a prompt non-interactively.

## Going deeper

- [12 Principles of Animation (Official Full Series)](https://youtu.be/uDqjIdI4bF4) — carried over from the old course: a video series on the twelve principles of animation, for the engine-neutral vocabulary of good motion, whatever tool keys it.
- [Making Fluid and Powerful Animations for Skullgirls (GDC)](https://youtu.be/Mw0h9WmBlsw) — carried over from the old course: a game-developer talk on making game animation fluid and powerful, a reference for the feel judgment this module leaves to you.
