# Module 14 — Game AI and Systems

CSYE 7270 · Fall 2026 · Week 14

## Executive summary

This module is about the systems that make a game act on its own: a non-player character that moves through the world and chooses what to do without anyone watching every frame. You will build one in Godot 4.7.2, a guard that patrols, chases the player and searches where it last saw them, in three handed-off tasks run from the command line (navigation, then a finite state machine, then the same behavior as a behavior tree), separated by a handoff file and your own checks. On 27 September 2026, Claude Code did the first two tasks, hit its usage limit on the third, and Codex finished it from the same handoff; several of the agents' tests passed while checking the wrong thing. The build proves state transitions, reachability and equivalence between two brains on what the tests observe. It does not prove the guard is fun to evade, fair or readable: those are human checks. Three labs on the [labs page](labs.md) cover learning agents, generated levels and networking, and this module feeds Assignment 10, the final project.

## The question

The first agent run in this module reported four passing checks for a guard that walks around an obstacle. "Reaches its target" meant within 64 pixels, the agent had set the arrival tolerance to 48, and the guard stopped 47.7 pixels short. "Never enters obstacle collision bounds" could not fail, because guard and obstacle share the default collision layer and `move_and_slide()` stops the guard before its centre can cross. And the conclusion that the guard starts moving "on the next physics tick" after its first path request held in some trials and not others: over 20 trials the first path arrived anywhere from the 2nd to the 9th physics frame.

An NPC's behavior is a sequence of decisions spread over time, and you will never watch every frame of it. So the question is practical: **what does a passing headless test of game AI actually establish, and how do you split the work so each piece's evidence still holds after the next is built on top of it?**

## The ideas

### The tick: where decisions run

Every system here runs the same loop: sense, decide, act, once per tick. The builds differ in who wrote the decision: you (a state machine or behavior tree), a learning rule, a seeded generator checked by a validator, or another computer; the last three are the labs. In Module 1's vocabulary, the guard is a **scene** of **nodes**, its brain a **script**, its body a **collision shape**, and a state change can be a **signal**.

Godot calls `_physics_process(delta)` at the rate set by `physics/common/physics_ticks_per_second`; the FSM demo sets 120 in `godot/project.godot`. Movement with `CharacterBody2D.move_and_slide()` belongs there because collision is resolved on the physics step ([idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)). A decision need not run every tick: the guard re-targets the player at most every 0.2 s.

### Finite state machines, as this project builds them

A finite state machine (FSM) is a set of states, exactly one current, plus rules for leaving each. The Walker build uses nodes, not an enum. `state.gd` defines the interface: `enter()`, `exit()`, `handle_input()`, `update(delta)` and a `finished(next_state_name)` signal. `state_machine.gd` connects every child's `finished` to `_change_state` and forwards `_physics_process` to the current state. `player_state_machine.gd` maps names to state nodes and **pushes** Jump, Stagger and Attack onto `states_stack`.

Two ideas are layered. **Hierarchical states** share transitions through a parent script: Idle and Move both inherit Jump from `on_ground.gd`, so you write it once. The **pushdown automaton** is `states_stack`: Jump goes on top of whatever was running, and the landing emits `"previous"` to pop back. On a pop, `_change_state` does **not** call `enter()` on the resumed state. Move resumes with its old speed instead of restarting, which is right after a jump and a trap if a resumed state must re-arm a timer. Robert Nystrom's [State chapter](https://gameprogrammingpatterns.com/state.html) covers both ideas.

The demo also shows an FSM's cost. To learn every way out of Move you must read `move.gd`, `on_ground.gd`, `motion.gd` and the Attack interrupt: transitions live on the edges, scattered across files. State names are strings, so a typo is a runtime error. And the base machine calls `initialize()` from `_enter_tree()`, before the children's `_ready()`, so a state that reaches for an `@onready` variable in `enter()` finds it empty on the first frame. You will meet that trap.

### Behavior trees: priority, re-evaluated or remembered

A behavior tree (BT) is ticked from the root, and every node returns **SUCCESS**, **FAILURE** or **RUNNING** (tick me again). A Condition asks a question; an Action moves the guard and usually returns RUNNING until it arrives. A **Sequence** ticks children left to right and stops at the first that does not succeed: AND with order. A **Selector** stops at the first that does not fail: OR with priority ("chase if you can, else search, else patrol"). A **blackboard** is the shared memory, such as the last known player position.

The difference from an FSM is where transition logic lives. An FSM stores it on edges; a BT stores it in the **order of the tree**, and because the root is re-ticked, a higher-priority branch that becomes true preempts a lower one. "Flee when hurt" is one new branch at the left of the root Selector; in an FSM it is a new state plus an exit edge from every state that can be hurt. That holds for **reactive** composites. Composites **with memory** resume the child that returned RUNNING and skip the checks to its left: cheaper, but they give up preemption, as the hands-on shows.

Godot 4.7 ships no behavior-tree node, but [LimboAI](https://github.com/limbonaut/limboai) (a C++ plugin; v1.8.1, 2026-08-20) and [Beehave](https://github.com/bitbrain/beehave) (GDScript; v2.9.3, 2026-08-18) provide one, both MIT-licensed. They add editor authoring, a debugger showing which node is running, ready-made nodes and a managed blackboard, at the cost of a dependency pinned to your engine version. Build the plain version first, so you know what an addon does for you.

### Navigation: a server, a region, an agent

Godot splits navigation in three ([using NavigationAgents](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html)). **NavigationServer2D** holds maps and answers path queries. A **NavigationRegion2D** registers a walkable **NavigationPolygon**, baked from outlines minus obstructions; its `agent_radius` leaves margin for the agent's collision size. A **NavigationAgent2D** sits in the moving body: you set `target_position`, call `get_next_path_position()` once per physics frame, and steer toward it. The agent does not move the body; your `move_and_slide()` does. Three queries sound alike and are not:

| Method | True when |
|---|---|
| `is_target_reachable()` | a path exists to within `target_desired_distance` of the target |
| `is_target_reached()` | the agent has actually moved within that distance of the target |
| `is_navigation_finished()` | the agent is done following the path, which for an unreachable target means it reached the *closest* point |

The timing rule matters for testing. The server applies changes at the end of the physics frame, so at the start of a scene any path query returns empty or wrong results ([using NavigationServer](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationservers.html)). The documented fixes are `call_deferred` and `await get_tree().physics_frame` before the first query. Godot 4.7 also synchronizes on a background thread by default, so the first path's arrival frame varies between runs: a test that requests a path in the frame the scene was added tests the synchronization, not your guard.

## The Walker example: walker-2d-finite-state-machine

[`walker-2d-finite-state-machine`](https://github.com/nikbearbrown/walker-2d-finite-state-machine) is a public repository that keeps the upstream MIT license. It is the Walker adaptation of Godot's official `2d/finite_state_machine` demo, taken from `godot-demo-projects` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`; the only production change is the application title. The player is a top-down `CharacterBody2D` whose `StateMachine` has six child states: Idle, Move, Jump, Stagger, Attack and Die. Controls: WASD or arrows, Shift to run, Space to jump, F to attack, R to fire, X to simulate damage.

**What its checks establish.** The Walker record reports 29 passing headless assertions in two scripts, both driving the real `Demo.tscn` with keyboard events, never setting a state directly. `godot/test_input.gd` has 18 checks: Idle at start, walk speed 450 and run speed 700, the Jump push and landing pop, Stagger, Attack, and the on-screen labels. `godot/test_combo.gd` has 11 on the three-hit sword combo. The instructor reran both on a scratch copy first: `RESULT 18 checks; 0 failures` and `RESULT 11 checks; 0 failures`.

**A caution the record does not contain.** `test_combo.gd` is flaky: on the untouched baseline it failed the same six combo checks in 3 of 16 runs (2 of 8 with `--fixed-fps 60`, 1 of 8 without), cause not found. One passing run cannot show that, so rerun it before believing a pass or a failure.

**What remains unverified.** No rendered frame has been inspected, and no human has played it. The scene has no enemy or health target, so sword hits and damage are untested, and Die is not in the player's `states_map`. The project has no NPC and no navigation, which makes it the right base: each task adds an NPC to a state-machine core that already has 29 checks, which must keep passing.

## Predict → Build It → Use It → Ship It → Verify

You will add an NPC guard in three separate runs. Each ends by writing `HANDOFF.md`; each later run starts by reading it and rerunning every test it lists.

### 1. Predict

Answer these in `FRICTIONAL.md` before the first run:

1. The guard gets a target in the same frame its scene is added. What will `get_next_path_position()` return on the first physics frame, and what will the guard do?
2. A target is placed in the middle of the solid obstacle. Where should the guard end up, and what should `is_target_reachable()`, `is_target_reached()` and `is_navigation_finished()` report?
3. The state-machine base calls `initialize()` from `_enter_tree()`. The guard's Patrol state needs the guard's `NavigationAgent2D` in `enter()`. What goes wrong, and when?
4. You have one set of behavioral tests for the FSM guard. What must they read, and never read, so the identical tests can later judge a BT guard?

### 2. Build It

Work in your own copy of the project, on a clean commit, with Godot 4.7.2 on your `PATH`. Why three runs instead of one? Each task fails differently: navigation on timing and geometry, the FSM on transitions and initialization order, the BT on priority and RUNNING. One giant prompt gives one giant diff in which those failures hide behind each other. Choosing the order, the context and the evidence required before the next run is the **Tool Orchestration** capacity the syllabus assigns this week.

The prompts below are the exact text given in the recorded run, each saved in a file and passed with `$(cat …)`. In your copies, make two changes. Add `--fixed-fps 60` after `--headless` in each prompt's `Run:` line (the recorded agents ran without it; Verify explains why). And add `--disallowedTools "Skill"` to each `claude -p` command so the session cannot invoke skills installed on your machine.

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

The prompt names the files you care about and those off limits, three checks with their failure cases, and the handoff, and it leaves out any algorithm. Check 3 is deliberately an open question: the honest answer is an observation, not a spec.

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

Three lines carry the design. "Extend them; do not edit them" keeps the guard on the project's FSM base, so the 29 player checks keep guarding it. `lose_radius > sight_radius` is **hysteresis**: with one radius, a player on the boundary flips the guard between Chase and Search every tick. And `mode` is the test contract from your question 4: tests read `mode` and positions, never the machine's internals, and move the player only as a labelled fixture.

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

Claude Code's run of this prompt reread the handoff, reran the four tests, and stopped at its usage limit before editing anything. The same prompt went to Codex from the same commit:

```bash
codex exec --ignore-user-config -s workspace-write --add-dir "$HOME/Library/Application Support/Godot" --add-dir "$HOME/Library/Caches/Godot" --json -o main-3-last-message.txt "$(cat main-3-bt.txt)" < /dev/null > session-main-3-codex.jsonl
```

This task asks for the same behavior from a different architecture, judged by the same tests. If the BT guard passes the FSM guard's checks, the two are equivalent on everything those checks observe, and nothing more. The composite unit checks exist because behavioral checks cannot tell a Sequence that resumes a RUNNING child from one that restarts from the left.

**The Codex difference.** `codex exec` has no per-run allowlist flag; its boundary is the sandbox mode, and `-s workspace-write` limits where commands may write, not which may run. Claude Code's `--allowedTools` says "only `godot` and `git`" directly, though the [labs page](labs.md) shows even that rule is weaker than it looks. The first Codex pass stopped on a bug in its own new test; a fresh Codex session got this correction, with the same command pattern:

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

It scopes the stop rule and defines a clean run as exit 0 with no `SCRIPT ERROR` or `ERROR:` lines.

**Between runs, your own gate.** Do not paste the next prompt when an agent says it is done. First, read `git diff` and the new `HANDOFF.md`, and check that every listed test exists and that "what the next task may rely on" is true of the code, not just the prose. Second, import once: agents create `.uid` files by hand, and until the import pass registers them every load prints `invalid UID … using text path instead`.

```bash
godot --headless --path godot --import
```

Third, rerun every test yourself with a pinned time step and read the whole log, not the `RESULT` line: `grep -c "SCRIPT ERROR"` should print 0, since a script error neither stops Godot nor changes its exit code. Fourth, commit, so the next diff has a baseline.

### 3. Use It

Tests cannot say whether the guard is good to play against. Open `godot/npc/guard_arena.tscn`, use **Run Current Scene**, and turn on **Debug > Visible Navigation** to draw the polygon and the guard's path. The player uses the FSM demo's controls. Then try to break it; every judgment here is a **HUMAN CHECK**.

- Stand in the guard's patrol route and watch the label switch to Chase.
- Circle the obstacle to block the line of sight, and time how long the guard keeps searching.
- Stand at the edge of its sight. Does the label flicker, or does hysteresis hold?
- Stand against the obstacle and let it chase you there. Does it slide along the wall or push?
- Let it lose you, then step back into plain view while it searches. Does it notice?

Then set the Guard's exported **Brain** from FSM to BT and repeat. If the brains feel different, write down how: the tests call them equivalent only on what they observe.

### 4. Ship It

Commit after each task, with a message naming the task, the test command and its result. `FRICTIONAL.md` gets your four predictions, the agent claims that turned out wrong or untested, and what you changed or reran because of them. The Brutalist film skill that fits is `godot-gamedev`: its input, state, output trace is literally the guard's mode label following the player's position. Use `godot-walkthrough` only after a human has played the guard, since it shows real gameplay. The skills come from the course-provided checkout; request the update if yours lacks one.

### 5. Verify

Run each test yourself. `godot --help` describes `--fixed-fps` as forcing a fixed frame rate and disabling real-time synchronization, so each frame advances exactly 1/60 s of game time however fast the machine runs. `timeout 120` ends a run that hangs, since a script error before `quit()` leaves headless Godot running. Stock macOS lacks `timeout`; Homebrew's `coreutils` provides it.

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

`test_guard_fsm.gd` runs each behavioral check once per brain; `test_bt.gd` holds the composite checks. **A pass establishes** that, in this arena on Godot 4.7.2, the guard reaches a reachable far-side target, stops at the closest point for an unreachable one, chases a visible player in range, falls back through Search to Patrol, ignores a player hidden behind the obstacle, and does the same under either brain, and that the 29 original player checks still pass (mind the `test_combo.gd` caveat). **It does not establish** that the guard is fun, fair or readable, that it copes with two guards, a moving obstacle or another arena, or that the first path arrives on any particular frame. Navigation sync runs on a background thread (`navigation/world/map_use_async_iterations` and `region_use_async_iterations` default to `true`), and `--fixed-fps` does not pin a thread. If a test truly needs that frame, turn both settings off in the test project (in a scratch copy the first path then arrived on frame 2 or 3 every time).

## What the agents got wrong

The recorded runs (Claude Code 2.1.150 with `claude-sonnet-4-6`, Codex CLI 0.153.4, 27 September 2026) show that "done" is a claim.

**Tests that could not fail, and a claim that did not hold.** Beyond the 48 versus 64 pixel tolerance, the instructor's audit measured the guard's closest approach to the obstacle at 17.9 px for a 16 px radius, with zero slide collisions, so the "never inside" check was vacuous. The agent's "next physics tick" was one outcome of several (frame 2 in 8 of 20 trials); with asynchronous sync off, every trial gave frame 2 or 3.

**Green on top of a script error.** In Task 2, the base machine called `Patrol.enter()` from `_enter_tree()` before the guard's `@onready` variable existed, and the test printed `RESULT 6 checks; 0 failures` over a `SCRIPT ERROR`. The agent spotted it in the log and deferred Patrol's first `set_target()`. In Task 3, Codex's first run stopped on a runtime error in its own new test, reading "if any test fails, stop" as covering it; the instructor's rerun of that state showed all 12 behavior checks passing and exit code 0 over 626 lines of `SCRIPT ERROR`. After the correction, all 61 checks passed (4 navigation, 14 behavior, 14 composite, 29 player).

**Equivalent, and equivalently blind.** The hysteresis test put the player 240 px away, but the chasing guard walked closer, so the band was never tested; holding the player at 260 px for 120 frames gave 0 mode changes. And with the guard in Search and the player 120 px away in plain sight, both brains stayed in Search for about 165 physics frames before going Patrol, then Chase. The spec never said what Search should do if the player reappears, and no test covered it. A player would notice in ten seconds.

## If you know Unity or Unreal

Unity and Unreal were not run for this module; the comparisons come from their official documentation, checked on 27 September 2026.

| Godot 4.7 | Unity 6 | Unreal Engine 5 |
|---|---|---|
| `NavigationRegion2D` + `NavigationAgent2D` | NavMesh Surface + `NavMeshAgent` | Nav Mesh Bounds Volume, `RecastNavMesh`, AI Move To |
| Plain-GDScript FSM | C# state machine | StateTree |
| Plain-GDScript BT, LimboAI, Beehave | C# BT, Unity Behavior package | Behavior Tree + Blackboard assets |
| Godot RL Agents (community) | ML-Agents | Learning Agents (Experimental) |
| Seeded generator + validator | C# generator, `Tilemap.SetTile` | PCG framework graph |
| `@rpc`, `MultiplayerSynchronizer` | `[Rpc]`, `NetworkVariable` | `Server`, `Client`, `NetMulticast` replication |
| `godot --headless --script …` | `Unity -runTests -batchmode -testPlatform PlayMode` | `-ExecCmds="Automation RunTest …;Quit"`, `-nullrhi` |

The biggest difference for an agent workflow is what the agent can read. In Godot the whole guard (scene, brain, tests) is text. Unity scenes and prefabs serialize as text, but every asset has a `.meta` GUID file an agent must not create by hand. In Unreal, Behavior Trees, Blackboards, StateTrees and PCG graphs are binary `.uasset` files: the agent writes C++ tasks and tests, and wiring the graph stays a human job or goes through editor automation. The [companion chapter](../../chapters/14-game-ai-and-systems.md) has the full comparison.

## Practice assessment (ungraded)

Answer in your own words, then check the source:

1. In `state_machine.gd` a pop does not call `enter()` on the resumed state. Name a case where that helps and one where it hurts.
2. Your FSM guard's test reads only `mode` and positions. Why must it never read the machine's internals, and why does that help when the brain becomes a BT?
3. An agent reports "guard reaches its target" and all four checks pass. Which numbers in the test would you read first?
4. Both brains ignore a player who reappears during Search. Write the one-sentence spec change, and say which brain needs the smaller code change.

An ungraded practice quiz covering the guard and the three labs is on this module's Canvas page. Do not paste Claude's explanation as proof of your understanding; ask it to question you, then answer from the source.

## The next step

Do the three labs on the [labs page](labs.md): reinforcement learning, a generated level with a validator, and networking in two processes. This module, with Module 15, feeds Assignment 10, the final project. That assignment opens in Module 14 and is due about Day 100 (Canvas dates govern); its own page sets the task and the required films, and this lesson adds no graded deliverable. Module 15, from brief to export, comes next. The long reading is [Chapter 14 — Game AI and Systems](../../chapters/14-game-ai-and-systems.md).
