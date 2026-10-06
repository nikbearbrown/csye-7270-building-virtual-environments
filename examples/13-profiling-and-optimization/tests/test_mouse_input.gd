extends SceneTree

func _initialize() -> void:
	run_probe.call_deferred()

func run_probe() -> void:
	var scene = load("res://shower.tscn").instantiate()
	root.add_child(scene)
	current_scene = scene
	await process_frame
	var event := InputEventMouseMotion.new()
	event.position = Vector2(240, 180)
	root.push_input(event, true)
	await process_frame
	var follows: bool = scene.get_node("Player").position == Vector2(240,164)
	var count_ok: bool = scene.get_node("Bullets").bullets.size() == 500
	print("MOUSE_FOLLOWS ", follows, " BULLET_COUNT_500 ", count_ok, " ACTUAL_POSITION ", scene.get_node("Player").position)
	scene.queue_free()
	await process_frame
	await process_frame
	quit(0 if follows and count_ok else 1)
