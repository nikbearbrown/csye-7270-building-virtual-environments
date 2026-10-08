extends SceneTree

func _initialize() -> void:
	run_probe.call_deferred()

func run_probe() -> void:
	var scene = load("res://shower.tscn").instantiate()
	root.add_child(scene)
	current_scene = scene
	await physics_frame
	var manager = scene.get_node("Bullets")
	var bullet = manager.bullets[0]
	# Isolated diagnostic fixture, never used for gameplay capture.
	if "--static-fixture" in OS.get_cmdline_user_args():
		PhysicsServer2D.body_set_mode(bullet.body, PhysicsServer2D.BODY_MODE_STATIC)
		print("CONSTRUCTED_STATIC_BODY_FIXTURE")
	var before: Vector2 = bullet.position
	var speed: float = bullet.speed
	for i in range(60):
		await physics_frame
	var distance: float = before.x - bullet.position.x
	var expected: float = speed * 60.0 / Engine.physics_ticks_per_second
	var motion_ok: bool = absf(distance - expected) < 0.05 and bullet.position.y == before.y
	await process_frame
	var transform: Transform2D = PhysicsServer2D.body_get_state(bullet.body, PhysicsServer2D.BODY_STATE_TRANSFORM)
	var body_ok: bool = transform.origin.distance_to(bullet.position) < 0.001
	print("BODY_MODE ", PhysicsServer2D.body_get_mode(bullet.body), " RIGID_ENUM ", PhysicsServer2D.BODY_MODE_RIGID, " VELOCITY ", PhysicsServer2D.body_get_state(bullet.body, PhysicsServer2D.BODY_STATE_LINEAR_VELOCITY))
	print("MOTION_DISTANCE ", distance, " EXPECTED ", expected, " MOTION_OK ", motion_ok, " BODY_SYNC ", body_ok, " BODY ", transform.origin, " BULLET ", bullet.position)
	var aligned_count := 0
	for item in manager.bullets:
		var body_transform: Transform2D = PhysicsServer2D.body_get_state(item.body, PhysicsServer2D.BODY_STATE_TRANSFORM)
		if body_transform.origin.distance_to(item.position) < 0.001:
			aligned_count += 1
	print("ALIGNED_BODIES ", aligned_count, "/", manager.bullets.size())
	scene.queue_free()
	await process_frame
	await process_frame
	quit(0 if motion_ok and body_ok and aligned_count == 500 else 1)
