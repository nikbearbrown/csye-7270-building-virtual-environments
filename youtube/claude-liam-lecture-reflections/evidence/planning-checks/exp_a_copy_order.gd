extends SceneTree
# Experiment A (Reflections layout): where a BackBufferCopy sits in the tree decides what a screen-reading shader sees.
#
# Scene: three flat sprites A, B, C added in that order (so C is drawn on top), then a "preview" ColorRect in the top-right corner
# whose shader (lab-shaders/01-screen-preview.gdshader) shows the WHOLE screen texture, so we can read what the shader sees.
# For each case a BackBufferCopy is placed at a different tree position (or none) and we classify the preview at five spots.
#
# Run: godot --path <scratch project> --script res://exp_a_copy_order.gd [-- --renderer-note forward_plus]
# Output: one RESULT line per case.

const SHADERS := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/lab-shaders/"
const CLEAR := Color("#D9D5CA")
const COL_A := Color("#4F8F7E")
const COL_B := Color("#7FA7C9")
const COL_C := Color("#B7A6D9")
const NAMES := ["clear", "A", "B", "C"]

var scene: Node2D

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func out(id: String, data: Dictionary) -> void:
	data["case"] = id
	print("RESULT " + JSON.stringify(data))

func flat(c: Color, n: int = 100) -> ImageTexture:
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	img.fill(c)
	return ImageTexture.create_from_image(img)

func sprite(name: String, c: Color, pos: Vector2) -> Sprite2D:
	var s := Sprite2D.new()
	s.name = name
	s.texture = flat(c)
	s.position = pos
	return s

func preview(name: String, pos: Vector2) -> ColorRect:
	var r := ColorRect.new()
	r.name = name
	r.position = pos
	r.size = Vector2(192, 108)          # 640x360 shrunk by 3.333: shows the whole screen texture
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(SHADERS + "01-screen-preview.gdshader")
	var mat := ShaderMaterial.new()
	mat.shader = sh
	r.material = mat
	return r

func build(bbc_index: int, mode: int, extra: Callable = Callable()) -> BackBufferCopy:
	# Fresh scene each case. bbc_index: tree position of the BackBufferCopy among [A, B, C, preview]; -1 = none.
	if scene != null:
		scene.queue_free()
		await process_frame
	scene = Node2D.new()
	root.add_child(scene)
	scene.add_child(sprite("A", COL_A, Vector2(120, 150)))
	scene.add_child(sprite("B", COL_B, Vector2(170, 190)))
	scene.add_child(sprite("C", COL_C, Vector2(220, 150)))
	scene.add_child(preview("Preview", Vector2(420, 20)))
	var b: BackBufferCopy = null
	if bbc_index >= 0:
		b = BackBufferCopy.new()
		b.name = "BackBufferCopy"
		b.copy_mode = mode
		scene.add_child(b)
		scene.move_child(b, bbc_index)
	if extra.is_valid():
		extra.call(b)
	return b

# Screen spots (in the 640x360 picture), chosen inside each zone: A only, A+B, B only, B+C, C only.
const SPOTS := {"A_only": Vector2(95, 120), "A_B": Vector2(145, 170), "B_only": Vector2(170, 220), "B_C": Vector2(195, 170), "C_only": Vector2(245, 150)}

func classify(c: Color) -> String:
	var refs := [CLEAR, COL_A, COL_B, COL_C]
	var best := 0
	var bd := 9.0
	for i in range(refs.size()):
		var d: float = (Vector3(c.r, c.g, c.b) - Vector3(refs[i].r, refs[i].g, refs[i].b)).length()
		if d < bd:
			bd = d
			best = i
	return NAMES[best] if bd < 0.03 else "other(%.3f,%.3f,%.3f)" % [c.r, c.g, c.b]

func read_case(id: String, extra: Dictionary = {}) -> void:
	await frames(4)
	var img := grab()
	var seen := {}
	var main := {}
	for k in SPOTS:
		var p: Vector2 = SPOTS[k]
		var pp := Vector2(420 + p.x / 640.0 * 192.0, 20 + p.y / 360.0 * 108.0)
		seen[k] = classify(img.get_pixel(int(pp.x), int(pp.y)))
		main[k] = classify(img.get_pixel(int(p.x), int(p.y)))
	var d := {"shader_sees": seen, "main_picture": main, "renderer": RenderingServer.get_current_rendering_method()}
	d.merge(extra)
	out(id, d)

func run() -> void:
	RenderingServer.set_default_clear_color(CLEAR)
	root.size = Vector2i(640, 360)
	await frames(3)
	var img0 := grab()
	out("env", {"engine": Engine.get_version_info()["string"], "image_size": [img0.get_width(), img0.get_height()], "adapter": RenderingServer.get_video_adapter_name(), "renderer": RenderingServer.get_current_rendering_method()})

	# 1. no BackBufferCopy: the preview is the first node to read the screen, so Godot copies the screen just before drawing it.
	await build(-1, 2)
	await read_case("A1-no-backbuffercopy")
	# 2..5. viewport-mode BackBufferCopy at each tree position (move_child index among A B C Preview: 3 after C, 2 between B and C, 1 between A and B, 0 first).
	await build(3, BackBufferCopy.COPY_MODE_VIEWPORT)
	await read_case("A2-copy-after-C-viewport", {"tree": "A B C copy Preview"})
	await build(2, BackBufferCopy.COPY_MODE_VIEWPORT)
	await read_case("A3-copy-between-B-and-C-viewport", {"tree": "A B copy C Preview"})
	await build(1, BackBufferCopy.COPY_MODE_VIEWPORT)
	await read_case("A4-copy-between-A-and-B-viewport", {"tree": "A copy B C Preview"})
	await build(0, BackBufferCopy.COPY_MODE_VIEWPORT)
	await read_case("A5-copy-before-A-viewport", {"tree": "copy A B C Preview"})
	await build(4, BackBufferCopy.COPY_MODE_VIEWPORT)
	await read_case("A2b-copy-AFTER-the-preview-viewport", {"tree": "A B C Preview copy"})
	# 6. a DISABLED BackBufferCopy does not count (docs: automatic copy happens when 'no BackBufferCopy (not disabled)' came before).
	await build(1, BackBufferCopy.COPY_MODE_DISABLED)
	await read_case("A6-copy-between-A-and-B-DISABLED", {"tree": "A copy(disabled) B C Preview"})
	# 7. live move: same scene, move_child at runtime (the script the capture would use).
	var b: BackBufferCopy = await build(3, BackBufferCopy.COPY_MODE_VIEWPORT)
	for idx in [3, 2, 1, 0, 4]:
		scene.move_child(b, idx)
		await read_case("A7-move_child-to-%d" % idx, {"index_after_move": idx})
	quit(0)
