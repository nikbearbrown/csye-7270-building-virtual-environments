# Module 9 — Particle effects

CSYE 7270 · Fall 2026 · Week 9

## Executive summary

A particle effect is a small simulation: many short-lived points are born, move, change and die, and the engine draws each one. This module takes Godot 4.7.2's particle system apart (what each node owns, how the emission cycle is timed, where the cost lands) and has you build one effect and price another. You direct Claude Code to add a one-shot death burst to the Dodge the Creeps game and check it with a headless test, a test run with no window. Then you direct Codex to measure what particle simulation costs the CPU. The run recorded on 27 September 2026 ended at 9 of 9 headless checks, with CPU particles costing 0.035 ms per frame at 1,000 particles and 1.61 ms at 50,000, and it holds three agent mistakes and two documentation-level defects worth learning from. None of it proves the burst looks like anything, or what it costs a GPU: headless Godot draws nothing, so those judgments are yours. It prepares you for Assignment 7, two particle effects, tuned and priced.

## The question

The player dies. Something should burst where they stood. A headless test prints `PASS emitting after hit`.

Is there a burst?

Not necessarily. The effect could be a child of a node that was just hidden. Each particle could be one pixel wide. Half of its velocity could point along a Z axis that a 2D camera never shows. And if it does look right, you still do not know whether it costs a tenth of a millisecond or four milliseconds per frame on the phone you will ship to, because a headless measurement will report that it costs almost nothing.

The question: how do you separate **visual intent** (what the effect should look like), **state** (what the engine says it is doing) and **measured cost** (what it takes from the frame), and which of the three can an agent, a test and a human each establish?

## The ideas

### A loop with three parts

William Reeves named the technique in 1983. His paper describes a fuzzy object, such as fire, as a cloud of primitives that are generated into the system, move and change over time, and die from it ([Reeves 1983, SIGGRAPH history archive](https://history.siggraph.org/learning/particle-systems-a-technique-for-modeling-a-class-of-fuzzy-objects-by-reeves/)). Every engine still runs that loop; what differs is where it runs (CPU or GPU) and what you can observe without looking at the screen. In Godot, keep three parts separate, in your head and in your prompts.

| Part | What it decides | Where it lives |
|---|---|---|
| Emission | how many particles are born, when, and where | node properties: `amount`, `lifetime`, `explosiveness`, `one_shot`, `emitting` |
| Process | how each particle moves and changes over its life | the process material on GPU nodes; node properties on CPU nodes |
| Draw | what each particle looks like | the node's `texture` (2D) or draw-pass mesh (3D), plus an ordinary material |

An effect can be wrong in any part independently. A burst can fire at the right moment, spray into an invisible axis and use one-pixel particles. A headless test reaches only the first part, and only partly.

### Four nodes, two families

Godot ships `GPUParticles2D`, `GPUParticles3D`, `CPUParticles2D` and `CPUParticles3D`. The [2D particle manual](https://docs.godotengine.org/en/stable/tutorials/2d/particle_systems_2d.html) says the CPU node has near-feature parity with the GPU one but lower performance with large amounts; the [3D manual](https://docs.godotengine.org/en/stable/tutorials/3d/particles/index.html) says CPU particles suit older hardware and phones. That parity hides a hard edge, so the instructor asked the installed engine which properties each class has (`ClassDB.class_get_property_list`, Godot 4.7.2, headless).

| Property | GPU nodes | CPU nodes |
|---|---|---|
| `process_material` | yes | no; the same settings are node properties |
| `sub_emitter` | yes | no |
| `trail_enabled` | yes | no |
| `emission_shape` on the node | no, it is on the material | yes |
| `explosiveness`, `one_shot`, `preprocess`, `fixed_fps`, `local_coords` | yes | yes |

Sub-emitters, trails and particle shaders are GPU-node features. The renderer draws a second edge: the [renderer comparison](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html) lists particle trails and particle SDF collision as unsupported in Compatibility, which Dodge the Creeps uses. Its player already has a node named `Trail`; it is an ordinary `GPUParticles2D` stamping faded copies of the sprite, not the `trail_enabled` feature. Read the node, not its name.

### The timing model: one emission cycle

Most particle bugs are timing bugs, and the model is small ([GPUParticles2D reference](https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html)).

- `lifetime` is how long each particle lives, and also the length of one emission cycle.
- `amount` is the number of particles in one cycle. A looping emitter births about `amount / lifetime` per second. Changing `amount` restarts the system.
- `explosiveness` of 0 spreads births across the cycle; 1 emits them all at its start. A burst is `explosiveness = 1`.
- `one_shot` means only one cycle occurs. `preprocess` starts the system as if it had already run for that many seconds, which is how smoke is already rising when a level loads, and large values are expensive.
- `restart()` restarts the cycle and clears existing particles. The `finished` signal fires when all active particles are done, and never when `one_shot` is off.

One more fact came from an experiment, not the docs: particle time is frame time, not wall-clock time. A 0.5 s one-shot `CPUParticles2D` started on the first frame of a headless run finished after 442–450 ms of wall-clock time but 510–514 ms of summed frame deltas, in six runs of six. A stopwatch can disagree with the engine by that much.

### Defaults that bite in 2D

`ParticleProcessMaterial` is shared by 2D and 3D nodes, so its defaults are 3D: direction `(1, 0, 0)`, spread 45 degrees, gravity `(0, -9.8, 0)`, and `particle_flag_disable_z` false (checked on 4.7.2). In 3D a spread of 180 degrees is every direction. In a 2D game, the part of each velocity pointing into Z is motion no one can see, which is why the official 2D particles demo says to enable Disable Z. Set your own gravity; the game's `Trail` uses `(0, 0, 0)`.

The second trap is the texture. The class reference says that with a null `texture`, particles are 1×1-pixel squares. A burst with no texture is thirty-two specks on a 480×720 screen.

### Triggering an effect from gameplay

A particle node is a node: it inherits its parent's transform and visibility. With `local_coords` false (the default), living particles stay where they were born when the emitter moves. A hidden parent hides the effect, so a burst parented to a player who calls `hide()` at the moment of death can be `emitting` and invisible. `emitting == true` is not "the player saw it"; `is_visible_in_tree()` is a better state check, and your eyes are the real one. Effects can also start from an animation track: in `walker-3d-platformer`, the coin's `take` animation keys `CPUParticles3D:emitting` to true. If an agent cannot find where an effect starts, look in the animations.

### Beyond the checkboxes, and where the cost lands

A **sub-emitter** is a second GPU particle system that spawns from the first one's particles; the material's `sub_emitter_mode` picks when (`CONSTANT`, `AT_END`, `AT_COLLISION`, `AT_START`). Sparks that each leave a puff when they die use `AT_END`. The [sub-emitter manual](https://docs.godotengine.org/en/stable/tutorials/3d/particles/subemitters.html) lists the surprises: a system used as a sub-emitter stops emitting on its own, and its total is capped by its own `amount`. When the material's settings run out, a [particle shader](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/particle_shader.html) (`shader_type particles;`) takes over. In 4.7.2 the dummy renderer still compiles shader source, so a type error is catchable without a window; what the particles look like is not.

Particles cost in three places, and a headless run sees one.

1. **CPU simulation.** CPU nodes update every particle on the CPU every frame. That time appears in any wall-clock measurement.
2. **GPU simulation.** GPU nodes run their process material on the GPU. `--headless` selects a dummy renderer that does no GPU work.
3. **Drawing.** Large, transparent, overlapping quads cost fill rate, which the [GPU optimization page](https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html) calls very expensive on mobile. Headless has no drawing at all.

So a headless measurement reports GPU particles as nearly free. That is a property of the instrument, not of GPU particles. The levers that matter regardless are `amount`, `lifetime`, `fixed_fps`, the `visibility_rect` (2D) or `visibility_aabb` (3D) and texture size and transparency; a rectangle that is too small makes an effect vanish at the screen edge. Real GPU cost needs the Profiler and Monitors on a real GPU, which Module 13 covers.

## The Walker example: walker-2d-dodge-the-creeps

[`walker-2d-dodge-the-creeps`](https://github.com/nikbearbrown/walker-2d-dodge-the-creeps) is the Walker adaptation of Godot's official Dodge the Creeps, copied from `godot-demo-projects` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`. The repository is public and keeps the upstream MIT license; its assets carry their own terms, which its README repeats (a CC-BY 3.0 music loop, CC0 Kenney images, an SIL OFL 1.1 font).

**What the game is.** A 480×720 portrait window on the Compatibility renderer. `godot/main.tscn` owns a `Player` (an `Area2D` with an `AnimatedSprite2D`, a capsule `CollisionShape2D` and the `Trail`), mobs spawned along a `Path2D`, a HUD, and music and death-sound players. When a mob touches the player, `player.gd` hides the player, emits `hit` and disables its collision shape. `main.gd`'s `game_over()` stops the timers and music and plays the death sound.

**Its one particle node.** The `Trail` has `amount = 10`, `speed_scale = 2`, the player's walk frame as its texture, zero gravity, a shrinking scale curve and a colour ramp from half-transparent white to transparent, drawn behind the player (`z_index = -1`). `emitting` is never set, so it is true: the Trail runs all the time, and is hidden on the title screen only because its parent is.

**What its checks establish.** The build's `FRICTIONAL.md` (24 September 2026) records a clean headless import and then `test_input.gd` with 14 passing checks, among them start state, diagonal speed near 400 px/s, timed spawning and scoring, and a collision fixture. The fixture is a frozen mob placed on the player, which hides it, stops the timers and music, and offers a restart. The log calls it an "explicit fixture, not a natural gameplay claim".

**What remains unverified.** The same log lists GPU trails, audibility, pixels, gamepad controls and extended play; no person has watched this adaptation run.

For 3D particle work, read [`walker-3d-platformer`](https://github.com/nikbearbrown/walker-3d-platformer): a `CPUParticles3D` coin burst and a `particle_material.tres` that keeps the draw half of an effect (additive blending, unshaded, billboarded) in its own file.

## Predict → Build It → Use It → Ship It → Verify

### 1. Predict

Write your answers before you open a terminal, and keep them.

1. `player.gd` hides the player the instant a mob touches it. If the burst is a child of `Player`, what will `emitting` report right after the hit, and what will you see? Which property tells those apart in a test?
2. After the first death, what must happen for a `one_shot` burst to fire again on the second: nothing, `emitting = true`, or `restart()`?
3. A headless test says the burst is emitting. List three things this does not establish.
4. You will time 50,000 `CPUParticles2D` and 50,000 `GPUParticles2D` headless. Which costs more CPU per frame, and will the GPU number mean anything?

### 2. Build It

Work in your own scratch copy; do not edit the instructor's repository. The quickest start is the public Walker repository, which already holds `test_input.gd` and the one-line `player.gd` fix.

```bash
git clone https://github.com/nikbearbrown/walker-2d-dodge-the-creeps.git
```

The chapter's Build It starts from the upstream demo instead (the recorded run itself used a scratch copy of the Walker build's `godot/` folder). To take the upstream route, pin it, copy `2d/dodge_the_creeps` into a new folder as `godot/`, apply [`walker-adaptation.diff`](../../examples/09-particle-effects/walker-adaptation.diff), add [`test_input.gd`](../../examples/09-particle-effects/tests/test_input.gd), run `git init` and commit a baseline.

```bash
git clone https://github.com/godotengine/godot-demo-projects.git
```

```bash
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

From the folder that contains `godot/`, import once so Godot builds its cache, then keep the harness output as your baseline.

```bash
godot --headless --path godot --import
```

```bash
godot --headless --path godot --script res://test_input.gd
```

**Step 1: the burst (Claude Code).** This prompt is a specification. It names the invariant the change must respect (the player hides on hit), the one change, what not to touch, and the evidence to bring back.

```text
You are working in a copy of walker-2d-dodge-the-creeps, a Godot 4.7.2 GDScript project in godot/. Inspect before editing: read godot/main.gd, godot/main.tscn, godot/player.gd, godot/player.tscn and godot/test_input.gd.

Goal: when a mob hits the player, a one-shot particle burst plays where the player was. One change only.

Requirements
1. Add a GPUParticles2D named DeathBurst to main.tscn, configured in the scene file (not built in code): emitting false, one_shot true, explosiveness 1.0, amount 32, lifetime 0.6, and a ParticleProcessMaterial that sprays in every direction (spread 180) at 150 to 300 px/s with zero gravity, shrinking over its life and fading to transparent through a color ramp.
2. The player hides itself when hit (player.gd, _on_body_entered). The burst must still be visible in the tree when it fires. Choose its parent with that in mind and explain the choice.
3. In main.gd game_over(), move DeathBurst to the player's global position and restart it. It must fire again on every later death, and it must never fire at game start.
4. Do not change player.gd, the Trail, collision shapes, timers, music, HUD or the existing test.
5. Add godot/tests/test_particles.gd (extends SceneTree), runnable with
   godot --headless --path godot --script res://tests/test_particles.gd
   Reuse the fixture style of test_input.gd: start through the real Start button, force a hit with a frozen mob at the player's position. Assert: not emitting before the hit; emitting and is_visible_in_tree() right after it; global position equals the player's position at the hit; the finished signal arrives within lifetime + 0.5 s; after a restart through the Start button and a second forced hit, it emits again. Print one PASS or FAIL line per check and quit(1) on any failure.
6. Run the new test and test_input.gd headlessly and paste their real output. Headless Godot uses a dummy renderer, so GPU particles are never drawn: state what a human must check on screen, and do not claim anything the output does not show.
```

The chapter's record used this non-interactive command with a scoped allow list; in an interactive Claude Code session, paste the prompt instead.

```bash
claude -p "$(cat prompt1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > session1.jsonl
```

`Bash(godot:*)` permits commands that begin with `godot`. It does not permit `/Applications/Godot.app/Contents/MacOS/Godot`, although that is the same program. Put the exact test commands in your project's `CLAUDE.md` or `AGENTS.md`, or you will reproduce the first failure in this module's record.

**Step 2: the cost (Codex).** A measurement is its own change, so it gets its own prompt. `-s workspace-write` limits Codex to writing inside the project, and `< /dev/null` stops it waiting for input when run from a script.

```text
Work in godot/ of this Godot 4.7.2 project. Do not edit any existing game file.

Add godot/tests/particle_cost.gd (extends SceneTree), runnable with
godot --headless --path godot --script res://tests/particle_cost.gd
It measures what particle simulation costs the CPU in this headless run, not how it looks.

For each node type (GPUParticles2D with a ParticleProcessMaterial, and CPUParticles2D) and each amount (1000, 10000, 50000): create one emitting emitter with lifetime 1.0, initial velocity 50 to 100 and gravity (0, 98) under an empty Node2D, wait 60 warm-up frames, then time 300 frames with Time.get_ticks_usec() and report the mean milliseconds per frame. Repeat each case 3 times in the same process; print min, mean and max of the three means. Also print one empty-scene baseline with no emitter. Free each emitter and wait two frames before the next case.

At the top of the output, print RenderingServer.get_current_rendering_method(), RenderingServer.get_video_adapter_name(), and one sentence stating that headless Godot uses a dummy renderer, so GPU particle simulation and all drawing are not measured. Run it and paste the real output. Do not interpret a GPUParticles2D number as its real cost.
```

```bash
codex exec -s workspace-write -C . --json -o codex-last.txt "$(cat prompt2.txt)" > codex1.jsonl < /dev/null
```

This prompt has a flaw. Find it before you reach "What the agents got wrong"; the section on why frames are not seconds in [Chapter 0](../../chapters/00-the-toolchain.md) is the hint.

### 3. Use It

Open the project in the Godot editor. You are the only instrument that can see here, so every look-and-judge item is a **HUMAN CHECK**.

1. In the **Scene** dock, select `DeathBurst` and confirm its parent is `Main`. In the **Inspector**, read `One Shot`, `Explosiveness`, `Amount`, `Lifetime` and `Texture`, then open the `Process Material` and read `Spread`, `Initial Velocity`, `Gravity` and `Disable Z`.
2. **HUMAN CHECK.** Tick `Emitting` to preview the effect in the 2D viewport. Is it a burst of visible dots or a sprinkle of single pixels? Does anything crawl as though it had no speed?
3. **HUMAN CHECK.** Run the game (F5) and die on purpose. Does the burst read as a death against the teal background? Does it clash with the "Game Over" message? Restart and die somewhere else: same burst, new place?
4. **HUMAN CHECK.** Move in every direction and look at the `Trail` ghosting, the effect the Walker log still lists as unverified.
5. Open **Debugger → Monitors** while playing. On a Mac, the [debugger panel documentation](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_panel.html) says the Visual Profiler is not supported with the Compatibility renderer. For per-stage GPU timing, switch to Mobile or Forward+ temporarily, knowing you are then measuring a different renderer.

Write down what you saw, with the date and your machine. That note is the only evidence of how the effect looks.

### 4. Ship It

- **Commit in three steps** so the history shows the work: the baseline; the burst with its test; the cost script with its real output.
- **`FRICTIONAL.md`:** the prompts, what the agent claimed, what you ran, what failed, what you changed, and what you saw on screen, including anything the agent got wrong about the engine.
- **`SOURCES.md`:** the burst's texture is a generated `GradientTexture2D`, so no third-party asset; state the human/AI split of the code.
- **Film:** `godot-gamedev` fits this practice: the `DeathBurst` node and material, the two lines in `game_over()`, the test's PASS lines and the cost table, each followed by what it does. Assignment 7 requires a `godot-walkthrough` film, which must be captured in real play on a real screen; a headless log cannot stand in for it. The Brutalist skills come from a course-provided checkout; if yours lacks one, request the update.

### 5. Verify

Run the checks yourself. A pasted transcript is not a result.

```bash
timeout 120 godot --headless --path godot --script res://tests/test_particles.gd
```

```bash
timeout 120 godot --headless --path godot --script res://test_input.gd
```

```bash
timeout 300 godot --headless --fixed-fps 60 --path godot --script res://tests/particle_cost.gd
```

`timeout` is there because a test that hits a script error before `quit()` never exits. Run the two gameplay tests in real time, with no `--fixed-fps`: they wait on `create_timer` and end by waiting 0.25 s for audio to stop. Under `--fixed-fps 60` that wait passes in milliseconds of wall time, so both tests still pass their assertions but exit with leaked audio playback objects. Run the cost script with `--fixed-fps 60`, for the reason given below.

A pass on `test_particles.gd` establishes that the burst is a configured one-shot with a texture and Disable Z, is silent before a death, starts on a death, is visible in the tree then, sits where the player was, emits `finished` within its lifetime plus half a second of engine time, and restarts on a second death. It does not establish that you can see it, that it looks like a death or reads against the background, or what it costs a GPU.

## What the agents got wrong

Everything here was run on 27 September 2026 on the instructor's Mac with Godot 4.7.2, Claude Code 2.1.150 (default model `claude-sonnet-4-6`) and Codex CLI 0.153.4.

**It predicted instead of running.** Claude Code's allow list said `godot`, but it called the absolute path to the app, was refused five times, and could not ask for permission in `-p` mode. Its report then printed a table headed "Expected headless output", predicting three failures and explaining each as an engine limitation. The instructor ran the test: one check failed, and two of the three predictions were wrong.

**It blamed the engine for its own bug.** Told to run the tests, the agent reported that the one FAIL was a headless limitation: the dummy renderer, it said, never advances particle timers. That was false. A probe run before any agent started had shown a one-shot `GPUParticles2D` with `lifetime = 0.5` emitting `finished` 504–513 ms after `restart()`. The fault was a GDScript lambda, which cannot reassign an outer local variable: the signal fired and the lambda set its own copy of the flag. The correction that was sent:

```text
Your explanation of the FAIL is wrong. finished does fire in headless Godot 4.7.2: in a separate probe, a one-shot GPUParticles2D with lifetime 0.5 emitted finished about 0.5 s after restart(). Look at your test instead. GDScript lambdas capture local variables by value, and a lambda cannot reassign an outer local (see "Lambda functions" in the GDScript reference). Fix the test so the flag can actually change, rerun both tests, and paste the output. Do not weaken or remove the check.

Two DeathBurst settings are also plausible but wrong for 2D, according to the documentation:
- GPUParticles2D.texture is null, and the class reference says a null texture draws 1x1-pixel squares. Give the burst a soft round dot: a GradientTexture2D sub-resource, 16x16, radial fill, white centre fading to transparent.
- ParticleProcessMaterial is shared with 3D, and the official 2d/particles demo README says to enable Disable Z when it is used in 2D. Set particle_flag_disable_z = true.
Add a check for each to test_particles.gd. Change nothing else.
```

**The state checks could not see a burst of thirty-two pixels.** Two defects came from reading the documentation, not from running anything: the first version had no texture and no Disable Z, which by the class reference makes it thirty-two single pixels, and its report still called it "32 white particles spray in all directions". The agent fixed both, but also added an unsupported claim about particles vanishing from the camera, and left a comment saying `emitting` "always returns false" above a check that passes. Remove that residue in review.

**The benchmark measured the engine's idle sleep.** Codex wrote the cost script exactly as specified and printed 6.90 ms for every case, including an empty scene. Headless Godot sleeps toward a 6,900 µs frame period unless a fixed frame rate is set, so any work under 6.9 ms hides inside the sleep. The flaw was in the prompt, which did not name `--fixed-fps 60`. With it, the three CPU amounts cost 0.035, 0.33 and 1.61 ms per frame (a linear 0.032 µs per particle on that machine), and `GPUParticles2D` cost 0.0023 to 0.0024 ms, the same as an empty scene.

## If you know Unity or Unreal

Unity and Unreal were not run for this module; the comparisons come from their official documentation, as checked in the chapter on 27 September 2026.

| Godot | Unity | Unreal Engine 5 |
|---|---|---|
| `GPUParticles2D` / `3D` | Visual Effect Graph | Niagara emitter, GPU Sim Target |
| `CPUParticles2D` / `3D` | Built-in Particle System | Niagara emitter, CPU Sim Target |
| `ParticleProcessMaterial` | modules (Built-in) | Particle Spawn / Update modules |
| `one_shot` | Looping off | Emitter State: Loop Behavior Once |
| `amount` with `explosiveness = 1` | Emission module Burst | Spawn Burst Instantaneous |
| `finished` | `OnParticleSystemStopped` | `OnSystemFinished` |
| sub-emitter (GPU only) | Sub Emitters module | event handler (CPU only) |

The biggest difference for an agent workflow is what it can read. A Godot `.tscn` is text, so the agent read and diffed `main.tscn` here. Unity's scenes and prefabs are YAML by default, but references go through GUIDs in `.meta` files, and a wrong one fails as quietly as a wrong path in a `.tscn`. A Niagara system is a binary `.uasset`: an agent can write the C++ that spawns it or drive the editor with Python, but cannot review the emitter as a diff. [The chapter](../../chapters/09-particle-effects.md) has the full comparison.

## Practice assessment (ungraded)

Answer in your own words, using the source and the running game:

1. Why is `emitting == true` not enough to say a death burst was seen, and which property would you assert instead?
2. Name two `DeathBurst` settings that pass state checks yet make a bad effect on screen. How would you find each without running anything?
3. Why did the first cost run report 6.90 ms for an empty scene, and what changed with `--fixed-fps 60`?
4. What can a headless `GPUParticles2D` measurement tell you about phone cost, and which tool would tell you more?

The Canvas practice quiz covers the same ground. Do not paste Claude's explanation as proof of your understanding. Ask it to question you, then answer and check the source yourself.

## The next step

This module feeds **Assignment 7 - Two Particle Effects, Tuned and Priced**. It opens in Module 9 and is due about Day 70. The earlier version of this course also asked for two particle effects and a video showing how they work and how you made them; that survives. The new part is the price: you will tune each effect and put a measured cost beside it. The long reading, with the full Unity and Unreal comparisons, is the companion chapter, [Chapter 9 — Particle Effects](../../chapters/09-particle-effects.md). Module 10 turns to animation.
