extends SceneTree
# Experiment H (Reflections layout): where does a rect-mode BackBufferCopy actually copy?
# Docs: rect "The area covered by the BackBufferCopy. Only used if copy_mode is COPY_MODE_RECT." Default Rect2(-100, -100, 200, 200).
# Test: window (shows the whole screen texture) + a full-screen stripe pattern drawn BEFORE the copy; for several node positions and
# rects, find which screen pixels the window shows as copied (not black). Fresh process, so uncopied = black.
# Each case runs in its OWN process when started with --case Hn (history would otherwise leak between cases: later cases show the union of
# earlier regions). Without --case it runs them one after another in one process (the first is clean, the rest are unions).
# Run: godot --path <scratch project> [--rendering-method gl_compatibility] --script res://exp_h_rect_region.gd -- --case H3
const P = preload("res://pond_common.gd")
const SHADERS := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/lab-shaders/"

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(1280, 720)
	await frames(3)
	var scene := Node2D.new()
	root.add_child(scene)
	var base := ColorRect.new()
	base.size = Vector2(1280, 720)
	base.color = Color("#5FA391")
	scene.add_child(base)
	var bbc := BackBufferCopy.new()
	bbc.copy_mode = BackBufferCopy.COPY_MODE_RECT
	scene.add_child(bbc)
	var pv := ColorRect.new()
	pv.position = Vector2(760, 40)
	pv.size = Vector2(480, 270)
	pv.material = P.load_shader("01-screen-preview.gdshader", SHADERS)
	scene.add_child(pv)
	var all_cases := [
		{"id": "H1", "pos": Vector2(0, 0), "rect": Rect2(-100, -100, 200, 200)},
		{"id": "H2", "pos": Vector2(100, 100), "rect": Rect2(-100, -100, 200, 200)},
		{"id": "H3", "pos": Vector2(500, 300), "rect": Rect2(-100, -100, 200, 200)},
		{"id": "H4", "pos": Vector2(500, 300), "rect": Rect2(0, 0, 300, 200)},
		{"id": "H5", "pos": Vector2(500, 300), "rect": Rect2(-100, -100, 200, 200), "scale": Vector2(2, 2)},
		{"id": "H6", "pos": Vector2(0, 0), "rect": Rect2(0, 0, 200, 200), "parent_pos": Vector2(200, 200)},
		{"id": "H7", "pos": Vector2(0, 0), "rect": Rect2(300, 300, 200, 200)},
		{"id": "H8", "pos": Vector2(500, 300), "rect": Rect2(-100, -100, 200, 200), "rotation": 0.5},
	]
	var want := ""
	var ua := OS.get_cmdline_user_args()
	if ua.size() >= 2 and ua[0] == "--case":
		want = ua[1]
	var cases := []
	for c in all_cases:
		if want == "" or c["id"] == want:
			cases.append(c)
	var first := true
	for c in cases:
		if c.has("parent_pos"):
			scene.remove_child(bbc)
			var holder := Node2D.new()
			holder.position = c["parent_pos"]
			scene.add_child(holder)
			scene.move_child(holder, bbc.get_index() if bbc.get_parent() == scene else 1)
			holder.add_child(bbc)
		bbc.position = c["pos"]
		bbc.rect = c["rect"]
		bbc.scale = c.get("scale", Vector2.ONE)
		bbc.rotation = c.get("rotation", 0.0)
		await frames(4)
		var img := grab()
		# in the window, find the bounding box of non-black pixels, convert back to screen coordinates (window scale 480/1280 = 0.375)
		var x0 := 9999
		var y0 := 9999
		var x1 := -1
		var y1 := -1
		for y in range(40, 310):
			for x in range(760, 1240):
				var p := img.get_pixel(x, y)
				if p.r + p.g + p.b > 0.05:
					x0 = mini(x0, x)
					y0 = mini(y0, y)
					x1 = maxi(x1, x)
					y1 = maxi(y1, y)
		var box := []
		if x1 >= 0:
			box = [snappedf((x0 - 760) / 0.375, 1.0), snappedf((y0 - 40) / 0.375, 1.0), snappedf((x1 + 1 - 760) / 0.375, 1.0), snappedf((y1 + 1 - 40) / 0.375, 1.0)]
		print("RESULT " + JSON.stringify({"case": c["id"], "node_position": [c["pos"].x, c["pos"].y], "rect": [c["rect"].position.x, c["rect"].position.y, c["rect"].size.x, c["rect"].size.y],
			"copied_region_on_screen_x0_y0_x1_y1": box, "scale": [c.get("scale", Vector2.ONE).x, c.get("scale", Vector2.ONE).y], "rotation": c.get("rotation", 0.0), "parent_pos": [c.get("parent_pos", Vector2.ZERO).x, c.get("parent_pos", Vector2.ZERO).y], "fresh_process": want != "", "renderer": RenderingServer.get_current_rendering_method()}))
	quit(0)
