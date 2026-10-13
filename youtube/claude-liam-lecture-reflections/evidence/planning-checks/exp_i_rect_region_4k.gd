extends SceneTree
# Experiment I (Reflections layout): experiment H again on the 4K capture route.
# The film's Godot captures are rendered into a 3840 x 2160 SubViewport over a 1280 x 720 canvas (size_2d_override + stretch, scale 3).
# Shaders that read only SCREEN_UV do not care. But a BackBufferCopy in Rect mode has a box measured in pixels, so: is the default box
# 100 canvas units (300 render pixels) or 100 render pixels (33 canvas units) on this route? Same scene and cases as exp_h_rect_region.gd.
# Each case runs in its OWN process (--case Ix) because the back buffer keeps history inside one process.
# Run: godot --path <scratch project> [--rendering-method gl_compatibility] --script res://exp_i_rect_region_4k.gd -- --case I1
const P = preload("res://pond_common.gd")
const SHADERS := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/lab-shaders/"
const K := 3          # render pixels per canvas unit on the 4K route

var sv: SubViewport

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return sv.get_texture().get_image()

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(1280, 720)
	sv = SubViewport.new()
	sv.size = Vector2i(3840, 2160)
	sv.size_2d_override = Vector2i(1280, 720)
	sv.size_2d_override_stretch = true
	sv.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sv)
	await frames(3)
	var scene := Node2D.new()
	sv.add_child(scene)
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
		{"id": "I1", "pos": Vector2(0, 0), "rect": Rect2(-100, -100, 200, 200)},
		{"id": "I3", "pos": Vector2(500, 300), "rect": Rect2(-100, -100, 200, 200)},
		{"id": "I4", "pos": Vector2(500, 300), "rect": Rect2(0, 0, 300, 200)},
		{"id": "I7", "pos": Vector2(0, 0), "rect": Rect2(300, 300, 200, 200)},
	]
	var want := ""
	var ua := OS.get_cmdline_user_args()
	if ua.size() >= 2 and ua[0] == "--case":
		want = ua[1]
	for c in all_cases:
		if want != "" and c["id"] != want:
			continue
		bbc.position = c["pos"]
		bbc.rect = c["rect"]
		await frames(4)
		var img := grab()
		# the window sits at canvas (760, 40), 480 x 270, and shows the whole screen texture: window fraction f = screen fraction
		var x0 := 99999
		var y0 := 99999
		var x1 := -1
		var y1 := -1
		for y in range(40 * K, 310 * K):
			for x in range(760 * K, 1240 * K):
				var p := img.get_pixel(x, y)
				if p.r + p.g + p.b > 0.05:
					x0 = mini(x0, x)
					y0 = mini(y0, y)
					x1 = maxi(x1, x)
					y1 = maxi(y1, y)
		var canvas := []
		var render_px := []
		if x1 >= 0:
			# window pixel -> screen fraction -> canvas units (x 1280, y 720)
			var fx0 := float(x0 - 760 * K) / (480.0 * K) * 1280.0
			var fy0 := float(y0 - 40 * K) / (270.0 * K) * 720.0
			var fx1 := float(x1 + 1 - 760 * K) / (480.0 * K) * 1280.0
			var fy1 := float(y1 + 1 - 40 * K) / (270.0 * K) * 720.0
			canvas = [snappedf(fx0, 1.0), snappedf(fy0, 1.0), snappedf(fx1, 1.0), snappedf(fy1, 1.0)]
			render_px = [snappedf(fx0 * K, 1.0), snappedf(fy0 * K, 1.0), snappedf(fx1 * K, 1.0), snappedf(fy1 * K, 1.0)]
		print("RESULT " + JSON.stringify({"case": c["id"], "node_position": [c["pos"].x, c["pos"].y], "rect": [c["rect"].position.x, c["rect"].position.y, c["rect"].size.x, c["rect"].size.y],
			"copied_region_canvas_units_x0_y0_x1_y1": canvas, "same_region_in_render_pixels": render_px, "route": "SubViewport 3840x2160 over 1280x720", "fresh_process": want != "", "renderer": RenderingServer.get_current_rendering_method()}))
	quit(0)
