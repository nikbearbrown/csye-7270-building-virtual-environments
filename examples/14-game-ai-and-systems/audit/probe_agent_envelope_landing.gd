extends SceneTree
## Chapter-author probe: replay the agent's running-jump sequence on the
## original world.tscn and report takeoff speed, where the run ends, and any
## wall contact during the flight.
func _initialize() -> void:
	call_deferred("run")
func key(code: Key, pressed: bool) -> void:
	var e := InputEventKey.new()
	e.physical_keycode = code
	e.pressed = pressed
	Input.parse_input_event(e)
func run() -> void:
	var demo: Node = load("res://world.tscn").instantiate()
	root.add_child(demo)
	var player: CharacterBody2D = demo.get_node("Player")
	await create_timer(0.3).timeout
	var floor_y := player.position.y
	player.position = Vector2(120.0, floor_y)
	player.velocity = Vector2.ZERO
	await create_timer(0.2).timeout
	key(KEY_D, true)
	for i in 60:
		await physics_frame
	var tx := player.position.x
	print("takeoff x=", snappedf(tx, 0.1), " vx=", snappedf(player.velocity.x, 0.1))
	key(KEY_W, true)
	await physics_frame
	key(KEY_W, false)
	var wall_frames := 0
	for i in 300:
		await physics_frame
		if player.is_on_ceiling():
			print("ceiling contact at x=", snappedf(player.position.x, 0.1), " frame=", i)
		if player.is_on_wall():
			wall_frames += 1
		if player.is_on_floor() and i > 10:
			break
	key(KEY_D, false)
	var ground: TileMapLayer = demo.get_node("Ground")
	print("landing x=", snappedf(player.position.x, 0.1), " y=", snappedf(player.position.y, 0.1), " floor_y=", snappedf(floor_y, 0.1), " frames_touching_wall=", wall_frames, " cell_right_of_landing=", ground.get_cell_source_id(ground.local_to_map(player.position + Vector2(12, 0))))
	quit(0)
