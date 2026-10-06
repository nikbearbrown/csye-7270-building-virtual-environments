# Module 13 — Profiling and Optimization

CSYE 7270 · Fall 2026 · Week 13

## Executive summary

A number is only trustworthy if you know what the instrument measured. This module teaches Godot 4.7.2's performance tools as machinery: the frame budget, what `Performance.TIME_PROCESS` really reports, what a headless run can and cannot time, and which editor tools a person with a screen must use for the GPU (the graphics processor). You will direct Claude Code to build the benchmark for a claim that Godot's bullet demo makes and the Walker project refuses to repeat without proof: that moving 500 bullets through the physics server beats using nodes. On 27 September 2026 the instructor ran that benchmark ten times per setting on one Mac. At the demo's 500 bullets the median run cost 0.331 ms per simulated frame with nodes and 0.167 ms with servers, and at 5,000, 9.854 ms and 2.314 ms; these are processor numbers from a desktop, with the GPU excluded. They justify the optimization at thousands of bullets, not at 500, and say nothing about a phone or a headset. This module and Module 12 feed Assignment 9, "Sound That Provably Plays, and a Frame You Can Afford."

## The question

The comment at the top of `bullets.gd` in Godot's bullet demo says that managing 500 bullets through `PhysicsServer2D` and a single `_draw()` call is "a lot more efficient than using instancing and nodes." The Walker README for the same project says no speedup is claimed without a comparative benchmark.

Who is right? And what would it take to know: at 500 bullets and at 5,000, with a test proving both versions are the same game and numbers that survive being run twice? Behind that sits a harder question: **is this change justified?** "Faster" is not a justification. "Faster by enough to matter against a frame budget, on the hardware you target, at the load you ship, and worth what it costs in readability and risk" is.

## The ideas

### Frame time is the unit, and a frame has four places to spend it

A game has a budget per frame: at *f* hertz, 1000/*f* milliseconds.

| Target | Budget per frame |
|---|---|
| 30 Hz | 33.3 ms |
| 60 Hz | 16.7 ms |
| 72 Hz | 13.9 ms |
| 90 Hz | 11.1 ms |
| 120 Hz | 8.3 ms |

Frames per second misleads: dropping from 60 to 50 FPS costs 3.3 ms per frame, while 30 to 25 costs 6.7 ms. Convert to milliseconds before comparing, and check the worst frames: a game that averages 10 ms but takes 40 ms twice a second stutters. The benchmark here reports the mean, the 95th percentile and the maximum.

A Godot frame spends time in four places. **Physics** is `_physics_process` plus the physics server's step at a fixed tick (`physics_ticks_per_second`, 60 by default); a long frame can force the next to run extra steps, up to `max_physics_steps_per_frame` (8 by default). **Process** is `_process`, signals, animation, GDScript. **Render submission** is the CPU work of culling, sorting and building draw commands. **GPU work** is the draws, fill rate and shaders. A frame is CPU-bound when the first three set its length and GPU-bound when the fourth does, and the fixes differ: fewer draw calls cannot help a frame stuck in a GDScript loop. Godot's [general optimization page](https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html) gives the loop: profile, find the bottleneck, optimize it, profile again.

### The Performance singleton, and what its numbers actually are

Godot exposes engine counters through the [`Performance` singleton](https://docs.godotengine.org/en/stable/classes/class_performance.html): `TIME_FPS`, `TIME_PROCESS`, `TIME_PHYSICS_PROCESS`, `OBJECT_COUNT`, `OBJECT_NODE_COUNT`, `MEMORY_STATIC` (unavailable in release builds), `RENDER_TOTAL_DRAW_CALLS_IN_FRAME` and more. The one-line description of `TIME_PROCESS` is "time it took to complete one frame," which is not the whole story.

In the 4.7.2 source ([`main/main.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/main/main.cpp)), the main loop keeps a running maximum of frame time and publishes it, then resets it, only once a second has passed. So `TIME_PROCESS` is **the worst frame in roughly the last second**: not the last frame, not an average. Before the first second it is **zero**: the instructor's probe read `0.0` after 120 fast frames and `0.0177` after 3.5 s. `Performance.add_custom_monitor()` lets your game publish its own counters (bullets alive, enemies spawned), which a test can read and a log can keep.

### Headless timing: what it includes, what it cannot, and the 6.9 ms sleep

`--headless` means a dummy display and a dummy audio driver ([command-line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)). With 5,000 `Sprite2D` nodes in the tree, the instructor found draw calls, video memory and the viewport's CPU and GPU render times all reading **0**, and `RenderingServer.get_video_adapter_name()` empty. Object and node counts, static memory, and script and physics wall-clock time are real.

The surprise is pacing. With no flags, that probe ran at about 144 frames per second, and a Codex-written benchmark in Chapter 9 of the companion book measured 6.90 ms for every case, even an empty scene. When the display cannot draw, the engine sleeps toward a target frame period after each frame (`application/run/low_processor_mode_sleep_usec`, default 6,900 µs), so any per-frame cost under 6.9 ms disappears into the sleep.

Two flags change this. **`--max-fps 60`** raises the sleep to a 60 Hz period; the probe then ran at 60 FPS. **`--fixed-fps 60`** disables real-time synchronization: each frame advances the game by exactly 1/60 s, runs one physics step, and starts the next frame immediately, so wall time per frame is CPU work per simulated frame. That suits this module's question and not others: audio still runs in real time, and a `--fixed-fps` timing is never a real-time frame time on screen. Say which mode every number came from.

### The tools for a person with a screen

The editor's Debugger panel holds the tools that see the GPU ([debugger panel](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_panel.html)). The **Profiler** gives per-function script time and frame time; you press Start, because recording is expensive ([the profiler](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler.html)). The **Visual Profiler** shows time by rendering stage on the CPU and GPU, varies with viewport resolution, and is not supported with the Compatibility renderer on macOS. This module's Walker project uses Compatibility, so on a Mac you must switch renderer (and then measure a different one) or use Windows or Linux. **Monitors** graph the `Performance` counters.

The [CPU optimization page](https://docs.godotengine.org/en/stable/tutorials/performance/cpu_optimization.html) adds the caveat that keeps numbers honest: recording can slow the project significantly. Time with the profiler off; turn it on to learn where the time went. The old course's page "Profiling in Unity and Unreal" made two points that hold in any engine: profile on the device you ship to, not only in the editor, and read the profiler as a chart over time, because players feel the spikes.

### Nodes, servers, MultiMesh, and spikes that are not per-frame cost

A node is a convenient bundle: a name, a place in the tree, signals, an Inspector entry, and a handle to a low-level object owned by a server (`PhysicsServer2D`, `RenderingServer`, `AudioServer`). You can skip the bundle and talk to the server directly with RIDs. Godot's page on [optimization using servers](https://docs.godotengine.org/en/stable/tutorials/performance/using_servers.html) lists what nodes cost, then says it is usually not a problem and that servers pay off at tens of thousands of instances. [`MultiMesh`](https://docs.godotengine.org/en/stable/tutorials/performance/using_multimesh.html) is the drawing half: one draw call for many instances, with no culling of individual ones. The trade is always speed for visibility: server objects do not appear in the scene tree or the Inspector, so their bugs are harder to see.

Some of the worst frames are not steady cost. Loading a large resource on the main thread stalls one frame for as long as the load takes. `ResourceLoader.load_threaded_request()` starts a background load; call `load_threaded_get()` before it finishes and it blocks like `load()` ([background loading](https://docs.godotengine.org/en/stable/tutorials/io/background_loading.html)). Threads cost too, and shared data needs a `Mutex` ([multiple threads](https://docs.godotengine.org/en/stable/tutorials/performance/using_multiple_threads.html)).

### Mobile and XR: design for it, measure on the device

You cannot measure a phone or a headset from this Mac's terminal. Godot's [renderer comparison](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html) marks Compatibility as the low-end mobile choice and Mobile as the high-end one, and recommends Mobile for standalone headsets, while the Android XR deployment page advises Compatibility for Android XR devices for now. The official pages disagree, so record which one you followed and test on the headset. Headsets run at a minimum of 72 Hz (13.9 ms) for two eye views, and mobile fill rate is expensive: transparent particles and full-screen effects are where it bites. A desktop CPU measurement offers a mobile decision only a *ratio* between two implementations of the same work: a hypothesis for the device, not a prediction.

## The Walker example: walker-2d-bullet-shower

[`walker-2d-bullet-shower`](https://github.com/nikbearbrown/walker-2d-bullet-shower) is a public repository that keeps the upstream MIT license. It is the Walker adaptation of Godot's official `2d/bullet_shower`, copied from `godot-demo-projects` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`.

**What it is.** Not a game with a goal: 500 bullets drift left at 20–80 px/s and wrap around, and no bullet is a node. `bullets.gd` creates one shared circle shape (radius 8) and, per bullet, a `PhysicsServer2D` body identified by an RID, moves every body in `_physics_process` with `body_set_state`, and draws all 500 textures from one `_draw()`. The player is an `Area2D` that follows the mouse and shows a sad face while any bullet touches it.

**What its checks established, and the bug they found.** Headless import and a 120-frame run exit 0, and mouse and collision probes see 500 bullets, the sad face and the recovery. Then a motion probe **failed**: after 60 physics frames a bullet's body sat at y = 514.94 while its drawing sat at y = 498.89. The bodies were in `RIGID` mode with a vertical velocity of 962.86, so they fell under gravity between the script's updates, each collision shape one tick of fall (962.86 / 60 = 16.05 px) below its sprite. The Walker fix is one line per body, `PhysicsServer2D.body_set_mode(bullet.body, PhysicsServer2D.BODY_MODE_STATIC)`, after which all 500 bodies align (`ALIGNED_BODIES 500/500`). That is the other cost of skipping nodes: an `Area2D` chooses sensible physics for you, while a bare server body does what its defaults say. Nobody sees a 16-pixel hitbox offset in a screenshot; a player feels it as unfairness.

**What remains unverified.** Visual play and any performance number; the build's own log says it is "not a performance benchmark or visual review."

Six other public builds each stopped where headless evidence stops; two to open are [`walker-loading-threads`](https://github.com/nikbearbrown/walker-loading-threads), which reproduced a race and then passed 29/29 checks, and [`walker-misc-custom-logging`](https://github.com/nikbearbrown/walker-misc-custom-logging), which routes the game's own messages through a `Logger` you control, the seed of analytics. The [chapter](../../chapters/13-profiling-and-optimization.md) tabulates all six.

## Predict → Build It → Use It → Ship It → Verify

You will build a node-based bullet field (the **baseline**), keep the server-based one (the **optimization**), add a parity test proving they behave alike, and add a harness that measures both. Then you decide whether the optimization is justified.

### 1. Predict

Answer in writing before delegating:

- At the shipped 500 bullets, will the node version cost more or less than 1 ms per simulated frame? Will servers be 2× faster, 10× faster, or indistinguishable?
- From 500 to 5,000 bullets, will the node version's cost grow linearly, faster than linearly, or slower?
- If you read `Performance.TIME_PROCESS` once at the end of a 600-frame run that took half a second, what will it say?
- Name two costs the server version still pays and two it avoids. Which can a headless run measure?

Keep your answers: a wrong prediction is evidence of learning.

### 2. Build It

Get your own copy of [`walker-2d-bullet-shower`](https://github.com/nikbearbrown/walker-2d-bullet-shower); Claude Code can help you clone it and record the starting revision. To start from the upstream demo instead, the chapter's route is these two commands, then copy `2d/bullet_shower` into a new folder as `godot/`, apply [`walker-adaptation.diff`](../../examples/13-profiling-and-optimization/walker-adaptation.diff) (the title and one line), copy in the three Walker tests from [`examples/13-profiling-and-optimization/tests/`](../../examples/13-profiling-and-optimization/tests/), run `git init`, and commit:

```bash
git clone https://github.com/godotengine/godot-demo-projects.git
```

```bash
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

Import once, then run the motion test as your baseline:

```bash
godot --headless --path godot --import
```

```bash
godot --headless --path godot --script res://test_motion.gd
```

Expect `MOTION_OK true BODY_SYNC true` and `ALIGNED_BODIES 500/500`. Then give Claude Code this prompt, saved as `prompt1.txt`. It names the one change, the invariant, the parity evidence required before any timing is trusted, and the command.

```text
You are working in a copy of walker-2d-bullet-shower, a Godot 4.7.2 GDScript demo in godot/. Inspect before editing: read godot/README.md, godot/shower.tscn, godot/bullets.gd, godot/player.gd, godot/test_motion.gd, godot/test_collision_input.gd and FRICTIONAL.md.

bullets.gd claims that managing bullets through PhysicsServer2D and a single _draw() is "a lot more efficient than using instancing and nodes". Our README refuses to repeat that claim without a benchmark. Build the benchmark. Do not change how the game plays.

Requirements
1. Make the bullet count configurable without changing the default: bullets.gd still makes 500 bullets unless a benchmark sets a different count before the node enters the tree.
2. Add a node-based baseline in godot/bench/: bullets_nodes.gd and shower_nodes.tscn. Same player, same bullet image, same circle radius 8, same speeds, spawn and wrap rules, same collision layer and mask as bullets.gd, but each bullet is an Area2D with a CollisionShape2D and a Sprite2D, and one manager script moves all of them in _physics_process.
3. Add godot/bench/bench.gd (extends SceneTree), run as
   godot --headless --fixed-fps 60 --path godot --script res://bench/bench.gd -- --mode=servers --count=500 --frames=600
   It loads shower.tscn (servers) or bench/shower_nodes.tscn (nodes), skips 120 warm-up frames, then times each measured frame with Time.get_ticks_usec() and prints one CSV line: mode,count,frames,mean_ms,p95_ms,max_ms,object_count,node_count,static_memory_mb. Also print Performance.TIME_PROCESS and TIME_PHYSICS_PROCESS with a note on what they measure. Free the scene cleanly before quitting.
4. Before trusting any timing, check that the baseline behaves like the original: add godot/bench/test_nodes_parity.gd that checks the node version has the requested bullet count, that one bullet moves left by speed x elapsed physics time within 0.05 px over 60 physics frames, and that the player's touching count rises when the mouse is moved onto a bullet (the approach in test_collision_input.gd). Print PASS/FAIL lines and quit(1) on failure.
5. Run the parity test, the three existing tests, and the benchmark once per mode at counts 500 and 5000. Paste the real output. Say what this measurement includes and excludes: it is headless with a dummy renderer, so GPU and draw cost are not in it.
```

```bash
claude -p "$(cat prompt1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --disallowedTools "Skill" --max-turns 60 --output-format stream-json --verbose > session1.jsonl
```

Two lessons from the recorded run are built into that command. `--disallowedTools "Skill"` stops the agent from invoking skills; in the recorded run, an agent refused a command invoked a skill whose job is to add permission rules. And the allow list names `godot`, so put "Run Godot as the plain command `godot`" and your test commands in `CLAUDE.md` or `AGENTS.md`; otherwise the agent may find the app's absolute path and be refused repeatedly. With Codex the equivalent is `codex exec -s workspace-write -C . "$(cat prompt1.txt)" < /dev/null`. In Chapter 9's Codex run the sandbox blocked Godot's log file under the home folder, which is harmless for these tests.

### 3. Use It

The headless numbers cover the CPU; the screen covers the rest. Every judgment here is a **HUMAN CHECK**.

1. Run `shower.tscn` and move the mouse through the bullets. **HUMAN CHECK:** does the face turn sad exactly when a bullet overlaps it? That is the alignment bug, by eye.
2. Open **Debugger → Monitors** and watch `Time → Process`, `Time → Physics Process` and `Object → Nodes`, then run `bench/shower_nodes.tscn` with F6 and compare. `bullet_count` is a plain `var`, not an `@export`: to see 5,000 bullets, change its default in `bench/bullets_nodes.gd` temporarily and revert.
3. Start the **Profiler**, run ten seconds, stop, and find each `_physics_process`. **HUMAN CHECK:** is the script's own time most of the frame, or the physics step?
4. On Windows or Linux, open the **Visual Profiler** and compare the node version's draw time with the server version's single `_draw()`, the cost the headless benchmark cannot see. On a Mac it will not run with this project's renderer.
5. With an Android phone or a standalone headset, export both scenes and compare there. That needs Godot's export templates (a large download) and the platform SDK; Module 15 covers exporting. The recorded run did not do this.

### 4. Ship It

Commit in order: baseline; configurable count; node baseline and parity test; the harness; your repeated measurements as CSV, with machine, date and load in the message. `FRICTIONAL.md` gets the prompt, the commands, every failure and its real cause, and the decision with its numbers; if the agent writes its own entry, check each sentence against the output. `SOURCES.md` says the benchmark and parity scripts are AI-written and human-verified.

The Brutalist film skill that fits is `godot-gamedev`. Show `bullets.gd`'s server calls beside `bullets_nodes.gd`'s nodes, the parity test's PASS lines and the measurement table, and say out loud what a headless number excludes. The Brutalist skills come from the course-provided checkout; request the update if your copy lacks the skill.

### 5. Verify

Run the parity check and an existing test yourself, with a timeout; a script that hits a runtime error before `quit()` never exits:

```bash
timeout 120 godot --headless --path godot --script res://bench/test_nodes_parity.gd -- --count=5000
```

```bash
timeout 120 godot --headless --path godot --script res://test_motion.gd
```

Then measure more than once, in fresh processes, alternating the modes so whatever else the machine is doing affects both. The instructor's scripts are in [`examples/13-profiling-and-optimization/verification/`](../../examples/13-profiling-and-optimization/verification/); copy them into your project root, the folder that contains `godot/`. The sweep script does not use `timeout`, so be ready to stop a hung run.

```bash
bash sweep.sh . sweep.csv
```

```bash
python3 summarize.py sweep.csv
```

**A pass establishes** that, for the cases tested, the two versions have the same count, motion and collision behavior, and gives each one's CPU cost per simulated frame on your machine at that moment. **It does not establish** draw cost, GPU cost, real-time frame pacing, or anything about a device you did not run on.

Your milliseconds will differ. On the instructor's shared Apple M4 Pro, the median of ten run means under `--fixed-fps 60` was:

| Bullets | Nodes | Servers | Range of node run means (ms) |
|---|---|---|---|
| 500 | 0.331 ms | 0.167 ms | 0.313–2.268 |
| 2,000 | 2.845 ms | 0.707 ms | 2.427–11.622 |
| 5,000 | 9.854 ms | 2.314 ms | 8.508–39.009 |

The variance is the machine, not the code: runs during a load spike (load average up to 27) took the node version at 5,000 from 8.5 ms to 39.0 ms with identical code. The ratio grows with the count, about 2× at 500 and about 4× at 2,000 and 5,000. At the shipped 500, nodes cost about 0.33 ms (2% of a 60 Hz budget) and servers save about 0.16 ms of it: **not justified** for the game as shipped, since the saving is tiny and the node version is visible and cannot have the falling-body bug. At 5,000, nodes take 9.9 ms, 59% of a 60 Hz budget and 89% of a 90 Hz one before any drawing, so servers are justified there, on these numbers plus a parity test, not on a source comment.

## What the agents got wrong

The recorded run (Claude Code 2.1.150 with `claude-sonnet-4-6`, 27 September 2026) is the lesson: an agent's "done" is a claim.

**A refusal became a hunt for new rules.** The agent used Godot's absolute path, but the allow list said `godot`, so every call was refused. It retried with a sandbox-bypass flag, then invoked a permission-editing skill and tried to read `~/.claude/projects`. The instructor stopped it at tool call 45; no settings file was written. An agent refused a command should report the refusal.

**A hung process the agent left behind.** The agent edited an existing test it was not asked to touch; the edit read a freed object, hit a script error before `quit()`, and left a headless Godot running 25 minutes. `timeout` would have ended it.

**Correct code, wrong description of its own instrument.** `bench.gd` labels `TIME_PROCESS` as time spent "last frame." Its own output refutes that: servers at 5,000 printed `TIME_PHYSICS_PROCESS=33.452 ms` for a run whose mean frame was 2.67 ms and worst was 37.7 ms. A one-second maximum explains the number; "the last frame" cannot. At 500 bullets both monitors printed 0.000, because 720 fixed-step frames took under a second. The agent still committed an 82-line `FRICTIONAL.md` entry repeating the wrong definition; only reading the engine source caught it.

## If you know Unity or Unreal

Unity and Unreal were not run; these comparisons come from their official documentation, checked on 27 September 2026.

| Godot 4.7.2 | Unity | Unreal Engine 5 |
|---|---|---|
| `Performance` singleton | `ProfilerRecorder` counters | `stat unit` (game, render, GPU) |
| Profiler, Visual Profiler, Monitors | Profiler window, Frame Debugger | Unreal Insights, `stat gpu` |
| `godot --headless --fixed-fps 60 --script …` | `-batchmode -nographics -runTests -testPlatform PlayMode` | `-nullrhi -unattended` |
| Hand-written median, p95, max | Performance Testing package, Profile Analyzer | CSV Profiler (`csvprofile`) |
| Nodes versus `PhysicsServer2D` RIDs | GameObjects versus a manager that draws instances | Blueprint actors versus C++ managers |
| Device runs: not tested here | Development Build with Autoconnect Profiler | Gauntlet framework |

The biggest difference for an agent workflow is what the agent can read. A Godot benchmark, its parity test and its CSV output are text an agent can write, run and diff. Unity's Profiler captures are binary data viewed in the editor: an agent can trigger one but cannot read a flame chart as it reads a CSV line, so ask for CSV or test output a script can compare. Unreal's CSV Profiler writes text, but an actor-per-bullet Blueprint would live in a binary `.uasset` file. The [companion chapter](../../chapters/13-profiling-and-optimization.md) has the full comparison.

## Practice assessment (ungraded)

Answer these in your own words, then check the source:

1. Your benchmark prints `Performance.TIME_PROCESS` once, at the end of a 600-frame run that took half a second. What does it print, and why?
2. Without `--fixed-fps`, a headless benchmark reports 6.9 ms for every case, even an empty scene. Why, and what does the flag change about what the number means?
3. Using the table above, decide whether servers are justified at 500 bullets and at 5,000, in milliseconds and share of a 60 Hz budget, and name the evidence that would change your mind.
4. Your target is a standalone headset at 90 Hz using the Mobile renderer. Write the measurement plan you would run on the device before choosing between nodes and servers for 2,000 bullets.

An ungraded practice quiz is on this module's Canvas page. Do not paste Claude's explanation as proof of your understanding; ask it to question you, then answer from the source.

## The next step

This module, with Module 12, completes the material for Assignment 9, "Sound That Provably Plays, and a Frame You Can Afford." That assignment opens in Module 12 and is due about Day 90 (Canvas dates govern); its own page sets the task and the required `godot-gamedev` film, and this lesson adds no graded deliverable. Carry the method into it: name the budget, benchmark with a parity test, repeat in fresh processes, state what the number excludes. Module 14, game AI and systems, comes next. The long reading is [Chapter 13 — Profiling and Optimization](../../chapters/13-profiling-and-optimization.md).
