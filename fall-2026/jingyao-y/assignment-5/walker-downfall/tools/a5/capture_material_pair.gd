extends SceneTree

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var scene: Node3D = load("res://tests/material_review.tscn").instantiate()
	root.add_child(scene)
	for i in 20: await process_frame
	await RenderingServer.frame_post_draw
	var tag := "materials-shared-shader-change"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--name="): tag = arg.trim_prefix("--name=")
	root.get_texture().get_image().save_png("res://evidence/a5/use-it/" + tag + ".png")
	print("A5_MATERIAL_PAIR_CAPTURE ", tag)
	quit()
