extends SceneTree
# What can a test that runs without a window see? Run twice and compare:
#   godot --headless --path <dir> --script res://verify-headless.gd      (no window, dummy renderer)
#   godot --path <dir> --script res://verify-headless.gd                  (a real window)
func _initialize() -> void: call_deferred("run")

func run() -> void:
	root.size = Vector2i(320, 180)
	var rect := ColorRect.new()
	rect.size = Vector2(320, 180)
	var sh := Shader.new()
	sh.code = "shader_type canvas_item;\nvoid fragment() { COLOR = vec4(0.2, 0.4, 0.6, 1.0); }\n"
	var mat := ShaderMaterial.new()
	mat.shader = sh
	rect.material = mat
	root.add_child(rect)
	for i in 3:
		await process_frame
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var d := {"display_driver": DisplayServer.get_name(), "rendering_method": RenderingServer.get_current_rendering_method(),
		"image_is_null": img == null}
	if img != null:
		var c := img.get_pixel(img.get_width() / 2, img.get_height() / 2)
		d["image_size"] = [img.get_width(), img.get_height()]
		d["centre_pixel"] = [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]
	print("RESULT " + JSON.stringify(d))
	quit(0)
