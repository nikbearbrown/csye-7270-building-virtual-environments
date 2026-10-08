extends SceneTree

# Read-only observations of actual gameplay driven exclusively by input actions.
# This headless probe is not visual evidence or a human playtest.
func _initialize() -> void:
	call_deferred("run_probe")

func run_probe() -> void:
	seed(7375)
	var game = load("res://game.tscn").instantiate()
	root.add_child(game)
	current_scene = game
	var player = game.get_node("Player")
	var rows: Array = []
	var origin: Vector3 = player.position
	var moved := false
	var jumped := false
	var shot := false
	var reset := false
	var actions = ["move_forward", "move_back", "move_left", "move_right", "jump", "shoot", "reset_position"]
	for frame in range(600):
		await physics_frame
		var desired: Array[String] = []
		if frame >= 120 and frame < 180:
			desired.append("move_forward")
		if frame >= 210 and frame < 230:
			desired.append("jump")
		if frame == 300 or frame == 330:
			desired.append("shoot")
		if frame >= 420 and frame < 425:
			desired.append("reset_position")
		for action in actions:
			if action in desired:
				Input.action_press(action)
			else:
				Input.action_release(action)
		await process_frame
		var pos: Vector3 = player.position
		if frame >= 120 and frame < 200:
			moved = moved or Vector2(pos.x-origin.x, pos.z-origin.z).length() > 0.5
		if frame >= 210 and frame < 250:
			jumped = jumped or player.velocity.y > 5.0
		var bullets := 0
		for child in game.get_children():
			if child is Bullet:
				bullets += 1
		shot = shot or bullets > 0
		if frame >= 420 and frame < 425:
			reset = reset or pos.distance_to(origin) < 0.2
		rows.append({"frame": frame, "position": [pos.x,pos.y,pos.z],
			"velocity": [player.velocity.x,player.velocity.y,player.velocity.z],
			"on_floor": player.is_on_floor(), "coins": player.coins, "bullets": bullets})
	for action in actions:
		Input.action_release(action)
	var checks = {"movement":moved,"jump":jumped,"projectile_created":shot,"reset_action":reset}
	var report = {"method":"normal scripted input; headless; no gameplay state writes",
		"human_playtest":false,"checks":checks,"frames":rows,
		"unverified":["coin pickup","enemy impact","camera image","audio","physical controls","fun"]}
	var target = get_cmdline_output()
	var file = FileAccess.open(target, FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t"))
	file.close()
	print(JSON.stringify(checks))
	# Teardown only: stop active streams before freeing scene ownership.
	game.process_mode = Node.PROCESS_MODE_DISABLED
	stop_audio(game)
	await create_timer(0.1).timeout
	current_scene = null
	game.queue_free()
	await process_frame
	await process_frame
	quit(0 if moved and jumped and shot and reset else 1)

func stop_audio(node: Node) -> void:
	if node is AudioStreamPlayer or node is AudioStreamPlayer2D or node is AudioStreamPlayer3D:
		node.stop()
	for child in node.get_children():
		stop_audio(child)

func get_cmdline_output() -> String:
	var args = OS.get_cmdline_user_args()
	assert(args.size() == 1, "Supply a fresh report path after --")
	assert(not FileAccess.file_exists(args[0]), "Refusing to overwrite evidence")
	return args[0]
