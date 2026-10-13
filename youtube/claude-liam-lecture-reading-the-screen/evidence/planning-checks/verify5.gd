extends SceneTree
# verify5: three practical claims about full-screen filters, checked in a real window of Godot 4.7.2.
#  N1 a full-screen ColorRect takes mouse clicks away from the game unless its Mouse Filter is Ignore
#  N2 screen reading works in the capture route: a 3840 x 2160 SubViewport drawing a 1280 x 720 canvas (size_2d_override)
#  N3 a window sprite parented under a moving node still reads at its screen position (the camera pan case)
# Run: ./run.sh verify5 [forward_plus|gl_compatibility]
const L = preload("res://rts_lib.gd")
const SIZE := Vector2(1280, 720)
const HANDLER := "extends Node\nvar count := 0\nfunc _unhandled_input(event):\n\tif event is InputEventMouseButton and event.pressed:\n\t\tcount += 1\n"

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

func click(at: Vector2) -> void:
	var ev := InputEventMouseButton.new()
	ev.button_index = MOUSE_BUTTON_LEFT
	ev.pressed = true
	ev.position = at
	ev.global_position = at
	root.push_input(ev)

func run() -> void:
	root.size = Vector2i(1280, 720)
	RenderingServer.set_default_clear_color(L.STAGE)
	L.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()})

	# N1
	var rows: Array = []
	for mode in [["default mouse_filter", -1], ["MOUSE_FILTER_STOP", Control.MOUSE_FILTER_STOP], ["MOUSE_FILTER_PASS", Control.MOUSE_FILTER_PASS], ["MOUSE_FILTER_IGNORE", Control.MOUSE_FILTER_IGNORE]]:
		await fresh()
		var scr := GDScript.new()
		scr.source_code = HANDLER
		scr.reload()
		var game := Node.new()
		game.set_script(scr)
		main.add_child(game)
		var cl := CanvasLayer.new()
		main.add_child(cl)
		var f := ColorRect.new()
		cl.add_child(f)
		f.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		var default_value := int(f.mouse_filter)
		if mode[1] >= 0:
			f.mouse_filter = mode[1]
		await frames(3)
		click(Vector2(400, 300))
		await frames(2)
		rows.append({"setting": mode[0], "ColorRect_default_mouse_filter_value": default_value, "clicks_that_reached_the_game": game.get("count")})
	L.out("N1-full-screen-colorrect-and-clicks", {"rows": rows, "enum": {"STOP": Control.MOUSE_FILTER_STOP, "PASS": Control.MOUSE_FILTER_PASS, "IGNORE": Control.MOUSE_FILTER_IGNORE}})

	# N2: the capture route. SubViewport 3840 x 2160 showing a 1280 x 720 canvas.
	await fresh()
	var sub := SubViewport.new()
	sub.size = Vector2i(3840, 2160)
	sub.size_2d_override = Vector2i(1280, 720)
	sub.size_2d_override_stretch = true
	sub.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	main.add_child(sub)
	var inner := Node2D.new()
	sub.add_child(inner)
	L.build_world(inner, SIZE)
	await frames(4)
	var base_sub := sub.get_texture().get_image()
	var win := L.rect(Vector2(0.5 * SIZE.x, 0.2 * SIZE.y), Vector2(384, 216), L.TEAL, "Win")
	win.material = L.mat_file("03-invert.gdshader")
	inner.add_child(win)
	var probe_rect := L.rect(Vector2(0.05 * SIZE.x, 0.05 * SIZE.y), Vector2(200, 100), Color.WHITE, "Probe")
	probe_rect.material = L.mat_from("shader_type canvas_item;\nvoid fragment() { COLOR = vec4(SCREEN_PIXEL_SIZE.x * 2000.0, SCREEN_PIXEL_SIZE.y * 2000.0, SCREEN_PIXEL_SIZE.y / SCREEN_PIXEL_SIZE.x / 4.0, 1.0); }\n")
	inner.add_child(probe_rect)
	await frames(4)
	var img := sub.get_texture().get_image()
	var cx := int((0.5 * SIZE.x + 192.0) * 3.0)
	var cy := int((0.2 * SIZE.y + 108.0) * 3.0)
	var p_world := base_sub.get_pixel(cx, cy)
	var p_win := img.get_pixel(cx, cy)
	var pp := img.get_pixel(int((0.05 * SIZE.x + 100.0) * 3.0), int((0.05 * SIZE.y + 50.0) * 3.0))
	L.out("N2-subviewport-4k-over-720p-canvas", {"subviewport_px": [img.get_width(), img.get_height()], "world_px": [snappedf(p_world.r, 0.0001), snappedf(p_world.g, 0.0001), snappedf(p_world.b, 0.0001)],
		"window_px": [snappedf(p_win.r, 0.0001), snappedf(p_win.g, 0.0001), snappedf(p_win.b, 0.0001)], "is_exact_inverse": absf((1.0 - p_world.r) - p_win.r) < 0.01 and absf((1.0 - p_world.g) - p_win.g) < 0.01 and absf((1.0 - p_world.b) - p_win.b) < 0.01,
		"SCREEN_PIXEL_SIZE_x_times_2000": snappedf(pp.r, 0.0001), "SCREEN_PIXEL_SIZE_y_times_2000": snappedf(pp.g, 0.0001), "expected_if_3840x2160": [snappedf(2000.0 / 3840.0, 0.0001), snappedf(2000.0 / 2160.0, 0.0001)],
		"ratio_y_over_x_decoded": snappedf(pp.b * 4.0, 0.001)})
	img.save_png("/private/tmp/claude-501/rts-checks/shots/n2-sub4k.png")

	# N3: a window that is a child of a moving world node: reads at its SCREEN position, not at the parent's
	await fresh()
	var worldroot := Node2D.new()
	main.add_child(worldroot)
	L.build_world(worldroot, SIZE)
	var w3 := L.rect(Vector2(0.20 * SIZE.x, 0.20 * SIZE.y), Vector2(320, 180), Color.WHITE, "Win")
	w3.material = L.mat_file("01-window.gdshader")
	worldroot.add_child(w3)
	await frames(3)
	var before := L.grab(root)
	worldroot.position = Vector2(0, 120)
	await frames(3)
	var after := L.grab(root)
	# the window follows the world (it is a child), so it still vanishes into the (moved) world
	var ok := 0
	var n := 0
	for y in range(int(w3.position.y) + 120 + 6, int(w3.position.y) + 120 + 174, 9):
		for x in range(int(w3.position.x) + 6, int(w3.position.x) + 314, 9):
			var a := after.get_pixel(x, y)
			var ground_only_expected := before.get_pixel(x, y - 120)
			n += 1
			if absf(a.r - ground_only_expected.r) < 0.01 and absf(a.g - ground_only_expected.g) < 0.01:
				ok += 1
	L.out("N3-window-child-of-a-moving-world", {"samples": n, "match_world_moved_down_120": ok})
	quit(0)
