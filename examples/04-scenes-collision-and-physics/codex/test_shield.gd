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
	await physics_frame


func click(button: Button) -> void:
	for down in [true, false]:
		var event := InputEventMouseButton.new()
		event.position = button.get_global_rect().get_center()
		event.global_position = event.position
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = down
		root.push_input(event, true)
		await physics_frame


func run() -> void:
	seed(456)
	root.size = Vector2i(480, 720)
	var game: Node = load("res://main.tscn").instantiate()
	root.add_child(game)
	await physics_frame
	await physics_frame
	var player: Area2D = game.get_node("Player")
	await click(game.get_node("HUD/StartButton"))

	var pickup: Area2D = load("res://pickup.tscn").instantiate()
	pickup.position = player.position + Vector2(100, 0)
	game.add_child(pickup)
	await physics_frame
	await key(KEY_D, true)
	for frame in 30:
		await physics_frame
		if not is_instance_valid(pickup):
			break
	await key(KEY_D, false)
	await physics_frame
	check(not is_instance_valid(pickup) and player.shielded, "real D-key movement collects pickup and enables shield")

	# Let the normal delayed game start occur, then remove incidental mobs before
	# installing the same deterministic frozen collision fixture as test_input.gd.
	while not game.get_node("StartTimer").is_stopped():
		await physics_frame
	for existing_mob in get_nodes_in_group("mobs"):
		existing_mob.queue_free()
	await physics_frame
	var mob: RigidBody2D = load("res://mob.tscn").instantiate()
	mob.position = player.position
	mob.freeze = true
	game.add_child(mob)
	await physics_frame
	await physics_frame
	check(player.visible and not player.get_node("CollisionShape2D").disabled, "shielded mob contact does not hide or disable player")
	check(not game.get_node("MobTimer").is_stopped() and not game.get_node("ScoreTimer").is_stopped() and not game.get_node("PickupTimer").is_stopped(), "shielded mob contact keeps gameplay timers running")

	while not player.get_node("ShieldTimer").is_stopped():
		await physics_frame
	var frames_after_expiry := 0
	while player.visible and frames_after_expiry < 10:
		await physics_frame
		frames_after_expiry += 1
	check(not player.visible and player.get_node("CollisionShape2D").disabled and frames_after_expiry <= 10, "overlapping mob hits within 10 physics frames of shield expiry")

	var leftover: Area2D = load("res://pickup.tscn").instantiate()
	leftover.position = Vector2(100, 100)
	game.add_child(leftover)
	await physics_frame
	await create_timer(2.2).timeout
	await click(game.get_node("HUD/StartButton"))
	await physics_frame
	await physics_frame
	check(get_nodes_in_group("pickups").is_empty(), "restart clears pickups")
	check(not player.shielded and player.get_node("ShieldTimer").is_stopped(), "restart clears shield")

	game.get_node("Music").stop()
	game.get_node("DeathSound").stop()
	await create_timer(0.25).timeout
	print("RESULT failures=", failures, "; headless shield state and collision fixtures, not footage")
	quit(1 if failures else 0)
