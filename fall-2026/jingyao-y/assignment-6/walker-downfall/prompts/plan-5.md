# Plan 5 — wire Effect B (`fire_pit_flames`) to `FirePit.burn_left`, and its state test

Written before any code edit. Contract: `CLAUDE.md`, `CHANGE-BRIEF.md` "Effect B —
fire_pit_flames" (B1–B7, the feedback mapping) and Revisions r3 (Flames quad 0.55,
already in the scene and config test). Frozen for this task: `effects/*.tscn`
(settings), `shaders/**`, `scripts/run-test.sh`, `effects/hit_spark.gd`, every
existing test. No commit.

## What was checked before planning

- `entities/fire_pit.gd`: `_flames`/`_embers` are `CPUParticles3D` built by
  `_particles()`; `_set_lit(on)` sets their `emitting` and blacks the `Glow` when off;
  `feed()` calls `_set_lit(true)`, `burn()` calls `_set_lit(false)` at 0.
- Writers of `burn_left`: `feed()`, `burn()` (inside `FirePit`) and
  `game/run_save.gd:211-213` (in-run resume writes `burn_left` then calls
  `_set_lit(burn_left > 0)`). So `_set_lit(on: bool)` keeps its signature and also
  refreshes the effect from `burn_left`.
- Callers of `feed()`: `GmFeatures.burn_fuel()` (the fuel picker's row,
  `ui/event_screens.gd:1131-1133`, opened by E → `GameManager._interact()` →
  `_open_fuel()`), the boss arena's first fire (`gm_features.gd:152`) and the rest
  stop's campfire (`gm_route.gd:225`). Both "lit at load" pits are fed right
  *after* `add_child` (so after `_ready`), in the same call that builds the floor.
- Callers of `burn()`: `_tick_features()` (physics, while `simulation_active()`) and
  `Boss._hammer_the_fire()`.
- No existing suite reads `_flames`/`_embers` or the `Flames`/`Embers` children
  (grep over `tests/`); only `previews/fire_pit_flames_preview.gd` does (by name).
- Menus do not pause the tree; `GameManager.simulation_active()` is false while any
  modal except a looting inventory is open (`game_manager.gd:441-442`). Esc with no
  modal opens the "pause" modal (`go_back()` → `toggle_panel("pause")`).

## Step 1 — wiring (presentation only), `entities/fire_pit.gd`

- Remove `_flames`, `_embers` (`CPUParticles3D`) and the `_particles()` builder.
- `const FLAMES_SCENE := preload("res://effects/fire_pit_flames.tscn")`; in `_ready`
  one instance is added as a child named `FirePitFlames` (the scene's root name) at
  the pit's origin (the scene's own emitter offsets 0.2/0.35 stay as set). Its
  `GPUParticles3D` children are kept in `_emitters`. No setting is written.
- One read-only function `_show_fuel()` implements the brief's mapping:
  - `on := burn_left > 0.0`
  - `ratio := 0.3 + 0.7 * clampf(burn_left / 120.0, 0.0, 1.0)` on both emitters
  - `amount_ratio = ratio`; `emitting = on`. On the rising edge (an emitter not
    emitting, `on` true) it calls `restart()` instead of only setting `emitting`
    (restart sets `emitting = true` and clears the buffer so the scene's
    `preprocess` runs again on a relight, B1; the very first lighting of a fresh
    node is preprocessed anyway, TUNING.md r0 frame 11). `amount` is never written.
- Called whenever `burn_left` changes: from `_set_lit()` (so `feed()`, the
  `burn()` that reaches 0, and the run-save resume all go through it) and from
  `burn()` after every decrement (each physics tick and the hammer). Also called
  from `_ready` via `_set_lit(lit())` (was `_set_lit(false)`), so a pit whose
  `burn_left` is already > 0 when it enters the tree starts emitting at the mapped
  ratio (B6). With `burn_left == 0` at `_ready` (every spawn today) it is exactly
  the old behaviour.
- Unchanged: the model, `Glow` halo and its flicker (`_process`), `burn_left`,
  `lit()`, `warms()`, `feed()`/`burn()` arithmetic and guards, `FLAME` const.
  `_show_fuel()` reads `burn_left`, never writes it.

## Step 2 — preview, `previews/fire_pit_flames_preview.gd` (minimal)

After step 1 the pit has its own `FirePitFlames`, so the preview would draw two
fires. Change: drop the hide-CPU-children loop and the second instance; take the
pit's own `FirePitFlames` as `effect` and turn `use_fixed_seed`/`seed` on its
emitters there (preview only; the scene keeps `use_fixed_seed = false`). `_apply()`
no longer writes `emitting`/`amount_ratio` (the pit does it from `burn_left`);
it only prints what the emitters read. The frame schedule (10/55/100) and the
`feed()`/`burn()` calls the fixture already makes stay.

## Step 3 — new state test `tests/test_fire_pit_flames_state.gd` (60 fps)

Real game (`res://game/main.tscn` under the test's SceneTree, as
`test_hit_spark_state.gd`), real loop. Floor: `fixed_map_seed = 2026` **and**
`seed_rng(2026)`, `start_contract("snow")`. Fixture setup (said so in the log):
`_clear_field()` (no enemies interfering), the player teleported beside the chosen
pit, fuel stacks put in the pack (as `test_map_features.gd` does).

Real input: E is a real `InputEventKey` (physical E) through
`Input.parse_input_event` (+ `root.push_input` headless, same reason as the
hit-spark test) → `GameManager._field_keys` → `_interact()` → fuel picker modal;
the picker row is clicked with real left-button press/release events at its
on-screen centre → `Button.pressed` → `burn_fuel()` → `feed()`. Burning is only
the real `_physics_process` → `_tick_features` → `burn()`. The test never calls
`feed()`, `burn()`, `_set_lit()` or `_show_fuel()`.

A monitor on `SceneTree.process_frame` samples **every** frame, for every
`FirePit` in the tree: `burn_left`, both emitters' `emitting`, `amount_ratio`,
`amount`. It counts violations of (a) `emitting == (burn_left > 0)`,
(b) `|amount_ratio − mapping(burn_left)| ≤ 1e-4`, (c) `amount == 24 / 10`, and
records rising (0 → > 0) and falling (> 0 → 0) edges with the sample's state.

| Assertion | Rule |
|---|---|
| plank fed via E + click: `burn_left` 0 → 60 on one sample, both emitting on that same sample; ratio 0.65 | B1, B3 (feed) |
| after ≈10 s of the physics loop: `burn_left` ≈ 50 and ratio = mapping (≈ 0.5917), different from 0.65 | B3 (burn) |
| monitor: no violation of (a)(b)(c) over the whole run, ≥ N distinct ratios seen | B3, `amount` never changes |
| `paused = true` 60 frames: `burn_left`, `emitting`, `amount_ratio` unchanged; both emitters `can_process() == false` | B4 (tree) |
| Esc (real key) opens the "pause" modal, `simulation_active()` false, 60 frames: `burn_left` frozen, ratio/emitting unchanged, emitters `can_process() == true`; Esc closes it | B4 (menu) |
| pit `visible = false`, ≈10 s of loop: ratio keeps following `burn_left` (changed, = mapping); shown again: current ratio | B5 |
| burn to 0 in the loop: on the sample `burn_left` hits 0, both `emitting == false`; 140 frames later still false, `burn_left` 0 | B2 |
| effect root `visible = false`, solid fuel fed via E + click: 0 → 120, emitting true that sample, ratio 1.0; a plank on top → 180, ratio 1.0; shown again | B1 (relight), B3 (≥ 120 clamp), B5 |
| `advance()` onto a 临时休整 (rest) node (next column's nodes set to "rest" as `test_route_map.gd` does): the rest fire's first sampled frame has `burn_left` 300, both emitting, ratio 1.0 | B6 |
| headless observation printed: whether `emitting` on these continuous emitters reads back true while lit | (report) |

B7: every existing suite through `./scripts/run-baseline.sh after-step5 8`,
compared with `logs/baseline-after-step3/summary.txt`.

## Rules that need the user's windowed check

- B1: that the first *drawn* frame of a lighting/relight shows a full fire
  (preprocess; the restart on relight) — headless draws nothing.
- B2: that live flames/embers finish their life instead of vanishing.
- B4: that the flames freeze on screen with the tree paused, and keep moving
  under a menu.
- B5: nothing drawn while hidden; the fire at the current ratio when shown.
- B6: the rest/arena fire looks steady on the floor's first drawn frame.
- B3 visually: thinning with no pop (strip 54 → 70 already recorded once).

## Not driven through real play

- The boss hammer's `burn()` (needs a boss floor); it goes through the same
  `burn()` → `_show_fuel()` line as the physics tick.
- The boss arena's first fire (B6's other case): same `feed()`-after-`add_child`
  path as the rest fire.
- Reaching a rest node: the route map node kinds are set by the test (fixture),
  then the real `advance()` builds the floor.

---

# Implementation record

## Step 1 done — `entities/fire_pit.gd` (checked against B1–B7 and the mapping before editing)

As planned. One addition found while editing: `burn()` now calls `_show_fuel()` after
every decrement that leaves fuel (the ratio must follow each tick), and `_set_lit()` at 0
as before. `_set_lit(on)` keeps its signature for `game/run_save.gd:213`.

```diff
diff --git a/fall-2026/jingyao-y/assignment-6/walker-downfall/entities/fire_pit.gd b/fall-2026/jingyao-y/assignment-6/walker-downfall/entities/fire_pit.gd
index 6bf4684e..52e9ad69 100644
--- a/fall-2026/jingyao-y/assignment-6/walker-downfall/entities/fire_pit.gd
+++ b/fall-2026/jingyao-y/assignment-6/walker-downfall/entities/fire_pit.gd
@@ -13,10 +13,15 @@ const FLAME := Color(1.0, 0.55, 0.18)
 const GLOW := Color(0.95, 0.5, 0.2)
 const GLOW_GAIN := 0.55
 const FLICKER := 7.0
+## The flames and embers (GPU particles; every setting lives in the scene).
+const FLAMES_SCENE := preload("res://effects/fire_pit_flames.tscn")
+## Fuel at or above this shows the full fire; below it the flames thin, down to
+## LOW_RATIO at the last second (CHANGE-BRIEF.md Effect B, feedback mapping).
+const FULL_FIRE := 120.0
+const LOW_RATIO := 0.3
 
 var burn_left := 0.0
-var _flames: CPUParticles3D
-var _embers: CPUParticles3D
+var _emitters: Array[GPUParticles3D] = []
 var _glow: StandardMaterial3D
 var _time := 0.0
 
@@ -34,13 +39,12 @@ func _ready() -> void:
 	_glow = halo.material_override
 	_glow.albedo_color = Color.BLACK
 	add_child(halo)
-	_flames = _particles(18, 0.7, 0.18, Vector2(0.5, 1.1), 0.22, [Color(1.0, 0.85, 0.4, 0.0), Color(1.0, 0.6, 0.2, 0.9), Color(0.8, 0.2, 0.05, 0.0)])
-	_flames.name = "Flames"
-	_flames.position.y = 0.2
-	_embers = _particles(8, 2.2, 0.25, Vector2(0.4, 0.9), 0.05, [Color(1.0, 0.7, 0.3, 0.0), Color(1.0, 0.5, 0.15, 0.9), Color(0.6, 0.15, 0.05, 0.0)])
-	_embers.name = "Embers"
-	_embers.position.y = 0.35
-	_set_lit(false)
+	var flames := FLAMES_SCENE.instantiate()
+	add_child(flames)
+	for child in flames.get_children():
+		if child is GPUParticles3D: _emitters.append(child)
+	# A pit already holding fuel when it enters the tree burns from its first frame.
+	_set_lit(lit())
 
 ## Stones, logs and the charm in plain shapes until the model is in.
 func _placeholder() -> void:
@@ -71,37 +75,6 @@ func _placeholder() -> void:
 		stick.rotation = Vector3(PI / 2.0, TAU * i / 3.0, 0.0)
 		add_child(stick)
 
-func _particles(amount: int, lifetime: float, radius: float, speed: Vector2, size: float, ramp: Array) -> CPUParticles3D:
-	var p := CPUParticles3D.new()
-	p.amount = amount
-	p.lifetime = lifetime
-	p.emission_shape = CPUParticles3D.EMISSION_SHAPE_SPHERE
-	p.emission_sphere_radius = radius
-	p.direction = Vector3.UP
-	p.spread = 15.0
-	p.gravity = Vector3.ZERO
-	p.initial_velocity_min = speed.x
-	p.initial_velocity_max = speed.y
-	var fade := Gradient.new()
-	fade.set_color(0, ramp[0])
-	fade.add_point(0.3, ramp[1])
-	fade.set_color(fade.get_point_count() - 1, ramp[2])
-	p.color_ramp = fade
-	var quad := QuadMesh.new()
-	quad.size = Vector2(size, size)
-	var material := StandardMaterial3D.new()
-	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
-	material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
-	material.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
-	# Fog on an additive quad lights its whole square.
-	material.disable_fog = true
-	material.vertex_color_use_as_albedo = true
-	material.billboard_mode = BaseMaterial3D.BILLBOARD_ENABLED
-	quad.material = material
-	p.mesh = quad
-	add_child(p)
-	return p
-
 func lit() -> bool:
 	return burn_left > 0.0
 
@@ -118,12 +91,24 @@ func burn(delta: float) -> void:
 	if burn_left <= 0.0: return
 	burn_left = maxf(0.0, burn_left - delta)
 	if burn_left <= 0.0: _set_lit(false)
+	else: _show_fuel()
 
 func _set_lit(on: bool) -> void:
-	if _flames != null: _flames.emitting = on
-	if _embers != null: _embers.emitting = on
+	_show_fuel()
 	if _glow != null and not on: _glow.albedo_color = Color.BLACK
 
+## Presentation only, read from burn_left (never written here): the flames burn
+## while there is fuel, and thin below FULL_FIRE. `amount` is never touched (it
+## would restart the buffer); a fire lit from cold restarts so the scene's
+## preprocess shows it full at once.
+func _show_fuel() -> void:
+	var on := burn_left > 0.0
+	var ratio := LOW_RATIO + (1.0 - LOW_RATIO) * clampf(burn_left / FULL_FIRE, 0.0, 1.0)
+	for p in _emitters:
+		p.amount_ratio = ratio
+		if on and not p.emitting: p.restart()
+		elif p.emitting != on: p.emitting = on
+
 func _process(delta: float) -> void:
 	if not lit() or _glow == null: return
 	_time += delta
```

## Step 2 done — `previews/fire_pit_flames_preview.gd`

The preview no longer hides CPU children (there are none) or instances a second
effect: it takes the pit's own `FirePitFlames`, sets `use_fixed_seed`/`seed` on that
pit's emitters only, and `_apply()` only logs what the pit set. Not re-captured.

```diff
diff --git a/fall-2026/jingyao-y/assignment-6/walker-downfall/previews/fire_pit_flames_preview.gd b/fall-2026/jingyao-y/assignment-6/walker-downfall/previews/fire_pit_flames_preview.gd
index d3cc1dee..13ba9507 100644
--- a/fall-2026/jingyao-y/assignment-6/walker-downfall/previews/fire_pit_flames_preview.gd
+++ b/fall-2026/jingyao-y/assignment-6/walker-downfall/previews/fire_pit_flames_preview.gd
@@ -4,19 +4,16 @@ extends Node
 ## starts a real 萨米 (`snow`) contract with a fixed map seed, freezes the
 ## simulation with the "capture" modal, picks the floor's first real FirePit,
 ## puts the player a few units from it, centres the camera on the pit at the
-## game's default size (24) and pitch, and instances
-## res://effects/fire_pit_flames.tscn at the pit's global_position under the
-## GameManager. The FirePitFlames instance made here is the only one with
-## use_fixed_seed on.
+## game's default size (24) and pitch, and captures the pit's own
+## res://effects/fire_pit_flames.tscn instance (FirePit makes it). That pit's
+## emitters are the only ones with use_fixed_seed on.
 ##
-## Gameplay is not wired yet (FirePit still makes its own CPU "Flames"/"Embers"),
-## so this fixture plays the condition itself, by the brief's feedback mapping:
+## The pit applies the brief's feedback mapping itself (FirePit._show_fuel):
 ##   emitting     = burn_left > 0
 ##   amount_ratio = 0.3 + 0.7 * clamp(burn_left / 120.0, 0, 1)
-## It changes the real pit's burn_left through FirePit.feed()/burn() (so the
-## pit's Glow halo follows) and hides the pit's own CPU particle children so
-## only the GPU effect is drawn. Frames: 10 feed 120 s (ratio 1.0), 55 burn to
-## 24 s (ratio 0.44), 100 burn to 0 (out).
+## This fixture changes the real pit's burn_left through FirePit.feed()/burn()
+## (so the flames and the Glow halo follow). Frames: 10 feed 120 s (ratio 1.0),
+## 55 burn to 24 s (ratio 0.44), 100 burn to 0 (out).
 ##
 ## Frame count: `frame` is 0 on this script's first _process and goes up by one
 ## per processed frame. PREVIEW_LOADED says on which frame the level was ready.
@@ -25,8 +22,6 @@ extends Node
 ##   godot --path . res://previews/fire_pit_flames_preview.tscn
 ##     --write-movie <abs>/captures/fire_pit_flames/r0/frame.png --fixed-fps 30 --quit-after 180
 
-const FLAMES := preload("res://effects/fire_pit_flames.tscn")
-
 @export var map_seed := 2026
 @export var particle_seed := 7370
 ## preview frame -> burn_left the pit is set to on that frame.
@@ -80,19 +75,14 @@ func _load_level() -> void:
 	if pit == null:
 		print("PREVIEW_ERROR no FirePit on this floor (region %s seed %d)" % [game.region_id, map_seed])
 		return
-	# The pit's own CPU particles stay off screen; the GPU effect is what is captured.
-	for child_name in ["Flames", "Embers"]:
-		var cpu := pit.get_node_or_null(NodePath(child_name)) as Node3D
-		if cpu != null: cpu.visible = false
 	game.player.teleport(game.world_map.nearest_walkable(pit.global_position + Vector3(2.5, 0.0, 0.0)))
-	effect = FLAMES.instantiate() as Node3D
-	effect.name = "FirePitFlames"
+	# The pit's own FirePitFlames (entities/fire_pit.gd) is the one captured; the fixed
+	# seed is turned on for this preview's pit only.
+	effect = pit.get_node("FirePitFlames") as Node3D
 	for child in effect.get_children():
 		if child is GPUParticles3D:
 			child.use_fixed_seed = true
 			child.seed = particle_seed
-	game.add_child(effect)
-	effect.global_position = pit.global_position
 	game._hud.hide()
 	game.camera_size_goal = GameManager.CAMERA_SIZE
 	game.camera.size = GameManager.CAMERA_SIZE
@@ -104,15 +94,10 @@ func _place_camera() -> void:
 	if is_instance_valid(pit):
 		game.camera.global_position = pit.global_position + game.camera_offset()
 
-## The brief's feedback mapping, played by the fixture from the pit's real burn_left.
+## The pit itself applies the feedback mapping from burn_left; this only logs it.
 func _apply() -> void:
-	var burn_left := pit.burn_left
-	var ratio := 0.3 + 0.7 * clampf(burn_left / 120.0, 0.0, 1.0)
-	for child in effect.get_children():
-		if child is GPUParticles3D:
-			child.amount_ratio = ratio
-			child.emitting = burn_left > 0.0
-	print("PREVIEW_SET preview_frame %d engine_frame %d burn_left %.1f emitting %s amount_ratio %.4f" % [frame, Engine.get_process_frames(), burn_left, burn_left > 0.0, ratio])
+	var flames := effect.get_node("Flames") as GPUParticles3D
+	print("PREVIEW_SET preview_frame %d engine_frame %d burn_left %.1f emitting %s amount_ratio %.4f" % [frame, Engine.get_process_frames(), pit.burn_left, flames.emitting, flames.amount_ratio])
 
 func _process(_delta: float) -> void:
 	frame += 1
```

## Step 3 done — `tests/test_fire_pit_flames_state.gd` (new file, no diff base)

As planned. Found while running: the headless display server never flushes the
`Input` event buffer, so the first run's E and Esc did nothing (18 failures, real
output in the report). The test's `send()` now calls `Input.flush_buffered_events()`
right after `Input.parse_input_event()`, as a windowed DisplayServer does each frame.
Second run: 0 failures (`logs/test_fire_pit_flames_state_60fps.log`).

## Step 4 — existing suites (B7)

`./scripts/run-baseline.sh after-step5 8` → **82 of 93 pass** (`logs/baseline-after-step5/summary.txt`)
against after-step3's 80 of 91. Two suites are new and both pass: `test_fire_pit_flames_config`
and `test_fire_pit_flames_state`. Changes from after-step3: `test_elevation` FAIL → PASS (known
load-sensitive); `test_arenas` PASS → FAIL, with 3 血债 (debt) values (5.5 where 5 was
expected), no fire check involved. Run alone (`./scripts/run-test.sh test_arenas.gd 60 1200`) it gives
85 checks, 0 failures. The other 10 failures are the known pre-existing ones.
`test_map_features` passed in the baseline; one earlier standalone run had 6 non-fire failures
(shower and 血债 checks in the mine and 叙拉古 sections), and two reruns gave 0 failures.
