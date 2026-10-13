extends SceneTree
# verify3: full-screen effects (Act II), checked in a real window of Godot 4.7.2.
#  K1 SCREEN_PIXEL_SIZE is one over the resolution, so its y over x is width over height
#  K2 05-gray: dot() weights, the dial from color (0) to gray (1)
#  K3 06-spotlight-oval vs 07-spotlight: the lit area is wider than tall until the address is corrected
#  K4 the game feeds the player's screen address to the shader every frame
#  K5 Full Rect: set_anchors_preset() alone keeps the size; set_anchors_and_offsets_preset() fits the viewport
#  K6 the same full-screen ColorRect on a CanvasLayer sees the world AND the player; a HUD on a higher layer is untouched
#  K7 reading the screen works inside a SubViewport too (the route the captures use)
# Run: ./run.sh verify3 [forward_plus|gl_compatibility]
const L = preload("res://rts_lib.gd")
var SIZE := Vector2(1280, 720)

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

func is_gray(c: Color) -> bool:
	return maxf(absf(c.r - c.g), maxf(absf(c.g - c.b), absf(c.r - c.b))) < 0.012

func full_screen_layer(shader: String) -> ColorRect:
	var cl := CanvasLayer.new()
	cl.layer = 1
	main.add_child(cl)
	var r := ColorRect.new()
	r.name = "Filter"
	cl.add_child(r)
	r.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	r.material = L.mat_file(shader)
	return r

func extent(img: Image, cx: int, cy: int, horizontal: bool) -> Array:
	# walk outwards from (cx, cy) along one axis; return [negative_extent_px, positive_extent_px] of the unbroken run of non-gray pixels
	var lo := 0
	var hi := 0
	var lim := (img.get_width() if horizontal else img.get_height())
	for s: int in [-1, 1]:
		var k: int = 0
		while true:
			var x: int = cx + (s * k if horizontal else 0)
			var y: int = cy + (0 if horizontal else s * k)
			if x < 0 or y < 0 or x >= img.get_width() or y >= img.get_height():
				break
			if is_gray(img.get_pixel(x, y)):
				break
			k += 1
			if k > lim:
				break
		if s < 0:
			lo = k
		else:
			hi = k
	return [lo, hi]

func run() -> void:
	root.size = Vector2i(1280, 720)
	RenderingServer.set_default_clear_color(L.STAGE)
	L.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()})

	# K1: SCREEN_PIXEL_SIZE
	var probe_code := "shader_type canvas_item;\nvoid fragment() { COLOR = vec4(SCREEN_PIXEL_SIZE.x * 500.0, SCREEN_PIXEL_SIZE.y * 500.0, SCREEN_PIXEL_SIZE.y / SCREEN_PIXEL_SIZE.x / 4.0, 1.0); }\n"
	var rows: Array = []
	for sz in [Vector2i(1280, 720), Vector2i(800, 600), Vector2i(1000, 500)]:
		root.size = sz
		await fresh()
		var r := ColorRect.new()
		r.size = Vector2(sz.x, sz.y)
		r.material = L.mat_from(probe_code)
		main.add_child(r)
		await frames(4)
		var img := L.grab(root)
		var c := img.get_pixel(sz.x / 2, sz.y / 2)
		rows.append({"window": [sz.x, sz.y], "x_pixel_size_times_500": snappedf(c.r * 1.0, 0.0001), "expected_x": snappedf(500.0 / sz.x, 0.0001), "y_pixel_size_times_500": snappedf(c.g, 0.0001), "expected_y": snappedf(500.0 / sz.y, 0.0001),
			"ratio_y_over_x_decoded": snappedf(c.b * 4.0, 0.001), "width_over_height": snappedf(float(sz.x) / float(sz.y), 0.001)})
	L.out("K1-SCREEN_PIXEL_SIZE", {"rows": rows})
	root.size = Vector2i(1280, 720)
	await frames(2)

	# K5 first (it decides how K2..K6 build the filter): Full Rect
	await fresh()
	var cl5 := CanvasLayer.new()
	main.add_child(cl5)
	var a := ColorRect.new()
	cl5.add_child(a)
	a.set_anchors_preset(Control.PRESET_FULL_RECT)
	var b := ColorRect.new()
	cl5.add_child(b)
	b.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var c5 := ColorRect.new()
	cl5.add_child(c5)
	c5.set_anchors_preset(Control.PRESET_FULL_RECT, true)
	await frames(3)
	L.out("K5-full-rect", {"viewport": [root.size.x, root.size.y], "set_anchors_preset_only_size": [a.size.x, a.size.y],
		"set_anchors_and_offsets_preset_size": [b.size.x, b.size.y], "set_anchors_preset_keep_offsets_true_size": [c5.size.x, c5.size.y],
		"anchors_of_b": [b.anchor_left, b.anchor_top, b.anchor_right, b.anchor_bottom], "offsets_of_b": [b.offset_left, b.offset_top, b.offset_right, b.offset_bottom]})
	# does a full rect follow a window resize?
	root.size = Vector2i(1000, 500)
	await frames(3)
	L.out("K5b-full-rect-follows-resize", {"viewport": [root.size.x, root.size.y], "size_after_resize": [b.size.x, b.size.y]})
	root.size = Vector2i(1280, 720)
	await frames(3)

	# K2: gray dial
	await fresh()
	L.build_world(main, SIZE)
	await frames(3)
	var base := L.grab(root)
	var f := full_screen_layer("05-gray.gdshader")
	var spots := [[0.20, 0.10], [0.55, 0.55], [0.30, 0.30]]
	var k2: Array = []
	for amt in [0.0, 0.5, 1.0]:
		(f.material as ShaderMaterial).set_shader_parameter("amount", amt)
		await frames(3)
		var img2 := L.grab(root)
		for s in spots:
			var w := base.get_pixel(int(s[0] * (base.get_width() - 1)), int(s[1] * (base.get_height() - 1)))
			var luma := 0.299 * w.r + 0.587 * w.g + 0.114 * w.b
			var expect := [snappedf(w.r + (luma - w.r) * amt, 0.0001), snappedf(w.g + (luma - w.g) * amt, 0.0001), snappedf(w.b + (luma - w.b) * amt, 0.0001)]
			var got := L.px(img2, s[0], s[1])
			k2.append({"amount": amt, "at": s, "world": L.px(base, s[0], s[1]), "luma_0.299_0.587_0.114": snappedf(luma, 0.0001), "expected": expect, "got": got, "matches": L.close(expect, got, 0.012)})
	L.out("K2-gray-dial", {"rows": k2})

	# K3: oval vs circle, radius 0.25 around the middle of the screen
	var pc := Vector2(640, 360)
	for pair in [["06-spotlight-oval.gdshader", "oval"], ["07-spotlight.gdshader", "fixed"]]:
		await fresh()
		L.build_world(main, SIZE)
		var flt := full_screen_layer(pair[0])
		(flt.material as ShaderMaterial).set_shader_parameter("player", Vector2(0.5, 0.5))
		(flt.material as ShaderMaterial).set_shader_parameter("radius", 0.25)
		await frames(4)
		var img3 := L.grab(root)
		var hx := extent(img3, int(pc.x), int(pc.y), true)
		var vy := extent(img3, int(pc.x), int(pc.y), false)
		L.out("K3-spotlight-" + pair[1], {"shader": pair[0], "radius_uniform": 0.25, "horizontal_radius_px_left_right": hx, "vertical_radius_px_up_down": vy,
			"expected_if_oval": {"horizontal": 0.25 * 1280.0, "vertical": 0.25 * 720.0}, "expected_if_round": {"both": 0.25 * 720.0}})
		img3.save_png("/private/tmp/claude-501/rts-checks/shots/k3-" + pair[1] + ".png")

	# K4: follow the player: place the player at two spots, feed the uniform from the node's position, measure the lit circle's centre
	await fresh()
	L.build_world(main, SIZE)
	var player := L.make_player(Vector2(300, 250))
	main.add_child(player)
	var flt4 := full_screen_layer("07-spotlight.gdshader")
	var k4: Array = []
	for pos in [Vector2(300, 250), Vector2(900, 480)]:
		player.position = pos
		(flt4.material as ShaderMaterial).set_shader_parameter("player", pos / SIZE)
		await frames(4)
		var img4 := L.grab(root)
		var hx4 := extent(img4, int(pos.x), int(pos.y), true)
		var vy4 := extent(img4, int(pos.x), int(pos.y), false)
		k4.append({"player_px": [pos.x, pos.y], "uniform_sent": [snappedf(pos.x / SIZE.x, 0.0001), snappedf(pos.y / SIZE.y, 0.0001)], "lit_run_left_right_px": hx4, "lit_run_up_down_px": vy4,
			"player_pixel_is_in_colour_not_gray": not is_gray(img4.get_pixel(int(pos.x), int(pos.y) + 25))})
	L.out("K4-follow-the-player", {"rows": k4})

	# K6: filter on layer 1; player on layer 0 is grayed too; HUD on layer 2 stays in colour
	await fresh()
	L.build_world(main, SIZE)
	var pl := L.make_player(Vector2(300, 250))
	main.add_child(pl)
	var flt6 := full_screen_layer("05-gray.gdshader")
	var hud_layer := CanvasLayer.new()
	hud_layer.layer = 2
	main.add_child(hud_layer)
	hud_layer.add_child(L.make_hud(SIZE))
	await frames(4)
	var img6 := L.grab(root)
	L.out("K6-filter-sees-player-and-hud-stays", {"player_body_px": L.px_abs(img6, 300, 275), "player_body_is_gray": is_gray(img6.get_pixel(300, 275)),
		"hud_fill_px": L.px(img6, 0.03, 0.05), "hud_fill_is_gray": is_gray(img6.get_pixel(int(0.03 * 1279), int(0.05 * 719))), "meadow_px": L.px(img6, 0.55, 0.9), "meadow_is_gray": is_gray(img6.get_pixel(int(0.55 * 1279), int(0.9 * 719)))})
	img6.save_png("/private/tmp/claude-501/rts-checks/shots/k6-gray-hud.png")

	# K7: SubViewport
	await fresh()
	var sub := SubViewport.new()
	sub.size = Vector2i(1920, 1080)
	sub.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	main.add_child(sub)
	var inner := Node2D.new()
	sub.add_child(inner)
	var sbig := Vector2(1920, 1080)
	L.build_world(inner, sbig)
	var base_sub := Image.new()
	await frames(3)
	base_sub = sub.get_texture().get_image()
	var win := L.rect(Vector2(0.5 * sbig.x, 0.2 * sbig.y), Vector2(480, 270), L.TEAL, "Win")
	win.material = L.mat_file("03-invert.gdshader")
	inner.add_child(win)
	await frames(4)
	var sub_img := sub.get_texture().get_image()
	var p_world := base_sub.get_pixel(int(0.5 * sbig.x) + 240, int(0.2 * sbig.y) + 135)
	var p_win := sub_img.get_pixel(int(0.5 * sbig.x) + 240, int(0.2 * sbig.y) + 135)
	L.out("K7-subviewport", {"subviewport": [sub_img.get_width(), sub_img.get_height()], "world_px": [snappedf(p_world.r, 0.0001), snappedf(p_world.g, 0.0001), snappedf(p_world.b, 0.0001)],
		"inverted_window_px": [snappedf(p_win.r, 0.0001), snappedf(p_win.g, 0.0001), snappedf(p_win.b, 0.0001)], "is_exact_inverse": absf((1.0 - p_world.r) - p_win.r) < 0.01 and absf((1.0 - p_world.g) - p_win.g) < 0.01})
	quit(0)
