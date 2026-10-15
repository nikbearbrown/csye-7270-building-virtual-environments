extends SceneTree
## Headless checks for S2: states, facing, jump, the pit, and art/collision alignment.
##   Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_player.gd
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.

const GROUND_TOP := 327.0

var main: Node
var player: Player
var results: Array[Dictionary] = []
var failures := 0
var fail_count := 0
var fail_reason := ""


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
	fail_count = 0
	fail_reason = ""
	player.failed.connect(func(r: String) -> void:
		fail_count += 1
		fail_reason = r)
	await steps(10)


func drive(move: float, frames: int, jump := false, hold := true) -> Dictionary:
	player.scripted.move = move
	player.scripted.jump_held = hold
	if jump:
		player.scripted.jump_pressed = true
	var peak := player.global_position.y
	var seen := {}
	for i in frames:
		await physics_frame
		peak = minf(peak, player.global_position.y)
		seen[Player.State.keys()[player.state]] = true
	return {"peak_y": peak, "states_seen": seen.keys()}


func run() -> void:
	Controls.ensure()

	await fresh(200)
	check("spawn-idle-on-ground", player.state == Player.State.IDLE and player.is_on_floor()
		and absf(player.global_position.y - GROUND_TOP) < 0.6 and player.sprite.texture == Player.TEXTURES[Player.State.IDLE],
		{"state": Player.State.keys()[player.state], "feet_y": player.global_position.y, "on_floor": player.is_on_floor()})

	await drive(1, 30)
	check("run-right-image-and-facing", player.state == Player.State.RUN and player.facing == 1 and not player.sprite.flip_h
		and player.sprite.texture == Player.TEXTURES[Player.State.RUN],
		{"state": Player.State.keys()[player.state], "facing": player.facing, "flip_h": player.sprite.flip_h, "vx": player.velocity.x})

	await drive(-1, 40)
	check("run-left-flips", player.state == Player.State.RUN and player.facing == -1 and player.sprite.flip_h,
		{"facing": player.facing, "flip_h": player.sprite.flip_h, "vx": player.velocity.x})

	await drive(0, 40)
	check("stop-returns-to-idle", player.state == Player.State.IDLE and player.facing == -1 and player.sprite.flip_h,
		{"state": Player.State.keys()[player.state], "facing_kept": player.facing})

	var j := await drive(0, 70, true)
	var height := GROUND_TOP - float(j.peak_y)
	check("jump-rise-fall-land", "RISE" in j.states_seen and "FALL" in j.states_seen and player.state == Player.State.IDLE
		and absf(height - 60.0) < 4.0,
		{"states_seen": j.states_seen, "jump_height_px": snappedf(height, 0.1), "landed_state": Player.State.keys()[player.state]})

	var s := await drive(0, 70, true, false)
	check("short-hop-when-released", GROUND_TOP - float(s.peak_y) < height * 0.5,
		{"short_hop_height_px": snappedf(GROUND_TOP - float(s.peak_y), 0.1)})

	# Clear the pit (gap x 520-580): run from x=400 and jump at the edge.
	await fresh(400)
	await drive(1, 1)
	while player.global_position.x < 512.0:
		await physics_frame
	var at := player.global_position.x
	await drive(1, 90, true)
	check("pit-cleared-with-running-jump", fail_count == 0 and player.is_on_floor() and player.global_position.x > 587.0,
		{"jumped_at_x": snappedf(at, 0.1), "landed_x": snappedf(player.global_position.x, 0.1), "fails": fail_count})

	# Walk into the pit: one fail, fall image, physics stopped; a second call changes nothing.
	await fresh(470)
	await drive(1, 120)
	var stopped := not player.is_physics_processing()
	player.fail("again", true)
	check("pit-fail-once-with-fall-image", fail_count == 1 and fail_reason == "Fell into the dark" and stopped
		and player.state == Player.State.FAIL and player.sprite.texture == Player.TEXTURES[Player.State.FALL],
		{"fails": fail_count, "reason": fail_reason, "physics_stopped": stopped, "y": snappedf(player.global_position.y, 0.1)})
	check("camera-frozen-on-fail", not main.failed_reason.is_empty(), {"main_failed_reason": main.failed_reason})

	# HP-0 style fail uses the kneeling image.
	await fresh(200)
	player.fail("Out of HP")
	check("hp-fail-uses-kneeling-image", player.sprite.texture == Player.TEXTURES[Player.State.FAIL], {"reason": fail_reason})

	# Art vs collision (CHARACTER-SHEET): anchor (31,67) at the feet; 14x44 rect at canvas x 24-38, y 23-67.
	var shape: CollisionShape2D = player.get_node("CollisionShape2D")
	var rect := (shape.shape as RectangleShape2D).size
	var canvas_rect := Rect2(shape.position - rect / 2 - player.sprite.offset, rect)
	check("collision-matches-sheet", rect == Vector2(14, 44) and canvas_rect == Rect2(24, 23, 14, 44)
		and player.sprite.offset == Vector2(-31, -67),
		{"rect_size": rect, "rect_in_canvas_px": canvas_rect, "sprite_offset": player.sprite.offset})

	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)
