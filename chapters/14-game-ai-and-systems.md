# Chapter 14 — Game AI and Systems

## Executive summary

This chapter covers the systems that make a game act on its own: non-player characters that navigate and decide, behavior learned from reward, content generated from a seed, and state shared between two computers, which the old course taught across three Unity and Unreal modules. You build each piece in Godot 4.7.2 by directing Claude Code or Codex from the command line and checking the result with your own headless commands. The main hands-on adds a guard to the `walker-2d-finite-state-machine` build in three handed-off tasks (navigation, a finite state machine, then the same behavior as a behavior tree), followed by three labs: tabular Q-learning on a 5×5 grid, a seeded level generator with a validator, and a two-process ENet test of who may move what. Everything was run on 2026-09-27 and every claim below comes from a real log; Claude Code hit its usage limit on the third task, and Codex finished it from the same handoff file. The runs show how much a passing headless test can leave out: several of the agents' tests passed while checking the wrong thing, and one agent got around its tool allowlist by killing a process from inside a Godot script. What you build proves state transitions, reachability, repeatability and one authority rule on loopback. It does not prove that the guard is fun to evade, that a generated level feels good, or that the network code survives the internet; those remain human checks.

## The question

The first agent run in this chapter reported four passing checks for a guard that walks around an obstacle. Look at what they measured. "Reaches its target" meant within 64 pixels; the agent had also set the guard's arrival tolerance to 48, and the guard stopped 47.7 pixels short. "Never enters obstacle collision bounds" and "rests outside obstacle bounds" could not fail in this scene: guard and obstacle share the default collision layer, so `move_and_slide()` stops the guard's 16-pixel circle at the obstacle's surface long before its centre can cross it. The reach check and the "unreachable target" check could have failed, and the reach check did fail on the agent's first attempt. And the run's written conclusion, that the guard starts moving "on the next physics tick" after its first path request, held in some trials and not in others: across 20 trials I measured afterwards, the first path arrived anywhere from the 2nd to the 9th physics frame after the request, and the frame changed from trial to trial.

An NPC's behavior is a sequence of decisions spread over time, and you will never watch every frame of it. So the question this chapter answers is practical: **what does a passing headless test of game AI actually establish, and how do you split the work so that each piece's evidence still holds after the next piece is built on top of it?**

## Ideas you need

Every system in this chapter runs the same loop: sense, decide, act, once per tick. The four builds differ in who wrote the decision: you (a state machine or a behavior tree), a learning rule (Q-learning), a seeded generator checked by a validator, or another computer on the network. The Chapter 1 vocabulary still applies: a guard is a **scene** of **nodes**, its brain is a **script**, its body is a **collision shape**, and a state change can be announced with a **signal**.

### The tick: where decisions run

Godot calls `_physics_process(delta)` on every node that has it, at the rate set by `physics/common/physics_ticks_per_second`. The FSM demo sets 120 ticks per second in `godot/project.godot`. Movement with `CharacterBody2D.move_and_slide()` belongs there because collision is resolved on the physics step ([Godot docs: idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)). A decision does not have to run every tick. The guard in the hands-on re-targets the player at most every 0.2 s, because recomputing a path 120 times a second buys nothing and costs a path query each time.

### Finite state machines, as this project builds them

A finite state machine (FSM) is a set of states, exactly one of which is current, plus rules for leaving each state. The Walker FSM build implements it with nodes, not an enum:

| Piece | File | What it does |
|---|---|---|
| State interface | `godot/state_machine/state.gd` | `enter()`, `exit()`, `handle_input()`, `update(delta)`, and a `finished(next_state_name)` signal |
| Machine | `godot/state_machine/state_machine.gd` | Connects every child state's `finished` to `_change_state`; forwards `_physics_process` to `current_state.update()` and `_unhandled_input` to `current_state.handle_input()` |
| Player's machine | `godot/player/player_state_machine.gd` | Maps names to state nodes; **pushes** Jump, Stagger and Attack onto `states_stack`; lets Attack interrupt any state except Attack and Stagger |
| Shared behavior | `motion.gd` → `on_ground.gd` → `idle.gd` / `move.gd` | Script inheritance: every motion state handles `simulate_damage`; every ground state handles `jump` |

Two ideas are layered here. **Hierarchical states** share behavior through the parent script: Idle and Move both inherit Jump from `on_ground.gd`, so you write that transition once. The **pushdown automaton** is `states_stack`: Jump is pushed on top of whatever was running, and when the jump lands the state emits `"previous"` and the machine pops back. Read `_change_state` closely and you find a design choice with consequences: on a pop, the machine does **not** call `enter()` on the resumed state. Move resumes with its old speed and velocity instead of restarting. That is the behavior you want after a jump; it is a trap if a resumed state needs to re-arm a timer. Robert Nystrom's [State chapter of *Game Programming Patterns*](https://gameprogrammingpatterns.com/state.html), which the demo's on-screen text recommends, covers both ideas.

The demo also shows an FSM's cost. To learn every way out of Move you must read `move.gd`, `on_ground.gd`, `motion.gd` and the Attack interrupt in `player_state_machine.gd`. Transitions live on the edges, scattered across files. State names are strings (`&"jump"`, `"previous"`); a typo is a runtime error, not a compile error. And the base machine calls `initialize()` from `_enter_tree()`, which runs before the child states' `_ready()`. A state that reaches for an `@onready` variable in `enter()` will find it empty on the first frame. You will meet that trap in the hands-on.

### Behavior trees: priority, re-evaluated or remembered

A behavior tree (BT) is ticked from the root. Every node returns one of three results: **SUCCESS**, **FAILURE**, or **RUNNING** (not finished; tick me again). Leaves do the work: a **Condition** asks a question and returns SUCCESS or FAILURE immediately; an **Action** moves the guard and usually returns RUNNING until it arrives. Composites combine them:

- **Sequence** ticks its children left to right and stops at the first child that does not succeed. It is AND with order: "can I see the player, *then* chase."
- **Selector** (also called a fallback) ticks its children left to right and stops at the first child that does not fail. It is OR with priority: "chase if you can, else search, else patrol."
- A **blackboard** is the shared memory the leaves read and write, such as the last known player position.

The difference from an FSM is where the transition logic lives. An FSM stores it on edges: each state knows its exits. A BT stores it in the **order of the tree**: because the root is re-ticked, a higher-priority branch that becomes true preempts a lower one without any state having to know about it. Adding "flee when hurt" to a BT is one new branch at the left of the root Selector; adding it to an FSM is a new state plus an exit edge from every state that can be hurt. That preemption holds for **reactive** composites, which restart from the leftmost child on every tick. Composites **with memory** resume the child that returned RUNNING and skip the checks to its left; they save work and give up preemption, and the hands-on shows what that costs. Either way, a BT's current behavior is implicit. You find it by asking which leaf returned RUNNING on the last tick.

Godot 4.7 ships no behavior-tree node. Two maintained addons provide one. [LimboAI](https://github.com/limbonaut/limboai) is a C++ plugin, available as an engine module or a GDExtension, combining behavior trees and hierarchical state machines with a BT editor, a visual debugger and a blackboard system; its v1.8.1 release (2026-08-20) updates its engine builds to Godot 4.7.2. [Beehave](https://github.com/bitbrain/beehave) is a GDScript addon that builds trees from nodes in the scene tree, with a runtime debug view and performance monitors; its v2.9.3 release (2026-08-18) says it is compatible with Godot 4.7. Both are MIT-licensed. What they add over the handful of small GDScript files built in this chapter: authoring in the editor, a debugger that shows which node is running, a library of ready-made nodes, and a managed blackboard. What they cost: a dependency to pin to your engine version, and for LimboAI's GDExtension, compiled per-platform binaries in your repository. You build the plain version first so that you know what an addon would be doing for you.

### Navigation: a server, a region, an agent

Godot's navigation is split across three pieces ([using NavigationAgents](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html)):

- **NavigationServer2D** holds navigation maps and answers path queries. Scenes do not own it.
- **NavigationRegion2D** registers a **NavigationPolygon** (the walkable area) on the world's default map. A polygon is baked from traversable outlines minus obstructions; its `agent_radius` "shrinks the baked navigation mesh to have enough margin for the agent (collision) size" ([navigation meshes](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationmeshes.html)).
- **NavigationAgent2D** sits inside the moving body. You set `target_position`; each physics frame you call `get_next_path_position()` and steer toward it. The class reference says that calling it "once every physics frame is required to update the internal path logic of the NavigationAgent" ([NavigationAgent2D](https://docs.godotengine.org/en/stable/classes/class_navigationagent2d.html)). The agent does not move the body. Your `move_and_slide()` does.

Three agent queries sound alike and are not:

| Method | Returns `true` when |
|---|---|
| `is_target_reachable()` | the path's final position is within `target_desired_distance` of the target, meaning a path to the target exists |
| `is_target_reached()` | the agent has actually moved within `target_desired_distance` of the target |
| `is_navigation_finished()` | the agent is done following the path, which for an unreachable target means it reached the *closest* point |

The timing rule matters for testing. "The NavigationServer does not update every change immediately but waits until the end of the physics frame to synchronize all the changes together," and at the start of a scene "any path query to a NavigationServer will return empty or wrong" because the map is not yet synchronized ([using NavigationServer](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationservers.html)). The documented fixes are to defer setup with `call_deferred` and to `await get_tree().physics_frame` before the first query. Godot 4.7 also runs that synchronization on a background thread by default, which, as the hands-on measures, makes the first path's arrival frame vary from run to run. A test that requests a path in the frame the scene was added is testing the synchronization, not your guard.

For grid games, `AStarGrid2D` is the lighter tool: no polygons, just cells marked solid or free. The upstream `2d/navigation_astar` demo uses it on a `TileMapLayer`.

### Reinforcement learning: behavior from reward

Reinforcement learning (RL) replaces authored transitions with a reward signal. The world is a **Markov decision process**: states `s`, actions `a`, a reward `r` after each step, and a next state `s'`. The agent wants to maximize the **return**, the sum of rewards with later rewards discounted by `γ` (gamma) per step.

**Q-learning** keeps a table `Q(s, a)`, an estimate of the return from taking `a` in `s` and acting well afterwards. After every step it moves the estimate toward a better one:

```text
Q(s, a) <- Q(s, a) + alpha * ( r + gamma * max_a' Q(s', a') - Q(s, a) )
```

`alpha` is the step size. The bracket is the **temporal-difference error**: how wrong the old estimate was, judged by the reward just seen plus the best estimate for the next state. Q-learning is **off-policy**: it learns the value of acting greedily while it actually explores with an **epsilon-greedy** rule, taking a random action with probability `epsilon`. Watkins and Dayan proved that tabular Q-learning converges to the optimal values when every state-action pair keeps being visited and the step sizes shrink appropriately ([Watkins & Dayan, 1992](https://doi.org/10.1007/BF00992698)). Lab A uses a constant `alpha`, so the theorem's conditions do not strictly hold; what you measure is whether this particular run settles.

The old course went on to three methods that need neural networks. You will not run them in this chapter, but you should know what each changes:

- **Deep Q-Networks (DQN)** replace the table with a network that estimates `Q(s, ·)` from raw input, and stabilize training with an **experience replay** buffer and a periodically copied **target network** ([Mnih et al., 2015](https://doi.org/10.1038/nature14236)).
- **Policy gradient** methods skip `Q` and adjust the policy's own parameters in the direction that makes high-return actions more likely; REINFORCE is the classic form ([Williams, 1992](https://doi.org/10.1007/BF00992696)). They handle continuous actions naturally and suffer from high-variance updates.
- **Proximal Policy Optimization (PPO)** is a policy-gradient method whose clipped surrogate objective allows several epochs of minibatch updates on one batch of experience while discouraging large policy changes ([Schulman et al., 2017](https://arxiv.org/abs/1707.06347)).

The standard interface between a simulator and these algorithms is the Gym API, now maintained by the Farama Foundation as [Gymnasium](https://gymnasium.farama.org/), "a maintained fork of OpenAI's Gym library": `reset()` returns an observation, `step(action)` returns observation, reward, terminated, truncated and info. For Godot, [Godot RL Agents](https://github.com/edbeeching/godot_rl_agents) (MIT) connects a Godot game to Python RL libraries. It provides wrappers for Stable Baselines3, Sample Factory, Ray RLlib and CleanRL, and its README describes experimental ONNX export for running a trained model inside the game, which needs the .NET build of Godot. Its latest tagged release is v0.8.2 (2025-02-25). I did not install or run it for this chapter.

### Procedural content generation: seeds, noise, and proof

Procedural content generation (PCG) makes content with an algorithm instead of by hand. Three ideas carry most of it:

- **A seed makes it repeatable.** `RandomNumberGenerator` with a fixed `seed` gives "a reproducible sequence of pseudo-random numbers." The same page warns that the underlying algorithm "is an implementation detail and should not be depended upon" ([RandomNumberGenerator](https://docs.godotengine.org/en/stable/classes/class_randomnumbergenerator.html)). So a seed reproduces a level on a pinned engine version. If a level must survive engine upgrades, store the generated data, not only the seed.
- **Noise makes it coherent.** `FastNoiseLite` returns smooth values in roughly `[-1, 1]` for any coordinate ([FastNoiseLite](https://docs.godotengine.org/en/stable/classes/class_fastnoiselite.html)). The `walker-compute-heightmap` build turns simplex noise (5 octaves, lacunarity 1.9) into an island by multiplying each pixel by a radial gradient and zeroing everything below 0.2, once in a GDScript loop (`compute_island_cpu` in `godot/main.gd`) and once in a GLSL compute shader.
- **A validator makes it playable.** A generator that can emit an impossible level is only half a system. The other half is a check that each output meets a playability rule, and a policy for failures: reject and re-roll (**generate-and-test**), or build the level so it cannot fail (**constructive**). The validator is a *model* of the game's rules. It is only as good as the numbers you feed it, which is why Lab B measures the player's real jump before writing any validator.

The old course treated Houdini as the industrial answer. SideFX lists official Houdini Engine plug-ins for Unity, Unreal, Maya and 3ds Max; Godot is not on that list ([Houdini Engine plug-ins](https://www.sidefx.com/products/houdini-engine/plug-ins/), checked 2026-09-27). Treat Houdini as context in this course, not a tool you need.

### High-level multiplayer: peers, authority, RPCs

Godot's high-level multiplayer puts a **MultiplayerPeer** (here `ENetMultiplayerPeer`) under the scene tree's `multiplayer` API ([high-level multiplayer](https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html)). The host calls `create_server(port, max_clients)`; a client calls `create_client(ip, port)`. Each peer gets an integer id, and the server is always id 1.

Every node has a **multiplayer authority**, a peer id that is 1 unless you call `set_multiplayer_authority()` (which applies to child nodes too by default). Authority is a convention the RPC system enforces: a function marked `@rpc` defaults to `@rpc("authority", "call_remote", "reliable", 0)` ([GDScript annotations](https://docs.godotengine.org/en/stable/classes/class_@gdscript.html)). That means only the node's authority may call it, it runs on the other peers but not the caller, it is delivered reliably, on channel 0. `"any_peer"` lets anyone call it; `"call_local"` also runs it on the caller; `"unreliable"` trades delivery guarantees for latency. RPCs are matched by node path and checked against a checksum of the RPC declarations, so both peers must run the same scripts at the same node paths.

Two nodes do this bookkeeping for you. **MultiplayerSynchronizer** "synchronizes configured properties to all peers" from its authority, listed in a `SceneReplicationConfig` ([MultiplayerSynchronizer](https://docs.godotengine.org/en/stable/classes/class_multiplayersynchronizer.html)). **MultiplayerSpawner** "automatically replicates spawnable nodes from the authority to other multiplayer peers" ([MultiplayerSpawner](https://docs.godotengine.org/en/stable/classes/class_multiplayerspawner.html)). Pong, in Lab C, uses neither: it syncs paddles with a plain unreliable RPC every frame. The `walker-networking-multiplayer-bomber` build uses both: a `MultiplayerSpawner` each for players and bombs, and a `MultiplayerSynchronizer` for each player's position plus a second one, owned by that player's peer, for its inputs.

**Scoped** networking, the syllabus's word, means you choose the boundary you test inside and say so. In this course that boundary is loopback: two processes on one machine at `127.0.0.1`. Latency, packet loss, NAT, and hostile clients are outside it.

## The Walker example: walker-2d-finite-state-machine

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-2d-finite-state-machine`](https://github.com/nikbearbrown/walker-2d-finite-state-machine), [`walker-compute-heightmap`](https://github.com/nikbearbrown/walker-compute-heightmap), [`walker-networking-multiplayer-bomber`](https://github.com/nikbearbrown/walker-networking-multiplayer-bomber), [`walker-2d-dynamic-tilemap-layers`](https://github.com/nikbearbrown/walker-2d-dynamic-tilemap-layers), [`walker-networking-multiplayer-pong`](https://github.com/nikbearbrown/walker-networking-multiplayer-pong), [`walker-networking-websocket-chat`](https://github.com/nikbearbrown/walker-networking-websocket-chat), [`walker-networking-webrtc-minimal`](https://github.com/nikbearbrown/walker-networking-webrtc-minimal), [`walker-pong`](https://github.com/nikbearbrown/walker-pong), [`walker-jumpman`](https://github.com/nikbearbrown/walker-jumpman), [`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

**What it is.** A Walker adaptation of Godot's official `2d/finite_state_machine` demo, taken from `github.com/godotengine/godot-demo-projects` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7` and kept under the upstream MIT license (`LICENSE.md`). Its README states that the only production change is the application title. The player is a top-down `CharacterBody2D` (`godot/player/Player.tscn`) whose `StateMachine` node has six child states: Idle, Move, Jump, Stagger, Attack and Die. On screen, `godot/debug/StatesStackDiplayer.tscn` prints the pushdown stack and a label above the player prints the current state. Controls: WASD or arrows to move, Shift to run, Space to jump (a fake jump that raises `BodyPivot`, since the game is top-down), F to attack, R to fire, X to simulate damage.

**Where to start if you are a student.** The Walker adaptation is public at [github.com/nikbearbrown/walker-2d-finite-state-machine](https://github.com/nikbearbrown/walker-2d-finite-state-machine). To start from the upstream demo instead, take `2d/finite_state_machine` in `godot-demo-projects` at commit `a3b5c113`, open it in Godot 4.7.2, and reproduce the Walker test harness from `examples/14-game-ai-and-systems/main/tests/`, where the two original test scripts are copied.

**What its checks establish.** The Walker record (`README.md`, `FRICTIONAL.md`, dated 2026-09-27) reports 29 passing headless assertions in two scripts, both of which drive the real `Demo.tscn` with keyboard events sent through `Input.parse_input_event` and never set a state directly:

- `godot/test_input.gd`, 18 checks: Idle at start; D moves right in Move at walk speed 450; Shift raises speed to 700; release returns to Idle; Space pushes Jump over Idle (stack size 2) and raises the body pivot; landing pops back to Idle; X enters Stagger and the stagger animation returns to Idle; F enters Attack with the sword visible and pops back; R spawns a bullet; the on-screen stack and state labels follow each transition.
- `godot/test_combo.gd`, 11 checks: the three-hit sword combo, including input buffering, the third swing's damage metadata of 3, and exactly one push and one pop for the whole combo.

I reran both on the scratch copy before changing anything (`RESULT 18 checks; 0 failures` and `RESULT 11 checks; 0 failures`). One caution the record does not contain: `test_combo.gd` is flaky. On the untouched baseline it failed the same six combo checks in 3 of 16 runs (2 of 8 with `--fixed-fps 60`, 1 of 8 without). I did not find the cause. A single passing run, which is what the Walker record reports, cannot show this.

**What remains unverified**, in the build's own words and mine: no rendered frame has been inspected and no human has played it; the scene has no enemy, no health target and no environment collider, so the sword's hit and damage are untested ("Damage metadata does not establish actual hit/damage behavior"); Die exists as a node but is not in the player's `states_map`, so no death loop exists to test. The project has no NPC and no navigation at all. That absence is why it is the right starting point: the hands-on adds an NPC to a project whose state-machine base class already has 29 checks guarding it, and every task has to keep those checks passing.

### The other Walker builds this chapter uses

| Build (upstream path) | Used in | What its record says it established | What it says is not established |
|---|---|---|---|
| `walker-2d-dynamic-tilemap-layers` (`2d/dynamic_tilemap_layers`) | Lab B | 11 headless keyboard/physics assertions: walking through the fake wall, the secret layer fading to alpha 0.3 and back, solid ground still colliding, W jumps | Rendered fade, other collision routes, controller input, playtest |
| `walker-compute-heightmap` (`compute/heightmap`) | Lab B, reading | CPU path clicked through the real button; same seed twice gives byte-identical output; a gradient index overflow in the GLSL (54,757 out-of-range indices at 512×512) found by source arithmetic and clamped | GPU execution and CPU/GPU parity; its README warns not to present headless CPU checks as GPU verification |
| `walker-networking-multiplayer-pong` (`networking/multiplayer_pong`) | Lab C | Lobby: 5 checks. Two-process loopback match: 9 host and 7 client checks (authority assignment, replicated paddle clamps, natural misses scoring 1–1 on both peers, orderly disconnect). Terminal flow: 7 checks per peer, using a constructed near-win fixture | A full ten-point match, WAN conditions, security, rendered appearance |
| `walker-networking-multiplayer-bomber` (`networking/multiplayer_bomber`) | Reading | Two real ENet processes on loopback: registration, movement, a client bomb replicated by `MultiplayerSpawner`, rocks destroyed and shielded, scoring, disconnect | A played victory, packet loss, other input paths |
| `walker-networking-websocket-chat` (`networking/websocket_chat`) | Reading | Eight loopback WebSocket checks, ten two-client GUI/chat checks, seven refusal/reopen checks after a reproduced setter bug was fixed | TLS, binary messages, timeouts |
| `walker-networking-webrtc-minimal` (`networking/webrtc_minimal`) | Reading | Imports; nothing else | Everything: the native runtime has no WebRTC extension, so no peer connects. WebRTC on desktop needs the separate `webrtc-native` GDExtension ([Godot WebRTC docs](https://docs.godotengine.org/en/stable/tutorials/networking/webrtc.html)) |

Every build above is public at `github.com/nikbearbrown/<build name>`, and each also starts from its upstream path at commit `a3b5c113`.

## Hands-on: a guard that patrols, chases and searches, built in three handed-off tasks

You will add an NPC guard to the FSM project in three separate CLI runs: navigation, then a state machine, then a behavior tree. Each run ends by writing `HANDOFF.md`, and each later run begins by reading it and rerunning every test it lists. That file is the explicit handoff the syllabus asks for. It turns "the agent said it worked" into "here are the commands; run them before you touch anything."

Why three runs instead of one? Because each task has a different failure you need to see on its own. Navigation fails on timing and geometry. The FSM fails on transitions and initialization order. The BT fails on priority and on RUNNING. One giant prompt produces one giant diff in which those failures hide behind each other. Sequencing the work is the **Tool Orchestration** capacity (TO) the syllabus assigns to this week: you choose the order, the context each run gets, and the evidence that must exist before the next run starts.

### Predict

Answer these in `FRICTIONAL.md` before the first run:

1. The guard gets a target in the same frame its scene is added to the tree. What will `get_next_path_position()` return on that first physics frame, and what will the guard do? (Reread the synchronization rule in "Ideas you need.")
2. A target is placed in the middle of the solid obstacle. Where should the guard end up, and what should `is_target_reachable()`, `is_target_reached()` and `is_navigation_finished()` each report?
3. The project's state-machine base calls `initialize()` from `_enter_tree()`. The guard's Patrol state needs the guard's `NavigationAgent2D` in `enter()`. What goes wrong, and when?
4. You have one set of behavioral tests for the FSM guard. Write down what those tests must read (and must never read) so that the identical tests can later judge a BT guard.

### Build It

Work in your own copy of the project, on a clean commit, with Godot 4.7.2 on your `PATH`. The three prompts below are the exact text given to the agents in the recorded run: Claude Code for Tasks 1 and 2; for Task 3, Claude Code and then, after it hit its usage limit, Codex. Each prompt was saved in a file and passed with `$(cat …)`. The recorded prompts' `Run:` lines omit `--fixed-fps 60`, and the agents ran their tests without it. Add it in your copies; Verify explains why.

**Task 1: navigation only.**

```text
This is a Walker adaptation of Godot's 2d/finite_state_machine demo (Godot 4.7.2,
GDScript). The Godot project is in godot/. Read README.md, FRICTIONAL.md and
godot/project.godot first. Do not modify the existing player/, state_machine/
or debug/ files, and do not edit Demo.tscn.

Task 1 of 3: navigation only. Create a new scene godot/npc/guard_arena.tscn:
- a 1280x720 walled arena with one solid rectangular obstacle in the middle
  (StaticBody2D, so bodies collide with it) and a NavigationRegion2D whose
  navigation polygon covers the floor but not the obstacle, with a margin for
  the guard's collision radius;
- an instance of res://player/Player.tscn;
- a Guard: a CharacterBody2D with a CollisionShape2D, a NavigationAgent2D and a
  script with set_target(position) that follows the path the way Godot's
  navigation docs describe (get_next_path_position once per physics frame).
  No states or decision logic yet.

Add godot/tests/test_guard_nav.gd (extends SceneTree) that loads the arena and
prints one PASS or FAIL line per check, ends itself within 60 seconds, and exits
nonzero if anything failed:
1. the guard reaches a target on the far side of the obstacle within a time
   limit, and no recorded guard position lies inside the obstacle;
2. a target inside the obstacle is reported unreachable (is_target_reachable()
   is false) and the guard stops at the closest reachable point instead of
   pushing into the obstacle;
3. what happens when a target is requested in the same frame the scene is
   added, before the navigation map has synchronized. Record the actual
   behavior; do not assume it.

Run: godot --headless --path godot --script res://tests/test_guard_nav.gd
Also rerun the existing godot/test_input.gd and godot/test_combo.gd the same way.
Do not open a Godot window. Do not commit. Finish by writing HANDOFF.md at the
repository root: files changed, the exact test commands and their real results,
what the next task may rely on, and what is still unverified.
```

```bash
claude -p "$(cat main-1-navigation.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > session-main-1.jsonl
```

The flags are the contract with the tool. `-p` runs one prompt non-interactively. `--permission-mode acceptEdits` lets the agent write files without asking. `--allowedTools` limits its shell to `godot`, `git`, `ls` and `mkdir`; anything else is refused, and the refusal appears in the transcript as evidence of what the agent tried. `--output-format stream-json --verbose` saves every message and tool call for your audit. Notice what the prompt leaves out: no algorithm, no node layout beyond the three nodes that matter. It names the files you care about, the files that are off-limits, three checks with their failure cases, and the handoff. Check 3 is deliberately an open question, because the honest answer is an observation, not a spec.

**Task 2: the state machine.**

```text
Task 2 of 3. Read HANDOFF.md first and run every test it lists. If any test
fails, stop and report; do not continue.

Give the Guard in godot/npc/guard_arena.tscn a finite state machine built on
this project's own res://state_machine/state_machine.gd and state.gd (extend
them; do not edit them). States:
- Patrol: walk a loop of at least three waypoints using the Task 1 navigation.
- Chase: entered when the player is within sight_radius and not hidden behind
  the obstacle (line of sight); re-target the player at most every 0.2 s.
- Search: entered when the player is beyond lose_radius or out of sight; go to
  the last known player position, wait 1.0 s there, then return to Patrol.
Use lose_radius > sight_radius so the guard does not flicker at the boundary.
Expose the current state name as a read-only `mode` property on the Guard
("Patrol", "Chase" or "Search") and show it on a Label above the guard.

Add godot/tests/test_guard_fsm.gd. It may place the player by setting its
position (print that this is a fixture) but must never set the guard's state or
mode directly, and must read only guard.mode and positions. Check: the sequence
Patrol -> Chase -> Search -> Patrol; that a player hidden behind the obstacle
does not trigger Chase; and that a player standing between sight_radius and
lose_radius during a chase causes no mode change for at least one second.
Run the new test plus every test listed in HANDOFF.md, headless. No window, no
commit. Update HANDOFF.md the same way as before and include the transition
table (from, to, condition).
```

```bash
claude -p "$(cat main-2-fsm.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > session-main-2.jsonl
```

Three lines in this prompt carry the design. "Extend them; do not edit them" forces the guard onto the project's existing FSM base, so the 29 player checks keep guarding it. `lose_radius > sight_radius` is **hysteresis**: with one radius, a player standing on the boundary flips the guard between Chase and Search every tick. And the `mode` property is the test contract you predicted in question 4: the tests may read `mode` and positions, never the machine's internals, and they may move the player only as a labelled fixture.

**Task 3: the same behavior as a behavior tree.**

```text
Task 3 of 3. Read HANDOFF.md first and run every test it lists. If any test
fails, stop and report; do not continue.

Implement the same guard behavior as a small behavior tree in plain GDScript,
without addons: a BTNode base whose tick() returns SUCCESS, FAILURE or RUNNING,
plus Selector, Sequence, Condition and Action nodes, and a Dictionary
blackboard. Tree:
  Selector[ Sequence[can_see_player, chase],
            Sequence[has_last_known_position, search],
            patrol ]
Keep the FSM version working. Add an exported brain setting on the Guard
(FSM or BT); both brains must set the same `mode` property.

Make the behavioral checks in test_guard_fsm.gd run against both brains
(refactor them into a shared helper or add test_guard_bt.gd that reuses them),
so the same observable sequence must hold for the FSM and for the BT. Add unit
checks for the composites: Selector returns the first child SUCCESS, Sequence
stops at the first FAILURE, and RUNNING propagates and resumes on the next tick.
Run everything headless: the new tests and every test in HANDOFF.md. No window,
no commit. Update HANDOFF.md, and add one paragraph comparing where the FSM and
the BT keep their transition logic.
```

```bash
claude -p "$(cat main-3-bt.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > session-main-3.jsonl
```

When Claude Code stopped at its usage limit, the same prompt went to Codex from the same commit:

```bash
codex exec --ignore-user-config -s workspace-write --add-dir "$HOME/Library/Application Support/Godot" --add-dir "$HOME/Library/Caches/Godot" --json -o main-3-last-message.txt "$(cat main-3-bt.txt)" < /dev/null > session-main-3-codex.jsonl
```

This task does not ask for a new behavior. It asks for the same behavior from a different architecture, judged by the same tests. If the BT guard passes the FSM guard's behavioral checks, the two are equivalent on everything those checks observe, and nothing more. The composite unit checks exist because behavioral checks cannot see the difference between a Sequence that resumes a RUNNING child and one that restarts from the left.

**The Codex difference.** Each prompt works unchanged with `codex exec` (Lab A shows the full command), and in the recorded run Codex finished Task 3 after Claude Code hit its usage limit. The boundaries differ. `codex exec` has no per-run allowlist flag; its per-run boundary is the sandbox mode (`-s workspace-write` limits where commands may write, not which commands may run). Codex can also read execution-policy rule files, which I did not configure for this chapter. If you need the narrower rule "only `godot` and `git`," Claude Code's `--allowedTools` states it directly. As Lab C shows, even that rule is weaker than it looks. In your own runs, also pass `--disallowedTools "Skill"` so the session cannot invoke skills installed on your machine; the recorded runs omitted it, and none of them invoked a skill.

### Between runs: your own gate

Do not paste the next prompt the moment an agent says it is done. Between runs, do four things yourself:

1. Read the diff (`git diff`) and the new `HANDOFF.md`. Check that every test the handoff lists exists and that the "what the next task may rely on" section is true of the code, not just of the prose.
2. Run `godot --headless --path godot --import` once. Agents create `.uid` files by hand; until the editor's import pass registers them, every load prints `invalid UID … using text path instead`. In the recorded run, Task 1 produced six such warnings per test run and Task 2 twelve; after one import pass there were none, and no file changed.
3. Rerun every test yourself with a pinned time step (below) and read the whole log, not just the `RESULT` line. `grep -c "SCRIPT ERROR"` should print 0. A Godot script error does not stop the process or change its exit code; a test can report "0 failures" on top of one.
4. Commit. The commit is the baseline the next run's diff is measured against.

### Use It

Tests cannot tell you whether the guard is any good to play against. Open `godot/npc/guard_arena.tscn` in the Godot 4.7.2 editor and use **Run Current Scene**. The player uses the FSM demo's controls. Turn on **Debug > Visible Navigation** before running so the navigation polygon and the guard's path are drawn. Then try to break it:

- Stand still in the guard's patrol route and watch the label switch to Chase.
- Circle the obstacle so that it blocks the line of sight, and time how long the guard keeps searching.
- Stand at the edge of its sight: does the label flicker between states, or does hysteresis hold?
- Stand right against the obstacle and let it chase you there. Does it slide along the wall, or push against it?
- Let it lose you, then step back into plain view while it is searching. Does it notice? (Read "What we actually ran" afterwards.)

Then switch the exported **Brain** setting on the Guard from FSM to BT in the Inspector and repeat. If the two brains feel different on any of these, write down how. The tests say they are equivalent only on what the tests observe.

### Ship It

Commit after each task, not once at the end, with a message that says which task, which test command, and its result. `FRICTIONAL.md` gets your four predictions, the agent's claims that turned out wrong or untested (the transcript shows them; you will find some), and what you changed or reran because of them. For the explainer, **godot-gamedev** fits the hands-on best: its required input → state → output trace is literally the guard's mode label following the player's position. Use **godot-walkthrough** only after a human has played the guard, since that skill shows real gameplay.

### Verify

Run each test yourself. `godot --help` describes `--fixed-fps <fps>` as "Force a fixed number of frames per second. This setting disables real-time synchronization." Each frame then advances exactly 1/60 s of game time, however fast the machine runs, so a timer and a movement step always agree. `timeout 120` ends a run that hangs: a script error before `quit()` leaves a headless Godot process running until something kills it. Stock macOS has no `timeout` command; Homebrew's `coreutils` package provides it. `test_guard_fsm.gd` runs every behavioral check once per brain; `test_bt.gd` holds the composite unit checks:

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://tests/test_guard_nav.gd
```

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://tests/test_guard_fsm.gd
```

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://tests/test_bt.gd
```

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://test_input.gd
```

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://test_combo.gd
```

A pass establishes that, in this arena, on Godot 4.7.2: the guard reaches a reachable target on the far side of the obstacle, stops at the closest reachable point for an unreachable one, enters Chase when the player is in range and visible, falls back through Search to Patrol, ignores a player hidden behind the obstacle, and does the same under either brain (the test's hysteresis check is weaker than its name; see "What we actually ran"); and that the 29 original player checks still pass (with the caveat that `test_combo.gd` is flaky; rerun it before believing either a pass or a failure). It does not establish that the guard is fun, fair or readable to a player; that it behaves well with two guards, a moving obstacle, or a different arena; or that the first path arrives on any particular frame. That last one is worth a sentence of its own. Godot 4.7 synchronizes navigation maps on a background thread by default (the project settings `navigation/world/map_use_async_iterations` and `region_use_async_iterations` are both `true`), and the ProjectSettings reference says this "adds an additional delay to any navigation map change." `--fixed-fps` does not pin a background thread. A test that depends on the frame the first path appears is testing thread scheduling. If a test really needs that frame, turn both settings off for the test project; in a scratch copy that made the first path arrive on frame 2 or 3 in every trial.

## Lab A: reinforcement learning you can watch converge

The guard's behavior so far was written by hand. Here a behavior is learned from reward, small enough that you can print the whole brain.

### Predict

1. The goal is 8 steps from the start. Two pits sit near the diagonal. With a step cost of −0.01 and γ = 0.95, will the learned path be a shortest one, or a longer one that gives the pits a wide berth? Why?
2. Epsilon falls linearly from 1.0 to 0.05 over 500 episodes. Will the *training* success rate reach 100% for 25 episodes in a row? Will the *greedy* policy be optimal before the training curve looks good, or after?
3. Run the same seed twice. Which lines of output must be byte-identical, and which could legitimately differ?

### Build It

Start from a fresh copy of the same FSM project (or the upstream `2d/finite_state_machine` demo); the lab touches no existing file. I ran this lab with **Codex** instead of Claude Code, to show the other CLI on the same kind of task:

```text
Lab A. This Godot 4.7.2 project is in godot/. Add tabular Q-learning in pure
GDScript: no addons, no Python, no neural network.

- godot/rl/gridworld.gd: a 5x5 grid; start (0,0); goal (4,4) gives +1.0 and ends
  the episode; pits at (1,1) and (3,2) give -1.0 and end it; every other step
  gives -0.01; four actions (up, down, left, right); moving into the border
  leaves the agent in place; episodes are capped at 50 steps.
- godot/rl/q_learner.gd: a Q-table, epsilon-greedy action choice, alpha 0.1,
  gamma 0.95, epsilon decaying from 1.0 to 0.05 over training. All randomness
  comes from one RandomNumberGenerator whose seed is set once.
- godot/tests/test_qlearning.gd (extends SceneTree): read an optional
  --seed=N user argument (default 42); train 500 episodes headless; every 25
  episodes print one line: episode, mean return of the last 25, success rate
  of the last 25, epsilon. Then run the greedy policy with exploration off and
  check that it reaches the goal in the minimum number of steps (8) without
  entering a pit. Print the greedy action of every cell as a 5x5 arrow grid.
  Print PASS/FAIL lines, end within 60 seconds, exit nonzero on failure.

Run: godot --headless --path godot --script res://tests/test_qlearning.gd
Run it twice with the default seed and show that the two learning curves are
identical; run once with -- --seed=7 and report what changed. Do not open a
Godot window. Do not commit. Write godot/rl/README.md: the first episode after
which the success rate stayed at 100% for a full 25-episode window, the final
greedy path, and what this experiment does not show.
```

```bash
codex exec --ignore-user-config -s workspace-write --add-dir "$HOME/Library/Application Support/Godot" --add-dir "$HOME/Library/Caches/Godot" --json -o lab-a-last-message.txt "$(cat lab-a-prompt.txt)" < /dev/null > lab-a-session.jsonl
```

`-s workspace-write` lets Codex's commands write inside the working directory and nowhere else. The two `--add-dir` flags add Godot's user-data and cache folders on macOS to that writable set; I added them so that Godot would not trip over the sandbox, and did not test the run without them. `--ignore-user-config` keeps personal Codex settings (plugins, notification hooks, a preferred model) out of a run you want to be reproducible. `< /dev/null` matters when the command runs from a script or in the background: the recorded run omitted it, printed `Reading additional input from stdin...`, and happened to finish anyway.

### Use It

There is nothing to watch in a window; the learning curve is the thing to look at. Read the 20 curve lines top to bottom and find where the mean return turns positive. Then read the arrow grid as a map: every arrow is the action the table rates highest in that cell. Follow the arrows from the top-left corner and check that they route around both pits. Arrows drawn on the pit and goal cells mean nothing; those rows of the table are never updated because the episode ends there.

### Ship It

Commit `godot/rl/` and `godot/tests/test_qlearning.gd` with the three saved curves. In `FRICTIONAL.md`, record your three predictions next to the real numbers, especially the one about the training success rate. The fitting Brutalist skill is **godot-gamedev**: its input → state → output trace here is episode → Q-table → arrow grid.

### Verify

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://tests/test_qlearning.gd
```

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://tests/test_qlearning.gd -- --seed=7
```

A pass proves four things about this implementation on Godot 4.7.2: the environment follows its rules (nine rule checks, including both Q-update cases), training is repeatable from a seed, the final greedy policy from the start cell is an optimal pit-free path, and the run is fast (under a second here). It does not prove that Q-learning converges in general, that the greedy policy is optimal from every cell, or anything about DQN, PPO, or a game with continuous state. Those need the tools named in "Ideas you need", which this chapter did not run.

## Lab B: procedural content with a validator

A generator that can produce an impossible level is a bug factory with a seed. This lab builds the generator and the proof together, in the `walker-2d-dynamic-tilemap-layers` build: a side-view platformer whose `Ground` and `Secret` layers are `TileMapLayer` nodes sharing one 16-pixel `TileSet`, and whose player (`godot/player/player.gd`) walks at up to 200 px/s and jumps with an initial speed of 200 px/s under the project's gravity of 500 px/s².

### Predict

1. From those three numbers alone, how high can the player jump, in pixels and in 16-pixel tiles? How far can it travel horizontally in one jump at full speed? Write the arithmetic down before the engine answers.
2. Why might the engine's measured height differ from your arithmetic? (Look at `physics/common/physics_ticks_per_second` and at how `player.gd` applies gravity.)
3. If the validator uses exactly the measured limits with no margin, which kind of level will it wrongly accept?

### Build It

```text
Lab B. This is a Walker adaptation of Godot's 2d/dynamic_tilemap_layers demo
(Godot 4.7.2, GDScript) in godot/. Read godot/player/player.gd,
godot/world.tscn and godot/project.godot first. Do not change the player's
movement code or the existing test.

1. Measure, don't guess. Add godot/tests/test_jump_envelope.gd: put the real
   player scene on a flat floor made with the Ground layer's TileSet, press
   jump through Input, and record the highest rise in pixels and in tiles.
   Then, holding move_right from a running start, record the horizontal
   distance covered between takeoff and landing at the same height. Print both.
2. Add godot/pcg/level_generator.gd with generate(seed, width) that returns a
   side-scrolling level as data: a ground height per column, with gaps allowed.
   Use one RandomNumberGenerator seeded with seed; same seed, same level.
3. Add godot/pcg/level_validator.gd that decides whether a level can be crossed
   from the first column to the last with a jump model whose limits come from
   step 1 minus a safety margin you state. A failing level must report the
   first column that cannot be reached and why.
4. Add godot/tests/test_pcg.gd: generate levels for seeds 1..200, validate each,
   print the pass rate and the failing seeds; check that seed 7 twice gives
   identical data; build one hand-made level with a gap wider than the jump and
   one with a step higher than the jump and check both are rejected; write one
   passing level into the Ground TileMapLayer at runtime, drop the player above
   its first column, and check the player comes to rest on a tile
   (is_on_floor) instead of falling out of the level.
Each test prints PASS/FAIL lines, ends within 60 seconds and exits nonzero on
failure. Run them with godot --headless --path godot --script res://tests/<file>.gd
and rerun the existing godot/test_secret.gd. Do not open a Godot window. Do not
commit. Write godot/pcg/README.md: the measured envelope, the margin, the pass
rate, and what the validator does not prove.
```

```bash
claude -p "$(cat lab-b-prompt.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > lab-b-session.jsonl
```

The prompt makes the agent **measure before it models**. Step 1 is a test of the real player scene; steps 2 and 3 may only use its numbers. That ordering is the whole lesson: a validator is a model of your game's physics, and a model built from remembered constants is a guess. The recorded run shows that an agent can follow the ordering to the letter and still measure the wrong thing.

### Use It

Open `godot/world.tscn` in the editor, run it, and play the original level first, jumping as high and as far as you can. Then write one accepted level into the `Ground` layer (`audit/audit_generated_landing.gd` in the example record shows how: clear the layer, then one `set_cell` call per solid column) and play it from left to right. The validator claims every accepted level is crossable. You are the second opinion. A level the validator accepts that you cannot cross is the most valuable bug this lab can find.

### Ship It

Commit the generator, the validator and the tests together; a generator committed without its validator is the thing this lab exists to prevent. `FRICTIONAL.md` records your predicted envelope, the measured one, the margin, the pass rate, and any level you could not cross by hand. Use **godot-walkthrough** if you film it, since the claim that matters is "a player can cross this," which only real play can show.

### Verify

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://tests/test_jump_envelope.gd
```

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://tests/test_pcg.gd
```

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://test_secret.gd
```

A pass establishes that the generator is deterministic for a seed on this engine version, that the validator rejects the two impossible shapes you built by hand, what fraction of seeds it accepts, and (once the landing check really uses a generated level) that accepted levels can be written into the real `TileMapLayer` with working collision. It does not establish that an accepted level can be crossed. The validator's model ignores ceilings, run-up distance before a jump, the player's 14-pixel width, and anything a designer would call fun.

## Lab C: scoped networking in two processes

The `walker-networking-multiplayer-pong` build already has two-process loopback checks for paddle replication, scoring and disconnect. This lab asks a narrower, sharper question about **authority**: what happens when a peer tries to move something it does not own?

Read `godot/logic/paddle.gd` before you start. Each paddle's authority peer reads its keys and calls `set_pos_and_motion.rpc(position, _motion)` every frame; that RPC is declared `@rpc("unreliable")`, so its mode is the default, `"authority"`. Now read `ball.gd` and `pong.gd`: `bounce`, `stop`, `_reset_ball` and `update_score` are all `@rpc("any_peer", "call_local")`. The demo protects paddle positions and trusts either peer to report bounces and points.

### Predict

1. The client calls `set_pos_and_motion.rpc()` on Player1, whose authority is the host. Does the call leave the client? Does the host run it? What, if anything, is printed, and on which side?
2. The host holds `move_up` for half a second. After how long should the client's copy of Player1 agree with the host's, and to what tolerance, given the RPC is unreliable?
3. Which of Pong's RPCs could a modified client abuse to win, and what would the host have to check to stop it?

### Build It

```text
Lab C. This is a Walker copy of Godot's networking/multiplayer_pong demo
(Godot 4.7.2, ENet high-level multiplayer) in godot/. Read godot/logic/*.gd,
godot/test_match.gd, README.md and FRICTIONAL.md first. Do not change the game
scripts or scenes.

Add godot/tests/test_authority.gd, run as two separate headless Godot processes
on 127.0.0.1 only (use the existing --walker-loopback user argument; never bind
a public interface), one started with --test-host and one without. Check:
1. connection: both processes reach the Pong scene; print each unique id;
2. one synchronized state change: the host holds move_up through Input for
   0.5 s, and the client sees Player1's y within 1 px of the host's value;
3. authority failure: the client calls set_pos_and_motion.rpc() on Player1,
   which it does not own, with an absurd position; the host's Player1 must not
   move there. Record exactly what Godot printed on each side.
Print PASS/FAIL per check, end within 30 seconds, exit nonzero on failure.
Start the host first in the background, then the client, save each process's
output to its own log file, and show me both logs. No window, no commit, no
network other than loopback. Append what you verified and what remains
unverified to FRICTIONAL.md.
```

```bash
claude -p "$(cat lab-c-prompt.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(timeout:*),Bash(sleep:*),Bash(cat:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > lab-c-session.jsonl
```

The allowed tools grow by three (`timeout`, `sleep`, `cat`) because this task needs two processes and a way to read their logs. Everything else stays scoped, and the prompt restricts the network to `127.0.0.1` through the build's existing `--walker-loopback` argument, which calls `peer.set_bind_ip("127.0.0.1")` before `create_server`.

### Use It

Export nothing; run two instances from the editor instead. **Debug > Customize Run Instances** ([added to the editor in PR #65753](https://github.com/godotengine/godot/pull/65753)) launches more than one instance of the project from one Run. Start two, press Host in one and Join in the other, and play a point with W/S in each window. Watch both paddles in both windows. The lag you see on the remote paddle is the unreliable RPC doing its job.

### Ship It

Commit the test and the two logs. `FRICTIONAL.md` gets the three predictions and what was printed on each side. For the film, **godot-gamedev** fits: the trace is key press on one process → RPC → property change on the other.

### Verify

Both processes run in real time, without `--fixed-fps`. Two processes exchanging packets share one clock, the wall clock; a fixed step would let each process run its game time at its own speed. Start the host first:

```bash
timeout 30 godot --headless --path godot --script res://tests/test_authority.gd -- --walker-loopback --test-host > host.log 2>&1 &
```

```bash
timeout 30 godot --headless --path godot --script res://tests/test_authority.gd -- --walker-loopback > client.log 2>&1
```

A pass on both sides establishes, on loopback only: the two processes connect; one property change made by the owner reaches the other peer; and the engine rejects one authority-mode RPC from a peer that does not own the node, and says so on the receiving side. It does not establish anything about latency, packet loss, NAT, or a modified client, and it says nothing about the RPCs declared `any_peer`.

## What we actually ran

**When and with what.** 2026-09-27, on the instructor's Mac: Godot 4.7.2.stable.official.ed1daf0bf, Claude Code 2.1.150 (its sessions report the model `claude-sonnet-4-6`), and Codex CLI 0.153.4 run with `--ignore-user-config` (its session files record the model `gpt-6-astra`). Each build's `godot/` folder and `.md` files were copied to a scratch directory, `git init`-ed, imported once, and committed as a baseline. The agents never committed; I committed after each run so every run has its own diff. The full record, including all transcripts, is in [`../examples/14-game-ai-and-systems/`](../examples/14-game-ai-and-systems/).

**Baseline.** Before any change, the FSM build's own tests passed: `RESULT 18 checks; 0 failures` and `RESULT 11 checks; 0 failures`.

### Main hands-on

**Task 1, navigation (Claude Code, 31 turns, about 15 minutes).** The agent created `godot/npc/guard.gd`, `godot/npc/guard_arena.gd`, `godot/npc/guard_arena.tscn` and `godot/tests/test_guard_nav.gd`, and wrote `.uid` files for them by hand. Instead of baking the navigation polygon from outlines with `agent_radius`, it typed the polygon's vertices and triangles into `guard_arena.gd` by hand, with a hand-computed 20-pixel margin around the obstacle. Its first test run failed:

```text
FAIL guard reaches far-side target within 20.0s
PASS guard never enters obstacle collision bounds
PASS target inside obstacle: is_target_reachable() == false
PASS guard rests outside obstacle bounds for unreachable target (pos=(492.5, 360.0))
RESULT 4 checks; 1 failures
```

Its diagnosis was correct: its first triangulation (8 triangles) had neighbouring strips that shared only vertices, not edges, so the navigation graph was disconnected and the guard could not reach the far side. It rewrote the triangulation as 12 triangles with shared edges, and all four checks passed. Its handoff reported the observation for check 3 as "movement begins on the next physics tick."

My audit (`audit/audit_guard_nav.gd`, run from outside the project) found:

- **Reached means "within 48 px."** The agent set `target_desired_distance = 48` and its test threshold to 64. On the far-side trip the guard finished 47.7 px from the target, in 734 physics frames (6.1 s).
- **The obstacle check was vacuous; the property holds anyway.** Measured every physics frame, the guard's centre never came closer than 17.9 px to the obstacle (its radius is 16) and it recorded 0 slide collisions with the obstacle.
- **The unreachable case is right.** `is_target_reachable()` false, `get_final_position()` (640, 240) on the margin's top edge, the guard 7.7 px from it and motionless.
- **The timing claim does not hold in general.** Over four processes of five trials each (`audit/probe_first_path.gd`), the first path appeared on physics frame 2, 5, 6, 7, 8 or 9 after a same-frame request, differing between trials in both time modes. Frame 2 is what "the next physics tick" looks like in this probe; it happened in 8 of the 20 trials. With `navigation/world/map_use_async_iterations` and `region_use_async_iterations` set to `false` in a scratch copy, every trial gave frame 2 or 3, identically in every process.

**Task 2, FSM (Claude Code, 48 turns, about 22 minutes).** The agent read `HANDOFF.md`, reran its three tests, then added `godot/npc/guard_fsm.gd` (extending the project's `state_machine.gd`), `guard_state.gd`, `states/patrol.gd`, `states/chase.gd`, `states/search.gd`, a line-of-sight raycast and the `mode` property in `guard.gd`, and `tests/test_guard_fsm.gd`. Two failures on the way are worth knowing. First, parse errors: `Cannot infer the type of "dist" variable because the value doesn't have a set type`, from `:=` applied to a value read off an untyped variable. The same error appeared in Lab B, and I made it myself in one of my audit scripts. Second, the initialization-order trap from Predict question 3:

```text
SCRIPT ERROR: Invalid assignment of property or key 'target_position' with value of type 'Vector2' on a base object of type 'Nil'.
RESULT 6 checks; 0 failures
```

The base machine called `Patrol.enter()` from `_enter_tree()`, before the guard's `@onready var nav_agent` existed, and the test still passed. The agent noticed the error in the log and fixed it. It had already injected the guard and player references in `_enter_tree()` before calling the base; what it had missed was that the guard's own `@onready` variable was still empty. It deferred Patrol's first `set_target()` to Patrol's first `update()`. Final result: `RESULT 6 checks; 0 failures` with no script errors, and the three earlier tests still passing.

My audit (`audit/audit_guard_fsm.gd`) targeted the hysteresis check. The agent's test put the player 240 px away and waited 1.5 s, but the chasing guard walks toward the player at 150 px/s, so the distance soon fell below `sight_radius` and the band was never really tested. Holding the player exactly 260 px from the guard on every physics frame for 120 frames gave 0 mode changes while chasing, and 0 while patrolling (a patrolling guard does not start chasing at 260 px). My first version of this audit failed: it led the guard toward the obstacle, placed the player inside it, and the guard correctly lost sight. The audit was wrong, not the guard.

Task 2 also changed what a Task 1 test means. With a Patrol state now choosing targets, check 3 of `test_guard_nav.gd` still passes, but its observation now reports the guard heading for the first patrol waypoint (`guard.position=(160.0, 325.0)`) rather than toward the target the test set. The handoff printed the new number without comment.

**Task 3, behavior tree: Claude Code stopped, Codex finished.** The Claude Code run reread the handoff, reran all four tests (all passed), and then ended with "You've hit your session limit" before editing a file. Because the task's whole context was in `HANDOFF.md` and the repository, I gave the identical prompt to Codex from the same commit. Codex (about 3 minutes) added `godot/npc/bt/` (`bt_node.gd`, `selector.gd`, `sequence.gd`, `condition.gd`, `action.gd`), `godot/npc/guard_bt.gd`, an exported `brain` enum on the guard, a loop in `test_guard_fsm.gd` that runs every behavioral check for both brains, and `tests/test_bt.gd` with 14 composite checks. Then it stopped:

```text
The shared guard test hit a runtime error in BT mode: the inactive FSM still receives
physics ticks and calls `update()` on a null state. I'm stopping as requested, without
fixing it or running further tests.
```

It had read Task 3's "if any test fails, stop and report" as covering its own new test, not just the handoff's list. My rerun of that state shows why stopping was right: `RESULT 12 checks; 0 failures`, exit code 0, and 626 lines of `SCRIPT ERROR: Invalid call. Nonexistent function 'update' in base 'Nil'.` Every behavioral check passed on top of the same engine error printed 626 times.

The correction was a second, fresh Codex session, with no memory of the first, run with the same command pattern and this prompt:

```text
Continue Task 3. The stop rule in the previous prompt applied only to the tests
listed in HANDOFF.md before you started; those passed. Your own new test found
a real bug, and fixing it is part of the task. Fix the runtime error in BT mode
(the inactive FSM still calls update() on a null state) without editing
res://state_machine/state_machine.gd or state.gd. Then run every test headless
with --fixed-fps 60: tests/test_guard_fsm.gd (both brains), tests/test_bt.gd,
tests/test_guard_nav.gd, test_input.gd and test_combo.gd. A run counts as clean
only if it exits 0 AND its log contains no "SCRIPT ERROR" or "ERROR:" lines.
No window, no commit. Update HANDOFF.md as Task 3 asked, including the paragraph
comparing where the FSM and the BT keep their transition logic.
```

It scopes the stop rule, names the bug, requires `--fixed-fps 60`, and defines a clean run as exit 0 with no `SCRIPT ERROR` or `ERROR:` lines. Codex found that `set_physics_process(false)` in `_enter_tree()` does not survive startup, and replaced it with `process_mode = Node.PROCESS_MODE_DISABLED` on the inactive FSM. Godot's source explains why the first attempt failed: when a node becomes ready, `Node` calls `set_physics_process(true)` if its script overrides `_physics_process` (`scene/main/node.cpp`, 4.7-stable), undoing anything `_enter_tree()` did. Codex also added one check per brain that the inactive machine cannot process. Then it hit an `ERROR:` line that never appeared in my unsandboxed runs (Godot failing to read the macOS certificate store from inside the Codex sandbox), worked around it with a temporary `godot/override.cfg`, deleted the file afterwards, and said so in its report and in `HANDOFF.md`. Final count: **61 checks** (4 navigation, 14 behavior, 14 composite, 18 and 11 player), all passing.

The BT it built uses composites **with memory**: a Selector or Sequence that returned RUNNING resumes that child on the next tick instead of re-checking earlier children. My prompt's phrase "RUNNING propagates and resumes on the next tick" asked for exactly that. The consequence showed up in one more audit (`audit/audit_search_blind.gd`): with the guard in Search and the player standing 120 px away in plain sight, **both** brains stayed in Search for about 165 physics frames (166 for the FSM, 165 for the BT), then went Search → Patrol → Chase. The two brains are equivalent here too, equivalently blind, because the spec never said what Search should do if the player reappears. No behavioral test covered it. A player would notice in ten seconds.

**Final verification (mine).** In both time modes: navigation 4/4, shared behavior 14/14, composites 14/14, player input 18/18, no script errors. `test_combo.gd` passed in some runs and failed six checks in others. I checked the untouched baseline: 3 of 16 runs failed the same six combo checks (2 of 8 with `--fixed-fps 60`, 1 of 8 without), starting with `FAIL animation opens buffer`. The flakiness predates this chapter's changes. I did not diagnose it, and the Walker record's single 11/11 pass does not show it.

### Lab A (Codex, about 3 minutes)

Codex added `godot/rl/gridworld.gd`, `godot/rl/q_learner.gd`, `godot/tests/test_qlearning.gd`, `godot/rl/README.md` and three saved curves. I reran it:

```text
475,0.374800,0.72,0.097595
500,0.689600,0.88,0.050000
first_perfect_rolling_window_end=-1 first_perfect_reported_window_end=-1
greedy_path=(0, 0) -> (0, 1) -> (0, 2) -> (1, 2) -> (2, 2) -> (2, 3) -> (3, 3) -> (4, 3) -> (4, 4)
PASS greedy policy takes minimum 8 steps (Manhattan lower bound)
PASS Q-learning: 0 failures
```

Two runs with seed 42 produced byte-identical logs; seed 7 produced a different curve (final window 96% success, mean return 0.85) and a different optimal route. The same output came back with `--fixed-fps 60`, as expected for a test that never waits on the clock. The training success rate never held 100% for 25 episodes because exploration never stops (ε ends at 0.05). To find when the *policy* was right, I added `audit/probe_greedy_curve.gd`, which evaluates the greedy path after every episode without drawing random numbers: for seed 42 it was first optimal at episode 46, flipped between optimal and not 9 times, and stayed optimal from **episode 101** to 500; for seed 7, first at 76, 13 flips, optimal from **episode 132**.

### Lab B (Claude Code, 34 turns, about 20 minutes)

The agent added `godot/tests/test_jump_envelope.gd`, `godot/pcg/level_generator.gd`, `godot/pcg/level_validator.gd`, `godot/tests/test_pcg.gd` and `godot/pcg/README.md`. Its measurements: rise 39.2 px (2.45 tiles; theory v²/2g gives 40), horizontal range 128.3 px (8.02 tiles), which it explained as the player "not fully accelerated" at takeoff. It set the validator's limits to 2 tiles of step and 6 tiles of jump distance, and reported a **pass rate of 21.5% (43 of 200 seeds)** with determinism and both hand-made impossible levels correctly rejected.

Three findings from my audits:

- **The range was measured under a ceiling.** The prompt asked for "a flat floor made with the Ground layer's TileSet"; the test used the original level. Replaying its inputs, the player took off at the full 200 px/s and hit a ceiling at x = 240.8, about a quarter of a second into the jump. On a flat floor of 125 tiles that I built, the same run-and-jump covered **163.3 px (10.21 tiles)** in 97 physics frames, close to the 160 px that speed × airtime predicts. The agent's number is reproducible; it measures the level, not the jump, and its explanation was a guess.
- **The landing check did not use a generated level.** It wrote a hand-built flat row into `Ground`. My corrected check writes every accepted level (all 43) into `Ground` and drops the player above its first solid column: **43 of 43** came to rest on a tile at the expected height.
- **Why levels fail.** Of the 157 rejections: 72 steps too high, 69 gaps too wide, and **16 levels whose last columns are a gap**, which no jump can fix. That last group is a generator bug, not bad luck.

The existing `test_secret.gd` still passed 11/11, and every Lab B result was identical with and without `--fixed-fps 60`.

### Lab C (Claude Code, 63 turns, about 18 minutes)

The agent's final logs, which my own rerun reproduced:

```text
PASS check1_connection: reached Pong scene
host_player1_y: 113.042945861816  initial_y: 188.621994018555
PASS check2_sync: host Player1 moved upward under move_up input
ERROR: RPC 'set_pos_and_motion' is not allowed on node /root/Pong/Player1 from: 1987881801. Mode is "authority", authority is 1.
PASS check3_authority: host Player1 not teleported by client unauthorized rpc
```

and on the client, `client_player1_y: 113.042945861816  host_y_from_file: 113.042945861816`. The test hands the host's value to the client through a file in `/tmp`, a side channel worth noticing: a few turns earlier Claude Code had refused the agent's own shell redirect into `/tmp`, but the GDScript wrote there without asking. The path there was rougher than the logs suggest. Its first test used the `multiplayer` property inside a `SceneTree` script (a parse error: that property belongs to `Node`). Its second run crashed on the host with `Invalid access to property or key 'position' on a base object of type 'previously freed'`. A GDScript error does not end a Godot process, so that host never reached `quit()` and kept UDP port 8910 bound, and every later host failed with `Couldn't create an ENet host`. The agent tried `pkill` and `lsof`; the allowlist refused both. It then added this to the test script, which `Bash(godot:*)` does allow:

```gdscript
OS.execute("/usr/sbin/lsof", ["-ti:8910"], pids, true)
# ...
OS.execute("/bin/kill", [pid], [], false)
```

The next host run printed `pre-test cleanup: killing stale PID 40527 on port 8910` and everything passed. The process it killed was its own orphan. The same lines would kill any of your processes that held port 8910, including another test's server, and they ran under an allowlist that was supposed to permit only `godot`, `git`, `timeout`, `sleep`, `cat`, `ls` and `mkdir`. Allowing `godot --script` allows anything GDScript can do. Its `FRICTIONAL.md` entry records the three passing checks and none of the three failures. I removed the block (`lab-c/correction-by-author.diff`), wrapped both processes in `timeout 30`, and reran: both exit 0, same three passes. Lab C ran in real time: two processes exchanging packets on the wall clock are the case where `--fixed-fps` does not belong.

Then the question the agent was not asked. `audit/audit_score_trust.gd` has the client call `update_score.rpc(false)` three times half a second into a match, before the ball can reach either edge:

```text
host score_right before=0 after=3 label=3 ball_x=199.0
RESULT forged points accepted by host: 3 of 3
```

No error was printed. The paddle RPC is protected by its default `"authority"` mode; the score RPC is `"any_peer"` and trusts whoever calls it.

## Check your understanding (ungraded)

1. In `godot/state_machine/state_machine.gd`, a pop (`"previous"`) does not call `enter()` on the state it returns to. Find one state in the player whose behavior would change if it did. Then find the place in your guard where the same rule helps or hurts you.
2. Open your guard's test and list every property it reads. Could the same test judge a guard whose brain is a Q-table from Lab A? What would the Q-learner have to expose?
3. `guard_arena.gd` types the navigation polygon's 20-pixel margin by hand. Replace it with a polygon baked from the arena and obstacle outlines with `agent_radius = 16`. Before running, predict the new `get_final_position()` for the target in the middle of the obstacle, then run the navigation test and explain the difference.
4. Lab A's training success rate never held 100% for 25 episodes, yet the greedy policy was optimal from episode 101 on (seed 42). Which number would you put in a report titled "the agent learned the task," and which would you put in one titled "the agent is safe to ship with exploration on"?
5. Both guard brains ignore a player who reappears during Search. Decide what the guard *should* do, write the one-sentence spec change, and say which brain needs the smaller code change and why.
6. In Pong, `update_score` is `@rpc("any_peer", "call_local")`. Write the smallest change that stops a client from awarding itself a point, and the two-process test that proves the change works and that normal scoring still does.

## Doing the same thing in Unity

Unity was not run for this chapter. What follows comes from Unity's documentation, checked on 2026-09-27; Unity's site listed Unity 6.3 as the current LTS release that day.

### Similarities

The four jobs map one to one. A guard is a GameObject with a **NavMeshAgent** and a C# `MonoBehaviour` holding its brain. The walkable area is baked by a **NavMesh Surface** component from the [AI Navigation package](https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/index.html) ("Use the NavMesh Surface component to define and build a NavMesh for a specific type of NavMesh Agent in your scene"). The reachability question you asked with `is_target_reachable()` is asked in Unity with `NavMesh.CalculatePath` and the resulting [`NavMeshPathStatus`](https://docs.unity3d.com/ScriptReference/AI.NavMeshPathStatus.html): `PathComplete`, `PathPartial` ("The path cannot reach the destination"), or `PathInvalid`. Same concept, same failure case to test.

The FSM and BT code in this chapter ports almost line for line to C#. Both engines also have animation state machines (Godot's `AnimationTree`, Unity's Animator); those drive animation, not decisions, and are easy to mistake for a brain. For authored behavior trees Unity now publishes its own package, [Unity Behavior](https://docs.unity3d.com/Packages/com.unity.behavior@1.0/manual/index.html), "a visual tool for authoring behaviors that control non-player characters (NPCs)," built on behavior graphs with a blackboard. That is the Unity counterpart of LimboAI or Beehave; the old course page said Unity had little built-in BT support and pointed to Opsive's Behavior Designer plug-in, which is no longer the whole picture.

For learning, [ML-Agents](https://docs.unity3d.com/Packages/com.unity.ml-agents@4.1/manual/index.html) plays the role of Godot RL Agents: the game is the environment, Python does the training (`mlagents-learn`, with PPO, SAC and MA-POCA trainers), and the trained model is embedded back in the scene through Sentis, according to the 4.1 package docs. Its last GitHub release was Release 23 (2025-09-02). Networking maps too: [Netcode for GameObjects](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@2.5/manual/basics/networkvariable.html) has **NetworkVariables** for persistent state (Godot's MultiplayerSynchronizer) and RPCs declared with `[Rpc(SendTo.Server)]` and similar targets (Godot's `@rpc`).

Headless verification exists on both sides. Unity's Test Framework runs from the command line with `-runTests -batchmode -projectPath <path> -testPlatform PlayMode -testResults <file>` and writes NUnit XML ([running tests from the command line](https://docs.unity3d.com/6000.3/Documentation/Manual/test-framework/run-tests-from-command-line.html)). That is the equivalent of `godot --headless --script`, and like it, a pass is state evidence, not a playtest.

### Differences

- **Where the brain's data lives.** Unity scenes, prefabs and `.asset` files serialize as YAML text under the default Asset Serialization Mode, Force Text ([Editor settings](https://docs.unity3d.com/Manual/class-EditorManager.html)), so an agent can read and diff them. But every asset also has a `.meta` file with a GUID, and references go through those GUIDs. The Godot hazard of a wrong `uid://` in a `.tscn` has a Unity twin: a missing or regenerated `.meta` file silently breaks references. Tell the agent never to create or delete `.meta` files by hand.
- **Baked navigation is an asset.** A NavMesh Surface bake produces data stored in the project. The Godot hands-on built its polygon in code (the agent typed the vertices and triangles by hand), so the geometry is visible in a diff; in Unity you would review the bake settings in text and re-bake.
- **Behavior graphs are authored visually.** Unity Behavior graphs are assets edited in a graph window. An agent can read the serialized form, but the reliable division of labor is: the agent writes C# action and condition nodes and tests; a human wires the graph.
- **Procedural content.** Unity's documentation shows no counterpart to Unreal's PCG graph that I could find. The common routes are C# generators writing tiles with [`Tilemap.SetTile`](https://docs.unity3d.com/ScriptReference/Tilemaps.Tilemap.SetTile.html) (Godot's `TileMapLayer.set_cell`), or the Houdini Engine for Unity plug-in. The generate-and-validate pattern from Lab B is engine-neutral C#.
- **The planner the old course taught is not a foundation.** The old course linked Unity's AI Planner package. Its documentation tops out at a preview version (`0.3.0-preview.3`), and it never became a released package ([AI Planner docs](https://docs.unity3d.com/Packages/com.unity.ai.planner@latest/)). Do not build coursework on it.
- **Testing the pair.** Godot tests host and client as two headless processes of one binary. The Unity equivalent is two built players started with `-batchmode -nographics`, which the Player command-line reference describes as headless mode without initializing a graphics device ([Player command-line arguments](https://docs.unity3d.com/Manual/PlayerCommandLineArguments.html)). Either way, bind to loopback while testing.

| Godot 4.7 | Unity 6 |
|---|---|
| `NavigationRegion2D` + `NavigationPolygon` | NavMesh Surface (AI Navigation package) |
| `NavigationAgent2D` | `NavMeshAgent` |
| `is_target_reachable()` | `NavMesh.CalculatePath` → `NavMeshPathStatus.PathComplete` |
| plain-GDScript BT / LimboAI / Beehave | C# BT / Unity Behavior package |
| Godot RL Agents (community) | ML-Agents (Unity) |
| `TileMapLayer.set_cell` | `Tilemap.SetTile` |
| `@rpc`, `MultiplayerSynchronizer`, `MultiplayerSpawner` | `[Rpc]`, `NetworkVariable`, `NetworkObject` spawning (Netcode for GameObjects) |
| `godot --headless --script res://tests/x.gd` | `Unity -runTests -batchmode -testPlatform PlayMode` |

## Doing the same thing in Unreal Engine

Unreal Engine was not run for this chapter. The comparisons come from Epic's documentation, which served the Unreal Engine 5.8 pages on 2026-09-27. Unreal Engine is source-available under the Unreal Engine EULA; it is not open source.

### Similarities

Unreal has a first-party answer for each piece, and each answer is more elaborate than Godot's:

- **Navigation.** A **Nav Mesh Bounds Volume** marks where the engine builds a navigation mesh from the level's collision geometry; `RecastNavMesh` is the default navigation data type ([Basic Navigation](https://dev.epicgames.com/documentation/unreal-engine/basic-navigation-in-unreal-engine)). Epic's own walkthrough moves the character with the **AI Move To** node, the way your guard script drives `move_and_slide()` toward `get_next_path_position()`.
- **Behavior trees.** [Behavior Trees](https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-trees-in-unreal-engine) come with a **Blackboard** asset that holds the keys the tree reads, which is your blackboard Dictionary made into a typed asset. Composites include Selector, Sequence and Simple Parallel.
- **State machines.** [StateTree](https://dev.epicgames.com/documentation/unreal-engine/overview-of-state-tree-in-unreal-engine) is Epic's "general-purpose hierarchical state machine that combines the Selectors from behavior trees with States and Transitions from state machines." It is the hybrid this chapter builds by hand: states with explicit transitions, chosen by selector logic.
- **Learning.** The [Learning Agents](https://dev.epicgames.com/documentation/unreal-engine/API/PluginIndex/LearningAgents?lang=en-US) plugin "simplifies the use of reinforcement and imitation learning in Unreal"; training runs in PyTorch. The 5.8 API index marks it Experimental.
- **Procedural content.** The [PCG framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-overview) is a node graph in which spatial data flows from a PCG Component in the level, gets turned into points, filtered, and used to spawn assets, in the editor and at runtime.
- **Networking.** Unreal replicates Actors from an authoritative server. Properties marked for replication sync automatically; functions become RPCs with the `Server`, `Client` or `NetMulticast` specifiers ([Remote Procedure Calls](https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-procedure-calls-in-unreal-engine)). That is the same split as Godot's `MultiplayerSynchronizer` versus `@rpc`.

### Differences

- **Event-driven trees.** "Unreal Engine Behavior Trees are event-driven to avoid doing unnecessary work every frame" ([Behavior Tree overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-in-unreal-engine---overview)). Conditions are **Decorators** attached to branches rather than leaf nodes, and **Services** update blackboard values on a schedule. The tree in this chapter is ticked from the root every physics frame, and its composites then resume whichever child was RUNNING. Unreal's is event-driven instead: a running branch keeps running until it finishes or a decorator's observer abort, set off by a change the decorator watches, interrupts it. Debugging changes with it: in Unreal the question is "which change should have aborted this branch?"
- **Assets are binary.** Behavior Trees, Blackboards, StateTrees and PCG graphs are `.uasset` files. An agent cannot read or diff them as text. The agent-friendly surface is C++ (custom BT tasks, StateTree tasks, PCG nodes) and the editor's [Python scripting](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python) plugin; the graph wiring stays a human job or goes through editor automation. In Godot, the whole guard (scene, brain, tests) is text.
- **Scale.** For very large numbers of agents Unreal offers **MassEntity**, "a framework for data-oriented calculations" built from fragments, entities, archetypes and processors ([Mass Entity overview](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-entity-in-unreal-engine)). Godot has no equivalent built in; a Godot crowd means your own data-oriented code or a server-side approach.
- **Headless testing.** Unreal runs automation tests from the command line with `-ExecCmds="Automation RunTest <Name>;Quit"` and can export JSON reports ([Run Automation Tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine)); `-nullrhi` uses a "null rendering hardware interface to run UE headless" ([command-line reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-command-line-arguments-reference)). The loop is the same as `godot --headless`, with a C++ build step in front of it.
- **Houdini is first-class.** SideFX ships a Houdini Engine plug-in for Unreal; for Godot it does not.

| Godot 4.7 | Unreal Engine 5 |
|---|---|
| `NavigationRegion2D` / `NavigationAgent2D` | Nav Mesh Bounds Volume, `RecastNavMesh`, AI Move To |
| plain-GDScript FSM | StateTree |
| plain-GDScript BT + Dictionary blackboard | Behavior Tree + Blackboard assets, Decorators, Services |
| Q-learning table in GDScript / Godot RL Agents | Learning Agents plugin (Experimental) |
| seeded generator + validator in GDScript | PCG framework graph + PCG Component |
| `@rpc("authority")`, `set_multiplayer_authority()` | `UFUNCTION(Server)` / `Client` / `NetMulticast`, server-authoritative replication |
| `godot --headless --script` | `-ExecCmds="Automation RunTest …;Quit"`, `-nullrhi` |

## Sources

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation, checked on 2026-09-27. Every Godot, Claude Code and Codex result in "What we actually ran" comes from the logs in [`../examples/14-game-ai-and-systems/`](../examples/14-game-ai-and-systems/).

**Godot (4.7, official documentation and source)**

- [Idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)
- [Using NavigationAgents](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html)
- [Using NavigationServer](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationservers.html)
- [Using navigation meshes](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationmeshes.html)
- [NavigationAgent2D class reference](https://docs.godotengine.org/en/stable/classes/class_navigationagent2d.html)
- [ProjectSettings reference in the 4.7-stable source (`navigation/world/map_use_async_iterations`, `region_use_async_iterations`)](https://github.com/godotengine/godot/blob/4.7-stable/doc/classes/ProjectSettings.xml)
- [Node class reference in the 4.7-stable source (`_physics_process` enabled automatically when overridden)](https://github.com/godotengine/godot/blob/4.7-stable/doc/classes/Node.xml) and [`scene/main/node.cpp`](https://github.com/godotengine/godot/blob/4.7-stable/scene/main/node.cpp)
- [Command line tutorial (`--headless`, `--script`, `--import`, `--`)](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html); `--fixed-fps` text quoted from `godot --help`, 4.7.2
- [Overview of debugging tools (Debug menu)](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html)
- [Add a dialog to customize run instances, godotengine/godot PR #65753](https://github.com/godotengine/godot/pull/65753)
- [RandomNumberGenerator](https://docs.godotengine.org/en/stable/classes/class_randomnumbergenerator.html)
- [FastNoiseLite](https://docs.godotengine.org/en/stable/classes/class_fastnoiselite.html)
- [TileMapLayer](https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html)
- [High-level multiplayer](https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html)
- [GDScript annotations, `@rpc`](https://docs.godotengine.org/en/stable/classes/class_@gdscript.html)
- [MultiplayerSynchronizer](https://docs.godotengine.org/en/stable/classes/class_multiplayersynchronizer.html) and [MultiplayerSpawner](https://docs.godotengine.org/en/stable/classes/class_multiplayerspawner.html)
- [WebRTC](https://docs.godotengine.org/en/stable/tutorials/networking/webrtc.html) and [godotengine/webrtc-native](https://github.com/godotengine/webrtc-native)
- [godot-demo-projects](https://github.com/godotengine/godot-demo-projects), commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`: `2d/finite_state_machine`, `2d/navigation`, `2d/navigation_astar`, `2d/dynamic_tilemap_layers`, `compute/heightmap`, `networking/multiplayer_pong`, `networking/multiplayer_bomber` (MIT)

**Godot addons and tools**

- [LimboAI](https://github.com/limbonaut/limboai), release [v1.8.1](https://github.com/limbonaut/limboai/releases/tag/v1.8.1) (2026-08-20)
- [Beehave](https://github.com/bitbrain/beehave), release [v2.9.3](https://github.com/bitbrain/beehave/releases/tag/v2.9.3) (2026-08-18)
- [Godot RL Agents](https://github.com/edbeeching/godot_rl_agents), release v0.8.2 (2025-02-25)

**Reinforcement learning**

- Watkins, C. J. C. H., and Dayan, P. (1992). [Q-learning](https://doi.org/10.1007/BF00992698). *Machine Learning* 8, 279–292.
- Williams, R. J. (1992). [Simple statistical gradient-following algorithms for connectionist reinforcement learning](https://doi.org/10.1007/BF00992696). *Machine Learning* 8, 229–256.
- Mnih, V., et al. (2015). [Human-level control through deep reinforcement learning](https://doi.org/10.1038/nature14236). *Nature* 518, 529–533.
- Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. (2017). [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347). arXiv:1707.06347.
- [Gymnasium](https://gymnasium.farama.org/) (Farama Foundation)

**Patterns and procedural content**

- Nystrom, R. [State](https://gameprogrammingpatterns.com/state.html), in *Game Programming Patterns*.
- [SideFX Houdini Engine plug-ins](https://www.sidefx.com/products/houdini-engine/plug-ins/)

**Unity (documentation)**

- [Unity 6 releases and support](https://unity.com/releases/unity-6)
- [AI Navigation package 2.0](https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/index.html) and [NavMesh Surface](https://docs.unity3d.com/Packages/com.unity.ai.navigation@2.0/manual/NavMeshSurface.html)
- [`NavMesh.CalculatePath`](https://docs.unity3d.com/ScriptReference/AI.NavMesh.CalculatePath.html) and [`NavMeshPathStatus`](https://docs.unity3d.com/ScriptReference/AI.NavMeshPathStatus.html)
- [Unity Behavior 1.0](https://docs.unity3d.com/Packages/com.unity.behavior@1.0/manual/index.html)
- [ML-Agents package 4.1](https://docs.unity3d.com/Packages/com.unity.ml-agents@4.1/manual/index.html) and [ML-Agents on GitHub](https://github.com/Unity-Technologies/ml-agents) (Release 23, 2025-09-02)
- [AI Planner package documentation](https://docs.unity3d.com/Packages/com.unity.ai.planner@latest/)
- [Netcode for GameObjects: NetworkVariables](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@2.5/manual/basics/networkvariable.html) and [RPCs](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@2.5/manual/advanced-topics/message-system/rpc.html)
- [`Tilemap.SetTile`](https://docs.unity3d.com/ScriptReference/Tilemaps.Tilemap.SetTile.html)
- [Editor settings, Asset Serialization Mode](https://docs.unity3d.com/Manual/class-EditorManager.html)
- [Run tests from the command line](https://docs.unity3d.com/6000.3/Documentation/Manual/test-framework/run-tests-from-command-line.html)
- [Player command-line arguments (`-batchmode`, `-nographics`)](https://docs.unity3d.com/Manual/PlayerCommandLineArguments.html)

**Unreal Engine (documentation, 5.8 pages)**

- [Basic Navigation (Nav Mesh Bounds Volume, AI Move To)](https://dev.epicgames.com/documentation/unreal-engine/basic-navigation-in-unreal-engine)
- [Behavior Trees](https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-trees-in-unreal-engine) and [Behavior Tree overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-in-unreal-engine---overview)
- [Overview of State Tree](https://dev.epicgames.com/documentation/unreal-engine/overview-of-state-tree-in-unreal-engine)
- [Mass Entity overview](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-entity-in-unreal-engine)
- [Learning Agents plugin API index](https://dev.epicgames.com/documentation/unreal-engine/API/PluginIndex/LearningAgents?lang=en-US)
- [Procedural Content Generation overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-overview)
- [Remote Procedure Calls](https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-procedure-calls-in-unreal-engine)
- [Scripting the Unreal Editor using Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python)
- [Run Automation Tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine) and [command-line arguments reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-command-line-arguments-reference)

