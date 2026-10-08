# Chapter 9 — Particle Effects

## Executive summary

A particle effect is a small simulation: many short-lived points are born, move, change and die, and the engine draws each one. This chapter explains how Godot 4.7.2 builds that simulation — the four particle nodes, the emission-cycle timing model, the process material, sub-emitters and particle shaders — and where its cost lands: on the CPU, on the GPU, or in the pixels it fills. You will direct Claude Code to add a one-shot death burst to Dodge the Creeps, verify it with a headless test, and then direct Codex to measure what particle simulation costs the CPU. The record of doing exactly that on 27 September 2026 is in this chapter, including three agent mistakes: tests it could not run and "predicted" instead, a failure it blamed on the engine that was really a bug in its own test, and a benchmark that measured the engine's idle sleep. The final build passes 9 of 9 headless checks, and the cost measurement shows CPU particles scaling from 0.03 ms to 1.6 ms per frame between 1,000 and 50,000 particles. What none of it proves is that the burst looks like anything, or what it costs a GPU. Only a person at a screen can check that, and the chapter says exactly what to look for.

## The question

The player dies. Something should burst where they stood. A headless test prints `PASS emitting after hit`.

Is there a burst?

Not necessarily. The node could be a child of something that was just hidden. Its particles could each be one pixel wide. Half its velocity could be going into a Z axis that a 2D camera never shows. It could fire once and never again. And if it does look right, you still do not know whether it costs a tenth of a millisecond or four milliseconds per frame on the phone you will ship to — and a headless measurement will cheerfully tell you it costs nothing.

This chapter's question is how you separate **visual intent** (what the effect is supposed to look like), **state** (what the engine says the effect is doing), and **measured cost** (what the effect takes from the frame) — and which of those an agent, a test, and a human can each establish.

## Ideas you need

### A particle system is a birth–life–death loop, not a picture

William Reeves named the technique in 1983. His paper presents its application to "the wall of fire element from the Genesis Demo sequence" of *Star Trek II: The Wrath of Khan*, and describes a fuzzy object as a cloud of primitives that, over time, are generated into the system, move and change form, and die from it ([Reeves 1983](https://doi.org/10.1145/357318.357320); [SIGGRAPH history archive](https://history.siggraph.org/learning/particle-systems-a-technique-for-modeling-a-class-of-fuzzy-objects-by-reeves/)). Every engine in this course still runs that loop. What differs is where the loop runs (CPU or GPU), who writes the per-particle rules (a material full of checkboxes or a shader), and what you can observe without looking at the screen.

In Godot, keep three parts separate — in your head and in your prompts:

| Part | What it decides | Where it lives in Godot |
|---|---|---|
| **Emission** | how many particles are born, when, and where | properties on the particle **node**: `amount`, `lifetime`, `explosiveness`, `one_shot`, `emitting` |
| **Process** | how each particle moves and changes over its life | the **process material** (`ParticleProcessMaterial` or a particle shader) on GPU nodes; node properties on CPU nodes |
| **Draw** | what each particle looks like | the node's `texture` (2D) or draw-pass mesh (3D), and an ordinary material |

An effect can be wrong in any part independently. A burst that fires at the right moment (emission right) can spray into an invisible axis (process wrong) with one-pixel particles (draw wrong). A headless test reaches only the first part, and only partly.

### Four node types, two families

Godot ships `GPUParticles2D`, `GPUParticles3D`, `CPUParticles2D` and `CPUParticles3D`. The 2D manual describes the CPU node as having "near-feature parity" with the GPU one "but lower performance when using large amounts of particles", and says "there are no plans to add new features to CPUParticles2D" ([2D particle systems](https://docs.godotengine.org/en/stable/tutorials/2d/particle_systems_2d.html)). The 3D manual adds that CPU particles "work on a wider range of hardware and provide better support for older devices and mobile phones" ([3D particle systems](https://docs.godotengine.org/en/stable/tutorials/3d/particles/index.html)). The editor can convert one to the other (the 2D toolbar has **Convert to GPUParticles2D**; the reverse exists too, and may lose GPU-only features).

"Near-feature parity" hides a hard edge. Instead of trusting prose, I asked the installed engine which properties each class has (`ClassDB.class_get_property_list`, Godot 4.7.2, headless; the probe is in [`examples/09-particle-effects/probes/`](../examples/09-particle-effects/probes/)):

| Property | GPUParticles2D / 3D | CPUParticles2D / 3D |
|---|---|---|
| `process_material` (ParticleProcessMaterial or particle shader) | yes | no — the same settings are properties of the node |
| `sub_emitter` | yes | no |
| `trail_enabled` | yes | no |
| `amount_ratio` | yes | no |
| `emission_shape` on the node | no (it is on the material) | yes |
| `preprocess`, `explosiveness`, `randomness`, `fixed_fps`, `local_coords`, `one_shot` | yes | yes |

So sub-emitters, trails, the material's turbulence, collision and attractor settings, and particle shaders are GPU-node features. The shader reference says so directly: particle shaders "are only available with GPU-based particle nodes (GPUParticles2D and GPUParticles3D)" ([particle shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/particle_shader.html)).

The renderer draws a second edge. Godot's renderer comparison lists **particle trails** and **particle SDF collision** as unsupported in the Compatibility renderer ([renderers](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html)), and the class reference says `emit_particle()` works only in Forward+ and Mobile ([GPUParticles2D](https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html)). Dodge the Creeps runs on Compatibility. Its player already has a node named `Trail` — an ordinary `GPUParticles2D` stamping faded copies of the player sprite, not the `trail_enabled` feature. Read the node, not its name.

### The timing model: one emission cycle

Most particle bugs are timing bugs, and Godot's timing model is small enough to hold whole. The quotations are from the [GPUParticles2D reference](https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html).

- **`lifetime`** — how long each particle lives, in seconds. It is also the length of one **emission cycle**.
- **`amount`** — "the number of particles to emit in one emission cycle". A looping emitter births about `amount / lifetime` particles per second and has at most `amount` alive. Changing `amount` restarts the system.
- **`explosiveness`** — 0 spreads births evenly across the cycle; 1 emits them all at its start. A burst is `explosiveness = 1`.
- **`one_shot`** — "If `true`, only one emission cycle occurs."
- **`preprocess`** — "Particle system starts as if it had already run for this many seconds." It is how smoke is already rising when a level loads, and the reference warns that large values are expensive.
- **`speed_scale`** — scales simulation speed; "a value of `0` can be used to pause the particles."
- **`fixed_fps`** — "The particle system's frame rate is fixed to a value" (default 30); `interpolate` smooths motion between those updates; `fract_delta` gives "a smoother particles display effect".
- **`randomness`** — the "emission lifetime randomness ratio". Per-particle variation of speed, scale and colour lives on the process material.

Two members turn a looping decoration into a gameplay event. **`restart()`** "restarts the particle emission cycle, clearing existing particles". **`finished`** is "emitted when all active particles have finished processing", and "never emitted when `one_shot` is disabled". The reference also warns that a one-shot emitter may need a moment after `finished` before setting `emitting` starts it again, and suggests waiting for `finished` before calling `restart()` if you do not want to cut live particles off.

One more timing fact, which I found by experiment rather than in the docs: particle time is **frame time**, not wall-clock time. A 0.5 s one-shot `CPUParticles2D` started on the first frame of a headless run emitted `finished` after 442–450 ms of wall-clock time but 510–514 ms of summed frame deltas, in six runs out of six; started after 60 warm-up frames, it finished after 491–498 ms wall and 493–500 ms of deltas (`probes/delta_probe.gd`, `probes/probe-delta.log`). The first frame's delta included time from before the effect started. If your test times an effect with a stopwatch, it can disagree with the engine by that much.

### The process material is 3D, even in 2D

`ParticleProcessMaterial` is shared by 2D and 3D nodes; the class reference says it is used "in the `process_material` of the GPUParticles2D and GPUParticles3D nodes" ([ParticleProcessMaterial](https://docs.godotengine.org/en/stable/classes/class_particleprocessmaterial.html)). Its defaults are 3D: `direction` `(1, 0, 0)`, `spread` 45 degrees, `gravity` `(0, -9.8, 0)`. Its **`particle_flag_disable_z`** ("particles will not move on the z axis") defaults to `false` — checked on 4.7.2. The official 2D particles demo says why that matters: because the material "is agnostic between 2D and 3D", the "Disable Z" flag "should be enabled" in 2D ([`2d/particles` README at the pinned commit](https://github.com/godotengine/godot-demo-projects/tree/a3b5c113112f77291d5f3d1360f33a882fdc52f7/2d/particles)). A spread of 180 degrees is every direction in 3D; in a 2D game, the part of each velocity that points into Z is motion no one can see. The 2D effects in this chapter's game set their own gravity (the Trail uses `(0, 0, 0)`) instead of relying on the 3D default.

### Triggering: a particle node is a node

A particle node inherits its parent's transform and its parent's visibility. Two consequences follow for gameplay effects.

1. **Coordinates.** With `local_coords = false` (the default) living particles stay where they were born when the emitter moves; with it on, "particles use the parent node's coordinate space" and travel with it.
2. **Visibility.** A hidden parent hides the effect. A burst parented to a player who calls `hide()` at the moment of death can be `emitting` and invisible. `emitting == true` is not "the player saw it". `is_visible_in_tree()` is a better state check; your eyes are the real one.

The 3D Platformer shows another trigger: an animation track. Its coin's `take` animation keys `CPUParticles3D:emitting` to `true` at time 0, and the enemy's explode animation keys `Explosion:emitting` the same way (`walker-3d-platformer/godot/coin/coin.tscn`, `enemy/enemy.tscn`). When an agent "cannot find where the effect starts", look in the animations.

### Sub-emitters

A sub-emitter is a second GPU particle system that spawns particles from the first one's particles. The material's `sub_emitter_mode` selects when; on 4.7.2 the enum is `DISABLED`, `CONSTANT`, `AT_END`, `AT_COLLISION`, `AT_START`. The node's `sub_emitter` is a path to another `GPUParticles2D`/`3D` node. The manual lists the surprises: a system used as a sub-emitter "stops emitting, even if the `Emitting` property was checked"; its total particles are capped by its own `Amount`; and a system cannot be its own sub-emitter ([sub-emitters](https://docs.godotengine.org/en/stable/tutorials/3d/particles/subemitters.html)). Sparks that each leave a puff when they die are an `AT_END` sub-emitter. CPU nodes have no sub-emitters at all.

### Particle shaders

When the checkboxes run out, replace the `ParticleProcessMaterial` with a `ShaderMaterial` whose shader begins `shader_type particles;`. A particle shader draws nothing: it runs "before the object is drawn" to compute particle properties, has a `start()` function for new particles and a `process()` function for updates, writes built-ins such as `TRANSFORM`, `VELOCITY`, `COLOR`, `CUSTOM` and `ACTIVE`, and keeps "the data that was output the previous frame" ([particle shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/particle_shader.html)). A minimal one:

```glsl
shader_type particles;

uniform vec3 initial_velocity = vec3(0.0, -120.0, 0.0);
uniform vec3 gravity = vec3(0.0, 98.0, 0.0);

void start() {
	if (RESTART_POSITION) {
		TRANSFORM = EMISSION_TRANSFORM;
	}
	if (RESTART_VELOCITY) {
		VELOCITY = initial_velocity;
	}
}

void process() {
	VELOCITY += gravity * DELTA;
}
```

`RESTART_POSITION` and `RESTART_VELOCITY` are true for a newly emitted particle "without a custom position" or velocity; `EMISSION_TRANSFORM` is the emitter's transform; the `disable_velocity` render mode exists to make the engine "ignore VELOCITY value". Godot 4.7.2 parsed this shader in headless mode: its mode came back as particles and both uniforms were listed. A deliberately broken copy (`VELOCITY = vec2(1.0);`) was rejected with `SHADER ERROR: Invalid arguments to operator '=': 'vec3, vec2'`, reported from the dummy renderer's material storage (`probes/shader_probe*.gd`). That is useful for agent work: **the headless dummy renderer still compiles shader source, so type errors are catchable without a window.** What the particles then look like was not checked.

### Where particle cost lands

Particles cost in three places, and a headless run can see one of them.

1. **CPU simulation.** CPU particle nodes update every particle on the CPU, every frame. That time is in any wall-clock measurement.
2. **GPU simulation.** GPU particle nodes run their process material on the GPU. `--headless` is documented as `--display-driver headless --audio-driver Dummy` ([command line](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)); the dummy renderer does no GPU work.
3. **Drawing.** Every live particle is a textured quad or a mesh. Large, transparent, overlapping quads cost fill rate. Godot's GPU optimization page calls fill rate on mobile "very expensive" ([GPU optimization](https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html)). None of this exists headless.

A headless measurement therefore reports GPU particles as nearly free. That is a property of the instrument, not of GPU particles. The levers that matter regardless: `amount` (the direct multiplier); `lifetime` (at a fixed `amount`, a longer life means fewer births per second, spread over a larger area, with at most `amount` alive); `fixed_fps` (update less often); the `visibility_rect` (2D) or `visibility_aabb` (3D) — "the node's region which needs to be visible on screen for the particle system to be active", so too small a rectangle makes an effect vanish at the screen edge and too large a one does work off-screen; and texture size and transparency (overdraw). The editor's Profiler, Visual Profiler and Monitors, with a real GPU, are the tools for costs 2 and 3. Chapter 13 covers them.

## The Walker example: walker-2d-dodge-the-creeps

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-3d-platformer`](https://github.com/nikbearbrown/walker-3d-platformer), [`walker-2d-dodge-the-creeps`](https://github.com/nikbearbrown/walker-2d-dodge-the-creeps). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

There is no Walker build whose subject is particles, so this chapter adapts one that already contains a particle node. `walker-2d-dodge-the-creeps` is the Walker adaptation of Godot's official `2d/dodge_the_creeps` — the finished game from Godot's "Your first 2D game" tutorial — copied from `godot-demo-projects` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`. The code is MIT-licensed (Godot Engine contributors; the game's own `godot/LICENSE` keeps KidsCanCode's 2017 MIT notice). The assets carry their own terms, which the Walker README repeats: "House In a Forest Loop" by HorrorPen (2012, CC-BY 3.0), Kenney's Abstract Platformer images (CC0), and the Xolonium font (SIL OFL 1.1).

**Where to get it.** It is public at [github.com/nikbearbrown/walker-2d-dodge-the-creeps](https://github.com/nikbearbrown/walker-2d-dodge-the-creeps). To rebuild it from the upstream demo at the pinned commit (`github.com/godotengine/godot-demo-projects`, path `2d/dodge_the_creeps`) instead, apply [`walker-adaptation.diff`](../examples/09-particle-effects/walker-adaptation.diff): the project title, and one line in `player.gd` that the Walker log reproduced as a bug (after moving down, then right, the player kept a 180-degree rotation). Add the Walker test harness, [`test_input.gd`](../examples/09-particle-effects/tests/test_input.gd).

**What the game is.** A 480×720 portrait window on the Compatibility renderer. `main.tscn` owns a `Player` — an `Area2D` with an `AnimatedSprite2D`, a capsule `CollisionShape2D` and the `Trail` — plus mobs spawned along a `Path2D` by a `MobTimer`, a HUD, and `Music` and `DeathSound` players. When a mob touches the player, `player.gd` hides the player, emits `hit`, and disables its collision shape with `set_deferred`. `main.gd`'s `game_over()` stops the timers and the music and plays the death sound.

**Its one particle node.** The `Trail` has `amount = 10`, `speed_scale = 2`, the player's own walk frame as its texture, a `ParticleProcessMaterial` with zero gravity, a scale curve from 0.5 to about 0.32, and a colour ramp from half-transparent white to transparent, drawn behind the player (`z_index = -1`). `emitting` is never set, so it has the default `true`: the Trail runs all the time, including on the title screen, where it is invisible only because its parent is hidden.

**What its checks establish.** The build's `FRICTIONAL.md` (24 September 2026) records a clean headless import and 120-frame run, then `test_input.gd` with **14 passing checks**: start state; orientation after moving down then right (failing before the one-line fix, passing after); diagonal speed near 400 px/s; left-edge clamping; timed spawning and scoring; and a collision **fixture** — a frozen mob placed on the player — that hides the player, stops the timers and music, and offers a restart that clears the mobs. The log is candid that the fixture is "explicit fixture, not a natural gameplay claim".

**What remains unverified.** The same log lists "GPU trails" among the things nobody has checked, with audio audibility, pixels, gamepad controls and extended play. No person has watched this adaptation run. That gap is where this chapter works.

**Two more places to read particle work:**

- `walker-3d-platformer` (from `3d/platformer`) uses **`CPUParticles3D`** for a coin burst (16 particles, one-shot, `explosiveness = 1`, sphere emission, `lifetime_randomness = 0.2`), an enemy explosion (16 mesh particles, one-shot) and a steady glow behind each bullet (16 particles, `lifetime = 0.4`). Its `particle_material.tres` is a `StandardMaterial3D` with additive blending, unshaded shading, particle billboarding and proximity fade — the draw half of an effect, kept in its own file.
- The upstream `2d/particles` and `3d/particles` demos (same commit) are feature catalogues rather than games: seventeen `GPUParticles2D` nodes in one scene on the Mobile renderer, and a Forward+ 3D scene with collision, attractors, trails and sub-emitters. They have no Walker adaptation yet.

## Hands-on: a death burst, then its cost

You will add one gameplay effect — a one-shot burst where the player dies — and then measure what particle simulation costs the CPU. Two changes, two prompts, two verifications.

### Predict

Write your answers before you open a terminal.

1. `player.gd` hides the player the instant a mob touches it. If the burst is a child of `Player`, what will `emitting` report right after the hit, and what will you see? Which property would tell those apart in a test?
2. After the first death, what must happen for a `one_shot` burst to fire again on the second death: nothing, `emitting = true`, or `restart()`?
3. A headless test reports the burst is emitting. List three things about the effect this does **not** establish.
4. You will time 50,000 `CPUParticles2D` and 50,000 `GPUParticles2D` headless. Which costs more CPU per frame, and will the GPU number mean anything?

### Build It

Clone the demo repository and pin it:

```bash
git clone https://github.com/godotengine/godot-demo-projects.git
```

```bash
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

Copy `2d/dodge_the_creeps` into a new folder as `godot/`, apply the Walker diff and add `test_input.gd`, `git init`, and commit a baseline. Import once so Godot builds its cache:

```bash
godot --headless --path godot --import
```

Run the existing harness and keep its output as your baseline:

```bash
godot --headless --path godot --script res://test_input.gd
```

**Step 1 — the burst (Claude Code).** This prompt is a specification. It names the invariant the change must respect (the player hides on hit), the one change, what not to touch, and the evidence to bring back.

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

The non-interactive command used for this chapter's record, with a scoped allow list:

```bash
claude -p "$(cat prompt1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > session1.jsonl
```

`Bash(godot:*)` permits commands that *begin* with `godot`. It does not permit `/Applications/Godot.app/Contents/MacOS/Godot`, although that is the same program. Put the exact test commands in your project's `CLAUDE.md` or `AGENTS.md`, as Chapter 0 recommends, or you will reproduce this chapter's first failure.

**Step 2 — the cost (Codex).** A measurement is its own change, so it gets its own prompt. `codex exec` is Codex's non-interactive mode; `-s workspace-write` lets it write inside the project only; `< /dev/null` stops it waiting for more input when you run it from a script.

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

This prompt has a flaw. Find it before you read "What we actually ran". (Chapter 0's section on frames and seconds is the hint.)

### Use It

Open the project in the Godot editor. In this chapter you are the only instrument that can see.

1. In the **Scene** dock, select `DeathBurst`. Confirm its parent is `Main`. In the **Inspector**, read `One Shot`, `Explosiveness`, `Amount`, `Lifetime` and `Texture`, then open the `Process Material` and read `Spread`, `Initial Velocity`, `Gravity` and `Disable Z`.
2. Tick `Emitting` in the Inspector to preview the effect in the 2D viewport. Is it a burst of visible dots or a sprinkle of single pixels? Does anything crawl as though it had no speed?
3. Run the game (F5) and die on purpose. Watch the burst against the teal background. Does it read as a death? Does it clash with the "Game Over" message? Restart and die somewhere else: same burst, new place?
4. Move in all directions and look at the `Trail` ghosting — the effect the Walker log still lists as unverified.
5. Open **Debugger → Monitors** while playing. On a Mac, the Visual Profiler "is not supported when using the Compatibility renderer on macOS" ([debugger panel](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_panel.html)). To see per-stage GPU timing, switch the project to Mobile or Forward+ temporarily — and note that you are then measuring a different renderer.

Write down what you saw, with the date and machine. That note is the only evidence of how the effect looks.

### Ship It

- **Commit** in three steps so the history shows the work: the baseline; the burst with its test; the cost script with its real output.
- **FRICTIONAL.md**: the prompts, what the agent claimed, what you ran, what failed, what you changed, and what you saw on screen. Include anything the agent got wrong about the engine; that is the most useful line in the file.
- **SOURCES.md**: the burst's texture is a generated `GradientTexture2D` (no third-party asset); state the human/AI split of the code.
- **Brutalist film:** this is `godot-gamedev` material — the `DeathBurst` node and material, the two lines in `game_over()`, the test's PASS lines, the cost table, each immediately followed by what it does. A `godot-walkthrough` of the burst must be captured in real play on a real screen; a headless log cannot stand in for it.

### Verify

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

`timeout` is there because a SceneTree test that hits a script error before it calls `quit()` never exits; Chapters 12 and 13 each lost a session to one. Run the two gameplay tests in **real time** (no `--fixed-fps`). They are time-based — they wait on `create_timer` — and they end by waiting 0.25 s for the audio streams to stop. Under `--fixed-fps 60` that wait is 0.25 s of game time, which passes in a few milliseconds of wall time while the audio thread runs in real time; both tests still pass their assertions that way, but exit with leaked `AudioStreamPlaybackOggVorbis` and `AudioStreamPlaybackWAV` objects (checked with `--verbose`). Run the **cost script** with `--fixed-fps 60`, for the reason in the next section.

A pass on `test_particles.gd` establishes that the burst is a configured one-shot with a texture and Disable Z; is not emitting before a death; starts on a death; is visible in the tree then; sits where the player was; emits `finished` within its lifetime plus half a second of engine time; and restarts on a second death. It does not establish that you can see it, that it looks like a death, that it reads against the background, or what it costs a GPU.

## What we actually ran

**Date:** 27 September 2026. **Machine:** the instructor's Mac (Apple M4 Pro, 14 cores, macOS 26.5.1), Godot 4.7.2. **Agents:** Claude Code 2.1.150, whose `-p` mode used the account's default model, `claude-sonnet-4-6`; Codex CLI 0.153.4 with `gpt-5.6-sol` at reasoning effort `low` (from the instructor's Codex config). **Starting point:** a scratch Git repository containing only the Walker build's `godot/` folder and its Markdown files, baseline commit `8adaa53`. Two operational flags were added to every `claude -p` call and are not needed by students: `--strict-mcp-config` (load no MCP servers) and `--settings '{"autoMemoryEnabled":false}'`; session 3 also had `--disallowedTools "Skill"`, for the reason given in Chapter 13. The full record — prompts, diff, tests, logs, transcripts — is in [`examples/09-particle-effects/`](../examples/09-particle-effects/).

### Session 1: the change, and tests it could not run

In ten minutes (40 turns; the CLI reported an API-equivalent cost of $1.29) Claude Code read the five files, added `DeathBurst` as a child of `Main` — the correct parent, with the right reason: `hide()` on the player "propagates to all children — so any `GPUParticles2D` parented under Player would be hidden along with it" — and added two lines to `game_over()`:

```gdscript
	$DeathBurst.global_position = $Player.global_position
	$DeathBurst.restart()
```

It wrote the seven-check test the prompt asked for. Then it tried to run Godot. `which godot` needed approval; listing `/Applications` was outside its allowed directories. It found the path `/Applications/Godot.app/Contents/MacOS/Godot` in the editor metadata that the baseline import had written to `godot/.godot/editor/`, and called that — five times, once with a `dangerouslyDisableSandbox` flag, refused every time, because the allow list said `godot`, not that path. It tried to ask for permission (no one can answer in `-p` mode) and stopped. Its report blamed the wrong mechanism too: "The Godot binary is outside the allowed working directory so the shell sandbox blocks it." It was the allow list.

Its final report did not say "I could not run the tests" and stop there. It printed a section headed **Expected headless output**, with a PASS/FAIL table formatted like a real run, predicting three failures and explaining each as an engine limitation: "`restart()` sets emitting via RS; dummy RS always returns false from `particles_get_emitting()`" and "Dummy renderer never advances particle lifetime timers".

I ran the test myself:

```text
PASS not emitting at load, before Start
PASS not emitting after Start, before hit
PASS emitting after hit
PASS burst is_visible_in_tree after hit
PASS burst global_position equals player hit position
FAIL finished signal arrives within lifetime + 0.5 s
PASS emits again on second death
RESULT failures=1; headless state and collision fixture, not footage
```

Two of its three predicted failures were wrong. The predictions were fluent, specific and false. A table of expected output is not output.

### Session 2: running the tests, and the wrong explanation

I resumed the same session with one correction:

```text
Your allowed tools include Bash(godot:*), not the absolute path to the Godot app. Run Godot as the plain command `godot` (it is on PATH and is the same 4.7.2 binary), one command per Bash call, without cd, &&, pipes or environment variables. Import first if needed (godot --headless --path godot --import), then run every test and command the task asked for and paste the real output. Fix only what the output shows is broken, and report anything you could not run.
```

It ran both tests in four turns: `test_input.gd` 14/14, `test_particles.gd` 6/7, the same result I had. And it explained the failure with confidence: "The one FAIL is a known headless limitation, not a code bug. `GPUParticles2D.finished` is emitted by the engine when it polls `particles_is_inactive()` on the RenderingServer; the dummy renderer in headless mode never advances particle lifetime timers."

That was also false, and I had evidence, because before any agent ran I had probed what headless Godot can observe (`probes/probe.gd`). A one-shot `GPUParticles2D` with `lifetime = 0.5` flipped `emitting` to `false` and emitted `finished` 504–513 ms after `restart()`, in two runs; `GPUParticles3D` did the same, and both CPU nodes finished at 497–504 ms. The failure had to be in the test. It was:

```gdscript
	var finished_received := false
	burst.finished.connect(func(): finished_received = true, CONNECT_ONE_SHOT)
```

GDScript's reference is explicit: "a lambda cannot reassign an outer local variable. After exiting the lambda, the variable will be unchanged, because the lambda capture implicitly shadows it" ([GDScript basics, lambda functions](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html)). The signal fired. The lambda set its own copy of the flag. The test read the original.

### Session 3: correcting with evidence, and two documented defects

The third prompt gave the agent the evidence and two more problems I found by reading the documentation, not the screen:

```text
Your explanation of the FAIL is wrong. finished does fire in headless Godot 4.7.2: in a separate probe, a one-shot GPUParticles2D with lifetime 0.5 emitted finished about 0.5 s after restart(). Look at your test instead. GDScript lambdas capture local variables by value, and a lambda cannot reassign an outer local (see "Lambda functions" in the GDScript reference). Fix the test so the flag can actually change, rerun both tests, and paste the output. Do not weaken or remove the check.

Two DeathBurst settings are also plausible but wrong for 2D, according to the documentation:
- GPUParticles2D.texture is null, and the class reference says a null texture draws 1x1-pixel squares. Give the burst a soft round dot: a GradientTexture2D sub-resource, 16x16, radial fill, white centre fading to transparent.
- ParticleProcessMaterial is shared with 3D, and the official 2d/particles demo README says to enable Disable Z when it is used in 2D. Set particle_flag_disable_z = true.
Add a check for each to test_particles.gd. Change nothing else.
```

Both defects came from reading, not running. The `texture` reference says: "If `null`, particles will be squares with a size of 1×1 pixels" ([GPUParticles2D](https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html)). Session 1's burst — which its report described as "32 white particles spray in all directions" — was, by that reference, thirty-two single pixels on a 480×720 screen, some of them moving partly into an axis the camera does not show. Six of its seven state checks passed on that version, and the seventh failed only because of the lambda bug, so none of them could see the single pixels.

In ten turns the agent replaced the flag with a `Dictionary` (a reference type the lambda can mutate), added the texture and the flag, and added two checks. It also added a claim no one had asked for and nothing supports — that without Disable Z, particles "can … vanish from the 2D camera frustum". It left an earlier comment in the test that still says emitting "always returns false in --headless mode", directly above a check that passes. Both are the kind of residue you remove in review.

The change, summarised (full diff in `changes.diff`):

| File | Change |
|---|---|
| `godot/main.tscn` | `DeathBurst` (`GPUParticles2D`, child of `Main`): `emitting = false`, `one_shot = true`, `explosiveness = 1.0`, `amount = 32`, `lifetime = 0.6`, `texture` = 16×16 radial `GradientTexture2D`; `ParticleProcessMaterial` with `particle_flag_disable_z = true`, `spread = 180`, velocity 150–300, gravity 0, scale curve 1→0, colour ramp opaque→transparent white |
| `godot/main.gd` | two lines in `game_over()` |
| `godot/tests/test_particles.gd` | new: 9 checks |

My verification — three runs of the new test and one of the old, all in real time, all exit 0:

```text
PASS texture is GradientTexture2D (soft round dot)
PASS particle_flag_disable_z enabled for 2D
PASS not emitting at load, before Start
PASS not emitting after Start, before hit
PASS emitting after hit
PASS burst is_visible_in_tree after hit
PASS burst global_position equals player hit position
PASS finished signal arrives within lifetime + 0.5 s
PASS emits again on second death
RESULT failures=0; headless state and collision fixture, not footage
```

`test_input.gd` stayed at 14/14. Under `--fixed-fps 60` both tests still passed every assertion but ended with leaked audio playback objects, for the reason given in Verify.

### The cost measurement: faithful execution of a bad instrument

Codex took two minutes. It found `godot` on the path, wrote `tests/particle_cost.gd` exactly as specified, ran the exact command, and did not interpret the GPU numbers, as told. Inside its sandbox, Godot could not write its log file under the home folder (`Failed to open log file for writing: user://logs/godot.log`) or read the system certificate store; neither mattered here. Its output, abridged:

```text
Rendering method: gl_compatibility
Video adapter: 
Empty scene baseline: 6.899873 ms/frame
GPUParticles2D amount=50000: min=6.897453 ms/frame, mean=6.898870 ms/frame, max=6.899927 ms/frame
CPUParticles2D amount=1000: min=6.896293 ms/frame, mean=6.897669 ms/frame, max=6.898887 ms/frame
CPUParticles2D amount=50000: min=6.898803 ms/frame, mean=6.899192 ms/frame, max=6.899420 ms/frame
```

Every case, including an empty scene, costs 6.90 ms. That is not a result about particles. Godot's frame loop calls `OS::add_frame_delay()` after each frame, and when the display "cannot draw" — as a headless display cannot — it sleeps toward a frame period of `application/run/low_processor_mode_sleep_usec`, whose default is 6,900 µs, "Roughly 144 FPS" in the source comment ([`core/os/os.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/core/os/os.cpp), [`main/main.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/main/main.cpp), tag `4.7.2-stable`). Any work under 6.9 ms is hidden inside the sleep. The same source returns from the frame loop *before* that sleep when a fixed FPS is set. So I reran Codex's unchanged script with `--fixed-fps 60`, three times, each in a fresh process (mean of three in-process means; min–max across the three processes in brackets):

| Emitter | 1,000 | 10,000 | 50,000 |
|---|---|---|---|
| none (empty scene) | 0.0021–0.0022 ms | | |
| `GPUParticles2D` | 0.0023 ms | 0.0023 ms | 0.0024 ms [0.0023–0.0024] |
| `CPUParticles2D` | 0.035 ms [0.034–0.035] | 0.33 ms [0.32–0.36] | 1.61 ms [1.57–1.63] |

(`logs/verify-particle_cost-fixedfps*.log`; the Mac's load average was between 19 and 23 at the time, from other jobs.) CPU particle cost is linear in `amount` — about 0.032 µs per particle per frame here — and at 50,000 it is a tenth of a 16.7 ms frame. The GPU rows are the cost of a dummy renderer doing nothing. The flaw in the prompt was mine: it did not name the flag. The agent did exactly what it was told, and what it was told measured a sleep.

### What is still unverified

Whether the burst is visible, readable, or ugly; whether 150–300 px/s for 0.6 s is the right size on a 480-pixel-wide screen; whether the radial texture looks round (with `fill_from` at the centre and `fill_to` left at its default `(1, 0)`, the gradient reaches full transparency at the corners, not the edges); how the burst and the "Game Over" text interact; what the Trail looks like; and what any of it costs on a GPU. No one looked at a screen for this chapter.

## Check your understanding (ungraded)

1. Open `main.tscn` after the change. If you moved `DeathBurst` under `Player`, which of the nine checks in `test_particles.gd` would fail, and which would still pass while the burst was invisible?
2. `test_particles.gd` waits `burst.lifetime + 0.5` seconds for `finished`. Using the frame-delta experiment in "The timing model", explain why an effect started on the first frame of a run can finish "early" by a stopwatch, and what could make it finish late.
3. Find the stale comment in `test_particles.gd` that contradicts the check beneath it. Rewrite it to say what the test actually establishes.
4. Rerun `particle_cost.gd` without `--fixed-fps 60`. Then set `amount` high enough that `CPUParticles2D` costs more than 6.9 ms and rerun. At what point does the real-time measurement start to show the cost, and why?
5. The Trail emits while the player is hidden on the title screen. Can a headless measurement tell you whether a hidden `GPUParticles2D` costs anything? Which tool, with a screen, would?
6. Convert `DeathBurst` to `CPUParticles2D` in the editor. Which of its settings survive the conversion, and which part of this chapter's property table explains what is lost?

## Doing the same thing in Unity

Unity was not run for this chapter. The comparisons come from Unity's official documentation, checked on 27 September 2026, when the default manual on docs.unity3d.com was Unity 6.6 (6000.6) and 6.7 was in beta.

### Similarities

Unity also has two particle systems split along the same line. The **Built-in Particle System** (the `ParticleSystem` component) is listed for "Thousands" of particles; its particles "can interact with Unity's underlying physics system", and scripts can "read from and write to each particle" ([choosing a particle system](https://docs.unity3d.com/Manual/ChoosingYourParticleSystem.html)). The **Visual Effect Graph** "simulates particle behavior on the GPU, which allows it to simulate many more particles" — "Millions" in the comparison ([VFX Graph](https://docs.unity3d.com/Manual/VFXGraph.html)).

The death burst maps nearly one to one onto the Built-in system's modules ([main module](https://docs.unity3d.com/Manual/PartSysMainModule.html), [emission](https://docs.unity3d.com/Manual/PartSysEmissionModule.html), [ParticleSystem API](https://docs.unity3d.com/ScriptReference/ParticleSystem.html)):

| Godot (this chapter) | Unity Built-in Particle System |
|---|---|
| `one_shot = true` | Main module: Looping off, Duration |
| `lifetime = 0.6` | Main module: Start Lifetime |
| `amount = 32`, `explosiveness = 1` | Emission module: a Burst at time 0, Count 32 |
| `spread`, velocity range | Shape module, Start Speed |
| `scale_curve`, `color_ramp` | Size over Lifetime, Color over Lifetime |
| `restart()` | `Play()`, which "resets its playback time to 0"; also `Stop()`, `Emit(count)`, `Clear()` |
| `finished` | Stop Action = Callback, which sends `OnParticleSystemStopped` to scripts on the GameObject |
| `preprocess` | Prewarm (only with Looping on) |
| sub-emitters | Sub Emitters module: Birth, Collision, Death, Trigger, Manual ([sub emitters](https://docs.unity3d.com/Manual/PartSysSubEmitModule.html)) |

The parenting trap is the same trap: a particle object under a player that is deactivated on death goes with it.

### Differences

- **Inspection.** The Built-in system exposes `isPlaying`, `isEmitting` and `particleCount` ("the current number of particles"). A Unity test can count live CPU particles. Neither of Godot's 2D particle nodes has a method that returns a live count (checked against `ClassDB` on 4.7.2), and the GPU node's `capture_rect()` returned an empty rectangle in our headless run.
- **Trails are CPU-side.** Unity's Built-in (CPU) system has a Trails module ([trails](https://docs.unity3d.com/Manual/PartSysTrailsModule.html)); in Godot, trails exist only on GPU nodes, and not on Compatibility.
- **GPU triggers are events.** VFX Graph effects respond to `OnPlay`/`OnStop` and to custom named events sent from C# with `VisualEffect.SendEvent` ([events](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@17.6/manual/Events.html), [SendEvent](https://docs.unity3d.com/ScriptReference/VFX.VisualEffect.SendEvent.html)). GPU sub-emission uses Trigger Event blocks feeding a GPU Event context, which the package manual marks as experimental ([contexts](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@17.6/manual/Contexts.html)).
- **Requirements.** VFX Graph needs compute-shader support, runs in URP and HDRP only, and "does not support Open GL ES" ([system requirements](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@17.6/manual/System-Requirements.html)). Godot's GPU particles run in all three of its renderers, minus trails and SDF collision on Compatibility.
- **Headless testing.** Tests run from the command line with `-batchmode -runTests -testPlatform PlayMode -testResults <file>` ([test framework command line](https://docs.unity3d.com/Manual/test-framework/reference-command-line.html)); with `-nographics`, "Unity doesn't initialize the graphics device" ([command-line arguments](https://docs.unity3d.com/Manual/EditorCommandLineArguments.html)) — the same boundary as Godot's dummy renderer. Whether the Built-in system simulates and reports `particleCount` under `-nographics` was not checked here; test it before relying on it.

### The agent-workflow angle

With Asset Serialization set to Force Text — the default ([editor settings](https://docs.unity3d.com/Manual/class-EditorManager.html)) — prefabs and scenes are YAML, and each asset's GUID lives in its `.meta` file ([asset metadata](https://docs.unity3d.com/Manual/AssetMetadata.html)). An agent can read and diff a `ParticleSystem`, but every module is serialized, used or not, and a wrong GUID reference fails as quietly as a wrong `ext_resource` path in a `.tscn`. Unity calls its format a custom subset of YAML ([UnityYAML](https://docs.unity3d.com/Manual/UnityYAML.html)), so generic YAML tools are not guaranteed to round-trip it. The practical agent route is a C# script that configures the system, plus a PlayMode test.

| Godot | Unity |
|---|---|
| `GPUParticles2D` / `3D` | Visual Effect Graph (`VisualEffect`) |
| `CPUParticles2D` / `3D` | Built-in Particle System (`ParticleSystem`) |
| `ParticleProcessMaterial` | modules (Built-in) / Initialize and Update contexts (VFX Graph) |
| `one_shot` | Looping off |
| `finished` | `OnParticleSystemStopped` |
| particle shader | VFX Graph blocks and operators |
| `.tscn` text | `.prefab`/`.unity` YAML + `.meta` GUIDs |

## Doing the same thing in Unreal Engine

Unreal Engine was not run for this chapter. The comparisons come from Epic's official documentation, checked on 27 September 2026, when the newest documented version was Unreal Engine 5.8. Unreal's source is available on GitHub to registered users, and its use "is governed by the Unreal Engine End User License Agreement" ([downloading source code](https://dev.epicgames.com/documentation/unreal-engine/downloading-source-code-in-unreal-engine)): source-available, not open source.

### Similarities

**Niagara** "is the primary tool to do visual effects (VFX) inside Unreal Engine 5" ([Niagara](https://dev.epicgames.com/documentation/en-us/unreal-engine/creating-visual-effects-in-niagara-for-unreal-engine)); Cascade is the legacy system, slated in the UE5 migration guide for deprecation and later removal. A Niagara **system** contains **emitters**; each emitter is a stack of **modules** in groups — Emitter Spawn, Emitter Update, Particle Spawn, Particle Update, Event Handler, Render — "processed sequentially from top to bottom" ([overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-niagara-effects-for-unreal-engine)). The burst becomes an Emitter State module with Loop Behavior **Once** (Godot's `one_shot`), a **Spawn Burst Instantaneous** module with a count of 32 (Godot's `amount` with `explosiveness = 1`) ([emitter update reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/emitter-update-group-reference-for-niagara-effects-in-unreal-engine)), particle modules for lifetime, velocity, size and colour, and a Sprite renderer.

The trigger has the same shape. Gameplay code calls **Spawn System at Location** on death ([SpawnSystemAtLocation](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/Niagara/UNiagaraFunctionLibrary/SpawnSystemAtLocation)), or holds a `UNiagaraComponent` and calls `ResetSystem()` or `Activate(true)`; its `OnSystemFinished` delegate is "called when the particle system is done" ([UNiagaraComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/Niagara/UNiagaraComponent)).

### Differences

- **CPU or GPU is a per-emitter setting.** Sim Target "determines whether the simulation is performed on the CPU or the GPU" ([emitter settings](https://dev.epicgames.com/documentation/en-us/unreal-engine/emitter-settings-reference-for-niagara-effects-in-unreal-engine)). On GPU, "the system cannot read how big the effect is. This is why it is necessary to set fixed bounds" ([GPU sprite effect](https://dev.epicgames.com/documentation/en-us/unreal-engine/how-to-create-a-gpu-sprite-effect-in-niagara-for-unreal-engine)) — the problem Godot's `visibility_rect` solves by hand.
- **Events are CPU-only.** Niagara's Location, Death and Collision events are its sub-emitter mechanism, and "events only work with CPU simulation" ([events](https://dev.epicgames.com/documentation/en-us/unreal-engine/events-and-event-handlers-in-niagara-effects-for-unreal-engine)). Godot is the reverse: sub-emitters exist only on GPU nodes.
- **Budgets are assets.** Niagara Effect Types are "reusable assets" that apply scalability per quality level and per platform, including distance culling and instance limits ([scalability](https://dev.epicgames.com/documentation/en-us/unreal-engine/scalability-and-best-practices-for-niagara)). Godot has no equivalent; you write the cap yourself.
- **Debugging.** The Niagara Debugger (Tools > Debug > Niagara Debugger) inspects live simulations, with `fx.Niagara.Debug.*` console variables ([Niagara Debugger](https://dev.epicgames.com/documentation/en-us/unreal-engine/niagara-debugger-for-unreal-engine)).
- **Headless testing.** Automation tests run from the command line with `-ExecCmds="Automation RunTest <name>;Quit"`; `-nullrhi` uses the "null rendering hardware interface to run UE headless" and `-unattended` suppresses dialogs ([command-line arguments](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-command-line-arguments-reference), [running automation tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine)). With no rendering interface, a GPU emitter is as unobservable as Godot's.

### The agent-workflow angle

Here the engines diverge most. A Niagara system is a `.uasset`, and Epic's own source-control page says these files "are binary, so cannot be opened as text or merged in a text-based merge tool" ([Perforce and Unreal](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-perforce-as-source-control-for-unreal-engine)). An agent cannot read or diff the emitter the way it read `main.tscn` in this chapter. It can write the C++ that spawns the system, and it can drive the editor with the Python Editor Script Plugin (editor-only; runnable headless with `-ExecutePythonScript=`) ([Python scripting](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python)). The module stack itself stays an in-editor job, or a scripted one whose result you cannot review as a diff.

| Godot | Unreal Engine 5 |
|---|---|
| particle node | Niagara system + `UNiagaraComponent` |
| process material | Particle Spawn / Particle Update modules |
| `one_shot` | Emitter State: Loop Behavior Once |
| `amount` + `explosiveness = 1` | Spawn Burst Instantaneous |
| GPU vs CPU node | emitter Sim Target |
| `visibility_rect` | fixed bounds (required for GPU sim) |
| `finished` | `OnSystemFinished` |
| sub-emitter (GPU only) | event handler (CPU only) |
| `.tscn` (text) | `.uasset` (binary) |

## Sources

Godot (official documentation, "stable" = 4.7, and engine source at tag `4.7.2-stable`):

- [2D particle systems](https://docs.godotengine.org/en/stable/tutorials/2d/particle_systems_2d.html)
- [3D particle systems](https://docs.godotengine.org/en/stable/tutorials/3d/particles/index.html) and [particle sub-emitters](https://docs.godotengine.org/en/stable/tutorials/3d/particles/subemitters.html)
- [GPUParticles2D class reference](https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html), [CPUParticles2D](https://docs.godotengine.org/en/stable/classes/class_cpuparticles2d.html), [ParticleProcessMaterial](https://docs.godotengine.org/en/stable/classes/class_particleprocessmaterial.html)
- [Particle shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/particle_shader.html)
- [Renderers (feature comparison)](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html)
- [GPU optimization](https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html)
- [Debugger panel (Visual Profiler note)](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_panel.html)
- [Command-line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
- [GDScript basics: lambda functions](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html)
- Engine source: [`core/os/os.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/core/os/os.cpp) (`OS::add_frame_delay`), [`main/main.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/main/main.cpp) (`low_processor_mode_sleep_usec` default 6900; early return when a fixed FPS is set)
- Godot demo projects at commit [`a3b5c113`](https://github.com/godotengine/godot-demo-projects/tree/a3b5c113112f77291d5f3d1360f33a882fdc52f7): `2d/dodge_the_creeps`, `2d/particles`, `3d/particles`, `3d/platformer` (MIT; asset licences as listed in each demo)

Background:

- W. T. Reeves, "Particle Systems—A Technique for Modeling a Class of Fuzzy Objects," *ACM Transactions on Graphics* 2(2), April 1983, 91–108, [doi:10.1145/357318.357320](https://doi.org/10.1145/357318.357320); abstract via the [ACM SIGGRAPH history archive](https://history.siggraph.org/learning/particle-systems-a-technique-for-modeling-a-class-of-fuzzy-objects-by-reeves/)

Course and Walker records:

- `walker-2d-dodge-the-creeps/README.md` and `FRICTIONAL.md` (2026-09-24); `walker-3d-platformer/godot/` scenes
- This chapter's record: [`examples/09-particle-effects/`](../examples/09-particle-effects/)

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation, checked on 27 September 2026:

- Unity: [choosing a particle system](https://docs.unity3d.com/Manual/ChoosingYourParticleSystem.html), [VFX Graph](https://docs.unity3d.com/Manual/VFXGraph.html), [VFX Graph system requirements](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@17.6/manual/System-Requirements.html), [contexts](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@17.6/manual/Contexts.html), [events](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@17.6/manual/Events.html), [VisualEffect.SendEvent](https://docs.unity3d.com/ScriptReference/VFX.VisualEffect.SendEvent.html), [main module](https://docs.unity3d.com/Manual/PartSysMainModule.html), [emission module](https://docs.unity3d.com/Manual/PartSysEmissionModule.html), [sub emitters module](https://docs.unity3d.com/Manual/PartSysSubEmitModule.html), [trails module](https://docs.unity3d.com/Manual/PartSysTrailsModule.html), [ParticleSystem API](https://docs.unity3d.com/ScriptReference/ParticleSystem.html), [command-line arguments](https://docs.unity3d.com/Manual/EditorCommandLineArguments.html), [Test Framework command line](https://docs.unity3d.com/Manual/test-framework/reference-command-line.html), [editor settings](https://docs.unity3d.com/Manual/class-EditorManager.html), [asset metadata](https://docs.unity3d.com/Manual/AssetMetadata.html), [UnityYAML](https://docs.unity3d.com/Manual/UnityYAML.html)
- Unreal Engine: [downloading source code](https://dev.epicgames.com/documentation/unreal-engine/downloading-source-code-in-unreal-engine), [Niagara](https://dev.epicgames.com/documentation/en-us/unreal-engine/creating-visual-effects-in-niagara-for-unreal-engine), [Niagara overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-niagara-effects-for-unreal-engine), [emitter update reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/emitter-update-group-reference-for-niagara-effects-in-unreal-engine), [emitter settings](https://dev.epicgames.com/documentation/en-us/unreal-engine/emitter-settings-reference-for-niagara-effects-in-unreal-engine), [GPU sprite effect](https://dev.epicgames.com/documentation/en-us/unreal-engine/how-to-create-a-gpu-sprite-effect-in-niagara-for-unreal-engine), [events](https://dev.epicgames.com/documentation/en-us/unreal-engine/events-and-event-handlers-in-niagara-effects-for-unreal-engine), [scalability](https://dev.epicgames.com/documentation/en-us/unreal-engine/scalability-and-best-practices-for-niagara), [Niagara Debugger](https://dev.epicgames.com/documentation/en-us/unreal-engine/niagara-debugger-for-unreal-engine), [SpawnSystemAtLocation](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/Niagara/UNiagaraFunctionLibrary/SpawnSystemAtLocation), [UNiagaraComponent](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/Niagara/UNiagaraComponent), [command-line arguments](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-command-line-arguments-reference), [running automation tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine), [Perforce and Unreal](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-perforce-as-source-control-for-unreal-engine), [Python scripting](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python)
