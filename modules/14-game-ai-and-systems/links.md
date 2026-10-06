# Module 14 — Helpful links

## Executive summary

This page collects the reading, Godot documentation, Walker projects, tools and optional resources behind the guard hands-on and the three labs. Open the navigation and multiplayer pages while you write your Predict answers, and the Walker repositories when a lab says to start from a copy.

## Read first

- [Chapter 14 — Game AI and Systems](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/14-game-ai-and-systems.md) — the long reading: every prompt, the audits that caught the agents' mistakes, the three labs, and the Unity and Unreal comparison.
- [walker-2d-finite-state-machine](https://github.com/nikbearbrown/walker-2d-finite-state-machine) — the public Walker build you add the guard to; its tests are the 29 baseline checks every task must keep passing.

## Godot documentation

- [Using NavigationAgents](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html) — `target_position`, `get_next_path_position()`, `is_navigation_finished()` and `target_desired_distance`; the NavigationAgent2D class reference has the other two queries.
- [Using NavigationServer](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationservers.html) — why a path query at the start of a scene returns an empty result, and how to wait for the map.
- [High-level multiplayer](https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html) — peers, authority and RPC modes, the machinery behind Lab C.
- [RandomNumberGenerator](https://docs.godotengine.org/en/stable/classes/class_randomnumbergenerator.html) — seeded, repeatable randomness for Lab B, and the caution about relying on the algorithm across engine versions.

## Walker projects

- [walker-2d-dynamic-tilemap-layers](https://github.com/nikbearbrown/walker-2d-dynamic-tilemap-layers) — the side-view platformer with `Ground` and `Secret` tile layers that Lab B generates levels for.
- [walker-networking-multiplayer-pong](https://github.com/nikbearbrown/walker-networking-multiplayer-pong) — the ENet Pong with lobby, loopback match and terminal-flow tests that Lab C builds on.
- [walker-networking-multiplayer-bomber](https://github.com/nikbearbrown/walker-networking-multiplayer-bomber) — two real ENet processes on loopback using `MultiplayerSpawner` and `MultiplayerSynchronizer`, for reading after Lab C.
- [walker-compute-heightmap](https://github.com/nikbearbrown/walker-compute-heightmap) — a seeded noise island computed on the CPU and in a compute shader, with a README that warns against passing off headless CPU checks as GPU verification.

## Tools

- [Godot Engine downloads](https://godotengine.org/download/) — the regular (not .NET) edition for GDScript; the recorded runs used 4.7.2.
- [Claude Code overview](https://code.claude.com/docs/en/overview) — the command-line agent you direct for the guard and Labs B and C.
- [OpenAI Codex CLI](https://github.com/openai/codex) — optional: the agent used for Lab A and for Task 3 in the recorded runs.

## Going deeper

- [State, in Game Programming Patterns](https://gameprogrammingpatterns.com/state.html) — Robert Nystrom on state machines and pushdown automata, the two ideas in the Walker FSM build.
- [The AI of Half-Life: Finite State Machines | AI 101](https://youtu.be/JyF0oyarz4U) — carried over from the old course: an engine-neutral episode on how finite state machines work in games.
- [Behaviour Trees: The Cornerstone of Modern Game AI | AI 101](https://youtu.be/6VBCXvfNlCM) — carried over from the old course: a ten-minute engine-neutral explanation of how behavior trees work.
- [Practical Procedural Generation for Everyone](https://youtu.be/WumyfLEa6bU) — carried over from the old course: a 2017 GDC session by Kate Compton on the simple algorithms behind procedural content generation.
- [Gymnasium](https://gymnasium.farama.org/) — the maintained fork of OpenAI's Gym, the standard interface between a simulator and reinforcement-learning algorithms.
