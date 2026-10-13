extends SceneTree
const Scn := preload("res://scenes_lib.gd")
func _initialize() -> void: call_deferred("run")
func run() -> void:
	RenderingServer.set_default_clear_color(Scn.STAGE)
	root.size = Vector2i(640, 360)
	var a := Scn.sprite(Scn.blob_texture(256, true), Vector2(160, 180), 1.0)
	var b := Scn.sprite(Scn.blob_texture(256, false), Vector2(480, 180), 1.0)
	root.add_child(a)
	root.add_child(b)
	for i in 4: await process_frame
	RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png("/private/tmp/claude-501/godot-shaders-local-world-and-screen-space/scratch/out/aa-test.png")
	var img: Image = Scn.blob_image(256, true)
	print("RESULT ", JSON.stringify({"id": "aa-blob", "centre_rgba": [img.get_pixel(128, 128).r, img.get_pixel(128, 128).a], "edge_pixel_alpha_at_x_51": img.get_pixel(51, 128).a, "outside_alpha": img.get_pixel(40, 128).a, "eye_pixel_rgb": [img.get_pixel(102, 120).r, img.get_pixel(102, 120).g, img.get_pixel(102, 120).b, img.get_pixel(102, 120).a]}))
	quit(0)
