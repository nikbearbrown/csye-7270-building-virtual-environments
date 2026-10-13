extends SceneTree
# Scratch verification for "Drawing Shapes with Math" (not shown in the film). Prints one RESULT line per check.
# Run (windowed, Forward+): godot --path <scratch project> --script res://verify-a.gd -- <absolute path to the film folder>
#   1. what the engine says about the crosshair's uniforms (type, hint, hint string): the data the Inspector builds its sliders from
#   2. the crosshair ColorRect over two different backdrops: is the outside really see-through?
#   3. an ODD-sized view, with arm_width at 0: does a hairline survive? (an edge case; the film does not claim it)

var film := ""

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func px(img: Image, x: int, y: int) -> Array:
	var c := img.get_pixel(x, y)
	return [snappedf(c.r, 0.0001), snappedf(c.g, 0.0001), snappedf(c.b, 0.0001)]

func make_shader() -> Shader:
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(film + "/lab-shaders/17-crosshair.gdshader")
	return sh

func run() -> void:
	var args := OS.get_cmdline_user_args()
	film = args[0] if args.size() > 0 else ""
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()})

	# 1. the uniform list
	var sh := make_shader()
	for u in sh.get_shader_uniform_list():
		out("1-uniform", {"name": u["name"], "type": u["type"], "hint": u["hint"], "hint_string": u["hint_string"],
			"PROPERTY_HINT_RANGE_is": PROPERTY_HINT_RANGE})

	# 2. see-through: two flat backdrops, the crosshair on top
	root.size = Vector2i(480, 480)
	var left := ColorRect.new()
	left.color = Color("#FAF9F5")
	left.position = Vector2(0, 0)
	left.size = Vector2(240, 480)
	var right := ColorRect.new()
	right.color = Color("#C9B79C")
	right.position = Vector2(240, 0)
	right.size = Vector2(240, 480)
	var cross := ColorRect.new()
	cross.size = Vector2(480, 480)
	var mat := ShaderMaterial.new()
	mat.shader = sh
	cross.material = mat
	root.add_child(left)
	root.add_child(right)
	root.add_child(cross)
	await frames(3)
	var img := grab()
	out("2-overlay", {"size": [img.get_width(), img.get_height()],
		"outside_shape_left_(60,60)": px(img, 60, 60), "backdrop_left_expected": [0.9804, 0.9765, 0.9608],
		"outside_shape_right_(420,60)": px(img, 420, 60), "backdrop_right_expected": [0.7882, 0.7176, 0.6118],
		"on_the_dot_(240,240)": px(img, 240, 240), "on_a_right_arm_(300,240)": px(img, 300, 240), "on_a_left_arm_(180,240)": px(img, 180, 240)})
	cross.queue_free(); left.queue_free(); right.queue_free()
	await frames(2)

	# 3. odd-sized view, arm_width = 0, arm_gap = 0, arm_length = 1, everything else 0
	root.size = Vector2i(481, 481)
	await frames(3)
	var odd := ColorRect.new()
	odd.size = Vector2(481, 481)
	var m2 := ShaderMaterial.new()
	m2.shader = sh
	for n in ["dot_size", "ring_distance", "ring_width", "arm_gap", "arm_width"]:
		m2.set_shader_parameter(n, 0.0)
	m2.set_shader_parameter("arm_length", 1.0)
	odd.material = m2
	root.add_child(odd)
	await frames(3)
	var img2 := grab()
	var teal := 0
	for x in range(img2.get_width()):
		var c := img2.get_pixel(x, 240)
		if c.g > 0.55 and c.r < 0.45: teal += 1
	var teal_even_row := 0
	for x in range(img2.get_width()):
		var c := img2.get_pixel(x, 100)
		if c.g > 0.55 and c.r < 0.45: teal_even_row += 1
	out("3-odd-view-zero-width-arms", {"view": [img2.get_width(), img2.get_height()], "teal_pixels_on_the_middle_row": teal, "teal_pixels_on_row_100": teal_even_row,
		"reading": "arm_width 0, arm_length 1, gap 0, all else 0. On an even view nothing is drawn (Lab run crosshair-all-0). A non-zero count on the middle row means the middle pixel row sits exactly on the axis."})
	quit(0)
