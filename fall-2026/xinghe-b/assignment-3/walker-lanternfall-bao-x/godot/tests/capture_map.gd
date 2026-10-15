extends SceneTree
## Whole-arena overview of the market layout (camera zoomed out to fit the 1920x1080 arena in the 640x360 view).
const Session = preload("res://game/session.gd")

func _initialize() -> void:
	call_deferred("_main")

func _main() -> void:
	var game = Session.new()
	game.test_mode = true
	game.test_no_spawn = true
	root.add_child(game)
	game.start_run(1)
	game.hud.visible = false
	game.camera.limit_left = -100000
	game.camera.limit_top = -100000
	game.camera.limit_right = 100000
	game.camera.limit_bottom = 100000
	game.camera.set_process(false)
	game.camera.zoom = Vector2.ONE / 3.0
	for i in 4:
		await process_frame
	var out := ProjectSettings.globalize_path("res://../design/map-overview.png")
	root.get_texture().get_image().save_png(out)
	print("saved ", out)
	quit()
