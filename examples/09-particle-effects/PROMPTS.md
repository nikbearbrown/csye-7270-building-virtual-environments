# Prompts and command lines — Chapter 9

Every prompt below is reproduced exactly as it was given. Paths in the command lines are shortened: the runs were made from a scratch copy of the project, whose root is shown as `.`.

## Session 1 — Claude Code, the burst (prompt printed in the chapter)

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

```bash
claude -p "$(cat prompt1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose --strict-mcp-config --settings '{"autoMemoryEnabled":false}' > session1.jsonl
```

`--strict-mcp-config` (load no MCP servers) and the `autoMemoryEnabled` setting were operational choices for the course record; students do not need them.

## Session 2 — Claude Code, resumed: run the tests

```text
Your allowed tools include Bash(godot:*), not the absolute path to the Godot app. Run Godot as the plain command `godot` (it is on PATH and is the same 4.7.2 binary), one command per Bash call, without cd, &&, pipes or environment variables. Import first if needed (godot --headless --path godot --import), then run every test and command the task asked for and paste the real output. Fix only what the output shows is broken, and report anything you could not run.
```

```bash
claude -p "$(cat correction.txt)" --resume 59324d13-6215-471b-8c74-f47e59f2de9d --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 40 --output-format stream-json --verbose --strict-mcp-config --settings '{"autoMemoryEnabled":false}' > session2.jsonl
```

## Session 3 — Claude Code, resumed: correction with evidence

```text
Your explanation of the FAIL is wrong. finished does fire in headless Godot 4.7.2: in a separate probe, a one-shot GPUParticles2D with lifetime 0.5 emitted finished about 0.5 s after restart(). Look at your test instead. GDScript lambdas capture local variables by value, and a lambda cannot reassign an outer local (see "Lambda functions" in the GDScript reference). Fix the test so the flag can actually change, rerun both tests, and paste the output. Do not weaken or remove the check.

Two DeathBurst settings are also plausible but wrong for 2D, according to the documentation:
- GPUParticles2D.texture is null, and the class reference says a null texture draws 1x1-pixel squares. Give the burst a soft round dot: a GradientTexture2D sub-resource, 16x16, radial fill, white centre fading to transparent.
- ParticleProcessMaterial is shared with 3D, and the official 2d/particles demo README says to enable Disable Z when it is used in 2D. Set particle_flag_disable_z = true.
Add a check for each to test_particles.gd. Change nothing else.
```

```bash
claude -p "$(cat prompt3.txt)" --resume 59324d13-6215-471b-8c74-f47e59f2de9d --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --disallowedTools "Skill" --max-turns 40 --output-format stream-json --verbose --strict-mcp-config --settings '{"autoMemoryEnabled":false}' > session3.jsonl
```

`--disallowedTools "Skill"` was added after another chapter's agent, refused a command, tried to invoke a skill that edits permission settings (see Chapter 13's record).

## Codex session — the cost measurement (prompt printed in the chapter)

```text
Work in godot/ of this Godot 4.7.2 project. Do not edit any existing game file.

Add godot/tests/particle_cost.gd (extends SceneTree), runnable with
godot --headless --path godot --script res://tests/particle_cost.gd
It measures what particle simulation costs the CPU in this headless run, not how it looks.

For each node type (GPUParticles2D with a ParticleProcessMaterial, and CPUParticles2D) and each amount (1000, 10000, 50000): create one emitting emitter with lifetime 1.0, initial velocity 50 to 100 and gravity (0, 98) under an empty Node2D, wait 60 warm-up frames, then time 300 frames with Time.get_ticks_usec() and report the mean milliseconds per frame. Repeat each case 3 times in the same process; print min, mean and max of the three means. Also print one empty-scene baseline with no emitter. Free each emitter and wait two frames before the next case.

At the top of the output, print RenderingServer.get_current_rendering_method(), RenderingServer.get_video_adapter_name(), and one sentence stating that headless Godot uses a dummy renderer, so GPU particle simulation and all drawing are not measured. Run it and paste the real output. Do not interpret a GPUParticles2D number as its real cost.
```

```bash
codex exec -s workspace-write -C . --json -o codex-last.txt "$(cat prompt2.txt)" > codex1.jsonl
```

The recorded run did not redirect standard input; Codex printed `Reading additional input from stdin...` and completed anyway. When running from a script, add `< /dev/null`, as the chapter does.

## Instructor verification commands

```bash
godot --headless --path godot --script res://tests/test_particles.gd
godot --headless --path godot --script res://test_input.gd
godot --headless --fixed-fps 60 --path godot --script res://tests/particle_cost.gd
godot --headless --path godot --script res://tests/particle_cost.gd
godot --headless --verbose --fixed-fps 60 --path godot --script res://test_input.gd
```
