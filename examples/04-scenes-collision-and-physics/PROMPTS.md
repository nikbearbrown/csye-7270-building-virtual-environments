# Prompts and command lines — Chapter 4

## Executive summary

The one prompt used for both agents, word for word, and the exact command lines, run on 27 September 2026 from the project root of each scratch copy. The prompt was saved as `prompt-shield.txt` next to the project folder. It encodes the student's Predict answers as requirements: the pickup's own layer, the unchanged mob mask, the expiry-with-overlap rule, and the group cleanup.

## The prompt

```text
This is walker-2d-dodge-the-creeps, a Walker adaptation of Godot's "Dodge the
Creeps" demo (Godot 4.7.2, GDScript). Read README.md, FRICTIONAL.md,
godot/project.godot, main.tscn, main.gd, player.tscn, player.gd, mob.tscn,
mob.gd and godot/test_input.gd before editing anything.

Add ONE mechanic: a shield pickup.
- New scene godot/pickup.tscn with pickup.gd: an Area2D root with its own
  CollisionShape2D, drawn in code (no new art files). main.gd instances it
  from a new PickupTimer at a random on-screen position during play.
- Give pickups their own named 2D physics layer in project.godot
  ([layer_names]). Change only the masks needed so the Player detects
  pickups. Mobs keep collision_mask = 0; the Player keeps collision_layer = 1.
- Touching a pickup frees it and shields the Player for 3.0 seconds. While
  shielded, touching a mob does not end the game. Show the shield on the
  Player (a tint or a drawn ring is enough).
- If the shield ends while a mob still overlaps the Player, the Player is hit
  at that moment. body_entered fires only when an overlap begins.
- new_game() clears pickups and any shield; game_over() stops the PickupTimer.

Invariants: do not change player speed, mob speeds, the spawn path, existing
timer intervals, the HUD, or any asset file. Do not edit godot/test_input.gd;
its 14 checks must still pass.

Write godot/tests/test_shield.gd, a SceneTree script in the style of
test_input.gd: start the game by clicking the Start button; place one pickup
100 px to the Player's right and collect it with real D-key input; then use a
frozen mob fixture (as test_input.gd does) to check that shielded contact
neither hides the Player nor stops the timers, that the hit happens within 10
physics frames after the shield expires while the mob still overlaps, and that
restart clears pickups and the shield. Await physics frames; never call signal
handlers directly or set the shield state by hand.

Run both tests with `godot --headless --path godot --script <res:// path>` and
report the real output. Do not commit. End with a short list of what these
headless tests cannot tell us.
```

## Claude Code (as run)

Started 2026-09-27T17:55:35Z, finished 18:11:38Z, exit 0.

```bash
claude -p "$(cat ../prompt-shield.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > ../session.jsonl 2> ../session.stderr
```

The session reported `model: claude-sonnet-4-6` (the print-mode default on this account), `permissionMode: acceptEdits`, 33 turns, and a CLI-reported cost of $1.35.

## Codex (as run)

Started 2026-09-27T18:06:21Z, finished 18:08:56Z, exit 0. Run from `codex-run/walker-2d-dodge-the-creeps/`, a clone of the same baseline, imported first.

```bash
codex exec --ignore-user-config -m gpt-5.6-sol --sandbox workspace-write --json -o ../codex-last-message.md "$(cat ../../prompt-shield.txt)" > ../codex-session.jsonl 2> ../codex-session.stderr
```

`--ignore-user-config` kept the machine's Codex plugins and notification hook out of the run. `-m gpt-5.6-sol` is the model that configuration names. The run printed `Reading additional input from stdin...`. Add `< /dev/null` when you run `codex exec` from a script.

## Reviewer commands (not agents)

```bash
godot --headless --path godot --script res://test_input.gd --fixed-fps 60
```

```bash
godot --headless --path godot --script res://tests/test_shield.gd --fixed-fps 60
```

```bash
godot --headless --path godot --script /absolute/path/to/verify_shield_timing.gd --fixed-fps 60
```

Mutation (Claude Code's version): set `const SHIELD_DURATION := 0.5` in `godot/player.gd`, rerun the last two commands, restore the file. Mutation (Codex's version): set the `ShieldTimer` node's `wait_time = 0.5` in `godot/player.tscn`, rerun the last two commands, restore the file.
