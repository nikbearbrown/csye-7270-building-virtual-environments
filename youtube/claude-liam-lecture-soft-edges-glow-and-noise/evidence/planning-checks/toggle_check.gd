extends SceneTree
# toggle_check.gd: can the capture switch HDR 2D and the environment's glow ON WHILE RUNNING, so one clip shows the before and the after?
# Plan for the glow captures: 0 s SDR; 1 s Viewport.use_hdr_2d = true on the root; 3 s a WorldEnvironment (glow on, background Canvas, intensity 2) appears.
# This script does exactly that and reads the same pixels as glow_check.gd after each step, to compare with the static runs G1, G3 and G6.
#   godot --path <scratch project> --script res://toggle_check.gd -- --shader <abs path of 14-glow-bubble.gdshader>
# Also: the flat-colour swatches (source_color hint vs none) switching to HDR 2D at run time (runs H0 to H3 in the static form).

var SHADER := ""

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func rgba(c: Color) -> Array:
	return [snappedf(c.r, 0.0001), snappedf(c.g, 0.0001), snappedf(c.b, 0.0001)]

func disp(c: Color) -> Array:
	var d := c
	if root.use_hdr_2d:
		d = Color(clampf(c.r, 0.0, 1.0), clampf(c.g, 0.0, 1.0), clampf(c.b, 0.0, 1.0)).linear_to_srgb()
	return rgba(d)

func read(label: String) -> void:
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	print("RESULT " + JSON.stringify({"step": label, "root_use_hdr_2d": root.use_hdr_2d, "fmt": img.get_format(),
		"shows_body": disp(img.get_pixel(346, 206)), "shows_band": disp(img.get_pixel(403, 180)), "shows_halo108": disp(img.get_pixel(428, 180)),
		"shows_halo118": disp(img.get_pixel(438, 180)), "shows_stage": disp(img.get_pixel(30, 30)),
		"swatch_hint": disp(img.get_pixel(60, 300)), "swatch_nohint": disp(img.get_pixel(560, 300))}))

func make(code: String, pos: Vector2, size: Vector2, params: Dictionary = {}) -> ColorRect:
	var sh := Shader.new()
	sh.code = code
	var mat := ShaderMaterial.new()
	mat.shader = sh
	for k in params:
		mat.set_shader_parameter(k, params[k])
	var r := ColorRect.new()
	r.position = pos
	r.size = size
	r.material = mat
	return r

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--shader":
			SHADER = a[i + 1]
	DisplayServer.window_move_to_foreground()   # a covered window is not drawn
	RenderingServer.set_default_clear_color(Color("#5F7A96"))
	root.size = Vector2i(640, 360)
	var bubble := make(FileAccess.get_file_as_string(SHADER), Vector2(192, 52), Vector2(256, 256), {"glow": 1.0})
	root.add_child(bubble)
	# two flat swatches, one with the hint and one without, far left and far right of the window
	var hint := make("shader_type canvas_item;\nuniform vec4 c : source_color = vec4(0.37, 0.64, 0.57, 1.0);\nvoid fragment() { COLOR = c; }\n", Vector2(40, 280), Vector2(60, 60))
	var nohint := make("shader_type canvas_item;\nuniform vec4 c = vec4(0.37, 0.64, 0.57, 1.0);\nvoid fragment() { COLOR = c; }\n", Vector2(540, 280), Vector2(60, 60))
	root.add_child(hint)
	root.add_child(nohint)
	await frames(8)
	read("0 SDR (no HDR 2D, no environment)")
	root.use_hdr_2d = true
	await frames(8)
	read("1 HDR 2D switched on at run time")
	var env := Environment.new()
	env.glow_enabled = true
	env.glow_intensity = 2.0
	env.background_mode = Environment.BG_CANVAS
	var we := WorldEnvironment.new()
	we.environment = env
	root.add_child(we)
	await frames(8)
	read("2 WorldEnvironment (glow on, background Canvas, intensity 2) added at run time")
	env.glow_enabled = false
	await frames(8)
	read("3 glow switched off again (environment still there)")
	env.glow_enabled = true
	await frames(8)
	read("4 glow switched on again")
	root.use_hdr_2d = false
	await frames(8)
	read("5 HDR 2D switched off again (environment and glow still on)")
	quit(0)
