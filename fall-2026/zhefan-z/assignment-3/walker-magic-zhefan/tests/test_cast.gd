extends SceneTree
## Headless checks for S3: cast, fireball, facing toward the cursor, walls, and the cast guards.
##   Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_cast.gd
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.

const GROUND_TOP := 327.0

var main: Node
var player: Player
var results: Array[Dictionary] = []
var failures := 0
var casts := 0
var last_origin := Vector2.ZERO
var last_dir := Vector2.ZERO


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


func fresh(x: float) -> void:
	if is_instance_valid(main):
		main.queue_free()
		await process_frame
	main = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	player = main.player
	player.use_scripted = true
	player.global_position = Vector2(x, GROUND_TOP)
	casts = 0
	player.cast_fired.connect(func(o: Vector2, d: Vector2) -> void:
		casts += 1
		last_origin = o
		last_dir = d)
	await steps(10)


func fireballs() -> Array:
	return main.get_children().filter(func(n: Node) -> bool: return n is Fireball)


func bursts() -> int:
	return main.get_children().filter(func(n: Node) -> bool: return n.name.begins_with("Burst")).size()


func cast_at(aim: Vector2) -> void:
	player.scripted.aim = aim
	player.scripted.cast_pressed = true
	await physics_frame


func run() -> void:
	Controls.ensure()

	await fresh(200)
	var aim := Vector2(400, 250)
	await cast_at(aim)
	var fb: Array = fireballs()
	var tip := player.global_position + Vector2(11, -60)
	check("cast-spawns-one-fireball-at-crystal", casts == 1 and fb.size() == 1 and last_origin.is_equal_approx(tip)
		and last_dir.is_equal_approx((aim - tip).normalized()),
		{"casts": casts, "fireballs": fb.size(), "origin": last_origin, "expected_tip": tip, "dir": last_dir})

	var cast_frames := 0
	for i in 30:
		if player.state == Player.State.CAST:
			cast_frames += 1
		await physics_frame
	check("cast-image-held-then-idle", cast_frames >= 13 and cast_frames <= 16 and player.state == Player.State.IDLE,
		{"frames_in_cast_image": cast_frames, "after": Player.State.keys()[player.state]})

	await fresh(200)
	await cast_at(Vector2(40, 260))
	check("cast-turns-toward-cursor", player.facing == -1 and player.sprite.flip_h and last_dir.x < 0
		and last_origin.is_equal_approx(player.global_position + Vector2(-11, -60)),
		{"facing": player.facing, "flip_h": player.sprite.flip_h, "dir": last_dir})
	await steps(30)
	check("facing-stays-after-cast-without-input", player.facing == -1, {"facing": player.facing})

	# Running right while casting left: faces the cast during the hold, then follows movement again.
	await fresh(200)
	player.scripted.move = 1.0
	await cast_at(Vector2(40, 260))
	await steps(5)
	var during := player.facing
	await steps(20)
	check("cast-facing-wins-during-hold-then-movement", during == -1 and player.facing == 1,
		{"facing_during_hold": during, "facing_after": player.facing})
	player.scripted.move = 0.0

	# Into the ground: removed, with a burst.
	await fresh(200)
	await cast_at(Vector2(260, 400))
	var saw_burst := false
	var frames := 0
	while fireballs().size() > 0 and frames < 120:
		await physics_frame
		frames += 1
		saw_burst = saw_burst or bursts() > 0
	await process_frame
	saw_burst = saw_burst or bursts() > 0
	check("fireball-destroyed-by-ground-with-burst", fireballs().is_empty() and saw_burst and frames < 30,
		{"frames_to_hit": frames, "burst_seen": saw_burst})
	await create_timer(0.3).timeout
	check("burst-removed-after-a-moment", bursts() == 0, {"bursts_left": bursts()})

	# Into the right-hand level wall (x = 1280): removed well before its 2 s lifetime.
	await fresh(1150)
	await cast_at(Vector2(1400, GROUND_TOP - 60))
	frames = 0
	while fireballs().size() > 0 and frames < 200:
		await physics_frame
		frames += 1
	check("fireball-destroyed-by-wall", fireballs().is_empty() and frames < 60, {"frames_to_hit": frames})

	# Real Input guards (not the scripted shortcut): hold for 2 s -> 1 cast; tap every frame -> cooldown-limited.
	await fresh(200)
	player.use_scripted = false
	Input.action_press("cast")
	await steps(120)
	Input.action_release("cast")
	await steps(30)
	check("held-cast-fires-once", casts == 1, {"casts_in_2s_held": casts})

	await fresh(200)
	player.use_scripted = false
	for i in 120:
		if i % 2 == 0:
			Input.action_press("cast")
		else:
			Input.action_release("cast")
		await physics_frame
	Input.action_release("cast")
	check("rapid-taps-limited-by-cooldown", casts == 6, {"casts_in_2s_tapping": casts, "expected": 6})

	await fresh(200)
	player.fail("test")
	player.scripted.cast_pressed = true
	await steps(5)
	check("no-cast-after-fail", casts == 0, {"casts": casts})

	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)
