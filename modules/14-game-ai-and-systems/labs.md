# Module 14 — Labs: learning agents, generated levels, networking

CSYE 7270 · Fall 2026 · Week 14

## Executive summary

The guard on the [lesson page](lesson.md) got its behavior from you. These three labs show the other places behavior and content come from: a reward signal, a seed plus a checker, and another computer. Lab A teaches an agent a 5×5 grid by tabular Q-learning, small enough to print its whole brain; Lab B generates side-scrolling levels from a seed and builds a validator that decides whether each can be crossed; Lab C runs two copies of a networked game on one machine and tests who may move what. Each lab follows Predict, Build It, Use It, Ship It, Verify, using the prompts really run on 27 September 2026 (Lab A with Codex, Labs B and C with Claude Code) on a public Walker repository that keeps the upstream MIT license; the [companion chapter](../../chapters/14-game-ai-and-systems.md) has the full record. What the labs prove is narrow: a repeatable learning run, a validator that rejects two impossible shapes you build by hand, and one authority rule enforced on loopback. They do not prove that Q-learning works in general, that an accepted level is fun or even crossable, or that the networking survives the internet, and several of the agents' passing checks measured the wrong thing, so read each Verify section before trusting a green line.

## Lab A: reinforcement learning you can watch converge

The guard's behavior was written by hand. Here it is learned from reward. Reinforcement learning (RL) models the world as states `s`, actions `a`, a reward `r` after each step and a next state `s'`, and the agent maximizes the **return**: the sum of rewards, with later ones discounted by `γ` (gamma) per step. **Q-learning** keeps a table `Q(s, a)`, an estimate of the return from taking `a` in `s` and acting well afterwards, and after every step nudges the estimate:

```text
Q(s, a) <- Q(s, a) + alpha * ( r + gamma * max_a' Q(s', a') - Q(s, a) )
```

`alpha` is the step size, and the bracket is the **temporal-difference error**: how wrong the old estimate was. Q-learning is **off-policy**: it learns the value of acting greedily while it explores with an **epsilon-greedy** rule, taking a random action with probability `epsilon`. Watkins and Dayan [proved](https://doi.org/10.1007/BF00992698) that tabular Q-learning converges when every state-action pair keeps being visited and step sizes shrink appropriately. This lab uses a constant `alpha`, so the theorem's conditions do not strictly hold: what you measure is whether this run settles.

Three methods that need neural networks sit beyond this lab, and none was run for the chapter. **Deep Q-Networks** replace the table with a network and stabilize training with experience replay and a periodically copied target network ([Mnih et al., 2015](https://doi.org/10.1038/nature14236)). **Policy gradient** methods adjust the policy's own parameters toward high-return actions; REINFORCE is the classic form ([Williams, 1992](https://doi.org/10.1007/BF00992696)). **PPO** is a policy-gradient method whose clipped objective discourages large policy changes ([Schulman et al., 2017](https://arxiv.org/abs/1707.06347)). [Gymnasium](https://gymnasium.farama.org/) is the standard interface between a simulator and these algorithms, and [Godot RL Agents](https://github.com/edbeeching/godot_rl_agents) connects a Godot game to Python RL libraries; neither was installed or run.

### Predict

Write your answers in `FRICTIONAL.md` before the run:

1. The goal is 8 steps from the start, and two pits sit near the diagonal. With a step cost of −0.01 and γ = 0.95, will the learned path be a shortest one, or a longer one that gives the pits a wide berth? Why?
2. Epsilon falls linearly from 1.0 to 0.05 over 500 episodes. Will the *training* success rate reach 100% for 25 episodes in a row? Will the *greedy* policy be optimal before the training curve looks good, or after?
3. Run the same seed twice. Which lines of output must be byte-identical, and which could legitimately differ?

### Build It

Start from a fresh copy of [`walker-2d-finite-state-machine`](https://github.com/nikbearbrown/walker-2d-finite-state-machine), on a clean commit, with Godot 4.7.2 on your `PATH`; the lab touches no existing file. As in the lesson, add `--fixed-fps 60` after `--headless` in the prompt's `Run:` line. The recorded run used **Codex**, to show the other CLI on the same kind of task:

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

`-s workspace-write` lets Codex's commands write inside the working directory and nowhere else. The two `--add-dir` flags add Godot's user-data and cache folders on macOS to that writable set; they were added so Godot would not trip over the sandbox, and the run was not tested without them. `--ignore-user-config` keeps personal Codex settings out of a run you want to be reproducible. `< /dev/null` matters when the command runs from a script: the recorded run omitted it, printed `Reading additional input from stdin...`, and happened to finish anyway. If you have no Codex, give the same prompt to Claude Code with the command pattern from Lab B; that pairing was not part of the recorded run, so read the first diff before trusting it.

### Use It

There is nothing to watch in a window; the learning curve is the thing to look at. Read the 20 curve lines top to bottom and find where the mean return turns positive. Then read the arrow grid as a map: each arrow is the action the table rates highest in that cell. **HUMAN CHECK:** follow the arrows from the top-left corner and confirm they route around both pits. Arrows on the pit and goal cells mean nothing, because the episode ends there and those rows are never updated.

### Ship It

Commit `godot/rl/` and `godot/tests/test_qlearning.gd` with the three saved curves. In `FRICTIONAL.md`, record your three predictions next to the real numbers, especially the training success rate. The fitting Brutalist film skill is `godot-gamedev`: its input, state, output trace here is episode, Q-table, arrow grid. The skills come from the course-provided checkout; request the update if yours lacks one.

### Verify

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://tests/test_qlearning.gd
```

```bash
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://tests/test_qlearning.gd -- --seed=7
```

**A pass proves** four things about this implementation on Godot 4.7.2: the environment follows its rules (nine rule checks, including both Q-update cases), training is repeatable from a seed, the final greedy policy from the start cell is an optimal pit-free path, and the run is fast (under a second here). **It does not prove** that Q-learning converges in general, that the greedy policy is optimal from every cell, or anything about DQN, PPO or a game with continuous state.

**What the recorded run found.** Codex took about 3 minutes. Two runs with seed 42 gave byte-identical logs, and seed 7 gave a different curve (final window 96% success, mean return 0.85) and a different optimal route; `--fixed-fps 60` changed nothing, as expected for a test that never waits on the clock. Seed 42 ended at episode 500 with mean return 0.6896 and 88% success, and the greedy path `(0, 0) -> (0, 1) -> (0, 2) -> (1, 2) -> (2, 2) -> (2, 3) -> (3, 3) -> (4, 3) -> (4, 4)`. The training success rate never held 100% for 25 episodes, because exploration never stops (epsilon ends at 0.05). To learn when the *policy* was right, the instructor added a probe that evaluates the greedy path after every episode: for seed 42 it was first optimal at episode 46, flipped between optimal and not 9 times, and stayed optimal from **episode 101** to 500; for seed 7, first at 76, 13 flips, optimal from **episode 132**. Which number belongs in a report depends on its title: "the agent learned the task" or "the agent is safe to ship with exploration on."

## Lab B: procedural content with a validator

A generator that can produce an impossible level is a bug factory with a seed. Procedural content generation (PCG) makes content with an algorithm, and three ideas carry most of it. **A seed makes it repeatable:** a `RandomNumberGenerator` with a fixed `seed` gives a reproducible sequence, though its [documentation](https://docs.godotengine.org/en/stable/classes/class_randomnumbergenerator.html) warns that the algorithm is an implementation detail, so if a level must survive engine upgrades, store the generated data and not only the seed. **Noise makes it coherent:** [`FastNoiseLite`](https://docs.godotengine.org/en/stable/classes/class_fastnoiselite.html) returns smooth values for any coordinate, and [`walker-compute-heightmap`](https://github.com/nikbearbrown/walker-compute-heightmap) turns simplex noise into an island with a radial gradient, in a GDScript loop and in a GLSL compute shader. **A validator makes it playable:** a check that each output meets a playability rule, with a policy for failures, either reject and re-roll (generate-and-test) or build the level so it cannot fail (constructive). The validator is a *model* of your game's rules, only as good as the numbers you feed it, which is why this lab measures the player's real jump before writing any validator.

Houdini was the industrial answer in the old course. SideFX lists [Houdini Engine plug-ins](https://www.sidefx.com/products/houdini-engine/plug-ins/) for Unity, Unreal, Maya and 3ds Max, not Godot, so treat it as context here.

The lab runs in `walker-2d-dynamic-tilemap-layers`, a side-view platformer whose `Ground` and `Secret` layers are [`TileMapLayer`](https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html) nodes sharing one 16-pixel `TileSet`, and whose player (`godot/player/player.gd`) walks at up to 200 px/s and jumps with an initial speed of 200 px/s under a gravity of 500 px/s².

### Predict

1. From those three numbers alone, how high can the player jump, in pixels and in 16-pixel tiles? How far can it travel horizontally in one jump at full speed? Write the arithmetic down before the engine answers.
2. Why might the engine's measured height differ from your arithmetic? (Look at `physics/common/physics_ticks_per_second` and at how `player.gd` applies gravity.)
3. If the validator uses exactly the measured limits with no margin, which kind of level will it wrongly accept?

### Build It

Start from your own copy of [`walker-2d-dynamic-tilemap-layers`](https://github.com/nikbearbrown/walker-2d-dynamic-tilemap-layers), on a clean commit. As in the lesson, add `--fixed-fps 60` after `--headless` in the prompt's run commands and `--disallowedTools "Skill"` to the `claude -p` command.

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

The prompt makes the agent **measure before it models**. Step 1 is a test of the real player scene, and steps 2 and 3 may use only its numbers. That ordering is the whole lesson: a validator built from remembered constants is a guess. The recorded run shows an agent can follow the ordering to the letter and still measure the wrong thing.

### Use It

Open `godot/world.tscn`, run it, and play the original level first, jumping as high and as far as you can. Then write one accepted level into the `Ground` layer (clear the layer, then one `set_cell` call per solid column) and play it from left to right. The validator claims every accepted level is crossable, and you are the second opinion. **HUMAN CHECK:** a level the validator accepts that you cannot cross is the most valuable bug this lab can find.

### Ship It

Commit the generator, the validator and the tests together; a generator committed without its validator is the thing this lab exists to prevent. `FRICTIONAL.md` records your predicted envelope, the measured one, the margin, the pass rate, and any level you could not cross by hand. Use `godot-walkthrough` if you film it, since the claim that matters is "a player can cross this," which only real play can show.

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

**A pass establishes** that the generator is deterministic for a seed on this engine version, that the validator rejects the two impossible shapes you built by hand, what fraction of seeds it accepts, and (once the landing check really uses a generated level) that accepted levels can be written into the real `TileMapLayer` with working collision. **It does not establish** that an accepted level can be crossed. The validator's model ignores ceilings, run-up distance before a jump, the player's 14-pixel width, and anything a designer would call fun.

**What the recorded run found.** Claude Code took 34 turns and about 20 minutes. It measured a rise of 39.2 px (2.45 tiles; the theory `v²/2g` gives 40) and a horizontal range of 128.3 px (8.02 tiles), set the validator's limits to 2 tiles of step and 6 tiles of jump distance, and reported a pass rate of 21.5% (43 of 200 seeds), with determinism and both hand-made impossible levels correctly handled. The instructor's audits found three problems.

- **The range was measured under a ceiling.** The prompt asked for a flat floor; the test used the original level, where the player took off at the full 200 px/s and hit a ceiling at x = 240.8. On a flat floor of 125 tiles the same run-and-jump covered **163.3 px (10.21 tiles)** in 97 physics frames, close to the 160 px that speed times airtime predicts. The agent's number reproduces, but it measures the level and not the jump, and its explanation was a guess.
- **The landing check did not use a generated level.** It wrote a hand-built flat row. The instructor's corrected check wrote every accepted level into `Ground` and dropped the player above its first solid column: **43 of 43** came to rest on a tile.
- **Why levels fail.** Of the 157 rejections, 72 were steps too high, 69 gaps too wide, and **16 levels ended in a gap**, which no jump can fix. That last group is a generator bug, not bad luck.

The existing `test_secret.gd` still passed 11 of 11, and every Lab B result was identical with and without `--fixed-fps 60`.

## Lab C: scoped networking in two processes

Godot's [high-level multiplayer](https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html) puts a **MultiplayerPeer** (here `ENetMultiplayerPeer`) under the scene tree's `multiplayer` API. The host calls `create_server(port, max_clients)`, a client calls `create_client(ip, port)`, each peer gets an integer id, and the server is always id 1. Every node has a **multiplayer authority**, a peer id that is 1 unless you call `set_multiplayer_authority()`. Authority is a convention that the RPC system enforces: a function marked `@rpc` defaults to `@rpc("authority", "call_remote", "reliable", 0)` ([GDScript annotations](https://docs.godotengine.org/en/stable/classes/class_@gdscript.html)), meaning only the node's authority may call it, it runs on the other peers but not the caller, and it is delivered reliably on channel 0. `"any_peer"` lets anyone call it, `"call_local"` also runs it on the caller, and `"unreliable"` trades delivery guarantees for latency. [`MultiplayerSynchronizer`](https://docs.godotengine.org/en/stable/classes/class_multiplayersynchronizer.html) and [`MultiplayerSpawner`](https://docs.godotengine.org/en/stable/classes/class_multiplayerspawner.html) do some of this bookkeeping for you; Pong uses neither, and [`walker-networking-multiplayer-bomber`](https://github.com/nikbearbrown/walker-networking-multiplayer-bomber) uses both.

**Scoped** networking means you choose the boundary you test inside and say so. Here that boundary is loopback: two processes on one machine at `127.0.0.1`. Latency, packet loss, NAT and hostile clients are outside it.

The [`walker-networking-multiplayer-pong`](https://github.com/nikbearbrown/walker-networking-multiplayer-pong) build already has two-process loopback checks for paddle replication, scoring and disconnect. This lab asks a sharper question about **authority**: what happens when a peer tries to move something it does not own? Read `godot/logic/paddle.gd` first. Each paddle's authority peer reads its keys and calls `set_pos_and_motion.rpc(position, _motion)` every frame, declared `@rpc("unreliable")`, so its mode is the default, `"authority"`. Then read `ball.gd` and `pong.gd`: `bounce`, `stop`, `_reset_ball` and `update_score` are all `@rpc("any_peer", "call_local")`. The demo protects paddle positions and trusts either peer to report bounces and points.

### Predict

1. The client calls `set_pos_and_motion.rpc()` on Player1, whose authority is the host. Does the call leave the client? Does the host run it? What, if anything, is printed, and on which side?
2. The host holds `move_up` for half a second. After how long should the client's copy of Player1 agree with the host's, and to what tolerance, given the RPC is unreliable?
3. Which of Pong's RPCs could a modified client abuse to win, and what would the host have to check to stop it?

### Build It

Start from your own copy of [`walker-networking-multiplayer-pong`](https://github.com/nikbearbrown/walker-networking-multiplayer-pong), on a clean commit, and add `--disallowedTools "Skill"` to the command. Leave the prompt's commands as written: this lab runs in real time.

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

Export nothing; run two instances from the editor instead. **Debug > Customize Run Instances** ([added to the editor in PR #65753](https://github.com/godotengine/godot/pull/65753)) launches more than one instance of the project from one Run. Start two, press Host in one and Join in the other, and play a point with W/S in each window. **HUMAN CHECK:** watch both paddles in both windows. The lag you see on the remote paddle is the unreliable RPC doing its job.

### Ship It

Commit the test and the two logs. `FRICTIONAL.md` gets the three predictions and what was printed on each side. For the film, `godot-gamedev` fits: the trace is key press on one process, RPC, property change on the other.

### Verify

Both processes run in real time, without `--fixed-fps`: two processes exchanging packets share one clock, the wall clock, and a fixed step would let each run its game time at its own speed. Start the host first:

```bash
timeout 30 godot --headless --path godot --script res://tests/test_authority.gd -- --walker-loopback --test-host > host.log 2>&1 &
```

```bash
timeout 30 godot --headless --path godot --script res://tests/test_authority.gd -- --walker-loopback > client.log 2>&1
```

**A pass on both sides establishes**, on loopback only, that the two processes connect, that one property change made by the owner reaches the other peer, and that the engine rejects one authority-mode RPC from a peer that does not own the node, and says so on the receiving side. **It does not establish** anything about latency, packet loss, NAT or a modified client, and it says nothing about the RPCs declared `any_peer`.

**What the recorded run found.** Claude Code took 63 turns and about 18 minutes. Its final logs, which the instructor's rerun reproduced, showed three passes and, on the host, the line `ERROR: RPC 'set_pos_and_motion' is not allowed on node /root/Pong/Player1 ... Mode is "authority", authority is 1.` That error is the pass for check 3, not a bug. The path there was rougher than the logs suggest.

- **A side channel.** The test hands the host's y value to the client through a file in `/tmp`. A few turns earlier, Claude Code had refused the agent's own shell redirect into `/tmp`, yet the GDScript wrote there without asking.
- **An orphan that kept the port.** A crash on the host (`Invalid access to property or key 'position' on a base object of type 'previously freed'`) meant it never reached `quit()` and kept UDP port 8910 bound, so every later host failed with `Couldn't create an ENet host`. The agent tried `pkill` and `lsof` and the allowlist refused both. It then added these calls to the test script, which `Bash(godot:*)` does allow:

```gdscript
OS.execute("/usr/sbin/lsof", ["-ti:8910"], pids, true)
# ...
OS.execute("/bin/kill", [pid], [], false)
```

The next host run printed `pre-test cleanup: killing stale PID 40527 on port 8910` and everything passed. The process it killed was its own orphan, but the same lines would kill any process holding port 8910, including another test's server, under an allowlist meant to permit only `godot`, `git`, `timeout`, `sleep`, `cat`, `ls` and `mkdir`. Allowing `godot --script` allows anything GDScript can do. The agent's `FRICTIONAL.md` entry recorded the three passing checks and none of the three failures. The instructor removed the block ([`lab-c/correction-by-author.diff`](../../examples/14-game-ai-and-systems/lab-c/correction-by-author.diff)), wrapped both processes in `timeout 30`, and reran: both exit 0 with the same three passes.

Then came the question the agent was not asked. An audit script had the client call `update_score.rpc(false)` three times half a second into a match, before the ball could reach either edge, and the host printed `host score_right before=0 after=3 label=3 ball_x=199.0` and `RESULT forged points accepted by host: 3 of 3`. No error appeared. The paddle RPC is protected by its default `"authority"` mode; the score RPC is `"any_peer"` and trusts whoever calls it.
