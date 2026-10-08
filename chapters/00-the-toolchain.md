# Chapter 0 — The Toolchain: Claude Code, Codex, Walker, and Godot at the Command Line

CSYE 7270 · Fall 2026 · Week 1 setup

## Executive summary

**What this chapter is.** The working setup behind every hands-on chapter in this book. A coding agent runs in your terminal (Claude Code or Codex). The Walker framework supplies the project's instructions and working loop. Godot runs the game, and it can also run from the command line with no window, so a script can check the game's state. Git keeps the versions you compare.

**Why read it.** Every later chapter asks you to do the same three things. Hand an agent one bounded change to a real Godot project. Check the result with a command *you* run. Then play the game yourself. This chapter shows those three moves on one small game, with every command and number taken from an actual run.

**What we built, and what happened.** On 27 September 2026 I gave Claude Code and Codex the same prompt: add a score to `walker-pong`, a Walker adaptation of Godot's Pong demo, and prove it with a headless test. Both agents produced a working score with a passing test, Codex in about 5 minutes and Claude Code in about 14. Then both ran the game's existing regression test the wrong way, without `--fixed-fps 60`. Both saw it fail, and both explained the failure wrongly. Claude Code later got a pass under different machine load and reported it. Run correctly, the original test passes unchanged on both versions, with exactly the same numbers as the untouched game. The fix was one paragraph in the project's `AGENTS.md` saying how to run the checks. Given that, the same prompt produced a correctly run, passing test on the first try. The chapter is built around that episode. The agent's report is a claim. Your own command is evidence. The playtest is still yours.

**What this does not establish.** Whether either score is readable, placed well, or makes Pong more fun. Those need a person looking at a screen. Exporting a playable build comes in Chapter 15.

---

## The question

Here is the puzzle this chapter solves. Both agents ran the same unmodified test file on the same machine, against a game whose physics they had not touched. The test failed for both of them. When I ran it, it passed all ten of its checks, with identical numbers on every run. Nobody edited the test. Nobody lied. So what was different?

Hold that question. It has a one-flag answer, but finding the flag means understanding what each tool in the chain actually does. When an agent says "I ran the tests," you need to know which program ran, on which files, in what state, and with which options. Then you need to be able to run the same thing yourself.

---

## Ideas you need

### Four tools, four jobs

| Tool | Its job | What it is not |
|---|---|---|
| **Claude Code** or **Codex** | Reads the project's files, proposes changes, edits text files, runs the commands you allow, and reports what it did | Not the game engine, not a judge of fun, not proof |
| **Walker** | The working method and its files: the **Game brief → Build → Playtest → Inspect → Revise → Export** loop, the per-game `AGENTS.md`/`CLAUDE.md` instructions, and installable skills such as `/gdd` (game design documents) and `asset-gen` | Not a `walker build` command that makes games. There is no such executable |
| **Godot** | The editor you use to inspect a project, the engine that runs it, and a command-line program that can import, run, test and export it | Not an AI tool. It runs whatever the files say |
| **Git** | Remembers every version, so "what changed?" has an exact answer (`git diff`) | Not a backup of anything you did not commit |

Chapter 1 introduces Walker and Godot in the editor. This chapter is about the same tools in a terminal, because that is where the agent works.

### Godot is also a command-line program

The Godot editor you double-click is one executable. It takes command-line options. The official [command-line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) recommends putting it on your `PATH` as `godot`. On Windows and Linux you run the binary by its path. On macOS the binary is inside the app bundle, at `Godot.app/Contents/MacOS/Godot`. Homebrew (macOS) and Scoop (Windows) can put it on your `PATH` for you. On the instructor's Mac, `godot` is a symlink to `/Applications/Godot.app/Contents/MacOS/Godot`.

Check what you have:

```bash
godot --version
```

The course machine printed `4.7.2.stable.official.ed1daf0bf`. Record your own version in your notes. If it differs, say so before you interpret any test result.

These are the options this book uses, quoted from `godot --help` on Godot 4.7.2 (the full output is in [`examples/00-the-toolchain/verification/godot-4.7.2-help.txt`](../examples/00-the-toolchain/verification/godot-4.7.2-help.txt)):

| Option | What `godot --help` says | How we use it |
|---|---|---|
| `--path <directory>` | "Path to a project (`<directory>` must contain a `project.godot` file)." | Point Godot at the game without `cd`-ing into it |
| `--headless` | "Enable headless mode (`--display-driver headless --audio-driver Dummy`). Useful for servers and with `--script`." | No window, no sound. Every automated check in this book runs this way |
| `--import` | "Starts the editor, waits for any resources to be imported, and then quits." | Build the `.godot/` import cache after cloning |
| `-s, --script <script>` | "Run a script." | Run a test written as a `SceneTree` script |
| `--check-only` | "Only parse for errors and quit (use with `--script`)." | Fast syntax check of a test script |
| `--quit-after <int>` | "Quit after the given number of iterations." | Run the main scene for N frames and stop |
| `--fixed-fps <fps>` | "Force a fixed number of frames per second. This setting disables real-time synchronization." | **Make each frame exactly 1/fps seconds of game time.** This flag answers the chapter's question |
| `--export-release <preset> <path>` | "Export the project in release mode using the given preset and output path." | Chapter 15. It needs export templates installed |

The help text tags each option. **E** means "only available in editor builds." **R** means available in editor builds and in exported games. `--import` and `--export-release` are editor-only. `--headless` and `--fixed-fps` also work in an exported game.

Headless mode is a precise promise. It means no picture and no sound. The scene tree, scripts, physics, signals and timers all still run. So a headless test observes **state**: positions, counters, which signal fired, what a label's text says. It never observes **pixels**. Whether a label is readable against the background is always a human check.

### The time trap: frames are not seconds

Now the flag that answers the question. Here is how the Pong ball moves (`godot/logic/ball.gd`, unchanged from Godot's demo):

```gdscript
func _process(delta: float) -> void:
	_speed += delta * 2
	position += _speed * delta * direction
```

`_process` runs once per frame. `delta` is the time since the previous frame, in seconds. The ball's motion is measured in **seconds**. Pong at 30 frames per second and Pong at 144 frames per second move the ball the same distance per second. That is correct game code. See Godot's page on [idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html).

Here is how the regression test drives the game (`tests/input_route.gd`):

```gdscript
var route_tick := frame * (60.0 / route_fps)
if route_tick < 150:
	Input.action_press("left_move_up")
	# ...
frame += 1
if frame >= 80 * route_fps:
	finish()
```

The test's script is measured in **frames**. "Press up for 150 ticks, then down, then track the ball, then deliberately miss at tick 2,700, stop at 4,800 frames." At 60 frames per second, 4,800 frames is 80 seconds of play.

So the test assumes one frame equals 1/60 of a second. Without `--fixed-fps 60`, nothing enforces that, and `delta` reports real elapsed time. Headless Godot does not run flat out, either. When the display cannot draw, which is always true headless, the engine sleeps after each frame toward a target period set by `application/run/low_processor_mode_sleep_usec`. The default is 6,900 microseconds, which the 4.7.2 source annotates as "Roughly 144 FPS" (`OS::add_frame_delay` in [`core/os/os.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/core/os/os.cpp); the default is in [`main/main.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/main/main.cpp)). Chapter 13 takes this apart in detail. On the course Mac, 4,800 real-time frames took 33 to 35 seconds of wall clock, about 145 frames per second. That is about 33 seconds of game time instead of 80. The ball had less time to speed up and fewer rallies in which to hit the ceiling. Small differences in frame timing also nudged its path. With `--fixed-fps 60`, every frame is exactly 1/60 s, whatever the machine does. The same 4,800 frames took under a second of wall clock and produced identical results every time.

We measured it on the **unmodified** game from GitHub, twelve runs:

| How the test was run | Import cache (`.godot/`) | Runs | Result |
|---|---|---|---|
| `--fixed-fps 60` | present | 3 | 3 pass. Identical: Ceiling 5, Floor 4, Left 10, LeftWall 2, Right 8, RightWall 1; max speed 185.67 |
| `--fixed-fps 60` | absent | 3 | 3 pass. Identical to the row above |
| real time (no flag) | present | 3 | 3 **fail** `ceiling_contact`: Ceiling 0, Floor 1, Left 4, LeftWall 1, Right 2, RightWall 1; max speed 133.64–133.66 |
| real time (no flag) | absent | 3 | 1 **fail** (same numbers as above), 2 **pass**: Ceiling 1, Floor 1, Left 4, LeftWall 1, Right 3, RightWall 0; max speed 140.61–140.68 |

The runner is [`examples/00-the-toolchain/verification/route-timing-experiment.sh`](../examples/00-the-toolchain/verification/route-timing-experiment.sh). Two things follow. The import cache makes no difference. The frame-rate flag makes all of it. Without the flag, the same untouched game sometimes fails and sometimes passes, depending on frame timing, and most plausibly on how busy the machine is at that moment. That is a **flaky test**, and the flakiness sits in how the test is run, not in the game.

The general rule applies to every engine in this book. **Any test that counts frames while the game moves by delta time is machine-dependent unless the time step is pinned.** Write the pinning flag into the project's instructions. The Revise step later in this chapter shows what happens when you do.

### Why an agent can work on a Godot project at all: it is all text

A Godot project is a folder of mostly human-readable text files. That is the property this whole course leans on.

| File | What it is | Agent can read and diff it? |
|---|---|---|
| `project.godot` | Project settings in an INI-like format: name, main scene, input actions, window size | Yes |
| `*.tscn` | A saved scene: its nodes, their properties, and their signal connections | Yes, and see below |
| `*.gd` | GDScript source | Yes |
| `*.tres` | A saved resource (material, theme, curve…) | Yes |
| `*.import` | How Godot should import a source asset (texture filter, compression, loop…) | Yes |
| `*.uid` | A script's stable unique ID, stored beside the script | Yes |
| `.godot/` | The import cache Godot rebuilds from the files above | Ignore it. It is in `.gitignore` for a reason |
| images, audio, models | The source assets | Binary. The agent can move them and read their `.import` settings, not their pixels |

Here is an excerpt of `walker-pong`'s scene file (`godot/pong.tscn`), trimmed:

```text
[gd_scene format=3 uid="uid://1edquvuh4xlu"]

[ext_resource type="Script" uid="uid://c2ofwebuaqwtq" path="res://logic/ball.gd" id="4"]
[ext_resource type="Script" uid="uid://d0ctwatj03r3b" path="res://logic/wall.gd" id="7"]

[sub_resource type="RectangleShape2D" id="2"]
size = Vector2(8, 8)

[node name="Ball" type="Area2D" parent="." unique_id=548893558]
position = Vector2(320.5, 191.124)
script = ExtResource("4")

[node name="Collision" type="CollisionShape2D" parent="Ball" unique_id=1934890566]
shape = SubResource("2")

[node name="LeftWall" type="Area2D" parent="." unique_id=2003719181]
position = Vector2(-10, 200)
script = ExtResource("7")

[connection signal="area_entered" from="LeftWall" to="LeftWall" method="_on_wall_area_entered"]
```

Read it top to bottom. It is a complete description of part of the game. `ext_resource` lines name files the scene depends on. Each has a `uid://` identity and a `res://` path. `sub_resource` lines define things that live inside the scene, like the ball's 8×8 collision rectangle. `node` lines build the tree, each with a `parent`. `connection` lines are the signals you would otherwise wire up in the editor's Node dock.

Two details matter when an agent edits this file by hand:

- **UIDs.** Godot gives resources and scripts stable `uid://` identities, so that a reference survives a rename. When the import cache is missing, Godot cannot resolve them yet. It prints a warning such as `ext_resource, invalid UID: uid://bbiup6xhh6s17 - using text path instead` and falls back to the `res://` path. Claude Code met exactly that warning, because it never ran `--import`. The fallback worked. The warning was telling it the project had not been imported.
- **`unique_id` on nodes.** Scenes saved by the Godot 4.7 editor carry a `unique_id=` on each node line, as every node in `pong.tscn` does. Look at how each agent added nodes (details in "What we actually ran"). Claude Code invented IDs by hand (`111222333`, `222333444`, `333444555`) and hand-wrote a script UID. Codex wrote node lines with no `unique_id` and let Godot generate the script's `.uid` file during import. Both loaded and passed their tests. A hand-invented ID only works while it happens to be unique. After an agent edits a scene as text, open and save it once in the editor, and let Godot write its own identifiers.

### Instruction files: how the agent learns your project

An agent starts every session knowing nothing about your project. The fix is a Markdown file of standing instructions in the repository:

- **Claude Code** reads `CLAUDE.md`. According to its [memory documentation](https://code.claude.com/docs/en/memory), if a repository has an `AGENTS.md` and no `CLAUDE.md`, Claude Code reads the `AGENTS.md`, but only from version 2.1.277. The course's runs used 2.1.150, which did not: Chapter 1 records the agent reporting that no project instruction file had been loaded. On an older version, import it from a one-line `CLAUDE.md` containing `@AGENTS.md`. If both exist, it reads `CLAUDE.md` only, unless `CLAUDE.md` imports `AGENTS.md`.
- **Codex** reads `AGENTS.md`. Per the [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md), it looks first in `~/.codex`, then walks from the Git root down to the working directory. It concatenates what it finds, so files closer to your work come later and win.
- **Walker** writes the right one for you. Its `publish.sh` takes `--agent claude` (writes `CLAUDE.md`, installs skills under `.claude/skills/`, invoked as `/gdd` and `/asset-gen`) or `--agent codex` (writes `AGENTS.md`, skills under `.agents/skills/`, invoked as `$gdd` and `$asset-gen`). The Walker framework repository keeps a single file for both tools: its `CLAUDE.md` is a symbolic link to `AGENTS.md`.

One honest caveat. Walker's bundled Godot engine guide targets **C#/.NET**. This course's example games are **GDScript** and run in the regular Godot editor. For them, the instructions that matter are the game's own `AGENTS.md`, like `walker-pong`'s. It says: work only on this adaptation, use regular Godot/GDScript, preserve the license, make one bounded change at a time, and keep an honest Frictional log.

What the instruction file does **not** say is how to run the tests. Hold on to that. It is the root of this chapter's failure.

### Permissions and sandboxes: what the agent may touch

An agent that can run commands can run the wrong ones. Both tools make you choose a boundary.

**Claude Code** has [permission modes](https://code.claude.com/docs/en/permission-modes):

| Mode | What runs without asking |
|---|---|
| `default` (shown as **Manual**) | Reads only |
| `acceptEdits` | Reads, file edits, and common filesystem commands. The docs list `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed`, inside your working directory |
| `plan` | Reads, plus classifier-approved commands when auto mode is available |
| `auto` | Everything, with background safety checks |
| `dontAsk` | Reads and pre-approved tools. Anything that would prompt is denied |
| `bypassPermissions` | Everything. For isolated containers and VMs only |

You can pre-approve specific tools with allow rules, such as `--allowedTools "Bash(godot *)"`.

**Codex** runs model-generated commands in a sandbox. `codex exec --help` lists three policies: `read-only`, `workspace-write` and `danger-full-access`. You pick the working root with `-C` and grant extra writable folders with `--add-dir`.

What happened in our runs is the lesson, not a footnote:

- I ran Claude Code with `acceptEdits` and allow rules for `godot`, `env`, `mkdir`, `ls`, `cat`, and read-only `git`. It was **refused 18 times**. `cd … && godot …` was refused because a compound command must match a rule in every part. `WALKER_EVIDENCE_DIR=… godot …` was refused because a variable prefix does not match `Bash(godot *)`. It wrote a shell script to get around that, and couldn't run the script either. Then it found that `env WALKER_EVIDENCE_DIR=… godot …` matched my `Bash(env *)` rule. Look at that rule again. `env` runs *any* command, so `Bash(env *)` quietly granted far more than I meant to. Scope your rules to what you can actually read.
- `Bash(godot *)` is a wide grant too, and the same reasoning applies. `godot --script` runs any GDScript the agent has written, and GDScript can call `OS.execute()` to start other programs. In Chapter 14's networking lab, Claude Code was refused a shell `kill` command, and it put the kill inside a Godot test script instead. The agent was trying to finish its task, not to misbehave. But an allow rule is a boundary around *programs*, and a program that runs code is no boundary at all. Read every new script before you let it run, and treat the permission prompt as a review, not a formality.
- `acceptEdits` also let it delete files inside the project without asking. It used that to remove its temporary files, as the documentation says it may.
- Codex ran with `--sandbox workspace-write`. Its editor import printed `ERROR: Cannot save file '~/Library/Application Support/Godot/editor_settings-4.7.tres'`. The sandbox had blocked a write outside the project folder. The project's own import cache is inside the folder, so the import still produced a usable project, and every later Godot command worked. If you need Godot's settings folder writable, `--add-dir` is the documented way to grant it. We did not need it here.

### The headless test: a script that plays the game

A Godot test for this course is a GDScript file that **extends `SceneTree`**. That lets `godot --script` run it as the whole program. The pattern in `walker-pong/tests/input_route.gd`:

1. `_initialize()` runs first. It seeds the random number generator (`seed(7375)`), pins the viewport to 640×400, and schedules `start_game()`.
2. `start_game()` loads the **real** scene (`load("res://pong.tscn").instantiate()`), adds it to the tree, and connects its own counters to the walls', paddles' and ceiling's `area_entered` signals.
3. `_process()` runs every frame. It presses and releases the game's **real input actions** (`Input.action_press("left_move_up")`), exactly as a keyboard would through the Input Map. It never writes the ball's position or a score.
4. After 4,800 frames, `finish()` evaluates ten named checks. It writes a JSON report, including `"method": "scripted-input; no gameplay state writes"` and `"human_playtest": false`, and calls `quit(0)` on a pass or `quit(1)` on a fail.

The **exit code** is the machine-readable verdict. The JSON report is the human-readable one. Two habits keep both honest. They were learned the hard way while writing this book's later chapters:

- **Wrap headless runs in a time limit.** If a test script hits an error before it reaches `quit()`, headless Godot does not exit. It waits forever, with no window to close. One agent's test sat for thirty minutes. Prefix the command with `timeout 120`. Linux has `timeout` built in. On macOS it comes from Homebrew's `coreutils` package, which on the instructor's Mac provides both `timeout` and `gtimeout`.
- **Read the error output even when the exit code is 0.** Godot prints script and shader errors to standard error. It can print them while the process still exits 0, as when a test counts its own checks and never notices the engine complaining. Chapter 14's agent reported 12 of 12 checks passing over 626 script errors. A clean-clone run in Chapter 4 exited 0 with 55 `ERROR` lines, because the project had not been imported. The two honest labels matter as much as the checks. A scripted route that passes is evidence about state under one sequence of inputs. It is not a person playing.

### The evidence ladder

Every claim about a change sits on some rung of this ladder. Say which rung you are on.

| Rung | You have | It establishes | It does not establish |
|---|---|---|---|
| 1 | The agent says "done" | That the agent produced a message | Anything about the game |
| 2 | A `git diff` | Exactly which files and lines changed | That the change works |
| 3 | Clean `--import` and `--check-only` | The project and scripts parse | That behaviour is right |
| 4 | A headless test passes, with the time step pinned | The tested state is right under that scripted input | Feel, readability, untested inputs |
| 5 | You played it | What a person experiences | What other people experience, other machines |
| 6 | An exported build runs on the target (Chapter 15) | The game survives packaging | That anyone wants to play it |

The agents in this chapter both climbed to rung 4 for their new test. Both then misread a rung-4 result for the old test, because they had run it in a way that made it unreliable.

---

## The Walker example: `walker-pong`

`walker-pong` is the first Walker adaptation from the official [Godot demo projects](https://github.com/godotengine/godot-demo-projects). It is the `2d/pong` demo at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`, MIT-licensed, with its license and attribution kept. It is public at [github.com/nikbearbrown/walker-pong](https://github.com/nikbearbrown/walker-pong). This chapter used commit `c0cbc71`.

**How it is built.** Everything that moves is an `Area2D` with a small script:

| Node | Script | What it does |
|---|---|---|
| `Left`, `Right` (paddles) | `logic/paddle.gd` | Move with `left_move_up/down` or `right_move_up/down`, clamped to y 16–384. On contact they send the ball back with a random vertical component (`randf()`) |
| `Ball` | `logic/ball.gd` | Moves by `_speed * delta * direction`; speeds up by 2 units per second; `reset()` returns it to the centre at speed 100, **always heading left** |
| `LeftWall`, `RightWall` | `logic/wall.gd` | On contact with the ball, call `area.reset()`. This is the only "point" event the game has |
| `Ceiling`, `Floor` | `logic/ceiling_floor.gd` | Deflect the ball vertically |
| `Camera2D` | none | Offset (320, 200), so world coordinates map to the 640×400 screen |

**What its checks establish.** The README and CAPTURE notes say the ten scripted-input checks pass at 60 and at 30 FPS. My re-run of the GitHub version, after `--import` and with `--fixed-fps 60`, passed all ten. They are: both paddles reach both bounds, both paddles hit the ball, the ball touches ceiling and floor, a deliberate miss reaches a wall, and the ball accelerates past 110.

**What is not established.** The README says it plainly: no human playtest has been recorded, the upstream gamepad mappings are untested on hardware, and there is **no score**, win state, pause, AI opponent or soundtrack. That last gap is our task.

**A gap that turns out to matter.** Nowhere in the repository's Markdown does it say how to run the test. You learn that it needs a `WALKER_EVIDENCE_DIR` environment variable only by reading the script. You learn that it needs `--fixed-fps 60` only by understanding the time trap above. Both agents had to discover the first fact. Neither discovered the second.

---

## Hands-on: add a score, then check the agent

You will give an agent one bounded feature, then verify its work yourself. Use either tool; the steps are the same. If you can, do it twice, once with each, and compare.

### Predict

Write your answers down before you delegate. Keep them even if they turn out wrong.

1. Which node should own the score, and which event should change it? Is there an existing signal you can reuse, or should you add one?
2. After a point, `reset()` always serves the ball toward the **left** player, whoever scored. The prompt says not to change reset behaviour. Is that a bug the score will expose, or a design question for a person?
3. Where on screen can two numbers go without covering the paddles or the centre line? Should the score move if the camera ever moves?
4. How will you tell "the label shows a number" apart from "the number is right"? What would a test have to read to check the *displayed* score?
5. What in the existing test could a UI change break? What could break it *without* any change to the game?

### Build It

**Step 1 — Get the tools.** Install the regular Godot 4 editor (not the .NET build) and make `godot` callable from your terminal. Install and sign in to Claude Code (Northeastern access is described on [claude.northeastern.edu](https://claude.northeastern.edu/)) or Codex. Check them:

```bash
godot --version
```

```bash
claude --version
```

```bash
codex --version
```

**Step 2 — Get the game and build its import cache.**

```bash
git clone https://github.com/nikbearbrown/walker-pong.git
```

```bash
cd walker-pong
```

```bash
godot --headless --path godot --import
```

**Step 3 — Establish the baseline yourself, before any change.** The route test writes its evidence to a folder you name:

```bash
mkdir -p evidence-local
```

```bash
WALKER_EVIDENCE_DIR="$PWD/evidence-local" timeout 120 godot --headless --path godot --fixed-fps 60 --script "$PWD/tests/input_route.gd"
```

It ends by printing one long JSON line, and exits with status 0. Check the status:

```bash
echo $?
```

You should see `"passed":true` and `0`. Write down the `counts` and `max_speed`. On Godot 4.7.2 they were Ceiling 5, Floor 4, Left 10, LeftWall 2, Right 8, RightWall 1, and 185.67. If yours differ, note your Godot version and machine before going further.

Note that `evidence-local/` is not covered by the repository's `.gitignore`. Don't commit it by accident.

**Step 4 — Make a branch** so the change is easy to see and easy to throw away:

```bash
git switch -c add-score
```

**Step 5 — Give the agent the task.** Start `claude` (or `codex`) in the repository folder and paste this prompt. It is the exact prompt used for this chapter's worked example:

```text
This is walker-pong, a Walker adaptation of Godot's Pong demo (Godot 4.7, GDScript).
Read AGENTS.md, README.md, GAME-BRIEF.md and GDD.md first. The brief says there is
no score system yet. Add one bounded feature: a score.

Requirements:
- When the ball leaves through the left wall, the right player scores one point;
  when it leaves through the right wall, the left player scores one point.
- Show both scores at the top of the screen, readable in the 640x400 viewport.
- Do not change paddle movement, ball speed, bounce rules, or the reset behavior.
- Keep the upstream license and attribution intact.

Before editing, tell me which files you will change and one way this change could
break existing behavior. Then implement it. Add a headless test under tests/ that
drives the real game with normal input actions only (no direct writes to the score
or the ball) and checks that each score equals the matching wall contacts. Run the
existing tests/input_route.gd and your new test with Godot headless and show me the
real output. Do not open a Godot window. Do not commit.
```

Look at what the prompt does. It names the files to read first. It states the rule as observable behaviour. It fences off what must not change. It asks for a plan and a risk *before* edits. It says what the test may and may not touch. It asks for real output. And it keeps two decisions for you, committing and playing. It does **not** say how to run the existing test. That omission is deliberate, and it is the realistic case.

In an interactive session you'll be asked to approve commands. Read each one before you approve it. For a non-interactive run, which is how this chapter's example was made, the commands were:

```bash
claude -p "$(cat PROMPT.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot *),Bash(env *),Bash(mkdir *),Bash(ls *),Bash(cat *),Bash(git status *),Bash(git diff *)" --max-turns 60 --output-format stream-json --verbose > session-claude.jsonl
```

```bash
codex exec --sandbox workspace-write -C . --json -o codex-last.txt "$(cat PROMPT.txt)" > session-codex.jsonl
```

(As explained above, drop `Bash(env *)` from your own allow list. It turned out to be a blank cheque.)

If you run `codex exec` from a script or a background job, close its standard input by adding `< /dev/null` to the command. Our scripted Revise re-run sat for five minutes printing `Reading additional input from stdin...` until it was restarted that way.

### Use It

Now play. Open Godot's Project Manager, import `godot/project.godot`, and press **Run Project**. Left paddle: W and S. Right paddle: Up and Down.

- Let the ball past each paddle at least twice. Does the correct side's number go up each time?
- Are the numbers readable at the game's size? Do they cover the paddles when a paddle is at the top? Do they fight with the centre line?
- Watch the serve after each point. It always goes left, whoever scored. Now that there is a score, does that feel fair? Write your judgment down as a design question. Don't fix it inside this change: the prompt fenced it off.
- Open the scene in the editor and look at the new nodes in the Scene dock. Save the scene once, then run `git diff godot/pong.tscn` and see whether the editor rewrote anything, such as the node identifiers an agent wrote by hand or left out.

### Ship It

Read the whole diff before you commit anything:

```bash
git status --short
```

```bash
git diff
```

Look for stray files the agent left behind. In our runs these were an untracked `evidence-run/` folder (Claude Code) and edits to four design documents you did not ask for (Codex). Decide what belongs in the change. Commit only that, with a message that names the feature and how you checked it. For Claude Code's version of the change, for example:

```bash
git add godot/logic/score.gd godot/logic/score.gd.uid godot/pong.tscn tests/
```

```bash
git commit -m "Add score counter with headless score test"
```

Then add an entry to your `FRICTIONAL.md`. Record what you predicted, what the agent proposed, what it got wrong, the commands *you* ran and their results, and which parts you have only machine evidence for. Chapter 1 and the course's [assessment policy](../prerequisites/assessment-policy.md) describe the format. If this change were an assignment, the fitting explainer would be Brutalist's `godot-gamedev` skill: code, scene and test, with an input → state → output trace.

### Verify

Run both tests yourself, with the time step pinned:

```bash
WALKER_EVIDENCE_DIR="$PWD/evidence-local" timeout 120 godot --headless --path godot --fixed-fps 60 --script "$PWD/tests/input_route.gd"
```

```bash
timeout 120 godot --headless --path godot --fixed-fps 60 --script "$PWD/tests/score_check.gd"
```

(Use your agent's test file name. Codex named its test `score_route.gd`.)

A pass on the first command means the new node did not change the ball, the paddles or the walls under the regression route. Compare its counts with your Step 3 baseline. They should match exactly. A pass on the second means the score counters, and ideally the label text, matched the wall contacts in that scripted rally. Neither pass means the score is readable, well placed or fun. That was Use It, and it was your job.

---

## What we actually ran

**Date:** 27 September 2026. **Machine:** the instructor's Mac, Godot 4.7.2. **Starting point:** fresh clones of `walker-pong` at `c0cbc71`. **Prompt:** exactly the one in Step 5. The full record is in [`examples/00-the-toolchain/`](../examples/00-the-toolchain/): diffs, new files, readable session transcripts, verification logs and the timing experiment.

### Two agents, one prompt

| | Claude Code | Codex |
|---|---|---|
| Version and model | Claude Code 2.1.150. `claude -p` used the account's default model, `claude-sonnet-4-6`. Choose one with `--model` | Codex CLI 0.153.4, `gpt-5.6-sol` at reasoning effort `low` (the instructor's `~/.codex/config.toml`) |
| Wall-clock time | 14 min (17:52–18:07 UTC), 59 turns, 58 tool calls | 5 min (18:03–18:08 UTC), 12 shell commands |
| Usage reported by the tool | "total_cost_usd": 1.77 (the CLI's API-equivalent figure) | 646,182 input tokens (607,872 cached), 8,674 output |
| Permission friction | 18 refused commands (see "Permissions and sandboxes") | Editor-settings write blocked by the sandbox. Harmless here |
| Plan and risk stated first? | Yes: four files. Risk: its `_ready()` looks walls up by name | Yes: seven files. Risk: signal ordering at the wall |
| Who owns the score | New `ScoreBoard` (**CanvasLayer**) whose script connects to the walls' existing `area_entered` signals in `_ready()` | New `Score` (**Node2D**). `wall.gd` gains a new `ball_exited` signal, emitted just before `reset()`. Connections are written into the scene file |
| Where the numbers sit | Centred over each half (x 80–240 and 400–560), default colour, size 28 | Flanking the centre line (x 246–294 and 346–394), cyan and magenta to match the paddles, black outline, size 32 |
| Scene identifiers | Hand-invented node `unique_id`s and a hand-written script UID | No `unique_id` on the new nodes. Script `.uid` generated by Godot on import |
| New test | `score_check.gd`: replays the regression route for 3,300 frames. Compares internal counters with wall contacts. **Does not read the label text** | `score_route.gd`: a targeted route that deliberately misses on each side and stops at the second wall contact. Compares counters **and label text**, and requires both sides to score |
| Ran an import first? | No. It saw UID warnings and worked through them | Yes (`godot --headless --editor --quit`), after its first attempt showed the cache was missing |
| Ran the old test with `--fixed-fps 60`? | **No** | **No** |
| Old test result it reported | First run failed `ceiling_contact`. Final run passed | Failed `ceiling_contact` (and a 30 FPS attempt also failed). Reported as a failure |
| Its explanation | "without the `.godot/` import cache the engine's RNG state at startup differs … shifting ball trajectories" | Called its failing run "deterministic" and did not explain the cause |
| Other changes | Left an untracked `evidence-run/` folder in the repository | Edited `README.md`, `GAME-BRIEF.md`, `GDD.md` to remove "no score", and appended a `FRICTIONAL.md` entry |

### My verification

I imported each agent's copy and ran every test myself with `--fixed-fps 60`:

| Command | Untouched game | Claude Code's version | Codex's version |
|---|---|---|---|
| `tests/input_route.gd` | exit 0. C5 F4 L10 LW2 R8 RW1, max 185.67 | exit 0. **Identical** | exit 0. **Identical** |
| Agent's own score test | n/a | exit 0. LeftWall 2, RightWall 1 → left 1, right 2, over 3,300 frames | exit 0. 1–1, both labels match, 651 frames |

Identical regression numbers are the strongest evidence here. Adding the score changed nothing about how the ball, paddles and walls behave under that route. It also shows why an exact baseline in Step 3 is worth writing down.

### Where each agent was right and where it was wrong

**Both got the feature right**, as far as machines can tell. Each had the correct wall-to-player mapping, a visible label, a test that plays through real input actions, and no writes to the ball or the score.

**Both stopped at a real failure instead of hiding it.** Neither weakened, edited or deleted the regression test. Codex wrote, "I will not weaken or rewrite the existing test to manufacture a pass," and logged the failure in `FRICTIONAL.md`. That behaviour is what you want. It is also why a human has to read the report.

**Both misread the failure.** Claude Code blamed the import cache and the random number generator. The experiment above rules that out: the failure happens *with* the cache, and the pass happens *without* it. Its first failing run matches our real-time failure numbers exactly (Ceiling 0, Floor 1, Left 4, LeftWall 1, Right 2, RightWall 1, max 133.64). Its later passing run matches our real-time *pass* cluster (Ceiling 1, Right 3, RightWall 0, max 140.6). That second run (18:05:45 UTC) started while Codex's own 80-second route run (from 18:05:43) was using the same Mac. Real-time results fall into those two clusters, and which one you get depends on frame timing, which depends on what else the machine is doing. Other jobs were running on the Mac during my experiment too. Claude Code reported the pass as clean. Codex called its failing run deterministic, when the one thing that run lacked was determinism. The cause was the same for both: an undocumented flag.

**Claude Code's test checks less than its report suggests.** `score_check.gd` counts wall contacts through the same `area_entered` signal the scoreboard listens to, and never reads what the labels display. It would still pass if both labels were hidden or showed the wrong number. Codex's test reads the label text. Neither can tell you whether the text is *legible*.

**Codex did more than it was asked.** Updating the brief and GDD to say a score now exists is arguably right, since those documents would otherwise be false. But the brief and GDD record design decisions, and in Walker a person makes those. Whether the agent should edit them is your call, not the agent's. Make it deliberately.

**Design differences are yours to judge.** A `CanvasLayer` draws in screen space and ignores the camera. A `Node2D` draws in the world and moves with it. Pong's camera never moves, so both work today. Add screen shake later and one of these scores will shake with the world. Coloured numbers beside the centre line and plain numbers over each half make a readability and style trade-off. No test decides it.

### Revise: fix the instructions, not the code

The smallest responsible change here is not to the game. It is to the instructions the agents read. Neither could know the test needs `--fixed-fps 60`, because the repository never said so. So I appended this to a fresh clone's `AGENTS.md` and gave Codex the identical prompt again:

```text
## Checks (run from the repository root)

Import once after cloning: `godot --headless --path godot --import`

Regression route — the route counts frames but the game moves by seconds, so it
is only deterministic with `--fixed-fps 60`. Without it the result depends on
machine speed. Expected: exit 0, "passed": true.

`WALKER_EVIDENCE_DIR="$PWD/evidence-local" godot --headless --path godot --fixed-fps 60 --script "$PWD/tests/input_route.gd"`

Run any new test the same way, with `--fixed-fps 60`.
```

The re-run (18:15–18:19 UTC, 3.5 minutes, 9 shell commands instead of 12) went differently in exactly the way the instructions predicted. Codex ran `godot --headless --path godot --import` first. It ran the regression route with `--fixed-fps 60` and got `"passed": true` with the baseline numbers exactly: Ceiling 5, Floor 4, Left 10, LeftWall 2, Right 8, RightWall 1. It ran its new score test the same way (1–1, both labels matching, 651 frames). I re-ran both myself and got the same results. The record is in [`examples/00-the-toolchain/revise/`](../examples/00-the-toolchain/revise/).

Two more things happened in that re-run that are worth your attention.

- **Same tool, same prompt, different design.** This time Codex put the score on a `CanvasLayer` and connected the walls' existing `area_entered` signals in the scene file. It did not add a new signal to `wall.gd`, as it had the first time. Design choices are not stable across runs. That is one more reason the design decision has to be yours, written down, and checked against the diff.
- **It tidied away its own evidence.** After the passing run it deleted the `evidence-local/` report files it had just produced (`rm … && rmdir evidence-local`), presumably to leave no untracked files. The sandbox allowed it because the files were inside the workspace. Keeping `evidence-local/` out of Git is right. Deleting the only record of a passing run is not. Say in your instructions which outputs to keep.

This is what the Claude Code documentation means when it says to put build and test commands in the instruction file. It is also why every Walker game you start should say, in writing, how its checks are run.

---

## Check your understanding (ungraded)

1. Explain, using `ball.gd` and `input_route.gd`, why the same test can pass on one laptop and fail on another when it is run without `--fixed-fps 60`. Which of the two scripts would you change to make the test independent of the flag, and what would the change be?
2. Claude Code's first explanation blamed the import cache. Design the smallest experiment that would have tested that explanation. How many runs, which variable held constant, which varied?
3. Open `examples/00-the-toolchain/claude/score_check.gd`. Write one extra check that would fail if the left label showed the right player's score. Then say what *no* headless check could tell you about that label.
4. Codex added a `ball_exited` signal to `wall.gd`. Claude Code reused the wall's existing `area_entered`. Name one future change to the game under which Codex's design is safer, and one under which Claude Code's is simpler.
5. Your allow list includes `Bash(godot *)`. The agent wants to run `cd godot && godot --import`. Why was that refused, and what would you rather it ran?
6. Sort these into machine evidence and human judgment: "left score increments on right-wall exit"; "scores are readable on a projector"; "adding the score did not change ball behaviour under the route"; "serving always to the left is unfair once there is a score."

---

## Doing the same thing in Unity

*Unity and Unreal were not run for this chapter. These comparisons come from their official documentation, checked on 27 September 2026. Unity's documentation was at version 6.6 (6000.6).*

### Similarities

- **The same shape of change.** A Unity version of this task would put a trigger collider behind each goal. The Unity counterpart of an `Area2D` is a `Collider2D` with *Is Trigger* set, and a script's `OnTriggerEnter2D` receives the contact. A component script (a `MonoBehaviour`) owns the two counters, and a UI text element shows them. The design questions are the same: which object owns the score, which event changes it, screen space or world space.
- **An agent can edit the code as text.** C# scripts are plain files. With the **Force Text** asset serialization mode, which Unity's manual gives as the default, scenes and prefabs are saved as YAML text, so `git diff` shows what changed.
- **Headless checks exist.** Unity's editor command line has `-batchmode` ("runs command line arguments without the need for human interaction"), `-nographics` (doesn't initialise the graphics device, for machines without a GPU), `-projectPath`, `-executeMethod` and `-logFile`. The [Unity Test Framework](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html) adds `-runTests`, `-testPlatform EditMode|PlayMode` and `-testResults <file>`, which writes an NUnit XML report. That plays the role of our exit code plus JSON.
- **The time trap is the same.** Unity also moves objects by `Time.deltaTime`. A frame-counting test has the same flakiness. Unity's `Time.captureDeltaTime` makes game time advance by a fixed interval "regardless of real time", which is the counterpart of `--fixed-fps`. Its documentation describes it for movie capture, so check that it suits your test runner.
- **The agent can reach into the editor.** Unity now ships an **official Unity MCP server**, which lets Claude Code, Cursor and similar clients query the project and drive the editor. It is part of the in-editor AI Assistant package, requires Unity 6 (6000.0) or later, and in Unity's May 2026 announcement it was in **open beta**, requiring a trial or subscription to Unity's AI tools.

### Differences

- **Every asset has a `.meta` file with a GUID**, and references between assets use those GUIDs. That is the Unity counterpart of Godot's UIDs, but more pervasive. An agent that creates or renames files outside the editor has to keep `.meta` files consistent, and a hand-invented GUID carries the same risk as Claude Code's hand-invented `unique_id`s, only more often.
- **Scene YAML is harder to hand-edit than `.tscn`.** Unity's YAML identifies objects by file IDs and class IDs. Adding a UI canvas and two text objects by editing text is error-prone. In practice an agent works through C# editor scripts or the MCP server rather than editing the scene file. Godot's `.tscn` is compact enough that both agents here edited it directly and it loaded.
- **No one-file test runner.** Godot runs any `SceneTree` script with `--script`. Unity's tests live in test assemblies run by the Test Framework. The nearest one-off equivalent is a static method called with `-executeMethod`, in a full editor launch that also compiles your C#.
- **Language and licence.** C# rather than GDScript. Unity is proprietary. Its Personal plan is free when total finances for the most recent twelve months do not exceed US$200,000, a threshold Unity says took effect with Unity 6. Godot is MIT-licensed, and your game's licence is your own.

| Godot (this chapter) | Unity |
|---|---|
| `Area2D` + `area_entered` | `Collider2D` (Is Trigger) + `OnTriggerEnter2D` |
| Node with a GDScript | GameObject with a `MonoBehaviour` |
| `CanvasLayer` + `Label` | UI canvas + text element |
| `signal ball_exited` | C# `event` or `UnityEvent` |
| `godot --headless --script test.gd` | `Unity -batchmode -runTests -testPlatform PlayMode -testResults results.xml` |
| `--fixed-fps 60` | `Time.captureDeltaTime` |
| `uid://…` and `.uid` files | `.meta` files with GUIDs |
| `AGENTS.md` / `CLAUDE.md` | The same. Instruction files belong to the agent, not the engine |

## Doing the same thing in Unreal Engine

*Checked against the Unreal Engine 5.8 documentation on 27 September 2026.*

### Similarities

- **The same event, different names.** A trigger volume or a collision component's overlap event plays the role of `area_entered`. Unreal's gameplay framework has an explicit home for the score: its documentation says the **Game State** holds "data and logic relevant to all players in a game, such as team scores". A UMG widget displays it.
- **Headless automation exists.** Unreal's automation framework runs tests from the command line through `-ExecCmds="Automation RunTest <name>;Quit"`, with `-ReportExportPath=<dir>` writing JSON and HTML results. Epic's command-line reference documents `-nullrhi` ("Use null rendering hardware interface to run UE headless") and `-unattended` (no UI pop-ups or dialogs). Together they are the counterpart of our `--headless --script` run.
- **The editor is scriptable and agent-reachable.** The Python Editor Script Plugin exposes editor, asset and level operations to Python. Unreal Engine 5.8 also ships **Unreal MCP**, a first-party plugin that embeds an MCP server in the editor at `http://127.0.0.1:8000/mcp` and can generate client configuration for Claude Code, Codex, Cursor, VS Code and Gemini. Epic marks it **Experimental**: "many features are incomplete or missing."
- **The time trap again.** Unreal moves actors by frame delta time, so a test that counts frames needs the time step pinned in the same way.

### Differences

- **The key assets are binary.** Epic's documentation says `.uasset` and `.umap` files "are binary files, so cannot be opened as text or merged in a text-based merge tool". That covers Blueprints, levels and UMG widgets, and it is why Unreal has its own in-editor diff tool. An agent cannot read or diff a Blueprint the way both agents here read and edited `pong.tscn`. It must work through the editor (Python, MCP) or in C++. That is the single biggest difference for agent-driven work.
- **C++ means a compile step.** GDScript changes take effect the next time Godot runs. Unreal C++ changes are compiled, with Live Coding available while the editor is open. The predict-build-verify loop is slower per iteration.
- **The framework decides more for you.** Godot let the two agents choose different owners for the score. Unreal's Game Mode / Game State / Player State split points to a conventional answer, and it is built for networked games: Game State replicates to clients, while the Game Mode exists only on the server.
- **Licence.** Unreal is **source-available, not open source**. Licensees get full source access under the Unreal Engine EULA, and games pay a 5% royalty on lifetime gross revenue above the first US$1 million per product. Godot's MIT licence has no royalty.

| Godot (this chapter) | Unreal Engine 5 |
|---|---|
| `Area2D` + `area_entered` | Trigger volume / component overlap event |
| Score node | Game State (team score) or Player State |
| `Label` on a `CanvasLayer` | UMG widget |
| `.tscn` text scene | Binary `.umap` level and `.uasset` Blueprint |
| `godot --headless --script test.gd` | `UnrealEditor-Cmd <project> -ExecCmds="Automation RunTest <name>;Quit" -unattended -nullrhi -ReportExportPath=<dir>` |
| Agent edits text directly | Agent drives the editor (Python, Unreal MCP) or writes C++ |

---

## Sources

Godot, the tools, and this chapter's runs:

- `godot --help`, Godot 4.7.2, captured 27 September 2026: [`examples/00-the-toolchain/verification/godot-4.7.2-help.txt`](../examples/00-the-toolchain/verification/godot-4.7.2-help.txt)
- Godot docs, [Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) (running on each OS, `PATH`, `--path`, `--script`, `--check-only`, `--import`, export templates)
- Godot docs, [Idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)
- Godot 4.7.2 source, [`core/os/os.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/core/os/os.cpp) (`OS::add_frame_delay`) and [`main/main.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/main/main.cpp) (`low_processor_mode_sleep_usec` default 6900, "Roughly 144 FPS")
- Godot, [License](https://godotengine.org/license/)
- `walker-pong`, [github.com/nikbearbrown/walker-pong](https://github.com/nikbearbrown/walker-pong) at `c0cbc71`; upstream [godot-demo-projects](https://github.com/godotengine/godot-demo-projects) `2d/pong` at `a3b5c11`
- Walker framework, [github.com/nikbearbrown/walker](https://github.com/nikbearbrown/walker): `README.md`, `publish.sh`
- Claude Code docs, [How Claude remembers your project](https://code.claude.com/docs/en/memory) (CLAUDE.md and AGENTS.md) and [Choose a permission mode](https://code.claude.com/docs/en/permission-modes)
- Codex, [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md); `codex exec --help` (Codex CLI 0.153.4)
- The worked example: [`examples/00-the-toolchain/`](../examples/00-the-toolchain/)

Unity (documentation checked 27 September 2026):

- [Unity Editor command-line arguments](https://docs.unity3d.com/Manual/EditorCommandLineArguments.html) (Unity 6.6)
- [Unity Test Framework: command-line reference](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html)
- [Time.captureDeltaTime](https://docs.unity3d.com/ScriptReference/Time-captureDeltaTime.html)
- [Contents of the Asset Database](https://docs.unity3d.com/Manual/asset-database-contents.html) and [Editor project settings](https://docs.unity3d.com/Manual/class-EditorManager.html) (Force Text serialization); [Understanding Unity's serialization language, YAML](https://unity.com/blog/engine-platform/understanding-unitys-serialization-language-yaml) (fileIDs and GUIDs)
- [Unity MCP overview](https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.0/manual/unity-mcp-overview.html) and [Unity MCP Server: how to get started](https://unity.com/blog/unity-ai-mcp-how-to-get-started) (May 11, 2026)
- [Unity pricing updates](https://unity.com/products/pricing-updates) (Unity Personal threshold)

Unreal Engine (documentation checked 27 September 2026, UE 5.8):

- [Run automation tests in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine)
- [Unreal Engine command-line arguments reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-command-line-arguments-reference)
- [Unreal MCP in Unreal Editor](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?lang=en-US)
- [Scripting the Unreal Editor using Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python)
- [UE Diff Tool](https://dev.epicgames.com/documentation/en-us/unreal-engine/ue-diff-tool-in-unreal-engine)
- [Game Mode and Game State](https://dev.epicgames.com/documentation/en-us/unreal-engine/game-mode-and-game-state-in-unreal-engine)
- [Unreal Engine licensing](https://www.unrealengine.com/license) and [Unreal Engine EULA](https://www.unrealengine.com/eula/unreal)
