# Prompts and command lines — Chapter 13

Prompts are reproduced exactly as given. The runs were made from a scratch copy of the project whose root is shown as `.`.

## Session 1 — Claude Code (prompt printed in the chapter)

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
claude -p "$(cat prompt1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose --strict-mcp-config --settings '{"autoMemoryEnabled":false}' > session1.jsonl
```

The recorded session 1 did **not** have `--disallowedTools "Skill"`. After five refused Godot calls, one with `dangerouslyDisableSandbox`, and an unanswerable question, the agent invoked the `fewer-permission-prompts` skill and tried to list `~/.claude/projects` (blocked). The instructor stopped the process at tool call 45; no settings file was written. The chapter's printed command adds `--disallowedTools "Skill"`. `--strict-mcp-config` and the `autoMemoryEnabled` setting were operational choices for the course record.

## Session 2 — Claude Code, resumed with a correction

```text
Stop trying to change permissions: do not invoke skills or edit any settings file. Your allowed tools include Bash(godot:*), not the absolute path to the Godot app. Run Godot as the plain command `godot` (it is on PATH and is the same 4.7.2 binary), one command per Bash call, without cd, &&, pipes or environment variables. Import first (godot --headless --path godot --import), then run every test and command the task asked for and paste the real output. Fix only what the output shows is broken, and report anything you could not run.
```

```bash
claude -p "$(cat correction-ch13.txt)" --resume edadb634-bbdd-4282-a35e-a6b37adebd13 --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --disallowedTools "Skill" --max-turns 40 --output-format stream-json --verbose --strict-mcp-config --settings '{"autoMemoryEnabled":false}' > session2.jsonl
```

The session printed its final report at about 18:17 UTC but did not exit until 18:37 UTC, when the instructor killed a headless `godot … test_motion.gd` process the agent had started at 18:12. That run had hit a script error before `quit()` and would never have exited.

## Instructor verification commands

```bash
timeout 120 godot --headless --path godot --script res://test_mouse_input.gd
timeout 120 godot --headless --path godot --script res://test_collision_input.gd
timeout 120 godot --headless --path godot --script res://test_motion.gd
timeout 120 godot --headless --path godot --script res://bench/test_nodes_parity.gd -- --count=500
timeout 120 godot --headless --path godot --script res://bench/test_nodes_parity.gd -- --count=5000
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://test_collision_input.gd
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://test_motion.gd
timeout 120 godot --headless --fixed-fps 60 --path godot --script res://bench/test_nodes_parity.gd -- --count=5000
bash verification/sweep.sh . verification/sweep1.csv
bash verification/sweep.sh . verification/sweep2.csv
python3 verification/summarize.py verification/sweep-combined.csv
```
