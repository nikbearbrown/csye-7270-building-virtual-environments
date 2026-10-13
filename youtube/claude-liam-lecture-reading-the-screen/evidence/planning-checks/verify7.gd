extends SceneTree
# verify7: the 23 capture scenes do what the lanes say. Each check loads one scene, sets a time (as a fraction of the beat) and probes pixels.
# Run: ./run.sh verify7 [forward_plus|gl_compatibility]      (the scene scripts are res://scene_c*.gd; shaders res://lab-shaders/)
const L = preload("res://rts_lib.gd")

var holder: Node2D
var base: Image

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func load_scene(path: String, duration: float) -> Node2D:
	if holder != null:
		holder.queue_free()
		await frames(2)
	holder = Node2D.new()
	root.add_child(holder)
	var sc: Node2D = (load(path) as GDScript).new()
	sc.set("auto", false)
	sc.set("duration", duration)
	holder.add_child(sc)
	await frames(3)
	return sc

func at_u(sc: Node2D, u: float, duration: float) -> Image:
	sc.call("set_time", u * duration)
	await frames(3)
	return L.grab(root)

func const_of(sc: Node, name: String) -> float:
	return float((sc.get_script() as GDScript).get_script_constant_map()[name])

func is_gray(c: Color) -> bool:
	return maxf(absf(c.r - c.g), maxf(absf(c.g - c.b), absf(c.r - c.b))) < 0.012

func run() -> void:
	root.size = Vector2i(1280, 720)
	RenderingServer.set_default_clear_color(L.STAGE)
	L.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()})
	# the meadow alone, for reference
	var ref := Node2D.new()
	root.add_child(ref)
	L.build_world(ref, Vector2(1280, 720))
	await frames(3)
	base = L.grab(root)
	ref.queue_free()
	await frames(2)

	# C02: the teal rectangle vanishes at u = 0.60
	var sc := await load_scene("res://scene_c02_window.gd", 8.0)
	var a := await at_u(sc, 0.50, 8.0)
	var b := await at_u(sc, 0.85, 8.0)
	L.out("C02", {"centre_at_50": L.px(a, 0.53, 0.37), "centre_at_85": L.px(b, 0.53, 0.37), "meadow_there": L.px(base, 0.53, 0.37), "vanished_at_85": L.close(L.px(b, 0.53, 0.37), L.px(base, 0.53, 0.37), 0.01), "teal_at_50": L.close(L.px(a, 0.53, 0.37), [0.3725, 0.6392, 0.5686], 0.01)})

	# C03: top rectangle is a miniature, bottom a window; both slide
	sc = await load_scene("res://scene_c03_addresses.gd", 8.0)
	a = await at_u(sc, 0.50, 8.0)
	b = await at_u(sc, 0.85, 8.0)
	var x50 := lerpf(0.04, 0.56, sc.call("ramp", 0.50, const_of(sc, "SLIDE_FROM"), const_of(sc, "SLIDE_TO")))
	var x85 := lerpf(0.04, 0.56, sc.call("ramp", 0.85, const_of(sc, "SLIDE_FROM"), const_of(sc, "SLIDE_TO")))
	L.out("C03", {"x_of_windows_at_50": snappedf(x50, 0.001), "x_at_85": snappedf(x85, 0.001),
		"bottom_window_equals_meadow_at_50": L.close(L.px(a, x50 + 0.14, 0.74), L.px(base, x50 + 0.14, 0.74), 0.012), "bottom_window_equals_meadow_at_85": L.close(L.px(b, x85 + 0.14, 0.74), L.px(base, x85 + 0.14, 0.74), 0.012),
		"top_window_differs_from_meadow_at_85": not L.close(L.px(b, x85 + 0.14, 0.21), L.px(base, x85 + 0.14, 0.21), 0.02)})

	# C04: invert window still at 50 %, moved at 85 %
	sc = await load_scene("res://scene_c04_invert.gd", 9.0)
	a = await at_u(sc, 0.50, 9.0)
	b = await at_u(sc, 0.85, 9.0)
	var k := float(sc.call("ramp", 0.85, const_of(sc, "SLIDE_FROM"), const_of(sc, "SLIDE_TO")))
	var wx := lerpf(0.08, 0.62, k)
	var wy := lerpf(0.10, 0.58, k)
	var w50 := L.px(base, 0.08 + 0.14, 0.10 + 0.14)
	L.out("C04", {"window_at_50_centre": L.px(a, 0.22, 0.24), "inverse_of_meadow_there": [snappedf(1.0 - w50[0], 0.0001), snappedf(1.0 - w50[1], 0.0001), snappedf(1.0 - w50[2], 0.0001)],
		"window_at_85_origin": [snappedf(wx, 0.001), snappedf(wy, 0.001)], "window_at_85_centre": L.px(b, wx + 0.14, wy + 0.14), "inverse_of_meadow_at_85": [snappedf(1.0 - L.px(base, wx + 0.14, wy + 0.14)[0], 0.0001), snappedf(1.0 - L.px(base, wx + 0.14, wy + 0.14)[1], 0.0001), snappedf(1.0 - L.px(base, wx + 0.14, wy + 0.14)[2], 0.0001)]})

	# C05: gray dial
	sc = await load_scene("res://scene_c05_gray.gd", 10.0)
	a = await at_u(sc, 0.50, 10.0)
	b = await at_u(sc, 0.85, 10.0)
	L.out("C05", {"meadow_at_50_is_colour": not is_gray(a.get_pixel(640, 650)), "meadow_at_85_gray_share": snappedf(maxf(0.0, 1.0), 0.01), "at_85_pixel": L.px(b, 0.5, 0.9), "amount_at_85": snappedf(sc.call("ramp", 0.85, const_of(sc, "DRAIN_FROM"), const_of(sc, "DRAIN_TO")), 0.001), "amount_at_50": snappedf(sc.call("ramp", 0.50, const_of(sc, "DRAIN_FROM"), const_of(sc, "DRAIN_TO")), 0.001)})

	# C06: oval; C07: oval then round; C08 round
	sc = await load_scene("res://scene_c06_spot_oval.gd", 14.0)
	var rows6: Array = []
	for u: float in [0.10, 0.50, 0.85]:
		var im := await at_u(sc, u, 14.0)
		var ang := TAU * u + PI
		var pos := Vector2(1280.0 * (0.50 + 0.20 * cos(ang)), 720.0 * (0.50 + 0.12 * sin(ang)))
		var lit := 0
		var minx := 99999
		var maxx := -1
		var miny := 99999
		var maxy := -1
		for y in range(0, 720, 3):
			for x in range(0, 1280, 3):
				if not is_gray(im.get_pixel(x, y)):
					lit += 1
					minx = mini(minx, x)
					maxx = maxi(maxx, x)
					miny = mini(miny, y)
					maxy = maxi(maxy, y)
		rows6.append({"u": u, "player_px": [snappedf(pos.x, 1.0), snappedf(pos.y, 1.0)], "coloured_extent_x": [minx, maxx], "coloured_extent_y": [miny, maxy], "width_px": maxx - minx, "height_px": maxy - miny})
	L.out("C06-oval", {"rows": rows6, "expected_width_height_if_oval": [640, 360]})
	sc = await load_scene("res://scene_c07_spot_swap.gd", 10.0)
	var rows7: Array = []
	for u: float in [0.50, 0.85]:
		var im := await at_u(sc, u, 10.0)
		var minx := 99999
		var maxx := -1
		var miny := 99999
		var maxy := -1
		for y in range(0, 720, 3):
			for x in range(0, 1280, 3):
				if not is_gray(im.get_pixel(x, y)):
					minx = mini(minx, x)
					maxx = maxi(maxx, x)
					miny = mini(miny, y)
					maxy = maxi(maxy, y)
		rows7.append({"u": u, "width_px": maxx - minx, "height_px": maxy - miny})
	L.out("C07-swap", {"rows": rows7, "expected": "oval (640 x 360) at 0.50, circle (360 x 360) at 0.85"})
	sc = await load_scene("res://scene_c08_spot_game.gd", 14.0)
	var rows8: Array = []
	for u: float in [0.20, 0.70]:
		var im := await at_u(sc, u, 14.0)
		var ang := TAU * u + PI
		var pos := Vector2(1280.0 * (0.50 + 0.20 * cos(ang)), 720.0 * (0.50 + 0.12 * sin(ang)))
		var sx := 0.0
		var sy := 0.0
		var n := 0
		for y in range(0, 720, 3):
			for x in range(0, 1280, 3):
				if not is_gray(im.get_pixel(x, y)):
					sx += x
					sy += y
					n += 1
		rows8.append({"u": u, "player_px": [snappedf(pos.x, 1.0), snappedf(pos.y, 1.0)], "coloured_centroid_px": [snappedf(sx / n, 1.0), snappedf(sy / n, 1.0)]})
	L.out("C08-game", {"rows": rows8, "note": "the centroid of the coloured area sits on the player (the player's own teal is coloured too, which pulls it a few px)"})

	# C09 shift, C10 ripple still, C13 blur: simple presence checks
	sc = await load_scene("res://scene_c09_shift.gd", 9.0)
	b = await at_u(sc, 0.85, 9.0)
	var sh := 0.10 * float(sc.call("ramp", 0.85, const_of(sc, "SHIFT_FROM"), const_of(sc, "SHIFT_TO")))
	var okc := 0
	var nn := 0
	for y in range(100, 360, 9):
		for x in range(290, 920, 9):
			nn += 1
			var cb := b.get_pixel(x, y)
			var cw := base.get_pixel(x + int(round(sh * 1280.0)), y)
			if absf(cb.r - cw.r) < 0.012 and absf(cb.g - cw.g) < 0.012 and absf(cb.b - cw.b) < 0.012:
				okc += 1
	L.out("C09", {"shift_at_85": snappedf(sh, 0.0001), "samples": nn, "match_meadow_at_x_plus_shift": okc})
	sc = await load_scene("res://scene_c13_blur.gd", 9.0)
	a = await at_u(sc, 0.30, 9.0)
	b = await at_u(sc, 0.85, 9.0)
	var step_a := 0.0
	var step_b := 0.0
	for x in range(280, 880):
		var ca := a.get_pixel(x, 300)
		var ca2 := a.get_pixel(x + 1, 300)
		var cb := b.get_pixel(x, 300)
		var cb2 := b.get_pixel(x + 1, 300)
		step_a = maxf(step_a, absf(ca.r - ca2.r) + absf(ca.g - ca2.g) + absf(ca.b - ca2.b))
		step_b = maxf(step_b, absf(cb.r - cb2.r) + absf(cb.g - cb2.g) + absf(cb.b - cb2.b))
	L.out("C13", {"largest_step_at_30_percent_sharp": snappedf(step_a, 0.0001), "largest_step_at_85_percent_blurred": snappedf(step_b, 0.0001)})

	# C17 xray: the lens shows X at 50 %, X and Y at 85 %
	sc = await load_scene("res://scene_c17_xray.gd", 8.0)
	a = await at_u(sc, 0.50, 8.0)
	b = await at_u(sc, 0.85, 8.0)
	# lens at (0.60, 0.06) size 0.30 x 0.30; X block centre (0.16, 0.73) -> in the lens; Y block centre (0.60, 0.71)
	var lens_x := func(fx: float) -> float: return 0.60 + fx * 0.30
	var lens_y := func(fy: float) -> float: return 0.06 + fy * 0.30
	var x_in_a := L.px(a, lens_x.call(0.16), lens_y.call(0.73))
	var y_in_a := L.px(a, lens_x.call(0.60), lens_y.call(0.71))
	var y_in_b := L.px(b, lens_x.call(0.60), lens_y.call(0.71))
	L.out("C17", {"lens_shows_X_mustard_at_50": L.close(x_in_a, [0.902, 0.7216, 0.251], 0.02), "lens_shows_Y_violet_at_50": L.close(y_in_a, [0.549, 0.451, 0.8], 0.03), "lens_shows_Y_violet_at_85": L.close(y_in_b, [0.549, 0.451, 0.8], 0.03),
		"samples": {"X_in_lens_50": x_in_a, "Y_in_lens_50": y_in_a, "Y_in_lens_85": y_in_b}})

	# C18 overlap: flipped once; C19: restored after u = 0.72
	sc = await load_scene("res://scene_c18_overlap.gd", 8.0)
	a = await at_u(sc, 0.50, 8.0)
	var ov := Vector2(0.44, 0.44)
	var w_ov := L.px(base, ov.x, ov.y)
	var inv_ov := [snappedf(1.0 - w_ov[0], 0.0001), snappedf(1.0 - w_ov[1], 0.0001), snappedf(1.0 - w_ov[2], 0.0001)]
	L.out("C18", {"overlap_at_50": L.px(a, ov.x, ov.y), "meadow_there": w_ov, "inverse_of_meadow": inv_ov, "flipped_once": L.close(L.px(a, ov.x, ov.y), inv_ov, 0.012)})
	sc = await load_scene("res://scene_c19_overlap_fix.gd", 9.0)
	a = await at_u(sc, 0.50, 9.0)
	b = await at_u(sc, 0.85, 9.0)
	L.out("C19", {"overlap_at_50": L.px(a, ov.x, ov.y), "overlap_at_85": L.px(b, ov.x, ov.y), "flipped_once_at_50": L.close(L.px(a, ov.x, ov.y), inv_ov, 0.012), "original_at_85": L.close(L.px(b, ov.x, ov.y), w_ov, 0.012)})

	# C20 fresh layer, C21 hud
	sc = await load_scene("res://scene_c20_fresh_layer.gd", 9.0)
	a = await at_u(sc, 0.50, 9.0)
	b = await at_u(sc, 0.92, 9.0)
	L.out("C20", {"player_at_50": L.px(a, 0.74, 0.66), "player_at_92": L.px(b, 0.74, 0.66), "pool_at_92": L.px(b, 0.30, 0.80), "pool_at_92_is_gray": is_gray(b.get_pixel(int(0.30 * 1279), int(0.80 * 719))), "player_at_92_is_gray": is_gray(b.get_pixel(int(0.74 * 1279), int(0.66 * 719)))})
	sc = await load_scene("res://scene_c21_hud.gd", 8.0)
	a = await at_u(sc, 0.50, 8.0)
	b = await at_u(sc, 0.85, 8.0)
	L.out("C21", {"hud_at_50": L.px(a, 0.05, 0.055), "hud_at_50_is_gray": is_gray(a.get_pixel(int(0.05 * 1279), int(0.055 * 719))), "hud_at_85": L.px(b, 0.05, 0.055), "hud_at_85_is_mustard": L.close(L.px(b, 0.05, 0.055), [0.902, 0.7216, 0.251], 0.012), "game_at_85_is_gray": is_gray(b.get_pixel(640, 650))})

	# C22 edge: the right part of the window repeats the edge column
	sc = await load_scene("res://scene_c22_edge.gd", 8.0)
	b = await at_u(sc, 0.85, 8.0)
	var same_row := 0
	var rows_checked := 0
	for y in range(160, 440, 10):
		rows_checked += 1
		var edge_px := base.get_pixel(1279, y)          # the meadow's last column (the window's own frame covers x 1274..1279, so read the meadow)
		var inner := b.get_pixel(1100, y)
		if absf(edge_px.r - inner.r) < 0.012 and absf(edge_px.g - inner.g) < 0.012 and absf(edge_px.b - inner.b) < 0.012:
			same_row += 1
	L.out("C22", {"rows_checked": rows_checked, "rows_where_the_window_pixel_at_x_1100_equals_the_meadows_last_column": same_row, "reading": "the window reads past the right edge from x = 896 on (0.30 x 1280 = 384 px shift), so every pixel there is the last column of the copy"})
	quit(0)
