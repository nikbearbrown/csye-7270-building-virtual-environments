extends SceneTree
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var game = load("res://game.tscn").instantiate()
	root.add_child(game)
	await physics_frame
	await physics_frame
	var pad = game.get_node("CheckpointPad")
	var p: Vector3 = pad.global_position
	var space := root.get_world_3d().direct_space_state
	var q := PhysicsRayQueryParameters3D.create(p + Vector3(0, 1.0, 0), p + Vector3(0, -3.0, 0))
	print("default collide_with_areas=", q.collide_with_areas, " collide_with_bodies=", q.collide_with_bodies)
	var hit := space.intersect_ray(q)
	print("default hit: ", hit.get("collider"), " y=", hit.get("position"))
	q.collide_with_areas = true
	var hit2 := space.intersect_ray(q)
	print("with areas: ", hit2.get("collider"), " y=", hit2.get("position"))
	game.queue_free()
	await process_frame
	quit(0)
