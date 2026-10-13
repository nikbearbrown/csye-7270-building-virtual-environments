extends SceneTree
# SubViewports film, check 9: the 4K capture route with the film's own SubViewports INSIDE the harness's 4K SubViewport.
# The harness renders a 1280 x 720 logical canvas into a 3840 x 2160 SubViewport (size_2d_override + stretch). Every capture scene of this film holds its own
# SubViewport (the picture), so the pictures are NESTED. Questions:
#  N1  does a nested picture appear in the 4K frame, in the same frame (no lag)?  Scene c04b slides a sprite at a known speed; the picture's position in the 4K frame
#      is compared with where the scene says the sprite is at frame f, and at frame f-1.
#  N2  does shader TIME advance 1/30 s per rendered frame in this route?
# Run: godot --path <project> --fixed-fps 30 --script res://verify9_nested_4k.gd

func _initialize() -> void: call_deferred("run")

func first_teal_x(image: Image, y: int) -> int:
	for x in image.get_width():
		var c := image.get_pixel(x, y)
		if Common.diff(c, Common.TEAL) < 0.03:
			return x
	return -1

func run() -> void:
	root.size = Vector2i(640, 360)
	Common.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	var outer := SubViewport.new()
	outer.size = Vector2i(3840, 2160)
	outer.size_2d_override = Vector2i(1280, 720)
	outer.size_2d_override_stretch = true
	outer.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(outer)
	var shown := Sprite2D.new()
	shown.texture = outer.get_texture()
	shown.scale = Vector2(0.1, 0.1)
	root.add_child(shown)
	var canvas := Node2D.new()
	outer.add_child(canvas)
	var sc := CaptureScene.new("c04b")
	sc.build(canvas)
	var tprobe := ColorRect.new()
	tprobe.size = Vector2(12, 12)
	tprobe.material = Common.material_from_code(Common.TIME_PROBE_CODE)
	canvas.add_child(tprobe)
	var rows: Array = []
	var times: Array = []
	for f in range(0, 136):
		sc.update(float(f) / 30.0)
		await process_frame
		RenderingServer.force_draw(false)   # one real draw per logical frame
		if f in [60, 75, 90, 105, 120, 135]:
			var image := outer.get_texture().get_image()
			var t := float(f) / 30.0
			var sprite_x: float = (sc.n["blob"] as Sprite2D).position.x
			# the picture's top-left on the logical canvas is (384, 104); the blob's left edge in picture px = sprite_x - 0.30 * 448 (clipped at 0)
			var left_logical := 384.0 + maxf(sprite_x - 134.4, 0.0)
			var y4k := int((104.0 + sprite_x) * 3.0)
			var expected_now := int(round(left_logical * 3.0))
			rows.append({"frame": f, "t": snappedf(t, 0.001), "sprite_x_in_the_scene": snappedf(sprite_x, 0.1), "measured_left_edge_in_the_4K_frame": first_teal_x(image, int((104.0 + sprite_x) * 3.0)), "expected_for_this_frame": expected_now, "TIME_read": snappedf(Common.time_of(image, 5 * 3, 5 * 3), 0.001)})
	Common.out("N1-N2-nested-in-the-4k-route", {"rows": rows, "reading": "measured left edge = expected for the same frame (no lag; 4K pixels = 3 x logical); a one-frame lag would put it about 3 x 3.8 px behind while the sprite slides (frames 60 to 120). TIME_read rises about 0.0333 per frame."})
	quit(0)
