extends SceneTree
# verify4: bending what is behind (Act III) and the hints, checked in a real window of Godot 4.7.2.
#  L1 08-shift: a pixel shows the world a little further along (address + shift)
#  L2 09-ripple-still: each row is pushed by amount * sin(60 * y): measured against a known vertical edge
#  L3 ripples with TIME change between frames
#  L4 11-water: mix(behind, water, 0.5) -> the tint, and what source_color does to the default value
#  L5 12-pool: the top edge is discarded in a wave; the world shows there
#  L6 13-ripple-ride (UV.y) vs 09-ripple-still (SCREEN_UV.y): move the node down; does the ripple move with it?
#  L7 hints: default vs repeat_disable vs repeat_enable at the screen edge; default vs filter_nearest vs filter_linear when magnified
#  L8 15-blur: mipmap filter + textureLod; without a mipmap filter a higher level looks like level 0
#  L9 a full-screen filter on layer 1 sees a pool and a player on layer 0 (no BackBufferCopy needed)
# Run: ./run.sh verify4 [forward_plus|gl_compatibility]
const L = preload("res://rts_lib.gd")
const SIZE := Vector2(1280, 720)

var main: Node2D

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func fresh() -> void:
	if main != null:
		main.queue_free()
	await frames(2)
	main = Node2D.new()
	main.name = "Main"
	root.add_child(main)
	L.build_world(main, SIZE)

func win_rect(pos: Vector2, size: Vector2, shader: String) -> ColorRect:
	var r := L.rect(pos, size, Color.WHITE, "Win")
	r.material = L.mat_file(shader)
	main.add_child(r)
	return r

func set_u(r: ColorRect, name: String, v: Variant) -> void:
	(r.material as ShaderMaterial).set_shader_parameter(name, v)

func run() -> void:
	root.size = Vector2i(1280, 720)
	RenderingServer.set_default_clear_color(L.STAGE)
	L.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()})
	await fresh()
	await frames(3)
	var base := L.grab(root)

	# L1: shift
	var w1 := win_rect(Vector2(0.20 * SIZE.x, 0.10 * SIZE.y), Vector2(0.50 * SIZE.x, 0.40 * SIZE.y), "08-shift.gdshader")
	var l1: Array = []
	for sh in [0.1, -0.05]:
		set_u(w1, "shift", sh)
		await frames(3)
		var img := L.grab(root)
		var ok := 0
		var n := 0
		var dx := int(round(sh * SIZE.x))
		for y in range(int(w1.position.y) + 4, int(w1.position.y + w1.size.y) - 4, 7):
			for x in range(int(w1.position.x) + 4, int(w1.position.x + w1.size.x) - 4, 7):
				var a := img.get_pixel(x, y)
				var b := base.get_pixel(x + dx, y)
				n += 1
				if absf(a.r - b.r) < 0.01 and absf(a.g - b.g) < 0.01 and absf(a.b - b.b) < 0.01:
					ok += 1
		l1.append({"shift": sh, "pixels_shifted": dx, "samples": n, "matching_world_at_x_plus_shift": ok, "share": snappedf(float(ok) / float(n), 0.001)})
		if sh == 0.1:
			img.save_png("/private/tmp/claude-501/rts-checks/shots/l1-shift.png")
	L.out("L1-shift", {"rows": l1})
	w1.queue_free()
	await frames(2)

	# L2: ripple rows. A window over the top strip; find where the tile edge at x = 640 appears in each row.
	var w2 := win_rect(Vector2(0.30 * SIZE.x, 0.02 * SIZE.y), Vector2(0.40 * SIZE.x, 0.20 * SIZE.y), "09-ripple-still.gdshader")
	await frames(4)
	var img2 := L.grab(root)
	img2.save_png("/private/tmp/claude-501/rts-checks/shots/l2-ripple-still.png")
	var rows: Array = []
	for y in range(int(w2.position.y) + 6, int(w2.position.y + w2.size.y) - 6, 14):
		var v := (float(y) + 0.5) / SIZE.y
		var predicted := 560.0 - 0.01 * sin(60.0 * v) * SIZE.x
		# the scan starts at x = 540 (inside tile column 6, x 480..560); the first transition it meets is the world's tile edge at x = 560
		var first := img2.get_pixel(540, y)
		var edge := -1
		for x in range(541, 740):
			var c := img2.get_pixel(x, y)
			if absf(c.r - first.r) + absf(c.g - first.g) + absf(c.b - first.b) > 0.08:
				edge = x
				break
		rows.append({"y": y, "v": snappedf(v, 0.001), "edge_x_measured": edge, "edge_x_predicted_560_minus_0.01_sin(60v)_W": snappedf(predicted, 0.1), "diff": snappedf(float(edge) - predicted, 0.1)})
	L.out("L2-ripple-rows", {"rows": rows})
	w2.queue_free()
	await frames(2)

	# L3: TIME moves the ripples
	var w3 := win_rect(Vector2(0.30 * SIZE.x, 0.02 * SIZE.y), Vector2(0.40 * SIZE.x, 0.20 * SIZE.y), "10-ripple.gdshader")
	await frames(4)
	var a3 := L.grab(root)
	await create_timer(0.4).timeout
	await frames(2)
	var b3 := L.grab(root)
	var diff := 0
	for y in range(int(w3.position.y) + 6, int(w3.position.y + w3.size.y) - 6, 5):
		for x in range(int(w3.position.x) + 6, int(w3.position.x + w3.size.x) - 6, 5):
			var ca := a3.get_pixel(x, y)
			var cb := b3.get_pixel(x, y)
			if absf(ca.r - cb.r) + absf(ca.g - cb.g) + absf(ca.b - cb.b) > 0.05:
				diff += 1
	L.out("L3-ripples-move-with-TIME", {"pixels_that_changed_in_0.4s": diff})
	w3.queue_free()
	await frames(2)

	# L3b: one shared clock. Window A is present from the start; window B is added 1.0 s later. At the same instant both show the same ripple phase on
	# the same screen rows (the shader's wave depends on SCREEN_UV.y and TIME only), so TIME was not restarted for the late node.
	var wa := win_rect(Vector2(0.10 * SIZE.x, 0.08 * SIZE.y), Vector2(0.30 * SIZE.x, 0.20 * SIZE.y), "10-ripple.gdshader")
	await create_timer(1.0).timeout
	var wb := win_rect(Vector2(0.55 * SIZE.x, 0.08 * SIZE.y), Vector2(0.30 * SIZE.x, 0.20 * SIZE.y), "10-ripple.gdshader")
	await frames(3)
	var img3b := L.grab(root)
	var rows3b: Array = []
	for y in [62, 140, 152, 164, 176, 188, 198]:
		var offs: Array = []
		for edge in [320, 800]:
			var first := img3b.get_pixel(edge - 45, y)
			var found := -999
			for x in range(edge - 44, edge + 45):
				var c := img3b.get_pixel(x, y)
				if absf(c.r - first.r) + absf(c.g - first.g) + absf(c.b - first.b) > 0.08:
					found = x - edge
					break
			offs.append(found)
		rows3b.append({"row": y, "edge_offset_px_window_present_from_start": offs[0], "edge_offset_px_window_added_1s_later": offs[1], "same": absi(offs[0] - offs[1]) <= 1})
	L.out("L3b-one-shared-clock", {"rows": rows3b})
	wa.queue_free()
	wb.queue_free()
	await frames(2)

	# L4: tint. amount 0 so the bend does not move anything; the pool pixel must be 0.5 * world + 0.5 * water
	var pool := win_rect(Vector2(0.06 * SIZE.x, 0.52 * SIZE.y), Vector2(0.40 * SIZE.x, 0.40 * SIZE.y), "11-water.gdshader")
	set_u(pool, "amount", 0.0)
	await frames(4)
	var img4 := L.grab(root)
	var rows4: Array = []
	for s in [[0.10, 0.60], [0.30, 0.80], [0.40, 0.88]]:
		var w := L.px(base, s[0], s[1])
		var water := [0.2, 0.5, 0.8]
		var expect := [snappedf(0.5 * w[0] + 0.5 * water[0], 0.0001), snappedf(0.5 * w[1] + 0.5 * water[1], 0.0001), snappedf(0.5 * w[2] + 0.5 * water[2], 0.0001)]
		var got := L.px(img4, s[0], s[1])
		rows4.append({"at": s, "world": w, "expected_half_world_half_default_water": expect, "got": got, "matches": L.close(expect, got, 0.012)})
	L.out("L4-tint-and-source_color-default", {"rows": rows4})
	# the same shader with water_color set the way the Inspector would (a Color) at one third
	set_u(pool, "water", Color(0.2, 0.5, 0.8))
	await frames(3)
	var img4b := L.grab(root)
	L.out("L4b-water_color-set-from-code-as-Color", {"got_at_0.30_0.80": L.px(img4b, 0.30, 0.80), "world": L.px(base, 0.30, 0.80)})
	pool.queue_free()
	await frames(2)

	# L5: pool with a wavy top edge. column scan: where does the pool start (first tinted pixel) at several x?
	var pool2 := win_rect(Vector2(0.06 * SIZE.x, 0.52 * SIZE.y), Vector2(0.40 * SIZE.x, 0.40 * SIZE.y), "12-pool.gdshader")
	await frames(4)
	var img5 := L.grab(root)
	img5.save_png("/private/tmp/claude-501/rts-checks/shots/l5-pool.png")
	var tops: Array = []
	for fx in [0.1, 0.3, 0.5, 0.7, 0.9]:
		var x := int(pool2.position.x + fx * pool2.size.x)
		var first_y := -1
		for y in range(int(pool2.position.y), int(pool2.position.y + pool2.size.y)):
			var c := img5.get_pixel(x, y)
			var w := base.get_pixel(x, y)
			if absf(c.r - w.r) + absf(c.g - w.g) + absf(c.b - w.b) > 0.06:
				first_y = y
				break
		tops.append({"u": fx, "first_changed_row_from_top_px": first_y - int(pool2.position.y), "as_uv_y": snappedf(float(first_y - int(pool2.position.y)) / pool2.size.y, 0.001)})
	L.out("L5-pool-edge", {"rows": tops, "world_above_edge_equals_base": L.close(L.px_abs(img5, int(pool2.position.x) + 40, int(pool2.position.y) + 2), L.px_abs(base, int(pool2.position.x) + 40, int(pool2.position.y) + 2), 0.01)})
	pool2.queue_free()
	await frames(2)

	# L6: ride vs glued. Frozen ripples (no TIME). Move each window down by 100 px; compare the picture inside before and after.
	# 'ride': window at y0 shows ripple pattern P(window-local y). 'glued': window shows P'(screen y). Measure edge displacement at a fixed SCREEN row.
	var ride := win_rect(Vector2(0.10 * SIZE.x, 0.10 * SIZE.y), Vector2(0.30 * SIZE.x, 0.40 * SIZE.y), "13-ripple-ride.gdshader")
	var glued := win_rect(Vector2(0.55 * SIZE.x, 0.10 * SIZE.y), Vector2(0.30 * SIZE.x, 0.40 * SIZE.y), "09-ripple-still.gdshader")
	await frames(4)
	var before := L.grab(root)
	ride.position.y += 100.0
	glued.position.y += 100.0
	await frames(4)
	var after := L.grab(root)
	# displacement of the world's tile edge at x = 320 (tile boundary 4 * 80) for ride window, x = 800 (10 * 80) for glued, at screen row y
	var l6: Array = []
	for pair in [["ride (13-ripple-ride, UV.y)", ride, 320], ["glued (09-ripple-still, SCREEN_UV.y)", glued, 800]]:
		var node: ColorRect = pair[1]
		var edge_x: int = pair[2]
		var measure: Array = []
		for y in [180, 200, 220, 240, 260, 280]:        # rows inside both windows before (y 72..360) and after (y 172..460) the move, away from the sand path
			var shifted := {}
			for tag in ["before", "after"]:
				var im: Image = before if tag == "before" else after
				var first := im.get_pixel(edge_x - 60, y)
				var e := -1
				for x in range(edge_x - 59, edge_x + 60):
					var c := im.get_pixel(x, y)
					if absf(c.r - first.r) + absf(c.g - first.g) + absf(c.b - first.b) > 0.08:
						e = x
						break
				shifted[tag] = e - edge_x
			measure.append({"row": y, "edge_offset_px_before": shifted["before"], "edge_offset_px_after": shifted["after"]})
		l6.append({"window": pair[0], "rows": measure})
	L.out("L6-ride-vs-glued", {"windows_moved_down_px": 100, "result": l6, "reading": "glued: the offset at a given screen row does not change when the window moves; ride: it changes (the pattern moved with the window)"})
	img_save(after, "l6-after")
	ride.queue_free()
	glued.queue_free()
	await frames(2)

	# L7: hints at the screen edge and under magnification
	var code_default := "shader_type canvas_item;\nuniform sampler2D s : hint_screen_texture;\nvoid fragment() { COLOR.rgb = texture(s, SCREEN_UV + vec2(0.2, 0.0)).rgb; }\n"
	var code_disable := code_default.replace("hint_screen_texture", "hint_screen_texture, repeat_disable")
	var code_enable := code_default.replace("hint_screen_texture", "hint_screen_texture, repeat_enable")
	var edge_rows: Array = []
	for pair in [["no repeat hint", code_default], ["repeat_disable", code_disable], ["repeat_enable", code_enable]]:
		await fresh()
		var r := L.rect(Vector2(0.78 * SIZE.x, 0.30 * SIZE.y), Vector2(0.22 * SIZE.x, 0.20 * SIZE.y), Color.WHITE, "EdgeWin")
		r.material = L.mat_from(pair[1])
		main.add_child(r)
		await frames(4)
		var im := L.grab(root)
		# pixels at the far right of the window read x + 0.2 * W, i.e. beyond the right edge of the screen
		var last_col := im.get_pixel(1279, 250)
		var edge_pixel := base.get_pixel(1279, 250)
		var left_col := base.get_pixel(int(0.2 * 1280) - 1 - 10, 250)    # what wrapping would show: world near x = 0.2 W - ...
		var samples := []
		for x in [1000, 1100, 1200, 1250, 1275]:
			var c := im.get_pixel(x, 250)
			samples.append([x, snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)])
		var wrapped := []
		for x in [1000, 1100, 1200, 1250, 1275]:
			var wx: int = (x + 256) % 1280
			var c2 := base.get_pixel(wx, 250)
			wrapped.append([x, snappedf(c2.r, 0.001), snappedf(c2.g, 0.001), snappedf(c2.b, 0.001)])
		var clamped := []
		for x in [1000, 1100, 1200, 1250, 1275]:
			var cx: int = mini(x + 256, 1279)
			var c3 := base.get_pixel(cx, 250)
			clamped.append([x, snappedf(c3.r, 0.001), snappedf(c3.g, 0.001), snappedf(c3.b, 0.001)])
		edge_rows.append({"hint": pair[0], "window_pixels": samples, "world_if_wrapped": wrapped, "world_if_clamped_to_edge": clamped})
	L.out("L7a-repeat-at-the-edge", {"rows": edge_rows})

	var zoom_code := "shader_type canvas_item;\nuniform sampler2D s : hint_screen_texture%s;\nvoid fragment() { COLOR.rgb = texture(s, vec2(0.5, 0.25) + (SCREEN_UV - vec2(0.5)) * 0.02).rgb; }\n"
	var zoom_rows: Array = []
	for pair in [["no filter hint", ""], ["filter_nearest", ", filter_nearest"], ["filter_linear", ", filter_linear"]]:
		await fresh()
		var r := L.rect(Vector2(0, 0), SIZE, Color.WHITE, "Zoom")
		r.material = L.mat_from(zoom_code % pair[1])
		main.add_child(r)
		await frames(4)
		var im := L.grab(root)
		# the window centre now shows the screen at (640, 180): the vertical edge between two tiles (x = 640), magnified 50x. Count distinct colours along a row across that edge.
		var y := 360
		var colors := {}
		for x in range(560, 720):
			var c := im.get_pixel(x, y)
			colors[Vector3i(int(c.r * 255.0), int(c.g * 255.0), int(c.b * 255.0))] = true
		zoom_rows.append({"hint": pair[0], "distinct_colours_in_a_160px_row_at_50x_zoom": colors.size()})
		if pair[0] == "no filter hint":
			im.save_png("/private/tmp/claude-501/rts-checks/shots/l7-zoom-default.png")
	L.out("L7b-filter-when-magnified", {"rows": zoom_rows, "reading": "nearest: a hard step (few colours); linear: a smooth ramp (many colours)"})

	# L8: blur
	await fresh()
	var bw := win_rect(Vector2(0.20 * SIZE.x, 0.20 * SIZE.y), Vector2(0.50 * SIZE.x, 0.50 * SIZE.y), "14-blur.gdshader")
	var rowsb: Array = []
	for lod in [0.0, 2.0, 4.0]:
		set_u(bw, "blur", lod)
		await frames(4)
		var im := L.grab(root)
		# steepest step between neighbouring pixels along a row that crosses tile edges; blur lowers it
		var y := 300
		var maxstep := 0.0
		for x in range(int(bw.position.x) + 8, int(bw.position.x + bw.size.x) - 8):
			var c1 := im.get_pixel(x, y)
			var c2 := im.get_pixel(x + 1, y)
			maxstep = maxf(maxstep, absf(c1.r - c2.r) + absf(c1.g - c2.g) + absf(c1.b - c2.b))
		rowsb.append({"lod": lod, "largest_step_between_neighbour_pixels": snappedf(maxstep, 0.0001)})
		if lod == 4.0:
			im.save_png("/private/tmp/claude-501/rts-checks/shots/l8-blur4.png")
	L.out("L8a-blur-with-mipmap-filter", {"rows": rowsb})
	bw.queue_free()
	await frames(2)
	var nm_code := "shader_type canvas_item;\nuniform sampler2D s : hint_screen_texture%s;\nvoid fragment() { COLOR.rgb = textureLod(s, SCREEN_UV, 4.0).rgb; }\n"
	var nm_rows: Array = []
	for pair in [["filter_nearest (no mipmap)", ", filter_nearest"], ["filter_linear (no mipmap)", ", filter_linear"], ["filter_nearest_mipmap", ", filter_nearest_mipmap"], ["filter_linear_mipmap", ", filter_linear_mipmap"], ["no filter hint", ""]]:
		await fresh()
		var r := L.rect(Vector2(0.2 * SIZE.x, 0.2 * SIZE.y), Vector2(0.5 * SIZE.x, 0.5 * SIZE.y), Color.WHITE, "Lod4")
		r.material = L.mat_from(nm_code % pair[1])
		main.add_child(r)
		await frames(4)
		var im := L.grab(root)
		var maxstep := 0.0
		var y := 300
		for x in range(int(r.position.x) + 8, int(r.position.x + r.size.x) - 8):
			var c1 := im.get_pixel(x, y)
			var c2 := im.get_pixel(x + 1, y)
			maxstep = maxf(maxstep, absf(c1.r - c2.r) + absf(c1.g - c2.g) + absf(c1.b - c2.b))
		nm_rows.append({"hint": pair[0], "textureLod_level_4_largest_step": snappedf(maxstep, 0.0001)})
	L.out("L8b-textureLod-needs-a-mipmap-filter", {"rows": nm_rows, "reading": "a large step means unblurred (same as level 0); a small step means blurred"})

	# L9: pool + player on layer 0; a full-screen gray filter on layer 1
	await fresh()
	var pool9 := win_rect(Vector2(0.06 * SIZE.x, 0.52 * SIZE.y), Vector2(0.40 * SIZE.x, 0.40 * SIZE.y), "12-pool.gdshader")
	var pl := L.make_player(Vector2(0.75 * SIZE.x, 0.70 * SIZE.y))
	main.add_child(pl)
	await frames(4)
	var no_filter := L.grab(root)
	var cl := CanvasLayer.new()
	cl.layer = 1
	main.add_child(cl)
	var f := ColorRect.new()
	cl.add_child(f)
	f.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	f.material = L.mat_file("05-gray.gdshader")
	await frames(4)
	var with_filter := L.grab(root)
	# the player's body must still be there (as a gray), the pool must still be tinted (as a gray different from the meadow's gray)
	var player_before := L.px_abs(no_filter, int(pl.position.x), int(pl.position.y + 25))
	var player_after := L.px_abs(with_filter, int(pl.position.x), int(pl.position.y + 25))
	var luma_player := 0.299 * float(player_before[0]) + 0.587 * float(player_before[1]) + 0.114 * float(player_before[2])
	var meadow_before := L.px_abs(no_filter, int(0.55 * 1280), int(0.90 * 720))
	var pool_before := L.px_abs(no_filter, int(0.30 * 1280), int(0.80 * 720))
	var pool_after := L.px_abs(with_filter, int(0.30 * 1280), int(0.80 * 720))
	var luma_pool := 0.299 * float(pool_before[0]) + 0.587 * float(pool_before[1]) + 0.114 * float(pool_before[2])
	L.out("L9-filter-on-layer-1-sees-pool-and-player", {"player_before": player_before, "player_after": player_after, "expected_gray_of_player": snappedf(luma_player, 0.0001),
		"pool_before": pool_before, "pool_after": pool_after, "expected_gray_of_pool": snappedf(luma_pool, 0.0001), "meadow_before": meadow_before})
	with_filter.save_png("/private/tmp/claude-501/rts-checks/shots/l9-pool-and-gray.png")
	no_filter.save_png("/private/tmp/claude-501/rts-checks/shots/l9-pool.png")
	quit(0)

func img_save(img: Image, name: String) -> void:
	img.save_png("/private/tmp/claude-501/rts-checks/shots/" + name + ".png")
