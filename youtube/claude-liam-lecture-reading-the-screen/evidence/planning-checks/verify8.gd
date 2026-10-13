extends SceneTree
# verify8: the game-side line of the spotlight with a moving camera.
#  Q1 position / viewport size is the player's WORLD position over the screen size: wrong as soon as a Camera2D has moved
#  Q2 get_global_transform_with_canvas().origin / viewport size is the player's position ON THE SCREEN: right with or without a camera
# Run: ./run.sh verify8 [forward_plus|gl_compatibility]
const L = preload("res://rts_lib.gd")
const SIZE := Vector2(1280, 720)

var main: Node2D

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func is_gray(c: Color) -> bool:
	return maxf(absf(c.r - c.g), maxf(absf(c.g - c.b), absf(c.r - c.b))) < 0.012

func lit_centroid(img: Image) -> Vector2:
	var sx := 0.0
	var sy := 0.0
	var n := 0
	for y in range(0, 720, 3):
		for x in range(0, 1280, 3):
			if not is_gray(img.get_pixel(x, y)):
				sx += x
				sy += y
				n += 1
	return Vector2(sx / float(n), sy / float(n))

func run() -> void:
	root.size = Vector2i(1280, 720)
	RenderingServer.set_default_clear_color(L.STAGE)
	L.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()})
	for variant in ["world_position_over_size", "canvas_transform_origin_over_size"]:
		main = Node2D.new()
		root.add_child(main)
		# a big world around the camera
		var world := L.build_world(main, SIZE, 2)
		var player := L.make_player(Vector2(900, 500))
		player.name = "Player"
		main.add_child(player)
		var cam := Camera2D.new()
		cam.position = Vector2(840, 460)        # the view is shifted by (200, 100) from the origin-centred default
		main.add_child(cam)
		cam.make_current()
		var layer := CanvasLayer.new()
		layer.layer = 1
		main.add_child(layer)
		var f := ColorRect.new()
		layer.add_child(f)
		f.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		f.mouse_filter = Control.MOUSE_FILTER_IGNORE
		f.material = L.mat_file("07-spotlight.gdshader")
		(f.material as ShaderMaterial).set_shader_parameter("radius", 0.25)
		await frames(3)
		var size := Vector2(root.get_visible_rect().size)
		var spot: Vector2 = player.position / size if variant == "world_position_over_size" else player.get_global_transform_with_canvas().origin / size
		(f.material as ShaderMaterial).set_shader_parameter("player", spot)
		await frames(4)
		var img := L.grab(root)
		var c := lit_centroid(img)
		var expected_screen := Vector2(900, 500) - Vector2(200, 100)
		L.out("Q-" + variant, {"viewport_rect_size": [size.x, size.y], "player_world_px": [900, 500], "camera_position": [840, 460], "player_screen_px_expected": [expected_screen.x, expected_screen.y],
			"canvas_transform_origin_px": [snappedf(player.get_global_transform_with_canvas().origin.x, 0.1), snappedf(player.get_global_transform_with_canvas().origin.y, 0.1)],
			"uniform_sent": [snappedf(spot.x, 0.0001), snappedf(spot.y, 0.0001)], "lit_area_centroid_px": [snappedf(c.x, 1.0), snappedf(c.y, 1.0)],
			"circle_is_on_the_player": absf(c.x - expected_screen.x) < 8.0 and absf(c.y - expected_screen.y) < 8.0})
		img.save_png("/private/tmp/claude-501/rts-checks/shots/q-" + variant + ".png")
		main.queue_free()
		await frames(3)
	quit(0)
