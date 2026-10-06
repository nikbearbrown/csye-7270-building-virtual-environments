# Module 10 — Animation foundations

CSYE 7270 · Fall 2026 · Week 10

## Executive summary

In Godot an animation is data: a clip holds tracks, each bound to a node, each holding keys that are times and values in a text scene file, which is why an agent can retime one in seconds and why a wrong number raises no error. This module teaches Godot 4.7.2 animation through the Week 10 rule: establish behavior checks before changing animation tracks, timing or transitions. You pin the sword timing of a combo demo with a frame-stepped headless check, make one animation change, read what the check says, fix what it catches, and re-pin on purpose. The run on 27 September 2026 found that the demo's second combo swing never plays on screen even though the build's own combo test passed; the final check passes 20 of 20, though Claude Code hit its usage limit before writing the test and Codex completed the same prompts. None of this shows that the swings look right, that the hitbox matches the blade, or that anything is hit, because the demo has no enemy; those judgments are yours. This module and Module 11 feed Assignment 8.

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

The combo counter says swing two started on frame 31. The playhead says the clip is a quarter of a second in, and the blade sits at 75° for 24 frames. It never moves. Both are right: the counter really did go to 2, and the blade really did not swing. The test checked a number in a script, not a motion on screen. Why does Godot keep playing instead of restarting? Which frame does a key at 0.1 s fire on? And how do you write a check that would have noticed?

## The ideas

### An animation is data bound to node paths

The [`Animation`](https://docs.godotengine.org/en/stable/classes/class_animation.html) class holds data divided into tracks, and each track is linked to a node. A track is a path to a node, usually plus one property, and a list of keys; each key is a time, a value and an easing value. The [`AnimationPlayer`](https://docs.godotengine.org/en/stable/classes/class_animationplayer.html) plays animations stored in `AnimationLibrary` resources, and shares a base class, [`AnimationMixer`](https://docs.godotengine.org/en/stable/classes/class_animationmixer.html), with the `AnimationTree` of Module 11; that base owns the timing rules both use. A scene file is text, so all of it is readable. Here is the sword's fast attack from `godot/player/weapon/Sword.tscn`, trimmed to two of its four tracks:

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

Read it as machinery. Track 0 swings the blade from −80° to 85° in 0.15 s and settles at 75° by 0.2 s; `0.439427` is an easing value. Track 3 calls two methods on the sword: at 0.1 s one opens the combo input buffer, at 0.25 s the other says the next swing may start. The clip is 0.45 s long, so the blade sits still for the last 0.25 s, because `length` is not delimited by the last key. Value tracks set node properties (`rotation_degrees`, `visible`, `monitoring`), method tracks call functions, and 4.7.2 has nine track types in all. The [track-types tutorial](https://docs.godotengine.org/en/stable/tutorials/animation/animation_track_types.html) warns that method-track events are not executed when you preview in the editor, so scrubbing never shows the combo window opening. The demo's `SETUP` animation has no special meaning to the engine and nothing plays it, so do not ask an agent to "fix the reset pose" there.

### Between keys, and Tween or AnimationPlayer

Three separate settings decide what happens between two keys ([introduction to animation](https://docs.godotengine.org/en/stable/tutorials/animation/introduction.html)).

- **Interpolation**, per track: nearest, linear or cubic; for rotations, linear-angle or cubic-angle, which take the shortest path around the circle.
- **Transition**, per key: the easing curve used when approaching that key. `1` is linear.
- **Update mode**, per value track: continuous updates between keys; discrete updates only at the keys; capture is continuous but captures the object's current value. A boolean such as `monitoring` wants discrete, because nothing lies between `true` and `false`.

A [`Tween`](https://docs.godotengine.org/en/stable/classes/class_tween.html) is created from code with `create_tween()`, animates toward a target and is then discarded; the reference says tweens are not designed to be reused. A clip is authored ahead of time, stored in a scene and replayed. The course rule: if a designer needs to scrub and retime it, it belongs in an `Animation`; if the end value comes from gameplay, such as a health bar sliding to the current value, it belongs in a `Tween`. A gameplay fact like "the hitbox is live" should not depend on a tween that can be killed halfway.

### When animation runs, and how to count frames

This decides whether a hitbox is live on frame 12 or 14, and none of it shows in the editor.

- **Callbacks.** `callback_mode_process` chooses physics, idle or manual processing; both `AnimationPlayer` and `AnimationTree` default to idle in 4.7.2. `callback_mode_method` defaults to deferred, so a method key runs at the end of the frame in which the playhead crossed it, after that frame's scripts have read the old value.
- **Starting.** The playhead is still 0.0 on the first processed frame after `play()`. The measurement later in this module saw a key at 0.1 s, frame 12 on paper at 120 fps, fire on frame 14.
- **Replaying the same name.** If `play()` is called with the animation already assigned, the reference says it resumes if paused. Nothing restarts a clip that is already playing. That sentence answers the question above.

Three command-line flags make this testable ([command-line reference](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)): `--headless` (no window, no sound device), `--script <path>` (run a script that `extends SceneTree` as the whole program) and `--fixed-fps <n>`, which disables real-time synchronization so every frame advances game time by exactly 1/n s. The project runs 120 physics ticks per second, so with `--fixed-fps 120` one rendered frame is one physics tick is 1/120 s, and `await process_frame` in a loop counts frames exactly. Without the flag, the pinned timing test that passes 3 of 3 times failed 7, 9 and 9 of its 20 checks in three runs, with different frame numbers each time.

### Sprite sheets, cycles and loop seams

The old course's animation assignment asked for three things that survive as engine-neutral ideas: a simple animation such as a rotating coin, a sprite sheet or rigged sprite, and a movement cycle whose first and last frame match. Godot's [2D sprite animation tutorial](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html) gives two routes. `AnimatedSprite2D` plays a `SpriteFrames` resource built from images or a sheet cut into a grid. Or a `Sprite2D` with `hframes` and `vframes` has its `frame` keyed in an `AnimationPlayer`, which the tutorial calls a bit more complex but able to animate other properties. Prefer it for anything gameplay reads, so the hitbox, the sound and the frame share one timeline.

A loop seam is a testable fact. For a looping clip the values at time 0 and at `length` should match, and `loop_mode` should be `LOOP_LINEAR` or `LOOP_PINGPONG`; you can assert both headlessly. Whether the cycle reads as a walk is a human check. The old rubric also named timing and spacing; in Godot terms, timing is the key times, and spacing is the interpolation and easing between them.

### Skeletons and IK

In 2D, a `Skeleton2D` holds `Bone2D` nodes and a `Polygon2D` is skinned to them with painted weights. In 3D, a `Skeleton3D` holds the poses that animation tracks write, and procedural changes on top are nodes that inherit [`SkeletonModifier3D`](https://docs.godotengine.org/en/stable/classes/class_skeletonmodifier3d.html). Two of its rules matter for tests: a modification always runs after the `AnimationMixer`'s playback, and the final pose exists when the skeleton's `skeleton_updated` signal fires. 4.7.2 ships solvers such as `TwoBoneIK3D`; the older `SkeletonIK3D` is marked Deprecated, yet the Walker IK build uses it because the upstream demo does.

## The Walker example: walker-2d-finite-state-machine

[`walker-2d-finite-state-machine`](https://github.com/nikbearbrown/walker-2d-finite-state-machine) is the Walker adaptation of `2d/finite_state_machine` from `godot-demo-projects` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`. It is public and keeps the upstream MIT license; its `godot/` folder differs from upstream only in the project name and two added tests.

**What it is.** A top-down character with a hierarchical state machine. Idle, Move, Jump, Stagger and Attack are child nodes of a `StateMachine` node, and the last three are pushed onto a stack. The sword is its own scene, `player/weapon/Sword.tscn`: an `Area2D` hitbox with a `CollisionPolygon2D`, a `Sprite2D` and an `AnimationPlayer` holding five animations (`SETUP`, `attack_circular`, `attack_fast`, `attack_medium`, `idle`). `sword.gd` runs a combo table: fast, fast, medium, with damage 1, 1 and 3.

**What its checks establish.** Two headless tests drive real key events through `Input.parse_input_event`. `test_input.gd` has 18 checks and `test_combo.gd` has 11; the instructor reran both on an unmodified copy on 27 September 2026 with Godot 4.7.2 and got 18 of 18 and 11 of 11.

**What remains unverified.** The build's `FRICTIONAL.md` says the main scene has no enemy or health target, so damage metadata does not establish hit behavior, and its `BodyPivot` and `sword.visible` assertions are state measurements, not inspected frames. No gameplay footage exists. Add one item: "second swing starts" asserts `sword.combo_count == 2` and never looks at the animation.

### The counterweight: walker-3d-ik

[`walker-3d-ik`](https://github.com/nikbearbrown/walker-3d-ik) adapts `3d/ik` (MIT): four scenes around the Godot Battle Bot model, driven by a GDScript FABRIK solver and the built-in `SkeletonIK3D`. Its first failures were about how to observe animation, not about the game.

1. **A real scheduling bug.** The FABRIK script's `update_mode` setter turned on `_process` when asked for physics updates. `test_modes.gd` reproduced it (7 of 8 before); a one-line change fixed it (8 of 8 after).
2. **A sampling trap.** The first navigation run passed 10 of 12. The test read `get_bone_global_pose()` after a timer, between skeleton updates, and saw a pose without the IK applied. Reading it inside a `skeleton_updated` handler made all 12 pass with no production change.
3. **A backend limit.** In a headless run, requesting `MOUSE_MODE_CAPTURED` reads back as visible (`requested 2 observed 0`), so the first-person navigation test stays at 4 of 8. The build neither patched gameplay around that nor opened a window.

Decide when in the frame you observe: reading at the wrong moment can fail a working rig or pass a broken one.

## Predict → Build It → Use It → Ship It → Verify

### 1. Predict

Write your answers down before you delegate.

1. `test_combo.gd` says "second swing starts" when `combo_count` reaches 2. What would a check have to record every frame to know the blade actually moved?
2. The hitbox is switched on by code for the whole attack. If you move it into `monitoring` keys at 0.0 s and 0.15 s in `attack_fast`, on which frame (at 120 fps) will it turn on and off? Exactly frames 0 and 18?
3. If swing two re-plays `attack_fast` without restarting it, what happens to swing two's hitbox once the window lives in the animation?
4. Which of the two existing Walker tests would notice?

### 2. Build It

**Set up your copy.** The chapter's Build It starts from the upstream demo at the commit every Walker adaptation came from (the recorded run itself used a scratch copy of the Walker build's `godot/` folder). The Walker repository is now public and already holds the two tests in its `godot/` folder, so you may take them from there.

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

Copy `test_input.gd` and `test_combo.gd` into `sword-timing/godot/` (the course repository keeps them under [`examples/10-animation-foundations/tests/walker-harness/`](../../examples/10-animation-foundations/tests/walker-harness/test_combo.gd)). Then, from inside `sword-timing`:

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

Import before any test. A fresh copy has no `.godot/` import cache. In the instructor's Codex sandbox check, a test run on an un-imported copy still printed 11 of 11 PASS while the textures and font failed to load, with `ERROR` lines in the output. A PASS line is not the whole log.

**Prompt 1: pin what exists.** Paste this into Claude Code or Codex, started in `sword-timing`.

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

Notice what the prompt does. It names the one file that may be created. It forbids the shortcuts that pass a test without playing the game: direct method calls and state writes. It separates numbers you may change later (TIMING) from facts that must survive (INVARIANT). And it keeps anomalies and reports them, because a pin records what is, not what should be.

With Claude Code, headless, scoped to the tools this task needs:

```bash
claude -p "$(cat prompt-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --disallowedTools "Skill" --max-turns 60 --output-format stream-json --verbose > session-1.jsonl
```

With Codex:

```bash
codex exec --sandbox workspace-write --json -o last-message-1.txt "$(cat prompt-1.txt)" < /dev/null > codex-session-1.jsonl
```

Two Codex differences matter. The `workspace-write` sandbox blocks writes outside the project, so Godot prints `ERROR: Failed to open 'user://logs/…'` and cannot save editor settings during import; both are harmless here. And `< /dev/null` stops `codex exec` waiting for standard input in a script. Commit the pinned test before you continue.

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

You expect failures, because you asked for a timing change. The question is whether you asked for every one.

**Prompt 3: fix what the check caught.** Write this one yourself from what prompt 2 reports. The chapter's version, after the pinned check flagged swing two:

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

**Prompt 4: re-pin, only after you approve.** Play the game first (Use It, below). The chapter's record skipped this: the instructor's lab machine runs headless only, so the re-pin was approved on the numbers and a probe alone, and the play check is still pending there. Do not copy that shortcut. Then:

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

Keep the change and the re-pin in separate prompts and commits: an agent that edits the behavior and the expectation in one step can make any change pass. Adjust the counts and dates quoted in prompts 3 and 4 to what your own run reports.

### 3. Use It

The headless check gives frame numbers, not whether a swing reads as a swing. Open `sword-timing/godot/project.godot` in the editor.

1. Select `player/weapon/Sword.tscn`, open the Animation panel and scrub `attack_fast`. Watch the blade and the new `monitoring` track. Remember that the method track does not fire while you scrub.
2. **HUMAN CHECK.** Run the project (F5) on the baseline commit. Press F three times with a short gap and watch swing two. Then check out your final commit and do it again.
3. While it runs, switch the Scene dock to **Remote** and select the Sword node; watch `monitoring` flip as you attack.
4. **HUMAN CHECK.** Turn on **Debug → Visible Collision Shapes** to see the sword's polygon against the sprite. Is the live window, the first 0.15 s, the part of the swing where the polygon sweeps through space in front of the player?
5. **HUMAN CHECK.** To see individual frames, run slower with `godot --path godot --time-scale 0.25`.

Write down what you saw, including anything that looks wrong. In the chapter's final version, swing two starts by snapping the blade from 75° back to about −60° within one frame. The numbers are pinned; whether that reads as a fast recovery or a glitch is your call.

### 4. Ship It

Commit in steps, so each can be diffed alone: baseline, pinned test, animation change, fix, re-pin. Add a dated entry to `FRICTIONAL.md`: what you asked for, what the check reported (every FAIL line, including the ones you did not ask for), what you saw when you played, and what stays unverified (no enemy to hit; feel judged by you alone). The old course asked for original animation project files, never just an exported GIF; in Godot the project file is the scene and its keys, so commit them.

For this practice, `godot-gamedev` fits: the one-line `seek(0.0)` and swing two, before and after. Assignment 8 requires a `godot-walkthrough` film, which shows the game running, so capture it on a real screen. The Brutalist skills come from a course-provided checkout; if yours lacks the skill, request the update.

### 5. Verify

Run all three checks yourself with the time step pinned. Do not take the agent's pasted output as the result.

```bash
godot --headless --path godot --script res://tests/test_sword_timing.gd --fixed-fps 120
```

```bash
godot --headless --path godot --script res://test_input.gd --fixed-fps 120
```

```bash
godot --headless --path godot --script res://test_combo.gd --fixed-fps 120
```

Wrap them in `timeout 120` if your shell has it: a GDScript error before `quit()` leaves headless Godot running forever, and one orphaned test process in a Chapter 11 run ran about half an hour.

A pass establishes that, under these three scripted input sequences at a fixed 120 fps, the sword's state follows the pinned frames and the invariants hold. It does not establish that anything is hit, that the hitbox matches the art, that other tap rhythms behave, or that the combo feels good.

## What the agents got wrong

All of this ran on 27 September 2026 on the instructor's Mac with Godot 4.7.2, Claude Code 2.1.150 (default model `claude-sonnet-4-6`) and Codex CLI 0.153.4 (configured model `gpt-5.6-sol`, low reasoning effort).

**A green test that counted swings, not motion.** The Walker build's own combo test passed 11 of 11 while swing two never moved, because it asserted a counter. The instructor found it with a frame-stepping probe written before any agent ran, so the truth was known independently of the agents' reports.

**An agent that ran out of road.** Claude Code worked for 59 minutes over 20 turns, read ten files and ran eight shell commands, then stopped on the account's session limit without writing the test. Codex completed the same prompt in about five minutes. A usage limit is a normal failure mode: the agent's work sits in your tree, uncommitted and unverified.

**A correct change that broke an unrelated promise.** Codex made the prompt 2 change as asked, and the pinned check printed three failures: two the change caused on purpose (the hitbox turned on at frame 2, not 1, and off at frame 20, not 56) and one it did not. The agent classified them correctly: swing two replays `attack_fast` while it is already at 0.25 s, so it never crosses the new 0.0 s `true` key. The older tests still passed 18 of 18 and 11 of 11, and would have shipped a combo whose second hit can never land.

**A test that sampled at the wrong moment.** The first `walker-3d-ik` navigation test read a bone pose between skeleton updates and failed a working rig, as described above. The fix was to observe at the moment the documentation says the pose is final, with no change to the game.

## If you know Unity or Unreal

Unity and Unreal were not run for this module; the comparisons come from their official documentation, checked in the chapter on 27 September 2026.

| Godot 4.7.2 | Unity 6.6 | Unreal Engine 5.8 |
|---|---|---|
| `AnimationPlayer` + `Animation` resource | `Animator` + Animation Clip (`.anim`) | Animation Sequence (`.uasset`) |
| method track key | Animation Event | Anim Notify |
| keyed `monitoring` window | animated collider `enabled`, or two Animation Events | Anim Notify State |
| combo table in `sword.gd` + three clips | Animator Controller states and transitions | Animation Montage with sections |
| `godot --headless --fixed-fps 120 --script …` | `Unity -batchmode -runTests -testPlatform PlayMode` | Automation test via `-ExecCmds="Automation RunTest …;Quit"` |
| `.tscn` text | `.anim` YAML (Force Text, the default) | `.uasset` binary |

The biggest difference for an agent workflow is where the timing lives and whether it can be read. In Godot the sword scene carries its own timing as text an agent can edit and `git diff` shows. Unity's clips are text too, but curves are key lists with tangents, so the same change is a longer diff, and even a one-clip swing is a state in an Animator Controller. In Unreal the timing is spread across a Sequence, a Montage, a Notify State and the Blueprint that reacts, all binary: an agent can move a notify with an editor script but cannot show you a diff, and the proof must come from a test that runs the game. [The chapter](../../chapters/10-animation-foundations.md) has the full comparison.

## Practice assessment (ungraded)

Answer in your own words, using the source and the running game:

1. What does the check "second swing starts" establish, and what would a check that catches the swing-two bug have to record?
2. Which of the final test's checks passed without `--fixed-fps`, and what does that say about checks that survive machine load?
3. Why did reading `get_bone_global_pose()` after a timer miss the IK result, and what did the fix rely on?
4. What does a passing 20 of 20 not tell you about the sword?

The Canvas practice quiz covers the same ground. Do not paste Claude's explanation as proof of your understanding. Ask it to question you, then answer and check the source yourself.

## The next step

This module and Module 11 feed **Assignment 8 - Animation Wired to Player Actions**, which opens in Module 10 and is due about Day 80. Keep the habit from this week: pin the behavior, change one thing, and read every failure before you approve it. Module 11 connects animation states to player actions. The long reading, with the full Unity and Unreal comparisons, is the companion chapter, [Chapter 10 — Animation Foundations](../../chapters/10-animation-foundations.md).
