extends SceneTree
var game: Node3D
func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame
func shot(name: String) -> void:
	for item in game.hud.get_parent().get_children():
		if item is CanvasItem: item.queue_redraw()
	RenderingServer.force_draw(true)
	var path := ProjectSettings.globalize_path("res://../evidence/assignments/screenshots")
	DirAccess.make_dir_recursive_absolute(path)
	root.get_texture().get_image().save_png(path + "/" + name + ".png")
	print("CAPTURE "+name)
func run() -> void:
	root.size = Vector2i(1280,720)
	game = load("res://signal-garden/main.tscn").instantiate()
	game.audio_enabled = false
	root.add_child(game)
	await frames(10)
	await shot("01-start")
	Input.action_press("garden_right")
	await frames(40)
	Input.action_release("garden_right")
	await frames(2)
	Input.action_press("garden_action")
	await frames(18)
	await shot("02-charge")
	Input.action_release("garden_action")
	await frames(20)
	await shot("03-burst")
	await frames(40)
	await shot("04-open-gate")
	Input.action_press("garden_right")
	await frames(140)
	Input.action_release("garden_right")
	await shot("05-finish")
	game.queue_free()
	await process_frame
	quit()
