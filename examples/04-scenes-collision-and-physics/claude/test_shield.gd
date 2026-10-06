extends SceneTree

var failures := 0

func _initialize() -> void:
	call_deferred("run")

func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
	print("PASS " if ok else "FAIL ", label)

func key(code: Key, down: bool) -> void:
	var event := InputEventKey.new()
	event.physical_keycode = code
	event.pressed = down
	Input.parse_input_event(event)
	await process_frame

func click(button: Button) -> void:
	for down in [true, false]:
		var event := InputEventMouseButton.new()
		event.position = button.get_global_rect().get_center()
		event.global_position = event.position
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = down
		root.push_input(event, true)
		await process_frame

func run() -> void:
	seed(789)
	root.size = Vector2i(480, 720)
	var game: Node = load("res://main.tscn").instantiate()
	root.add_child(game)
	await process_frame
	await process_frame

	# Start the game via the HUD Start button.
	await click(game.get_node("HUD/StartButton"))
	# Wait for StartTimer (2 s) to expire so MobTimer and ScoreTimer are running.
	await create_timer(2.2).timeout

	var player: Area2D = game.get_node("Player")

	# Place one pickup 100 px to the player's right.
	var pickup_scene: PackedScene = load("res://pickup.tscn")
	var pickup = pickup_scene.instantiate()
	pickup.position = player.position + Vector2(100.0, 0.0)
	game.add_child(pickup)
	await process_frame

	# Collect the pickup with real D-key input (player moves ~120 px in 0.3 s at 400 px/s).
	await key(KEY_D, true)
	await create_timer(0.35).timeout
	await key(KEY_D, false)
	# Allow area_entered to propagate through the physics pipeline.
	await process_frame
	await process_frame

	check(player.shielded, "pickup collected: player shielded")

	# Place a frozen mob fixture at the player's current position.
	var mob: RigidBody2D = load("res://mob.tscn").instantiate()
	mob.position = player.position
	mob.freeze = true
	game.add_child(mob)
	# Wait long enough for the physics overlap to register.
	await create_timer(0.15).timeout

	# Shielded contact: player must remain visible and timers must keep running.
	check(player.visible, "shielded contact does not hide player")
	check(
		not game.get_node("MobTimer").is_stopped() and not game.get_node("ScoreTimer").is_stopped(),
		"shielded contact does not stop gameplay timers"
	)

	# Wait for the 3-second shield to expire (with a margin).
	await create_timer(3.2).timeout

	# The hit must fire within 10 physics frames of shield expiry while mob still overlaps.
	var hit_within_frames := false
	for _i in range(10):
		await physics_frame
		if not player.visible:
			hit_within_frames = true
			break

	check(hit_within_frames, "hit fires within 10 physics frames after shield expires with mob overlapping")
	check(
		game.get_node("MobTimer").is_stopped(),
		"game over: MobTimer stopped after post-shield hit"
	)

	# Wait for the game-over message sequence and the Start button to appear.
	await create_timer(2.5).timeout
	await click(game.get_node("HUD/StartButton"))
	await process_frame
	await process_frame

	check(player.visible and not player.shielded, "restart clears shield and shows player")
	check(get_nodes_in_group("pickups").is_empty(), "restart clears all pickups")

	game.get_node("Music").stop()
	game.get_node("DeathSound").stop()
	await create_timer(0.25).timeout
	print("RESULT failures=", failures, "; headless state and collision fixture, not footage")
	quit(1 if failures else 0)
