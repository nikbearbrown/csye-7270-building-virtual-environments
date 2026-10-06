# Prompts — Chapter 14 worked example

Every prompt below is the exact text passed to the CLI on 2026-09-27 (saved to a file and passed with `"$(cat file)"`). Commands follow each prompt. Run each agent from the repository root of your scratch copy (the folder that contains `godot/`).

These are the commands as recorded. For your own runs, two changes: add `--disallowedTools "Skill"` to each `claude -p` line so the session cannot invoke skills installed on your machine (no recorded run invoked one), and add `--fixed-fps 60` to the `Run:` lines inside the single-process prompts (the agents ran their tests without it; see the chapter's Verify section). Lab C's two processes should stay in real time.

## Main hands-on, Task 1 — navigation (Claude Code)

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

## Main hands-on, Task 2 — finite state machine (Claude Code)

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

## Main hands-on, Task 3 — behavior tree

Given first to Claude Code with the same command pattern. That run reread the handoff, reran its four tests (all passed), and stopped at the account's usage limit before editing anything (`transcripts/claude-main-3-stopped-at-usage-limit.jsonl`). The identical prompt was then given to Codex from the same commit.

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

```bash
codex exec --ignore-user-config -s workspace-write --add-dir "$HOME/Library/Application Support/Godot" --add-dir "$HOME/Library/Caches/Godot" --json -o main-3-last-message.txt "$(cat main-3-bt.txt)" < /dev/null > session-main-3-codex.jsonl
```

## Main hands-on, Task 3 correction (Codex, fresh session)

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

```bash
codex exec --ignore-user-config -s workspace-write --add-dir "$HOME/Library/Application Support/Godot" --add-dir "$HOME/Library/Caches/Godot" --json -o main-3b-last-message.txt "$(cat main-3b-correction.txt)" < /dev/null > session-main-3b-codex.jsonl
```

## Lab A — Q-learning (Codex)

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
codex exec --ignore-user-config -s workspace-write --add-dir "$HOME/Library/Application Support/Godot" --add-dir "$HOME/Library/Caches/Godot" --json -o lab-a-last-message.txt "$(cat lab-a-qlearning.txt)" < /dev/null > session-lab-a.jsonl
```

The recorded Lab A run was launched without `< /dev/null`; its stderr shows `Reading additional input from stdin...` and the run still completed. Add the redirect: `codex exec` started from a script or in the background can otherwise wait on stdin.

## Lab B — procedural content with a validator (Claude Code)

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
claude -p "$(cat lab-b-pcg.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > session-lab-b.jsonl
```

## Lab C — scoped networking (Claude Code)

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
claude -p "$(cat lab-c-network.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(timeout:*),Bash(sleep:*),Bash(cat:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > session-lab-c.jsonl
```
