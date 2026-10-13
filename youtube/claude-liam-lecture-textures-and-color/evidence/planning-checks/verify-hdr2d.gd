extends SceneTree
# Does a canvas_item shader's source_color hint matter when the viewport renders 2D in HDR (use_hdr_2d = true)?
# Compares the centre pixel of a flat colour and of a mid-tone mix, with and without the hint, with use_hdr_2d off and on.
# With use_hdr_2d on, Viewport.get_texture() returns a LINEAR HDR image (docs, Viewport.get_texture note), so the script also
# converts the read value with linear_to_srgb(): that is the number the screen shows after the final blit.
# Run: godot --path <project dir> [--rendering-method forward_plus|mobile|gl_compatibility] --script res://verify-hdr2d.gd

const FLAT_H := "shader_type canvas_item;\nuniform vec4 a : source_color = vec4(0.2, 0.4, 0.6, 1.0);\nvoid fragment() { COLOR = a; }\n"
const FLAT_P := "shader_type canvas_item;\nuniform vec4 a = vec4(0.2, 0.4, 0.6, 1.0);\nvoid fragment() { COLOR = a; }\n"
const MIX_H := "shader_type canvas_item;\nuniform vec4 a : source_color = vec4(0.2, 0.2, 0.2, 1.0);\nuniform vec4 b : source_color = vec4(0.8, 0.8, 0.8, 1.0);\nvoid fragment() { COLOR = mix(a, b, 0.5); }\n"
const MIX_P := "shader_type canvas_item;\nuniform vec4 a = vec4(0.2, 0.2, 0.2, 1.0);\nuniform vec4 b = vec4(0.8, 0.8, 0.8, 1.0);\nvoid fragment() { COLOR = mix(a, b, 0.5); }\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func centre() -> Dictionary:
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var fmt := img.get_format()
	img.convert(Image.FORMAT_RGBAF)
	var c := img.get_pixel(img.get_width() / 2, img.get_height() / 2)
	var s := c.linear_to_srgb()
	return {"format": fmt, "read_rgb": [snappedf(c.r, 0.0001), snappedf(c.g, 0.0001), snappedf(c.b, 0.0001)],
		"read_as_if_linear_then_encoded": [snappedf(s.r, 0.0001), snappedf(s.g, 0.0001), snappedf(s.b, 0.0001)]}

func shot(code: String) -> Dictionary:
	var rect := ColorRect.new()
	rect.size = Vector2(640, 360)
	var sh := Shader.new()
	sh.code = code
	var mat := ShaderMaterial.new()
	mat.shader = sh
	rect.material = mat
	root.add_child(rect)
	await frames(4)
	var r := centre()
	rect.queue_free()
	await frames(2)
	return r

func run() -> void:
	root.size = Vector2i(640, 360)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name(), "use_hdr_2d_at_start": root.use_hdr_2d})
	for hdr in [false, true]:
		root.use_hdr_2d = hdr
		await frames(3)
		for pair in [["flat_hinted", FLAT_H], ["flat_plain", FLAT_P], ["mix_hinted", MIX_H], ["mix_plain", MIX_P]]:
			var r: Dictionary = await shot(pair[1])
			r["case"] = pair[0]
			r["use_hdr_2d"] = root.use_hdr_2d
			out("hdr2d-%s-%s" % [str(hdr), pair[0]], r)
	quit(0)
