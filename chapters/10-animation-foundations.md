# Chapter 10 — Animation Foundations

CSYE 7270 · Fall 2026 · Week 10

## Executive summary

**What this chapter is.** How animation works in Godot 4.7.2, taught through the Week 10 rule: "Establish behavior checks before changing animation tracks, timing, or transitions." Animation keys are numbers in a text scene file, so an agent can change them in seconds, and a wrong number raises no error.

**What we built, and what happened.** An agent wrote a frame-stepped headless check that pins the sword timing in `walker-2d-finite-state-machine`. The measurement showed that the demo's second combo swing never plays on screen, although the build's own combo test passes, because that test counts swings instead of watching them. We then moved the hitbox's live window into the animation, and the pinned check caught what the request never mentioned: swing two lost its hitbox entirely. A one-line fix and a deliberate re-pin brought the check back to 20 of 20. Claude Code hit the account's usage limit before writing the test; Codex completed the same prompts, and both outcomes are recorded.

**What this does not establish.** Whether the swings look and feel right, whether the hitbox matches the blade on screen, or whether anything is hit, since the demo has no enemy. Those checks are yours, with the game running in front of you.

---

## The question

The Walker build of the finite-state-machine demo ships a combo test. It sends real F key presses, waits, and asserts things. Eleven checks, zero failures, including this one:

```text
PASS second swing starts
```

Step the same scene one frame at a time at a fixed 120 frames per second and record the sword's rotation, and you get this:

```text
 31 anim=attack_fast    pos=0.2500 ... combo=2 state=Attack rot=75.0
 32 anim=attack_fast    pos=0.2583 ... combo=2 state=Attack rot=75.0
 ...
 54 anim=attack_fast    pos=0.4417 ... combo=2 state=Attack rot=75.0
 55 anim=attack_medium  pos=0.0000 ... combo=3 state=Attack rot=75.0
```

The combo counter says swing two started on frame 31. The animation's playhead says the clip is a quarter of a second in, and the blade sits at 75° for 24 frames. It never moves.

Which is right? Both. The counter really did go to 2, and the blade really didn't swing. The test checked a number in a script, not a motion on screen. This chapter is about the gap between those two things. Why does Godot keep playing instead of restarting? Which frame does a key at 0.1 s actually fire on? And how do you write a check that would have noticed?

---

## Ideas you need

### An animation is data bound to node paths

In Godot an animation is a resource, not a behavior. The [`Animation`](https://docs.godotengine.org/en/stable/classes/class_animation.html) class "holds data that can be used to animate anything in the engine. Animations are divided into tracks and each track must be linked to a node." A track is a path to a node, usually plus one property on it, and a list of keys. Each key is a time, a value, and an easing value for how to approach it.

The node that plays animations is the [`AnimationPlayer`](https://docs.godotengine.org/en/stable/classes/class_animationplayer.html). It holds one or more [`AnimationLibrary`](https://docs.godotengine.org/en/stable/classes/class_animationlibrary.html) resources, and each library maps names to `Animation` resources. `AnimationPlayer` and `AnimationTree` (Chapter 11) share a base class, [`AnimationMixer`](https://docs.godotengine.org/en/stable/classes/class_animationmixer.html). That base class owns the playback timing and blending rules both of them use.

A scene file is text, so all of this is readable. Here is the sword's fast attack from `godot/player/weapon/Sword.tscn`, trimmed to two of its four tracks:

```text
[sub_resource type="Animation" id="3"]
length = 0.45
step = 0.05
tracks/0/type = "value"
tracks/0/path = NodePath(".:rotation_degrees")
tracks/0/keys = {
"times": PackedFloat32Array(0, 0.15, 0.2),
"transitions": PackedFloat32Array(0.439427, 1, 1),
"update": 0,
"values": [-80.0, 85.0, 75.0]
}
tracks/3/type = "method"
tracks/3/path = NodePath(".")
tracks/3/keys = {
"times": PackedFloat32Array(0.1, 0.25),
"values": [{ "args": [], "method": &"set_attack_input_listening" },
           { "args": [], "method": &"set_ready_for_next_attack" }]
}
```

Read it as machinery. Track 0 swings the blade from −80° to 85° in 0.15 s and settles at 75° by 0.2 s. The `0.439427` on the first key is an easing value, the same curve as [`@GlobalScope.ease()`](https://docs.godotengine.org/en/stable/classes/class_animation.html#class-animation-method-track-set-key-transition). Track 3 calls two methods on the sword. The one at 0.1 s opens the combo input buffer. The one at 0.25 s says the next swing may start. The clip is 0.45 s long, so the blade sits still for the last 0.25 s. The class reference is explicit that `length` "is not delimited by the last key."

This is why an agent can edit animation in Godot: the keys are numbers in a text file. It is also why an agent can break animation in Godot without any error, because a changed number is still a valid number.

### Track types

Godot 4.7.2 has nine track types. We printed the enum values from the engine binary; the descriptions are the class reference's.

| Track type | What it does | Where you meet it |
|---|---|---|
| Value (`TYPE_VALUE`) | "Value tracks set values in node properties" | `rotation_degrees`, `visible`, `monitoring` on the sword |
| Position 3D, Rotation 3D, Scale 3D | Transform channels for 3D nodes and skeleton bones | imported character clips |
| Blend shape | "optimized for animating blend shape in MeshInstance3D" | faces |
| Method (`TYPE_METHOD`) | "Method tracks call functions with given arguments per key" | the sword's combo window |
| Bezier | Interpolates a value "using custom curves" | hand-shaped camera or UI motion |
| Audio | Plays streams "with AudioStreamPlayer nodes" | swing whooshes (Chapter 12) |
| Animation | Plays "animations in other AnimationPlayer nodes" | sequencing a sub-rig |

The [track-types tutorial](https://docs.godotengine.org/en/stable/tutorials/animation/animation_track_types.html) adds a warning that matters for testing. Method-track events "are not executed when the animation is previewed in the editor for safety." Scrubbing the timeline in the editor will never show you the combo window opening. Only a running game does.

### Between keys: interpolation, easing, update mode

Three separate settings decide what happens between two keys, and they are easy to confuse.

- **Interpolation**, per track: nearest, linear, cubic, and, for rotations, linear-angle and cubic-angle, which take the shortest path around the circle ([introduction to animation](https://docs.godotengine.org/en/stable/tutorials/animation/introduction.html)).
- **Transition**, per key: the easing curve used when approaching that key. `1` is linear.
- **Update mode**, per value track. `UPDATE_CONTINUOUS` will "update between keyframes and hold the value." `UPDATE_DISCRETE` will "update at the keyframes" only. `UPDATE_CAPTURE` is continuous but "works as a flag to capture the current object value." A boolean such as `visible` or `monitoring` wants discrete, because there is nothing between `true` and `false`.

### When animation actually runs

This part decides whether a hitbox is live on frame 12 or frame 14, and none of it shows in the editor.

- **Process callback.** `AnimationMixer.callback_mode_process` is physics ("Process animation during physics frames"), idle ("Process animation during process frames"), or manual ("Do not process animation. Use advance() to process the animation manually."). `AnimationPlayer` and `AnimationTree` both default to idle in 4.7.2; we printed `callback_mode_process=1` from the binary.
- **Method callback.** `callback_mode_method` is deferred ("Batch method calls during the animation process, then do the calls after events are processed") or immediate ("Make method calls immediately when reached in the animation"). The default is deferred. So a method key at 0.1 s runs at the end of the frame in which the playhead crossed 0.1 s, after that frame's scripts have already read the old value.
- **Starting.** The measurement later in this chapter shows the playhead still at 0.0 on the first processed frame after `play()`, and the first attack after launch showing the blade at 0° for one frame before the −80° key applies. Add the deferred method call, and a key at 0.1 s (frame 12 at 120 fps, on paper) was observed on frame 14.
- **Replaying the same name.** The class reference: if `play()` "is called with that same animation `name`, or with no `name` parameter, the assigned animation will resume playing if it was paused." Nothing restarts a clip that is already playing. That sentence explains the question at the top of this chapter.
- **Discrete tracks under blending.** `callback_mode_discrete` decides whether discrete or continuous tracks win when animations blend. Recessive, in which a continuous or capture track value "takes precedence", is "the default behavior for AnimationPlayer." Force-continuous will "always treat the Animation.UPDATE_DISCRETE track value as Animation.UPDATE_CONTINUOUS with Animation.INTERPOLATION_NEAREST", and is "the default behavior for AnimationTree." We also printed both defaults from the 4.7.2 binary.

### RESET, and a demo's SETUP

Godot supports a special animation named `RESET` that holds "the 'default pose'." With **Reset On Save**, "the scene will be saved with the effects of the reset animation applied (as if it had been seeked to time `0.0`)." The finite-state-machine demo instead has an animation called `SETUP`. That name means nothing to the engine. It is an ordinary animation that nothing in the demo plays. Know that before you ask an agent to "fix the reset pose" there.

### Tween or AnimationPlayer

A [`Tween`](https://docs.godotengine.org/en/stable/classes/class_tween.html) is created from code with `create_tween()`. It animates values toward a target and is then discarded: "Tweens are not designed to be reused and trying to do so results in an undefined behavior." The class reference says they are "mostly useful for animations requiring a numerical property to be interpolated over a range of values", especially when you don't know the final value in advance. An `AnimationPlayer` clip is authored ahead of time, stored in a scene, and replayed.

The rule for this course: if a designer needs to see it, scrub it and retime it, it belongs in an `Animation`. If the end value comes from gameplay, such as a camera zoom to whatever the player targeted or a health bar sliding to the current value, it belongs in a `Tween`. Either way, a gameplay fact like "the hitbox is live" should not depend on a tween that can be killed halfway.

### Frames, sprite sheets and cycles

The old Assignment 6 asked for a sprite-sheet animation and a movement cycle whose "first and last frame must be the same." Godot's [2D sprite animation tutorial](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html) gives two routes. `AnimatedSprite2D` plays a `SpriteFrames` resource built from individual images or from a sheet cut into a grid. Or a `Sprite2D` with `hframes`/`vframes` has its `frame` property keyed in an `AnimationPlayer`. The tutorial's own comparison: `AnimationPlayer` "is a bit more complex than AnimatedSprite2D, but it provides additional functionality, since you can also animate other properties like position or scale." Prefer it for anything gameplay reads. Then the hitbox, the sound and the frame live on one timeline.

A loop seam is a testable fact, not only a visual one. For a looping clip, the values at time 0 and at `length` should match, and `loop_mode` should be `LOOP_LINEAR` or `LOOP_PINGPONG`. You can assert both headlessly. Whether the cycle reads as a walk is a human check.

### Skeletons and IK

**2D.** A [`Skeleton2D`](https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html) holds a hierarchy of `Bone2D` nodes. A `Polygon2D` is skinned to those bones with painted weights: "Points in white have a full weight assigned, while points in black are not influenced by the bone." The rest pose is "the default pose for a skeleton, you can come back to it anytime you want." 2D IK and constraints live in `SkeletonModificationStack2D`, which the class reference marks **Experimental**.

**3D.** A `Skeleton3D` holds bone poses that animation tracks write. In Godot 4.x, procedural changes layered on top of animation are nodes that inherit [`SkeletonModifier3D`](https://docs.godotengine.org/en/stable/classes/class_skeletonmodifier3d.html). Two rules in its documentation matter for testing. First, "if there is an AnimationMixer, a modification always performs after playback process of the AnimationMixer." Second, a modified pose is read "at the moment" the modifier's `modification_processed` signal fires. On the skeleton itself, [`skeleton_updated`](https://docs.godotengine.org/en/stable/classes/class_skeleton3d.html) is emitted "when the final pose has been calculated … This means that all SkeletonModifier3D processing is complete."

We asked the 4.7.2 binary for every subclass of `SkeletonModifier3D`. It returned `AimModifier3D`, `BoneConstraint3D`, `BoneTwistDisperser3D`, `CCDIK3D`, `ChainIK3D`, `ConvertTransformModifier3D`, `CopyTransformModifier3D`, `FABRIK3D`, `IKModifier3D`, `IterateIK3D`, `JacobianIK3D`, `LimitAngularVelocityModifier3D`, `LookAtModifier3D`, `ModifierBoneTarget3D`, `PhysicalBoneSimulator3D`, `RetargetModifier3D`, `SkeletonIK3D`, `SplineIK3D`, `SpringBoneSimulator3D`, `TwoBoneIK3D`, `XRBodyModifier3D` and `XRHandModifier3D`. The IK solvers sit under `IKModifier3D`. [`TwoBoneIK3D`](https://docs.godotengine.org/en/stable/classes/class_twoboneik3d.html), for example, is the "rotation based intersection of two circles" solver that "requires a pole target." The older [`SkeletonIK3D`](https://docs.godotengine.org/en/stable/classes/class_skeletonik3d.html) still exists and is marked **Deprecated** ("may be changed or removed in future versions"). The Walker IK build uses `SkeletonIK3D` and a GDScript FABRIK plugin, because that is what the upstream demo uses.

### Running animation deterministically without a window

Every machine check in this chapter uses three flags from the [command-line reference](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html):

| Flag | What it does |
|---|---|
| `--headless` | "Enable headless mode (`--display-driver headless --audio-driver Dummy`)." No window, no sound device |
| `--script <path>` | Runs a script (here, one that `extends SceneTree`) as the whole program |
| `--fixed-fps <n>` | "Force a fixed number of frames per second. This setting disables real-time synchronization." Every frame advances game time by exactly 1/n s, as fast as the machine can go |

The finite-state-machine project runs 120 physics ticks per second (`physics/common/physics_ticks_per_second=120` in `project.godot`). With `--fixed-fps 120`, one rendered frame is one physics tick is 1/120 s. A test that does `await process_frame` in a loop can then count frames exactly. Without the flag, the same test counts frames of whatever length the machine produces. Chapter 0 showed what that does to a frame-counted route test. This chapter's example shows it again for animation: the same pinned timing test that passes 3 of 3 times with `--fixed-fps 120` failed 7, 9 and 9 of its 20 checks in three runs without it, with different frame numbers each time. The existing Walker tests use `create_timer()` waits, which are measured in game seconds. They passed at 120 fps, at 60 fps and in real time (three runs), but they cannot pin a frame.

---

## The Walker example: walker-2d-finite-state-machine

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-2d-finite-state-machine`](https://github.com/nikbearbrown/walker-2d-finite-state-machine), [`walker-3d-ik`](https://github.com/nikbearbrown/walker-3d-ik). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

**What it is.** A top-down character with a hierarchical state machine. Idle, Move, Jump, Stagger and Attack are child nodes of a `StateMachine` node. Jump, Stagger and Attack are pushed onto a stack, so the player returns to whatever it was doing (a pushdown automaton). The sword is its own scene, `player/weapon/Sword.tscn`: an `Area2D` hitbox with a `CollisionPolygon2D`, a `Sprite2D`, and an `AnimationPlayer` holding five animations (`SETUP`, `attack_circular`, `attack_fast`, `attack_medium`, `idle`). `sword.gd` runs a three-swing combo table: fast, fast, medium, with damage 1, 1 and 3.

**Where it came from.** `2d/finite_state_machine` in `github.com/godotengine/godot-demo-projects` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`, under the Godot Engine contributors' MIT license, retained in `LICENSE.md`. We diffed the Walker copy against that commit. The only differences are the project name and the two added tests. The embedded font is Source Code Pro Bold 2.030 under the SIL Open Font License 1.1, according to the build's own `FONT-PROVENANCE.md`, which also records that separate license packaging is still pending. The Walker build is public at [github.com/nikbearbrown/walker-2d-finite-state-machine](https://github.com/nikbearbrown/walker-2d-finite-state-machine). Build It below starts from the upstream demo instead; this chapter's example folder carries the two Walker tests and the new one.

**What its checks establish.** Two headless tests, both driven by real key events through `Input.parse_input_event`:

- `test_input.gd`: 18 checks, 0 failures (`input-debug-20260927.log`). Idle; walk and run speeds (450 and 700); Space pushes Jump over Idle and raises the body pivot; landing pops back; X staggers; F attacks and shows the sword; R spawns a bullet; the debug labels follow the stack.
- `test_combo.gd`: 11 checks, 0 failures (`combo-20260927.log`). The buffer opens, a second F registers, `combo_count` reaches 2 and then 3, swing three uses `attack_medium` with damage 3, a fourth F does not start a fourth swing, and the whole combo is one push and one pop.

We reran both on an unmodified copy on 2026-09-27 with Godot 4.7.2: 18 of 18 and 11 of 11.

**What remains unverified, in the build's own words.** `FRICTIONAL.md` records that the main scene "has no enemy/Health target or environment collider", so "damage metadata does not establish actual hit/damage behavior." `Die` "is present as a node but not mapped in player states." Assertions about `BodyPivot` height and `sword.visible` "are state measurements, not claims that rendered frames were inspected." No gameplay footage exists, because a standing capture constraint blocks it.

Add one item to that list. The combo check "second swing starts" asserts `sword.combo_count == 2`. It never looks at the animation. As the question above showed, the second swing does not happen on screen.

## The Walker example: walker-3d-ik

**What it is.** Four scenes built around the Godot Battle Bot model: a look-at scene; a scene driven by a GDScript FABRIK solver from the demo's own `addons/sade` plugin; a scene using the built-in `SkeletonIK3D` node on both arms; and a first-person scene whose arms hold a pistol through the plugin's FABRIK and look-at scripts. Mouse position moves a `Targets` node in front of the camera, and the solvers pull the head and arms toward it.

**Where it came from.** `3d/ik` at the same upstream commit, MIT. Walker's production edits are the title and one scheduling fix, described next. The DAE asset headers name the author as "Anonymous" and a Blender Collada exporter by Juan Linietsky. The build's `FRICTIONAL.md` notes that "exporter authorship is NOT model authorship" and leaves asset-specific provenance pending.

**What its checks establish, and where headless evaluation was hard.** This build is the honest counterweight to the 2D one. Several of its first checks failed, and the failures were about how to observe animation, not about the game.

1. **A real scheduling bug, fixed with a regression check.** The FABRIK script's `update_mode` setter turned on `_process` when asked for physics-mode updates. `test_modes.gd` reproduced it (7 of 8 before). A one-line change to `set_physics_process(true)` fixed it (8 of 8 after), and the navigation test still passed 12 of 12.
2. **A sampling trap, not a solver bug.** The first navigation run passed 10 of 12. Both `SkeletonIK3D` "upper arm responds" checks failed, even though the diagnostic showed the targets had moved and both solvers reported `is_running() == true`. The cause was the test. It read `get_bone_global_pose()` after a timer, between skeleton updates, and saw a pose without the IK applied. Connecting a read-only observer to `Skeleton3D.skeleton_updated` and reading the pose there made all 12 pass, with no production change. We reproduced both results on 2026-09-27. The harness's `--raw` mode (the original sampling) prints `RESULT 12 checks; 2 failures`; the default mode prints `RESULT 12 checks; 0 failures`.
3. **A backend limit no test can cross.** The FPS scene's mouse-look only works with the mouse captured. In a headless run, requesting `MOUSE_MODE_CAPTURED` reads back as visible: `test_mouse_backend.gd` printed `DIAG display backend: headless` and `requested 2 observed 0`, both when the build was made and when we reran it. The FPS navigation test therefore stays at 4 of 8, with the captured-mode, yaw and both pitch-clamp checks failing. The build did not patch gameplay to get around that gate, and did not open a visible window to test it. Those four behaviors remain unverified.

The lesson carries into every animation test you write: decide *when* in the frame you observe. The engine documents when modified poses are final (`skeleton_updated`). A test that reads at some other moment can fail a working rig, or pass a broken one.

---

## Hands-on: pin the sword's timing, then change it

You will do what we did, on your own copy: pin the timing first, make one animation change, read what the check says, fix what it catches, and re-pin on purpose.

### Predict

Write your answers down before you delegate anything.

1. `test_combo.gd` says "second swing starts" when `combo_count` reaches 2. What would a check have to record, every frame, to know the blade actually moved?
2. The hitbox is currently switched on by code for the whole attack. If you move it into `monitoring` keys at 0.0 s and 0.15 s in `attack_fast`, on which frame (at 120 fps) will it turn on, and on which will it turn off? Exactly frames 0 and 18?
3. If swing two re-plays `attack_fast` without restarting it, what happens to swing two's hitbox once the window lives in the animation?
4. Which of the two existing Walker tests would notice?

### Build It

**Set up your copy.** You can clone the public `walker-2d-finite-state-machine`, or, as below, start from the upstream demo at the commit every Walker adaptation came from and copy in the two Walker tests.

```bash
git clone https://github.com/godotengine/godot-demo-projects.git
```

```bash
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

```bash
mkdir -p sword-timing
```

```bash
cp -R godot-demo-projects/2d/finite_state_machine sword-timing/godot
```

Copy the two Walker tests from this book's `examples/10-animation-foundations/tests/walker-harness/` into `sword-timing/godot/`, then, from inside `sword-timing`:

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
git commit -m "baseline: 2d/finite_state_machine at a3b5c11 + Walker tests"
```

Import before any test. A fresh copy has no `.godot/` import cache. In our Codex sandbox check, a test run on an un-imported copy still printed 11 of 11 PASS while the textures and font failed to load, with `ERROR` lines in the output. A PASS line is not the whole log.

**Prompt 1: pin what exists.** Paste this into Claude Code or Codex, started in `sword-timing`:

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

Notice what the prompt does. It names the one file that may be created. It forbids the shortcuts that make a test pass without playing the game: direct method calls, state writes. It separates numbers you may change later (TIMING) from facts that must survive (INVARIANT). And it asks for anomalies to be *kept and reported*, not fixed, because a pin records what is, not what should be.

With Claude Code, headless, scoped to the tools this task needs:

```bash
claude -p "$(cat prompt-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --disallowedTools "Skill" --max-turns 60 --output-format stream-json --verbose > session-1.jsonl
```

With Codex:

```bash
codex exec --sandbox workspace-write --json -o last-message-1.txt "$(cat prompt-1.txt)" < /dev/null > codex-session-1.jsonl
```

Two Codex differences matter here. The `workspace-write` sandbox blocks writes outside the project, so Godot prints `ERROR: Failed to open 'user://logs/…'` (it cannot write its log in your user folder) and, during import, cannot save editor settings. Both are harmless for these tests; Chapter 0 covers why. And `< /dev/null` stops `codex exec` from waiting for more input on standard input when you run it from a script.

**Prompt 2: one animation change.** Run this only after you have committed the pinned test.

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

The last paragraph is the point of the week. You expect failures, because you asked for a timing change. The question is whether every failure is one you asked for.

**Prompt 3: fix what the check caught.** Write this one yourself from what prompt 2 reports. Ours, after the pinned check flagged swing two:

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

**Prompt 4: re-pin, only after you approve.** Play the game first (Use It, below). Then:

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

Keep the change and the re-pin in separate prompts and separate commits. An agent that edits the behavior and the expectation in one step can make any change pass.

### Use It

The headless check tells you frame numbers. It cannot tell you whether a swing reads as a swing. On your own machine, open `sword-timing/godot/project.godot` in the Godot editor. The instructor's lab machine runs headless only, but yours need not.

1. Select `player/weapon/Sword.tscn`, open the Animation panel, and scrub `attack_fast`. Watch the blade and the new `monitoring` track. Remember that the method track does not fire while you scrub.
2. Run the project (F5) on the baseline commit. Press F three times with a short gap, as in the combo. Watch swing two. Then check out your final commit and do it again.
3. While it runs, switch the Scene dock to **Remote** and select the Sword node. The documentation says that in Remote "you can inspect or change the nodes' parameters in the running project." Watch `monitoring` flip as you attack.
4. Turn on **Debug > Visible Collision Shapes** to see the sword's polygon relative to the sprite. Is the live window (the first 0.15 s) the part of the swing where the polygon sweeps through space in front of the player?
5. To see individual frames, run slower: `godot --path godot --time-scale 0.25` ("Force time scale … 1.0 is normal speed").

Write down what you saw, including anything that looks wrong. In our final version, swing two starts by snapping the blade from 75° back to about −60° within one frame. The numbers are pinned; whether that snap reads as a fast recovery or as a glitch is your call.

### Ship It

Commit in steps, so every step can be diffed on its own: baseline, pinned test, animation change, fix, re-pin. Add a dated entry to your project's `FRICTIONAL.md`. Say what you asked for, what the check reported (all FAIL lines, including the ones you did not ask for), what you saw when you played, and what stays unverified (no enemy to hit; feel judged by you alone).

The Brutalist skill that fits this week is **`godot-gamedev`** ("pairing each focused code excerpt with the visible game result it produces"). The syllabus lists a game-development explainer for Week 10. Here, the natural pair is the one-line `seek(0.0)` and swing two, before and after.

### Verify

Run all three checks yourself, with the time step pinned. Don't take the agent's pasted output as the result.

```bash
godot --headless --path godot --script res://tests/test_sword_timing.gd --fixed-fps 120
```

```bash
godot --headless --path godot --script res://test_input.gd --fixed-fps 120
```

```bash
godot --headless --path godot --script res://test_combo.gd --fixed-fps 120
```

Wrap them in `timeout 120` if your shell has it. A GDScript error before `quit()` leaves headless Godot running forever. That happened to one of our Chapter 11 runs, where an orphaned test process ran for about half an hour before it was stopped.

A pass establishes that, under these three scripted input sequences at a fixed 120 fps, the sword's state follows the pinned frames and the invariants hold. It does not establish that anything is hit, that the hitbox matches the art, that other tap rhythms behave, or that the combo feels good. Those four are yours.

---

## What we actually ran

Everything below happened on 2026-09-27 on the instructor's Mac, in a scratch copy, with Godot `4.7.2.stable.official.ed1daf0bf`. The full record is in [`../examples/10-animation-foundations/`](../examples/10-animation-foundations/).

**Starting point.** The Walker build's `godot/` folder and Markdown files, copied and committed as the scratch baseline (`980dee1`). Both existing tests passed: 18 of 18 and 11 of 11. Before delegating anything, we ran our own frame-stepping probe (`reviewer/probe_sword_frames.gd`) so that we would know the truth independently of whatever the agent reported. It showed swing two holding at 75°.

**Run 1: Claude Code 2.1.150, prompt 1.** Model `claude-sonnet-4-6` (the account default), with the permission flags above but without `--disallowedTools "Skill"`, which we added to the printed command afterwards on a colleague's report that a nested session had tried to invoke a settings-writing skill. The session ran from 17:58 to 18:57 UTC. In 20 turns it read ten files, ran eight shell commands, wrote one temporary measuring script, and produced 13 extended-reasoning blocks totalling about 248,000 characters. Then it stopped with:

```text
You've hit your session limit · resets 6:40pm (America/New_York)
```

It never wrote the test. (The Chapter 11 session, running at the same time on the same account, stopped with the same message.) The transcript's trimmed excerpt and the leftover measuring script are in `sessions/`. Treat a usage limit as a normal failure mode: the agent's work to that point is in your working tree, uncommitted, and nothing about it is verified.

**Run 1b: Codex CLI 0.153.4, the same prompt.** Configured model `gpt-5.6-sol` at low reasoning effort (from `~/.codex/config.toml`), `--sandbox workspace-write`. It took about five minutes (18:58–19:03 UTC). It reported the timing sources with line references, then created only `godot/tests/test_sword_timing.gd` (187 lines). Its report listed four anomalies without fixing any of them:

```text
- Swing 2 starts `attack_fast` at animation position `0.25`, travels `0°`,
  and finishes at the original animation's endpoint. Calling
  `play("attack_fast")` while that animation is already playing does not
  restart it.
- Swing 1 begins with rotation `0°`, despite the animation's time-zero
  rotation key being `-80°`.
- At 120 Hz, the 0.10 and 0.25 method keys are observed on frames 14 and 32,
  rather than the nominal frames 12 and 30.
- The hitbox remains enabled for the entire Attack state; there is no
  narrower animation-keyed damage window.
```

The first matches our own probe. The second we had not isolated: the very first attack after launch shows the blade at 0° for one frame. We read the test for the prompt's rules. It uses only `Input.parse_input_event`, loads a fresh `Demo.tscn` per scenario, and only reads state. Our run of it, three times: `RESULT 20 checks; 0 failures`. Commit `9d42df2`.

**Run 2: Codex, prompt 2 (77 seconds).** The diff added a discrete `monitoring` track to each attack animation (`[true, false]` at `0, 0.15` and `0.05, 0.25`) and deleted one line, `monitoring = true`, from `sword.gd`. Our run:

```text
FAIL single: hitbox turns on at frame 1 (actual 2)
FAIL single: hitbox turns off at frame 56 (actual 20)
FAIL every combo swing has at least one hitbox-on frame
RESULT 20 checks; 3 failures
```

`test_input.gd` still printed 18 of 18 and `test_combo.gd` 11 of 11. The agent classified the failures correctly. The first two were asked for (the key at 0.0 s applies on the next processed frame; the key at 0.15 s is observed on frame 20, two frames after the nominal 18). The third was "Change not asked for. The second combo swing replays `attack_fast` while that same animation is already at 0.25 seconds … it never crosses the new 0.0-second `true` key." That is the whole chapter in one line of output. The change was correct as requested. It exposed a latent bug, and it would have shipped a combo whose second hit can never land. The two older tests would have let it through. Commit `917c521`.

**Run 3: Codex, prompt 3 (67 seconds).** One line, added after `play()` in `sword.gd`:

```gdscript
$AnimationPlayer.play(attack_current["animation"])
$AnimationPlayer.seek(0.0)
```

All seven invariants passed, including the one that had failed. Ten TIMING pins moved, and the agent listed each one as a behavior "a designer now has to approve." Swing two now starts at position 0.0 and travels 289.75° instead of 0°. The one-frame 0° flash on swing one is gone (its travel drops from 255° to 175°). Every later key arrives one frame earlier: buffer at 13, ready at 31, Idle at 55, hitbox off at 19. Our probe after the change shows swing two moving: 75.0°, −59.9°, −41.2°, −24.0° on consecutive frames. Commit `2422163`.

**Run 4: Codex, prompt 4 (69 seconds).** The diff touches only the constants block and its comment (9 lines changed). Commit `9b174cf`. The approval in prompt 4 was given for this worked example on the strength of the numbers and the probe. The human play check in Use It has not been done by us on a visible build. It is pending, and the example README says so.

**Our verification of the final state.**

| Command | Runs | Result |
|---|---|---|
| `test_sword_timing.gd --fixed-fps 120` | 3 | 20/20 each |
| `test_sword_timing.gd` with no `--fixed-fps` | 3 | 7, 9 and 9 failures, different frame numbers each run; all 7 invariants passed every time |
| `test_input.gd --fixed-fps 120` | 1 | 18/18 |
| `test_combo.gd --fixed-fps 120` | 1 | 11/11 |

The unpinned rows show what the invariants are good for. They do not depend on frame numbers, so they held without a pinned time step. The frame-number pins only mean something with one.

**The whole change**, from `changes.diff`: 24 lines added to `Sword.tscn` (two tracks), one line removed and one added in `sword.gd`, and the new 187-line test. The scratch repository's per-step diffs are in `diffs/01…04`.

---

## Check your understanding (ungraded)

1. Open `Sword.tscn` in a text editor. Which track on `attack_fast` would you change to make swing one's wind-up start from −100° instead of −80°, and which pinned numbers in `test_sword_timing.gd` would you expect to fail?
2. In the baseline, the key at 0.1 s is observed on frame 14 at 120 fps. List the two separate mechanisms (one from `play()`, one from the method callback mode) that each add a frame. Find the evidence for each in `logs/03-reviewer-probe-baseline.log` (that probe calls the first processed frame after the key press frame 0; the test calls it frame 1).
3. `test_combo.gd` passed 11 of 11 before and after every change in this chapter. Name one of its checks that could be rewritten to catch the swing-two bug, and write the one extra condition it needs.
4. The FSM demo's `SETUP` animation keys `monitoring = true`. Does anything ever play `SETUP`? How would you find out from the source, without running the game?
5. In `walker-3d-ik`, why did reading `get_bone_global_pose()` after a timer fail to show the IK result, while reading it inside a `skeleton_updated` handler succeeded? Quote the documentation sentence that justifies the fix.
6. Run the final test once without `--fixed-fps`. Which group of checks still passes, and why does that tell you something about how to write animation checks that survive machine load?

---

## Doing the same thing in Unity

Unity and Unreal were not run for this chapter. The comparisons come from their official documentation, checked on 2026-09-27; the Unity manual pages consulted identify themselves as Unity 6.6 (6000.6).

### Similarities

The task has the same shape: pin the hitbox timing and the combo window with a check that drives real input, change the clip, and read the check.

- **Clips are keyed data.** In Unity you author an Animation Clip in the Animation window by keying properties, the same idea as a Godot value track. The first time you create a clip on a GameObject, the manual says Unity "creates a new Animator Controller Asset", "adds the new clip into the Animator Controller as the default state", "adds an Animator Component to the selected GameObject", and assigns the controller to it.
- **Method tracks have an equivalent.** An Animation Event is used "to call a function at a specific point in time." The function "can be in any script attached to the GameObject" and takes at most one parameter. The sword's two method keys would be two Animation Events. Events can also be attached to imported, read-only clips, from the import settings' Animation tab.
- **Headless tests exist.** The Unity Test Framework runs Play Mode tests from the command line: `-runTests -batchmode -projectPath <path> -testResults <file> -testPlatform PlayMode`. With the Input System package, a test class that derives from `InputTestFixture` gets an isolated input system and helpers such as `Press`, `Release` and `Set`. A test can press the attack button rather than call the attack method, the same discipline as `Input.parse_input_event`.
- **Stepping can be controlled.** `AnimatorUpdateMode` offers Normal (the Update loop), Fixed (the FixedUpdate loop) and UnscaledTime. `Animator.Update(deltaTime)` "evaluates the animator based on deltaTime", with the manual's caution that it "might not work well with the physics engine or any other system that is normally evaluated by the Game loop."
- **Text an agent can read.** With the editor's Asset Serialization mode at Force Text, which the manual lists as the default, scenes, prefabs, `.anim` clips and `.controller` files are stored as text.

### Differences

- **An extra layer is standard.** A Godot `AnimationPlayer` plays a named clip directly. Unity's `Animation` component can too, but the manual calls it "the Legacy Animation component" and says: "For new projects, use the Animator component." So in Unity even a one-clip sword swing is a state in an Animator Controller, and "play the same swing again" is a question about that state machine's transitions and about `Animator.Play(stateName, layer, normalizedTime)`. The `Animator.Play` reference describes the `normalizedTime` offset, but it does not say what re-playing the current state does. That is exactly the kind of engine rule you pin with a test instead of assuming, as this chapter's Godot run showed.
- **Where the hitbox window lives.** In Godot you can key `monitoring` on the `Area2D` directly. In Unity the equivalent is an animated `enabled` property on the collider component, or a pair of Animation Events that enable and disable it. Both are clip data. The choice changes what your test must watch: a property value, or a function call.
- **IK is a package, not a node family.** Godot 4.7.2 ships `TwoBoneIK3D` and its siblings in the engine. Unity's two-bone IK is a constraint in the Animation Rigging package, which lets "the Tip of a limb … reach a Target position." 2D rigging is the 2D Animation package, which "includes features and tools that allow you to quickly rig and animate 2D characters."
- **YAML diffs are longer.** A forced-text `.anim` file is diffable, but curves are stored as key lists with tangents, so the change we made (two short key arrays) would be a longer YAML diff. Review it in the Animation window as well as with `git diff`.

| Godot 4.7.2 | Unity 6.6 |
|---|---|
| `AnimationPlayer` | `Animator` + Animator Controller (legacy: `Animation` component) |
| `Animation` resource in a `.tscn` | Animation Clip (`.anim`) |
| `AnimationLibrary` | clips referenced by controller states |
| Value track | Property curve |
| Method track | Animation Event |
| `callback_mode_process` idle / physics / manual | `AnimatorUpdateMode` Normal / Fixed / UnscaledTime; `Animator.Update()` |
| `TwoBoneIK3D` (`SkeletonModifier3D`) | Animation Rigging: Two Bone IK constraint |
| `Skeleton2D` / `Bone2D` / `Polygon2D` | 2D Animation package |
| `godot --headless --fixed-fps 120 --script res://tests/…` | `Unity -batchmode -runTests -testPlatform PlayMode` |

## Doing the same thing in Unreal Engine

Checked against the Unreal Engine documentation on 2026-09-27; the pages consulted identify themselves as Unreal Engine 5.8. Unreal Engine is source-available, not open source. The source is on GitHub for accounts that link an Epic account and accept the Unreal Engine EULA.

### Similarities

- **Timed events in the clip.** Animation Notifies "provide a way for you to create repeatable events synchronized to Animation Sequences." A plain Notify fires once, like a method key. An Anim Notify State has a duration, with Begin, Tick and End. The sword's live-hitbox window maps naturally onto one Notify State whose Begin turns collision on and whose End turns it off. That pairing is this chapter's suggestion, not an example on Epic's page, whose examples are effects, sounds, cloth and trails.
- **Combos as sequenced sections.** An Animation Montage lets you "combine several Animation Sequences into a single asset and control playback with Blueprints", divided into Montage Sections that "can be dynamically played back in any order through logic at runtime." The fast-fast-medium combo is a montage with three sections, and the combo buffer decides which section plays next. Whether jumping back to the start of the same section restarts it is, again, something to pin with a test.
- **IK after animation.** IK Rig "provides a method of interactively creating Solvers that perform pose editing", and the resulting asset "can then be embedded into any animation systems, such as Animation Blueprints." Control Rig lets you rig and animate characters in the editor. Both play the role of Godot's `SkeletonModifier3D` family: they change the pose after animation has produced it.
- **Automated tests.** The Automation System is "designed to do gameplay level testing." Its test types include unit, feature, smoke, content stress, screenshot comparison and functional tests. The documented command-line form is `-ExecCmds="Automation RunTest <Name>;Quit"`.

### Differences

- **Assets are binary.** Animation Sequences, Montages, Notifies and Blueprints are `.uasset` files. Epic's own diff-tool page says that "with Assets and Blueprints, a textual representation would not be constructive." An agent cannot read or change a notify's timing the way it edits `"times": PackedFloat32Array(0.1, 0.25)` in a `.tscn`.
- **Editor scripting is the agent's way in.** The Python Editor Script Plugin lets a script change assets, but "the Python environment is only available in the Unreal Editor, not when your Project is running … including Play In Editor, Standalone Game, cooked executable." An agent could move a notify with an editor script. The proof that the hitbox now opens on a different frame would still have to come from an automation or functional test that runs the game.
- **More moving parts per swing.** In Godot, the sword scene carries its own timing. In Unreal it is spread across the Sequence (keys), the Montage (sections), the Notify State (window), and the Blueprint or C++ that reacts to the notify. Pinning behavior before a change matters more when the change touches four assets you cannot diff as text.

| Godot 4.7.2 | Unreal Engine 5.8 |
|---|---|
| `Animation` resource | Animation Sequence (`.uasset`) |
| Method track key | Anim Notify |
| Keyed `monitoring` window | Anim Notify State (Begin / Tick / End) |
| Combo table in `sword.gd` + three clips | Animation Montage with sections |
| `SkeletonModifier3D`, `TwoBoneIK3D` | IK Rig, Control Rig |
| `git diff` of `.tscn` text | UE Diff Tool (visual) |
| `godot --headless --script` test | Automation test via `-ExecCmds="Automation RunTest …;Quit"` |

---

## Sources

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation, checked on 2026-09-27. Godot behavior marked "printed from the binary" or "measured" comes from runs of Godot 4.7.2 recorded in `examples/10-animation-foundations/logs/`.

**Godot (docs.godotengine.org, stable = 4.7 on 2026-09-27)**
- Animation class: https://docs.godotengine.org/en/stable/classes/class_animation.html
- AnimationPlayer: https://docs.godotengine.org/en/stable/classes/class_animationplayer.html
- AnimationMixer: https://docs.godotengine.org/en/stable/classes/class_animationmixer.html
- AnimationLibrary: https://docs.godotengine.org/en/stable/classes/class_animationlibrary.html
- Introduction to the animation features: https://docs.godotengine.org/en/stable/tutorials/animation/introduction.html
- Animation track types: https://docs.godotengine.org/en/stable/tutorials/animation/animation_track_types.html
- Tween: https://docs.godotengine.org/en/stable/classes/class_tween.html
- 2D sprite animation: https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html
- 2D skeletons: https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html
- SkeletonModificationStack2D (Experimental): https://docs.godotengine.org/en/stable/classes/class_skeletonmodificationstack2d.html
- Skeleton3D: https://docs.godotengine.org/en/stable/classes/class_skeleton3d.html
- SkeletonModifier3D: https://docs.godotengine.org/en/stable/classes/class_skeletonmodifier3d.html
- SkeletonIK3D (Deprecated): https://docs.godotengine.org/en/stable/classes/class_skeletonik3d.html
- TwoBoneIK3D: https://docs.godotengine.org/en/stable/classes/class_twoboneik3d.html
- Command line tutorial: https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- Overview of debugging tools (Remote scene tree, Visible Collision Shapes): https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html

**Walker and course files**
- `walker-2d-finite-state-machine`: `README.md`, `FRICTIONAL.md`, `FONT-PROVENANCE.md`, `input-debug-20260927.log`, `combo-20260927.log`
- `walker-3d-ik`: `README.md`, `FRICTIONAL.md`, and its `*-20260927.log` files
- `walker-demo-series/queue.json` (items 62 and 63)
- Upstream: https://github.com/godotengine/godot-demo-projects at `a3b5c113112f77291d5f3d1360f33a882fdc52f7` (`2d/finite_state_machine`, `3d/ik`), MIT
- Old course pages (Canvas export): Animation; Animation in Unity; Animation in Unreal Engine; Animation in Blender; Spriter tutorials; Assignment 6 – Animation
- Revised syllabus (`CSYE_7270_Virtual_Environments_and_Real-Time_3D.docx`), Week 10 row
- Chapter 0 of this book, on `--fixed-fps` and on the Codex sandbox

**Unity (docs.unity3d.com, pages showing Unity 6.6)**
- Animation Events: https://docs.unity3d.com/Manual/script-AnimationWindowEvent.html
- Animation events on imported clips: https://docs.unity3d.com/Manual/AnimationEventsOnImportedClips.html
- Creating a new Animation Clip: https://docs.unity3d.com/Manual/animeditor-CreatingANewAnimationClip.html
- Legacy Animation component: https://docs.unity3d.com/Manual/class-Animation.html
- Animator.Play: https://docs.unity3d.com/ScriptReference/Animator.Play.html
- Animator.Update: https://docs.unity3d.com/ScriptReference/Animator.Update.html
- AnimatorUpdateMode: https://docs.unity3d.com/ScriptReference/AnimatorUpdateMode.html
- Editor settings, Asset Serialization: https://docs.unity3d.com/Manual/class-EditorManager.html
- Test Framework command line (package 1.4): https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html
- Input System testing (package 1.11): https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/Testing.html
- Animation Rigging, Two Bone IK (package 1.3): https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/constraints/TwoBoneIKConstraint.html
- 2D Animation package (10.1): https://docs.unity3d.com/Packages/com.unity.2d.animation@10.1/manual/index.html

**Unreal Engine (dev.epicgames.com, pages showing 5.8)**
- Animation Notifies: https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-notifies-in-unreal-engine
- Animation Montage: https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-montage-in-unreal-engine
- IK Rig: https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-ik-rig
- Control Rig: https://dev.epicgames.com/documentation/en-us/unreal-engine/control-rig-in-unreal-engine
- Automation Test Framework: https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine
- Run Automation Tests: https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine
- UE Diff Tool: https://dev.epicgames.com/documentation/en-us/unreal-engine/ue-diff-tool-in-unreal-engine
- Scripting the Unreal Editor using Python: https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python
- Unreal Engine on GitHub (source access under the EULA): https://www.unrealengine.com/ue-on-github

**Tools**
- Claude Code 2.1.150 (`claude --help`, run on 2026-09-27); Codex CLI 0.153.4 (`codex exec --help`, run on 2026-09-27)
