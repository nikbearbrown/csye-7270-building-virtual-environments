extends SceneTree

func _initialize() -> void:
	run_probe.call_deferred()

func move_mouse(point: Vector2) -> void:
	var event := InputEventMouseMotion.new()
	event.position = point
	root.push_input(event, true)

func run_probe() -> void:
	var scene = load("res://shower.tscn").instantiate()
	root.add_child(scene)
	current_scene = scene
	var player = scene.get_node("Player")
	var bullets = scene.get_node("Bullets")
	for i in range(10):
		move_mouse(bullets.bullets[0].position + Vector2(0,16))
		await physics_frame
	var touched: bool = player.touching > 0 and player.sprite.frame == 1
	move_mouse(Vector2(-1000,-1000))
	for i in range(10):
		await physics_frame
	var recovered: bool = player.touching == 0 and player.sprite.frame == 0
	print("COLLISION_SAD ", touched, " RECOVERY_HAPPY ", recovered)
	scene.queue_free()
	await process_frame
	await process_frame
	quit(0 if touched and recovered else 1)
