extends SceneTree
# Experiment B (Reflections layout): copy modes, and what a SECOND node that reads the screen sees.
#
# B1..B4  copy modes: a BackBufferCopy right after sprite C (so the snapshot should hold A, B and C) in each mode.
#         Rect mode is tried with the node's DEFAULT rect (-100,-100,200,200) at two positions, then with a rect that covers the screen.
#         INCONCLUSIVE BY DESIGN: all cases run in one process, so the back buffer still holds the earlier cases' pixels (the docs' "garbage from previous
#         frames") and a rect that copies almost nothing still looks right. exp_b2, exp_c4 and exp_h repeat it in fresh processes.
# B5..B6  two screen readers: Preview1 sits between B and C, Preview2 after C. Docs: the second reader does not get a fresh copy.
#         Then the same with a BackBufferCopy between C and Preview2.
#
# Run: godot --path <scratch project> --script res://exp_b_modes_and_second_reader.gd [-- --compat is passed to godot as --rendering-method]
# Output: one RESULT line per case; 'shader_sees' lists what the preview shows at five spots (see exp_a_copy_order.gd).

const SHADERS := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/lab-shaders/"
const CLEAR := Color("#D9D5CA")
const COL_A := Color("#4F8F7E")
const COL_B := Color("#7FA7C9")
const COL_C := Color("#B7A6D9")
const NAMES := ["clear", "A", "B", "C"]
const SPOTS := {"A_only": Vector2(95, 120), "A_B": Vector2(145, 170), "B_only": Vector2(170, 220), "B_C": Vector2(195, 170), "C_only": Vector2(245, 150)}

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
	r.size = Vector2(192, 108)
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(SHADERS + "01-screen-preview.gdshader")
	var mat := ShaderMaterial.new()
	mat.shader = sh
	r.material = mat
	return r

func fresh() -> void:
	if scene != null:
		scene.queue_free()
		await process_frame
	scene = Node2D.new()
	root.add_child(scene)
	scene.add_child(sprite("A", COL_A, Vector2(120, 150)))
	scene.add_child(sprite("B", COL_B, Vector2(170, 190)))

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

func read_preview(img: Image, origin: Vector2) -> Dictionary:
	var seen := {}
	for k in SPOTS:
		var p: Vector2 = SPOTS[k]
		var pp := Vector2(origin.x + p.x / 640.0 * 192.0, origin.y + p.y / 360.0 * 108.0)
		seen[k] = classify(img.get_pixel(int(pp.x), int(pp.y)))
	return seen

func case_single(id: String, mode: int, pos: Vector2, rect: Rect2, use_rect: bool) -> void:
	await fresh()
	scene.add_child(sprite("C", COL_C, Vector2(220, 150)))
	var b := BackBufferCopy.new()
	b.name = "BackBufferCopy"
	b.copy_mode = mode
	b.position = pos
	if use_rect:
		b.rect = rect
	scene.add_child(b)
	scene.add_child(preview("Preview", Vector2(420, 20)))
	await frames(4)
	var img := grab()
	out(id, {"mode": mode, "node_position": [pos.x, pos.y], "rect": [b.rect.position.x, b.rect.position.y, b.rect.size.x, b.rect.size.y],
		"shader_sees": read_preview(img, Vector2(420, 20)), "renderer": RenderingServer.get_current_rendering_method()})

func run() -> void:
	RenderingServer.set_default_clear_color(CLEAR)
	root.size = Vector2i(640, 360)
	await frames(3)
	# default node values, for the record
	var probe_b := BackBufferCopy.new()
	out("defaults", {"copy_mode": probe_b.copy_mode, "rect": [probe_b.rect.position.x, probe_b.rect.position.y, probe_b.rect.size.x, probe_b.rect.size.y]})
	probe_b.free()

	await case_single("B1-viewport", BackBufferCopy.COPY_MODE_VIEWPORT, Vector2.ZERO, Rect2(), false)
	await case_single("B2-rect-default-node-at-origin-(INCONCLUSIVE-here-stale-pixels-from-earlier-cases)", BackBufferCopy.COPY_MODE_RECT, Vector2.ZERO, Rect2(), false)
	await case_single("B3-rect-default-node-moved-to-170-170-(position-has-no-effect-see-exp_h)", BackBufferCopy.COPY_MODE_RECT, Vector2(170, 170), Rect2(), false)
	await case_single("B4-rect-covering-the-screen", BackBufferCopy.COPY_MODE_RECT, Vector2.ZERO, Rect2(0, 0, 640, 360), true)
	await case_single("B4b-disabled", BackBufferCopy.COPY_MODE_DISABLED, Vector2.ZERO, Rect2(), false)

	# B5: two readers. Preview1 (top right) between B and C. Preview2 (below it) after C. No BackBufferCopy at all.
	await fresh()
	scene.add_child(preview("Preview1", Vector2(420, 20)))
	scene.add_child(sprite("C", COL_C, Vector2(220, 150)))
	scene.add_child(preview("Preview2", Vector2(420, 190)))
	await frames(4)
	var img5 := grab()
	out("B5-two-readers-no-copy-node", {"preview1_between_B_and_C": read_preview(img5, Vector2(420, 20)), "preview2_after_C": read_preview(img5, Vector2(420, 190)),
		"renderer": RenderingServer.get_current_rendering_method()})

	# B6: same, with a BackBufferCopy between C and Preview2.
	await fresh()
	scene.add_child(preview("Preview1", Vector2(420, 20)))
	scene.add_child(sprite("C", COL_C, Vector2(220, 150)))
	var b6 := BackBufferCopy.new()
	b6.copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT
	scene.add_child(b6)
	scene.add_child(preview("Preview2", Vector2(420, 190)))
	await frames(4)
	var img6 := grab()
	out("B6-two-readers-with-a-copy-between", {"preview1_between_B_and_C": read_preview(img6, Vector2(420, 20)), "preview2_after_copy": read_preview(img6, Vector2(420, 190)),
		"renderer": RenderingServer.get_current_rendering_method()})
	quit(0)
