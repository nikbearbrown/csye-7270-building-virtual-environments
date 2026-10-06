# CSYE 7270 companion book — chapters (Godot edition)

## Executive summary

**What this is.** The chapter map of the CSYE 7270 companion book after the course moved from Unity and Unreal to Godot, the Walker framework, and a coding CLI (Claude Code or Codex). There are sixteen chapters: one per module of the revised Fall 2026 syllabus, plus Chapter 0 for the command-line toolchain.

**Why read it.** It shows where each old Canvas module went. It tells you which public Walker project each chapter works in, and what you will actually do in each hands-on section.

**What the chapters have in common.** Every chapter is hands-on. You give a coding agent one bounded change to a real Walker Godot project, run Godot headless to check the result yourself, and then play it. Each chapter's worked example was really run on 27 September 2026, with Claude Code, Codex or both. The record of each run, including what the agents got wrong, is in [`../examples/`](../examples/). Every chapter ends with **Doing the same thing in Unity** and **Doing the same thing in Unreal Engine** (similarities, then differences). Those two sections come from each vendor's documentation; neither engine was run.

**What they are not.** These are review drafts. No AI+1 book gate is signed, visual and audio judgments are marked as human checks, and Professor Bear has not yet reviewed the text.

---

## The chapters

| Ch | Chapter | Syllabus week | Old `.imscc` material it replaces | Hands-on |
|---|---|---|---|---|
| 0 | [The Toolchain: Claude Code, Codex, Walker, and Godot at the Command Line](00-the-toolchain.md) | 1 (setup) | "Learning Unity" / "Unreal Engine" onboarding; the Claude Code handout | Add a score to `walker-pong`, twice, once with each agent, then find out why both misread the regression test |
| 1 | [Walker and Godot](01-walker-and-godot.md) | 1 | How to Learn Unity 3D; Unity C#; Unreal Engine; Assignment 2 – Learning Unity | Trace one input to its visible result, then change one number and predict the tests |
| 2 | [Prompting Game Art (and Sound) Against the Engine](02-prompting-game-art.md) | 2 | Mini-Assignments 1 and 3 (generative art and audio); Animation Assets | Turn one generated image into a checked Godot asset, then wire sound to real events |
| 3 | [Blender to Godot: MCP, Scripts, and a Prop You Can Measure](03-blender-mcp-to-godot.md) | 3 | Animation in Blender; Houdini (context) | Build a checkpoint post in Blender headless and verify it in the 3D platformer |
| 4 | [Scenes, Collision and Physics](04-scenes-collision-and-physics.md) | 4 | Unity C#; Unreal Blueprints; 2D Games; Assignment 3 – Unreal Blueprints | Add a shield pickup to Dodge the Creeps |
| 5 | [The GDD and Virtual Worlds](05-the-gdd-and-virtual-worlds.md) | 5 | Game Design Document; Best Practices; Prototyping a Project; the GDD assignments; Pitch Your Game | Recover a GDD from code with `/gdd reverse`, then specify and build one 3D interaction |
| 6 | [Shader Foundations](06-shader-foundations.md) | 6 | Unity Shaders and Unreal Materials; CgFX; ShaderToy; Assignment 4 – Shaders | Write the project context, then build a failure flash |
| 7 | [Materials and Textures](07-materials-and-textures.md) | 7 | Unity Shader Graph; HLSL and Custom Nodes in Unreal; material link pages | Audit a ship's materials, then give the hull its ambient occlusion |
| 8 | [Shader Verification](08-shader-verification.md) | 8 | Assignment 4 – Shaders (verification) | Review a plausible but incorrect shader change |
| 9 | [Particle Effects](09-particle-effects.md) | 9 | Particle Effects; Particle Effects in Unity; VFX Graph flocking; Assignment 5 | A death burst, then its cost |
| 10 | [Animation Foundations](10-animation-foundations.md) | 10 | Animation; Animation in Unity / Unreal / Blender; Spriter; Assignment 6 | Pin the sword's timing, then change it |
| 11 | [Animation and Interaction](11-animation-and-interaction.md) | 11 | Mini-Assignment 2 (generative animation) | Wire a state machine to the player, then test the edges |
| 12 | [Audio and Triggers](12-audio-and-triggers.md) | 12 | Audio; Mini-Assignment 3 | A hit click, two buses, and proof that the click reaches the mix |
| 13 | [Profiling and Optimization](13-profiling-and-optimization.md) | 13 | Profiling in Unity and Unreal | Benchmark nodes against servers, then decide |
| 14 | [Game AI and Systems](14-game-ai-and-systems.md) | 14 | Game AI (FSM, behavior trees, NPCs, logic, simulation, reinforcement learning); Game AI with Unity (NavMesh, ML-Agents, AI Planner); Procedural Content Generation | A guard that patrols, chases and searches, plus labs in Q-learning, validated level generation and two-process networking |
| 15 | [Final Projects: From Brief to Export](15-final-projects-brief-to-export.md) | 15 | Final Portfolio Piece; Show and Tell; take-home midterm and final | A persistent best time, reproduced from a clean clone and exported |

Chapter 1 is the book version of the Canvas lesson in [`../modules/01-walker-and-godot/lesson.md`](../modules/01-walker-and-godot/lesson.md). Assignments 1 and 2 are in [`../assignments/`](../assignments/). No new graded assignments are defined here.

## Where to get the Walker projects

- The course starters: [`walker-jumpman`](https://github.com/nikbearbrown/walker-jumpman) and Professor Bear's semester example [`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd).
- The Walker adaptations of Godot's official demos, such as [`walker-pong`](https://github.com/nikbearbrown/walker-pong), [`walker-2d-dodge-the-creeps`](https://github.com/nikbearbrown/walker-2d-dodge-the-creeps) and [`walker-3d-platformer`](https://github.com/nikbearbrown/walker-3d-platformer). They are public under `github.com/nikbearbrown/walker-*`, published 27 September 2026, and each keeps the upstream MIT license. The one exception is `walker-gui-bidi-and-font-features`, which is private and not used in these chapters. Their source is [`godotengine/godot-demo-projects`](https://github.com/godotengine/godot-demo-projects) at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`.
- The Walker framework: [`walker`](https://github.com/nikbearbrown/walker). Its `/gdd` skill, which Chapter 5 uses, is not yet in the public repository.

## Rules every chapter follows

The writing contract is [`../pantry/chapter-spec.md`](../pantry/chapter-spec.md), including the rules learned while drafting. The ones students feel most:

- Run Godot headless (`--headless`), import once after cloning (`--import`), and run frame-counted tests with `--fixed-fps 60`, wrapped in `timeout`.
- An agent's "done" is a claim. Your own command is evidence. A passing headless test is not a playtest.
- Keep permissions narrow. `Bash(env *)` and `Bash(godot *)` are wider grants than they look.
- Anything visual, audible or about feel is a human check, and the chapters say so.
