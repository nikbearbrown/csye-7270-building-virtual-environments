# Module 4 — Scenes, collision and physics

CSYE 7270 · Fall 2026 · Week 4

## Executive summary

A Godot game is a tree of nodes, saved pieces of that tree are scenes you reuse, and the pieces talk through signals. Code runs on two clocks, and contact is detected by collision objects filtered by layers and masks and measured against collision shapes that are not the artwork. This is where agent-written gameplay fails most quietly: the code reads well, the game runs, and the bug is a mask bit, a signal that fires only once, or a collider that no longer sits under its drawing. You will add a shield pickup to a Walker adaptation of Godot's "Dodge the Creeps", as its own scene on its own named physics layer, with a headless test that steps physics frames. On 27 September 2026 the same prompt went to Claude Code and to Codex. Both produced a working shield and a passing test, yet Claude Code's test also passed when the shield was broken on purpose, and a check written by a human caught it. The tests establish state, not that the shield is visible, that pickups appear in fair places, or that the game is fun. This module is the physics half of Assignment 3.

## The question

You pick up a shield. A creep flies into you while you are shielded, and nothing happens, as intended. The creep is slow and is still on top of you when the shield runs out. Do you die?

In "Dodge the Creeps" as written, the player dies in exactly one place: the handler for its `body_entered` signal. That signal fires when an overlap **begins**. This overlap began while you were shielded, and nothing new enters when the shield ends, so unless your code checks again you survive standing inside a creep. The code looks correct and the game runs. A playtest may never hit the case, because creeps move at 150 to 250 pixels per second and one has to stay on you until the shield ends. An agent writes this kind of bug fluently.

## The ideas

The Module 1 vocabulary still holds (node, scene, scene tree, signal, script, collision shape, asset); this module adds the machinery under it.

### Scenes, instances and ownership

A **node** does one job. A **scene** is a saved tree of nodes, stored as a `.tscn` text file, which is why an agent can read and edit it. The [TSCN format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html) has four kinds of section: `[ext_resource]`, `[sub_resource]`, `[node]` and `[connection]`. **Instancing** reuses a saved scene as a template: change the source scene and every instance updates, but a property changed on an instance overrides it ([instancing](https://docs.godotengine.org/en/stable/getting_started/step_by_step/instancing.html)). Dodge the Creeps instances in both directions. The Player is placed once at edit time; `main.gd` instances a Mob at run time on every `MobTimer` timeout (every 0.5 s). The design question hiding in every instanced scene is **ownership**: who creates it, and who frees it. A Mob frees itself when it leaves the screen, and `new_game()` frees the rest.

One detail explains many confusing diffs: Godot does not store a property that equals its default. The Player's collision layer and mask never appear in `player.tscn` because both are the default, 1. When an agent adds `collision_mask = 5`, that single line is the whole change. Also remember that the saved scene is not the running **scene tree**. In `walker-jumpman`, `main.tscn` holds one node, and `session.gd` builds the level, player and camera in code ([SceneTree](https://docs.godotengine.org/en/stable/tutorials/scripting/scene_tree.html)). When the editor shows a tiny tree, ask what the scripts add.

### Signals, groups and autoloads: who tells whom

A **signal** is a message a node emits, and other nodes connect to it ([signals](https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html)). Emitting calls every connected method immediately; only `CONNECT_DEFERRED` waits for the end of the frame. Dodge wires its loop through five `[connection]` lines in `main.tscn`.

Trace one death. The physics engine notices a mob inside the Player's shape and emits the built-in `body_entered`. That calls `_on_body_entered` in `player.gd`, which hides the player and emits the custom `hit` signal. `hit` calls `Main.game_over()`, which stops the timers and music and asks the HUD for "Game Over". Each object emits, and the scene file says who listens. The handler disables the player's collision shape with `set_deferred`, because you cannot change physics properties inside a physics callback ([Coding the player](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/03.coding_the_player.html)).

A **group** is a tag a node carries ([groups](https://docs.godotengine.org/en/stable/tutorials/scripting/groups.html)). `mob.tscn` saves its root in the group `mobs`, and `new_game()` clears the board with one line. Anything you spawn that is not in a group, and not freed by its own logic, survives a restart.

```gdscript
get_tree().call_group(&"mobs", &"queue_free")
```

An **autoload** is a script or scene Godot adds to the root before any other scene and keeps across scene changes ([autoload](https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html)). `walker-loading-autoload` registers one as `global="*res://global.gd"`, and its `goto_scene()` defers the switch with `call_deferred`, because the button that asked for the change belongs to the scene being deleted. `walker-loading-scene-changer` uses the engine's `change_scene_to_file()`, which builds that deferral in.

### Two clocks: `_process` and `_physics_process`

`_process(delta)` runs once per rendered frame, at a rate that varies across devices; use it for visuals and UI. `_physics_process(delta)` runs at a fixed rate, 60 times per second by default; use it for movement that collides and anything that must be reproducible ([idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)).

The engine updates contact information once per physics tick. The list from `Area2D.get_overlapping_bodies()` changes once during the physics step, not immediately after objects move ([Area2D](https://docs.godotengine.org/en/stable/classes/class_area2d.html)). Dodge moves its Player in `_process` by setting `position`, which works because the Player is an `Area2D`, a sensor rather than a body; contact is still judged on the next physics tick. A headless test that counts frames must pin this clock with `--fixed-fps 60`, so every frame is exactly 1/60 s of game time. Chapter 0's "time trap" shows a Pong test failing four runs out of six without the flag and passing every time with it.

### Four collision objects, and one way around them

The [physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html) defines four node types.

| Type | What the engine does with it | Where you meet it |
|---|---|---|
| `Area2D` | detects overlaps; never blocks or pushes | Dodge's Player, all of Pong, the pickup you will build |
| `StaticBody2D` | not moved by physics; others collide with it | jumpman's floor and walls |
| `RigidBody2D` | simulated physics: you set forces or velocity | Dodge's mobs |
| `CharacterBody2D` | collision detection, no physics: you call `move_and_slide()` | jumpman's Clawd |

Do not steer a `RigidBody2D` by rewriting its transform every frame ([RigidBody2D](https://docs.godotengine.org/en/stable/classes/class_rigidbody2d.html)), and keep a `CharacterBody2D` in `_physics_process` ([using CharacterBody2D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html)). The fifth option is no node at all: `walker-2d-bullet-shower` keeps 500 bullets as plain data, each owning a body handle in `PhysicsServer2D`, and one `_draw()` paints them ([servers](https://docs.godotengine.org/en/stable/tutorials/performance/using_servers.html)). You trade scene conveniences for lower per-object overhead; its README claims no speedup without a benchmark.

### Layers and masks: who can notice whom

`collision_layer` describes the layers an object appears **in**; `collision_mask` describes what layers it will **scan**. The [CollisionObject2D reference](https://docs.godotengine.org/en/stable/classes/class_collisionobject2d.html) states the rule: A can detect B only if B is in a layer A scans. Read it as asymmetric. Dodge's Player has layer 1 and mask 1, so it scans layer 1 and detects mobs. The Mob has layer 1 and a mask of `0`, so it scans nothing and mobs pass through each other. That mask does **not** stop the player from noticing mobs: detection runs from the player's mask to the mob's layer.

**Layer numbers are not bit values.** The editor and `project.godot` count layers from 1, but fields in code and in `.tscn` files are bitmasks, so layer *n* has the value 2^(n−1). `walker-jumpman-clawd` names layer 4 "Hazard" and layer 5 "Goal", and `session.gd` writes `collision_layer = 8` and `16` for them. Writing `4` "for layer 4" would put the object on layer 3. The functions `set_collision_layer_value(layer_number, value)` and `set_collision_mask_value(...)` take layer numbers, so prefer them. Name layers under Project Settings, Layer Names.

### The art is not the collider

A **collision shape** is geometry the physics engine uses; a sprite is what the player sees. Only your care ties them together. Dodge's Player draws its sprite at scale 0.5 and collides with a capsule of radius 27; change the art and nothing moves the capsule. `walker-jumpman-clawd` swapped in a wide mascot and kept the old 18 × 28 collider, and its FRICTIONAL log records that the broad arms can extend past the left world boundary. `walker-2d-dynamic-tilemap-layers` separates them on purpose: its `Secret` layer draws a wall but removes its collision at run time.

The sharpest case is `walker-2d-bullet-shower`. After 60 physics frames, a bullet's body sat at y = 272.394, sixteen pixels below its drawing at y = 256.3463. `PhysicsServer2D.body_create()` defaults to a rigid body, so gravity moved the body while the drawing never moved vertically. You would not see this by playing; bullets would only sometimes seem to hit you from below. The fix is one line setting the body mode to static, after which the log records `ALIGNED_BODIES 500/500`.

## The Walker example: walker-2d-dodge-the-creeps

**Get it.** [`walker-2d-dodge-the-creeps`](https://github.com/nikbearbrown/walker-2d-dodge-the-creeps) is public and keeps the upstream MIT license, published 27 September 2026 with a Walker brief, a recovered GDD and headless tests. Its provenance is Godot's [`godot-demo-projects`](https://github.com/godotengine/godot-demo-projects), path `2d/dodge_the_creeps`, commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`; starting there and applying the patch in the [example record](../../examples/04-scenes-collision-and-physics/README.md) is still valid. Obtain your own copy and do not edit the instructor's repository. Its music is CC-BY 3.0 and needs attribution if you show or ship it.

**What it is.** Godot's official "first 2D game": dodge creeps on a portrait 480 × 720 screen; score is survival time; one touch ends the run. The Walker adaptation changed two lines: the project title, and `rotation = 0` in `player.gd`'s horizontal branch, a fix for an upside-down player that the log reproduced first.

**What its checks establish.** `godot/test_input.gd` is a `SceneTree` script. It clicks the real Start button, presses real WASD keys through `Input.parse_input_event`, and passes 14 checks, among them orientation, normalized diagonal speed, the left boundary, timer-driven spawning and scoring, game over and restart. Its collision check is an explicit fixture that places a frozen mob on the player, and says so. Against the unmodified upstream demo it passes 13 of 14 and fails `horizontal movement resets orientation`, the reproduced bug, still there upstream.

**What remains unverified**, in the project's own words: no sound was heard and no GPU frames were inspected. It also lists gamepad controls, the GPU particle trail, offscreen mob cleanup and extended play.

Four smaller public builds show the same ideas:

| Build | What it demonstrates | Honest limit |
|---|---|---|
| [`walker-pong`](https://github.com/nikbearbrown/walker-pong) | every object an `Area2D`; 10 scripted-input checks at 30 and 60 FPS | not shown to be fun |
| [`walker-2d-bullet-shower`](https://github.com/nikbearbrown/walker-2d-bullet-shower) | 500 server-side bodies; 500/500 aligned after the fix | no speedup claimed |
| [`walker-2d-dynamic-tilemap-layers`](https://github.com/nikbearbrown/walker-2d-dynamic-tilemap-layers) | per-tile collision removed at run time; 11 assertions | fade appearance not seen |
| [`walker-loading-autoload`](https://github.com/nikbearbrown/walker-loading-autoload), [`walker-loading-scene-changer`](https://github.com/nikbearbrown/walker-loading-scene-changer) | persistent autoload; engine scene-change helpers; 12 and 48 assertions | layout unverified |

## Predict → Build It → Use It → Ship It → Verify

### 1. Predict

Answer in your own words before you delegate anything, and keep the answers.

1. The pickup and the player are both `Area2D`s. Which object's **mask** must change for the player to notice the pickup? Why doesn't the mob's `collision_mask = 0` already stop the player from noticing mobs?
2. A creep is overlapping you when the shield expires. Will `body_entered` fire again? What happens if the code only guards `_on_body_entered`?
3. `new_game()` frees mobs through the `mobs` group. What happens to a pickup left on screen at game over if nobody puts it in a group?
4. The pickup is freed in the player's `area_entered` handler, during physics processing. Which call is safe there, `free()` or `queue_free()`, and why is the player's own shape disabled with `set_deferred`?

### 2. Build It

Work on a copy with its own baseline commit, then record the baseline and run the existing test.

```bash
git init
```

```bash
git add -A
```

```bash
git commit -m "Baseline: walker-2d-dodge-the-creeps"
```

```bash
godot --headless --path godot --import
```

```bash
godot --headless --path godot --script res://test_input.gd --fixed-fps 60
```

Expect `RESULT failures=0`. The import matters: Godot must import the PNG and OGG assets into `godot/.godot/` before a script can load them. The chapter's own runs were not wrapped in `timeout` and none hung, but a script error before `quit()` leaves headless Godot running forever, so put `timeout 120` in front of every headless command.

The prompt was written *after* Predict, so your answers to questions 1 to 3 are in it as requirements. That is problem formulation, not cheating. Paste it into Claude Code as a single message.

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

The chapter ran this command from the project root, with the prompt saved as `prompt-shield.txt` one folder up. The allow list is deliberately narrow, because a rule like `Bash(env *)` would quietly allow any command.

```bash
claude -p "$(cat ../prompt-shield.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > ../session.jsonl
```

The Codex difference, on the same prompt and starting commit. Redirect stdin from `/dev/null`, or `codex exec` can wait on "Reading additional input from stdin..." in a script. The `workspace-write` sandbox blocks writes outside the project, and on macOS Godot's `user://` folder lives outside it, so Codex reported warnings about an unwritable `user://logs`. Codex reads `AGENTS.md` where Claude Code reads `CLAUDE.md`.

```bash
codex exec --sandbox workspace-write --json -o ../codex-last-message.md "$(cat ../prompt-shield.txt)" < /dev/null > ../codex-session.jsonl
```

### 3. Use It

Nothing below can be checked headless. Every item is a **HUMAN CHECK**; write down what you saw, not what you expected.

1. **HUMAN CHECK.** Open `godot/project.godot` in the Godot 4.7.2 editor, then `pickup.tscn`. Select the `CollisionShape2D` and compare its radius with the circle drawn in `pickup.gd`'s `_draw()`. They are two separate numbers.
2. **HUMAN CHECK.** Turn on Debug, Visible Collision Shapes ([debugging tools](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html)), and run with F5. Watch the capsules move with the sprites and the pickup's circle sit on its drawing.
3. **HUMAN CHECK.** Collect a pickup. Can you tell, without reading code, that you are shielded, and for how long? A 3-second shield with no countdown may feel arbitrary. That is a design finding, not a bug.
4. **HUMAN CHECK.** Park inside a creep while shielded and wait. You should die the moment the shield ends. If you survive, the expiry check is missing.
5. **HUMAN CHECK.** Let a pickup appear, die elsewhere, and restart. The old pickup must be gone.

### 4. Ship It

Commit the agent's change and your own check separately, so the history says who did what.

```bash
git add -A
```

```bash
git commit -m "Add shield pickup (agent) with its headless test"
```

Your own check is [`reviewer/verify_shield_timing.gd`](../../examples/04-scenes-collision-and-physics/reviewer/verify_shield_timing.gd), or one you write. Copy it into `godot/tests/`, run the import so Godot creates its `.uid` sidecar, then commit both files.

```bash
git add godot/tests/verify_shield_timing.gd godot/tests/verify_shield_timing.gd.uid
```

```bash
git commit -m "Add reviewer's shield timing check (human-written)"
```

Add a dated `FRICTIONAL.md` entry: your predictions and which were right, what the agent changed, what you checked, the mutation result, and what you have not seen on screen. Say plainly which parts were the agent's.

The Brutalist film skill that fits this work is `godot-gamedev`, the one Assignment 3 uses. The shield is a mechanism: touching a pickup changes state (`shielded`), which delays the hit. Show actual code, scenes, an input → state → output trace and the tests, and label headless checks as headless. The Brutalist Godot skills come from a course-provided checkout of [brutalist.art](https://github.com/nikbearbrown/brutalist.art); if your copy lacks the skill, request the update rather than inventing commands.

### 5. Verify

Run the checks yourself; do not accept the agent's pasted output as evidence.

```bash
godot --headless --path godot --script res://test_input.gd --fixed-fps 60
```

```bash
godot --headless --path godot --script res://tests/test_shield.gd --fixed-fps 60
```

```bash
godot --headless --path godot --script res://tests/verify_shield_timing.gd --fixed-fps 60
```

Then try to break the code the test protects. Change the shield duration to 0.5 seconds, run the agent's test, and put the duration back. In Claude Code's version the duration is the constant `SHIELD_DURATION` in `godot/player.gd`; in Codex's it is the `wait_time` of the `ShieldTimer` node in `godot/player.tscn`. If the test still passes, it is not measuring what its label claims.

**What a pass proves:** under scripted input and an explicit frozen-mob fixture, the pickup is collected through real movement, shielded contact is ignored, the hit lands a measured number of physics ticks after collection, the layer and mask values match the spec, and restart clears state. **What it does not prove:** that a player can see the shield, that pickups spawn somewhere fair, that natural collisions at glancing angles behave the same, or that the change improves the game.

## What the agents got wrong

Run on 27 September 2026 (Godot 4.7.2, Claude Code 2.1.150, Codex CLI 0.153.4) and re-checked by a human with `--fixed-fps 60`.

1. **A test that claimed more than it measured.** Both agents re-check `get_overlapping_bodies()` when the shield ends, so the hard case was right. But Claude Code's check "hit fires within 10 physics frames after shield expires" starts counting about 3.35 seconds after the mob is placed, not at expiry. With the shield shortened to 0.5 s, its test still passed 7 of 7. Codex's test caught that mutant only by accident of its timeline. The reviewer's check records `Engine.get_physics_frames()` at collection and at the hit, expects 177 to 190 ticks, passes both agents' real code at 181, and fails the mutant at 31.
2. **Engine bookkeeping invented by hand.** Claude Code wrote `pickup.gd.uid` with a made-up value and cited it from `pickup.tscn`; Godot rejected it with an `invalid UID` warning and the agent deleted the reference. Two other invented identifiers stayed, the scene's own `uid` and a `unique_id` on `PickupTimer`. Godot loads them, but they are the engine's bookkeeping, not fields to write. Codex left them out; its own slip was naming layer 1 "Mobs" although the Player sits on layer 1 too. One thing went right: when Claude Code's first test run failed, the agent fixed the **test** with a 2.2 s wait and did not weaken the assertion.
3. **An exit code that hid 55 errors.** A fresh clone ran `test_shield.gd` before importing and printed seven `PASS` lines, exit code 0, and 55 `ERROR` lines for textures and sounds that could not load. After the import the same tests ran with zero errors. Exit code 0 is not a clean run; read the log.

## If you know Unity or Unreal

Unity and Unreal were not run for this module; the comparisons come from official documentation, checked on 27 September 2026.

| Godot | Unity | Unreal Engine 5 |
|---|---|---|
| scene (`.tscn`), instance | Prefab, prefab instance | Blueprint class or Actor, placed instance |
| `Area2D` + `body_entered` | trigger collider + `OnTriggerEnter2D` | collision component + `OnComponentBeginOverlap` |
| `collision_layer` + `collision_mask` | one layer per object + Layer Collision Matrix | Object Type + Block/Overlap/Ignore, both sides |
| `get_overlapping_bodies()` | `OnTriggerStay2D`, `Collider2D.IsTouching` | Get Overlapping Actors |
| `_physics_process` (60 Hz) | `FixedUpdate` (50 Hz default) | tick groups around the physics step |
| autoload | `DontDestroyOnLoad` object | Game Instance Subsystem |

Overlap events fire on entry in all three, so the shield-expiry question is the same everywhere. The big difference for an agent workflow is what it can read. Godot's `.tscn` files are text an agent can diff. Unity's default scene and prefab serialization is text too, but it references assets by GUIDs and file IDs, so a careless hand edit is the Unity version of the invented `uid://`. Unreal's Blueprints and levels are binary: an agent can review a C++ pickup but not a Blueprint graph, so more review lands on you in the editor. The [chapter](../../chapters/04-scenes-collision-and-physics.md) has the full comparison.

## Practice assessment (ungraded)

Answer in your own words, from your own run and the source. An ungraded practice quiz on Canvas covers the same ground; take it as often as you like and read the feedback.

1. A creep overlaps you when a 3-second shield ends. Explain why a game guarded only by `body_entered` lets you survive, and name the call both agents used to fix it.
2. Give the `collision_layer` value for an object on layer 3 and on layer 2. Which single wrong digit in a player mask would make the player stop seeing pickups?
3. You shorten the shield to 0.5 s and the agent's test still passes. What does that tell you about the test, and what would a better check record?
4. Why is moving an `Area2D` in `_process` acceptable here, and why would it not be for a `CharacterBody2D` that must stop at walls?
5. Name two things a headless pass cannot tell you about the shield, and the human check for each.

Do not paste Claude's explanation as proof of your understanding. Ask it to question you, then answer and check the source yourself.

## The next step

Next is **Assignment 3, "Build a Prop in Blender and Make It Work in Godot."** It opens in Module 3, this module completes it, and it is due about Day 30. Treat this module as the physics half of that work: once your prop is in Godot, its visible mesh and its collision shape are separate things, and layers, masks and signals on entry decide whether anything notices it. The shield is taught in 2D because those builds are small enough to read; Chapter 5's 3D example uses `Area3D` with the same layer arithmetic. Read the assignment's own text for what it requires. Module 5 then moves to specifying an interaction before building it. The long reading is the companion chapter, [Chapter 4 — Scenes, Collision and Physics](../../chapters/04-scenes-collision-and-physics.md).
