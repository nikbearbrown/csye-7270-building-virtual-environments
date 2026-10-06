extends SceneTree

# Read-only probe: raycasts downward at candidate pad positions near player start.
# Candidates avoid the input_probe forward-walk path (X in [-9.5,-4.7], Z≈3.93).
func _initialize() -> void:
	call_deferred("run_probe")

func run_probe() -> void:
	var game := load("res://game.tscn").instantiate() as Node3D
	root.add_child(game)
	current_scene = game
	await physics_frame
	await physics_frame
	await physics_frame

	var space_state := root.get_world_3d().direct_space_state
	var start := Vector2(-9.498, 3.933)

	# Candidate XZ positions, all off the +X forward-walk path
	var candidates: Array[Vector2] = [
		Vector2(-9.498, 6.933),   # +3 m Z
		Vector2(-9.498, 7.933),   # +4 m Z (primary target)
		Vector2(-9.498, 8.933),   # +5 m Z
		Vector2(-9.498, 9.933),   # +6 m Z
		Vector2(-9.498, 0.933),   # -3 m Z
		Vector2(-9.498, -0.067),  # -4 m Z
		Vector2(-7.498, 6.933),   # +2m X +3m Z diagonal
		Vector2(-11.498, 6.933),  # -2m X +3m Z diagonal
	]

	for c in candidates:
		var dist: float = (c - start).length()
		var query := PhysicsRayQueryParameters3D.create(
			Vector3(c.x, 20.0, c.y),
			Vector3(c.x, -20.0, c.y)
		)
		var hit := space_state.intersect_ray(query)
		var floor_y: float = -999.0
		var normal_str := "none"
		if not hit.is_empty():
			floor_y = (hit["position"] as Vector3).y
			normal_str = str(hit["normal"])
		print(JSON.stringify({
			"x": c.x, "z": c.y,
			"dist_from_start_m": snappedf(dist, 0.001),
			"floor_hit": not hit.is_empty(),
			"floor_y": snappedf(floor_y, 0.001),
			"normal": normal_str
		}))

	current_scene = null
	game.queue_free()
	await process_frame
	quit(0)
