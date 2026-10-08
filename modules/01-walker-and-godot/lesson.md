# Module 1 — Walker and Godot

CSYE 7270 · Fall 2026 · Week 1

## Executive summary

This module introduces the three tools you will use all semester, Walker, Claude Code and Godot, and has you inspect a real, working game before you change anything. You trace one input, pressing Space, from the line that binds the key to the rectangle you see rise on screen, and you learn to tell "the agent says it works" apart from "the game works." The hands-on project is walker-jumpman, a small playable 2D platformer with 34 automated checks. By the end you have a baseline to compare every later change against, and you know which questions an automated check can answer and which only a person playing can. It does not make you a Godot expert in a week; it makes you hard to fool. Assignment 1 builds directly on it.

## The question

Change one line in walker-jumpman: the run speed in `godot/features/player/tuning.gd`, from `160.0` to `192.0`. Nothing else. Run the project's mechanics test and two of its 25 checks fail. One, `speed-cap`, is unsurprising. The other, `neutral-stop`, is a check about the player coming to rest when you let go of the keys, and on its face it has nothing to do with top speed. Meanwhile a scripted run over two gaps and a spike, which looks far more fragile, still reaches the flag.

Why does a stopping test fail when you change top speed? And if a capable agent can read every line of a small project and still mispredict, what is the human's job when an agent does the reading? This module gives you the machinery to answer both: what Walker, Claude Code and Godot each do, how a Godot project is put together, and how to check an agent's claim against the source.

## The ideas

### What is Walker?

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

#### Who does what?

| Part of the system | Its job |
|---|---|
| You, the designer | Choose the experience, predict failures, approve changes, play the game, and judge the result. |
| Walker | Organize the brief, implementation, evidence, and revision workflow. |
| Claude Code | Read project files, propose changes, write authorized code, run available checks, and explain its work. |
| Godot | Execute the game: input, movement, collisions, graphics, interface, and game state. |
| GitHub | Preserve and share identifiable versions of the source and documentation. |
| Brutalist | Turn the game's design, code, and observed behavior into an explainer film. |

AI does the work you can specify and inspect. Humans own the purpose, trade-offs, and judgment. You can delegate implementation without delegating responsibility.

### What is Godot?

Godot is a free, open-source game engine and editor for building interactive 2D and 3D projects. The **editor** is the application you use to inspect and change a project. The **engine** runs its behavior. Godot handles recurring game-development needs so you do not have to build an input system, renderer, and physics engine from nothing.

Godot does not need an AI assistant to run a game. Claude Code helps create and modify the files that Godot uses. A change is not established by Claude saying “done”; it is established by inspecting those files and running the result.

#### The vocabulary you need first

**Node:** A building block with a particular responsibility. A camera, a collision shape, and a controllable character can be different nodes.

**Scene:** A saved arrangement of nodes. A scene can represent a character, a menu, or a level; it does not have to be an entire game screen.

**Scene tree:** The hierarchy of nodes in the running game. Some nodes are saved in scene files; others can be created by code while the game runs.

**Signal:** An event notification that another part of the game can respond to—for example, a button being pressed. Not every interaction must use a signal; inspect how the supplied project actually works.

See [Godot's overview of its key concepts](https://docs.godotengine.org/en/stable/getting_started/introduction/key_concepts_overview.html).

**Script:** Code that defines behavior. This course starts with GDScript, Godot's integrated scripting language. Its syntax may look familiar if you know Python, but GDScript is not Python.

**Collision shape:** Geometry the physics system uses to detect contact. It is distinct from the artwork the player sees. Drawing a larger hat does not automatically make the character's collider taller.

**Asset:** Material a game uses, such as an image, model, font, or sound. The opening project draws its character and environment in code, so there is no character sprite file to replace by default. Godot also supports [custom 2D drawing](https://docs.godotengine.org/en/stable/tutorials/2d/custom_drawing_in_2d.html).

#### Why Godot fits this course

A coding agent can read and edit the project's scripts, scene files, and structured level data. You can inspect the resulting changes in Git and then examine their consequences in the editor and the running game. That gives us a useful connection between **a request, a file change, and a visible result**.

We begin in 2D to make that connection easy to inspect. The course later develops 3D environments, art pipelines, shaders, particles, and other real-time systems. A small platformer is our starting point, not the limit of Godot or of the course.

## The Walker example: walker-jumpman

[walker-jumpman](https://github.com/nikbearbrown/walker-jumpman) is a compact 2D platformer: a 960 × 360 level, two small steps, a 64 px and a 48 px gap, one three-spike hazard, and a finish flag. Start with Enter, move with A/D or the arrows, jump with Space, retry with R, pause with Escape or P. It is the control-and-retry slice of a larger design, not the full game its GDD describes: cherries, audio, settings, moving platforms and any export are not built.

Its checks are two headless Godot scripts. `tests/test_game.gd` has 25 checks (speed cap, stopping, wall contact, jump height, no double jump, coyote and buffer windows, spike contact, respawn, twenty consecutive retries, a scripted run of the real level, replay). `tests/test_keyboard.gd` has 9 checks that inject real key events through Godot's input system. On 27 September 2026 both passed on Godot 4.7.2, and the build report's numbers reproduced: a jump rise of 56.07 logical pixels, a longest automatic retry of 34 physics ticks, and a scripted route that reaches the flag with zero deaths and five jumps in 325 ticks.

What remains unverified is any human playtest: whether the jump reads well, whether a player sees the next landing in time, and any exported build. The repository has no license file, so use it as course material and credit it; do not assume you may redistribute it outside the course. The semester's example, [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd), changes only presentation (the character's drawing, plus a separate animation gallery) and keeps the same 34 checks, adding an animation test, `tests/test_clawd.gd`. Its change brief predicted what the numbers cannot settle: the wide Clawd art overhangs the unchanged 18 × 28 collider, so an arm can appear to touch a spike with no contact. That is recorded as an open question for a human playtest, not fixed silently.

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

Then, if you do the optional second task below, answer these about changing the run speed in `godot/features/player/tuning.gd` from `160.0` to `192.0`:

1. `speed-cap` holds right for 8 steps and then asserts the horizontal velocity equals exactly 160. Acceleration is 1280 px/s² at 60 ticks per second. If you raise the cap to 192, what velocity will the check observe? Do the arithmetic.
2. `neutral-stop` runs right after `speed-cap` in the same game and gives the player 5 ticks with no input to reach zero. Deceleration is 1920 px/s². Will 5 ticks still be enough?
3. The route driver presses jump at fixed x positions (138, 292, 424, 548, 712), tuned at 160 px/s. A jump lasts about 40 ticks. Will the route still finish with zero deaths at 192? Write yes or no and how confident you are.

### 2. Build It

Start by understanding what already exists. For this practice, establish a working baseline before building anything new.

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

#### Then trace one input

Paste this second prompt too. It is the trace prompt that was run on 27 September 2026 with Claude Code and with Codex, and its answers are what "What the agents got wrong" below checks.

```text
Inspect only; do not edit any file. This is the walker-jumpman project
(Godot 4.7.2, GDScript). Trace what happens when the player presses Space
during play, from the key to the jump the player sees on screen. For each
step give the file and line number: where the key is bound to an action,
where the action is read, where the jump velocity is applied, where gravity
and movement are integrated, and where the character is drawn. Then list
which checks in godot/tests/ exercise this path, by check id. Finish with
two short lists: what those tests establish about the jump, and what only
a person playing the game can judge.
```

Check the answer against the source yourself: open every file and line it cites, and mark each claim correct, wrong or unsupported.

#### Optional second task: change one number, prediction first

Make a branch for the experiment so `main` stays clean.

```bash
git switch -c experiment/run-speed-192
```

Then paste this into Claude Code. Add `--fixed-fps 60` to both test commands when you paste it: the original run omitted the flag, and for this project the result happened to be identical, but a frame-counted test should always have it.

```text
One bounded change in this walker-jumpman project (Godot 4.7.2, GDScript).
The change: in godot/features/player/tuning.gd set speed from 160.0 to 192.0.
Nothing else.

Before you edit anything, write PREDICTION.md. For every check id in
godot/tests/test_game.gd and godot/tests/test_keyboard.gd, say PASS or FAIL
after the change and give the reason from the test code. Then make the one
edit. Do not edit any test, level file, or other script.

Run these two commands and read their real output:
godot --headless --path godot --script res://tests/test_game.gd
godot --headless --path godot --script res://tests/test_keyboard.gd

Report each failing check id with its observed values, compare the results
with PREDICTION.md line by line, and show git diff. Do not try to make
a failing check pass. Tell me what a person should still check by playing.
```

Three sentences in that prompt do the real work. "Before you edit anything, write PREDICTION.md" makes the agent commit to a claim you can grade. "Do not edit any test" protects the design contract, because an agent asked to make tests pass will sometimes change the test. "Do not try to make a failing check pass" tells it a failure is an acceptable outcome. The syllabus calls this a prompt that is a specification, not a request: it names the one concern, the invariant, and what not to touch.

### 3. Use It

Use the **FileSystem** dock to find a script. Use the **Scene** dock to inspect the node hierarchy. Select a node and use the **Inspector** to examine its properties. Run the project and check the **Output/Debugger** panels when behavior differs from your expectation. These are tools for answering questions, not panels to memorize. See [Godot's editor introduction](https://docs.godotengine.org/en/stable/getting_started/introduction/first_look_at_the_editor.html).

In the starter, press **Enter** to start, **A/D or the arrow keys** to move, **Space** to jump, **R** to restart, and **Escape/P** to pause. Deliberately encounter a failure and observe the retry. Then finish and replay.

Read the [build report](https://github.com/nikbearbrown/walker-jumpman/blob/main/BUILD-REPORT.md) alongside the [GDD](https://github.com/nikbearbrown/walker-jumpman/blob/main/GDD.md). The larger design describes features beyond this small playable slice. A feature written in the GDD is not automatically implemented.

### 4. Ship It

Record your engine version, starting source revision, run instructions, and observations. Save the source through your version-control workflow so a later change has something concrete to be compared against.

For this practice, “ship” means a reproducible source snapshot. It does not mean publishing a game, uploading a video to YouTube, or claiming that a distributable export has been tested.

If you ran the optional experiment, commit it on its own branch with the failures in the message, then go back to `main`. It does not belong in Assignment 1, which asks you to preserve the movement tuning. If you later explain this work in a film, the fitting Brutalist skill is `godot-gamedev`, which walks through the actual code, scenes and tests and asks for an input to state to output trace.

### 5. Verify

Run the checks yourself. Do not rely on the agent's report. Both commands step the engine one sixtieth of a second per frame without waiting for the clock, and `timeout` stops a script error from hanging the run forever. If Godot reports missing resources or UID warnings on a fresh clone, run `godot --headless --path godot --import` once first (Module 0 explains why).

```bash
timeout 120 godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_keyboard.gd --fixed-fps 60
```

On the unmodified starter the mechanics test ends with `WALKER TESTS: 25 checks / 0 failures`. The keyboard test prints nine `PASS` lines and no summary: its exit code, 0, is the verdict. On the speed experiment branch you should see `25 checks / 2 failures` and exit code 1.

What a pass proves: at this engine version, the scripted inputs produce the tested states. What it does not prove: that a person can play the route, that the speed feels right, that landings are readable, or that anything outside these 34 checks still works. A failing check proves less than it seems, too. `speed-cap` failing at 192 is not a bug in the game. It is the test doing its job, telling you the build no longer matches the number the design specified. Whether to change the design (and then the GDD, then the test) or revert is a decision, and it is yours.

## What the agents got wrong

On 27 September 2026 the companion chapter's trace prompt (trace Space from the key to the jump on screen, with file and line numbers, inspect only) was run with Claude Code and with Codex, and their answers were checked line by line against the source. The mistakes are the lesson.

- **A wrong line number.** Claude cited gravity at `tuning.gd` line 5. Line 5 is deceleration; gravity is line 7. Every test line number it gave was right, which is exactly why the one wrong number is easy to miss.
- **A target reported as a measurement.** Claude said the jump "rises exactly ~53.3 px over 13 ticks." The test asserts a rise within 5 px of 53.33; the measured rise is 56.07 px, and 13 is the tick at which the test presses jump a second time. Codex repeated the same figure.
- **An overclaim about a test.** Claude said the route test proves the tuning constants are consistent with the level design. It proves that one scripted route reaches the flag.

Two agents, one prompt, different mistakes. The check is the source, not a second agent. And in the speed experiment, the agent's own prediction that the route would fail was wrong: it passed, because every landing in the first level is wide enough to absorb the extra distance. Nothing in the test, and nothing the agent read, said so in advance.

## If you know Unity or Unreal

| Godot | Unity | Unreal Engine 5 |
|---|---|---|
| Node | GameObject plus Components | Actor and its Components |
| Scene (`.tscn`, text) | Scene or Prefab, YAML under Force Text | Level or Blueprint class, binary |
| GDScript | C# MonoBehaviour | Blueprint graphs or C++ |
| `Resource` with `@export` | `ScriptableObject` asset | Data Asset |
| Signal | C# event or `UnityEvent` | Event Dispatcher or delegate |
| `godot --headless --script …` | `Unity -batchmode -runTests …` | `UnrealEditor-Cmd … -ExecCmds="Automation RunTest …"` |

The biggest difference for working with a coding agent is the file format. A Godot scene, resource and project file are plain text an agent can read and diff. Unity can store scenes as text, but they refer to each other through GUIDs that are hard to check by eye. Unreal's assets and levels are binary, so an agent cannot read or change a Blueprint by editing a file. Unity and Unreal were not run for this course material; the comparisons come from their official documentation, and the [companion chapter](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/01-walker-and-godot.md) has the full treatment.

## Practice assessment (ungraded)

These are ungraded practice questions, not an additional assignment. There is also an ungraded practice quiz in Canvas for this module; take it as often as you like and read the feedback.

These are **ungraded practice assessments**, not an additional assignment:

1. Explain the difference between Walker, Claude Code, and Godot without treating them as interchangeable.
2. Trace a jump from the input action to the movement code and the visible result.
3. Point to the character's visual code and its collision code. Explain why they are separate.
4. Identify one proposed GDD feature that the baseline does not implement.
5. State one thing an automated check can establish and one judgment that requires a person to play.

Do not paste Claude's explanation as proof of your understanding. Ask it to question you, then answer and check the source yourself.

## The next step

Open the separate Canvas assignment **“Assignment 1 - Extend Walker Jumpman.”** You will change the main character's visual identity, extend the playable level, and use a Brutalist Godot explainer to show what you built and how you checked it. That assignment has its own submission instructions and 100-point rubric; this lesson page does not add another graded deliverable. The full chapter, [Walker and Godot](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/01-walker-and-godot.md), has the complete record of the agents' runs.
