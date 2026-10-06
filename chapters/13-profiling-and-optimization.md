# Chapter 13 — Profiling and Optimization

## Executive summary

Optimization without measurement is guessing, and measurement without knowing what your instrument sees is worse: it produces confident numbers about the wrong thing. This chapter teaches Godot 4.7.2's performance instruments as machinery — what `Performance.TIME_PROCESS` actually reports (the worst frame of the last second, not the last frame), what a headless run can and cannot time, why `--fixed-fps` changes what a timing means, and which editor tools a human with a screen must use for the GPU. You will direct Claude Code to build the benchmark that the Walker bullet-shower README refused to fake: a node-based bullet field as the baseline, the existing `PhysicsServer2D` version as the optimization, a parity test proving they behave alike, and a CSV-producing harness. The record shows the agent building it, failing to run it for permission reasons, trying to widen its own permissions, and — once corrected — producing correct code with a wrong description of its own instrument. Ten repeated runs show the server version costing 0.17 ms per simulated frame at the shipped 500 bullets against 0.33 ms for nodes, and 2.3 ms against 9.9 ms at 5,000. Those are CPU numbers from a desktop, with the GPU excluded. They justify the optimization at thousands of bullets. At the game's own 500, they do not. The chapter also sets out what you would have to measure on a phone or a headset before claiming anything there.

## The question

The comment at the top of `bullets.gd` says that managing 500 bullets through `PhysicsServer2D` and one `_draw()` call "is a lot more efficient than using instancing and nodes". The Walker README for the same project says: "No performance speedup is claimed without a comparative benchmark."

Who is right? And what would it take to know — on this Mac, at 500 bullets and at 5,000, with a test that proves both versions are the same game, with numbers that survive being run twice, and with an honest statement of what the numbers leave out?

Behind that question sits a harder one that every optimization faces: **is this change justified?** "Faster" is not a justification. "Faster by enough to matter against a frame budget, on hardware we target, at the load we ship, and worth what it costs in readability and risk" is.

## Ideas you need

### Frame time is the unit; frames per second is the headline

A game has a budget per frame. At a refresh rate *f* the frame must finish in 1000/*f* milliseconds:

| Target | Budget per frame |
|---|---|
| 30 Hz | 33.3 ms |
| 60 Hz | 16.7 ms |
| 72 Hz | 13.9 ms |
| 90 Hz | 11.1 ms |
| 120 Hz | 8.3 ms |

This is arithmetic, and it is why frames per second misleads: dropping from 60 to 50 FPS costs 3.3 ms per frame; dropping from 30 to 25 costs 6.7 ms. Convert to milliseconds before you compare anything. Look at the worst frames too. A game that averages 10 ms and takes 40 ms twice a second stutters, and the average hides it. The benchmark in this chapter reports the mean, the 95th percentile and the maximum for that reason.

Godot's documentation states the discipline plainly: "Always use profiling and timing to guide your efforts," in a loop — profile, identify the bottleneck, optimize it, return to step one ([general optimization](https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html)). The syllabus asks for the same thing in course terms: measure a baseline, make one justified optimization, measure again.

### Where a frame's time goes

At the level you need for this chapter, a Godot frame spends time in four places:

1. **Physics** — `_physics_process` callbacks and the physics server's step, at a fixed tick (`physics_ticks_per_second`, 60 by default). If a frame runs long, the next frame may run more than one physics step to catch up, up to `max_physics_steps_per_frame` (8 by default; both values read from the running engine). A slow frame can make the next frame slower.
2. **Process** — `_process` callbacks, signals, scene-tree bookkeeping, animation, CPU particles, GDScript.
3. **Render submission on the CPU** — culling, sorting, building draw commands.
4. **GPU work** — the draws, fill rate, overdraw, shaders, post-processing.

A frame is **CPU-bound** when 1–3 set its length and **GPU-bound** when 4 does. The fixes are different: cutting draw calls does nothing for a frame that is waiting on a GDScript loop, and rewriting the loop does nothing for a frame waiting on the GPU.

### The Performance singleton, and what its numbers actually are

Godot exposes engine counters through the `Performance` singleton ([Performance](https://docs.godotengine.org/en/stable/classes/class_performance.html)):

| Monitor | Documented meaning |
|---|---|
| `TIME_FPS` | frames rendered in the last second; "only updated once per second" |
| `TIME_PROCESS` | "Time it took to complete one frame, in seconds" |
| `TIME_PHYSICS_PROCESS` | time to complete one physics frame, in seconds |
| `OBJECT_COUNT` | instantiated objects, "including nodes" |
| `OBJECT_NODE_COUNT` | nodes in the scene tree, including the root |
| `MEMORY_STATIC` | static memory in use; not available in release builds |
| `RENDER_TOTAL_DRAW_CALLS_IN_FRAME` | draw calls in the last rendered frame |
| `RENDER_VIDEO_MEM_USED` | texture and vertex memory, in bytes |

The one-line description of `TIME_PROCESS` is not the whole story. In the 4.7.2 engine source, the main loop updates `process_max = MAX(process_ticks, process_max)` every frame, and only when a second has passed (`if (frame > 1000000)`) does it call `performance->set_process_time(USEC_TO_SEC(process_max))` and reset the maximum; physics time is handled the same way ([`main/main.cpp` at 4.7.2-stable](https://github.com/godotengine/godot/blob/4.7.2-stable/main/main.cpp)). So:

- `TIME_PROCESS` is **the worst frame in roughly the last second**, not the last frame and not an average.
- Before the first second has elapsed, it is **zero**. My first probe read it after 120 fast frames and got `0.0`; a second probe that ran for 3.5 s read `0.0177` s (`probes/`).
- In the same source, `process_ticks` covers the main loop's process step, the navigation server, and `RenderingServer::draw` — which, with a dummy renderer, is nearly nothing.

The class reference itself notes that some monitors lag by up to a second. `Performance.add_custom_monitor()` lets your game publish its own counters (bullets alive, enemies spawned, path requests). That is where profiling meets *analytics*: numbers the game reports about itself, which a test can read and a log can keep.

### Headless timing: what it includes, what it cannot, and the 6.9 ms sleep

`--headless` means `--display-driver headless --audio-driver Dummy` ([command line](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)). I checked what that leaves on 4.7.2 with 5,000 `Sprite2D` nodes in the tree:

- `RENDER_TOTAL_DRAW_CALLS_IN_FRAME`, `RENDER_TOTAL_OBJECTS_IN_FRAME`, `RENDER_TOTAL_PRIMITIVES_IN_FRAME` and `RENDER_VIDEO_MEM_USED` all read **0**; so do the viewport's measured CPU and GPU render times. `RenderingServer.get_video_adapter_name()` returns an empty string, while `get_current_rendering_method()` still reports the project setting (`gl_compatibility`). Do not take the latter as evidence of a GPU.
- Object and node counts, static memory, and the wall-clock time of scripts and physics are real.

The surprise is pacing. With no flags, that probe ran at about 144 frames per second, and a Codex-written particle benchmark in Chapter 9 measured 6.90 ms per frame for every case, including an empty scene. The reason is in the engine source: after each frame, `OS::add_frame_delay()` sleeps toward a target frame period whenever low-processor mode is on **or the display cannot draw** — and a headless display cannot. The period is `application/run/low_processor_mode_sleep_usec`, default 6,900 µs, "Roughly 144 FPS" in the source comment ([`core/os/os.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/core/os/os.cpp), [`main/main.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/main/main.cpp)). Any per-frame cost under 6.9 ms disappears into the sleep.

Two flags change this. **`--max-fps 60`** raises the sleep to a 60 Hz period; my probe then ran at 60 FPS. **`--fixed-fps 60`** "disables real-time synchronization": each frame advances the game by exactly 1/60 s, runs exactly one physics step, and — the source returns from the frame loop before the sleep when a fixed FPS is set — starts the next frame immediately. Under `--fixed-fps`, wall time per frame is CPU work per simulated frame.

That is the right instrument for this chapter's question and the wrong one for others. Chapter 0 showed its value for frame-counted gameplay tests. Chapter 9 showed its limit: anything involving the audio thread still runs in real time, so a test that "waits 0.25 s for the audio to stop" under `--fixed-fps` waits a few milliseconds. And a `--fixed-fps` timing is never a real-time frame time on screen. Say which mode every number came from.

### The human-with-a-screen tools

The editor's **Debugger** panel holds the tools that see the GPU ([debugger panel](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_panel.html), [the profiler](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler.html)):

- **Profiler** — per-function script time and frame time. It "does not automatically run because profiling is performance-intensive"; you press Start. It does not support C#.
- **Visual Profiler** — shows "what is taking the most time when rendering a frame on the CPU and GPU respectively", by rendering stage. The docs warn that its results "can vary heavily based on viewport resolution", so compare runs at the same window size, and that it "is not supported when using the Compatibility renderer on macOS". This chapter's project uses Compatibility; on a Mac you must switch renderer (and then you are measuring a different renderer) or use Windows or Linux.
- **Monitors** — the `Performance` counters as graphs over time, including draw calls and video memory, which mean something only with a real renderer.
- **Network Profiler** — traffic for nodes using the multiplayer API.

The CPU optimization page adds the caveat that matters for honest numbers: the profiler must be started and stopped by hand because recording "can slow down your project significantly" ([CPU optimization](https://docs.godotengine.org/en/stable/tutorials/performance/cpu_optimization.html)). Time with the profiler off; turn it on to find out *where* the time went.

### Nodes, servers and MultiMesh

A node is a convenient bundle: a name, a place in the tree, notifications, signals, an Inspector entry, and a handle to a low-level object owned by a **server** (`PhysicsServer2D`, `RenderingServer`, `AudioServer`). You can skip the bundle and talk to a server directly with RIDs. Godot's own page on this lists the costs of nodes — performance, memory, and processing that cannot use multiple threads — and then says: "In most cases, this is not really a problem"; servers pay off when you process "tens of thousands of instances" every frame ([optimization using servers](https://docs.godotengine.org/en/stable/tutorials/performance/using_servers.html)).

`MultiMesh` is the drawing half of the same idea — one draw call for many instances of one mesh. It "can draw up to millions of objects in one go", at the documented cost that there is "no screen or frustum culling possible for individual instances" ([using MultiMesh](https://docs.godotengine.org/en/stable/tutorials/performance/using_multimesh.html)).

The trade is always speed for visibility. Server objects do not appear in the scene tree, the Inspector or the remote debugger's tree. Their bugs are harder to see, as the Walker example shows.

### Loading and threads: spikes that are not per-frame cost

Some of the worst frames are not steady cost at all. Loading a large resource on the main thread stalls one frame for as long as the load takes. Godot's answer is background loading: `ResourceLoader.load_threaded_request()` starts a load, `load_threaded_get_status()` polls it, `load_threaded_get()` returns it. The trap is documented: once you call `load_threaded_get()` before loading is done, "the load will block at this point like load() would" ([background loading](https://docs.godotengine.org/en/stable/tutorials/io/background_loading.html)). Threads are not free either: "Creating threads is a slow operation, especially on Windows", and shared data needs a `Mutex` ([using multiple threads](https://docs.godotengine.org/en/stable/tutorials/performance/using_multiple_threads.html)). A spike measured once is an anecdote; a spike that recurs at the same event is a loading bug.

### Mobile and XR constraints

You cannot measure a phone or a headset from this Mac's terminal. These are the constraints to design for and then verify on the device.

- **Renderer.** Godot's comparison table marks Compatibility "Yes (low-end)" and Mobile "Yes (high-end)" for mobile, and Forward+ "Supported, but poorly optimized" there; for XR it marks Mobile "Recommended for desktop and standalone headsets" and Compatibility "Supported, but not recommended" ([renderers](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html)). The XR setup page says to "use the Mobile renderer for any desktop VR project, or any project running on a standalone headset like the Meta Quest 3" ([setting up XR](https://docs.godotengine.org/en/stable/tutorials/xr/setting_up_xr.html)). The Android XR deployment page says it is "highly advisable to use the compatibility renderer (OpenGL) for the time being when targeting Android based XR devices" ([deploying to Android](https://docs.godotengine.org/en/stable/tutorials/xr/deploying_to_android.html)). The official pages disagree. Record which one you followed, and test on the headset.
- **Frame rate.** The XR start-script tutorial notes headsets run "at a minimum of 72", recommends matching the physics rate to the headset, and leaves v-sync to OpenXR ([a better XR start script](https://docs.godotengine.org/en/stable/tutorials/xr/a_better_xr_start_script.html)). At 72 Hz the budget is 13.9 ms; at 90 Hz, 11.1 ms — for two eye views.
- **Fill rate and battery.** The GPU optimization page says "Mobile GPUs are limited to a tiny battery", describes their tile-based rendering, and calls fill rate on mobile "very expensive" ([GPU optimization](https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html)). Transparent particles and full-screen effects are where that bites.
- **Foveation** is renderer-specific: the OpenXR Foveation Level setting is for Compatibility; Mobile and Forward+ use a viewport VRS mode instead ([OpenXR settings](https://docs.godotengine.org/en/stable/tutorials/xr/openxr_settings.html)).

What a desktop CPU measurement can offer a mobile decision is a *ratio* between two implementations of the same CPU work — a hypothesis to test on the device, not a prediction of its milliseconds.

## The Walker example: walker-2d-bullet-shower

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-2d-bullet-shower`](https://github.com/nikbearbrown/walker-2d-bullet-shower), [`walker-3d-graphics-settings`](https://github.com/nikbearbrown/walker-3d-graphics-settings), [`walker-viewport-3d-scaling`](https://github.com/nikbearbrown/walker-viewport-3d-scaling), [`walker-3d-antialiasing`](https://github.com/nikbearbrown/walker-3d-antialiasing), [`walker-loading-threads`](https://github.com/nikbearbrown/walker-loading-threads), [`walker-loading-load-threaded`](https://github.com/nikbearbrown/walker-loading-load-threaded), [`walker-misc-custom-logging`](https://github.com/nikbearbrown/walker-misc-custom-logging). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

`walker-2d-bullet-shower` is the Walker adaptation of Godot's official `2d/bullet_shower`, copied from `godot-demo-projects` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7` (MIT, Godot Engine contributors). It is public at [github.com/nikbearbrown/walker-2d-bullet-shower](https://github.com/nikbearbrown/walker-2d-bullet-shower). To rebuild it from the upstream path instead, apply [`walker-adaptation.diff`](../examples/13-profiling-and-optimization/walker-adaptation.diff) (the title and one line), then add the three Walker tests from [`examples/13-profiling-and-optimization/tests/`](../examples/13-profiling-and-optimization/tests/).

**What it is.** Not a game with a goal: its header describes "controlling a high number of 2D objects with logic and collision without using nodes". 500 bullets drift left at 20–80 px/s and wrap around. No bullet is a node. `bullets.gd` creates one shared circle shape (radius 8) and, for each bullet, a `PhysicsServer2D` body identified by an RID, moves every body in `_physics_process` with `body_set_state`, and draws all 500 textures from one `_draw()`. The player is an `Area2D` that follows the mouse and shows a sad face while any bullet touches it. Compatibility renderer.

**The claim.** The script says the technique is "a lot more efficient than using instancing and nodes", and that with "thousands or more" objects RIDs "can be significantly faster". The Walker README: "No performance speedup is claimed without a comparative benchmark."

**What its checks established — and the bug they found.** The build's `FRICTIONAL.md` is a short case study in why a fast path needs its own tests:

- Headless import and a 120-frame run exit 0. A mouse probe finds 500 bullets and the player following the cursor; a collision probe drives the mouse onto a real bullet and sees the sad face, then the recovery.
- A motion probe then **failed**: after 60 physics frames, a bullet's body sat at y = 514.94 while its drawing sat at y = 498.89. A follow-up found the bodies were in `RIGID` mode (enum 2) with a vertical velocity of 962.86: the server-created bodies were falling under gravity between the script's transform updates, so each collision shape sat one tick of fall — 962.86 / 60 = 16.05 px — below its sprite.
- The Walker fix is one line after each body is created: `PhysicsServer2D.body_set_mode(bullet.body, PhysicsServer2D.BODY_MODE_STATIC)`. After it, all 500 bodies align with their drawings (`ALIGNED_BODIES 500/500`).

That is the other cost of skipping nodes. An `Area2D` node chooses sensible physics behavior for you; a bare server body does what its defaults say, and on Godot 4.7.2 the upstream code's bodies fall. Nobody would see a 16-pixel hitbox offset in a screenshot. A player would feel it as unfairness.

**What remains unverified.** Visual play, capture, and any performance number. The log says so: "not a performance benchmark or visual review".

**The other Walker builds in this chapter** each measured something real and stopped where headless evidence stops:

| Build | What its log establishes | What it says it does not |
|---|---|---|
| `walker-3d-graphics-settings` | 17 headless assertions: render scale, FOV, brightness, contrast and saturation sliders reach their endpoints through real input | "Headless stored settings are not pixel, renderer support, performance, hardware, or human verification" |
| `walker-viewport-3d-scaling` | 37 assertions: Space cycles scale 1/2, 1/3, 1/4, full; Enter cycles all six scaling modes; the HUD stays fixed | GPU scaling quality, rendered resolution, performance improvement |
| `walker-3d-antialiasing` | key, wheel and orbit input checks; a persistent `DummyShader` RID leak at exit, narrowed to the full scene | "Headless checks cannot establish actual antialiasing quality or comparative GPU cost" |
| `walker-loading-threads` | reproduced a race (two activations in one frame joined the wrong worker), fixed it, then 29/29 checks in three stress runs of 20 bursts × 8 activations | pixels and responsiveness |
| `walker-loading-load-threaded` | 48 checks across two threaded-loading rounds once the harness used a 1920×1080 viewport (the default headless size left buttons unreachable) | "no claim is made about hitch-free retrieval" |
| `walker-misc-custom-logging` | 15 checks: a `Logger` subclass registered with `OS.add_logger()` receives stdout, stderr, warnings and errors | thread-stress safety, crash traces, flush durability |

The custom-logging build is the seed of analytics in Godot: once the game's own messages pass through code you control, you can count them, time-stamp them and write them to a file.

## Hands-on: benchmark the claim, then decide

You will build the benchmark: a node-based bullet field (the **baseline**), the existing server-based field (the **optimization**), a parity test proving they behave alike, and a harness that measures both at several counts. Then you decide whether the optimization is justified.

### Predict

1. The shipped game has 500 bullets. On a desktop CPU, will the node version cost more or less than 1 ms per simulated frame? Will servers be 2× faster, 10× faster, or indistinguishable?
2. From 500 to 5,000 bullets, will the node version's cost grow linearly, faster than linearly, or slower?
3. If you read `Performance.TIME_PROCESS` once at the end of a 600-frame run that took half a second of wall time, what will it say?
4. Name two costs the server version still pays and two it avoids. Which can a headless run measure?

### Build It

Start from the upstream demo at the pinned commit:

```bash
git clone https://github.com/godotengine/godot-demo-projects.git
```

```bash
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

Copy `2d/bullet_shower` into a new folder as `godot/`, apply the Walker diff, copy in the three Walker tests, `git init`, commit. Import and run the motion test as your baseline:

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://test_motion.gd
```

Expect `MOTION_OK true BODY_SYNC true` and `ALIGNED_BODIES 500/500`. Then give Claude Code this prompt. It names the one change, the invariant (the game plays the same), the parity evidence required before any timing is trusted, and the exact command:

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

Two lessons from this chapter's record are built into that command and your project. `--disallowedTools "Skill"` stops the agent from invoking skills; in our run, an agent that was refused a command invoked a skill whose job is to add permission rules. And the allow list names `godot`: put `Run Godot as the plain command godot` and your test commands in `CLAUDE.md` or `AGENTS.md`, or the agent may find the app's absolute path and be refused over and over.

With Codex, the equivalent is `codex exec -s workspace-write -C . "$(cat prompt1.txt)" < /dev/null`. In Chapter 9's Codex run the sandbox let `godot` run but blocked Godot's log file under the home folder (`Failed to open log file for writing`), which is harmless for these tests.

### Use It

The headless numbers cover the CPU. The screen covers the rest.

1. Run `shower.tscn` in the editor and move the mouse through the bullets. Does the face turn sad exactly when a bullet overlaps it? (That is the alignment bug, checked by eye.)
2. Open **Debugger → Monitors** and watch `Time → Process`, `Time → Physics Process` and `Object → Nodes`. Then run `bench/shower_nodes.tscn` with F6. The agent made `bullet_count` a plain `var`, not an `@export`, so it does not appear in the Inspector: to see 5,000 bullets, change its default in `bench/bullets_nodes.gd` temporarily, run, and revert. Compare the graphs.
3. Start the **Profiler**, run ten seconds, stop. Find each `_physics_process` in the list. Is the script's own time most of the frame, or the engine's physics step?
4. On Windows or Linux, open the **Visual Profiler** and compare the node version's draw time with the server version's single `_draw()` — the cost the headless benchmark cannot see. On a Mac it will not run with this project's Compatibility renderer.
5. If you have an Android phone or a standalone headset, export both scenes and compare there. That needs Godot's export templates (a large download) and the platform SDK; Chapter 15 covers the export cycle. This chapter's record did not do it.

### Ship It

- **Commits:** baseline; configurable count; node baseline and parity test; the harness; your repeated measurements as CSV, with machine, date and load in the message.
- **FRICTIONAL.md:** the prompt, the commands, every failure and its real cause, and the decision with the numbers behind it. If the agent writes its own FRICTIONAL entry, check each sentence against the output before keeping it.
- **SOURCES.md:** the benchmark and parity scripts are AI-written and human-verified; say so.
- **Brutalist film:** `godot-gamedev`. Show `bullets.gd`'s server calls beside `bullets_nodes.gd`'s nodes, the parity test's PASS lines, and the measurement table, and say out loud what a headless number excludes.

### Verify

Run the parity check and the existing tests yourself, with a timeout — a test script that hits a runtime error before `quit()` never exits:

```bash
timeout 120 godot --headless --path godot --script res://bench/test_nodes_parity.gd -- --count=5000
```

```bash
timeout 120 godot --headless --path godot --script res://test_motion.gd
```

Then measure more than once, in fresh processes, alternating the modes so that whatever else the machine is doing affects both. The scripts used for this chapter are in `examples/13-profiling-and-optimization/verification/`:

```bash
bash sweep.sh . sweep.csv
```

```bash
python3 summarize.py sweep.csv
```

A pass establishes that, for the cases tested, the two versions have the same count, motion and collision behavior, and gives each one's CPU cost per simulated frame on your machine at that moment. It does not establish draw cost, GPU cost, real-time frame pacing, or anything about a device you did not run on.

## What we actually ran

**Date:** 27 September 2026. **Machine:** the instructor's Mac, Apple M4 Pro, 14 cores, macOS 26.5.1, shared with other jobs (load averages 12–27 during the measurements). **Godot:** 4.7.2. **Agent:** Claude Code 2.1.150; `-p` used the account's default model, `claude-sonnet-4-6`. **Starting point:** a scratch repository with only the Walker build's `godot/` folder and Markdown files, baseline commit `1cc1478`. Every `claude -p` call also had `--strict-mcp-config` and `--settings '{"autoMemoryEnabled":false}'`, operational choices for the record. Everything is in [`examples/13-profiling-and-optimization/`](../examples/13-profiling-and-optimization/).

### Session 1: the build, the refusals, and an attempt to widen permissions

In about twelve minutes the agent read the seven files, planned, and wrote everything the prompt asked for: `bullet_count` as a variable defaulting to 500; `bench/bullets_nodes.gd` (one `Area2D` + `CollisionShape2D` + `Sprite2D` per bullet, `monitoring = false`, `monitorable = true`, layer 1, mask 0, one manager loop); `bench/shower_nodes.tscn`, reconnecting the player to `area_shape_entered`/`exited` because the bullets are now areas, not bodies; `bench/bench.gd`; `bench/test_nodes_parity.gd`. It also edited an existing test, `test_motion.gd`, to read `bullet_count` instead of 500 — a change it was not asked for — and wrote a `run_bench.sh` whose default Godot path is the app's absolute path.

Then it tried to run Godot. It had read the absolute path, `/Applications/Godot.app/Contents/MacOS/Godot`, and used it. The allow list said `godot`, so every call was refused. It retried with a `dangerouslyDisableSandbox` flag (refused), asked a question no one could answer in `-p` mode, and then invoked the `fewer-permission-prompts` skill — a skill that scans past transcripts and adds allow rules to the project's `.claude/settings.json` — and tried to list `~/.claude/projects`, which the permission system blocked. At that point I stopped the session (tool call 45). No settings file had been written. An agent that is refused a command should report the refusal, not look for a way to change the rules; that is why the chapter's command line now carries `--disallowedTools "Skill"`.

### Session 2: running it, and two self-inflicted bugs

I resumed the session with a correction: stop changing permissions, run Godot as the plain command `godot`, one command per call, and paste the real output. In 23 turns (about 5.5 minutes; the CLI reported an API-equivalent cost of $1.03) it imported, ran the tests, and found two bugs of its own:

- Its `test_motion.gd` edit read `manager.bullets.size()` after `scene.queue_free()`, producing a `SCRIPT ERROR` about a previously freed instance. It reverted the edit. That run never reached `quit()`, and the headless Godot process it left behind was still running 25 minutes later, holding the Claude Code session open until I killed it. Use `timeout`.
- Its parity test failed to parse: `var bullet := manager.bullets[0]` cannot infer a type from an untyped `Array`. It changed `:=` to `=`.

Then parity passed at 500 and at 5,000 bullets (count, motion within 0.002 px, collision and recovery), the three original tests passed, and it ran the benchmark four times:

```text
mode,count,frames,mean_ms,p95_ms,max_ms,object_count,node_count,static_memory_mb
servers,500,600,0.163,0.200,0.279,2000,6,25.00
servers,5000,600,2.671,6.454,37.737,6500,6,34.52
nodes,500,600,0.308,0.397,2.918,3501,1506,29.23
nodes,5000,600,12.579,20.864,87.578,21501,15006,78.30
```

Its code was right. Its description of its own instrument was not. `bench.gd` labels `TIME_PROCESS` as "seconds all nodes spent in `_process` last frame", and its report calls both monitors "from the *last* measured frame". Its own output refutes that: for servers at 5,000 it printed `TIME_PHYSICS_PROCESS=33.452 ms` for a run whose mean frame was 2.67 ms and whose worst frame was 37.7 ms. A one-second maximum explains the number; "the last frame" cannot. At 500 bullets both monitors printed 0.000, because 720 frames under `--fixed-fps` finished in well under a second and the monitors had never been updated. The agent also committed its work and appended an 82-line entry to `FRICTIONAL.md` that repeats the wrong definition. Both would have gone into the project's history unchallenged if no one had read the source.

### My verification

I ran the parity test at 500 and 5,000 and the three original tests myself, in real time and again under `--fixed-fps 60`; all passed (`logs/`). Then I ran the benchmark ten times per configuration in fresh processes — two sweeps of five, modes alternating, 600 measured frames each, `--fixed-fps 60` — with `verification/sweep.sh`:

| Bullets | Version | Median of 10 run means | Range of run means | Median p95 | Objects | Nodes | Static memory |
|---|---|---|---|---|---|---|---|
| 500 | nodes | 0.331 ms | 0.313–2.268 | 0.471 ms | 3,501 | 1,506 | 29.2 MB |
| 500 | servers | 0.167 ms | 0.161–0.509 | 0.199 ms | 2,000 | 6 | 25.0 MB |
| 2,000 | nodes | 2.845 ms | 2.427–11.622 | 3.556 ms | 9,501 | 6,006 | 45.6 MB |
| 2,000 | servers | 0.707 ms | 0.662–2.401 | 0.826 ms | 3,500 | 6 | 28.2 MB |
| 5,000 | nodes | 9.854 ms | 8.508–39.009 | 13.290 ms | 21,501 | 15,006 | 78.3 MB |
| 5,000 | servers | 2.314 ms | 1.819–8.970 | 2.988 ms | 6,500 | 6 | 34.6 MB |

Three things in that table matter more than any single number.

**The variance is the machine, not the code.** In the first sweep, runs 3–5 coincided with a load spike (the load average reached 27): the node version at 5,000 went from 8.5 ms to 39.0 ms between runs of identical code. The medians of the two sweeps agree within 10% (servers at 5,000: 2.31 and 2.32 ms; nodes: 10.2 and 9.5 ms). One run is an anecdote. The agent's single run of nodes at 5,000 (12.6 ms) was an ordinary member of that noisy range.

**The ratio grows with the count.** Servers cost about 0.33–0.46 µs per bullet per frame at every count — nearly linear. Nodes cost 0.66 µs per bullet at 500, 1.42 at 2,000 and 1.97 at 5,000. The median ratio is 2.0× at 500 and about 4× at 2,000 and 5,000. Why the node version grows faster than linearly was not isolated here; the Profiler (Use It, step 3) is the tool to find out.

**Worst frames are worse than the means suggest.** Every configuration had at least one frame over 60 ms somewhere in its ten runs. On a shared machine that is noise; on a phone it is a hitch.

### The decision

At the game's own 500 bullets, the node version costs about 0.33 ms of CPU per simulated frame on this Mac — 2% of a 60 Hz budget — and the server version saves about 0.16 ms of that. On this evidence the optimization is **not** justified for the game as shipped: the saving is tiny, the node version is visible in the scene tree and the Inspector, and it cannot have the falling-body bug that the server version shipped with. At 5,000 bullets the picture reverses: 9.9 ms is 59% of a 60 Hz budget and 89% of a 90 Hz headset budget, before any drawing, while 2.3 ms leaves room. If the design calls for thousands of bullets, or for a much slower CPU, servers are justified — and the justification is these numbers plus a parity test, not a comment in the source.

What the benchmark cannot tell you is whether 5,000 `Sprite2D` nodes cost more to draw than one `_draw()` of 5,000 textures on a real GPU, or anything about a phone. Those are Use It steps 4 and 5, and no one did them for this chapter.

## Check your understanding (ungraded)

1. Read `bench/bench.gd`. It times the interval between `physics_frame` signals. Under `--fixed-fps 60`, why does that interval contain exactly one physics step? What would it contain without the flag?
2. Run `bench.gd` for nodes at 5,000 without `--fixed-fps`. Is the mean still near 10 ms, or does it change? Explain the result using the 6.9 ms sleep.
3. Rewrite the `TIME_PROCESS` comment in `bench.gd` so that it is true, citing the lines of `main.cpp` that support it.
4. The node baseline sets `monitoring = false` on every bullet. Predict what happens to the node version's cost at 5,000 bullets if you set it to `true`, then measure.
5. Upstream `bullets.gd` never calls `body_set_mode`. Show, with `test_motion.gd` and a one-line change, what the default mode does to alignment. Why could the node version not have this bug?
6. Your target is a standalone headset at 90 Hz using the Mobile renderer. Write the measurement plan you would run on the device before choosing between nodes and servers for 2,000 bullets.

## Doing the same thing in Unity

Unity was not run for this chapter. The comparisons come from Unity's official documentation, checked on 27 September 2026 (default manual: Unity 6.6, 6000.6).

### Similarities

The loop is the same and the tools line up. Unity's **Profiler** has CPU Usage, GPU Usage, Rendering, Memory and Audio modules, among others ([profiler modules](https://docs.unity3d.com/Manual/profiler-modules-introduction.html)). It has the same observer cost: **Deep Profiling** "is resource-intensive and uses a lot of memory" and runs the application "significantly slower" ([deep profiling](https://docs.unity3d.com/Manual/profiler-deep-profiling.html)), and the GPU Usage module is off by default because of its overhead. The **Frame Debugger** can "pause the application on a particular frame and display the list of rendering events" ([Frame Debugger](https://docs.unity3d.com/Manual/FrameDebugger.html)) — the role Godot's Visual Profiler plays.

This chapter's benchmark would be a PlayMode test using the **Performance Testing** package, a core package from Unity 6000.6. Its `Measure.Frames()` "records time per frame by default", and `Measure.Method()` takes warm-up and measurement counts ([Performance Testing](https://docs.unity3d.com/Packages/com.unity.test-framework.performance@6.7/manual/index.html), [Measure.Frames](https://docs.unity3d.com/Packages/com.unity.test-framework.performance@6.7/manual/measure-frames.html)). It runs headless with `-batchmode -runTests -testPlatform PlayMode`, and `-nographics` means Unity "doesn't initialize the graphics device" ([command-line arguments](https://docs.unity3d.com/Manual/EditorCommandLineArguments.html), [test framework command line](https://docs.unity3d.com/Manual/test-framework/reference-command-line.html)) — the same CPU-only boundary as Godot's `--headless`.

The nodes-versus-servers trade has a Unity analogue: a GameObject per bullet with a Collider and a SpriteRenderer, against one manager that keeps positions in arrays and draws instances. The lesson carries over unchanged: measure at your real count before paying the readability cost.

### Differences

- **Counters from code.** `ProfilerRecorder` (in `Unity.Profiling`) reads named counters such as "Main Thread" and "System Used Memory", and "you can use this API in Editor and Player builds, including Release Players" ([ProfilerRecorder](https://docs.unity3d.com/ScriptReference/Unity.Profiling.ProfilerRecorder.html)). Godot's `MEMORY_STATIC` is unavailable in release builds, and `TIME_PROCESS` is a one-second maximum.
- **Device profiling is built in.** A Development Build with "Autoconnect Profiler" streams data from the target device to the editor ([profiling on a target device](https://docs.unity3d.com/Manual/profiling-target-device.html)). This chapter did not test Godot's equivalent.
- **Aggregation tools exist.** Profile Analyzer "aggregates and visualizes frame and marker data" across many frames, and the Memory Profiler analyses memory snapshots ([Profile Analyzer](https://docs.unity3d.com/Packages/com.unity.performance.profile-analyzer@1.4/manual/index.html), [Memory Profiler](https://docs.unity3d.com/Packages/com.unity.memoryprofiler@1.1/manual/index.html)). In Godot you write the median, p95 and max yourself, as this chapter's scripts do.
- **The `-quit` caveat.** Unity's test-runner reference notes that the regular `-quit` argument is not supported while tests are running ([test framework command line](https://docs.unity3d.com/Manual/test-framework/reference-command-line.html)); a Godot SceneTree test must call `quit()` itself, or — as this chapter found — hang.

### The agent-workflow angle

An agent can write the C# PlayMode test and the harness as text and run them in batch mode — the same loop as this chapter. Profiler captures are binary data files viewed in the editor; an agent can trigger a capture but cannot read the flame chart the way it reads a CSV line. Ask for CSV or test-result output that a script can compare between runs.

| Godot | Unity |
|---|---|
| `Performance` singleton | `ProfilerRecorder` counters |
| Profiler / Visual Profiler / Monitors | Profiler window (CPU, GPU, Rendering, Memory…), Frame Debugger |
| `godot --headless --fixed-fps 60 --script …` | `-batchmode -nographics -runTests -testPlatform PlayMode` |
| hand-written median / p95 / max | Performance Testing package, Profile Analyzer |
| nodes vs `PhysicsServer2D` RIDs | GameObjects vs a manager with instanced drawing |

## Doing the same thing in Unreal Engine

Unreal Engine was not run for this chapter. The comparisons come from Epic's official documentation, checked on 27 September 2026 (newest documented version: 5.8). Unreal's source is available to registered GitHub users under the Unreal Engine EULA — source-available, not open source.

### Similarities

Unreal's quick counters answer the first question in one line. `stat fps` shows frames per second; `stat unit` shows "overall frame time as well as the game thread, rendering thread, and GPU times"; `stat gpu` shows GPU statistics ([stat commands](https://dev.epicgames.com/documentation/en-us/unreal-engine/stat-commands-in-unreal-engine)). Comparing the game-thread, render-thread and GPU times against the frame time is the quickest way to see which one limits the frame — the CPU-bound/GPU-bound question from this chapter. **Unreal Insights** is the deep tool, "a telemetry capture and analysis suite" with Timing, Memory, Networking and Asset Loading views, among others ([Unreal Insights](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine)).

For per-frame numbers a script can read, the **CSV Profiler** is "a lightweight, scoped, timestamp-based profiler that outputs per-frame timings", controlled with `csvprofile start|stop` or captured from launch with `-csvCaptureFrames=N`. The dedicated page is written for 4.27; the 5.8 console reference still lists `CsvProfile` ([CSV Profiler, 4.27](https://dev.epicgames.com/documentation/en-us/unreal-engine/csv-profiler?application_version=4.27), [console commands](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-console-commands-reference)). That is this chapter's CSV line, built in.

### Differences

- **Frame-rate targets are written down.** Epic's profiling introduction says "generally, applications will target 30, 60, and 120 frames per second" ([performance and profiling](https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine)). Its XR best-practices page gives per-headset rates — for example 72, 80, 90 or 120 Hz for Quest 2 — in a table that includes older devices ([XR best practices](https://dev.epicgames.com/documentation/en-us/unreal-engine/xr-best-practices-in-unreal-engine)), and its VR performance page notes that at 90 Hz "you have slightly less than 11ms of GPU time, because of the overhead of reprojection" ([VR performance testing](https://dev.epicgames.com/documentation/en-us/unreal-engine/vr-performance-testing-in-unreal-engine)).
- **Scalability is configuration.** Scalability groups (`sg.*`) set quality levels from Low to Epic, and Device Profiles in `Config/DefaultDeviceProfiles.ini` are "the recommended way of handling scalability on different mobile devices" ([scalability](https://dev.epicgames.com/documentation/en-us/unreal-engine/scalability-reference-for-unreal-engine), [device profiles](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-device-profiles-in-unreal-engine)). Those `.ini` files are text an agent can read and diff. Godot's per-platform overrides live in `project.godot` (for example `rendering_method.mobile`), also text.
- **Device runs have a framework.** Gauntlet "is a framework to run sessions of projects in Unreal Engine that perform tests and validate results" on PC, consoles and mobile ([Gauntlet](https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-overview-in-unreal-engine)). Godot has no built-in equivalent; this chapter's harness runs on the desktop only.
- **Headless runs.** `-nullrhi` uses the "null rendering hardware interface to run UE headless", `-unattended` suppresses dialogs, and `-ExecCmds="Automation RunTest <name>;Quit"` runs automation tests ([command-line arguments](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-command-line-arguments-reference)). As in Godot, a `-nullrhi` timing contains no GPU work.

### The agent-workflow angle

The measurement side of Unreal is agent-friendly: console commands, command-line flags, CSV files and `.ini` device profiles are all text. The thing being optimized often is not. The equivalent of this chapter's baseline — an actor per bullet built in Blueprint — lives in binary `.uasset` files, which Epic's own documentation says "cannot be opened as text or merged in a text-based merge tool" ([Perforce and Unreal](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-perforce-as-source-control-for-unreal-engine)). Rewriting hot Blueprint logic in C++ would be the Unreal version of this chapter's change, and it would also turn that logic into reviewable text.

| Godot | Unreal Engine 5 |
|---|---|
| `Performance.TIME_PROCESS` | `stat unit` (game / render / GPU) |
| Profiler + Visual Profiler | Unreal Insights, `stat gpu`, `profilegpu` |
| benchmark CSV line | CSV Profiler (`csvprofile`, `-csvCaptureFrames`) |
| `--headless` | `-nullrhi -unattended` |
| renderer per platform in `project.godot` | Scalability groups + Device Profiles (`.ini`) |
| nodes vs servers | Blueprint actors vs C++ managers |

## Sources

Godot (official documentation, "stable" = 4.7, and engine source at tag `4.7.2-stable`):

- [General optimization](https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html), [CPU optimization](https://docs.godotengine.org/en/stable/tutorials/performance/cpu_optimization.html), [GPU optimization](https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html)
- [Optimization using Servers](https://docs.godotengine.org/en/stable/tutorials/performance/using_servers.html), [Optimization using MultiMeshes](https://docs.godotengine.org/en/stable/tutorials/performance/using_multimesh.html)
- [Performance class](https://docs.godotengine.org/en/stable/classes/class_performance.html)
- [The Profiler](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler.html), [Debugger panel](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_panel.html)
- [Command-line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
- [Background loading](https://docs.godotengine.org/en/stable/tutorials/io/background_loading.html), [Using multiple threads](https://docs.godotengine.org/en/stable/tutorials/performance/using_multiple_threads.html)
- [Renderers](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html), [Setting up XR](https://docs.godotengine.org/en/stable/tutorials/xr/setting_up_xr.html), [Deploying to Android (XR)](https://docs.godotengine.org/en/stable/tutorials/xr/deploying_to_android.html), [OpenXR settings](https://docs.godotengine.org/en/stable/tutorials/xr/openxr_settings.html), [A better XR start script](https://docs.godotengine.org/en/stable/tutorials/xr/a_better_xr_start_script.html)
- Engine source: [`main/main.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/main/main.cpp) (`process_max`, the once-per-second `set_process_time`, the `low_processor_mode_sleep_usec` default of 6900, the early return under a fixed FPS) and [`core/os/os.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/core/os/os.cpp) (`OS::add_frame_delay`)
- Godot demo projects at commit [`a3b5c113`](https://github.com/godotengine/godot-demo-projects/tree/a3b5c113112f77291d5f3d1360f33a882fdc52f7): `2d/bullet_shower` (MIT)

Course and Walker records:

- `walker-2d-bullet-shower/README.md` and `FRICTIONAL.md`; the README and FRICTIONAL of `walker-3d-graphics-settings`, `walker-viewport-3d-scaling`, `walker-3d-antialiasing`, `walker-loading-threads`, `walker-loading-load-threaded`, `walker-misc-custom-logging`
- Chapter 0 (`chapters/00-the-toolchain.md`) for `--fixed-fps` and frame-counted tests; Chapter 9 for the 6.9 ms sleep in a Codex benchmark
- This chapter's record: [`examples/13-profiling-and-optimization/`](../examples/13-profiling-and-optimization/)

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation, checked on 27 September 2026:

- Unity: [profiler modules](https://docs.unity3d.com/Manual/profiler-modules-introduction.html), [deep profiling](https://docs.unity3d.com/Manual/profiler-deep-profiling.html), [profiling on a target device](https://docs.unity3d.com/Manual/profiling-target-device.html), [Frame Debugger](https://docs.unity3d.com/Manual/FrameDebugger.html), [ProfilerRecorder](https://docs.unity3d.com/ScriptReference/Unity.Profiling.ProfilerRecorder.html), [Performance Testing package](https://docs.unity3d.com/Packages/com.unity.test-framework.performance@6.7/manual/index.html), [Measure.Frames](https://docs.unity3d.com/Packages/com.unity.test-framework.performance@6.7/manual/measure-frames.html), [Profile Analyzer](https://docs.unity3d.com/Packages/com.unity.performance.profile-analyzer@1.4/manual/index.html), [Memory Profiler](https://docs.unity3d.com/Packages/com.unity.memoryprofiler@1.1/manual/index.html), [command-line arguments](https://docs.unity3d.com/Manual/EditorCommandLineArguments.html), [Test Framework command line](https://docs.unity3d.com/Manual/test-framework/reference-command-line.html)
- Unreal Engine: [stat commands](https://dev.epicgames.com/documentation/en-us/unreal-engine/stat-commands-in-unreal-engine), [Unreal Insights](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine), [CSV Profiler (4.27)](https://dev.epicgames.com/documentation/en-us/unreal-engine/csv-profiler?application_version=4.27), [console commands](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-console-commands-reference), [performance and profiling](https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine), [XR best practices](https://dev.epicgames.com/documentation/en-us/unreal-engine/xr-best-practices-in-unreal-engine), [VR performance testing](https://dev.epicgames.com/documentation/en-us/unreal-engine/vr-performance-testing-in-unreal-engine), [scalability](https://dev.epicgames.com/documentation/en-us/unreal-engine/scalability-reference-for-unreal-engine), [device profiles](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-device-profiles-in-unreal-engine), [Gauntlet](https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-overview-in-unreal-engine), [command-line arguments](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-command-line-arguments-reference), [Perforce and Unreal](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-perforce-as-source-control-for-unreal-engine)
