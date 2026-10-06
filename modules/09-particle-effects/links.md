# Module 9 — Helpful links

## Executive summary

This page collects the readings, documentation, Walker projects and tools behind Module 9, Particle effects. Open it when you start the death-burst exercise, when an agent's claim about a particle setting needs checking against the documentation, or when you begin Assignment 7.

## Read first

- [Chapter 9 — Particle Effects](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/09-particle-effects.md) — the long reading behind this lesson: the full run of 27 September 2026, the probes, and the Unity and Unreal comparisons.
- [Worked-example record for Chapter 9](../../examples/09-particle-effects/README.md) — open it for the exact prompts, one diff per agent session, the final test, and every headless log.
- [walker-2d-dodge-the-creeps](https://github.com/nikbearbrown/walker-2d-dodge-the-creeps) — clone it to get the game, its `test_input.gd` harness and its Walker log; it keeps the upstream MIT license.

## Godot documentation

- [2D particle systems](https://docs.godotengine.org/en/stable/tutorials/2d/particle_systems_2d.html) — the manual's tour of the 2D particle nodes and how the CPU and GPU versions differ.
- [3D particle systems](https://docs.godotengine.org/en/stable/tutorials/3d/particles/index.html) — the 3D manual, including why CPU particles suit older hardware and phones.
- [GPUParticles2D class reference](https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html) — the exact wording for `amount`, `lifetime`, `one_shot`, `restart()`, `finished` and a null `texture`.
- [ParticleProcessMaterial class reference](https://docs.godotengine.org/en/stable/classes/class_particleprocessmaterial.html) — the shared 2D and 3D material: spread, velocity, gravity, `particle_flag_disable_z` and sub-emitter modes.
- [Particle sub-emitters](https://docs.godotengine.org/en/stable/tutorials/3d/particles/subemitters.html) — the rules for spawning one system from another, including what stops a sub-emitter emitting.
- [Particle shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/particle_shader.html) — `shader_type particles;`, its `start()` and `process()` functions, and the built-ins you can write.
- [GPU optimization](https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html) — the page that calls fill rate on mobile very expensive; open it when you price an effect on a real GPU.

## Walker projects

- [walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer) — open it for a `CPUParticles3D` coin burst, an enemy explosion, and `particle_material.tres`; look in its animations for `emitting` being keyed.
- [Godot demo `2d/particles`, pinned commit](https://github.com/godotengine/godot-demo-projects/tree/a3b5c113112f77291d5f3d1360f33a882fdc52f7/2d/particles) — a catalogue of seventeen `GPUParticles2D` nodes in one scene, and the README that says to enable Disable Z in 2D.
- [Godot demo `3d/particles`, pinned commit](https://github.com/godotengine/godot-demo-projects/tree/a3b5c113112f77291d5f3d1360f33a882fdc52f7/3d/particles) — a 3D scene with collision, attractors, trails and sub-emitters, for features the 2D game does not use.

## Tools

- [Godot Engine downloads](https://godotengine.org/download/) — install the regular, non-.NET build; the recorded runs used Godot 4.7.2.
- [Claude Code documentation](https://code.claude.com/docs/en/overview) — the official overview for running Claude Code; access through Northeastern is set up as in Module 1.
- [Codex CLI](https://developers.openai.com/codex/cli) — needed only for the cost-measurement step, where `codex exec` runs a prompt non-interactively.

## Going deeper

- [Reeves, "Particle Systems" (1983), SIGGRAPH history archive](https://history.siggraph.org/learning/particle-systems-a-technique-for-modeling-a-class-of-fuzzy-objects-by-reeves/) — the abstract of the paper that named the technique; the full paper is doi:10.1145/357318.357320.
- [The Nature of Code, Chapter 4: Particle Systems](https://natureofcode.com/particles/) — carried over from the old course's particle page: a free chapter that builds a particle system from scratch in code, whatever engine you use.
