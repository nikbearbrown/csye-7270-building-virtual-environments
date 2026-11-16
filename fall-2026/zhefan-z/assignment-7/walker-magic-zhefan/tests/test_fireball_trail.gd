extends SceneTree
## Assignment 6 headless state test for Effect B, the fireball trail (CHANGE-BRIEF rules B1-B5): emitting from the
## fireball's first frame; on an impact or the 2.0 s timeout moved to the fireball's former parent, still in the tree,
## no longer emitting and freed about 0.3 s later; unchanged and not processing while the tree is paused; still
## emitting while hidden; none before a cast or on scene load.
## From fall-2026/zhefan-z/assignment-6/, at 30, 60 and 144 fps:
##   ./scripts/run-test.sh test_fireball_trail.gd 30
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.
## Driven through the real game loop: every cast is a real mouse event (motion to the aim point, then a left click),
## every pause a real Esc key event, and fireballs fly, collide and time out through physics. Nothing here calls
## cast(), explode(), _release_trail() or toggle_pause(), or sets `emitting`. The only thing the test sets on a trail is
## `visible`, for B4. Aliveness is instance presence in the tree, never `emitting`.
## Headless runs no GPU particle process and draws nothing: what is drawn (B4 "nothing drawn", the freeze on screen,
## the fade where the trail stopped) is a check in the running game, not here.

const TRAIL_SCENE := "res://effects/fireball_trail.tscn"
const GROUND_TOP := 327.0
const TRAIL_FADE := 0.3        # CHANGE-BRIEF B2 / fireball_trail.tscn lifetime
const FIREBALL_LIFE := 2.0     # features/fireball/fireball.gd LIFETIME
const SPEED := 260.0           # features/fireball/fireball.gd SPEED
const PHYSICS_STEP := 1.0 / 60.0   # physics rate is not set in project.godot
const EPS := 0.01


## Game time: the sum of process deltas while the tree runs (pausable, like the trail's free timer).
class Clock extends Node:
	var t := 0.0

	func _init(always := false) -> void:
		process_priority = -1000
		if always:
			process_mode = Node.PROCESS_MODE_ALWAYS

	func _process(delta: float) -> void:
		t += delta


var main: Node
var player: Player
var clock: Clock     # game time, stops while paused
var wall: Clock      # wall time, runs while paused
var results: Array[Dictionary] = []
var failures := 0
var casts := 0
var fireballs: Array[Dictionary] = []   # {id, node, trail, t_in, t_out, hits, first, release_pos, release_rot}
var trails: Array[Dictionary] = []      # detached trails: {node, fireball, t_in, w_in, t_out, w_out, pos, rot, emitting_next}
var ledger: Array[Dictionary] = []


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


func steps(n: int) -> void:
	for i in n:
		await physics_frame


func frames(n: int) -> void:
	for i in n:
		await process_frame


func wait_s(seconds: float) -> void:
	var end := clock.t + seconds
	while clock.t < end - 1e-6:
		await process_frame


func wait_wall(seconds: float) -> void:
	var end := wall.t + seconds
	while wall.t < end - 1e-6:
		await process_frame


func wait_until(cond: Callable, max_wall_s: float) -> void:
	var end := wall.t + max_wall_s
	while not cond.call() and wall.t < end:
		await process_frame


func alive_trails() -> Array:
	return trails.filter(func(r: Dictionary) -> bool: return r.t_out < 0.0)


## A case is over when every fireball has ended and every trail it left has been freed.
func case_done() -> bool:
	return fireballs.all(func(f: Dictionary) -> bool: return f.t_out >= 0.0) and alive_trails().is_empty() \
		and trails.size() >= fireballs.size()


func trails_under_main() -> int:
	return main.find_children("*", "GPUParticles2D", true, false).filter(
		func(n: Node) -> bool: return n.scene_file_path == TRAIL_SCENE).size()


func _on_child(node: Node) -> void:
	if node.scene_file_path == TRAIL_SCENE:
		var rec := {"node": node, "fireball": 0, "t_in": clock.t, "w_in": wall.t, "t_out": -1.0, "w_out": -1.0,
			"pos": Vector2.INF, "rot": 0.0, "emitting_next": null}
		for fb: Dictionary in fireballs:
			if fb.trail == node:
				rec.fireball = fb.id
		trails.append(rec)
		# reparent(keep_global) restores the global transform after add_child, and fireball.gd sets emitting = false after
		# the move: read all three once the frame's callbacks are done.
		process_frame.connect(func() -> void:
			if is_instance_valid(node):
				rec.pos = (node as Node2D).global_position
				rec.rot = (node as Node2D).global_rotation
				rec.emitting_next = (node as GPUParticles2D).emitting, CONNECT_ONE_SHOT)
		node.tree_exited.connect(func() -> void:
			rec.t_out = clock.t
			rec.w_out = wall.t)
	elif node is Fireball:
		var fb := {"id": node.get_instance_id(), "node": node, "trail": node.get_node_or_null("FireballTrail"),
			"t_in": clock.t, "t_out": -1.0, "hits": [], "first": {}, "release_pos": Vector2.INF, "release_rot": 0.0}
		fireballs.append(fb)
		# The fireball's ready signal: its _ready has run (rotation set) and its children are in the tree. B1.
		node.ready.connect(func() -> void:
			var tr := fb.trail as GPUParticles2D
			fb.first = {"has_trail": tr != null, "in_tree": tr != null and tr.is_inside_tree(),
				"parent_is_fireball": tr != null and tr.get_parent() == node, "emitting": tr != null and tr.emitting,
				"at_fireball": tr != null and tr.global_position.distance_to((node as Node2D).global_position) < EPS})
		node.body_entered.connect(func(body: Node2D) -> void:
			fb.hits.append({"pos": (node as Node2D).global_position, "rot": (node as Node2D).global_rotation, "t": clock.t}))
		# Where the fireball is when its trail leaves it (independent of where the trail says it is).
		node.child_exiting_tree.connect(func(child: Node) -> void:
			if child == fb.trail:
				fb.release_pos = (node as Node2D).global_position
				fb.release_rot = (node as Node2D).global_rotation)
		node.tree_exited.connect(func() -> void: fb.t_out = clock.t)


func fresh(x: float) -> void:
	if is_instance_valid(main):
		if paused:
			await esc()
		await wait_until(case_done, FIREBALL_LIFE + 1.0)
		close_case()
		main.queue_free()
		await process_frame
	fireballs = []
	trails = []
	casts = 0
	main = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	main.child_entered_tree.connect(_on_child)
	root.add_child(main)
	player = main.player
	player.use_scripted = false
	player.global_position = Vector2(x, GROUND_TOP)
	player.cast_fired.connect(func(_o: Vector2, _d: Vector2) -> void: casts += 1)
	await steps(10)


func close_case() -> void:
	for fb: Dictionary in fireballs:
		var mine := trails.filter(func(r: Dictionary) -> bool: return r.fireball == fb.id)
		ledger.append({"fireball_ended": fb.t_out >= 0.0, "detached": mine.size(),
			"freed": mine.all(func(r: Dictionary) -> bool: return r.t_out >= 0.0 and not is_instance_valid(r.node))})
	for r: Dictionary in trails:
		if r.fireball == 0:
			ledger.append({"unattributed": true})


## Real input: the mouse moves to the aim point (world -> screen through the camera), then a left click.
func move_mouse(world: Vector2) -> Vector2:
	var screen := world - Vector2(main.camera.get_screen_center_position().x - 320.0, 0.0)
	var motion := InputEventMouseMotion.new()
	motion.position = screen
	motion.global_position = screen
	Input.parse_input_event(motion)
	return screen


func mouse_button(screen: Vector2, pressed: bool) -> void:
	var ev := InputEventMouseButton.new()
	ev.button_index = MOUSE_BUTTON_LEFT
	ev.pressed = pressed
	ev.position = screen
	ev.global_position = screen
	Input.parse_input_event(ev)


func click_at(world: Vector2) -> void:
	var screen := move_mouse(world)
	mouse_button(screen, true)
	await steps(2)
	mouse_button(screen, false)
	await steps(1)


## Real Esc: pressed and released, then a few frames for SessionInput to forward it to Main.toggle_pause().
func esc() -> void:
	for pressed: bool in [true, false]:
		var ev := InputEventKey.new()
		ev.keycode = KEY_ESCAPE
		ev.physical_keycode = KEY_ESCAPE
		ev.pressed = pressed
		Input.parse_input_event(ev)
	await frames(3)


func trail_of(fb: Dictionary) -> Dictionary:
	for r: Dictionary in trails:
		if r.fireball == fb.id:
			return r
	return {}


func life_tol() -> float:
	return root.get_process_delta_time() + PHYSICS_STEP + 1e-4


## B2 for one ended fireball, called 0.2 s after the trail was detached: on the frame it moved into Main it was at the
## fireball's position and rotation and not emitting, and it is still in the tree as a child of Main.
func check_detached(case: String, fb: Dictionary, end_pos: Vector2, end_rot: float) -> void:
	var tr := trail_of(fb)
	check("B2-%s-trail-moved-to-main-at-fireball-not-emitting" % case, not tr.is_empty()
		and tr.pos.distance_to(end_pos) < EPS and absf(angle_difference(tr.rot, end_rot)) < EPS and tr.emitting_next == false,
		{"detached": not tr.is_empty(), "trail_pos": tr.get("pos"), "fireball_pos": end_pos, "trail_rot": tr.get("rot"),
		"fireball_rot": end_rot, "emitting_next_frame": tr.get("emitting_next")})
	var in_tree: bool = not tr.is_empty() and is_instance_valid(tr.node) and tr.node.is_inside_tree()
	var parent_main: bool = in_tree and tr.node.get_parent() == main
	check("B2-%s-trail-in-tree-under-main-0.2s-later" % case, in_tree and parent_main,
		{"in_tree": in_tree, "parent_is_main": parent_main, "game_s_since_detach": snappedf(clock.t - tr.get("t_in", 0.0), 0.001)})


func check_freed(case: String, fb: Dictionary) -> void:
	await wait_until(func() -> bool: return not trail_of(fb).is_empty() and trail_of(fb).t_out >= 0.0, 1.0)
	await process_frame
	var tr := trail_of(fb)
	var life: float = tr.t_out - tr.t_in if not tr.is_empty() and tr.t_out >= 0.0 else -1.0
	check("B2-%s-trail-freed-0.3s-after-detach" % case, life >= 0.0 and absf(life - TRAIL_FADE) <= life_tol()
		and not is_instance_valid(tr.node), {"life_s": snappedf(life, 0.0001), "tolerance_s": snappedf(life_tol(), 0.0001),
		"instance_valid_after": is_instance_valid(tr.get("node"))})


func run() -> void:
	clock = Clock.new()
	wall = Clock.new(true)
	root.add_child(clock)
	root.add_child(wall)

	# Scene load, then idle: no trail anywhere under Main (B5).
	await fresh(200)
	await wait_s(1.0)
	check("B5-no-trail-on-scene-load-or-before-cast", trails_under_main() == 0 and trails.is_empty()
		and fireballs.is_empty() and casts == 0, {"trails_under_main": trails_under_main(), "casts": casts})

	# Into the ground (B1, B2 impact).
	await fresh(200)
	await click_at(Vector2(300, 340))
	var fb: Dictionary = fireballs[0] if fireballs.size() > 0 else {"first": {}, "id": 0, "t_out": -1.0}
	check("B1-trail-emitting-from-fireballs-first-frame", casts == 1 and fireballs.size() == 1
		and fb.first.get("has_trail", false) and fb.first.get("in_tree", false) and fb.first.get("parent_is_fireball", false)
		and fb.first.get("emitting", false) and fb.first.get("at_fireball", false), {"casts": casts, "first_frame": fb.first})
	await wait_until(func() -> bool: return not trail_of(fb).is_empty(), 1.0)
	await process_frame
	var tr := trail_of(fb)
	await wait_s(0.2)
	var hit: Dictionary = fb.hits[0] if fb.hits.size() > 0 else {"pos": Vector2.INF, "rot": 0.0}
	check_detached("impact", fb, hit.pos, hit.rot)
	await check_freed("impact", fb)

	# Leftward into the left level wall (B2 wall; the emitter's rotation for the direction question).
	await fresh(150)
	await click_at(Vector2(0, 267))
	await wait_until(func() -> bool: return fireballs.size() == 1 and not trail_of(fireballs[0]).is_empty(), 1.5)
	await process_frame
	fb = fireballs[0] if fireballs.size() > 0 else {"id": 0, "hits": [], "t_out": -1.0}
	tr = trail_of(fb)
	await wait_s(0.2)
	hit = fb.hits[0] if fb.hits.size() > 0 else {"pos": Vector2.INF, "rot": 0.0}
	check_detached("wall", fb, hit.pos, hit.rot)
	var trail_pm := (load(TRAIL_SCENE) as PackedScene).instantiate() as GPUParticles2D
	var dir: Vector3 = (trail_pm.process_material as ParticleProcessMaterial).direction
	trail_pm.free()
	var rot: float = tr.get("rot", 0.0)
	# Observation for the direction question: the emitter itself is rotated to the flight direction; what the GPU does
	# with `direction` under that rotation is not observable headless (probe_trail_direction.gd, windowed).
	check("direction-leftward-trail-emitter-rotated-material-direction-unchanged", not tr.is_empty() and cos(rot) < -0.99
		and dir.is_equal_approx(Vector3(-1, 0, 0)), {"trail_global_rotation": snappedf(rot, 0.0001),
		"material_direction": dir, "world_direction_if_rotated": Vector2(dir.x, dir.y).rotated(rot).snappedf(0.001)})
	await check_freed("wall", fb)

	# Straight up into open air: the fireball times out after 2.0 s with no hit (B2 timeout).
	await fresh(200)
	await click_at(Vector2(211, 20))
	await wait_until(func() -> bool: return fireballs.size() == 1 and fireballs[0].t_out >= 0.0, FIREBALL_LIFE + 0.5)
	await process_frame
	fb = fireballs[0] if fireballs.size() > 0 else {"id": 0, "hits": [], "t_in": 0.0, "t_out": -1.0, "release_pos": Vector2.INF, "release_rot": 0.0}
	var timed_out: bool = fb.hits.is_empty() and fb.t_out - fb.t_in > FIREBALL_LIFE - 0.1
	await wait_s(0.2)
	check_detached("timeout", fb, fb.release_pos, fb.release_rot)
	check("B2-timeout-was-a-timeout", timed_out, {"hits": fb.hits.size(), "fireball_life_s": snappedf(fb.t_out - fb.t_in, 0.001)})
	await check_freed("timeout", fb)

	# Real Esc mid-flight: frozen while paused, flying and emitting again after (B3).
	await fresh(200)
	await click_at(Vector2(211, 20))
	await wait_s(0.3)
	fb = fireballs[0] if fireballs.size() > 0 else {"node": null, "trail": null}
	var node := fb.node as Node2D
	var trail := fb.trail as GPUParticles2D
	await esc()
	var p0 := node.global_position if is_instance_valid(node) else Vector2.INF
	var e0 := trail.emitting if is_instance_valid(trail) else false
	await wait_wall(0.5)
	var during := {"paused": paused, "fireball_moved_px": snappedf(node.global_position.distance_to(p0), 0.001)
		if is_instance_valid(node) else -1.0, "emitting_before": e0, "emitting_during": trail.emitting if is_instance_valid(trail) else null,
		"trail_can_process": trail.can_process() if is_instance_valid(trail) else null,
		"trail_parent_is_fireball": is_instance_valid(trail) and trail.get_parent() == node}
	check("B3-paused-trail-unchanged-and-not-processing", paused and during.fireball_moved_px == 0.0 and e0
		and during.emitting_during == true and during.trail_can_process == false and during.trail_parent_is_fireball, during)
	await esc()
	var p1 := node.global_position if is_instance_valid(node) else Vector2.INF
	await steps(10)
	var after := {"paused": paused, "fireball_moved_px": snappedf(node.global_position.distance_to(p1), 0.001)
		if is_instance_valid(node) else -1.0, "emitting": trail.emitting if is_instance_valid(trail) else null,
		"trail_can_process": trail.can_process() if is_instance_valid(trail) else null}
	check("B3-resumed-trail-emitting-and-processing", not paused and after.fireball_moved_px > 30.0
		and after.emitting == true and after.trail_can_process == true, after)

	# Real Esc right after an impact, held longer than the fade: the detached trail waits, then is freed 0.3 s of
	# game time after it was detached (B2 + B3).
	await fresh(200)
	await click_at(Vector2(300, 340))
	await wait_until(func() -> bool: return fireballs.size() == 1 and not trail_of(fireballs[0]).is_empty(), 1.0)
	fb = fireballs[0] if fireballs.size() > 0 else {"id": 0}
	await esc()
	await wait_wall(0.6)
	tr = trail_of(fb)
	var held := {"paused": paused, "in_tree": not tr.is_empty() and is_instance_valid(tr.node) and tr.node.is_inside_tree(),
		"parent_is_main": not tr.is_empty() and is_instance_valid(tr.node) and tr.node.get_parent() == main,
		"emitting": tr.node.emitting if not tr.is_empty() and is_instance_valid(tr.node) else null,
		"wall_s_since_detach": snappedf(wall.t - tr.get("w_in", 0.0), 0.001)}
	check("B2-B3-paused-detached-trail-held-past-its-fade", paused and held.in_tree and held.parent_is_main
		and held.emitting == false and held.wall_s_since_detach > TRAIL_FADE, held)
	await esc()
	await wait_until(func() -> bool: return trail_of(fb).get("t_out", -1.0) >= 0.0, 1.0)
	await process_frame
	tr = trail_of(fb)
	var game_life: float = tr.t_out - tr.t_in if tr.get("t_out", -1.0) >= 0.0 else -1.0
	var wall_life: float = tr.w_out - tr.w_in if tr.get("w_out", -1.0) >= 0.0 else -1.0
	check("B2-B3-freed-0.3s-of-game-time-after-detach", absf(game_life - TRAIL_FADE) <= life_tol() and wall_life > 0.6
		and not is_instance_valid(tr.get("node")), {"game_life_s": snappedf(game_life, 0.0001),
		"wall_life_s": snappedf(wall_life, 0.0001), "tolerance_s": snappedf(life_tol(), 0.0001)})

	# Hidden mid-flight: still emitting and processing, the fireball flies on (B4, node state only).
	await fresh(200)
	await click_at(Vector2(211, 20))
	await wait_s(0.2)
	fb = fireballs[0] if fireballs.size() > 0 else {"node": null, "trail": null}
	node = fb.node as Node2D
	trail = fb.trail as GPUParticles2D
	trail.visible = false
	var p_h := node.global_position
	await steps(18)
	var hidden := {"visible_in_tree": trail.is_visible_in_tree(), "emitting": trail.emitting,
		"can_process": trail.can_process(), "parent_is_fireball": trail.get_parent() == node,
		"fireball_moved_px": snappedf(node.global_position.distance_to(p_h), 0.01), "expected_px": snappedf(SPEED * 18 * PHYSICS_STEP, 0.01)}
	check("B4-hidden-trail-still-emitting-and-processing", not hidden.visible_in_tree and hidden.emitting
		and hidden.can_process and hidden.parent_is_fireball
		and absf(hidden.fireball_moved_px - hidden.expected_px) <= SPEED * PHYSICS_STEP + 0.01, hidden)
	trail.visible = true
	await steps(2)
	check("B4-shown-again-still-emitting", trail.is_visible_in_tree() and trail.emitting,
		{"visible_in_tree": trail.is_visible_in_tree(), "emitting": trail.emitting})

	await wait_until(case_done, FIREBALL_LIFE + 1.0)
	close_case()

	# Across every case: each ended fireball's trail was detached exactly once and freed; none unattributed (B2, B5).
	var per_fb := ledger.filter(func(e: Dictionary) -> bool: return e.has("detached"))
	var wrong := per_fb.filter(func(e: Dictionary) -> bool: return not e.fireball_ended or e.detached != 1 or not e.freed)
	var stray := ledger.filter(func(e: Dictionary) -> bool: return e.get("unattributed", false)).size()
	check("B2-B5-every-trail-detached-once-and-freed", not per_fb.is_empty() and wrong.is_empty() and stray == 0,
		{"fireballs": per_fb.size(), "wrong": wrong, "unattributed_trails": stray})

	main.queue_free()
	clock.queue_free()
	wall.queue_free()
	await process_frame
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)
