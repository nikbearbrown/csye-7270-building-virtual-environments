# Module 11 — Animation and Interaction

CSYE 7270 · Fall 2026 · Week 11

## Executive summary

This module is about the wire between what the player does and what the character shows: in Godot 4.7.2, the `AnimationTree`, its state machine and blend nodes, and the tests that tell you whether the wire holds. Animation is where an agent's change can pass every check and still be wrong: a transition left at its default mode never fires, and a timing gap between physics and rendering can hold the wrong pose for a whole jump. You will replace the 3D platformer's hard ground-or-air switch with a three-state machine driven by the robot's physics, and write a scripted-input test for normal play and three edge cases. On 27 September 2026 that test found a real bug in the agent's machine, and the agent first called it a test problem. The fix is one transition. The build still does not show that the cross-fades look good or that the robot feels better; no person has played it. Those judgments are yours, marked here as HUMAN CHECK.

## The question

Hold Space in Godot's 3D platformer and the robot hops: it lands and jumps again on the same key press. Every hop has a landing. On some hops, the animation never finds out.

Here is the robot on one of them, one line per physics tick, from a trace of the new state machine before its final fix (columns trimmed):

```text
137 floor=true  vy=  0.00 state=fall
138 floor=false vy= 12.50 state=fall
139 floor=false vy= 12.32 state=fall
...
176 floor=false vy=  5.53 state=fall
```

On tick 137 the robot stands on the floor. On tick 138 it is flying upward at 12.5 units per second. The animation state says `fall` the whole time, so the robot plays its falling pose while it rises. On an earlier hop in a different trace, the same machine did see the landing.

How can a character be on the floor while its animation does not know? Why only sometimes? And what kind of test catches it every time instead of by luck?

## The ideas

### The AnimationTree plays clips through a graph

Module 10's `AnimationPlayer` plays one clip at a time. An [`AnimationTree`](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html) "does not contain its own animations. Instead, it uses animations contained in an AnimationPlayer node." Its `tree_root` is a single animation, a blend tree, a 1D or 2D blend space, or a state machine, and roots nest.

Every tunable number is a **parameter** addressed by path: `parameters/run/blend_amount`, `parameters/playback`. Code drives the tree by writing parameters. The path encodes the graph's nesting, so moving a node changes its path, and a script still writing the old path writes to nothing useful. The syllabus calls changes like this the "dangerous middle": they need a person to inspect them.

### Blends mix, state machines commit

Blend nodes mix inputs. `Blend2` and `Blend3` take a `blend_amount`, blend spaces take a `blend_position`, `TimeScale` takes a `scale`, and `OneShot` plays an animation once over whatever is below it, then fades back. **Filters** restrict a blend to named bones: the platformer's `gun` Blend2 is filtered to eleven upper-body bones, so shooting replaces the arms while the legs keep running. A [`BlendSpace1D`](https://docs.godotengine.org/en/stable/classes/class_animationnodeblendspace1d.html) crossfades between adjacent clips on an axis (idle at 0, walk at 0.5, run at 1, fed normalized speed), so the gait follows the speed with no state change. For frame-by-frame 2D sprites, a BlendSpace2D's discrete mode plays the nearest clip instead of blending.

Blends suit continuous input. They are the wrong tool when the character must commit: a jump that has started should play its takeoff even if the player lets go.

### The state machine, taken apart

An [`AnimationNodeStateMachine`](https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachine.html) holds states connected in a graph, with built-in `Start` and `End` nodes. Each connection is an [`AnimationNodeStateMachineTransition`](https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachinetransition.html):

| Setting | Values (4.7.2 default first) | What it decides |
|---|---|---|
| `switch_mode` | Immediate, Sync, At End | Blend now, seek to the old playback position, or wait for the state to finish |
| `advance_mode` | Enabled, Disabled, Auto | Enabled: only `travel()` uses it. Auto: used when its condition or expression is true |
| `advance_expression` | an expression | Evaluated against the tree's `advance_expression_base_node` (default: the tree itself) |
| `xfade_time` | 0.0 | Cross-fade length in seconds |

An `advance_condition` is the simpler cousin: a boolean parameter your code sets, which only checks for true. Read the `advance_mode` row twice. The default is Enabled, not Auto. A transition with an expression and the default mode never fires on its own. The first agent in this module's run made exactly this mistake.

You steer a running machine through the [`AnimationNodeStateMachinePlayback`](https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachineplayback.html) object at `parameters/playback`. `travel(to)` follows the shortest path to another state. A trap for testers: `get_current_node()` changes to the next state immediately after a cross-fade begins, so it cannot show that a long fade is still running. Read `get_fading_from_node()` for that.

There are two ways to connect a machine to gameplay, and they fail differently. **Pull:** Auto transitions evaluate expressions such as `is_on_floor()` each time the tree processes. It fails when gameplay changes and changes back between two tree updates. **Push:** gameplay code calls `travel()` when the action happens. It fails when a code path forgets to, or when two calls in one frame race.

### Where timing gaps come from

The player's physics run in `_physics_process`; the tree runs in the idle step by default. The platformer runs 120 physics ticks per second, and a test at `--fixed-fps 60` renders 60 frames per second, so every frame holds two ticks. A robot that touches the floor at the end of one tick and leaves it during the next, inside one frame, has landed and taken off between two tree updates. Neither system is wrong; that is the sampling rate of "is the player on the floor?" You can process the tree in physics frames, push state from code, or add transitions that tolerate a missed sample. The hands-on adds one.

### Where the character's state lives

Before adding a state machine, find the one the game already has; the next section shows three Walker builds that keep it in three different places. A second state machine that disagrees with the first is worse than none, so the hands-on keeps the platformer's physics as the single authority. Root motion is the related decision: select a bone as `root_motion_track` and the clip's movement is cancelled on screen and handed to you to apply, which gives movement authority to the animation data. The platformer leaves that track empty.

### Generated motion: what it can supply, and what it cannot

The old course's Mini-Assignment 2 asked for a 15 to 30 second clip from AI animation tools, submitted as an MP4 with the tool used for each element, screenshots of the iterations, and a reflection comparing the result with traditional animation. The revised syllabus keeps the subject but changes the deliverable to a playable state that responds to input and has been tested. Three habits still hold: record which tool made each element, keep the iterations and not only the survivor, and say how the result compares with a hand-made method.

An MP4 is pixels, with no skeleton, loop point or event keys. A game needs one of two things from it:

1. **Frames, for 2D.** Cut the clip, pack a sprite sheet, and play it through `AnimatedSprite2D` or a keyed `Sprite2D.frame` ([2D sprite animation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html)). You still supply a clean loop (the old Assignment 6's rule: first and last frame must be the same), a steady pivot, matching silhouette sizes, and transparency. A video model does not know your collision rectangle.
2. **Pose data, for 3D.** Markerless motion-capture services estimate a skeleton per video frame and export animation files. Godot's import documentation lists glTF 2.0 (recommended), `.blend`, DAE, OBJ and FBX; BVH is not listed, so convert it outside Godot. You still supply retargeting onto your bones, foot contacts that do not skate, a root-motion decision, and cleanup where the estimator lost a limb.

What generation never supplies is the state logic. A generated jump clip does not know that releasing Space cuts the jump short, that holding Space re-jumps on landing, or that reset can teleport the robot mid-air. Those decisions live in your files and are testable the same way whatever made the clip, which is why this module's test never looks at a pixel. Whether the clip reads as a jump is a HUMAN CHECK.

Provenance travels with the file: record the tool, the input (your own video, or someone else's performance), the terms, the date, and what you changed. Do not capture anyone who has not agreed. The cheapest tool is still a motion reference: film yourself doing the action and step through it. At 30 fps, 0.1 s is three frames, the number to compare your `xfade_time` against.

## The Walker example: walker-3d-platformer

**What it is.** [`walker-3d-platformer`](https://github.com/nikbearbrown/walker-3d-platformer) is a public Walker adaptation of Godot's 3D platformer demo (`3d/platformer` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`), keeping the upstream MIT license; only the project name differs. The player is a `CharacterBody3D` in `player/player.gd`, and its model brings a `Skeleton3D` and an `AnimationPlayer` with eight clips, among them `idle`, `walk`, `run`, `jump` and `falling`. `jump` and `falling` are 0.433 s each. There is no landing clip.

**How its animation is wired.** The tree is a blend tree, not a state machine:

```text
output ← gun (Blend2, filtered to upper-body bones)
           ├─ 0: state (Blend2)
           │      ├─ 0: scale (TimeScale 1.5) ← run (Blend2: idle ↔ speed)
           │      │                              speed (Blend2: walk ↔ run)
           │      └─ 1: air_dir (Blend2: jump ↔ falling)
           └─ 1: shooting_standing
```

Every physics tick `player.gd` writes five parameters. `state` is an integer, 0 on the floor and 1 in the air, written into a Blend2 with no fade: in a run on 27 September 2026 at `--fixed-fps 60`, it went from 0 to 1 in one tick at takeoff and back in one tick at landing. That is a cut. Whether the cut shows is a HUMAN CHECK.

**What its checks establish.** Its input probe loads the real scene, presses ordinary movement, jump, shoot and reset actions, and records 600 frames at fixed 60 FPS. Two runs passed four assertions: displacement, upward jump velocity, a `Bullet` node created, and a return near the start after reset. **What remains unverified:** coin pickup, enemy impact, camera image, audio, physical controls and fun, and nothing checks animation at all. The four assertions would pass with the `AnimationTree` deleted.

**Two neighbours.** [`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd) draws Clawd in code, with no `AnimationPlayer` or `AnimationTree`. One function in `features/player/player.gd` picks the animation every frame:

```gdscript
func visual_animation() -> String:
	var context: String = get_parent().player_animation_context()
	if context == "complete": return "celebrate"
	if context == "failed": return "error"
	if not enabled: return "idle"
	if not is_on_floor(): return "jump"
	if absf(velocity.x) >= 100: return "run"
	if absf(velocity.x) > 8: return "walk"
	return "idle"
```

That is a complete state machine as a priority list, and its price is visible: no blends, rising and falling look the same, and a speed near 100 px/s flips between run and walk. Its `test_clawd.gd` passed 1,950 checks over 162 animation samples on 27 September 2026, but its presentation checks set `velocity.x` directly and ask the selector what it would show. That tests the selector, not a key press.

In [`walker-2d-finite-state-machine`](https://github.com/nikbearbrown/walker-2d-finite-state-machine), pressing Space and then F while airborne pushes an Attack state over Jump, and the body hangs at 79.3 px for about 54 frames (0.45 s) at `--fixed-fps 120`, because `Jump.update()` no longer runs. Its 18-check keyboard test never presses F in the air. Bug or feature is a judgment a test cannot make; once you decide, a test should pin it.

## Predict → Build It → Use It → Ship It → Verify

### 1. Predict

Answer in writing before you delegate anything.

1. The tree evaluates once per rendered frame, and physics runs twice per frame (120 ticks, 60 fps). If the robot lands on one tick and jumps on the next, what does the tree see?
2. A 0.1 s cross-fade replaces a one-tick cut. What changes on screen? What changes in gameplay?
3. Press reset while the robot is rising. Which state should the machine be in a few frames later, and what evidence would you accept?
4. List every transition out of `fall` the machine needs. Write your list before you read the agent's.

### 2. Build It

Set up your own copy from the upstream demo (the public Walker repository holds the same project). If you kept `godot-demo-projects` from Module 10, reuse it.

```bash
git clone https://github.com/godotengine/godot-demo-projects.git
```

```bash
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

```bash
mkdir -p motion-states
```

```bash
cp -R godot-demo-projects/3d/platformer motion-states/godot
```

Then, inside `motion-states`:

```bash
git init
```

```bash
godot --headless --path godot --import
```

```bash
git add -A
```

```bash
git commit -m "baseline: 3d/platformer at a3b5c11"
```

**Prompt 1: the state machine and the test.** Save it as `prompt-1.txt` in `motion-states`.

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

The prompt names the invariant (the machine follows physics, never input), the single structural change, and what not to touch. It forbids the three shortcuts that make animation tests meaningless: writing velocity, writing tree parameters, calling `travel()`. Its last paragraph hands the agent a judgment, test or setup, and in the recorded run that judgment went wrong. Ask for a trace.

With Claude Code:

```bash
claude -p "$(cat prompt-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --disallowedTools "Skill" --max-turns 80 --output-format stream-json --verbose > session-1.jsonl
```

With Codex, the optional alternative that took over the recorded run when Claude Code's usage limit ended the session:

```bash
codex exec --sandbox workspace-write --json -o last-message-1.txt "$(cat prompt-1.txt)" < /dev/null > codex-session-1.jsonl
```

**Prompt 2: fix the setup, from your own trace.** If check 2 fails, do not accept "the test is wrong" until you have logged `is_on_floor()`, `velocity.y` and `get_current_node()` on every physics tick of the hop; the record's trace script is `reviewer/trace_check2_copy_of_run1_test.gd` in the [example folder](../../examples/11-animation-and-interaction/README.md). If your trace shows the machine in `fall` while the robot rises, send:

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

**Prompt 3: make the edge case impossible to miss.** Which tick of a frame the landing falls on depends on everything that ran before it, so a check like 2a can flip after an unrelated edit. Pin both cases:

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

Then prove the stronger test is stronger. Put the pre-fix `player.tscn` back in a throwaway copy and run the new test against it. It must fail. A test that passes on the broken version has not tested the fix.

### 3. Use It

Run the game yourself (F5 in the editor, or `godot --path godot`) and play the edges. Items 1 to 5 are **HUMAN CHECK**s: record a verdict and the date, not a test result.

1. **Hold Space** and hop ten times. On one tick offset the robot rises for 0.1 s still in its ground blend before the jump pose arrives. Can you see it? Does it read as a stumble, or as weight?
2. **Reverse at full run.** The machine should stay in `ground`. Does the turn read?
3. **Reset mid-jump** with the `reset_position` action. Does the robot snap to a falling pose?
4. **Shoot mid-jump.** The upper body should take the shooting pose over the jump or fall pose. Does it?
5. **Compare with a motion reference.** Film yourself doing a small hop in place, count the frames from landing to leaving the floor again, and compare with the 0.05 to 0.1 s cross-fades. Write down the numbers and your verdict.
6. While the game runs, switch the Scene dock to **Remote**, select the `AnimationTree`, and read its parameters in the Inspector ([debugging tools](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html)). This is observation, not judgment.

### 4. Ship It

Commit in the order you worked: baseline, the agent's state machine and test, the setup fix, the stronger test. In `FRICTIONAL.md`, record every check that failed on the way and what you decided about it, including any time the agent, or you, called a failure a test problem. Record your play verdicts as verdicts, with dates.

The Brutalist skill that fits is `godot-walkthrough` (the toolkit's original spelling, `godot-waikthrough`, is also accepted). The Week 11 syllabus note is "Check feel and readability through play," so a played walkthrough of the four edges is the natural film, and Assignment 8 asks for one. Use the course-provided Brutalist checkout, and request the update if your copy lacks the skill.

### 5. Verify

```bash
godot --headless --path godot --fixed-fps 60 --script res://tests/test_motion_states.gd
```

Wrap it in `timeout 180` if your shell has it ([Chapter 0](../../chapters/00-the-toolchain.md) says where it comes from on macOS): a script error before `quit()` leaves headless Godot running forever, as happened in the recorded run. Keep `--fixed-fps 60`. Without it the final test passed 14 of 14 in one run and failed 5b and 1b in two others, and a test that counts frames needs its time step pinned. Then re-run your movement checks on the final scene. The public repository keeps an input probe in `tests/input_probe.gd`, outside `godot/`; ask Claude Code how it runs, then run it yourself. On the instructor's final version it reported jump, movement, projectile and reset all true.

**A pass establishes** that under these scripted inputs, at 60 fps with 120 physics ticks, the machine's state follows the robot's physics, including both tick offsets of a held-jump landing, and the old movement still works. **It does not establish** that the cross-fades look right, that the jump reads as a jump, or that a player likes it.

## What the agents got wrong

In the recorded run (Claude Code 2.1.150 with `claude-sonnet-4-6`, then Codex CLI 0.153.4, on 27 September 2026) an agent's "done" was a claim.

**An invented property and an orphaned process.** Claude Code gave the state machine a `start_node` property that does not exist. Its diagnostic script died with a script error before `quit()`, so headless Godot kept running for about half an hour until another session stopped it. The error text exposed the invention; `timeout` would have ended the process.

**Transitions that could never fire.** The agent's five expression transitions kept the default `advance_mode` (Enabled), so nothing moved the machine on its own. It caught this itself and switched all five to Auto, only after the state failed to follow the jump.

**A real bug filed as a test problem.** After the agent changed the test's own timing, checks 2a and 2b began failing, and it wrote that this was a test fix. A check that flips when only timing changed is the signature of a timing bug. The instructor's per-tick trace showed the machine in `fall` while the robot rose. The agent had decided without a trace; its frame-count edits would at best have moved the landing back onto the lucky tick.

**A green test that hides a lag.** The final test passes at both tick offsets, yet traces show two behaviors for one held key. At offset 1 the machine goes straight from `fall` to `jump`. At offset 0 it sees the landing and starts a 0.1 s fade to `ground`, so the robot rises in its ground blend and `jump` starts 12 ticks after the landing. No check forbids `ground` while rising. Whether 0.1 s is acceptable is a feel decision, still open, and yours.

## If you know Unity or Unreal

Unity and Unreal were not run for this module; the comparisons come from their official documentation, checked on 27 September 2026.

| Godot 4.7.2 | Unity 6.6 | Unreal Engine 5.8 |
|---|---|---|
| `AnimationTree` + state machine | Animator Controller | Animation Blueprint + State Machine |
| `xfade_time` | Transition Duration | Transition Duration |
| `advance_expression` | Conditions on parameters | Transition rule (boolean graph) |
| `BlendSpace1D` / `2D` | 1D / 2D Blend Tree | Blend Space |
| Filtered Blend2 | Layer + Avatar Mask | Layered blend per bone |
| `root_motion_track` | Root Transform | Root Motion Mode |

The biggest difference for an agent workflow is what the agent can read. In Godot the machine, its transitions and its expressions are text in a `.tscn` file, so a change is a diff you can read. Unity controllers are YAML text under Force Text but long and positional, and Unreal's state machines and Blend Spaces are `.uasset` files, reached through editor Python or C++. The full comparison is in [Chapter 11](../../chapters/11-animation-and-interaction.md).

## Practice assessment (ungraded)

Answer these in your own words, then check the source. The Canvas practice quiz for this module covers related ground in multiple choice. Do not paste Claude's explanation as proof of your understanding; ask it to question you, then answer and check the source yourself.

1. In the one-transition fix, name the two places the new transition had to be added, and say what happens if only the first is added. Use the diff in the example folder.
2. Using the class reference, explain why `travel()` could use an Enabled transition while the Auto behavior never happened.
3. A check reads `get_current_node()` within the cross-fade plus two frames after reset. Would it pass for a machine with a five-second cross-fade out of `jump`? What would you read instead?
4. For `walker-jumpman-clawd`, write the line you would add for a distinct falling pose, and a test for it that uses key input rather than setting `velocity`.
5. State one thing the headless test establishes and one judgment only play can supply.

## The next step

This module completes the material for Assignment 8, "Animation Wired to Player Actions." It covers Modules 10 and 11, opened with Module 10, and is due about Day 80 (Canvas dates govern); its page sets the exact task and the required `godot-walkthrough` film. This lesson adds no graded deliverable. Module 12, audio and triggers, comes next. The long reading is the companion chapter, [Chapter 11 — Animation and Interaction](../../chapters/11-animation-and-interaction.md).
