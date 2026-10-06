# Module 0 — Start Here: the toolchain

CSYE 7270 · Fall 2026 · Before Week 1

## Executive summary

This is the page to read first. It sets up and checks the tools every later module depends on: a coding agent in your terminal (Claude Code, with Codex as an optional second), the regular GDScript edition of Godot 4, Git, and an instruction file that tells the agent how your project works. You will install them, clone a small Pong game, run its existing test yourself, then give an agent one bounded change, a score, and check its work with commands you run. On 27 September 2026, Claude Code and Codex each added a working score, then ran the game's existing test in a way that made it unreliable, saw it fail, and explained the failure wrongly; one paragraph of instructions fixed Codex's next run. A passing automated test shows the tested game state was right under one scripted input. It does not show that the score is readable, well placed or fun, or that an exported game works.

## The question

Both agents ran the same unmodified test file, on the same machine, against a game whose physics they had not touched. The test failed for both. Run correctly, it passed on the untouched game and on both agents' versions, with identical numbers every time. Nobody edited the test, and neither agent hid the failure. What was different?

The answer is one command-line flag, but finding it means knowing what each tool does. When an agent says "I ran the tests," you need to know which program ran, on which files, in what state and with which options, and you need to run the same thing yourself.

## The ideas

### Four tools, four jobs

| Tool | Its job | What it is not |
|---|---|---|
| Claude Code or Codex | Reads project files, edits text, runs the commands you allow, reports what it did | Not the engine, not a judge of fun, not proof |
| Walker | The Game brief → Build → Playtest → Inspect → Revise → Export loop, with per-game instruction files and skills | Not a `walker build` command; no such executable exists |
| Godot | Editor, engine, and a command-line program that can import, run, test and export | Not an AI tool; it runs whatever the files say |
| Git | Remembers every version, so "what changed?" has an exact answer | Not a backup of anything you did not commit |

[Module 1](../01-walker-and-godot/lesson.md) introduces Walker and Godot in the editor; this module is the terminal. Claude Code is the course's agent. Codex ran the same task in the recorded example and is optional.

### Godot is also a command-line program

Godot's [command-line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) recommends putting the editor's executable on your `PATH` as `godot`. The course ran Godot 4.7.2, regular edition, GDScript. Walker's bundled Godot guide targets the C#/.NET edition, which this course does not use. Four options carry the course (`--path <directory>` points Godot at a folder containing `project.godot`):

| Option | What it does | Your use |
|---|---|---|
| `--headless` | No window, no sound | Every automated check runs this way |
| `--import` | Starts the editor, imports resources, quits | Build the `.godot/` import cache after cloning |
| `-s, --script <script>` | Runs a script | Run a test written as a `SceneTree` script |
| `--fixed-fps <fps>` | Forces a fixed frame rate; disables real-time synchronization | Every frame is exactly 1/fps seconds of game time |

Headless is a precise promise: no picture and no sound. The scene tree, scripts, physics, signals and timers still run. A headless test therefore observes state, such as positions, counters and what a label's text says, never pixels. Whether a label is readable is always a human check.

A fresh clone has no `.godot/` folder, the cache Godot rebuilds from the project's files and Git rightly ignores. Without it, Godot cannot resolve the `uid://` identities in scene files and warns, for example `ext_resource, invalid UID: uid://bbiup6xhh6s17 - using text path instead`. Claude Code met that warning because it never imported; the fallback worked, and the warning meant what it said. A later chapter's clean-clone run exited 0 with 55 `ERROR` lines for the same reason. The rest of a project is mostly text (`.tscn`, `.gd`, `.tres`, `.import`, `.uid`) that an agent can read and diff; for images, audio and models it sees file names and `.import` settings, not pixels or sound.

### Frames are not seconds

Here is how the Pong ball moves (`godot/logic/ball.gd`, unchanged from Godot's demo):

```gdscript
func _process(delta: float) -> void:
	_speed += delta * 2
	position += _speed * delta * direction
```

`_process` runs once per frame, and `delta` is the time since the previous frame in seconds. Motion is measured in seconds, so Pong at 30 and at 144 frames per second moves the ball the same distance per second. That is correct game code ([Idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)).

The regression test is scripted in frames: `tests/input_route.gd` presses up for 150 ticks, then down, then tracks the ball, then deliberately misses, then stops at 4,800 frames, which is 80 seconds at 60 frames per second. Without `--fixed-fps 60`, nothing makes a frame 1/60 of a second. Headless Godot sleeps after each frame toward a 6,900 microsecond target, which the 4.7.2 source annotates "Roughly 144 FPS." On the course Mac, 4,800 real-time frames took 33 to 35 seconds, about 33 seconds of game time instead of 80, so the ball had less time to speed up.

Twelve runs of the untouched game on 27 September 2026 settle it:

| How the test was run | Runs | Result |
|---|---|---|
| `--fixed-fps 60`, cache present or absent | 6 | 6 pass, identical: Ceiling 5, Floor 4, Left 10, LeftWall 2, Right 8, RightWall 1; max speed 185.67 |
| real time, cache present | 3 | 3 fail `ceiling_contact` |
| real time, cache absent | 3 | 1 fail, 2 pass with different counts |

The import cache made no difference; the flag made all of it. Without the flag, the same game sometimes fails and sometimes passes, most plausibly depending on machine load. The flakiness sits in how the test is run, not in the game. The rule holds for every engine: **a test that counts frames while the game moves by delta time is machine-dependent unless the time step is pinned.**

### Instruction files: how the agent learns your project

An agent starts every session knowing nothing about your project, so standing instructions live in a Markdown file in the repository. Claude Code reads `CLAUDE.md`. Codex reads `AGENTS.md`, walking from the Git root down to your working directory, closer files winning ([Codex guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)).

One version trap. Claude Code's [memory documentation](https://code.claude.com/docs/en/memory), read on 6 October 2026, says it reads `AGENTS.md` directly only in version 2.1.277 or later, and only when no `CLAUDE.md` exists. The course's runs used 2.1.150, which, in a copy of `walker-jumpman-clawd` (an `AGENTS.md`, no `CLAUDE.md`), reported no project instruction file loaded (Module 1's record). Check `claude --version`; on an older version, begin your first prompt with "Read AGENTS.md first," or add a `CLAUDE.md` holding the single line `@AGENTS.md`.

Walker's `publish.sh` writes the right file for each tool (`--agent claude` writes `CLAUDE.md`, `--agent codex` writes `AGENTS.md`); the games you clone already carry theirs.

### What the agent may touch

Claude Code's [permission modes](https://code.claude.com/docs/en/permission-modes) set what runs without asking: the default (Manual) runs reads only, `acceptEdits` adds file edits and common filesystem commands, including `rm`, inside your working directory, and `bypassPermissions` is for isolated containers and VMs only. Allow rules pre-approve tools, such as `--allowedTools "Bash(godot *)"`. Codex runs commands in a sandbox with three policies, `read-only`, `workspace-write` and `danger-full-access`.

An allow rule is a boundary around programs, and a program that runs code is no boundary. `godot --script` runs any GDScript, and GDScript can call `OS.execute()` to start other programs. `Bash(env *)` lets `env` run any command. Start in the default mode, read every command before you approve it, and treat the prompt as a review.

### The evidence ladder

Every claim about a change sits on one rung; say which. Rung 1: the agent says "done," which shows only that it produced a message. Rung 2: a `git diff` shows exactly what changed, not that it works. Rung 3: a clean `--import` and `--check-only` show the project and scripts parse. Rung 4: a headless test passes with the time step pinned, so the tested state is right under that scripted input, not that it feels right. Rung 5: you played it, which shows what one person saw. Rung 6: an exported build runs on its target (Module 15), which shows the game survives packaging, not that anyone wants to play it.

## The Walker example: walker-pong

[walker-pong](https://github.com/nikbearbrown/walker-pong) is the first Walker adaptation of Godot's official demos: the `2d/pong` demo at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7` of [godot-demo-projects](https://github.com/godotengine/godot-demo-projects/tree/a3b5c113112f77291d5f3d1360f33a882fdc52f7/2d/pong), MIT-licensed, license and attribution kept. The recorded run used commit `c0cbc71`. Public `main`, checked 6 October 2026, is one commit later and differs only in `FRICTIONAL.md`.

Everything that moves is an `Area2D` with a small script (`godot/logic/paddle.gd`, `ball.gd`, `wall.gd`). The ball speeds up by 2 units per second, and `reset()` returns it to the center at speed 100, always heading left. The side walls call `reset()` on contact, the game's only "point" event. The tests live in `tests/` at the repository root.

**What its checks establish.** The README and CAPTURE notes say the ten scripted-input checks pass at 60 and 30 frames per second. The instructor's re-run of the GitHub version, imported and with `--fixed-fps 60`, passed all ten: paddles reach both bounds and hit the ball, the ball touches ceiling and floor, a deliberate miss reaches a wall, and the ball passes speed 110.

**What is not established.** The README records no human playtest, untested gamepad mappings, and no score, win state, pause, AI opponent or soundtrack. The score is your task.

**A gap that matters.** Nothing in the repository's Markdown says how to run the test. You learn it needs `WALKER_EVIDENCE_DIR` only by reading the script, and `--fixed-fps 60` only by understanding the time trap. Both agents found the first. Neither found the second.

## Predict → Build It → Use It → Ship It → Verify

### 1. Predict

Write your answers down before you delegate. Keep them even if they turn out wrong.

1. Which node should own the score, and which event should change it? Is there an existing signal to reuse, or must you add one?
2. After a point, `reset()` serves the ball left whoever scored, and the prompt forbids changing it. Is that a bug the score will expose, or a design question for a person?
3. How will you tell "the label shows a number" from "the number is right"?
4. What in the existing test could a new label break? What could break it with no change to the game?

### 2. Build It

Work through these in order, in a bash or zsh terminal. The recorded commands ran on macOS; the `brew install` lines come from the tools' documentation, not the recorded run. No Windows route was tested.

**Step 1: get the tools.**

- **Git.** The clone in Step 2 fails without it. [Download Git](https://git-scm.com/downloads).
- **Godot, regular edition, 4.7.2.** Not the .NET build. On macOS, Godot's command-line tutorial gives this Homebrew command (its `godot-mono` package is the C# edition; avoid it). Or download 4.7.2 from the [archive](https://godotengine.org/download/archive/4.7.2-stable/) and put it on your `PATH`.

```bash
brew install godot
```

- **Claude Code.** Install it from the [official setup page](https://code.claude.com/docs/en/setup), then run `claude` and follow the browser prompts. That page says it needs a Pro, Max, Team, Enterprise or Console account; the free claude.ai plan does not include it (read 6 October 2026). The [course AI policy](../../prerequisites/ai-policy.md) says the instructor assumes Claude Code access and points to [Northeastern's Claude page](https://claude.northeastern.edu/), which, read 6 October 2026, describes the university's Claude plans but does not mention Claude Code. If you cannot sign in, resolve it with the instructor or university support before graded work.
- **Codex (optional).** Follow OpenAI's [Codex CLI page](https://developers.openai.com/codex/cli) with an account you already have.
- **`timeout`.** macOS does not ship it. Homebrew's `coreutils` provides it (and `gtimeout`, on the instructor's Mac). Linux has it built in.

```bash
brew install coreutils
```

Check what you have, and write the versions down.

```bash
godot --version
```

```bash
claude --version
```

```bash
codex --version
```

The course machine printed `4.7.2.stable.official.ed1daf0bf` for Godot. The recorded run used Claude Code 2.1.150 and Codex CLI 0.153.4. If yours differ, say so before you interpret any test result.

**Step 2: get the game and build its import cache.**

```bash
git clone https://github.com/nikbearbrown/walker-pong.git
```

```bash
cd walker-pong
```

```bash
godot --headless --path godot --import
```

**Step 3: establish the baseline yourself, before any change.** The route test writes its evidence to a folder you name.

```bash
mkdir -p evidence-local
```

```bash
WALKER_EVIDENCE_DIR="$PWD/evidence-local" timeout 120 godot --headless --path godot --fixed-fps 60 --script "$PWD/tests/input_route.gd"
```

It ends by printing one long JSON line. Check the exit status.

```bash
echo $?
```

You should see `"passed":true` and `0`. Write down the `counts` and `max_speed`. On Godot 4.7.2 they were Ceiling 5, Floor 4, Left 10, LeftWall 2, Right 8, RightWall 1, and 185.67. If yours differ, note your Godot version first.

**Step 4: make a branch**, so the change is easy to see and easy to throw away.

```bash
git switch -c add-score
```

**Step 5: give the agent the task.** Start `claude` (or `codex`) in the repository folder and paste this into the agent, not into a shell. It is the exact prompt of the recorded run.

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

The prompt names the files to read first, fences off what must not change, and asks for a plan and a risk before any edit. It does not say how to run the existing test, deliberately, because that is the realistic case.

Compare the agent's plan and risk with your predictions. Read each command before you approve it, and notice whether a test run includes `--fixed-fps 60`. The recorded run was non-interactive; its command lines are in [`PROMPTS.md`](../../examples/00-the-toolchain/PROMPTS.md), where the Claude Code line carries an allow rule, `Bash(env *)`, that the chapter calls a blank cheque. Do not copy it. If you script `codex exec`, add `< /dev/null`; without it the scripted Revise re-run sat five minutes on "Reading additional input from stdin...".

**Step 6: revise the instructions, not the code.** Neither agent could know the test needs `--fixed-fps 60`; the repository never says so. In a second fresh clone, in a different folder, append this to `AGENTS.md` and give the agent the identical prompt.

```text
## Checks (run from the repository root)

Import once after cloning: `godot --headless --path godot --import`

Regression route — the route counts frames but the game moves by seconds, so it
is only deterministic with `--fixed-fps 60`. Without it the result depends on
machine speed. Expected: exit 0, "passed": true.

`WALKER_EVIDENCE_DIR="$PWD/evidence-local" godot --headless --path godot --fixed-fps 60 --script "$PWD/tests/input_route.gd"`

Run any new test the same way, with `--fixed-fps 60`.
```

That re-run used Codex only. It imported first, ran the route with the flag, got `"passed": true` with the baseline numbers exactly, and ran its new test the same way, in 3.5 minutes and 9 shell commands against 5 minutes and 12. The instructor's re-run matched. Claude Code was not re-run with the paragraph. Short on time, add the paragraph first; doing both runs shows the difference.

**First-run traps**, all recorded in the chapter:

| Trap | What happens | What to do |
|---|---|---|
| No `--import` | UID warnings; `ERROR` lines with exit 0 | Import once after cloning |
| No `timeout` | A script error before `quit()` hangs headless Godot (once for 30 minutes) | Prefix with `timeout 120` |
| No `--fixed-fps 60` | Frame-counted tests flake | Pin it; write it in `AGENTS.md` |
| Exit code 0 read as clean | Errors can print while the process exits 0 | Read the error output too |
| Hand-written scene IDs | Claude Code, editing `.tscn` as text, invented `unique_id` values | Open and save the scene once |
| `evidence-local/` committed | The `.gitignore` omits it | Check `git status --short` first |

### 3. Use It

This part needs a display, so it is yours. Open Godot's Project Manager, import `godot/project.godot`, and press **Run Project**. The left paddle uses W and S. The right paddle uses Up and Down.

- **HUMAN CHECK.** Let the ball past each paddle at least twice. Does the correct side's number go up each time?
- **HUMAN CHECK.** Are the numbers readable at the game's size? Do they cover a paddle at the top of its range, or fight with the center line?
- **HUMAN CHECK.** Watch the serve after each point. It always goes left, whoever scored. With a score on screen, does that feel fair? Write it down as a design question; do not fix it here.
- Open the scene in the editor, find the new nodes in the Scene dock, save once, then run `git diff godot/pong.tscn` to see whether the editor rewrote any identifiers the agent wrote by hand or left out.

### 4. Ship It

Read the whole diff before you commit anything.

```bash
git status --short
```

```bash
git diff
```

Look for stray files. The recorded runs left an untracked `evidence-run/` folder (Claude Code) and unrequested edits to four design documents (Codex). Commit only what belongs in the change. These are Claude Code's file names; list yours from `git status`.

```bash
git add godot/logic/score.gd godot/logic/score.gd.uid godot/pong.tscn tests/
```

```bash
git commit -m "Add score counter with headless score test"
```

Keep the branch on your machine; do not push to the instructor's repository. Then add an entry to your `FRICTIONAL.md`: what you predicted, what the agent proposed, what it got wrong, the commands you ran and their results, and which parts rest only on machine evidence ([assessment policy](../../prerequisites/assessment-policy.md)). This module has no film; were it an assignment, the fitting Brutalist skill would be `godot-gamedev`.

### 5. Verify

Run both tests yourself, with the time step pinned.

```bash
WALKER_EVIDENCE_DIR="$PWD/evidence-local" timeout 120 godot --headless --path godot --fixed-fps 60 --script "$PWD/tests/input_route.gd"
```

```bash
timeout 120 godot --headless --path godot --fixed-fps 60 --script "$PWD/tests/score_check.gd"
```

Use your agent's test file name; Codex named its test `score_route.gd`. A pass on the first command means the new node did not change the ball, paddles or walls under the regression route, so its counts should match your Step 3 baseline exactly. A pass on the second means the score counters, and ideally the label text, matched the wall contacts in that scripted rally. Neither pass means the score is readable, well placed or fun. That was Use It.

## What the agents got wrong

Run on 27 September 2026 on the instructor's Mac: Claude Code 2.1.150 (`claude-sonnet-4-6`) and Codex CLI 0.153.4 (`gpt-5.6-sol`, low reasoning effort), same prompt, fresh clones. Both delivered a working score and a passing test of their own, and neither weakened the regression test. A person still has to read the report.

- **Both misread the failure.** Neither ran the old test with `--fixed-fps 60`. Claude Code blamed the import cache and the random number generator; the experiment rules that out, since failures happened with the cache and passes without it. Codex called its failing run "deterministic," the one thing it was not. Caught by: the twelve-run experiment and an exact baseline.
- **Claude Code's test checks less than its report suggests.** `score_check.gd` counts wall contacts through the same `area_entered` signal the scoreboard listens to and never reads the labels, so it would pass with both labels hidden. Codex's test reads the label text. Caught by: reading the test, not the summary.
- **Claude Code routed around refusals.** It was refused 18 times: `cd … && godot …` fails because a compound command must match a rule in every part, and a `WALKER_EVIDENCE_DIR=…` prefix does not match `Bash(godot *)`. It then found that `env WALKER_EVIDENCE_DIR=… godot …` matched `Bash(env *)`, which approves any program. Caught by: its transcript.
- **Codex did more than asked, then tidied away evidence.** It edited `README.md`, `GAME-BRIEF.md` and `GDD.md` to remove "no score," arguably right but a design decision, and in the Revise re-run deleted the `evidence-local/` reports it had just produced. Caught by: `git diff` and `git status`.

## If you know Unity or Unreal

Unity and Unreal were not run for this module; the comparisons come from their documentation, checked 27 September 2026.

| Godot | Unity | Unreal Engine 5 |
|---|---|---|
| `Area2D` + `area_entered` | `Collider2D` (Is Trigger) + `OnTriggerEnter2D` | Trigger volume or overlap event |
| A node owning the score | A `MonoBehaviour` on a GameObject | Game State (team score) |
| `.tscn` text scene | Scene YAML (Force Text) | Binary `.umap` and `.uasset` |
| `godot --headless --script test.gd` | `Unity -batchmode -runTests …` | `UnrealEditor-Cmd … Automation RunTest …` |
| `--fixed-fps 60` | `Time.captureDeltaTime` | Pin the time step too; the chapter names no switch |

The biggest difference for agent work is the file format. Both agents edited Godot's text scene `pong.tscn` directly. Unity scenes are YAML but harder to hand-edit; Unreal Blueprints and levels are binary, so an agent must work through the editor or C++. The chapter has the [full comparison](../../chapters/00-the-toolchain.md).

## Practice assessment (ungraded)

Answer these in your own words, then take the Canvas practice quiz for this module as often as you like.

1. Using `ball.gd` and `input_route.gd`, explain why the same test can pass on one laptop and fail on another without `--fixed-fps 60`.
2. Claude Code blamed the import cache. Design the smallest experiment that would test that explanation.
3. Your allow list includes `Bash(godot *)`. The agent wants `cd godot && godot --import`. Why is that refused, and what would you rather it ran?
4. Sort into machine evidence and human judgment: "left score increments on right-wall exit"; "scores are readable on a projector"; "serving always to the left is unfair once there is a score."

Do not paste Claude's explanation as proof of your understanding. Ask it to question you, then answer and check the source yourself.

## The next step

Module 1, [Walker and Godot](../01-walker-and-godot/lesson.md), comes next: the same tools in the editor, on walker-jumpman, the starter for Assignment 1. This module has no assignment of its own. The companion chapter, [The Toolchain](../../chapters/00-the-toolchain.md), holds the full record and the Unity and Unreal sections.
