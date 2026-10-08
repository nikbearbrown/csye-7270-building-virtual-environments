# Chapter 11 — Animation and Interaction

CSYE 7270 · Fall 2026 · Week 11

## Executive summary

**What this chapter is.** How a player's actions drive animation states in Godot 4.7.2 (`AnimationTree`, state machines, blend spaces, one-shots, root motion), and how to test the wiring. The Week 11 syllabus line is "Connect animation states to player actions. Use motion references and test blends and edge cases," with the note "Check feel and readability through play."

**What we built, and what happened.** In the 3D platformer, an agent replaced a hard ground-or-air switch with a three-state machine (ground, jump, fall) driven by the robot's physics, and wrote a scripted-input test for normal play and three edge cases. The test found a real bug in the new machine: when the robot lands on one physics tick and jumps on the next, inside a single rendered frame, the tree never sees the landing and stays in `fall` for the whole rise. The first agent, Claude Code, classified that failure as a test problem and began adjusting frame counts before it hit the account's usage limit. A one-transition fix, a test that runs the edge case at both tick offsets, and a mutation check against the old scene closed it.

**What this does not establish.** Whether the new cross-fades look good, whether a 0.1 s landing blend in mid-air reads as a stutter, and whether the robot feels better to play. Those need a person, a screen and, ideally, a motion reference.

---

## The question

Hold Space in Godot's 3D platformer and the robot hops: it lands and jumps again on the same key press. Every hop has a landing. On some hops, the animation never finds out.

Here is the robot on one of them, one line per physics tick, from a trace of the new state machine before its final fix (columns trimmed; the full log is in the example folder):

```text
137 floor=true  vy=  0.00 state=fall
138 floor=false vy= 12.50 state=fall
139 floor=false vy= 12.32 state=fall
...
176 floor=false vy=  5.53 state=fall
```

On tick 137 the robot is standing on the floor. On tick 138 it is flying upward at 12.5 units per second. The animation state says `fall` the whole time, so the robot plays its falling pose while it rises. On an earlier hop in a different trace, the same machine did see the landing.

How can a character be on the floor and its animation not know? Why only sometimes? And what kind of test would catch it every time rather than by luck?

---

## Ideas you need

### AnimationTree plays an AnimationPlayer's clips through a graph

Chapter 10's `AnimationPlayer` plays one clip at a time. An [`AnimationTree`](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html) "does not contain its own animations. Instead, it uses animations contained in an AnimationPlayer node." Each time it processes, it decides how much of each clip goes into the final pose. Both are `AnimationMixer`s, so Chapter 10's timing rules still apply. In Godot 4.7.2 an `AnimationTree` defaults to idle processing, to `deterministic = true`, and to force-continuous discrete tracks ("the default behavior for AnimationTree"). We printed all three from the binary.

The tree's `tree_root` is one of five root node types: `AnimationNodeAnimation` (one clip), `AnimationNodeBlendTree` (a graph of nodes), `AnimationNodeBlendSpace1D`, `AnimationNodeBlendSpace2D`, and `AnimationNodeStateMachine`. Roots nest. A state machine's states can be blend trees, and a blend tree can contain a state machine.

Every tunable number in the graph appears as a **parameter** on the `AnimationTree` node, addressed by path: `parameters/run/blend_amount`, `parameters/OneShot/request`, `parameters/playback`. Code drives the tree by writing parameters. The path encodes the graph's nesting. Move a node inside another node and its path changes, and any script still writing the old path now writes to nothing useful. The syllabus calls this kind of thing the "dangerous middle", changes involving resource paths and scene references that need a human to inspect them, and parameter paths are a clean example.

### The blend-tree nodes you will use

We listed each node's parameter paths from a tree built in the 4.7.2 binary.

| Node | What it does | Parameter code writes |
|---|---|---|
| Blend2 / Blend3 | Mix two or three inputs by a blend value | `blend_amount` (0 to 1; −1 to 1 for Blend3) |
| Add2 / Add3 | Add an input on top, additively | `add_amount` |
| OneShot | "This node will execute an animation once and return when it finishes." | `request` (fire, abort, fade out) |
| TimeScale | Scale the speed of its input | `scale` |
| TimeSeek | Seek its input to a time | `seek_request` |
| Transition | "This node is a simplified version of a StateMachine": pick one input by index, with cross-fade | `transition_request` |
| BlendSpace1D / 2D | Blend clips placed on a line or a plane | `blend_position` |
| StateMachine | States and transitions, controlled through a playback object | `playback` |

Two features do most of the work in real characters. **Filters** restrict a blend to named bones or tracks. The 3D platformer's `gun` Blend2 is filtered to eleven bones (`MASTER`, `chest`, `head`, `headtracker`, `hip`, both arms and forearms, `vent`, `waist`), so the shooting pose replaces the upper body while the legs keep running. **OneShot** plays an animation once over whatever is below it and fades back. The documentation's call is `animation_tree.set("parameters/OneShot/request", AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE)`.

### BlendSpace: continuous input, continuous pose

A [`BlendSpace1D`](https://docs.godotengine.org/en/stable/classes/class_animationnodeblendspace1d.html) is "a set of AnimationRootNodes placed on a virtual axis, crossfading between the two adjacent ones." Put idle at 0, walk at 0.5 and run at 1, feed it normalized speed, and the gait follows the speed with no state change. A BlendSpace2D does the same on a plane. Its `blend_mode` matters for 2D sprites. `BLEND_MODE_DISCRETE` "plays the animation of the animation node which blending position is closest to. Useful for frame-by-frame 2D animations." `BLEND_MODE_DISCRETE_CARRY` does the same but "starts the new animation at the last animation's playback position", so a walk cycle doesn't restart from frame zero every time the direction changes.

Blends handle *how much* of each motion. They suit continuous input. They are the wrong tool when the character must *commit*: a jump that has started should play its takeoff even if the player lets go.

### The state machine, as machinery

An [`AnimationNodeStateMachine`](https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachine.html) "contains multiple AnimationRootNodes representing animation states, connected in a graph. State transitions can be configured to happen automatically or via code, using a shortest-path algorithm." Every machine also has built-in `Start` and `End` nodes; the tree we built in the binary exposed parameters for both. Each connection is an [`AnimationNodeStateMachineTransition`](https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachinetransition.html):

| Setting | Values (4.7.2 default in bold) | What it decides |
|---|---|---|
| `switch_mode` | **Immediate**, Sync, At End | Immediate: "The current state will end and blend into the beginning of the new one." Sync: seek the new state "to the playback position of the old state." At End: "Wait for the current state playback to end." |
| `advance_mode` | Disabled, **Enabled**, Auto | Enabled: "Only use this transition during AnimationNodeStateMachinePlayback.travel()." Auto: use it "if the advance_condition and advance_expression checks are true" |
| `advance_condition` | a name | Becomes a boolean parameter you set from code; it "only checks if a variable is *true*, and it cannot check for falseness" |
| `advance_expression` | an expression | Evaluated against `AnimationTree.advance_expression_base_node` (default `.`, the tree itself). "An expression is anything you could put in an `if` statement." |
| `xfade_time`, `xfade_curve` | **0.0**, none | Cross-fade length and its easing |
| `priority` | **1** | "Lower priority transitions are preferred" |
| `reset` | **true** | Play the destination "from the beginning when switched" |

Read the `advance_mode` row twice. The default is **Enabled**, not Auto. A transition with an expression that you leave at the default will never fire on its own; only `travel()` will use it. The first agent in this chapter's example made exactly this mistake.

You control a running machine through the [`AnimationNodeStateMachinePlayback`](https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachineplayback.html) object at `parameters/playback`, or `parameters/<name>/playback` when the machine is nested in a blend tree. `travel(to)` "transitions from the current state to another one, following the shortest path" (the tutorial: "This is done via the A\* algorithm"); if no path exists, the machine teleports. `get_current_node()` has a trap for testers: "When using a cross-fade, the current state changes to the next state immediately after the cross-fade begins." Use `get_fading_from_node()` to see what it is fading from. The playback also emits `state_started` and `state_finished`.

There are two ways to connect a state machine to gameplay, and they fail differently.

- **Pull: Auto transitions with expressions or conditions.** The tree asks the game each time it processes: `is_on_floor()`, `velocity.y > 0.0`. The machine mirrors gameplay state. It fails when gameplay state changes *and changes back* between two tree updates, because the tree never saw it.
- **Push: `travel()` from code.** Gameplay code tells the tree where to go at the moment the action happens. It fails when a code path forgets to call `travel()`, or when two calls in one frame race.

### Where the timing gaps come from

The player's physics run in `_physics_process`. The tree runs in the idle step by default. When the physics rate is higher than the frame rate, several physics ticks run per rendered frame, and the tree only sees the state at the end of each frame. The 3D platformer runs 120 physics ticks per second. A test at `--fixed-fps 60` therefore runs two ticks per frame. A robot that touches the floor at the end of one tick and leaves it during the next, inside one frame, has landed and taken off between two tree updates.

Neither system is wrong; that is the sampling rate of the question "is the player on the floor?" You can process the tree in physics frames (`callback_mode_process`), push the state from code, or add transitions that tolerate a missed sample. The hands-on does the third.

### Root motion

Some clips move the character's root bone as part of the animation (a lunge, a vault). If you select that bone as the tree's `root_motion_track`, Godot will "cancel the bone transformation visually (the animation will stay in place)". You then read the motion each frame with `get_root_motion_position()` (and the rotation, scale and accumulator variants) and apply it to the body yourself. Root motion makes feet match the floor. It also hands movement authority to the animation, so your movement tests become tests of animation data. The 3D platformer does not use it: its `root_motion_track` is empty (printed from the running scene), and all movement comes from `player.gd`.

### Where the character's state lives

Before you add a state machine to a tree, find the one the game already has. The three Walker builds in this chapter keep it in three different places.

| Build | Gameplay state lives in | Animation chosen by |
|---|---|---|
| `walker-2d-finite-state-machine` | State nodes under `StateMachine`, with a pushdown stack | Each state's `enter()` calls `AnimationPlayer.play()`; the sword runs its own clips |
| `walker-jumpman-clawd` | Physics (`is_on_floor()`, `velocity`) plus session state (playing, failed, complete, paused) | `visual_animation()`, a priority list evaluated every frame, no transitions |
| `walker-3d-platformer` | Physics (`is_on_floor()`, `velocity`, a `jumping` flag) | `player.gd` writes blend amounts into an `AnimationTree` every physics tick |

A second state machine that disagrees with the first is worse than none, so the hands-on keeps the platformer's physics as the single authority.

### Generated motion: what it can supply, and what it cannot

The old Mini-Assignment 2 asked for a 15–30 second sequence made with "AI animation tools (RunwayML, D-ID, Synthesia, or similar)", submitted "as an MP4 file" with a reflection. The old Week 11 listed VEO 3, Runway Gen-2 and Pika Labs under "AI-assisted animation creation, motion synthesis" and "Converting AI videos to animation sequences." The revised syllabus keeps the subject and changes the deliverable: a playable state that responds to input and has been tested. It is worth being exact about where generated motion fits.

**An MP4 is pixels.** A generated video has no skeleton, no loop point, no event keys, and no notion of "the frame where the foot is planted." A game needs one of two things from it.

1. **Frames, for 2D.** Cut the clip into frames, pack a sprite sheet, and play it through `AnimatedSprite2D` or a keyed `Sprite2D.frame`. You still have to supply a clean loop (the old Assignment 6's own rule: "First and last frame must be the same"), a steady pivot so the character doesn't slide inside its collision box, the same silhouette size across clips so the idle-to-run switch doesn't pop, and transparency. A video model does not know your collision rectangle. `walker-jumpman-clawd`'s README names what happens when art ignores it: its "wide art extends beyond the original 18 × 28 collision box; that tradeoff needs human inspection."
2. **Pose data, for 3D.** Markerless motion-capture services estimate a skeleton pose in each video frame and export animation files. DeepMotion's Animate 3D, for example, documents "Video to 3D Animation" with "FBX, BVH, GLB, and MP4" output. Godot's 3D import documentation lists glTF 2.0 (recommended), `.blend`, DAE, OBJ and FBX, with FBX going through the ufbx importer by default "in Godot 4.3 or later." BVH is not in that list, so a BVH file needs converting outside Godot first. You still have to supply retargeting onto your bone names and proportions, foot contacts that don't skate, a decision about root motion, loop trimming, and cleanup of the frames where the estimator lost a limb.

**What generation never supplies is the state logic.** A generated jump clip doesn't know that the platformer cuts the jump short when you release Space (`vertical_velocity *= 0.7` in `player.gd`), that holding Space re-jumps on landing, or that the reset button can teleport the robot mid-air. It doesn't know which transitions exist, how long each cross-fade is, or which states may interrupt which. Every one of those is a decision in your files. Every one is testable the same way whether the clip came from an animator, a mocap suit, a video model or a function. That is why this chapter's test never looks at a pixel. It checks the tree's *state* against what the *player* is doing. Swap in a generated jump clip tomorrow and the same test tells you whether the wiring survived. Whether the new clip reads as a jump, you judge through play.

**Provenance travels with the file.** Record next to the asset which tool produced it, from what input (your own video? someone else's performance?), under which terms, on what date, and what you changed afterwards. `walker-2d-finite-state-machine` keeps a `FONT-PROVENANCE.md` for a single font file; that is the standard. Motion captured from video of a real person is that person's motion, so don't capture anyone who hasn't agreed. No paid generation was run for this chapter.

**Motion references are still the cheapest tool.** Before you tune a cross-fade, film yourself doing the action on a phone, or find a reference you are allowed to use, and step through it. How long is the crouch before a jump? How long does the landing absorb? At 30 fps, 0.1 s is three frames. That number is what you compare your `xfade_time` against. The reference informs a judgment. The test pins the judgment once you've made it.

---

## The Walker example: walker-3d-platformer

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-2d-finite-state-machine`](https://github.com/nikbearbrown/walker-2d-finite-state-machine), [`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd), [`walker-3d-platformer`](https://github.com/nikbearbrown/walker-3d-platformer), [`walker-3d-ik`](https://github.com/nikbearbrown/walker-3d-ik). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

**What it is.** A third-person 3D platformer: a robot that runs, jumps, shoots and collects coins on a `GridMap` stage, with enemies and a touch-screen joystick. The player is a `CharacterBody3D` (`player/player.gd`). Its model, `player/player.glb`, brings a `Skeleton3D` and an `AnimationPlayer` with eight clips. Printed from the running scene: `idle` (1.233 s, looping), `walk` (1.033 s, looping), `run` (0.833 s, looping), `jump` (0.433 s, looping), `falling` (0.433 s, looping), `shooting` and `shooting_standing` (0.433 s each, not looping), and `RESET`. There is no landing clip.

**Where it came from.** `3d/platformer` in the Godot demo projects at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`, MIT; the upstream README credits Marco F's Virtual Joystick add-on. We diffed the Walker copy against that commit, and only the project name differs. The Walker build is public at [github.com/nikbearbrown/walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer); starting from upstream also works. The project uses Jolt physics at 120 ticks per second.

**How its animation is wired.** The `AnimationTree` is a blend tree, not a state machine:

```text
output ← gun (Blend2, filtered to upper-body bones)
           ├─ 0: state (Blend2)
           │      ├─ 0: scale (TimeScale 1.5) ← run (Blend2: idle ↔ speed)
           │      │                              speed (Blend2: walk ↔ run)
           │      └─ 1: air_dir (Blend2: jump ↔ falling)
           └─ 1: shooting_standing
```

Every physics tick, `player.gd` writes five parameters: `run/blend_amount = horizontal_speed / MAX_SPEED`, `speed/blend_amount`, `state/blend_amount = anim` (0 on the floor, 1 in the air), `air_dir/blend_amount = clampf(-velocity.y / 4 + 0.5, 0, 1)`, and `gun/blend_amount`, which decays by `shoot_blend *= 0.97` per tick after a shot.

Look at the `state` line. It is an integer, 0 or 1, written into a Blend2 that has no fade of its own. We stepped the unmodified game at `--fixed-fps 60` and logged the parameters every physics tick. At takeoff, `state` went from 0 to 1 in one tick; at landing, from 1 to 0 in one tick. The robot cuts from its ground blend to its air blend with no cross-fade, and cuts back. `air_dir` does blend, from 0.03 to 1.00 over 21 ticks around the apex. Whether the hard cut shows at 60 fps is for your eyes, not the log.

**What its checks establish.** From its `FRICTIONAL.md`: an input probe "loads the actual scene, presses only ordinary movement/jump/shoot/reset actions and records 600 frames at fixed 60 FPS." Two runs passed four assertions: displacement, upward jump velocity, a `Bullet` node created, and a return near the start after the reset action. A jump comparison measured rises of 1.5300083 and 3.6030544 units for 6-tick and 60-tick holds of the jump key, "specific route measurements, not universal jump heights." Runs with headless Dummy audio at accelerated fixed FPS reported shutdown leaks of playback objects. A run with CoreAudio and normal timing exited clean. Both films exist as native 4K masters with listening review pending (`walker-demo-series/queue.json`, 2026-09-27).

**What remains unverified.** In the probe's own list: "coin pickup, enemy impact, camera image, audio, physical controls, fun." And nothing checks animation at all. The four assertions would pass with the `AnimationTree` deleted.

## The Walker example: walker-jumpman-clawd

**What it is.** Professor Bear's evolving 2D example: `github.com/nikbearbrown/walker-jumpman-clawd` (public; the local checkout used here is at `382f2baa5ee5e90a5afc083d82a5337845157f34`). Clawd is drawn in code. `features/player/clawd_art.gd` holds "Clawd's 18 code-driven animations", and states its own boundary: "Drawing only: never writes a body's position, velocity, input, or collision shape." There is no `AnimationPlayer` and no `AnimationTree`.

**How animation connects to actions.** One function in `features/player/player.gd` decides every frame:

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

`_process` resets `animation_seconds` to zero whenever the name changes. That is a complete state machine written as a priority list. There are no transitions to configure and no cross-fades, and every rule fits on one screen. The price is just as visible. There is no blend, so run to walk is a cut. Airborne always shows the jump pose sampled at a fixed 0.1 s, so rising and falling look the same. A speed that hovers around 100 px/s will flip between run and walk each time it crosses the line.

**What its checks establish.** On a scratch copy on 2026-09-27, the three commands in its README all exited 0. `test_game.gd` printed "25 checks / 0 failures". `test_keyboard.gd` passed nine keyboard checks (start, move, jump, pause, resume, retry, replay, main menu, start again). `test_clawd.gd` passed 1,950 checks over 162 animation samples against a reference file, reported with its own scope label: "Numeric animation parity and staged presentation checks, not human playtesting." Read the word *staged*. The presentation checks set `game.player.velocity.x = 30` and `= 160` directly, then ask `visual_animation()` what it would show. That tests the selector function. It does not test that pressing a key produces the walk animation. Both kinds of check are useful; they establish different things. (`test_clawd.gd` also writes a JSON report into `evidence/clawd/` next to `godot/`, one more reason to test on your own copy.)

## The Walker example: walker-2d-finite-state-machine, from the interaction side

Chapter 10 used this build for timing. Here it shows the third wiring: gameplay states own the animation. `Idle.enter()`, `Move.enter()`, `Jump.enter()` and `Stagger.enter()` each call `AnimationPlayer.play()` on the player, and `Attack` hands control to the sword's own `AnimationPlayer`. Jump, Stagger and Attack are pushed onto a stack, and only the top state's `update()` runs.

That design produces an edge case you can pin. Press Space, then F while airborne. We stepped it at `--fixed-fps 120`. The robot jumps, and on the frame F arrives the stack becomes `Attack, Jump, Idle`. From then until the sword finishes, the body's height stays at exactly 79.3 px for about 54 frames (0.45 s, the length of `attack_fast`), because `Jump.update()`, which applies gravity, no longer runs. Then Attack pops and the jump resumes from where it hung. The 18-check keyboard test never presses F in the air. Whether an attack that hangs in the air is a bug or a feature is not a question a test can decide. It is what the syllabus means by interpretive judgment (IJ), and once you decide, a test should pin it.

---

## Hands-on: wire a state machine to the player, then test the edges

You will replace the platformer's hard ground/air switch with a state machine that follows the robot's physics, and write a scripted-input test for normal play and three edge cases: jump held through landing, direction reversal, and an interrupt (reset mid-jump, and a shot mid-jump).

### Predict

1. The tree evaluates once per rendered frame. The robot's physics runs twice per rendered frame at 120 ticks and 60 fps. If the robot lands on one tick and jumps again on the next, what does the tree see?
2. A cross-fade of 0.1 s replaces a one-tick cut. What does that change on screen? What does it change in gameplay?
3. Press reset while the robot is rising. Which state should the machine be in a few frames later, and what evidence would you accept?
4. List every transition out of `fall` the machine needs. Write your list before you read the agent's.

### Build It

**Set up your copy** from the upstream demo. If you kept `godot-demo-projects` from Chapter 10, reuse it.

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

**Prompt 1: the state machine and the test.**

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

The prompt names the invariant (the machine follows physics, never input), the single structural change, and what not to touch, and it forbids the three shortcuts that make animation tests meaningless: writing velocity, writing tree parameters, calling `travel()`. Its last paragraph hands the agent a judgment, test or setup. In our run that judgment went wrong; read What we actually ran before you trust your agent's answer.

With Claude Code:

```bash
claude -p "$(cat prompt-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --disallowedTools "Skill" --max-turns 80 --output-format stream-json --verbose > session-1.jsonl
```

With Codex:

```bash
codex exec --sandbox workspace-write --json -o last-message-1.txt "$(cat prompt-1.txt)" < /dev/null > codex-session-1.jsonl
```

**Prompt 2: fix the setup, from your own trace.** If check 2 fails, don't accept "the test is wrong" until you have traced it. Log `is_on_floor()`, `velocity.y` and `get_current_node()` on every physics tick of the hop (our trace script is in the example folder). If the trace shows the machine in `fall` while the robot rises, send:

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

**Prompt 3: make the edge case impossible to miss.** Whether the landing falls on the first or second tick of a frame depends on everything that ran before it in the test, which is why a check like 2a can pass or fail after an unrelated edit. Pin both cases:

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

### Use It

Run the game on your own machine (F5 in the editor, or `godot --path godot`) and play the edges yourself.

1. **Hold Space** and hop ten times. Watch each landing. Our traces found two behaviors depending on tick timing (details below). In one, the robot rises for 0.1 s still in its ground blend before the jump pose arrives. Can you see it? Does it read as a stumble, or as weight?
2. **Reverse at full run.** The machine should stay in ground; the run blend dips as the robot decelerates and turns. Does the turn read?
3. **Reset mid-jump** (the `reset_position` action). The robot teleports to the start above the floor and falls. Does it snap straight to a falling pose?
4. **Shoot mid-jump.** The upper body should take the shooting pose over the jump or fall pose.
5. **Compare with a motion reference.** Film yourself doing a small hop in place, count the frames from landing to leaving the floor again, and compare with the 0.05–0.1 s cross-fades. Write down the numbers and your verdict.
6. While the game runs, switch the Scene dock to **Remote**, select the `AnimationTree`, and look at its parameters in the Inspector. The docs say that in Remote "you can inspect or change the nodes' parameters in the running project."

### Ship It

Commit in the order you worked: baseline, agent's state machine and test, the setup fix, the stronger test. Record in `FRICTIONAL.md` every check that failed on the way and what you decided about it, including any time the agent (or you) called a failure a test problem. Record your play verdicts from Use It as verdicts, with the date. They are not test results.

The Brutalist skill that fits this week is **`godot-waikthrough`** (also accepted as `godot-walkthrough`), which will "play a Godot game, capture every implemented feature" and comment on it. The syllabus note for Week 11 is "Check feel and readability through play," and a played walkthrough of the four edges is the natural film.

### Verify

```bash
godot --headless --path godot --fixed-fps 60 --script res://tests/test_motion_states.gd
```

Wrap it in `timeout 180` if your shell has it. A script error before `quit()` leaves headless Godot running forever. That happened in our run, as described below.

Then re-run your movement checks on the final scene. The Walker build keeps its input probe outside `godot/`, and it passed on our final version (next section). A pass establishes that under these scripted inputs, at 60 fps with 120 physics ticks, the machine's state follows the robot's physics, including on both tick offsets of a held-jump landing, and that the old movement still works. It does not establish that the cross-fades look right, that the jump reads as a jump, or that a player likes it.

---

## What we actually ran

Everything below ran on 2026-09-27 on the instructor's Mac, in a scratch copy of `walker-3d-platformer` (`godot/` plus its Markdown files; baseline commit `221f0a4`), with Godot `4.7.2.stable.official.ed1daf0bf`. The full record is in [`../examples/11-animation-and-interaction/`](../examples/11-animation-and-interaction/).

**Baseline.** Before any agent ran, we logged the unmodified tree's parameters under scripted input (`reviewer/probe_blend_parameters_baseline.gd`). That showed the one-tick ground/air cut described above. We also listed the clips and tree nodes from the running scene, and noted that `root_motion_track` was empty.

**Run 1: Claude Code 2.1.150, prompt 1.** Model `claude-sonnet-4-6`, the permission flags shown above but without `--disallowedTools "Skill"`, `--max-turns 80`. It started at 18:07 UTC and ran 49 turns in 44 minutes of session time, with one automatic context compaction. Its sequence, all visible in `sessions/claude-run1-excerpt.md`:

1. It explained the old tree accurately, with line references. It noted that `is_on_floor()` at the top of `_physics_process` "reflects the previous frame's `move_and_slide()`."
2. It rewrote the `AnimationTree` section of `player.tscn` and wrote the test. It gave the state machine a `start_node = &"ground"` property. The first run: 7 of 11 checks failed.
3. It wrote a diagnostic version of the test, which stopped on `SCRIPT ERROR: Invalid access to property or key 'start_node' on a base object of type 'AnimationNodeStateMachine'`. The property does not exist; the agent had invented it. Because the script stopped before `quit()`, headless Godot kept running. Claude Code's Bash tool moved the command to the background, and the orphaned Godot process ran for about half an hour until another session on the machine stopped it.
4. It removed `start_node` and found the machine stuck in the built-in `Start` node: nothing led out of it. It added an Auto `Start → ground` transition.
5. It found that its five expression transitions had `advance_mode = 1` (Enabled), the default, and would never fire on their own: "`ADVANCE_MODE_ENABLED (1)` does NOT auto-evaluate `advance_expression` in Godot 4.7 — it requires an external trigger." It changed all of them to Auto. Then the state followed the jump.
6. With the real test back in place, only 1b failed. It diagnosed that correctly as a test problem: 40 frames of running carried the robot off the starting platform before the jump.
7. Its fix for 1b added a reset at the start of check 1. That shifted every later check's timing, and 2a and 2b began to fail. It wrote: "The internal `await _reset()` in `_check1` broke checks 2a/2b (more total frames) … This is a **test fix**." It then reverted that reset and shortened the pre-jump run from 40 frames to 5 instead.
8. Then: `You've hit your session limit · resets 6:40pm (America/New_York)`. (The Chapter 10 session on the same account stopped at the same time.)

Step 7 is the one to study. The agent saw a check change from pass to fail when nothing but the test's own timing had changed, and concluded the test was at fault. That is a plausible reading. It is also exactly the signature of a real bug that depends on timing. The prompt asked it to decide "whether the test or the animation setup is wrong". It decided without a trace. We ran its final state ourselves: 9 of 11, with 2a and 2b failing.

**Our trace.** We added one `print` per physics tick to a copy of its check 2 (`reviewer/trace_check2_copy_of_run1_test.gd`). The result is the excerpt at the top of this chapter. On tick 137 the robot is on the floor; on tick 138 it has jumped; the machine is in `fall` and stays there while `velocity.y` falls from 12.50 through 5.53. Ticks 136 and 137 ran in the same rendered frame. The robot finished tick 136 on the floor and left it during tick 137, so when the tree evaluated at the end of that frame the robot was already airborne and rising. The machine had no transition out of `fall` for that. In a fresh-start trace (`reviewer/probe_held_jump_fresh.gd`) the same landing fell across a frame boundary, the tree saw `ground`, and the hop worked. The agent's frame-count edits would, at best, have moved the landing back onto the lucky tick.

**Run 2: Codex CLI 0.153.4, prompt 2.** Claude Code was unavailable until the limit reset, so we continued with Codex (configured model `gpt-5.6-sol`, low reasoning effort, `--sandbox workspace-write`). In 43 seconds it added exactly one transition resource and one entry in the `transitions` array. Our runs, three times: 11 of 11.

**Run 3: Codex, prompt 3 (51 seconds).** It gave `_check2` a `physics_tick_offset` argument and ran it at 0 and 1, changing only the test. Result: 14 of 14.

**Mutation check.** We put run 1's `player.tscn` (no `fall → jump`) into a throwaway copy and ran the new test against it: 2a and 2b failed at *both* offsets. Across three hops, each run hits the unlucky tick at least once. On the fixed scene, the same test passed.

**Regression.** The Walker build's own input probe (`tests/input_probe.gd`, kept outside `godot/`), run against the final scene: `{"jump":true,"movement":true,"projectile_created":true,"reset_action":true}`.

**Final state.**

| Command | Runs | Result |
|---|---|---|
| `test_motion_states.gd --fixed-fps 60` | 3 | 14/14 each |
| `test_motion_states.gd` with no `--fixed-fps` | 3 | 13/14 (5b failed), 13/14 (1b failed), 14/14 |
| Walker input probe, `--fixed-fps 60` | 1 | 4/4 true |

Some runs ended with `WARNING: 13 ObjectDB instances were leaked at exit` and `ERROR: 5 resources still in use at exit`; others printed none, or 5 and 1. The Walker build's `FRICTIONAL.md` records the same class of shutdown warning with headless Dummy audio. The agent's test calls `quit()` without freeing the game scene, which does not help.

**What review of the final test found.** Two things we would change. First, its constant `XFADE_FRAMES := 8` carries the comment "Worst-case xfade is 0.1 s = 6 frames; +2 buffer", but its loops count physics ticks, and at 120 ticks per second 0.1 s is 12 ticks. The check is stricter than its comment claims. That happens to be harmless here, but it is the same frames-versus-seconds confusion Chapter 0 describes. Second, nothing checks that the machine is *not* in `ground` while the robot rises. That matters, because of what the traces showed next.

**Two behaviors, one input.** On the final scene we traced every tick around each landing at both offsets (`reviewer/probe_held_jump_offsets.gd`). At offset 1 the tree misses the landing and goes straight from `fall` to `jump`. At offset 0 it sees the landing, starts the 0.1 s `fall → ground` cross-fade, and does not take the `ground → jump` transition until that cross-fade has finished. So from takeoff on tick 138 the robot rises in its ground blend (`current=ground fading_from=fall`, velocity 12.50 down to 10.67), and the jump state starts on tick 149, 12 ticks (0.1 s) after the landing. The same held key produces a different landing on alternate timings. The tests pass both.

**An experiment we did not ship.** In another throwaway copy we set the tree's `callback_mode_process` to physics. Both offsets then behaved identically: `ground` through the rise, `jump` from tick 149, 12 ticks after the landing. The test still passed 14 of 14. That makes the behavior consistent, not better. Whether a 0.1 s landing blend in mid-air is acceptable, or whether landing should use a shorter cross-fade or none at all when the jump is already held, is a feel decision. It belongs to the person who plays it (IJ), and it is recorded in the example's README as open.

---

## Check your understanding (ungraded)

1. In `diffs/02-codex-fall-to-jump.diff`, what are the two places the new transition had to be added, and what would happen if only the first were added?
2. The agent's first version left five transitions at `advance_mode = 1`. Using the class reference, explain why `travel()` would still have been able to use them while the Auto behavior never happened.
3. `get_current_node()` "changes to the next state immediately after the cross-fade begins." Look at check 4a ("leaves jump within the cross-fade plus two frames"). Would it pass for a machine whose cross-fade out of `jump` was 5 seconds long? What would you check instead?
4. Run `reviewer/probe_held_jump_offsets.gd` on the final scene with `-- 0` and `-- 1`. At which tick does `jump` begin in each case, and which one would you call correct?
5. `walker-jumpman-clawd` picks its animation with an `if` chain. Write the one line you would add to make it show a distinct falling pose, and the test you would write for it that uses key input rather than setting `velocity` directly.
6. In `walker-2d-finite-state-machine`, pressing F in mid-air freezes the jump for 0.45 s. Write the INVARIANT line you would add to a test if you decided that was a bug, and the TIMING line if you decided it was a feature.

---

## Doing the same thing in Unity

Unity and Unreal were not run for this chapter. The comparisons come from their official documentation, checked on 2026-09-27; the Unity manual pages consulted identify themselves as Unity 6.6 (6000.6).

### Similarities

The task translates almost one to one. You would replace a hard ground/air switch with Animator Controller states, drive them from the character's physics, and write a Play Mode test that presses real inputs and reads which state the Animator is in.

- **State machine with blended transitions.** "Use animation transitions in the state machine to switch or blend from one animation state to another." Each transition has a Transition Duration (in seconds when Fixed Duration is checked, otherwise as a fraction), an optional Exit Time, a Transition Offset into the destination, and Conditions, which "must all be met before transition is triggered." These are Godot's `xfade_time`, switch mode and advance condition under other names.
- **Blend trees for continuous input.** Unity separates transitions ("smoothly transition from one Animation State to another over a given amount of time") from Blend Trees ("smoothly blend multiple animations by incorporating parts of each animation, at varying degrees"), with 1D, 2D and Direct blending. The platformer's idle/walk/run chain is a 1D blend on speed in either engine.
- **Layers and masks.** Unity's manual gives nearly this chapter's example: "a lower-body layer for walking-jumping, and an upper-body layer for throwing objects / shooting," with an Avatar Mask restricting the upper layer. That is the platformer's filtered `gun` Blend2.
- **Root motion.** "At every frame, a change in the Root Transform is computed. This change in transform is then applied to the Game Object to make it move." The trade is the same as Godot's `root_motion_track`.
- **Scripted input in tests.** `InputTestFixture` "sets up a blank, default-initialized version of the Input System for each test", and `Press`, `Release`, `Set` and `Trigger` feed input. A Play Mode test can press jump instead of setting velocity, and read the state with `Animator.GetCurrentAnimatorStateInfo(layer)` and `IsName("Jump")`. Run it headless with `-runTests -batchmode -testPlatform PlayMode`.

### Differences

- **Conditions compare parameters; there are no expressions.** A Unity transition's conditions compare Animator parameters (floats, ints, bools, triggers) that your script sets. Nothing like Godot's `advance_expression` calls `is_on_floor()` on the character directly, so the pull design becomes "script pushes parameters, conditions pull them." The sampling question is the same. The Animator evaluates in its update mode (Normal, Fixed or UnscaledTime), and a one-physics-step floor contact can fall between two evaluations when the Animator runs in Update.
- **Interruption is an explicit setting.** Unity transitions have an Interruption Source ("control the circumstances under which this transition might be interrupted") and Ordered Interruption. In our Godot run, a transition waited for the current cross-fade to finish before the next one fired. We found that by tracing, not from a setting. In Unity you would set the rule, and still test it.
- **The controller is a long asset.** `.controller` files are YAML text under Force Text serialization, so an agent can edit states and transitions. But a controller with blend trees is long, positional YAML. Review it in the Animator window, and trust the Play Mode test over the diff.

| Godot 4.7.2 | Unity 6.6 |
|---|---|
| `AnimationTree` + `AnimationNodeStateMachine` | Animator + Animator Controller |
| Transition `xfade_time` | Transition Duration (Fixed Duration) |
| `switch_mode` At End | Has Exit Time |
| `advance_condition` / `advance_expression` | Conditions on Animator parameters |
| `BlendSpace1D` / `BlendSpace2D` | 1D / 2D Blend Tree |
| Filtered Blend2 | Layer + Avatar Mask |
| `playback.get_current_node()` | `GetCurrentAnimatorStateInfo(layer).IsName(…)` |
| `root_motion_track` | Root Transform / root motion |
| `Input.action_press()` in a SceneTree test | `InputTestFixture.Press()` in a Play Mode test |

## Doing the same thing in Unreal Engine

Checked against the Unreal Engine documentation on 2026-09-27; the pages consulted identify themselves as Unreal Engine 5.8. Unreal Engine is source-available under the Unreal Engine EULA, not open source.

### Similarities

- **State machines in an Animation Blueprint.** "State Machines are modular systems you can build in Animation Blueprints in order to define certain animations that can play, and when they are allowed to play." States "contain their own Anim Graph layer", so a ground state can hold a Blend Space, just as this chapter's `ground` state holds a nested blend tree. "All State Machines begin with an entry point." Conduits create "1-to-many, many-to-1, or many-to-many transitions."
- **Transition rules pull from gameplay.** A transition rule outputs a boolean: "A true value is used to determine whether the state can transition to the next state." The documentation says transition rules "are typically informed by the movement component and other character variables." Each transition has a Duration ("The length of time, in seconds, that the transition takes") and a Blend Logic.
- **Blend Spaces for locomotion.** "Blend Spaces are graphs where you can plot any number of animations to be blended between based on the values of multiple inputs," in 1D or 2D, used through a Blend Space player in the AnimGraph.
- **Interrupts through slots.** Montages "exclusively play animation using Slots", and the documentation describes an "Upper Body Slot … together with a Layered blend per bone node to remove animation on the lower body so that only the upper body is affected." That is the platformer's filtered shooting layer.
- **Root motion modes.** An Animation Blueprint's Root Motion Mode chooses No Root Motion Extraction, Ignore Root Motion, Root Motion from Everything, or Root Motion from Montages Only.

### Differences

- **Rules are graphs, not strings.** Where Godot evaluates a text expression against a base node, Unreal evaluates a small Blueprint graph per transition. It is the same pull model, with more machinery and no text to diff.
- **Threading shapes the design.** Epic's root-motion page warns that with Root Motion from Everything or from Montages, "the Animation Graph is updated on the Game Thread instead of a Worker Thread." When animation updates relative to gameplay is an engineering constraint there, exactly as the tree's process callback is here.
- **Nothing here is text.** State machines, transition rules, Blend Spaces and Montages are `.uasset` files. An agent's way in is editor Python, which is editor-only, or C++ in the Anim Instance. Its way to prove a transition is an Automation or functional test, run with `-ExecCmds="Automation RunTest …;Quit"`.

| Godot 4.7.2 | Unreal Engine 5.8 |
|---|---|
| `AnimationTree` | Animation Blueprint (AnimGraph + EventGraph) |
| `AnimationNodeStateMachine` | State Machine |
| Transition + `advance_expression` | Transition rule (boolean graph) |
| (no equivalent) | Conduit |
| `xfade_time` | Transition Duration, Blend Logic |
| `BlendSpace1D` / `2D` | Blend Space (1D / 2D) |
| `OneShot`, filtered Blend2 | Montage in a slot, Layered blend per bone |
| `root_motion_track` | Root Motion Mode |
| SceneTree test with `Input.action_press()` | Automation or functional test |

---

## Sources

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation, checked on 2026-09-27. Godot behavior marked "printed from the binary", "measured" or "traced" comes from runs of Godot 4.7.2 recorded in `examples/11-animation-and-interaction/logs/`.

**Godot (docs.godotengine.org, stable = 4.7 on 2026-09-27)**
- Using AnimationTree: https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html
- AnimationNodeStateMachine: https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachine.html
- AnimationNodeStateMachineTransition: https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachinetransition.html
- AnimationNodeStateMachinePlayback: https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachineplayback.html
- AnimationNodeOneShot: https://docs.godotengine.org/en/stable/classes/class_animationnodeoneshot.html
- AnimationNodeBlendSpace1D: https://docs.godotengine.org/en/stable/classes/class_animationnodeblendspace1d.html
- AnimationMixer: https://docs.godotengine.org/en/stable/classes/class_animationmixer.html
- Available 3D formats (import): https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html
- 2D sprite animation: https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html
- Overview of debugging tools (Remote scene tree): https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html
- Command line tutorial: https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html

**Walker and course files**
- `walker-3d-platformer`: `README.md`, `SOURCES.md`, `GAME-BRIEF.md`, `FRICTIONAL.md`, `tests/input_probe.gd`
- `walker-jumpman-clawd` (public: https://github.com/nikbearbrown/walker-jumpman-clawd): `README.md`, `godot/features/player/player.gd`, `godot/features/player/clawd_art.gd`, `godot/tests/*.gd`
- `walker-2d-finite-state-machine`: `README.md`, `FRICTIONAL.md`, `FONT-PROVENANCE.md`
- `walker-3d-ik`: `FRICTIONAL.md`
- `walker-demo-series/queue.json` (item 2)
- Upstream: https://github.com/godotengine/godot-demo-projects at `a3b5c113112f77291d5f3d1360f33a882fdc52f7` (`3d/platformer`), MIT
- Old course pages (Canvas export): Mini-Assignment 2 – Generative AI for Animation; Assignment 6 – Animation; syllabus Week 11
- Revised syllabus (`CSYE_7270_Virtual_Environments_and_Real-Time_3D.docx`), Week 11 row and the "dangerous middle" paragraph
- Chapter 0 (frames versus seconds) and Chapter 10 (timing, pins) of this book

**Generated motion**
- DeepMotion Animate 3D documentation: https://www.deepmotion.com/doc/animate-3d

**Unity (docs.unity3d.com, pages showing Unity 6.6)**
- Transitions: https://docs.unity3d.com/Manual/class-Transition.html
- Blend Trees: https://docs.unity3d.com/Manual/class-BlendTree.html
- Animation Layers: https://docs.unity3d.com/Manual/AnimationLayers.html
- Root Motion: https://docs.unity3d.com/Manual/RootMotion.html
- Animator.GetCurrentAnimatorStateInfo: https://docs.unity3d.com/ScriptReference/Animator.GetCurrentAnimatorStateInfo.html
- AnimatorUpdateMode: https://docs.unity3d.com/ScriptReference/AnimatorUpdateMode.html
- Editor settings, Asset Serialization: https://docs.unity3d.com/Manual/class-EditorManager.html
- Input System testing (package 1.11): https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/Testing.html
- Test Framework command line (package 1.4): https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html

**Unreal Engine (dev.epicgames.com, pages showing 5.8)**
- State Machines: https://dev.epicgames.com/documentation/en-us/unreal-engine/state-machines-in-unreal-engine
- Transition Rules: https://dev.epicgames.com/documentation/en-us/unreal-engine/transition-rules-in-unreal-engine
- Blend Spaces: https://dev.epicgames.com/documentation/en-us/unreal-engine/blend-spaces-in-unreal-engine
- Animation Slots: https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-slots-in-unreal-engine
- Root Motion: https://dev.epicgames.com/documentation/en-us/unreal-engine/root-motion-in-unreal-engine
- Run Automation Tests: https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine
- Scripting the Unreal Editor using Python: https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python
- Unreal Engine on GitHub (source access under the EULA): https://www.unrealengine.com/ue-on-github

**Tools**
- Claude Code 2.1.150 and Codex CLI 0.153.4 (`--help` output, 2026-09-27)
