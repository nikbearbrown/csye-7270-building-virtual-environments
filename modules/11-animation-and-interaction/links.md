# Module 11 — Helpful links

## Executive summary

This page collects the reading, the official Godot documentation, the public Walker projects and the tools behind Module 11. Open it while you build the state machine and test, and again when you write up what the agent got wrong.

## Read first

- [Chapter 11 — Animation and Interaction](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/11-animation-and-interaction.md) — the long reading behind this module: the full record of the 27 September 2026 runs and the Unity and Unreal comparisons.
- [Worked example record for Module 11](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/examples/11-animation-and-interaction/README.md) — the prompts, diffs, traces and logs from the state-machine run; open it to run the held-jump trace yourself.

## Godot documentation

- [Using AnimationTree](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html) — how a tree reads an AnimationPlayer's clips, how parameters are addressed, and how root motion is read back.
- [AnimationNodeStateMachine](https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachine.html) — states, the built-in Start and End nodes, and how transitions are chosen.
- [AnimationNodeStateMachineTransition](https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachinetransition.html) — `advance_mode`, `advance_expression`, `xfade_time` and the other settings whose defaults decide whether a transition ever fires.
- [AnimationNodeStateMachinePlayback](https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachineplayback.html) — `travel()`, `get_current_node()` and `get_fading_from_node()`, the calls a state test reads.
- [AnimationNodeBlendSpace1D](https://docs.godotengine.org/en/stable/classes/class_animationnodeblendspace1d.html) — blending idle, walk and run along one axis from a single speed value.
- [2D sprite animation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html) — where frames cut from a generated clip end up in a 2D game.
- [Overview of debugging tools](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html) — the Remote scene tree, for reading an AnimationTree's parameters while the game runs.

## Walker projects

The two adaptations of Godot's demo projects keep the upstream MIT license; `walker-jumpman-clawd` is Professor Bear's own evolving example.

- [walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer) — the build you modify: the robot, its AnimationTree blend tree, and the input probe in `tests/`.
- [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd) — Clawd's code-driven animations and the `visual_animation()` priority list; open it to compare a priority list with a state machine.
- [walker-2d-finite-state-machine](https://github.com/nikbearbrown/walker-2d-finite-state-machine) — gameplay states that own the animation, and the mid-air attack edge case.

## Tools

- [Godot Engine downloads](https://godotengine.org/download/) — the regular (non-.NET) build; the recorded runs used 4.7.2.
- [Claude Code documentation](https://code.claude.com/docs/en/overview) — install and run Claude Code, the agent the lesson's prompts are written for.

## Going deeper

- [12 Principles of Animation (Official Full Series)](https://youtu.be/uDqjIdI4bF4) — carried over from the old course's Animation page; engine-neutral timing and spacing vocabulary for talking about a cross-fade.
- [Making Fluid and Powerful Animations For Skullgirls](https://youtu.be/Mw0h9WmBlsw) — a conference talk carried over from the old course's Animation page; engine-neutral.
- [So You Wanna Make Games?? | Episode 6: Character Animation](https://youtu.be/VmNUAX2V8JQ) — an introduction to character animation, carried over from the old course's Animation page.
- [DeepMotion Animate 3D documentation](https://www.deepmotion.com/doc/animate-3d) — an example of a video-to-3D-animation service and its export formats; read its terms, and capture only people who have agreed.
