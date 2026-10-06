# Chapter 1 — Walker and Godot

## Executive summary

This chapter teaches you to read a real Godot project through a coding agent and to change it without fooling yourself. The project is `walker-jumpman`, the small 2D platformer that every student in CSYE 7270 starts from, and the agent is Claude Code (or Codex) run from the command line. You will trace one keypress, Space, from the line that binds it to the rectangle you see rise on screen, then change one number, the run speed, after predicting which of the project's 34 automated checks will fail. We did exactly this on September 27, 2026: the agent's trace was mostly right and wrong or unsupported in four specific places, the speed change broke two checks, one of them a check about stopping rather than speed, and the check that looked most at risk passed. The build proves that the project's headless checks detect a design change and that you can reproduce and read them. It does not prove the faster game is better, readable, or fun; only a person playing can judge that. It is also not Assignment 1: you will not touch the character or the level here.

## The question

Open `godot/features/player/tuning.gd` in walker-jumpman and change one line: the run speed, from `160.0` to `192.0`. Nothing else. Then run the project's mechanics test. Two of its 25 checks fail. The first, `speed-cap`, is unsurprising. The second, `neutral-stop`, is a check about the player *coming to rest* when you let go of the keys, and on its face it has nothing to do with top speed. Meanwhile the check that looks most fragile, a scripted run over two gaps and a spike that presses jump at fixed positions, still reaches the flag with zero deaths.

Before the change we asked Claude Code to predict all of this. It predicted both failures correctly, with the exact observed values, and predicted that the scripted route would fail. It passed.

So there are two puzzles. Why does a stopping test fail when you change top speed? And if a capable agent can read every line of a project with 352 lines of game code and still mispredict, what exactly is the human's job when an agent does the reading? The answer to both is the same machinery: fixed-rate physics ticks, tests that encode design numbers, and state that carries from one check to the next. This chapter takes that machinery apart.

## Ideas you need

### Walker is a method and a set of files, not a program you run

Walker is the course's framework for building games through a structured conversation with an AI coding agent. Its loop is **Game brief → Build → Playtest → Inspect → Revise → Export** ([Walker README](https://github.com/nikbearbrown/walker)). The framework repository contains instructions and tools, not games. Its publisher, `publish.sh`, writes an agent manifest (`CLAUDE.md` or `AGENTS.md`), an engine guide, and the `asset-gen` skill into a new game folder, then runs `git init` there. It does not create a playable game, and there is no `walker` shell command. Each game lives in its own `walker-*` repository. One version note: on September 27, 2026 the public repository's `main` (commit `10fedb8`, September 11) is older than the instructor's working copy, which adds the `/gdd` design skill used in Chapter 5 and a `publish.sh` that installs it. Until that change is published, what you clone is the older version.

One honest warning before you read the framework: its bundled Godot guide, `engines/godot.md`, targets Godot's **C#/.NET** build. The Walker README says so itself. This course uses the regular Godot editor and **GDScript**, which is what walker-jumpman is written in. Do not install .NET for this chapter, and do not follow the C# scene-builder advice in that guide when you work on walker-jumpman.

### The project: a text file and a virtual file system

A Godot project is a folder with a `project.godot` file at its root. That file is plain text in an INI-like format, and `res://` always means "the folder that contains `project.godot`" ([File system](https://docs.godotengine.org/en/stable/tutorials/scripting/filesystem.html)). In walker-jumpman the project is the `godot/` subfolder, which is why every command in this chapter says `--path godot`. Its `project.godot` sets the main scene (`res://game/main.tscn`), a 640 × 360 logical viewport shown in a 1280 × 720 window, the Compatibility (OpenGL) renderer, 60 physics ticks per second, and names for four 2D physics layers.

### Nodes, scenes, and the scene tree

A **node** is the smallest building block; a **scene** is a saved arrangement of nodes; the **scene tree** is the running hierarchy all scenes join ([Key concepts](https://docs.godotengine.org/en/stable/getting_started/introduction/key_concepts_overview.html)). Scenes are saved as `.tscn` text: a header, external resources, internal resources, nodes, and signal connections ([TSCN format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html)). Because the format is text, an agent can read it and `git diff` can show you what changed.

walker-jumpman's saved scene is almost empty. `godot/game/main.tscn` is six lines: one `Node2D` named `WalkerJumpman` with `session.gd` attached. (It still carries a `load_steps=2` attribute, which the Godot docs now describe as deprecated since 4.6 and ignored; it is harmless.) Everything else is built by code when the game starts. `session.gd`'s `_ready()` reads the level JSON, then creates one `StaticBody2D` per solid (five from the level plus two invisible side walls), one `Area2D` per hazard and one for the goal, the player, a `Camera2D`, and a `CanvasLayer` holding the HUD. If you open the project in the editor and see one node, the project is not empty; it is procedural. The editor's **Remote** tab in the Scene dock shows the tree of the *running* game ([Debugging tools](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html)).

### Scripts and the two clocks

A **script** attaches behavior to a node. GDScript is indentation-based and looks like Python, but the docs are explicit that it "is entirely independent from Python and is not based on it" ([GDScript basics](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html)).

Godot calls your scripts on two clocks. `_process(delta)` runs once per rendered frame, as often as the machine can manage. `_physics_process(delta)` runs at a fixed rate, 60 times per second by default, set in Project Settings ([Idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)). walker-jumpman does all gameplay in `_physics_process`, so every number in its tuning is "per second" but every change happens in steps of 1/60 s. That is the first half of the answer to this chapter's question.

The order of physics callbacks matters too. Nodes with a *lower* `process_physics_priority` run first ([Node](https://docs.godotengine.org/en/stable/classes/class_node.html)). `session.gd` sets its own priority to 10, so on every tick the player (priority 0) moves first and the session checks hazards and the goal afterwards, against the position the player just reached.

### Input: actions, not keys

Godot separates *keys* from *actions*. An action such as `jump` is a name with any number of input events bound to it, and code asks about the action ([Input examples](https://docs.godotengine.org/en/stable/tutorials/inputs/input_examples.html)). Usually actions live in Project Settings; walker-jumpman has no `[input]` section in `project.godot` at all. Instead `session.gd` builds the map in `_setup_input()` (line 48), binding physical key positions: A/D and arrows to move, Space to jump, Escape/P to pause, R to restart, Enter to confirm, M for menu. Physical keycodes represent "the physical location of a key on the 101/102-key US QWERTY keyboard," which the docs recommend for WASD-style controls ([InputEventKey](https://docs.godotengine.org/en/stable/classes/class_inputeventkey.html)).

There are two ways to read input and this project uses both. The player *polls* each tick: `Input.is_action_just_pressed("jump")` is true only on the frame or physics tick the press began ([Input](https://docs.godotengine.org/en/stable/classes/class_input.html)). The session *receives events* in `_unhandled_input()` for menu keys. Tests can feed either path: `Input.action_press()` simulates an action, and `Input.parse_input_event()` "feeds an InputEvent to the game," exactly as a keyboard would.

### Bodies, shapes, layers

Godot has four collision-object types ([Physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html)). A `StaticBody2D` does not move but can be hit. A `RigidBody2D` is moved by simulated forces. A `CharacterBody2D` "provides collision detection, but no physics. All movement and collision response must be implemented in code." An `Area2D` detects overlaps and can emit signals when bodies enter or exit.

The player is a `CharacterBody2D`. Its script sets `velocity` and calls `move_and_slide()`, which moves the body, slides it along whatever it hits, and updates `is_on_floor()` for the next check; you do not multiply the velocity by `delta` yourself ([Using CharacterBody2D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html)).

A **collision shape** is separate from anything drawn. The player's collider is an 18 × 28 rectangle offset 14 px upward (`player.gd`, `_ready()`), and its drawing is seven rectangles in `_draw()`. Change one and the other does not follow. That separation is the whole point of Assignment 1's warning about a larger hat.

Layers and masks decide who can touch whom. `collision_layer` is where an object *is*; `collision_mask` is what it *scans for*. In code both are bitmasks: layer *n* has the value 2^(n−1), so layer 5 is the value 16. walker-jumpman names layer 4 "Hazard" and layer 5 "Goal" in `project.godot`, and `session.gd` puts spikes on value 8 and the goal on value 16. Those match. Keep this rule in your head; in Chapter 5 you will see an agent get it wrong.

### Areas are snapshots, and snapshots go stale

walker-jumpman does not wait for a signal when the player touches spikes. Each physics tick the session *asks* `hazard.overlaps_body(player)`. The Godot docs warn that the overlap list "is updated once per frame and before the physics step" ([Area2D/Area3D](https://docs.godotengine.org/en/stable/classes/class_area3d.html)). That warning explains a real bug in this project's history. The first test run found four failures, including a *second* death after respawn: the player had been teleported to the start, but the overlap snapshot still said "touching spikes" ([BUILD-REPORT](https://github.com/nikbearbrown/walker-jumpman/blob/main/BUILD-REPORT.md)). The fix is visible in `restart_attempt()`: `contact_settle_ticks = 2` discards two ticks of contact reports after a reset. When you read a line like that, ask what failure it prevents. The code usually tells you if you look.

### Resources: data with a type

A **resource** is a data container that nodes use; you make your own by extending `Resource` and marking fields `@export` ([Resources](https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html)). `tuning.gd` is such a class: speed 160, acceleration 1280, deceleration 1920, jump velocity −320, gravity 960, terminal velocity 480, coyote 6 ticks, buffer 6 ticks. Its comment says "Values from GDD 0.2.0. A shared resource for gameplay and fixtures." Notice two things. The player creates it with `Tuning.new()`, not by loading a `.tres` file, so there is no asset to open in the Inspector. And the test fixtures do *not* read it: `test_game.gd` writes the literal `160` into its speed check. The comment says one thing; the tests do another. That gap is the second half of this chapter's answer.

### Drawing

The player and level are drawn with `_draw()` in the node's local coordinates. Godot calls `_draw()` once and caches the result until you call `queue_redraw()` ([Custom drawing in 2D](https://docs.godotengine.org/en/stable/tutorials/2d/custom_drawing_in_2d.html)). That is why `player.gd` calls `queue_redraw()` at the end of every physics tick: without it, the picture would not update even though the body moved.

### Running Godot without a window

Everything you verify in this course you verify headless. The relevant options ([Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)):

| Option | What the docs say it does |
|---|---|
| `--headless` | Headless display and dummy audio; "useful for servers and with `--script`" |
| `--path <dir>` | The folder that contains `project.godot` |
| `--script <file>` | Run a script; it "must inherit from `SceneTree` or `MainLoop`" |
| `--fixed-fps <n>` | "Force a fixed number of frames per second. This setting disables real-time synchronization." |
| `--import` | Start the editor, wait for resources to import, then quit |
| `-- <args>` | Arguments after `--` are ignored by the engine and read with `OS.get_cmdline_user_args()` |

walker-jumpman's tests are `SceneTree` scripts. Each builds a fresh game, drives it, prints one JSON line per check, writes a JSON report into `evidence/` beside the `godot/` folder, and calls `quit(1)` if anything failed. The exit code is the verdict; the printed lines are the evidence.

Read Chapter 0's section "The time trap: frames are not seconds" before you trust any headless number. Its point, in one line: a test that counts *frames* while the game moves by *seconds* measures a different amount of game time on every machine unless you pin the time step with `--fixed-fps 60`. walker-jumpman happens to be immune. Every gameplay change happens in `_physics_process`, whose `delta` is always one physics tick, and the test helper `steps()` waits for `physics_frame` before it counts. Its tests count physics ticks, not rendered frames, and we got identical numbers with and without the flag. Pass the flag anyway. It costs nothing, it makes the run take a third of a second instead of twenty, and the next project you test will not be immune.

One more guard. If a test script hits a runtime error before it calls `quit()`, headless Godot does not exit; it sits there with no window until you kill it. We checked with a deliberate error: Godot printed the `SCRIPT ERROR` and was still running when `timeout 15` killed it (exit code 124). Every test command in this chapter is therefore wrapped in `timeout 120`, which turns a hang into a failure you can see. macOS does not ship `timeout`; Homebrew's `coreutils` package provides it (on the instructor's Mac, coreutils 9.11 installs both `timeout` and `gtimeout`).

### What an agent can read

| Godot artifact | Format | Can an agent read and diff it? |
|---|---|---|
| `project.godot` | INI-like text | Yes |
| `.tscn`, `.tres` | Text | Yes, but references by path and UID are easy to break |
| `.gd` | Text | Yes |
| `levels/*.json` | Text | Yes |
| `*.uid` | One-line text | Yes; commit them. Since Godot 4.4 scripts get a `.uid` file, and forgetting to commit them breaks references on another machine ([UID changes in 4.4](https://godotengine.org/article/uid-changes-coming-to-godot-4-4/)) |
| `.godot/` | Editor cache | Do not commit ([Version control](https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html)) |
| Imported textures, models, audio | Binary | No; the agent sees file names and `.import` settings, not pictures or sounds |

walker-jumpman draws everything in code and loads no image, model, or sound, so every behavior in it is visible to an agent as text. That is unusual, and it is why we start here.

### The two coding CLIs

Both tools can run without an interactive session, which is how we produced this chapter's record.

- **Claude Code**: `claude -p "<prompt>"` prints a response and exits ([CLI reference](https://code.claude.com/docs/en/cli-reference)). `--permission-mode acceptEdits` lets it edit files without asking. `--allowedTools` lists tools that run *without prompting*; the docs are explicit that it does not restrict what is available: "To restrict which tools are available, use `--tools` instead." Separately, Claude Code treats a built-in set of Bash commands, including `ls`, `cat`, `grep`, `find`, and read-only `git`, as read-only and runs them without a prompt in every mode ([Permissions](https://code.claude.com/docs/en/permissions)). `--output-format stream-json --verbose` writes every step as JSON lines, which is your transcript.
- **Codex**: `codex exec "<prompt>"` runs non-interactively, and "by default, `codex exec` runs in a read-only sandbox"; add `--sandbox workspace-write` to let it edit ([Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)). `--json` writes JSON lines; `-o <file>` saves the final message.

Project instructions differ. Codex reads `AGENTS.md` files from the project root down to the working directory ([AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)). Claude Code reads `CLAUDE.md`; its docs say it can read `AGENTS.md` directly only from version 2.1.277 on ([Memory](https://code.claude.com/docs/en/memory)). This matters for `walker-jumpman-clawd`, which ships an `AGENTS.md` and no `CLAUDE.md`. In our run with Claude Code 2.1.150 inside a copy of that repository, the agent reported that no project instruction file had been loaded. If your version is older than 2.1.277, start your first prompt with "Read AGENTS.md first," or add a one-line `CLAUDE.md` containing `@AGENTS.md`.

## The Walker example: walker-jumpman

**What it is.** A compact 2D platformer: a 960 × 360 level, two small steps, a 64 px and a 48 px gap, one three-spike hazard, and a finish flag. Start with Enter, move with A/D or arrows, jump with Space, retry with R, pause with Escape or P. It is the "control/retry slice" of a larger design, not the full game its GDD describes: cherries, the three-zone course, audio, settings, moving platforms, and any export are not built ([README](https://github.com/nikbearbrown/walker-jumpman), [BUILD-REPORT](https://github.com/nikbearbrown/walker-jumpman/blob/main/BUILD-REPORT.md)).

**Where it came from.** I asked for it on September 10, 2026 ("Build a simple level for walker-jumpman"). The public repository is `github.com/nikbearbrown/walker-jumpman`; its `main` branch was at commit `9387542ca473b0a252c43bfe6d4fd39b61f8d439` when this chapter was checked (September 27, 2026). The design traces back further than Godot: the GDD's source-evidence table lists an older Unity `PlayerMovement.cs` that used a `Rigidbody2D` with speed and jump both set to 7, and records the decision to "preserve intent, not units." Every tuning value in `tuning.gd` is a new Godot proposal from GDD 0.2.0, not a port.

**License.** The repository has no license file. Its GDD treats asset provenance carefully, and the sibling Clawd repository says plainly that "public availability is not itself a license grant." Use it as course material and credit it; do not assume you may redistribute it outside the course.

**What its checks establish.** On Godot 4.7.2 the project ships two headless test scripts:

- `tests/test_game.gd`, 25 checks: speed cap, stopping, opposing inputs, wall contact, jump height, no double jump, held-jump bounce, coyote and buffer windows at 5, 6, and 7 ticks, a low ceiling, pause and focus loss, real spike contact, duplicate-death suppression, respawn, manual restart, twenty consecutive retries, death-before-finish precedence, the fall boundary, a scripted run of the real level, and replay.
- `tests/test_keyboard.gd`, 9 checks that inject real key events through Godot's input system: start, move, jump, pause, resume, retry, replay, menu, and restart from menu.

The build report records the numbers: a jump rise of **56.07 logical pixels**, a longest automatic retry of **34 physics ticks** (about 0.567 s), and a scripted route that reaches the flag with **zero deaths, five jumps, in 325 ticks**. We reproduced all three on September 27. The report is honest about what these mean: the coyote and buffer boundaries "explicitly seed controller timing state; they are unit fixtures," and the route is "a fast known route," not a prediction of a new player's time.

**What remains unverified.** Any human playtest (the design status records none), whether the jump reads well, whether players see the next landing in time, and any exported build (export templates were absent).

**The semester example: walker-jumpman-clawd.** `github.com/nikbearbrown/walker-jumpman-clawd` (`main` at `382f2ba`) is my running example for the course. Iteration 1 replaces the character's drawing with Clawd, the Claude mascot, using 18 code-drawn animations ported from Brutalist, and adds a separate animation gallery. It changes presentation only: its log records that the physics function, tuning resource, level JSON, and HUD are byte-identical to the starter, the 18 × 28 collider is unchanged, and gameplay uses six of the 18 animations. Its checks are the same 25 and 9, plus `tests/test_clawd.gd`, which compares 162 animation samples from a TypeScript reference; we ran it and it reported 1,950 checks with zero failures. Its `CHANGE-BRIEF.md` predicted the one thing the numbers cannot settle: the wide Clawd art overhangs the unchanged 18 × 28 collider, so an arm can appear to touch a spike without any contact. That is recorded as an open question for a human playtest, not fixed silently. Read its `FRICTIONAL.md` for what an honest log looks like: two capture failures, a malformed script, a rejected take, each kept.

## Hands-on: trace one input, then change one number

You will work on your own clone, on a branch you will not merge. The task has two prompts. The first is inspect-only. The second makes one edit after a written prediction.

### Predict

Write your answers in your notes before you run anything. Keep them even if they turn out wrong.

1. Where is the Space key bound to the `jump` action? (Guess the file before you look.)
2. `speed-cap` holds right for 8 steps and then asserts the horizontal velocity equals exactly 160. Acceleration is 1280 px/s² at 60 ticks per second. If you raise the cap to 192, what velocity will the check observe? Do the arithmetic.
3. `neutral-stop` runs right after `speed-cap` in the same game and gives the player 5 ticks with no input to reach zero. Deceleration is 1920 px/s². Will 5 ticks still be enough?
4. The route driver presses jump at fixed x positions (138, 292, 424, 548, 712), tuned at 160 px/s. A jump lasts about 40 ticks. Will the route still finish with zero deaths at 192? Write yes or no and how confident you are.

### Build It

Clone the starter and record where you started.

```bash
git clone https://github.com/nikbearbrown/walker-jumpman.git
```

```bash
cd walker-jumpman
```

```bash
git rev-parse HEAD
```

```bash
godot --version
```

Run both test scripts before you change anything. `--fixed-fps 60` makes the engine step exactly one sixtieth of a second per frame without waiting for the wall clock; without it the mechanics test takes about 22 seconds, with it about a third of a second, and on our machine the results were identical.

```bash
timeout 120 godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_keyboard.gd --fixed-fps 60
```

```bash
echo $?
```

The mechanics test ends with `WALKER TESTS: 25 checks / 0 failures`. The keyboard test prints nine `PASS` lines and no summary; its exit code (0) is the verdict. Now make a branch for the experiment.

```bash
git switch -c experiment/run-speed-192
```

**Prompt 1: trace, no edits.** Start Claude Code in the repository (`claude`) and paste this, or run it headless as shown after it.

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

To run it headless and keep a transcript, make a `notes/` folder (`mkdir -p notes`), save the prompt as `notes/prompt-1-trace.txt`, and run:

```bash
claude -p "$(cat notes/prompt-1-trace.txt)" --permission-mode default --allowedTools "Read,Glob,Grep" --max-turns 40 --output-format stream-json --verbose > notes/session-1-trace.jsonl
```

That is the command we ran. It pre-approves reading tools; it does not forbid others, and our agent did run `find` through Bash, which Claude Code allows as a read-only command. If you want the agent physically unable to do anything but read, replace `--allowedTools "Read,Glob,Grep"` with `--tools "Read,Glob,Grep"`.

The Codex equivalent is read-only by default. The trailing `< /dev/null` matters when you run it from a script or in the background: without it, `codex exec` can sit waiting on "Reading additional input from stdin."

```bash
codex exec --json -o notes/codex-trace.md "$(cat notes/prompt-1-trace.txt)" < /dev/null > notes/codex-trace.jsonl
```

Check the answer against the source yourself: open every file and line it cites. Mark each claim correct, wrong, or unsupported.

**Prompt 2: one change, prediction first.**

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

Headless form, saved as `notes/prompt-2-tuning.txt`:

```bash
claude -p "$(cat notes/prompt-2-tuning.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*)" --max-turns 60 --output-format stream-json --verbose > notes/session-2-tuning.jsonl
```

That prompt is printed exactly as we ran it, and its two test commands omit `--fixed-fps 60`. For this project that does not change the result (see "Running Godot without a window" above), and we reran everything with the flag in Verify. In your own prompts, include the flag in every test command you hand an agent: in Chapter 0's runs, neither Claude Code nor Codex added it on its own.

Three sentences in that prompt do the real work. "Before you edit anything, write PREDICTION.md" makes the agent commit to a claim you can grade. "Do not edit any test" protects the design contract: an agent asked to make tests pass will sometimes change the test. "Do not try to make a failing check pass" tells it a failure is an acceptable outcome. The syllabus calls this writing a prompt that is "a specification, not a request": it names the one concern, the invariant, and what not to touch.

For Codex, the edit needs a writable sandbox. We ran only the read-only trace under Codex for this chapter; whatever either agent reports about the tests, you will rerun them yourself in Verify.

```bash
codex exec --sandbox workspace-write "$(cat notes/prompt-2-tuning.txt)" < /dev/null
```

### Use It

This part needs a display, so it is yours to do; we did not do it for this chapter. Open Godot's Project Manager, import `godot/project.godot`, and press Run.

1. While the game runs, switch the Scene dock to **Remote**. From `session.gd` you should expect seven `StaticBody2D` nodes, two `Area2D` nodes, the player, a `Camera2D`, and a `CanvasLayer` with the HUD. Confirm or correct that from what you see.
2. Play the route at 192. Then `git stash`, play at 160, and `git stash pop`. The GDD gives the reason for 160 px/s in one phrase: it "allows course reading within the viewport." At 192, can you still see the next landing before you have to commit to the jump? That is a judgment about the design, and no check in this project measures it.
3. Jump into the spikes on purpose. Watch the retry. Does anything about the faster speed change how the failure reads?

Write what you observed, not what you expected.

### Ship It

"Ship" here means a reproducible snapshot of an experiment, not a release. Commit the experiment on its branch with the failures in the message, then go back to `main`. This change does not belong in Assignment 1, which asks you to preserve the movement tuning.

```bash
git add godot/features/player/tuning.gd PREDICTION.md
```

```bash
git commit -m "Experiment: run speed 160 -> 192; speed-cap and neutral-stop fail, route passes"
```

```bash
git switch main
```

Add an entry to your `FRICTIONAL.md` in the course's format: date and session, intention, your prediction, the actual attempt, what failed or surprised you, the evidence (commands, commit hash, check ids and values), what you changed or rejected, retest and limits, human versus AI contributions, and one next step. If your route prediction was wrong, say so and say why.

If you later explain this work in a film, the fitting Brutalist skill is **godot-gamedev**: it walks through the actual code, scenes, and tests and asks for an input → state → output trace, which is exactly what Prompt 1 produced. This exercise does not require a film.

### Verify

Run the checks yourself on the experiment branch, then on `main`. Do not rely on the agent's report.

```bash
git switch experiment/run-speed-192
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

```bash
git switch main
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_keyboard.gd --fixed-fps 60
```

On the branch you should see `25 checks / 2 failures` and exit code 1; on `main`, `25 checks / 0 failures` and nine keyboard passes.

What a pass proves: at this engine version, the scripted inputs produce the tested states. What it does not prove: that a person can play the route, that the speed feels right, that landings are readable, or that anything outside these 34 checks still works. A failing check proves less than it seems, too: `speed-cap` failing at 192 is not a bug in the game; it is the test doing its job, telling you the build no longer matches the number the design specified. Whether to change the design (and then the GDD, then the test) or revert is a decision, and it is yours.

## What we actually ran

**When and with what.** September 27, 2026, on macOS with an Apple M4 Pro. Godot `4.7.2.stable.official.ed1daf0bf`. Claude Code 2.1.150; the transcript records the model as `claude-sonnet-4-6`, the account's default (we did not pass `--model`). Codex CLI 0.153.4 with the model set in the local Codex config (`gpt-5.6-sol`, reasoning effort low). Starting revision: walker-jumpman `9387542`, copied (the `godot/` folder and Markdown files only) into a scratch folder and committed as a local baseline. The full record, including trimmed transcripts, is in [`../examples/01-walker-and-godot/`](../examples/01-walker-and-godot/).

**Baseline.** Both scripts passed: 25 of 25, then 9 of 9. Real-time, the mechanics test took 22.4 s; with `--fixed-fps 60`, 0.34 s, with the same observed jump rise (56.07 px), longest retry (34 ticks), and route (325 ticks).

```text
{"id":"fixed-jump-and-no-double","observed":{"jumps":1,"rise_px":56.07470703125},"status":"PASS"}
{"id":"complete-real-route","observed":{"deaths":0,"jump_marks_used":5,"position":"(912.8837, 319.9253)","state":4,"ticks":325},"status":"PASS"}
WALKER TESTS: 25 checks / 0 failures
```

**Prompt 1, the trace (Claude Code, 10 turns, 1 min 36 s).** The agent read the right files and cited the right lines for the binding (`session.gd:48`), the reads (`player.gd:46–47`), the jump (`player.gd:61–65`), integration (`player.gd:57, 60, 66`), and drawing (`player.gd:68, 70`), and every test line number it gave was correct. It also noticed that `project.godot` has no `[input]` section. Checked line by line, four claims failed:

- It cited gravity at `tuning.gd` line 5. Line 5 is deceleration; gravity is line 7.
- It said the jump "rises exactly ~53.3 px over 13 ticks." The test asserts a rise within 5 px of 53.33, the textbook value; the measured rise is 56.07 px. And 13 is the tick at which the test presses jump a second time, not the rise time, which is about 20 ticks (320 ÷ 960 s).
- It described the buffer checks as "a press recorded 5–6 ticks before the player touches down." The test starts on the floor and seeds `jump_request_tick` directly. The build report calls these unit fixtures for exactly that reason.
- It said the route test proves "the tuning constants are internally consistent with the level design." It proves that one scripted route reaches the flag.

It also ran `find` through Bash although only Read, Glob, and Grep were pre-approved, which Claude Code permits as a read-only command. No file changed.

**The same prompt under Codex (53 s, read-only sandbox).** Codex cited gravity at the correct line and drew a distinction Claude missed: only `keyboard-jump` exercises the physical Space binding; the other checks drive the controller through test variables. It repeated the "approximately 53.3 px" figure, which is the test's target, not the measurement. Two agents, one prompt, different mistakes: the check is the source, not a second agent.

**Predictions, written before Prompt 2.** Ours, written for this example by the agent that drafted the chapter, standing in for a student, and timestamped in `author-prediction.md` before any run: `speed-cap` fails near 170.7, `neutral-stop` fails because its 5-tick braking budget (5 × 32 = 160 px/s) was sized for exactly 160, the route "lean PASS, low confidence," everything else passes. The agent's `PREDICTION.md`: the same two failures with the same arithmetic, plus a third, the route, because "at 192 the player lands ~21 px further per jump, likely overshooting platforms."

**Prompt 2, the change (Claude Code, 13 turns, 4 min 7 s).** The agent wrote `PREDICTION.md`, changed one line, ran both scripts, did not touch a test, and reported honestly that its route prediction was wrong. The diff, apart from the new `PREDICTION.md`:

```text
--- a/godot/features/player/tuning.gd
+++ b/godot/features/player/tuning.gd
-@export var speed: float = 160.0
+@export var speed: float = 192.0
```

**Our own verification.** The agent ran the tests without `--fixed-fps 60`, as the prompt told it to, and so did our first rerun. We then reran both scripts ourselves on the branch with the flag, and the check values below were identical in both modes:

```text
{"id":"speed-cap","observed":{"velocity_x":170.666656494141},"status":"FAIL"}
{"id":"neutral-stop","observed":{"velocity_x":10.6666564941406},"status":"FAIL"}
{"id":"complete-real-route","observed":{"deaths":0,"jump_marks_used":5,"position":"(915.7248, 319.9253)","state":4,"ticks":280},"status":"PASS"}
WALKER TESTS: 25 checks / 2 failures
```

Exit code 1. Keyboard: 9 of 9. The route finished 45 ticks sooner. (Our runs were not wrapped in `timeout`; none hung.) We committed the experiment on its branch (`ed4ec86` in the scratch repository), switched to `main`, and reran with and without the flag: 25 of 25 and 9 of 9 each time.

**The answer to the question.** `neutral-stop` fails because it inherits state: it begins wherever `speed-cap` left the player, and its budget of five 32 px/s decrements was written for a player at exactly 160. The route survives because every landing in First Steps is wide enough to absorb about 21 extra pixels per jump; nothing in the test knew that in advance, and neither did the agent. And the human's job is not to read faster than the agent. It is to hold the claim against the source, run the check yourself, and decide what a failure means.

Nothing went wrong that needed correcting in this run; the "failures" are the intended result of an unapproved design change. What we did not do: open the editor, play either speed, or judge readability. Those are human checks.

## Check your understanding (ungraded)

1. `session.gd` sets `process_physics_priority = 10`. Using the Node documentation, explain in which order the player and the session run each tick. What would the hazard check see if the session ran first?
2. Find `contact_settle_ticks` in `session.gd`. Which failure in the first test run does it prevent, and why does `overlaps_body()` make that failure possible?
3. The player's collider is created in code. Give its size and offset, and point to the line in `_draw()` that makes the drawing wider than the collider when the character faces left.
4. The keys are bound with `physical_keycode`. On a French AZERTY keyboard, which printed key moves the player left, and why is that the intended behavior?
5. `neutral-stop` would pass at speed 192 if it had more ticks. Should you change the test? Argue both sides, then say what document would have to change first.
6. Run `test_game.gd` with and without `--fixed-fps 60`. Compare wall time and the `ticks` value of `complete-real-route`. What does the flag change, and what does it leave alone?

## Doing the same thing in Unity

Unity and Unreal were the engines this course used through Spring 2026. Neither was run for this chapter; the comparisons below come from their official documentation.

### Similarities

The shape of the task carries over. Unity also separates a fixed-rate physics callback (`FixedUpdate`, performed at the interval `Time.fixedDeltaTime`) from the per-frame `Update` ([Time.fixedDeltaTime](https://docs.unity3d.com/ScriptReference/Time-fixedDeltaTime.html)), so a tuning change also lands in discrete steps and a stopping test can inherit state exactly as ours did. Unity also stores most of a project as text. Its default asset serialization mode is **Force Text** ([Editor settings](https://docs.unity3d.com/Manual/class-EditorManager.html)), which writes scenes and prefabs as YAML ([Text-based scene files](https://docs.unity3d.com/Manual/YAMLSceneExample.html)), and its Input System stores actions in `.inputactions` files in plain JSON ([Input action assets](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.18/manual/ActionAssets.html)). An agent can read both. Unity keeps a regenerable cache, the `Library` folder, that you do not commit ([Default project directories](https://docs.unity3d.com/6000.0/Documentation/Manual/default-directories.html)), just as Godot keeps `.godot/`.

Unity can also run tests without a person. The Unity Test Framework is NUnit-based; a `[UnityTest]` returns `IEnumerator`, runs as a coroutine in Play Mode, and can `yield return new WaitForFixedUpdate()` to step physics ([UnityTest attribute](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-attribute-unitytest.html)). The Input System's `InputTestFixture` provides `Press`, `Release`, and `PressAndRelease` against virtual devices ([Input testing](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.4/manual/Testing.html)), the equivalent of our `Input.parse_input_event`.

### Differences

Here is this chapter's task in Unity. The run speed would live in a `ScriptableObject` asset (a `PlayerTuning.asset`), a serializable data type that exists "in the project as assets, independent of GameObjects" ([ScriptableObject](https://docs.unity3d.com/Manual/class-ScriptableObject.html)). Under Force Text that asset is YAML, so the diff is readable, but the scene references it through a GUID stored in the asset's `.meta` file ([Asset metadata](https://docs.unity3d.com/Manual/AssetMetadata.html)). An agent that edits YAML by hand can produce a file that parses and silently points at nothing; Godot's `res://` paths and `.uid` files carry the same risk, but Unity's `fileID`/GUID pairs are harder for a person to check by eye.

Movement would be a `MonoBehaviour` on a `Rigidbody2D` (the original jumping-man prototype did exactly this) or a `CharacterController` in 3D. The physics callbacks such as `OnTriggerEnter` need a `Rigidbody` on one of the objects and run after all `FixedUpdate` calls ([OnTriggerEnter](https://docs.unity3d.com/ScriptReference/Collider.OnTriggerEnter.html)), where our session polls an `Area2D` itself.

The tests would be a Play Mode test assembly, run headless:

```bash
Unity -batchmode -projectPath . -runTests -testPlatform PlayMode -testResults results.xml
```

`-runTests` runs the project's tests, `-testPlatform PlayMode` selects Play Mode tests in the Editor (the default is Edit Mode), and results are written as NUnit XML ([Command-line arguments](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html)). Two practical differences for agent work: a Unity test run requires the full Editor to open and import the project, which is far heavier than a Godot headless script, and the agent needs a test assembly definition set up before it can add tests at all.

| Godot (this chapter) | Unity |
|---|---|
| Node | GameObject plus Components |
| Scene (`.tscn`, text) | Scene (`.unity`) or Prefab (`.prefab`), YAML under Force Text |
| Script (`.gd`, GDScript) | MonoBehaviour (`.cs`, C#) |
| `Resource` with `@export` | `ScriptableObject` asset |
| Signal | C# event or `UnityEvent` |
| `_physics_process` / `_process` | `FixedUpdate` / `Update` |
| `CharacterBody2D` | `Rigidbody2D` (kinematic or dynamic); `CharacterController` in 3D |
| `Area2D` overlap | Collider with `isTrigger`, `OnTriggerEnter` |
| InputMap action | Input System `InputAction` in `.inputactions` (JSON) |
| `.godot/` cache | `Library/` cache |
| `godot --headless --script …` | `Unity -batchmode -runTests …` |

## Doing the same thing in Unreal Engine

### Similarities

Unreal Engine 5 has the same parts under different names. The player would be a `Character` whose `CharacterMovementComponent` owns walking and jumping; `MaxWalkSpeed` is the run speed and `JumpZVelocity` the initial jump velocity, and the component computes its movement during its own tick ([UCharacterMovementComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UCharacterMovementComponent)). Input goes through Enhanced Input, where Input Actions represent "something that the user can do" and Input Mapping Contexts collect the bindings ([Enhanced Input](https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine)), the same separation of action from key that Godot's InputMap makes. Unreal can also run tests unattended: the Automation system runs named tests from the command line with `-ExecCmds="Automation RunTest <name>;Quit"` and can export JSON and HTML reports with `-ReportExportPath` ([Run automation tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine)), and `-nullrhi` runs the engine headless ([Command-line arguments](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-command-line-arguments-reference)).

### Differences

The biggest difference for agent work is the file format. Unreal assets (`.uasset`) and levels (`.umap`) "are binary, so cannot be opened as text or merged in a text-based merge tool," and the editor locks them while you work ([Perforce and Unreal](https://dev.epicgames.com/documentation/unreal-engine/using-perforce-as-source-control-for-unreal-engine?lang=en-US)). If the run speed lives on a Blueprint character, as it does in most templates, an agent cannot read or change it by editing a file. You would either set the default in a C++ constructor, which an agent can edit as text and which must then be compiled, or have the agent write an editor Python script (the Python Editor Script Plugin must be enabled first) and run it inside the editor ([Python scripting](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python)). To see what changed in a Blueprint you use the editor's diff tool, not `git diff` ([UE Diff Tool](https://dev.epicgames.com/documentation/en-us/unreal-engine/ue-diff-tool-in-unreal-engine)).

Our route test would become either a C++ automation test or a **functional test**: a Functional Test actor placed in a level and scripted to run ([Functional testing](https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine)). The test itself is then partly a binary asset. A run looks like:

```bash
UnrealEditor-Cmd MyProject.uproject -ExecCmds="Automation RunTest Project.Movement;Quit" -nullrhi -unattended -ReportExportPath=Saved/TestReport
```

Treat that as a documented form, not a command we ran. One correction to carry forward from the old syllabus: Unreal is not open source. Its source is available on GitHub to accounts that accept the Unreal Engine EULA, and use is governed by that license ([Unreal Engine on GitHub](https://www.unrealengine.com/en-US/ue-on-github)).

| Godot (this chapter) | Unreal Engine 5 |
|---|---|
| Node | Actor and its Components |
| Scene (`.tscn`, text) | Level (`.umap`) or Blueprint class (`.uasset`), binary |
| GDScript | Blueprint graphs or C++ |
| `Resource` with `@export` | Data Asset, or `UPROPERTY` defaults on a class |
| Signal | Event Dispatcher (Blueprint) or delegate (C++) |
| `CharacterBody2D` + `move_and_slide` | `Character` + `CharacterMovementComponent` |
| `tuning.speed` | `MaxWalkSpeed` |
| `Area2D` | Trigger volume with overlap events |
| InputMap action | Enhanced Input: Input Action + Input Mapping Context |
| `.godot/` cache | `Intermediate/`, `Saved/`, derived-data caches |
| `godot --headless --script …` | `UnrealEditor-Cmd … -ExecCmds="Automation RunTest …" -nullrhi` |

## Sources

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation, checked on September 27, 2026 (Unity manual pages for Unity 6.x; Epic documentation pages for Unreal Engine 5.8).

**Godot (official documentation, stable branch, Godot 4.7)**

- [Key concepts overview](https://docs.godotengine.org/en/stable/getting_started/introduction/key_concepts_overview.html)
- [File system (`project.godot`, `res://`)](https://docs.godotengine.org/en/stable/tutorials/scripting/filesystem.html)
- [TSCN file format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html)
- [GDScript basics](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html)
- [Idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)
- [Node class (`process_physics_priority`, `_ready`)](https://docs.godotengine.org/en/stable/classes/class_node.html)
- [Input examples](https://docs.godotengine.org/en/stable/tutorials/inputs/input_examples.html)
- [Input class](https://docs.godotengine.org/en/stable/classes/class_input.html)
- [InputEventKey class](https://docs.godotengine.org/en/stable/classes/class_inputeventkey.html)
- [Physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html)
- [Using CharacterBody2D/3D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html)
- [Area3D class (overlap list timing; Area2D documents the same method)](https://docs.godotengine.org/en/stable/classes/class_area3d.html)
- [Resources](https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html)
- [Custom drawing in 2D](https://docs.godotengine.org/en/stable/tutorials/2d/custom_drawing_in_2d.html)
- [Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
- [Overview of debugging tools (Remote scene tree)](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html)
- [Version control systems](https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html)
- [UID changes coming to Godot 4.4 (Godot blog)](https://godotengine.org/article/uid-changes-coming-to-godot-4-4/)

**Coding agents**

- [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference)
- [Claude Code permissions](https://code.claude.com/docs/en/permissions)
- [Claude Code memory (CLAUDE.md and AGENTS.md)](https://code.claude.com/docs/en/memory)
- [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)
- [Codex: custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)

**Walker and the example projects**

- [Walker framework](https://github.com/nikbearbrown/walker) (README, `AGENTS.md`, `publish.sh`, `engines/godot.md`)
- [walker-jumpman](https://github.com/nikbearbrown/walker-jumpman) at `9387542` (README, BUILD-REPORT, GDD 0.2.0, tests)
- [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd) at `382f2ba` (CHANGE-BRIEF, FRICTIONAL, SOURCES, `tests/test_clawd.gd`)
- This chapter's run: [`examples/01-walker-and-godot/`](../examples/01-walker-and-godot/)

**Unity (official documentation)**

- [Editor settings: Asset Serialization Mode](https://docs.unity3d.com/Manual/class-EditorManager.html)
- [An example of a YAML scene file](https://docs.unity3d.com/Manual/YAMLSceneExample.html)
- [Asset metadata (`.meta` files)](https://docs.unity3d.com/Manual/AssetMetadata.html)
- [Default project directories (`Library`)](https://docs.unity3d.com/6000.0/Documentation/Manual/default-directories.html)
- [ScriptableObject](https://docs.unity3d.com/Manual/class-ScriptableObject.html)
- [Time.fixedDeltaTime](https://docs.unity3d.com/ScriptReference/Time-fixedDeltaTime.html)
- [Collider.OnTriggerEnter](https://docs.unity3d.com/ScriptReference/Collider.OnTriggerEnter.html)
- [Input action assets](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.18/manual/ActionAssets.html)
- [Input System: input testing](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.4/manual/Testing.html)
- [Test Framework: UnityTest attribute](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-attribute-unitytest.html)
- [Test Framework: command-line arguments](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html)
- [UnityEvents](https://docs.unity3d.com/Manual/unity-events.html)

**Unreal Engine (official documentation)**

- [UCharacterMovementComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UCharacterMovementComponent)
- [Enhanced Input](https://dev.epicgames.com/documentation/en-us/unreal-engine/enhanced-input-in-unreal-engine)
- [Run automation tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine)
- [Command-line arguments reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-command-line-arguments-reference)
- [Functional testing](https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine)
- [Scripting the Unreal Editor using Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python)
- [UE Diff Tool](https://dev.epicgames.com/documentation/en-us/unreal-engine/ue-diff-tool-in-unreal-engine)
- [Using Perforce as source control (binary `.uasset`/`.umap`)](https://dev.epicgames.com/documentation/unreal-engine/using-perforce-as-source-control-for-unreal-engine?lang=en-US)
- [Event Dispatchers and delegates quick start](https://dev.epicgames.com/documentation/en-us/unreal-engine/event-dispatchers-and-delegates-quick-start-guide-in-unreal-engine)
- [Unreal Engine directory structure](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-directory-structure)
- [Unreal Engine on GitHub (EULA-gated source access)](https://www.unrealengine.com/en-US/ue-on-github)
