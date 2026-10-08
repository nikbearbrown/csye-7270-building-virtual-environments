# Prompts — Example 10

Exact text sent to the agents on 2026-09-27, in order. Each prompt was sent as the whole of the command-line prompt argument (`"$(cat prompt.txt)"`), with the scratch repository root as the working directory.

| # | Prompt | CLI and model | Command | Time (UTC) | Outcome |
|---|---|---|---|---|---|
| 1 | Pin the timing | Claude Code 2.1.150, `claude-sonnet-4-6` | `claude -p "$(cat prompt-1-pin.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > session-1-pin.jsonl` | 17:58–18:57 | Stopped on the account session limit after 20 turns; test not written |
| 1b | Pin the timing (same text) | Codex CLI 0.153.4, configured `gpt-5.6-sol`, low reasoning effort | `codex exec --sandbox workspace-write --json -o codex-1-pin-last.txt "$(cat prompt-1-pin.txt)" < /dev/null > codex-1-pin.jsonl` | 18:58–19:03 | Created `godot/tests/test_sword_timing.gd`; 20/20; four anomalies reported |
| 2 | Hitbox window in the animation | Codex (as above) | same form | 19:04–19:05 | 3 failures, correctly classified (2 asked for, 1 not) |
| 3 | Every swing restarts | Codex | same form | 19:06–19:07 | One line, `$AnimationPlayer.seek(0.0)`; invariants pass; 10 timing pins moved |
| 4 | Re-pin after approval | Codex | same form | 19:08–19:09 | Constants only; 20/20 |

The printed command in Chapter 10 adds `--disallowedTools "Skill"` to the Claude Code command. Our run did not include it; it was added afterwards on a report that a nested session elsewhere had tried to invoke a settings-writing skill.

## Prompt 1-pin

```text
Inspect first; do not change any game file. Read godot/player/weapon/Sword.tscn
(the AnimationPlayer and its animation library), godot/player/weapon/sword.gd,
godot/player/player_state_machine.gd, godot/player/states/combat/attack.gd and
the existing godot/test_combo.gd. Tell me, with line references, which code and
which animation keys decide when the sword's hitbox (Area2D.monitoring) is on,
when the combo buffer opens, and when the next swing may start.

Then write ONE new file, godot/tests/test_sword_timing.gd: a headless
SceneTree script that pins the sword's CURRENT timing before anyone changes
the animation. Rules:
- Load res://Demo.tscn and drive it only with keyboard events sent through
  Input.parse_input_event (F is attack). Never call attack(), _change_state()
  or AnimationPlayer methods, and never assign to sword or player variables.
- Step one frame at a time with `await process_frame`. The test is run with
  --fixed-fps 120 and the project runs 120 physics ticks per second, so one
  frame is one physics tick is 1/120 s. Count frames from the frame the F press
  is sent.
- Every frame, record: AnimationPlayer current_animation and
  current_animation_position, sword.visible, sword.monitoring,
  sword.rotation_degrees, sword.attack_input_state,
  sword.ready_for_next_attack, sword.combo_count, and the player state name.

Scenarios: (a) one F tap, then wait for Idle; (b) a three-swing combo made of
F taps sent 20 frames after each swing starts; (c) an F tap sent 5 frames
into a swing.

Print PASS/FAIL lines in two labelled groups.
TIMING (numbers we may change on purpose later): for scenario (a) the frame
the hitbox turns on and the frame it turns off, the frame the combo buffer
opens, the frame ready_for_next_attack becomes true, and the frame the player
is back in Idle; for scenario (b) the frame, animation name, animation
position and rotation_degrees at the start of each swing, and how far
rotation_degrees travels during each swing; for scenario (c) whether the
early tap chains.
INVARIANT (must survive any timing change): the hitbox is never on while the
player is not in Attack; in Idle the sword is hidden and not monitoring; every
swing (every increase of combo_count) has at least one frame with the hitbox
on; swing 3 plays attack_medium with damage 3; a fourth tap does not start a
fourth swing; the whole combo is one push and one pop of the Attack state;
the next attack after the combo starts at combo 1.

Measure first (a temporary print-only run is fine; tell me about any file you
create), then write the measured numbers into the test as named constants
with the comment "measured on baseline 2026-09-27". If a measurement
contradicts what the code or the animation names suggest, keep the measured
value and list it under a heading ANOMALIES in your final message; do not fix
it. End the test with a RESULT line and quit(1) on any failure. Run it from
the repository root with:
godot --headless --path godot --script res://tests/test_sword_timing.gd --fixed-fps 120
and paste the real output. Do not commit.
```

## Prompt 2-hitbox-window

```text
One concern: the sword's hitbox is live for the whole attack animation,
including the wind-up and the recovery. Make it live only while the blade
is sweeping.

Do it in the animation, not in code. In godot/player/weapon/Sword.tscn add a
`monitoring` value track with Discrete update mode to attack_fast (true at
0.0 s, false at 0.15 s) and to attack_medium (true at 0.05 s, false at
0.25 s). Make the animation the only thing that turns monitoring on during
an attack: remove the line in sword.gd that sets monitoring = true when an
attack starts, and keep the Idle branch that sets it false.

Do not change: the rotation or scale keys, the method-track keys (0.1 s and
0.25 s), animation lengths, the combo table, the state machines, any other
scene, or any test file. Do not edit godot/tests/test_sword_timing.gd to make
it pass.

Then run, from the repository root:
godot --headless --path godot --script res://tests/test_sword_timing.gd --fixed-fps 120
godot --headless --path godot --script res://test_input.gd --fixed-fps 120
godot --headless --path godot --script res://test_combo.gd --fixed-fps 120
and report every FAIL line. For each FAIL, say whether it is a change I asked
for or a change I did not ask for, and why it happened. Do not commit.
```

## Prompt 3-restart-swing

```text
One concern: in godot/player/weapon/sword.gd, a combo swing that replays the
animation already playing does not restart it. The timing test shows swing 2
starting attack_fast at position 0.25 s, travelling 0 degrees, and, since
the hitbox window moved into the animation, never turning the hitbox on.
Make every swing start its animation from 0.0 s. Change sword.gd only, with
the smallest change that does it. Do not change Sword.tscn, the combo table,
or any test.

Then run, from the repository root:
godot --headless --path godot --script res://tests/test_sword_timing.gd --fixed-fps 120
godot --headless --path godot --script res://test_input.gd --fixed-fps 120
godot --headless --path godot --script res://test_combo.gd --fixed-fps 120
and report every FAIL line. For each, say whether it follows from this
change, and whether it is a behavior a designer now has to approve. Do not
commit.
```

## Prompt 4-repin

```text
I have reviewed the ten TIMING failures from the last run and approve them
as the new intended behavior: the hitbox is live only inside the keyed
window, every swing restarts its animation, and the one-frame shifts that
follow from the restart. Update only the measured TIMING constants in
godot/tests/test_sword_timing.gd to the values the game now produces, and
change their comment to "re-pinned 2026-09-27 after approved changes:
hitbox window keyed in the animation; every swing restarts". Do not change
any INVARIANT check, any tolerance, or any game file. Then run, from the
repository root:
godot --headless --path godot --script res://tests/test_sword_timing.gd --fixed-fps 120
and paste the real output. Do not commit.
```

