extends SceneTree
# I: the same fraction of the picture on images of different sizes, and the sheet-safe shader.
#  I1: three versions of the sprite (32, 64 and 128 pixels wide) drawn the same size on screen, outlined with a step of 0.02 of the picture (literal) -> how many image pixels is that, how does the line look?
#  I2: the same three outlined with TEXTURE_PIXEL_SIZE * 1 -> always one image pixel, so the on-screen line differs.
#  I3: the sheet-safe shader (reads clamped into REGION_RECT) on the packed sheet from verify_c.
# Run: godot --path <scratch project> --script res://verify_i_sizes.gd -- --out <png dir>
const Lib := preload("res://ol_lib.gd")
var OUT := "/tmp"

func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

const LITERAL := "shader_type canvas_item;\nuniform vec4 line_color : source_color = vec4(0.25, 0.25, 0.75, 1.0);\nvoid fragment() {\n\tvec2 dx = vec2(0.02, 0.0);\n\tvec2 dy = vec2(0.0, 0.02);\n\tvec4 color = texture(TEXTURE, UV);\n\tfloat around = texture(TEXTURE, UV + dx).a + texture(TEXTURE, UV - dx).a + texture(TEXTURE, UV + dy).a + texture(TEXTURE, UV - dy).a;\n\tCOLOR = mix(color, line_color, min(around, 1.0) * (1.0 - color.a));\n}\n"

func shoot_three(shader_code: String, name: String, params: Dictionary) -> void:
	var nodes: Array = []
	var xs := [110.0, 320.0, 530.0]
	var i := 0
	for n in [32, 64, 128]:
		var img := Lib.blob(n)
		var sp := Sprite2D.new()
		sp.texture = ImageTexture.create_from_image(img)
		sp.position = Vector2(xs[i], 180)
		sp.scale = Vector2(192.0 / n, 192.0 / n)      # all drawn 192 screen pixels wide
		sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		var sh := Shader.new(); sh.code = shader_code
		var m := ShaderMaterial.new(); m.shader = sh
		for k in params: m.set_shader_parameter(k, params[k])
		sp.material = m
		root.add_child(sp)
		nodes.append(sp)
		i += 1
	await frames(3)
	Lib.save(Lib.snap(root), OUT + "/" + name + ".png")
	for sp in nodes: sp.queue_free()
	await frames(1)

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--out": OUT = a[i + 1]
	RenderingServer.set_default_clear_color(Lib.STAGE)
	root.size = Vector2i(640, 360)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	await shoot_three(LITERAL, "sizes-literal-0.02", {})
	var px_code := Lib.shader_code("06-pixel-steps.gdshader")
	await shoot_three(px_code, "sizes-pixelsteps-t1", {"thickness": 1.0})
	await shoot_three(px_code, "sizes-pixelsteps-t2", {"thickness": 2.0})

	# I3: sheet-safe shader on the packed sheet
	var img := Image.create_empty(128, 64, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	for y in 64:
		for x in 64:
			img.set_pixel(x, y, Lib.TEAL)
	var c := Vector2(96, 32)
	for y in 64:
		for x in range(64, 128):
			if Vector2(x, y).distance_to(c) < 14.0:
				img.set_pixel(x, y, Lib.CREAM)
	var sheet := ImageTexture.create_from_image(img)
	var sp := Sprite2D.new()
	sp.texture = sheet; sp.hframes = 2; sp.frame = 1; sp.centered = false
	sp.position = Vector2(192, 52); sp.scale = Vector2(4, 4)
	sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	sp.material = Lib.material("12-sheet-safe.gdshader", {"thickness": 4.0})
	root.add_child(sp)
	await frames(3)
	var im := Lib.snap(root)
	Lib.save(im, OUT + "/sheet-safe-t4.png")
	var run: Array = []
	for x in range(192, 215):
		var col := im.get_pixel(x, 180)
		run.append(1 if (absf(col.r - 0.25) < 0.02 and absf(col.b - 0.75) < 0.02) else 0)
	out("I3-sheet-safe", {"line_pixels_along_row_y180_from_frame_left": run, "reading": "all zeros = no phantom line at the frame's left edge"})
	# and is the ring around the small disc still drawn?
	var ring := 0
	for y in range(52, 308):
		for x in range(192, 448):
			var col2 := im.get_pixel(x, y)
			if absf(col2.r - 0.25) < 0.02 and absf(col2.b - 0.75) < 0.02:
				ring += 1
	out("I3b-sheet-safe-ring", {"line_pixels_in_frame": ring, "reading": "the disc's own ring (4 image pixels thick, x16 screen pixels per image pixel^2) must still be there"})
	quit(0)
