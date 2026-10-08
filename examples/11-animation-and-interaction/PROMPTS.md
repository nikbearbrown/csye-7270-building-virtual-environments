# Prompts — Example 11

Exact text sent to the agents on 2026-09-27, in order, each as the whole prompt argument (`"$(cat prompt.txt)"`), from the scratch repository root. Prompt 2 was written by us after tracing the failure (`reviewer/trace_check2_copy_of_run1_test.gd`); it is not agent output.

| # | Prompt | CLI and model | Command | Time (UTC) | Outcome |
|---|---|---|---|---|---|
| 1 | State machine + edge-case test | Claude Code 2.1.150, `claude-sonnet-4-6` | `claude -p "$(cat prompt-1-state-machine.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 80 --output-format stream-json --verbose > session-1-state-machine.jsonl` | started 18:07; 49 turns / 44 min of session time; process exited 19:05 | Stopped on the account session limit; our run of its final state: 9/11 (2a, 2b fail) |
| 2 | Add `fall → jump` | Codex CLI 0.153.4, configured `gpt-5.6-sol`, low reasoning effort | `codex exec --sandbox workspace-write --json -o codex-2-missed-contact-last.txt "$(cat prompt-2-missed-contact.txt)" < /dev/null > codex-2-missed-contact.jsonl` | 18:58:26–18:59:09 | One transition added; 11/11 |
| 3 | Check 2 at both tick offsets | Codex (as above) | same form | 19:00:15–19:01:06 | Test-only change; 14/14 |

The chapter's printed Claude Code command adds `--disallowedTools "Skill"`; our run did not include it.

## Prompt 1-state-machine

```text
Inspect first; change nothing yet. Read godot/player/player.gd and the
AnimationTree inside godot/player/player.tscn (its BlendTree and the
parameters player.gd writes). Explain, with line references, how the tree
currently chooses between ground and air animation, and what the blend does
on the physics tick the player leaves or touches the floor.

Then make one change: replace the `state` Blend2 and the `air_dir` Blend2
with an AnimationNodeStateMachine named `motion`, placed where `state` is in
the existing BlendTree, so the `gun` node still layers shooting on top. The
state machine has three states:
- ground: the existing idle/walk/run blend (the `run`, `speed` and `scale`
  nodes and their animations), unchanged, as a nested BlendTree;
- jump: the `jump` animation, while the player is airborne and rising;
- fall: the `falling` animation, while the player is airborne and not rising.
Drive every transition with an advance_expression evaluated on the Player
(set AnimationTree.advance_expression_base_node), using only the player's
physics state (is_on_floor(), velocity.y), never input. Give each transition
a cross-fade between 0.05 and 0.15 s. Update the parameter paths player.gd
writes so the ground blend and the gun blend still respond, and delete the
lines that wrote state/blend_amount and air_dir/blend_amount. Do not change
movement, jumping, shooting, constants, input actions, the camera, any other
scene, or the stage.

Then write godot/tests/test_motion_states.gd, a headless SceneTree script
that loads res://game.tscn and drives the player ONLY with Input.action_press
and Input.action_release (never set position, velocity or tree parameters,
and never call travel()). Step frame by frame. Each frame, record the
physics state (is_on_floor(), velocity.y, horizontal speed) and
parameters/motion/playback get_current_node(). Check:
1. Normal: standing gives ground; run forward, then jump: the machine visits
   jump, then fall, then ground, in that order.
2. Jump held through landing (the player re-jumps as soon as it lands): over
   three hops the machine enters jump on every hop, and is never in fall
   while the player rises, or in jump or fall while the player stands on the
   floor, for longer than the cross-fade plus two frames.
3. Direction reversal at full speed: the machine stays in ground the whole
   time, and the ground run blend falls and then rises again.
4. Interrupt: press reset_position while rising: the machine leaves jump
   within the cross-fade plus two frames after the reset, and reaches ground
   once the player lands.
5. Shoot during a jump: the gun blend is above zero while the machine is in
   jump or fall, and the jump, fall, ground order is unchanged.
Print one PASS/FAIL line per check, a RESULT line, and quit(1) on any
failure. Run it from the repository root with:
godot --headless --path godot --fixed-fps 60 --script res://tests/test_motion_states.gd
and paste the real output. If a check fails, find out whether the test or
the animation setup is wrong, fix the one that is wrong, and tell me which it
was and why. Do not commit.
```

## Prompt 2-missed-contact

```text
One concern. godot/tests/test_motion_states.gd fails checks 2a and 2b. A
per-tick trace of check 2 shows why: with Space held, the player lands on
one physics tick and jumps again on the next, inside the same rendered
frame. The AnimationTree only evaluates once per frame, so it never sees
is_on_floor() == true, stays in `fall`, and has no transition out of `fall`
while the player is rising (velocity.y = 12.5 and above zero for the next
~70 ticks).

Fix the animation setup, not the test: in godot/player/player.tscn add one
transition from `fall` to `jump`, advance_mode Auto, advance_expression
"not is_on_floor() and velocity.y > 0.0", xfade_time 0.05. Change nothing
else: not the other transitions, not player.gd, not the test.

Then run from the repository root:
godot --headless --path godot --fixed-fps 60 --script res://tests/test_motion_states.gd
and paste the real output. Do not commit.
```

## Prompt 3-both-parities

```text
One concern: make check 2 in godot/tests/test_motion_states.gd independent
of luck. The game runs 120 physics ticks per second and the test runs at
--fixed-fps 60, so every rendered frame holds two physics ticks. Whether a
held-jump landing is visible to the AnimationTree depends on which of those
two ticks the landing falls on. Run the three-hop sequence of check 2 twice:
once as now, and once starting exactly one physics tick later (await one
extra physics_frame before pressing jump). Report 2a, 2b and 2c separately
for each run, labelled "(offset 0)" and "(offset 1)".

Change only the test. Do not change player.tscn, player.gd or any
threshold, and do not remove any existing check. Then run from the
repository root:
godot --headless --path godot --fixed-fps 60 --script res://tests/test_motion_states.gd
and paste the real output. Do not commit.
```

