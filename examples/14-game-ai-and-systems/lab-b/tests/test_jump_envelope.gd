extends SceneTree

# Measures the player's actual jump envelope from a flat Ground-layer floor.
# Prints JUMP_RISE_PIXELS, JUMP_RISE_TILES, JUMP_HORIZ_PIXELS, JUMP_HORIZ_TILES.

func _initialize() -> void:
	call_deferred("run")

func key(code: Key, pressed: bool) -> void:
	var event := InputEventKey.new()
	event.physical_keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)

func run() -> void:
	var demo: Node = load("res://world.tscn").instantiate()
	root.add_child(demo)
	var player: CharacterBody2D = demo.get_node("Player")

	# Let the player settle on the floor.
	await create_timer(0.3).timeout

	if not player.is_on_floor():
		print("WARN: player not on floor at start; results may be wrong")

	# --- Vertical rise: still jump ---
	var floor_y := player.position.y

	key(KEY_W, true)
	await physics_frame
	key(KEY_W, false)

	var peak_y := player.position.y
	for _i in 200:
		await physics_frame
		if player.position.y < peak_y:
			peak_y = player.position.y
		if player.is_on_floor() and _i > 10:
			break

	var rise_pixels := floor_y - peak_y
	var tile_size := 16.0
	print("JUMP_RISE_PIXELS %.1f" % rise_pixels)
	print("JUMP_RISE_TILES  %.2f" % (rise_pixels / tile_size))

	# Let the player fully land before the horizontal test.
	await create_timer(0.5).timeout

	# Reset to a known start position so the acceleration run stays on solid ground.
	player.position = Vector2(120.0, floor_y)
	player.velocity = Vector2.ZERO
	await create_timer(0.2).timeout

	# Accelerate to near top speed.
	key(KEY_D, true)
	for _i in 60:
		await physics_frame

	var takeoff_x := player.position.x

	# Jump while running.
	key(KEY_W, true)
	await physics_frame
	key(KEY_W, false)

	# Measure until landing (or 300 frames).
	for _i in 300:
		await physics_frame
		if player.is_on_floor() and _i > 10:
			break

	key(KEY_D, false)

	var horiz_pixels := player.position.x - takeoff_x
	print("JUMP_HORIZ_PIXELS %.1f" % horiz_pixels)
	print("JUMP_HORIZ_TILES  %.2f" % (horiz_pixels / tile_size))

	demo.queue_free()
	await process_frame
	quit(0)
