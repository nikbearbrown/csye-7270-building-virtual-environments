extends SceneTree
# Parity tests for the node-based bullet manager (bench/bullets_nodes.gd).
# Checks: correct count, correct horizontal motion, player collision on overlap.
# Prints PASS/FAIL lines; exits 1 on any failure.


func _initialize() -> void:
	run_probe.call_deferred()


func move_mouse(point: Vector2) -> void:
	var event := InputEventMouseMotion.new()
	event.position = point
	root.push_input(event, true)


func run_probe() -> void:
	var count := 500
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--count="):
			count = int(arg.substr(8))

	var scene := (load("res://bench/shower_nodes.tscn") as PackedScene).instantiate()
	(scene.get_node("Bullets") as Node).set("bullet_count", count)
	root.add_child(scene)
	current_scene = scene

	await physics_frame

	var manager: Node = scene.get_node("Bullets")
	var player: Node = scene.get_node("Player")
	var bullets: Array = manager.get("bullets")

	var all_ok := true

	# --- Test 1: bullet count ---
	var count_ok: bool = bullets.size() == count
	if count_ok:
		print("PASS: BULLET_COUNT=%d" % bullets.size())
	else:
		print("FAIL: BULLET_COUNT=%d expected=%d" % [bullets.size(), count])
		all_ok = false

	# --- Test 2: one bullet moves left by speed * elapsed physics time ---
	var bullet = bullets[0]
	var before: Vector2 = bullet.position
	var speed: float = bullet.speed

	for _i in 60:
		await physics_frame

	var distance: float = before.x - bullet.position.x
	var expected: float = speed * 60.0 / Engine.physics_ticks_per_second
	var motion_ok: bool = absf(distance - expected) < 0.05 and absf(bullet.position.y - before.y) < 0.001
	if motion_ok:
		print("PASS: MOTION distance=%.3f expected=%.3f y_delta=%.6f" % [
			distance, expected, absf(bullet.position.y - before.y)
		])
	else:
		print("FAIL: MOTION distance=%.3f expected=%.3f y_delta=%.6f" % [
			distance, expected, absf(bullet.position.y - before.y)
		])
		all_ok = false

	# --- Test 3: player.touching rises when mouse overlaps a bullet ---
	var bullet_pos: Vector2 = bullets[0].position
	for _i in 10:
		move_mouse(bullet_pos + Vector2(0, 16))
		await physics_frame
	var touched: bool = player.get("touching") > 0
	if touched:
		print("PASS: COLLISION touching=%d" % player.get("touching"))
	else:
		print("FAIL: COLLISION touching=%d (player not detecting bullet)" % player.get("touching"))
		all_ok = false

	move_mouse(Vector2(-2000, -2000))
	for _i in 10:
		await physics_frame
	var recovered: bool = player.get("touching") == 0
	if recovered:
		print("PASS: RECOVERY touching=%d" % player.get("touching"))
	else:
		print("FAIL: RECOVERY touching=%d" % player.get("touching"))
		all_ok = false

	scene.queue_free()
	await process_frame
	await process_frame
	quit(0 if all_ok else 1)
