# Module 1 — Walker and Godot

CSYE 7270 · Fall 2026

## What is Walker?

Walker is a project for making games through a structured conversation with an AI coding assistant. You describe a playable experience, turn that idea into concrete requirements, direct a small implementation, play it, inspect the results, and revise it. In this course, the assistant is Claude Code and the game engine is Godot.

The important word is **playable**. A convincing description of a game is not a game. A generated script is not proof that the controls work. A successful test does not tell you whether a first-time player understands where to go.

Walker organizes the work around this cycle:

**Game brief → Build → Playtest → Inspect → Revise → Export**

- **Game brief:** State what the player does, what success looks like, what can go wrong, and what is outside the current scope. A game design document, or GDD, develops these decisions in more detail.
- **Build:** Ask the agent to implement one bounded change in the actual project.
- **Playtest:** Run the game and experience that change. Record what happened, not what the agent expected to happen.
- **Inspect:** Compare the behavior with your brief. Look at the relevant source, settings, errors, and evidence.
- **Revise:** Change the smallest responsible part and repeat the affected checks.
- **Export:** Produce and test the agreed distributable when the project is ready. An editor run is not an exported application, and an export is not a public release.

Walker is not another name for Godot. It is also not a promise that typing one sentence produces a finished game. The current course workflow uses project files and instructions that Claude Code can read. Do not assume that a shell command such as `walker build` exists. The working example is the [walker-jumpman source project](https://github.com/nikbearbrown/walker-jumpman).

### Who does what?

| Part of the system | Its job |
|---|---|
| You, the designer | Choose the experience, predict failures, approve changes, play the game, and judge the result. |
| Walker | Organize the brief, implementation, evidence, and revision workflow. |
| Claude Code | Read project files, propose changes, write authorized code, run available checks, and explain its work. |
| Godot | Execute the game: input, movement, collisions, graphics, interface, and game state. |
| GitHub | Preserve and share identifiable versions of the source and documentation. |
| Brutalist | Turn the game's design, code, and observed behavior into an explainer film. |

AI does the work you can specify and inspect. Humans own the purpose, trade-offs, and judgment. You can delegate implementation without delegating responsibility.

## What is Godot?

Godot is a free, open-source game engine and editor for building interactive 2D and 3D projects. The **editor** is the application you use to inspect and change a project. The **engine** runs its behavior. Godot handles recurring game-development needs so you do not have to build an input system, renderer, and physics engine from nothing.

Godot does not need an AI assistant to run a game. Claude Code helps create and modify the files that Godot uses. A change is not established by Claude saying “done”; it is established by inspecting those files and running the result.

### The vocabulary you need first

**Node:** A building block with a particular responsibility. A camera, a collision shape, and a controllable character can be different nodes.

**Scene:** A saved arrangement of nodes. A scene can represent a character, a menu, or a level; it does not have to be an entire game screen.

**Scene tree:** The hierarchy of nodes in the running game. Some nodes are saved in scene files; others can be created by code while the game runs.

**Signal:** An event notification that another part of the game can respond to—for example, a button being pressed. Not every interaction must use a signal; inspect how the supplied project actually works.

See [Godot's overview of its key concepts](https://docs.godotengine.org/en/stable/getting_started/introduction/key_concepts_overview.html).

**Script:** Code that defines behavior. This course starts with GDScript, Godot's integrated scripting language. Its syntax may look familiar if you know Python, but GDScript is not Python.

**Collision shape:** Geometry the physics system uses to detect contact. It is distinct from the artwork the player sees. Drawing a larger hat does not automatically make the character's collider taller.

**Asset:** Material a game uses, such as an image, model, font, or sound. The opening project draws its character and environment in code, so there is no character sprite file to replace by default. Godot also supports [custom 2D drawing](https://docs.godotengine.org/en/stable/tutorials/2d/custom_drawing_in_2d.html).

### Why Godot fits this course

A coding agent can read and edit the project's scripts, scene files, and structured level data. You can inspect the resulting changes in Git and then examine their consequences in the editor and the running game. That gives us a useful connection between **a request, a file change, and a visible result**.

We begin in 2D to make that connection easy to inspect. The course later develops 3D environments, art pipelines, shaders, particles, and other real-time systems. A small platformer is our starting point, not the limit of Godot or of the course.

## Before you begin

This course assumes that you have Claude Code access through Northeastern. Start at [Northeastern's Claude access page](https://claude.northeastern.edu/) for university access information. Resolve access problems before beginning graded work; you do not need to purchase API credits for this opening module.

Watch [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz). You may use AI throughout, but you must identify its contributions and be able to explain your submission.

Install the **regular Godot Engine**, not the .NET edition, for this GDScript starter. The supplied project was tested with Godot 4.7.2. Record the version you actually use and resolve version differences before interpreting test results. Use the [official downloads](https://godotengine.org/download/); the [.NET download](https://godotengine.org/download/macos/) is a separate option for C# support, which this starter does not require.

## Predict → Build It → Use It → Ship It → Verify

This is the course's learning template. Walker's development cycle operates inside it; inspection and testing recur throughout, not only at the end.

### 1. Predict

Before asking Claude to change anything, answer these questions in your own words:

- If the character's drawing changes but its collider does not, what should stay the same? What might become visually misleading?
- If the level becomes wider, what besides platform positions might need to change?
- What evidence would distinguish “the game starts” from “the extended level can be completed”?

Keep your original answers. A prediction that turns out to be wrong is useful evidence of learning.

### 2. Build It — start by understanding what already exists

For this practice, establish a working baseline before building anything new.

1. Obtain your own copy of [walker-jumpman](https://github.com/nikbearbrown/walker-jumpman). Claude Code can help you clone it and record the starting revision. Do not edit the instructor's repository.
2. In Godot's Project Manager, import **`godot/project.godot` inside the downloaded game folder**. This is an existing project; do not create an empty project over it.
3. Open the project and use **Run Project**. Start the game, move, jump, and reach the flag.
4. Ask Claude to explain the source without editing it.

Paste this request into Claude Code, not directly into a shell:

```text
We are using Walker's Game brief → Build → Playtest → Inspect → Revise → Export
workflow on this walker-jumpman project. First inspect only; do not edit.
Read README.md and BUILD-REPORT.md, then inspect godot/project.godot.
Locate the main scene, player drawing, movement rules, collision shape,
level data, game-state logic, camera, and tests. Explain each with an actual
file reference. Distinguish implemented features from proposals in GDD.md.
Tell me how to run the existing game and what I should observe.
```

The supplied starter separates several responsibilities:

| File inside the game package | What to inspect |
|---|---|
| `godot/project.godot` | Project settings and the main-scene reference. |
| `godot/game/main.tscn` | The saved entry scene. |
| `godot/game/session.gd` | Runtime world creation, input setup, game states, retry, finish, and camera behavior. |
| `godot/features/player/player.gd` | Character drawing, collider creation, and movement behavior. |
| `godot/features/player/tuning.gd` | Movement and jump parameters. |
| `godot/levels/first_steps.json` | Level dimensions, platforms, hazard, spawn, and finish data. |
| `godot/tests/` | Automated mechanics, keyboard, and route fixtures. |

The editor may initially show a very small scene tree: much of this starter's world is created by code at runtime. That is not evidence that the project is empty. Compare the saved scene with the running scene and its source.

### 3. Use It — learn the editor by asking questions

Use the **FileSystem** dock to find a script. Use the **Scene** dock to inspect the node hierarchy. Select a node and use the **Inspector** to examine its properties. Run the project and check the **Output/Debugger** panels when behavior differs from your expectation. These are tools for answering questions, not panels to memorize. See [Godot's editor introduction](https://docs.godotengine.org/en/stable/getting_started/introduction/first_look_at_the_editor.html).

In the starter, press **Enter** to start, **A/D or the arrow keys** to move, **Space** to jump, **R** to restart, and **Escape/P** to pause. Deliberately encounter a failure and observe the retry. Then finish and replay.

Read the [build report](https://github.com/nikbearbrown/walker-jumpman/blob/main/BUILD-REPORT.md) alongside the [GDD](https://github.com/nikbearbrown/walker-jumpman/blob/main/GDD.md). The larger design describes features beyond this small playable slice. A feature written in the GDD is not automatically implemented.

### 4. Ship It — preserve a baseline

Record your engine version, starting source revision, run instructions, and observations. Save the source through your version-control workflow so a later change has something concrete to be compared against.

For this practice, “ship” means a reproducible source snapshot. It does not mean publishing a game, uploading a video to YouTube, or claiming that a distributable export has been tested.

### 5. Verify — check your own understanding

These are **ungraded practice assessments**, not an additional assignment:

1. Explain the difference between Walker, Claude Code, and Godot without treating them as interchangeable.
2. Trace a jump from the input action to the movement code and the visible result.
3. Point to the character's visual code and its collision code. Explain why they are separate.
4. Identify one proposed GDD feature that the baseline does not implement.
5. State one thing an automated check can establish and one judgment that requires a person to play.

Do not paste Claude's explanation as proof of your understanding. Ask it to question you, then answer and check the source yourself.

## The next step

Open the separate Canvas assignment **“Assignment 1 - Extend Walker Jumpman.”** You will change the main character's visual identity, extend the playable level, and use a Brutalist Godot explainer to show what you built and how you checked it. That assignment has its own submission instructions and 100-point rubric; this lesson page does not add another graded deliverable.
