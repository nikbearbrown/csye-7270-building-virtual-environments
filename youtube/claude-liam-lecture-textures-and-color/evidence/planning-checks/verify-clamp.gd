extends SceneTree
# Does a colour value above one survive? A shader writes COLOR = (1.5, 1.2, 0.5); read the root viewport's pixel as a float, with HDR 2D off and on.
# With HDR 2D on, the root texture is linear (docs), so the value is reported raw and also converted with linear_to_srgb().
# Run: godot --path <dir> [--rendering-method ...] --script res://verify-clamp.gd
func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func run() -> void:
	root.size = Vector2i(320, 180)
	var rect := ColorRect.new()
	rect.size = Vector2(320, 180)
	var sh := Shader.new()
	sh.code = "shader_type canvas_item;\nvoid fragment() { COLOR = vec4(1.5, 1.2, 0.5, 1.0); }\n"
	var mat := ShaderMaterial.new()
	mat.shader = sh
	rect.material = mat
	root.add_child(rect)
	out("env", {"renderer": RenderingServer.get_current_rendering_method()})
	for hdr in [false, true]:
		if hdr and RenderingServer.get_current_rendering_method() == "gl_compatibility":
			out("skip", {"reason": "Compatibility does not support HDR 2D (docs)"})
			continue
		root.use_hdr_2d = hdr
		await frames(4)
		RenderingServer.force_draw(false)
		var img := root.get_texture().get_image()
		var fmt := img.get_format()
		img.convert(Image.FORMAT_RGBAF)
		var c := img.get_pixel(160, 90)
		out("clamp-hdr2d-%s" % str(hdr), {"image_format": fmt, "raw_read": [snappedf(c.r, 0.0001), snappedf(c.g, 0.0001), snappedf(c.b, 0.0001)],
			"note": "written (1.5, 1.2, 0.5): a read of exactly 1.0 means the 2D buffer cut it off at one; above one means it was kept (linear values with HDR 2D on)"})
	quit(0)
