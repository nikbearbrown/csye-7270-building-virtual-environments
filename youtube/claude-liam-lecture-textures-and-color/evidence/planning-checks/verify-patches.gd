extends SceneTree
# Three patches, one typed colour (0.2, 0.4, 0.6): (1) a ColorRect with that colour, (2) a shader patch whose uniform has the source_color hint,
# (3) a shader patch whose uniform has no hint. Rendered with HDR 2D ON (Forward+/Mobile) and, for contrast, in Compatibility (HDR 2D unsupported).
# Saves a PNG of what the screen shows and prints the three centre pixels. Run: godot --path <dir> --rendering-method forward_plus --script res://verify-patches.gd -- --hdr2d --png /abs/path.png
const HINTED := "shader_type canvas_item;\nuniform vec4 tint : source_color = vec4(0.2, 0.4, 0.6, 1.0);\nvoid fragment() { COLOR = tint; }\n"
const PLAIN := "shader_type canvas_item;\nuniform vec4 tint = vec4(0.2, 0.4, 0.6, 1.0);\nvoid fragment() { COLOR = tint; }\n"

func _initialize() -> void: call_deferred("run")

func patch(code: String, x: float) -> ColorRect:
	var r := ColorRect.new()
	r.position = Vector2(x, 20)
	r.size = Vector2(96, 140)
	if code == "":
		r.color = Color(0.2, 0.4, 0.6)
	else:
		var sh := Shader.new()
		sh.code = code
		var m := ShaderMaterial.new()
		m.shader = sh
		r.material = m
	return r

func run() -> void:
	var args := OS.get_cmdline_user_args()
	var hdr := args.has("--hdr2d")
	var png := ""
	var i := args.find("--png")
	if i >= 0: png = args[i + 1]
	root.size = Vector2i(320, 180)
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	if hdr: root.use_hdr_2d = true
	root.add_child(patch("", 8))
	root.add_child(patch(HINTED, 112))
	root.add_child(patch(PLAIN, 216))
	for k in 5: await process_frame
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	img.convert(Image.FORMAT_RGBAF)
	if hdr:
		for y in img.get_height():
			for x in img.get_width():
				img.set_pixel(x, y, img.get_pixel(x, y).linear_to_srgb())
	var pts := {"node_color": 56, "hinted_uniform": 160, "plain_uniform": 264}
	var d := {"renderer": RenderingServer.get_current_rendering_method(), "hdr2d": hdr}
	for k in pts.keys():
		var c := img.get_pixel(pts[k], 90)
		d[k] = [snappedf(c.r, 0.0001), snappedf(c.g, 0.0001), snappedf(c.b, 0.0001)]
	if png != "":
		img.convert(Image.FORMAT_RGBA8)
		img.save_png(png)
		d["png"] = png
	print("RESULT " + JSON.stringify(d))
	quit(0)
