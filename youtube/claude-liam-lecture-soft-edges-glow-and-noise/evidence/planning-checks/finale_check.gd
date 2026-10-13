extends SceneTree
# finale_check.gd: the film's last picture, all layers at once: lab-shaders/15-bubble-complete.gdshader (soft edge, highlight, a scrolling
# NoiseTexture2D, the glow dial) with HDR 2D on, a WorldEnvironment (glow on, background Canvas, intensity 2) and the slate stage.
# Renders it at glow 0, 0.3, 0.6 and 1.0 and reads the same pixels as glow_check.gd. Prints one RESULT line per step; saves display-referred PNGs.
#   godot --path <scratch project> --script res://finale_check.gd -- --film <abs path of the film folder> --png-dir <abs dir>

var FILM := ""
var PNGDIR := ""

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func disp(c: Color) -> Array:
	var k := Color(clampf(c.r, 0.0, 1.0), clampf(c.g, 0.0, 1.0), clampf(c.b, 0.0, 1.0)).linear_to_srgb()
	return [snappedf(k.r, 0.0001), snappedf(k.g, 0.0001), snappedf(k.b, 0.0001)]

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--film": FILM = a[i + 1]
		elif a[i] == "--png-dir": PNGDIR = a[i + 1]
	DisplayServer.window_move_to_foreground()   # a covered window is not drawn
	RenderingServer.set_default_clear_color(Color("#5F7A96"))
	root.size = Vector2i(640, 360)
	root.use_hdr_2d = true
	var tex := NoiseTexture2D.new()
	tex.noise = FastNoiseLite.new()
	tex.seamless = true
	await tex.changed
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(FILM + "/lab-shaders/15-bubble-complete.gdshader")
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.set_shader_parameter("noise", tex)
	var rect := ColorRect.new()
	rect.size = Vector2(256, 256)
	rect.position = Vector2(192, 52)
	rect.material = mat
	root.add_child(rect)
	var env := Environment.new()
	env.glow_enabled = true
	env.glow_intensity = 2.0
	env.background_mode = Environment.BG_CANVAS
	var we := WorldEnvironment.new()
	we.environment = env
	root.add_child(we)
	var uniforms: Array = []
	for u in sh.get_shader_uniform_list():
		uniforms.append(str(u["name"]) + ":" + str(u["type"]))
	for g in [0.0, 0.3, 0.6, 1.0]:
		mat.set_shader_parameter("glow", g)
		await frames(10)
		RenderingServer.force_draw(false)
		var img := root.get_texture().get_image()
		print("RESULT " + JSON.stringify({"glow": g, "uniforms": uniforms, "renderer": RenderingServer.get_current_rendering_method(),
			"body_shows": disp(img.get_pixel(346, 206)), "highlight_shows": disp(img.get_pixel(282, 142)), "band_shows": disp(img.get_pixel(403, 180)),
			"halo108": disp(img.get_pixel(428, 180)), "halo118": disp(img.get_pixel(438, 180)), "stage": disp(img.get_pixel(30, 30))}))
		if PNGDIR != "":
			var shot := img.duplicate() as Image
			shot.convert(Image.FORMAT_RGBA8)
			shot.linear_to_srgb()
			shot.save_png(PNGDIR + "/finale-glow-" + str(g) + ".png")
	quit(0)
