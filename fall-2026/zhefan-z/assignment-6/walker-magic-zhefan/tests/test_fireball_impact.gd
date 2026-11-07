extends SceneTree
## Assignment 6 headless state test for Effect A, the fireball impact (CHANGE-BRIEF rules A1-A6 and the revisions of
## 2026-11-05): one impact per explode() on the ground, a wall and the wolf, never on scene load, on a cast, on a
## timeout or twice for one fireball; at the fireball's position; overlapping; a child of Main; freed after 0.9 s.
## From fall-2026/zhefan-z/assignment-6/, at 30, 60 and 144 fps:
##   ./scripts/run-test.sh test_fireball_impact.gd 30
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.
## Driven through the real game loop: every cast is a real mouse event (Input.parse_input_event: motion to the aim
## point, then a left click), and fireballs fly and collide through physics. Nothing here calls cast(), explode() or
## take_damage(). Aliveness is instance presence in the tree, never `emitting` (CHANGE-BRIEF revision 2026-11-05).

const IMPACT_SCENE := "res://effects/fireball_impact.tscn"
const GROUND_TOP := 327.0
const IMPACT_LIFE := 0.9       # CHANGE-BRIEF A6
const WOLF_DOWN := 0.6         # features/wolf/wolf.gd DOWN_TIME
const COOLDOWN := 0.35         # features/player/tuning.gd CAST_COOLDOWN
const PHYSICS_STEP := 1.0 / 60.0   # physics rate is not set in project.godot
const EPS := 0.01


## Game time: the sum of process deltas, read when impacts and fireballs enter and leave the tree.
class Clock extends Node:
	var t := 0.0

	func _init() -> void:
		process_priority = -1000

	func _process(delta: float) -> void:
		t += delta


var main: Node
var player: Player
var clock: Clock
var results: Array[Dictionary] = []
var failures := 0
var casts := 0
var impacts: Array[Dictionary] = []     # {node, pos, t_in, t_out, fireball, alive_at_entry}
var fireballs: Array[Dictionary] = []   # {id, t_in, t_out, hits: [{pos, t, wolf}]}
var ledger: Array[Dictionary] = []      # closed cases: per-fireball hits and impacts, every impact's life
var max_alive := 0
var _hitting := 0                       # instance id of the fireball whose body_entered is being handled


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


func wait_s(seconds: float) -> void:
	var end := clock.t + seconds
	while clock.t < end - 1e-6:
		await process_frame


func wait_until(cond: Callable, max_s: float) -> void:
	var end := clock.t + max_s
	while not cond.call() and clock.t < end:
		await process_frame


func alive() -> Array:
	return impacts.filter(func(r: Dictionary) -> bool: return r.t_out < 0.0)


func _on_child(node: Node) -> void:
	if node.scene_file_path == IMPACT_SCENE:
		var rec := {"node": node, "pos": (node as Node2D).global_position, "t_in": clock.t, "t_out": -1.0,
			"fireball": _hitting, "parent_is_main": node.get_parent() == main, "alive_at_entry": alive().size()}
		_hitting = 0
		impacts.append(rec)
		max_alive = maxi(max_alive, alive().size())
		node.tree_exited.connect(func() -> void: rec.t_out = clock.t)
	elif node is Fireball:
		var fb := {"id": node.get_instance_id(), "t_in": clock.t, "t_out": -1.0, "hits": []}
		fireballs.append(fb)
		# Connected before Fireball._ready connects its own handler, so this runs first: the position read here is
		# the one explode() uses.
		node.body_entered.connect(func(body: Node2D) -> void:
			_hitting = fb.id
			fb.hits.append({"pos": (node as Node2D).global_position, "t": clock.t, "wolf": body is Wolf}))
		node.tree_exited.connect(func() -> void: fb.t_out = clock.t)


func fresh(x: float) -> void:
	if is_instance_valid(main):
		await wait_until(func() -> bool: return alive().is_empty(), IMPACT_LIFE + 0.3)
		close_case()
		main.queue_free()
		await process_frame
	impacts = []
	fireballs = []
	casts = 0
	max_alive = 0
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
		ledger.append({"hits": fb.hits.size(),
			"impacts": impacts.filter(func(r: Dictionary) -> bool: return r.fireball == fb.id).size()})
	for r: Dictionary in impacts:
		ledger.append({"life": r.t_out - r.t_in if r.t_out >= 0.0 else -1.0, "unattributed": r.fireball == 0})


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


func impact_of(fb: Dictionary) -> Dictionary:
	for r: Dictionary in impacts:
		if r.fireball == fb.id:
			return r
	return {}


func run() -> void:
	clock = Clock.new()
	root.add_child(clock)

	# Scene load, then idle: no impact (A2).
	await fresh(200)
	await wait_s(1.0)
	check("A2-no-impact-on-scene-load", impacts.is_empty() and casts == 0, {"impacts": impacts.size(), "casts": casts})

	# Into the ground (A1, A2 cast, A3, A5).
	await fresh(200)
	await click_at(Vector2(300, 340))
	check("A2-no-impact-on-cast", casts == 1 and fireballs.size() == 1 and impacts.is_empty(),
		{"casts": casts, "fireballs": fireballs.size(), "impacts_right_after_cast": impacts.size()})
	await wait_until(func() -> bool: return fireballs.size() == 1 and fireballs[0].t_out >= 0.0, 1.0)
	await process_frame
	var fb: Dictionary = fireballs[0]
	var imp := impact_of(fb)
	check("A1-ground-one-impact", fb.hits.size() >= 1 and impacts.size() == 1 and not imp.is_empty(),
		{"hits": fb.hits.size(), "impacts": impacts.size()})
	var hit_pos: Vector2 = fb.hits[0].pos if fb.hits.size() > 0 else Vector2.INF
	check("A3-ground-impact-at-fireball-position", not imp.is_empty() and imp.pos.distance_to(hit_pos) < EPS,
		{"impact": imp.get("pos"), "fireball_at_hit": hit_pos})
	check("A5-impact-child-of-main-outlives-fireball", not imp.is_empty() and imp.parent_is_main
		and is_instance_valid(imp.node) and imp.node.is_inside_tree() and imp.t_out < 0.0,
		{"parent_is_main": imp.get("parent_is_main"), "fireball_freed_at": fb.t_out,
		"impact_in_tree_after": is_instance_valid(imp.get("node")) and imp.node.is_inside_tree()})

	# Into the right-hand level wall (A1, A3).
	await fresh(1150)
	await click_at(Vector2(1270, 267))
	await wait_until(func() -> bool: return fireballs.size() == 1 and fireballs[0].t_out >= 0.0, 1.0)
	fb = fireballs[0]
	imp = impact_of(fb)
	hit_pos = fb.hits[0].pos if fb.hits.size() > 0 else Vector2.INF
	check("A1-wall-one-impact", casts == 1 and impacts.size() == 1 and not imp.is_empty(),
		{"casts": casts, "hits": fb.hits.size(), "impacts": impacts.size(), "hit_x": hit_pos.x})
	check("A3-wall-impact-at-fireball-position", not imp.is_empty() and imp.pos.distance_to(hit_pos) < EPS,
		{"impact": imp.get("pos"), "fireball_at_hit": hit_pos})

	# Into the wolf until it is defeated, leading the patrolling target (A1 wolf, A5).
	await fresh(620)
	var wolf: Wolf = main.get_node("Level/Wolf")
	var wolf_out := {"t": -1.0, "impact_alive": false}
	wolf.tree_exited.connect(func() -> void:
		wolf_out.t = clock.t
		var last := impacts.filter(func(r: Dictionary) -> bool: return r.fireball != 0)
		wolf_out.impact_alive = not last.is_empty() and last.back().t_out < 0.0 and is_instance_valid(last.back().node))
	var tries := 0
	while not wolf.dead and tries < 8:
		var centre := wolf.global_position + Vector2(8, -14)
		var flight := centre.distance_to(player.global_position + Vector2(Player.STAFF_TIP.x, Player.STAFF_TIP.y)) / Fireball.SPEED
		await click_at(centre + wolf.velocity * flight)
		await wait_until(func() -> bool: return fireballs.size() > tries and fireballs[tries].t_out >= 0.0, 1.5)
		tries += 1
		await wait_s(COOLDOWN)
	var wolf_hits := fireballs.filter(func(f: Dictionary) -> bool: return f.hits.any(func(h: Dictionary) -> bool: return h.wolf))
	var wolf_impacts := wolf_hits.filter(func(f: Dictionary) -> bool: return not impact_of(f).is_empty())
	check("A1-wolf-one-impact-per-hit", wolf.dead and wolf_hits.size() == 2 and wolf_impacts.size() == 2,
		{"casts": casts, "wolf_dead": wolf.dead, "fireballs_hitting_wolf": wolf_hits.size(), "their_impacts": wolf_impacts.size()})
	var t_kill: float = wolf_hits.back().hits[0].t if wolf_hits.size() > 0 else -1.0
	await wait_until(func() -> bool: return wolf_out.t >= 0.0, WOLF_DOWN + 0.5)
	check("A5-impact-outlives-freed-wolf", wolf_out.t >= 0.0 and wolf_out.impact_alive,
		{"wolf_freed_after_s": snappedf(wolf_out.t - t_kill, 0.001), "last_impact_in_tree_then": wolf_out.impact_alive})

	# Straight up into open air: the fireball times out after 2.0 s with no impact (A2).
	await fresh(200)
	await click_at(Vector2(211, 20))
	await wait_until(func() -> bool: return fireballs.size() == 1 and fireballs[0].t_out >= 0.0, 2.5)
	fb = fireballs[0] if fireballs.size() > 0 else {"t_in": 0.0, "t_out": -1.0, "hits": []}
	check("A2-no-impact-on-timeout", casts == 1 and fb.t_out >= 0.0 and fb.hits.is_empty() and impacts.is_empty()
		and fb.t_out - fb.t_in > 1.9, {"casts": casts, "fireball_life_s": snappedf(fb.t_out - fb.t_in, 0.001),
		"hits": fb.hits.size(), "impacts": impacts.size()})

	# Into the ground/right-wall corner: two contacts in one frame would hit the _spent guard (A2; best effort).
	await fresh(1150)
	await click_at(Vector2(1279, 326))
	await wait_until(func() -> bool: return fireballs.size() == 1 and fireballs[0].t_out >= 0.0, 1.0)

	# Two impacts inside one lifetime: the second spawns while the first is still in the tree (A4 overlap).
	await fresh(200)
	await click_at(Vector2(300, 340))
	await wait_s(COOLDOWN)
	await click_at(Vector2(300, 340))
	await wait_until(func() -> bool: return impacts.size() == 2, 1.5)
	var first: Dictionary = impacts[0] if impacts.size() > 0 else {}
	var second: Dictionary = impacts[1] if impacts.size() > 1 else {}
	check("A4-overlap-second-impact-while-first-alive", casts == 2 and impacts.size() == 2
		and second.alive_at_entry == 1 and first.t_out < 0.0 and second.t_in - first.t_in < IMPACT_LIFE,
		{"casts": casts, "impacts": impacts.size(), "alive_when_second_spawned": second.get("alive_at_entry"),
		"spawn_gap_s": snappedf(second.get("t_in", 0.0) - first.get("t_in", 0.0), 0.001)})

	# Steady casting at the cooldown into the ground for 3 s: at most 3 alive at once (A4).
	await fresh(200)
	var screen := move_mouse(Vector2(300, 340))
	for i in 180:
		mouse_button(screen, i % 2 == 0)
		await physics_frame
	mouse_button(screen, false)
	await wait_until(func() -> bool: return fireballs.all(func(f: Dictionary) -> bool: return f.t_out >= 0.0), 1.0)
	check("A4-steady-casting-at-most-3-alive", casts >= 8 and max_alive >= 2 and max_alive <= 3,
		{"casts_in_3s": casts, "impacts": impacts.size(), "max_alive": max_alive})

	await wait_until(func() -> bool: return alive().is_empty(), IMPACT_LIFE + 0.3)
	close_case()

	# Across every case: one impact per fireball that collided, none for the rest (A1, A2 _spent).
	var per_fb := ledger.filter(func(e: Dictionary) -> bool: return e.has("hits"))
	var wrong := per_fb.filter(func(e: Dictionary) -> bool: return e.impacts != (1 if e.hits > 0 else 0))
	var multi := per_fb.filter(func(e: Dictionary) -> bool: return e.hits > 1).size()
	var stray := ledger.filter(func(e: Dictionary) -> bool: return e.get("unattributed", false)).size()
	check("A1-A2-one-impact-per-colliding-fireball-never-two", not per_fb.is_empty() and wrong.is_empty() and stray == 0,
		{"fireballs": per_fb.size(), "collided": per_fb.filter(func(e: Dictionary) -> bool: return e.hits > 0).size(),
		"mismatched": wrong, "unattributed_impacts": stray, "fireballs_with_2_or_more_contacts": multi})

	# Every impact frees itself 0.9 s after it spawns (A6), within one frame plus one physics tick.
	var lives := ledger.filter(func(e: Dictionary) -> bool: return e.has("life")).map(func(e: Dictionary) -> float: return e.life)
	var tol := root.get_process_delta_time() + PHYSICS_STEP + 1e-4
	var bad := lives.filter(func(l: float) -> bool: return absf(l - IMPACT_LIFE) > tol)
	check("A6-each-impact-freed-after-0.9s", not lives.is_empty() and bad.is_empty(),
		{"impacts": lives.size(), "min_s": snappedf(lives.min(), 0.0001) if lives else -1.0,
		"max_s": snappedf(lives.max(), 0.0001) if lives else -1.0, "tolerance_s": snappedf(tol, 0.0001), "outside": bad})

	main.queue_free()
	clock.queue_free()
	await process_frame
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)
