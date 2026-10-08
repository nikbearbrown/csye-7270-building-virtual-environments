# Chapter 4 — Scenes, Collision and Physics

CSYE 7270 · Fall 2026 · Week 4

## Executive summary

**What this chapter is.** How a Godot game is put together and how it notices contact. A game is a tree of nodes. Scenes are saved pieces of that tree, and you instance them as often as you need. Parts talk through signals, groups and autoloads. Code runs on two clocks, the frame and the physics tick. Contact is detected by four kinds of collision object, filtered by layers and masks, and measured against collision shapes that are not the artwork.

**Why read it.** This is where agent-written gameplay goes wrong most quietly. The code is plausible, the game runs, and the bug is a mask bit, a signal that fires only once, or a collider that no longer sits under its drawing. You cannot catch those by reading a summary. You catch them by knowing what the engine reports, and when.

**What you build.** A shield pickup for Godot's "Dodge the Creeps", as its own scene, on its own named physics layer, with a headless test that steps physics frames. On 27 September 2026 we gave the same prompt to Claude Code and to Codex. Both produced a working shield and a passing test. Claude Code's test also passed when we broke the shield on purpose, shortening it from 3.0 seconds to 0.5. A check we wrote ourselves caught that, because it pins the timing to the physics tick.

**What it does and does not prove.** The tests establish state: the pickup is collected, the player survives shielded contact, the hit lands 181 physics ticks after collection, restart clears everything. They do not establish that the shield is visible, that pickups appear in fair places, or that the game is more fun. A person has to play it.

---

## The question

You pick up a shield. A creep flies into you while you are shielded. Nothing happens, as intended. The creep is slow and still on top of you when the shield runs out.

Do you die?

In "Dodge the Creeps" as written, the player dies in exactly one place: the handler for its `body_entered` signal. That signal fires when an overlap **begins**. This overlap began while you were shielded, and nothing new enters when the shield ends. So unless your code checks again, you survive standing inside a creep. The code looks correct and the game runs. A playtest may never hit the case: the creeps move at 150 to 250 pixels per second, so one has to stay on you until the very moment the shield ends. That is exactly the kind of bug an agent writes fluently.

This chapter answers the question by taking apart what Godot actually reports about contact, when it reports it, and how to test it one physics tick at a time.

---

## Ideas you need

The course vocabulary from Chapter 1 still holds: node, scene, scene tree, signal, script, collision shape, asset. This chapter adds the machinery under those words.

### Nodes and scenes: composition you can save

A **node** does one job: draw a sprite, hold a collision shape, count down a timer. A **scene** is a saved tree of nodes. It can be a whole level or a single creep. Godot stores scenes as `.tscn` text files, and that is why an agent can read and edit them. The [TSCN format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html) has four kinds of section: `[ext_resource]` for files the scene uses, `[sub_resource]` for resources defined inside it, `[node]` for each node, and `[connection]` for each signal connection.

**Instancing** means reusing a saved scene as a template. The [instancing page](https://docs.godotengine.org/en/stable/getting_started/step_by_step/instancing.html) is blunt about the rule: when you change the source scene, "all instances … will see their values update", but "changing a property on an instance always overrides values from the corresponding packed scene." Dodge the Creeps instances in both directions. The Player is placed once, at edit time. The Mob is instanced many times while the game runs:

```text
# godot/main.tscn — edit-time instance, and a scene handed to the script
[node name="Main" type="Node" unique_id=1975992027]
script = ExtResource("1_0r6n5")
mob_scene = ExtResource("2_50pww")
[node name="Player" parent="." unique_id=927660131 instance=ExtResource("3_veqnc")]
```

```gdscript
# godot/main.gd — run-time instances, one per MobTimer timeout (every 0.5 s)
func _on_MobTimer_timeout():
	var mob = mob_scene.instantiate()
	# ... choose a point on MobPath, a direction, and a speed of 150–250 px/s
	add_child(mob)
```

The design question hiding in every instanced scene is **ownership**: who creates it, and who frees it. Get that wrong and you leak objects or free something still in use.

| Scene | Root node type | Who instances it | Who frees it |
|---|---|---|---|
| `main.tscn` | `Node` | the project (`run/main_scene`) | the engine, on quit |
| `player.tscn` | `Area2D` | `main.tscn`, at edit time | nobody; it is hidden and reused |
| `mob.tscn` | `RigidBody2D` | `main.gd`, on every `MobTimer` timeout | itself when it leaves the screen; `new_game()` frees the rest |
| `hud.tscn` | `CanvasLayer` | `main.tscn`, at edit time | nobody |

One detail explains a lot of confusing diffs. "To make files more compact, properties equal to the default value are not stored" ([TSCN format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html)). The Player's collision layer and mask never appear in `player.tscn`, because both are the default, 1. When an agent adds `collision_mask = 5`, that line is the whole change.

### The scene tree: what is actually running

The **scene tree** is the live hierarchy. The [SceneTree page](https://docs.godotengine.org/en/stable/tutorials/scripting/scene_tree.html) describes the rules you will trip over. Processing and drawing happen "in tree order, or top to bottom as seen in the editor". But a parent's `_ready()` runs "only after all its child nodes have their `_ready()` functions called". When a scene is removed, nodes are notified bottom to top.

The saved scene and the running tree are not the same thing. In Chapter 1's `walker-jumpman`, `main.tscn` holds one node. `session.gd` builds the level, the player and the camera in code at run time. When the editor shows a tiny tree, ask what the scripts add.

### Signals: who tells whom

A **signal** is a message a node emits when something happens to it. Other nodes connect to it. The [signals page](https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html) calls this the observer pattern: it lets "one game object … react to a change in another without them referencing one another." By default, emitting calls every connected method **immediately**. Only a connection made with `CONNECT_DEFERRED` waits until "idle time (at the end of the frame)" ([Object](https://docs.godotengine.org/en/stable/classes/class_object.html)).

Dodge the Creeps wires its whole game loop through five connections at the bottom of `main.tscn`:

```text
[connection signal="hit" from="Player" to="." method="game_over"]
[connection signal="timeout" from="MobTimer" to="." method="_on_MobTimer_timeout"]
[connection signal="timeout" from="ScoreTimer" to="." method="_on_ScoreTimer_timeout"]
[connection signal="timeout" from="StartTimer" to="." method="_on_StartTimer_timeout"]
[connection signal="start_game" from="HUD" to="." method="new_game"]
```

Trace one death. The physics engine notices a mob inside the Player's shape and emits the Player's built-in `body_entered`. That calls `player.gd`'s `_on_body_entered`. It hides the player and emits the custom `hit` signal. `hit` calls `Main.game_over()`, which stops the timers and the music and asks the HUD for "Game Over". No object reaches into another. Each one emits, and the scene file says who listens.

There is a physics detail in `_on_body_entered`, and the upstream comment states it plainly: you must disable the collision shape with `set_deferred`, because "we can't change physics properties on a physics callback." The [tutorial](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/03.coding_the_player.html) explains that disabling it immediately "can cause an error if it happens in the middle of the engine's collision processing."

### Groups: tags you can call

A **group** is a tag, and a node can have as many as it needs ([groups](https://docs.godotengine.org/en/stable/tutorials/scripting/groups.html)). `mob.tscn` saves its root with `groups=["mobs"]`. `new_game()` then clears the board with one line:

```gdscript
get_tree().call_group(&"mobs", &"queue_free")
```

Anything you spawn that is not in a group, and not freed by its own logic, survives a restart. The hands-on depends on that.

### Autoloads: nodes that outlive scenes

An **autoload** is a script or scene that Godot adds "to the root viewport before any other scenes are loaded" and keeps across scene changes ([autoload](https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html)). You register it under Project Settings, Globals, Autoload. The docs add a warning: it is not a "true" singleton, since you can still instance it again yourself.

`walker-loading-autoload` registers one in `project.godot`:

```text
[autoload]
global="*res://global.gd"
```

Its `goto_scene()` never frees the current scene directly. It calls `_deferred_goto_scene.call_deferred(path)`, because the button that asked for the change belongs to the scene being deleted. Freeing a scene from inside its own callback "might be a bad idea", as the script's comment puts it. The sibling project, `walker-loading-scene-changer`, uses the engine's helpers, `change_scene_to_file()` and `change_scene_to_packed()`. They build the same deferral into the engine: the current scene is removed at once, and the old one is deleted and the new one added at the end of the frame ([SceneTree](https://docs.godotengine.org/en/stable/classes/class_scenetree.html)).

### Two clocks: `_process` and `_physics_process`

Godot runs your code on two schedules ([idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)):

| Callback | When it runs | Use it for |
|---|---|---|
| `_process(delta)` | once per rendered frame; the rate "varies over time and across devices" | visuals, UI, anything that only needs to look smooth |
| `_physics_process(delta)` | at a fixed rate, "60 times per second by default" | movement that collides, forces, anything that must be reproducible |

The physics engine updates contact information once per physics tick. `Area2D.get_overlapping_bodies()` says so directly: "this list is modified once during the physics step, not immediately after objects are moved" ([Area2D](https://docs.godotengine.org/en/stable/classes/class_area2d.html)). Dodge the Creeps moves its Player in `_process`, by setting `position`. That works because the Player is an `Area2D`, a sensor rather than a body. Contact is still judged on the next physics tick.

A headless test that counts frames has to pin this clock. Pass `--fixed-fps 60` so every frame is exactly 1/60 s of game time. [Chapter 0, "The time trap"](00-the-toolchain.md#the-time-trap-frames-are-not-seconds) shows the same untouched Pong test failing four runs out of six without the flag, and passing every time with it.

### Four collision objects, and one way around them

The [physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html) defines four node types. Every Walker example in this chapter uses at least one of them:

| Type | What the engine does with it | Where you meet it |
|---|---|---|
| `Area2D` | "detection and influence": reports overlaps, never blocks or pushes | Dodge's Player, all of Pong, jumpman's spikes and flag, the pickup you will build |
| `StaticBody2D` | "not moved by the physics engine"; others collide with it | jumpman's floor and walls |
| `RigidBody2D` | "simulated 2D physics": you set forces or velocity, the engine moves it | Dodge's mobs: `gravity_scale = 0.0`, `linear_velocity` set once at spawn |
| `CharacterBody2D` | "collision detection, but no physics": you move it with `move_and_slide()` | the tilemap demo's player, jumpman's Clawd |

Two cautions come straight from the class references. A `RigidBody2D` should not be steered by rewriting its transform every frame: "Changing the 2D transform or linear_velocity very often may lead to unpredictable behaviors" ([RigidBody2D](https://docs.godotengine.org/en/stable/classes/class_rigidbody2d.html)). And a `CharacterBody2D` belongs in `_physics_process`, where `is_on_floor()` reflects the last `move_and_slide()` ([using CharacterBody2D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html)).

The fifth option is no node at all. `walker-2d-bullet-shower` keeps 500 bullets as plain data. Each bullet owns only a body handle in `PhysicsServer2D`, and one `_draw()` paints them all. The [servers page](https://docs.godotengine.org/en/stable/tutorials/performance/using_servers.html) explains the trade. Nodes cost something per object, "tens of thousands of instances" can be a bottleneck, and servers give you opaque RIDs that you "allocate and free manually". You trade the scene system's conveniences for lower per-object overhead. The Walker README declines to put a number on that gain: "No performance speedup is claimed without a comparative benchmark."

### Layers and masks: who can notice whom

Every collision object has two 32-bit fields. The [physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html) defines them in one line each. `collision_layer` "describes the layers that the object appears **in**". `collision_mask` "describes what layers the body will **scan**". The [CollisionObject2D reference](https://docs.godotengine.org/en/stable/classes/class_collisionobject2d.html) states the rule that decides every contact: "Object A can detect a contact with object B only if object B is in any of the layers that object A scans."

Read that rule as asymmetric, and Dodge the Creeps makes sense:

| Object | Layer | Mask | Consequence |
|---|---|---|---|
| Player (`Area2D`) | 1 (default) | 1 (default) | scans layer 1, so it detects mobs |
| Mob (`RigidBody2D`) | 1 (default) | `0` (set in `mob.tscn`) | scans nothing, so mobs pass through each other |

The mob's mask of 0 does **not** stop the player from noticing mobs. Detection runs from the player's mask to the mob's layer. The mob's mask only controls what the mob collides with. `bullets.gd` uses the same trick: `body_set_collision_mask(bullet.body, 0)`, with the comment "Don't make bullets check collision with other bullets".

**Layer numbers are not bit values.** The editor and `project.godot` count layers from 1. The fields in code and in `.tscn` files are bitmasks, so layer *n* has the value 2^(n−1). `walker-jumpman-clawd` names its layers in `project.godot`:

```text
[layer_names]
2d_physics/layer_1="World"
2d_physics/layer_2="Player"
2d_physics/layer_4="Hazard"
2d_physics/layer_5="Goal"
```

and then, in `session.gd`, puts hazards on layer 4 by writing `collision_layer = 8`, and the goal on layer 5 by writing `16`. Writing `collision_layer = 4` "for layer 4" would put the object on layer 3. The functions `set_collision_layer_value(layer_number, value)` and `set_collision_mask_value(...)` take layer numbers, so prefer them in code you want to read. You name layers in Project Settings, under Layer Names, 2D Physics.

### The art is not the collider

A **collision shape** is geometry the physics engine uses. A **sprite** is what the player sees. Nothing ties them together except your care:

- Dodge's Player draws its sprite at `scale = Vector2(0.5, 0.5)` and collides with a capsule of radius 27, height 68. The Mob's capsule is radius 37, height 100, rotated 90° on its own node, under a sprite scaled 0.75. Change the art and nothing moves the capsule.
- `walker-jumpman-clawd` swapped in the wide Clawd mascot and deliberately kept the old 18 × 28 collider. Its FRICTIONAL log records the result: "the broad arms can extend beyond the left world boundary", which is a question for a human.
- `walker-jumpman`'s spikes are three exact triangular `CollisionPolygon2D`s, matching the drawn triangles, "no oversized invisible box".
- `walker-2d-dynamic-tilemap-layers` separates art from collision on purpose. Its `Secret` layer draws a wall but removes the wall's collision at run time, in `_tile_data_runtime_update`, so the player can walk through a fake wall.

The sharpest example is `walker-2d-bullet-shower`. Its FRICTIONAL log records a failed check. After 60 physics frames, a bullet's physics body sat at y = 272.394, 16 pixels below its drawing at y = 256.3463. The body was falling. `PhysicsServer2D.body_create()` defaults to `BODY_MODE_RIGID` ([PhysicsServer2D](https://docs.godotengine.org/en/stable/classes/class_physicsserver2d.html)), so gravity integrated each body between the script's position updates. The drawing never moved vertically. The collider did. The Walker fix is one line, `body_set_mode(bullet.body, PhysicsServer2D.BODY_MODE_STATIC)`, after which the log records `ALIGNED_BODIES 500/500`. You would not see this bug by playing. You would only notice that bullets sometimes seem to hit you from below.

---

## The Walker example: `walker-2d-dodge-the-creeps`

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-jumpman`](https://github.com/nikbearbrown/walker-jumpman), [`walker-loading-autoload`](https://github.com/nikbearbrown/walker-loading-autoload), [`walker-loading-scene-changer`](https://github.com/nikbearbrown/walker-loading-scene-changer), [`walker-2d-bullet-shower`](https://github.com/nikbearbrown/walker-2d-bullet-shower), [`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd), [`walker-2d-dynamic-tilemap-layers`](https://github.com/nikbearbrown/walker-2d-dynamic-tilemap-layers), [`walker-2d-dodge-the-creeps`](https://github.com/nikbearbrown/walker-2d-dodge-the-creeps), [`walker-pong`](https://github.com/nikbearbrown/walker-pong). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

**What it is.** Godot's official "first 2D game". The [tutorial](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/index.html) builds it from scratch; the finished project lives in the demo repository. The player dodges creeps that cross the screen. Score is survival time. One touch ends the run.

**Where it came from.** Godot's demo collection, [`godot-demo-projects`](https://github.com/godotengine/godot-demo-projects), path `2d/dodge_the_creeps`, commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`. The code is MIT-licensed: the root `LICENSE.md` keeps the Godot contributors' notice, and `godot/LICENSE` keeps KidsCanCode's 2017 notice. The assets carry their own terms, recorded in `godot/README.md`. The music, "House In a Forest Loop" by HorrorPen, is CC-BY 3.0 and needs attribution. The images, Kenney's Abstract Platformer, are CC0. The Xolonium font is under the SIL OFL 1.1.

**What the Walker adaptation changed.** Two lines. The project title became "Walker — Dodge the Creeps", and `player.gd` gained `rotation = 0` in its horizontal-movement branch. The FRICTIONAL log explains why. Source reading suggested that moving down, then right, left the player drawn upside down. The log says not to "call that a confirmed bug yet", and it was reproduced first, in `input-repro-20260924.log`, before the fix.

**What its checks establish.** `godot/test_input.gd` is a `SceneTree` script. It clicks the real Start button, presses real WASD keys through `Input.parse_input_event`, and passes 14 checks: start state, orientation, normalized diagonal speed, the left boundary, timer-driven spawning and scoring, and game over and restart. Its collision check is an explicit fixture. It places a frozen mob on the player, and the comment says so: "Explicit collision fixture, not a claimed natural encounter or footage."

**What remains unverified**, in the project's own words: "No sound was heard or GPU frames inspected." It also lists the remaining screen bounds, gamepad controls, the GPU particle trail, offscreen mob cleanup and extended play as unverified. The original game is portrait, 480 × 720.

**How you get it.** The Walker build is public at [github.com/nikbearbrown/walker-2d-dodge-the-creeps](https://github.com/nikbearbrown/walker-2d-dodge-the-creeps). To rebuild it from the upstream demo at the commit above instead, apply [`examples/04-scenes-collision-and-physics/starting-point/walker-adaptation.diff`](../examples/04-scenes-collision-and-physics/starting-point/walker-adaptation.diff) with `patch -p1`, and copy in `test_input.gd` from the same folder. We checked what happens if you skip the patch. The unmodified upstream demo passes 13 of the 14 checks and fails `horizontal movement resets orientation` ([log](../examples/04-scenes-collision-and-physics/logs/02-upstream-demo-with-walker-harness.log)). That is the reproduced bug, still there upstream.

### Four smaller Walker builds for the same ideas

| Build | What it demonstrates | Its recorded checks | Honest limit |
|---|---|---|---|
| [`walker-pong`](https://github.com/nikbearbrown/walker-pong) | Every object is an `Area2D`; paddles, walls, ceiling and floor react through `area_entered` connected to themselves | 10 scripted-input checks at 30 and 60 FPS: paddle bounds 16–384, contacts on all four surfaces, a deliberate miss, acceleration above 110 | its first route test failed on a harness viewport, not the game; "Machine checks do not establish whether it is fun" |
| `walker-2d-bullet-shower` | 500 server-side bodies, one `_draw()`, `body_shape_entered` counting touches | mouse-follow, count 500, collision and recovery, 500/500 bodies aligned with drawings after the `STATIC` fix | "No performance speedup is claimed without a comparative benchmark" |
| `walker-2d-dynamic-tilemap-layers` | A `TileMapLayer` whose collision is removed per tile at run time; an `Area2D` detector fades it | 11 input and physics assertions: the player walks through the fake wall to x = 310.396, fade to 0.3 and back, solid ground still collides | fade appearance not seen |
| `walker-loading-autoload` / `walker-loading-scene-changer` | a persistent autoload with deferred manual switching, and the engine's two change-scene helpers | 12 assertions over 4 button-driven transitions (autoload instance ID constant); 48 assertions over 12 mouse and keyboard transitions | rendered layout unverified |

Starting points: every build in the table is public at `github.com/nikbearbrown/<build name>`, and each also comes from the same upstream commit (Pong from `2d/pong`, the other four from paths `2d/bullet_shower`, `2d/dynamic_tilemap_layers`, `loading/autoload` and `loading/scene_changer`).

---

## Hands-on: add a shield pickup

### Predict

Answer these in your own words before you delegate anything. Keep the answers.

1. The pickup and the player are both `Area2D`s. Which object's **mask** must change for the player to notice the pickup? Why doesn't the mob's `collision_mask = 0` already stop the player from noticing mobs?
2. A creep is overlapping you when the shield expires. Will `body_entered` fire again? What happens if the code only guards `_on_body_entered`?
3. `new_game()` frees mobs through the `"mobs"` group. What happens to a pickup left on screen at game over if nobody puts it in a group?
4. The pickup is freed in the player's `area_entered` handler, during physics processing. Which call is safe there, `free()` or `queue_free()`, and why is the player's own shape disabled with `set_deferred`?

### Build It

Work on a copy. Get the starting point described above, then record a baseline:

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
timeout 120 godot --headless --path godot --script res://test_input.gd --fixed-fps 60
```

Expect `RESULT failures=0`. The import step matters. This project has PNG and OGG assets, and Godot must import them into `godot/.godot/` before a script can load them. See "What we actually ran" for what happens when you skip it.

Now the prompt. It was written *after* the Predict step, so the answers to questions 1–3 are in it as requirements. That is Problem Formulation, not cheating. Paste it into Claude Code as a single message:

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

This is the command we ran from the project root. The prompt was saved as `prompt-shield.txt` one folder up:

```bash
claude -p "$(cat ../prompt-shield.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > ../session.jsonl
```

`--max-turns` was accepted by Claude Code 2.1.150 but does not appear in `claude --help`. The allow list is deliberately narrow. As [Chapter 0](00-the-toolchain.md#permissions-and-sandboxes-what-the-agent-may-touch) found, a rule like `Bash(env *)` quietly allows any command.

**The Codex difference.** Same prompt, same starting commit, run from the project root:

```bash
codex exec --sandbox workspace-write --json -o ../codex-last-message.md "$(cat ../prompt-shield.txt)" < /dev/null > ../codex-session.jsonl
```

Redirect stdin from `/dev/null`. Without it, `codex exec` prints `Reading additional input from stdin...`, and from a script it can wait there. Our recorded run did not include the redirect. It printed that line and continued, but do not rely on that. The `workspace-write` sandbox allows writes inside the project and blocks them elsewhere. Codex reported that Godot "emitted environment warnings about its unwritable `user://logs` location". On macOS, `user://` lives under `~/Library/Application Support/Godot/app_userdata/`, which is outside the workspace. That matters again in Chapter 15, where the game saves data there. Codex reads `AGENTS.md` where Claude Code reads `CLAUDE.md`; Chapter 0 covers both.

### Use It

Nothing below can be checked headlessly. These are your human checks:

1. Open `godot/project.godot` in the Godot 4.7.2 editor. Open `pickup.tscn`. Select the `CollisionShape2D` and compare its radius with the circle drawn in `pickup.gd`'s `_draw()`. They are two separate numbers.
2. Turn on **Debug → Visible Collision Shapes**, which makes "collision shapes and raycast nodes … visible in the running project" ([debugging tools](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html)), and run the project (F5). Watch the capsules move with the sprites. Watch the pickup's circle sit on its drawing.
3. Collect a pickup. Can you tell, without reading code, that you are shielded, and for how long? A 3-second shield with no countdown may feel arbitrary. That is a design finding, not a bug.
4. Park inside a creep while shielded and wait. You should die the moment the shield ends. If you survive, the expiry check is missing.
5. Let a pickup appear, die elsewhere, restart. The old pickup must be gone.

Write down what you saw, not what you expected.

### Ship It

Commit the agent's change and your own check separately, so the history says who did what:

```bash
git add -A
```

```bash
git commit -m "Add shield pickup (agent) with its headless test"
```

Your own check is [`reviewer/verify_shield_timing.gd`](../examples/04-scenes-collision-and-physics/reviewer/verify_shield_timing.gd), or one you write. Copy it into `godot/tests/`, run `godot --headless --path godot --import` so Godot creates its `.uid`, then:

```bash
git add godot/tests/verify_shield_timing.gd godot/tests/verify_shield_timing.gd.uid
```

```bash
git commit -m "Add reviewer's shield timing check (human-written)"
```

Add a dated `FRICTIONAL.md` entry: your predictions, and which were right. Record what the agent changed, what you checked, and the mutation result below. Say what you still have not seen on screen. The "Next-entry template" at the end of `walker-jumpman-clawd`'s `FRICTIONAL.md` is a good shape. Say plainly which parts were the agent's.

The Brutalist skill that fits this work is **`godot-gamedev`**. The shield is a mechanism: an input (touching a pickup) changes state (`shielded`) that changes an outcome (the hit is delayed). The skill's contract, from [Required Brutalist Godot explainers](../prerequisites/brutalist-godot-explainers.md), is "actual code, scenes, resources, assets/art, an input → state → output trace, and relevant tests". Label the headless checks as headless.

### Verify

Run the checks yourself. Do not accept the agent's pasted output as evidence:

```bash
godot --headless --path godot --script res://test_input.gd --fixed-fps 60
```

```bash
godot --headless --path godot --script res://tests/test_shield.gd --fixed-fps 60
```

```bash
godot --headless --path godot --script res://tests/verify_shield_timing.gd --fixed-fps 60
```

Then try to break the code the test is supposed to protect. Change the shield duration to 0.5 seconds, run the agent's test, and put the duration back. If the test still passes, it is not measuring what its label claims.

**What a pass proves:** under scripted input and an explicit frozen-mob fixture, the pickup is collected through real movement, shielded contact is ignored, the hit lands a measured number of physics ticks after collection, the layer and mask values are what the spec said, and restart clears state. **What it does not prove:** that a player can see the shield, that pickups spawn somewhere fair, that natural collisions at glancing angles behave the same, or that the change improves the game.

---

## What we actually ran

**Date and tools.** 27 September 2026, macOS on the course Mac, Godot 4.7.2.stable.official.ed1daf0bf. Claude Code 2.1.150 with its default model in print mode, `claude-sonnet-4-6`. Codex CLI 0.153.4 with `gpt-5.6-sol`, the model set in the machine's Codex configuration. We passed it with `-m` and ignored the rest of that configuration with `--ignore-user-config`.

**Starting revision.** A scratch copy of `walker-2d-dodge-the-creeps`, containing its `godot/` folder and Markdown files, committed as baseline `03da9b0`. The editor import exited 0, and `test_input.gd` passed 14 of 14. The import also generated `godot/test_input.gd.uid`: that script had no `.uid` sidecar, and Godot 4.7.2's import created one. That file appears in both agents' diffs. Neither agent wrote it.

**Claude Code's change** (full diff in [`claude/changes.diff`](../examples/04-scenes-collision-and-physics/claude/changes.diff)). It ran 33 turns in 16 minutes, and the CLI reported a cost of $1.35.

- `project.godot`: named layer 3 `"Pickups"`. `pickup.tscn`: `collision_layer = 4` (layer 3's bit value), `collision_mask = 0`, `groups=["pickups"]`, and a `CircleShape2D` of radius 16 under a code-drawn circle of radius 14 with a ring at 17.
- `player.tscn`: `collision_mask = 5`, that is, layers 1 and 3. `player.gd`: a `shielded` flag and a float countdown in a new `_physics_process`. On expiry it loops over `get_overlapping_bodies()` and calls its own `_on_body_entered`. It also adds a blue `modulate` tint and an `area_entered` handler connected **in code**. The player's `body_entered` is still connected in the scene file, so this player's signals are now wired in two places.
- `main.gd` and `main.tscn`: a `PickupTimer` (5 s) and `_on_PickupTimer_timeout()` spawning at hard-coded x 40–440, y 40–680. `game_over()` stops it and `new_game()` clears the `"pickups"` group.

Two things went wrong inside the session. The agent noticed both from Godot's output:

1. It **hand-wrote UIDs**. It created `pickup.gd.uid` with the made-up value `uid://dp4q7rk9m8xv1` and cited it from `pickup.tscn`. Godot rejected it: `WARNING: res://pickup.tscn:3 - ext_resource, invalid UID: uid://dp4q7rk9m8xv1 - using text path instead`. The agent deleted the reference. Two other invented identifiers stayed: the scene's own `uid="uid://bn8r3k5p7qmlt"` and `unique_id=123456789` on the new `PickupTimer` node. Godot loads them. But the [TSCN format page](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html) says `unique_id` exists so Godot can track a node "even when [it is] moved or renamed". It is the engine's bookkeeping, not a field to invent. Codex left both fields out and let the engine handle it. That is the safer habit.
2. Its first `test_shield.gd` run failed `shielded contact does not stop gameplay timers`. The test placed the mob before the 2-second `StartTimer` had started the other timers. The agent fixed the **test**, adding a 2.2 s wait, and did not weaken the assertion. That was correct.

The Codex run's exact command line was `codex exec --ignore-user-config -m gpt-5.6-sol --sandbox workspace-write --json -o ../codex-last-message.md "$(cat ../../prompt-shield.txt)" > ../codex-session.jsonl`, run in the background without the `< /dev/null` redirect recommended above.

**Codex's change** ([`codex/changes.diff`](../examples/04-scenes-collision-and-physics/codex/changes.diff)) took about 2.5 minutes. It used 221,142 input tokens, of which 202,240 were cached, and 5,130 output tokens. Pickups went on layer 2, with the player's mask set to 3. The shield uses a one-shot `ShieldTimer` node (3.0 s) and a drawn ring. The spawn area is computed from the viewport, not hard-coded. Its test frees naturally spawned mobs before placing the fixture. One plausibility flag: it named layer 1 `"Mobs"`. But the Player sits on layer 1 too, so the name misdescribes the layer.

**Our verification.** Every command below was run by us, not by the agents. Both agents ran their tests without `--fixed-fps 60`, the flag [Chapter 0](00-the-toolchain.md#the-time-trap-frames-are-not-seconds) shows you need. So we re-ran everything with it, and every row in the table comes from runs with the flag. Without it, Claude Code's test also passed five real-time runs in a row. The logs are in [`examples/04-scenes-collision-and-physics/logs/`](../examples/04-scenes-collision-and-physics/logs/).

| Check | Claude Code's version | Codex's version |
|---|---|---|
| `test_input.gd`, `--fixed-fps 60`, 3 runs | 14/14 each run | 14/14 each run |
| agent's `test_shield.gd`, `--fixed-fps 60`, 3 runs | 7/7 each run | 6/6 each run |
| our `verify_shield_timing.gd` (11 checks) | 11/11; hit **181 ticks** after collection | 11/11; hit 181 ticks after collection |
| **mutant:** shield shortened to 0.5 s, agent's own test | **still 7/7 — did not notice** | 2 failures — noticed |
| mutant: shield 0.5 s, our check | fails: `elapsed 31 ticks` | fails: `elapsed 31 ticks` |
| mutant: expiry re-check deleted, agent's test | 3 failures — noticed | not run |

Those mutation rows are the finding. The agents did write the tricky part correctly: both re-check `get_overlapping_bodies()` when the shield ends. Claude Code's test even catches a naive expiry. But its "hit fires within 10 physics frames after shield expires" check starts counting about 3.35 seconds after the mob is placed (0.15 s plus a fixed 3.2 s wait), not at the moment the shield ends. A 0.5-second shield has long expired by then, the player is already hidden, and the check passes. The label claims more than the measurement. Codex's test caught the same mutant only by accident of its timeline. It waits for the 2-second start delay after collecting the pickup, so a short shield is gone before its "shielded contact" check runs.

Our own check, [`reviewer/verify_shield_timing.gd`](../examples/04-scenes-collision-and-physics/reviewer/verify_shield_timing.gd), records `Engine.get_physics_frames()` at collection and at the hit. It requires 177–190 ticks at 60 ticks per second. It also reads the layer and mask values from the running nodes, and it waits for a pickup spawned by the real `PickupTimer`, which landed at (67.6, 153.9), inside the view. Writing it took two tries. The first version left Godot reporting leaked audio objects at exit. Under `--fixed-fps 60`, `create_timer(0.25)` is game time, not wall time, so the audio thread had not drained the stopped streams. Waiting in wall time (`OS.delay_msec(300)`) fixed it. Walker's own `test_input.gd` shows the same end-of-run warning under `--fixed-fps 60`. Its checks are unaffected.

**One more trap.** We cloned the finished repository into an empty folder and ran `test_shield.gd` *before* importing. It printed seven `PASS` lines and exited 0, and the same log holds 55 `ERROR` lines. Every texture and sound had failed to load (`Unable to open file: res://.godot/imported/enemyFlyingAlt_1.png-….ctex`). After `godot --headless --path godot --import`, the same three test files ran with zero errors. An exit code of 0 is not a clean run. Read the log.

What nobody did: look at the game. Every run here was headless. The shield tint, the ring and the pickup drawing are unverified.

---

## Check your understanding (ungraded)

1. In `mob.tscn`, change `collision_mask = 0` to `collision_mask = 1`. Predict what changes in play, then run it and watch with Visible Collision Shapes on. Why doesn't `test_input.gd` catch the difference?
2. Claude Code put pickups on layer 3 and wrote `collision_layer = 4`. Codex put them on layer 2 and wrote `collision_layer = 2`. Give each version's player mask as a sum of bit values, and say which single wrong digit would make the player stop seeing pickups.
3. `walker-2d-bullet-shower`'s player counts `body_shape_entered` and `body_shape_exited` instead of using `body_entered`. How would a counter solve this chapter's question without calling `get_overlapping_bodies()`? What could make the counter drift?
4. Find where Dodge the Creeps' Player moves (`_process`) and where contact is judged. Explain why moving an `Area2D` in `_process` is acceptable here, and why it would not be for a `CharacterBody2D` that must stop at walls.
5. Open `walker-loading-autoload/godot/global.gd`. What would go wrong if `goto_scene()` called `get_tree().current_scene.free()` directly from the button's `pressed` handler?
6. Take the agent test you trust least and write one mutation that should make it fail. Run it. Did it?

---

## Doing the same thing in Unity

*Unity was not run for this chapter. The comparisons come from Unity's official documentation (the Unity 6 manual, 6000.x) and the Unity Test Framework manual, checked on 27 September 2026.*

### Similarities

- **Saved, reusable pieces.** A Unity [Prefab](https://docs.unity3d.com/Manual/Prefabs.html) stores "a GameObject complete with all its components, property values, and child GameObjects as a reusable asset", and supports instance overrides. That matches Godot's scenes and instance overrides. A pickup becomes a Pickup prefab, instanced from a spawner script.
- **Triggers that fire on entry.** Make the pickup's `CircleCollider2D` a trigger (`isTrigger`). Unity then calls [`OnTriggerEnter2D`](https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnTriggerEnter2D.html) "when another object enters a trigger collider", provided one of the two objects has a `Rigidbody2D`. Like `body_entered`, it fires on **entry**. The shield-expiry question is identical. Unity's answers are [`OnTriggerStay2D`](https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnTriggerStay2D.html), sent "once per physics update" while overlapping, or [`Collider2D.IsTouching`](https://docs.unity3d.com/ScriptReference/Collider2D.IsTouching.html), which, like Godot's overlap list, reports "the last physics system update".
- **Two clocks.** `Update` runs per rendered frame. [`FixedUpdate`](https://docs.unity3d.com/ScriptReference/MonoBehaviour.FixedUpdate.html) runs at fixed intervals, "0.02 seconds (50 calls per second)" by default, so Unity's default physics rate is 50 Hz where Godot's is 60. A test that counts physics steps must use the right rate.
- **Objects that outlive a scene.** [`DontDestroyOnLoad`](https://docs.unity3d.com/ScriptReference/Object.DontDestroyOnLoad.html) keeps a root object when "the load of a new Scene destroys all current Scene objects", which is the autoload role.

### Differences

- **Layers work differently.** In Unity, "you can only assign each GameObject to one layer" ([layers](https://docs.unity3d.com/6000.2/Documentation/Manual/create-layers.html)). Which layers collide is one project-wide table, the [Layer Collision Matrix](https://docs.unity3d.com/Manual/LayerBasedCollision.html), a checkbox per pair of layers. Godot gives every object a multi-bit layer *and* its own mask, and detection runs one way. The Dodge setup, where the player detects mobs that detect nothing, is one mask value in Godot. In Unity it is a matrix setting shared by every object on those layers. Unity also reserves a layer: "Layer 31 is used internally by the Editor's Preview window mechanics."
- **Components, not node types.** A Unity GameObject gains physics by adding `Rigidbody2D` and `Collider2D` components. Its [body type](https://docs.unity3d.com/Manual/2d-physics/rigidbody/body-types/rigidbody-2d-body-types-landing.html) is Dynamic, Kinematic or Static. Godot makes the choice by picking the node type (`RigidBody2D`, `CharacterBody2D`, `StaticBody2D`, `Area2D`).
- **Signals versus events.** Godot's scene file lists `[connection]` lines. Unity wires C# events, or UnityEvents, inside serialized components.
- **What an agent can read.** Unity's default [Asset Serialization Mode](https://docs.unity3d.com/Manual/class-EditorManager.html) is Force Text, so scenes and prefabs are text. The format is "a custom subset of the YAML data serialization language" ([format](https://docs.unity3d.com/Manual/FormatDescription.html)), and it references objects by `fileID` and asset GUIDs. An agent can diff a prefab, but a hand edit that breaks a `fileID` or GUID is the Unity version of this chapter's invented `uid://`. C# scripts are plain text.
- **Headless testing.** Write a Play Mode test with the Unity Test Framework. A [`[UnityTest]`](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-attribute-unitytest.html) runs as a coroutine, and `yield return new WaitForFixedUpdate()` steps one physics cycle, the equivalent of `await physics_frame`. Run it with `-runTests -batchmode -projectPath … -testPlatform PlayMode -testResults results.xml` ([command line](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html)).

| Godot | Unity |
|---|---|
| scene (`.tscn`), instance | Prefab, prefab instance |
| node type (`Area2D`, `RigidBody2D`…) | GameObject + components (`Collider2D`, `Rigidbody2D`) |
| `Area2D` + `body_entered` | trigger collider + `OnTriggerEnter2D` |
| `get_overlapping_bodies()` | `OnTriggerStay2D`, `Collider2D.IsTouching` |
| `collision_layer` + `collision_mask` per object | one layer per GameObject + Layer Collision Matrix |
| `_process` / `_physics_process` (60 Hz) | `Update` / `FixedUpdate` (50 Hz default) |
| signal, `[connection]` | C# event, UnityEvent |
| group, `call_group` | tag, or a list you keep |
| autoload | `DontDestroyOnLoad` object |
| `godot --headless --script` | `Unity -batchmode -runTests` |

## Doing the same thing in Unreal Engine

*Unreal Engine was not run for this chapter. The comparisons come from Epic's Unreal Engine 5 documentation (5.8 at the time of checking), checked on 27 September 2026. Unreal is source-available under the Unreal Engine End User License Agreement, not open source: "Your access to and use of Unreal Engine on GitHub is governed by the Unreal Engine End User License Agreement" ([source access](https://dev.epicgames.com/documentation/en-us/unreal-engine/downloading-source-code-in-unreal-engine)).*

### Similarities

- **Overlap events fire on entry.** The pickup is a Blueprint Actor with a sphere collision component. Its `OnComponentBeginOverlap` event plays the part of `area_entered`. For the expiry check, [Get Overlapping Actors](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Collision/GetOverlappingActors) plays the part of `get_overlapping_bodies()`. The same question applies, and so does the same answer.
- **Timers and messages.** [Set Timer by Event](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Utilities/Time/SetTimerbyEvent) replaces `ShieldTimer`. [Event Dispatchers](https://dev.epicgames.com/documentation/en-us/unreal-engine/event-dispatchers-in-unreal-engine) are the Blueprint form of signals: you bind events, and a Call fires every bound event.
- **Frame work versus physics.** Actors tick every frame, and [tick groups](https://dev.epicgames.com/documentation/en-us/unreal-engine/actor-ticking-in-unreal-engine) such as `TG_PrePhysics` and `TG_PostPhysics` order that work around the physics step.
- **Something that outlives a level.** A `UGameInstanceSubsystem` is an automatically instanced system that shares "the lifetime of the game instance" ([subsystems](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-subsystems-in-unreal-engine)). That is the closest match to an autoload.

### Differences

- **Collision is a response table, and both sides vote.** "Every object that can collide gets an Object Type and a series of responses", Block, Overlap or Ignore, for every other type ([collision overview](https://dev.epicgames.com/documentation/unreal-engine/collision-in-unreal-engine---overview)). Blocking requires that "they both need to be set to block their respective object types". And "for an overlap to occur, both Actors need to enable Generate Overlap Events." Godot's rule is one-sided: A notices B if B's layer is in A's mask. In Unreal, forgetting Generate Overlap Events on the *creep* would silently disable the shield check.
- **Blueprints are binary.** Assets "are binary, so cannot be opened as text or merged in a text-based merge tool" ([Perforce guide](https://dev.epicgames.com/documentation/unreal-engine/using-perforce-as-source-control-for-unreal-engine?lang=en-US)). Epic ships a separate [diff tool](https://dev.epicgames.com/documentation/en-us/unreal-engine/ue-diff-tool-in-unreal-engine) because "a textual representation would not be constructive". A coding agent can write and diff the **C++** version of this chapter's pickup. It cannot read or review a Blueprint graph the way it read `player.tscn`, so a Blueprint implementation moves more of the review onto you, inside the editor.
- **2D is a plugin.** Unreal's 2D path is the [Paper 2D](https://dev.epicgames.com/documentation/en-us/unreal-engine/paper-2d-overview-in-unreal-engine) plugin: sprites, flipbooks, tile maps. Godot's 2D nodes and 2D physics are part of the engine.
- **Headless tests.** Use the [Automation Test Framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine), or a [Functional Test](https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine) actor placed in a test level. Run it from the command line with `-ExecCmds="Automation RunTest MySet.MySubSet;Quit"` ([running tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine)).

| Godot | Unreal Engine 5 |
|---|---|
| scene, instance | Blueprint class / Actor, placed instance |
| node | Actor or Component |
| `Area2D` + `area_entered` | collision component + `OnComponentBeginOverlap` |
| `collision_layer` / `collision_mask` | Object Type + per-channel Block/Overlap/Ignore, both sides |
| `get_overlapping_bodies()` | Get Overlapping Actors |
| signal | Event Dispatcher / delegate |
| `Timer` node | Set Timer by Event |
| autoload | Game Instance Subsystem |
| `.tscn` text | `.uasset` / `.umap` binary |
| `godot --headless --script` | `-ExecCmds="Automation RunTest …;Quit"` |

---

## Sources

Official documentation first. Godot pages are the `stable` manual, checked on 27 September 2026 against Godot 4.7.2 behaviour on the course Mac.

**Godot**
- [Your first 2D game](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/index.html) and [Coding the player](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/03.coding_the_player.html)
- [Creating instances](https://docs.godotengine.org/en/stable/getting_started/step_by_step/instancing.html)
- [Using SceneTree](https://docs.godotengine.org/en/stable/tutorials/scripting/scene_tree.html) and [SceneTree class](https://docs.godotengine.org/en/stable/classes/class_scenetree.html)
- [TSCN file format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html)
- [Using signals](https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html) and [Object](https://docs.godotengine.org/en/stable/classes/class_object.html) (`CONNECT_DEFERRED`)
- [Groups](https://docs.godotengine.org/en/stable/tutorials/scripting/groups.html)
- [Singletons (Autoload)](https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html)
- [Idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)
- [Physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html), [CollisionObject2D](https://docs.godotengine.org/en/stable/classes/class_collisionobject2d.html), [Area2D](https://docs.godotengine.org/en/stable/classes/class_area2d.html), [RigidBody2D](https://docs.godotengine.org/en/stable/classes/class_rigidbody2d.html), [Using CharacterBody2D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html)
- [Optimization using Servers](https://docs.godotengine.org/en/stable/tutorials/performance/using_servers.html) and [PhysicsServer2D](https://docs.godotengine.org/en/stable/classes/class_physicsserver2d.html)
- [TileMapLayer](https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html)
- [Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html); [Overview of debugging tools](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html) (Visible Collision Shapes)
- Demo source: [godotengine/godot-demo-projects](https://github.com/godotengine/godot-demo-projects) at `a3b5c113112f77291d5f3d1360f33a882fdc52f7`

**Walker records (local, read on 27 September 2026)**
- `walker-2d-dodge-the-creeps/README.md`, `FRICTIONAL.md`, `godot/test_input.gd`, `input-fixed-20260924.log`
- `walker-pong/README.md`, `FRICTIONAL.md`, `tests/input_route.gd`, `evidence/route-1789143192-56772.json` (public: [github.com/nikbearbrown/walker-pong](https://github.com/nikbearbrown/walker-pong))
- `walker-2d-bullet-shower/README.md`, `FRICTIONAL.md`, `godot/bullets.gd`, `godot/test_motion.gd`
- `walker-2d-dynamic-tilemap-layers`, `walker-loading-autoload`, `walker-loading-scene-changer`: `README.md`, `FRICTIONAL.md`, test scripts
- `walker-jumpman-clawd/godot/project.godot`, `game/session.gd`, `FRICTIONAL.md` (public: [github.com/nikbearbrown/walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd))
- `walker-demo-series/queue.json`
- This chapter's run: [`examples/04-scenes-collision-and-physics/`](../examples/04-scenes-collision-and-physics/)

**Unity** (documentation-based; Unity was not run for this chapter; checked 27 September 2026)
- [Prefabs](https://docs.unity3d.com/Manual/Prefabs.html); [Create functional layers](https://docs.unity3d.com/6000.2/Documentation/Manual/create-layers.html); [Layer-based collision detection](https://docs.unity3d.com/Manual/LayerBasedCollision.html)
- [OnTriggerEnter2D](https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnTriggerEnter2D.html), [OnTriggerStay2D](https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnTriggerStay2D.html), [Collider2D.IsTouching](https://docs.unity3d.com/ScriptReference/Collider2D.IsTouching.html), [FixedUpdate](https://docs.unity3d.com/ScriptReference/MonoBehaviour.FixedUpdate.html), [Rigidbody 2D body types](https://docs.unity3d.com/Manual/2d-physics/rigidbody/body-types/rigidbody-2d-body-types-landing.html), [DontDestroyOnLoad](https://docs.unity3d.com/ScriptReference/Object.DontDestroyOnLoad.html)
- [Editor settings: Asset Serialization](https://docs.unity3d.com/Manual/class-EditorManager.html); [Format of text serialized files](https://docs.unity3d.com/Manual/FormatDescription.html)
- Unity Test Framework: [UnityTest attribute](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-attribute-unitytest.html), [command line](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html)

**Unreal Engine** (documentation-based; Unreal was not run for this chapter; checked 27 September 2026)
- [Collision overview](https://dev.epicgames.com/documentation/unreal-engine/collision-in-unreal-engine---overview); [Get Overlapping Actors](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Collision/GetOverlappingActors); [Set Timer by Event](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Utilities/Time/SetTimerbyEvent)
- [Event Dispatchers](https://dev.epicgames.com/documentation/en-us/unreal-engine/event-dispatchers-in-unreal-engine); [Actor ticking](https://dev.epicgames.com/documentation/en-us/unreal-engine/actor-ticking-in-unreal-engine); [Programming subsystems](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-subsystems-in-unreal-engine)
- [Using Perforce as source control](https://dev.epicgames.com/documentation/unreal-engine/using-perforce-as-source-control-for-unreal-engine?lang=en-US); [UE Diff Tool](https://dev.epicgames.com/documentation/en-us/unreal-engine/ue-diff-tool-in-unreal-engine)
- [Paper 2D overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/paper-2d-overview-in-unreal-engine)
- [Automation Test Framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine); [Run automation tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine); [Functional testing](https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine)
- [Downloading source code](https://dev.epicgames.com/documentation/en-us/unreal-engine/downloading-source-code-in-unreal-engine) (Unreal Engine EULA)
