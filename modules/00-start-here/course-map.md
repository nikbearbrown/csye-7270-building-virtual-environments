# Course map and schedule

CSYE 7270 · Fall 2026

## Executive summary

This page shows the whole semester on one screen: sixteen modules (a setup module and one per week), ten graded assignments, and which module feeds which assignment. Read it first, then keep it open. It tells you what to read and build each week, when each assignment is due, and how the pieces connect into one game that you build across the whole course. It does not set dates: Canvas shows the real deadlines, and the day numbers below only describe the 10-day rhythm. Everything on it is the plan for the course, not a promise that any single tool will behave the same way next week; you will find out how Claude Code, Godot and your own game actually behave by running them.

## How the course is organized

Every module is one Canvas module with the same four parts, modeled on the earlier course:

| Part | What it is |
|---|---|
| **Lecture** | One page that teaches the week's machinery, then walks you through a hands-on task with Claude Code on a real Walker project: Predict, Build It, Use It, Ship It, Verify. |
| **Practice (ungraded)** | A short Canvas quiz. Take it as often as you like; read the feedback. It checks understanding and earns no points. |
| **Assignment** | Appears in the first module it covers, so you can see the target while you learn. An assignment that covers two modules (Assignment 3, for example, covers Modules 3 and 4) is listed in both and is due after the second one. 100 points. |
| **Links** | Official documentation, the Walker projects used, and further reading for that week. |

Each module also maps one-to-one to a chapter of the companion book. The chapter is the long reading: the full record of what the coding agents did, including their mistakes, and a complete comparison with doing the same task in Unity and in Unreal Engine. You can do the course from the lecture pages alone; the chapters are where to go when you want the whole story.

## Who does what

| Part of the system | Its job |
|---|---|
| You | Choose the game, predict failures, approve changes, play the build, judge the result. |
| Walker | The workflow and project files: Game brief, Build, Playtest, Inspect, Revise, Export. |
| Claude Code | Reads the project, proposes and makes the changes you authorize, runs checks, explains. |
| Godot 4 | Runs the game. You use the regular GDScript edition, not the .NET one. |
| Brutalist | Turns your game, code and evidence into the explainer film each assignment requires. |

## The semester at a glance

Day 1 is the first class day. The assignment column shows the suggested due day; Canvas has the exact deadline.

| Week | Module | You build (hands-on) | Assignment due |
|---|---|---|---|
| Before 1 | 0. Start Here: the toolchain | Set up Claude Code, Godot and the headless checks; add a score to `walker-pong` | — |
| 1 | 1. Walker and Godot | Trace one input to its visible result; change one number and predict the tests | Assignment 1, Day 10 |
| 2 | 2. Prompting game art | Turn one generated image into a checked Godot asset; wire sound to real events | Assignment 2, Day 20 |
| 3 | 3. Blender MCP to Godot | Build a prop in Blender from the command line and verify it in a 3D game | Assignment 3, Day 30 (with Module 4) |
| 4 | 4. Scenes, collision and physics | Add a shield pickup to a 2D game and test what it does to collisions | Assignment 3 |
| 5 | 5. The GDD and virtual worlds | Recover a design document from code, then specify and build one 3D interaction | Assignment 4, Day 40 |
| 6 | 6. Shader foundations | Write the project context for Claude Code, then build a failure-flash effect | Assignment 5, Day 50 (with Module 7) |
| 7 | 7. Materials and textures | Audit a ship's materials, then add ambient occlusion to its hull | Assignment 5 |
| 8 | 8. Shader verification | Review a plausible but incorrect shader change | Assignment 6, Day 60 |
| 9 | 9. Particle effects | Build a burst effect, then measure what it costs | Assignment 7, Day 70 |
| 10 | 10. Animation foundations | Pin down timing with checks before changing any animation | Assignment 8, Day 80 (with Module 11) |
| 11 | 11. Animation and interaction | Wire animation states to player actions and test the edges | Assignment 8 |
| 12 | 12. Audio and triggers | Make a sound fire on a real event and prove it reaches the mix | Assignment 9, Day 90 (with Module 13) |
| 13 | 13. Profiling and optimization | Benchmark two ways of doing the same job, then decide | Assignment 9 |
| 14 | 14. Game AI and systems | Direct a guard that patrols, chases and searches; labs in learning agents, generated levels and networking | Assignment 10, Day 100 (with Module 15) |
| 15 | 15. Final projects: from brief to export | Add a persistent best time, reproduce the build from a clean clone, and export it | Assignment 10 |

## Assignments: 100 points every 10 days

| # | Assignment | Covers | Required film (Brutalist skill) |
|---|---|---|---|
| 1 | Extend Walker Jumpman | Module 1 | `godot-walkthrough` |
| 2 | Generate Art, Sound, and Music for Your Game | Module 2 | `godot-gamedev` |
| 3 | Build a Prop in Blender and Make It Work in Godot | Modules 3, 4 | `godot-gamedev` |
| 4 | Specify It, Then Build One 3D Interaction | Module 5 | `godot-gdd` |
| 5 | A Shader and a Material That Say Something About Your Game | Modules 6, 7 | `godot-gamedev` |
| 6 | Audit a Plausible but Incorrect Shader Change | Module 8 | `godot-gamedev` |
| 7 | Two Particle Effects, Tuned and Priced | Module 9 | `godot-walkthrough` |
| 8 | Animation Wired to Player Actions | Modules 10, 11 | `godot-walkthrough` |
| 9 | Sound That Provably Plays, and a Frame You Can Afford | Modules 12, 13 | `godot-gamedev` |
| 10 | Final Project: From Brief to Export | Modules 14, 15 and the whole course | `godot-walkthrough` and `godot-gdd` |

Every assignment is graded the same way: **60** points for the assignment-specific work and its explainer, **10** for your Frictional log, **10** for posting the same version to GitHub and Canvas, and **20** for Relative Quartile. Read [how assignments are graded](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/prerequisites/assessment-policy.md) and the AI policy page in this module before you start Assignment 1. Late work loses 10% per day.

## One game all semester

After Assignment 1 you pick the game you actually want to build (in Assignment 2) and keep building that one game. Assignments 3 to 10 each add one layer to the same repository, and you submit each one as a git tag on it (`a3`, `a4`, and so on up to `a10`). The final project is therefore the sum of your semester, not a restart. If your game is 2D, you add a 3D scene to it when an assignment needs one; a project may mix 2D and 3D scenes. You may change games once, before Assignment 4, if you explain why in your `FRICTIONAL.md`.

## The weekly rhythm

1. **Read the module's lecture page.** It teaches the machinery in plain terms and shows a real run.
2. **Predict before you delegate.** Write your answers down. A wrong prediction is useful evidence.
3. **Build it with Claude Code,** one bounded change at a time, then check it with your own command, not the agent's report.
4. **Use it.** Play the game. Anything visual, audible or about feel is a judgment only you can make.
5. **Ship it and verify.** Commit, log what happened in `FRICTIONAL.md`, and re-check from a clean copy.

An agent saying "done" is a claim. A passing headless test is evidence about state, not a playtest. These two sentences are the course in miniature.

## Where to find things

- **Syllabus:** the Canvas Syllabus tab.
- **Course repository (chapters, examples, assignments):** [github.com/nikbearbrown/csye-7270-building-virtual-environments](https://github.com/nikbearbrown/csye-7270-building-virtual-environments).
- **Walker framework:** [github.com/nikbearbrown/walker](https://github.com/nikbearbrown/walker). Example games are separate repositories named `walker-*`.
- **Brutalist film toolkit:** [github.com/nikbearbrown/brutalist.art](https://github.com/nikbearbrown/brutalist.art). Use the course-provided copy; ask for an update if your copy lacks a `godot-*` skill.
- **Help:** write to the instructor early; the syllabus has the address.
