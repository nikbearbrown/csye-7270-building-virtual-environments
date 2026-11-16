# Course map and schedule

CSYE 7270 · Fall 2026

## Executive summary

This page shows the whole semester on one screen: seventeen modules (a Conducting AI preface, a setup module and one per week), ten numbered assignments plus the existing five-point GDD milestone, and which module feeds which assignment. Begin with the [Conducting AI preface](../preface-conducting-ai/lesson.md), then keep this map open. It tells you what to read and build each week, when each assignment is due, and how the pieces connect into one game that you build across the whole course. The [Fall 2026 schedule](../../assignments/fall-2026-assignment-schedule.md) distinguishes confirmed Canvas dates from proposed remaining deadlines. Canvas remains the official source. Everything on it is the plan for the course, not a promise that any single tool will behave the same way next week; you will find out how Claude Code, Godot and your own game actually behave by running them.

## How the course is organized

Every module is one Canvas module with the same four parts, modeled on the earlier course:

| Part | What it is |
|---|---|
| **Lecture** | One page that teaches the week's machinery, then walks you through a hands-on task with Claude Code on a real Walker project: Predict, Build It, Use It, Ship It, Verify. |
| **Practice (ungraded)** | A short Canvas quiz. Take it as often as you like; read the feedback. It checks understanding and earns no points. |
| **Assignment** | Appears in the first module it covers, so you can see the target while you learn. An assignment that covers two modules (Assignment 5, for example, covers Modules 6 and 7) is listed in both and is due after the second one. Points are stated in each assignment. |
| **Links** | Official documentation, the Walker projects used, and further reading for that week. |

Each module also maps one-to-one to a chapter of the companion book. The chapter is the long reading: the full record of what the coding agents did, including their mistakes, and a complete comparison with doing the same task in Unity and in Unreal Engine. You can do the course from the lecture pages alone; the chapters are where to go when you want the whole story.

Every module ends with pointers on doing the same work in Unity and Unreal: what carries over, what differs from Godot, and where to read further. The preface explains the Godot choice: a direct code-and-file workflow with engine checks, without requiring an MCP bridge.

## Who does what

| Part of the system | Its job |
|---|---|
| You | Choose the game, predict failures, approve changes, play the build, judge the result. |
| Walker | The workflow and project files: Game brief, Build, Playtest, Inspect, Revise, Export. |
| Claude Code | Reads the project, proposes and makes the changes you authorize, runs checks, explains. |
| Godot 4 | Runs the game. You use the regular GDScript edition, not the .NET one. |
| Brutalist | Turns your game, code and evidence into the explainer film each assignment requires. |

## The semester at a glance

Module order describes the learning sequence. The assignment sequence and its confirmed Canvas deadlines are below. The GDD is Assignment 4, the pitch is Assignment 8, and the final is 250 points.

| # | Assignment | Points | Due (America/New_York) | Modules | Required film |
|---|---|---:|---|---|---|
| 1 | [Assignment 1 - Extend Walker Jumpman](../assignments/01-extend-walker-jumpman.md) | 100 | 2026-09-24, 11:59 pm | 1 | godot-walkthrough |
| 2 | [Assignment 2 - Generate Art, Sound, and Music for Your Game](../assignments/02-generate-art-sound-music-for-your-game.md) | 100 | 2026-10-07, 11:59 pm | 2 | godot-gamedev |
| 3 | [Assignment 3 - Your First 3D Game Assets with Claude, the Blender MCP, and Blender](../assignments/03-first-3d-assets-with-blender-mcp.md) | 100 | 2026-10-15, 11:59 pm | 3 | godot-gamedev |
| 4 | [Assignment 4 - Create a Game Design Document or GDD](../assignments/04-create-a-game-design-document.md) | 5 | 2026-10-19, 11:59 pm | 5 | No film specified |
| 5 | [Assignment 5 - Shaders, Materials, and the Godot Shading Language](../assignments/05-shaders-materials-and-godot-shading-language.md) | 100 | 2026-10-29, 11:59 pm | 6, 7 | godot-gamedev |
| 6 | [Assignment 6 - Creating Particle Effects with Godot and Claude](../assignments/06-creating-particle-effects.md) | 100 | 2026-11-03, 11:59 pm | 9 | godot-gamedev |
| 7 | [Assignment 7 - Doing Animation with Claude and Godot](../assignments/07-doing-animation.md) | 100 | 2026-11-15, 11:59 pm | 10, 11 | godot-walkthrough |
| 8 | [Assignment 8 - Final Project Pitch Film — Show What You Will Build](../assignments/08-final-project-pitch-film.md) | 50 | 2026-11-22, 11:59 pm | 5, 15 | Brutalist pitch film |
| 9 | [Assignment 9 - Teach One Game-AI Technique: Explain, Show, Try](../assignments/09-teach-one-game-ai-technique.md) | 100 | 2026-12-12, 11:59 pm | 14 | godot-walkthrough (Explain → Show → Try) |
| 10 | [Assignment 10 - Final Project: From Brief to Export](../assignments/10-final-project.md) | 250 | 2026-12-20, 11:59 pm | 15 | godot-walkthrough + godot-gdd |

The seven 100-point assignments follow their stated 60/10/10/20 rubrics. Assignment 8 uses 30/5/5/10; the final uses 150/25/25/50. Assignment 4 follows its five-point GDD requirements. Read [the assessment policy](../../prerequisites/assessment-policy.md) and each brief. Late work loses 10% per day.

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
