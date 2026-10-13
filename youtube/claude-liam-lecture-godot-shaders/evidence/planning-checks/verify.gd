extends SceneTree
# Scratch verification for the Godot Shaders film plan. Prints one RESULT line per check.
# Run non-headless: godot --path <dir> --script res://verify.gd

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func out(id: String, data: Dictionary) -> void:
	data["id"] = id
	print("RESULT " + JSON.stringify(data))

func make_rect(code: String, pos: Vector2, size: Vector2) -> ColorRect:
	var rect := ColorRect.new()
	rect.position = pos
	rect.size = size
	var sh := Shader.new()
	sh.code = code
	var mat := ShaderMaterial.new()
	mat.shader = sh
	rect.material = mat
	return rect

func run() -> void:
	root.size = Vector2i(640, 360)
	await frames(3)
	var probe := grab()
	var scale := float(probe.get_width()) / 640.0
	out("env", {"engine": Engine.get_version_info()["string"], "root_size": [root.size.x, root.size.y], "image_size": [probe.get_width(), probe.get_height()], "scale": scale, "adapter": RenderingServer.get_video_adapter_name(), "renderer": RenderingServer.get_current_rendering_method()})

	# ---- A: what is TIME? Add a node ~3 s after start. 8 stripes lit if TIME >= k+1.
	await create_timer(3.0).timeout
	var ticks_at_add := Time.get_ticks_msec() / 1000.0
	var rect_a := make_rect("shader_type canvas_item;\nvoid fragment() { float k = floor(UV.y * 8.0); COLOR = TIME >= k + 1.0 ? vec4(1.0) : vec4(0.0, 0.0, 0.0, 1.0); }", Vector2(20, 20), Vector2(80, 320))
	root.add_child(rect_a)
	await frames(2)
	var img_a := grab()
	var lit := 0
	for k in range(8):
		var y := int((20.0 + (k + 0.5) * 40.0) * scale)
		var c := img_a.get_pixel(int(60.0 * scale), y)
		if c.r > 0.5: lit += 1
	var ticks_at_read := Time.get_ticks_msec() / 1000.0
	out("A-time-is-engine-time", {"ticks_at_add_s": ticks_at_add, "ticks_at_read_s": ticks_at_read, "stripes_lit_first_frame": lit, "reading": "stripes lit == floor(TIME). If TIME restarted at node creation this would be 0."})
	rect_a.queue_free()
	await frames(1)

	# ---- B: UV orientation + discard in one rect.
	var rect_b := make_rect("shader_type canvas_item;\nvoid fragment() { if (UV.x > 0.5) { discard; } COLOR = vec4(UV.y, 0.0, 0.0, 1.0); }", Vector2(120, 20), Vector2(100, 100))
	root.add_child(rect_b)
	await frames(2)
	var img_b := grab()
	var bg := img_b.get_pixel(int(400.0 * scale), int(300.0 * scale))
	var top_left := img_b.get_pixel(int(140.0 * scale), int(24.0 * scale))
	var bottom_left := img_b.get_pixel(int(140.0 * scale), int(116.0 * scale))
	var right_half := img_b.get_pixel(int(200.0 * scale), int(60.0 * scale))
	out("B-uv-y-and-discard", {"background": [bg.r, bg.g, bg.b], "top_left_r": top_left.r, "bottom_left_r": bottom_left.r, "right_half_after_discard": [right_half.r, right_half.g, right_half.b], "reading": "UV.y ~0 at top, ~1 at bottom; discarded half shows the background"})
	rect_b.queue_free()
	await frames(1)

	# ---- C: vertex() moves corners only. Sprite2D has 4 vertices; bottom pair shifts +50.
	var img := Image.create(100, 100, false, Image.FORMAT_RGBA8)
	img.fill(Color.WHITE)
	var spr := Sprite2D.new()
	spr.texture = ImageTexture.create_from_image(img)
	spr.centered = false
	spr.position = Vector2(300, 100)
	var sh_c := Shader.new()
	sh_c.code = "shader_type canvas_item;\nvoid vertex() { VERTEX.x += 50.0 * step(0.5, UV.y); }"
	var mat_c := ShaderMaterial.new()
	mat_c.shader = sh_c
	spr.material = mat_c
	root.add_child(spr)
	await frames(2)
	var img_c := grab()
	var firsts: Array = []
	for row in [2, 25, 50, 75, 97]:
		var y := int((100.0 + row) * scale)
		var first_x := -1
		for xx in range(int(280.0 * scale), int(400.0 * scale)):
			if img_c.get_pixel(xx, y).r > 0.9:
				first_x = int(round(xx / scale))
				break
		firsts.append([row, first_x])
	out("C-vertex-moves-corners-only", {"left_edge_x_by_row": firsts, "reading": "sprite left edge is x=300 at rest. A straight ramp 300->350 down the rows = only the 4 corners moved and the GPU interpolated. A step at row 50 would mean per-pixel."})
	spr.queue_free()
	await frames(1)

	# ---- D: the slow loop. Naive set_pixel vs packed-array fill, one 1920x1080 frame.
	var t0 := Time.get_ticks_usec()
	var big := Image.create(1920, 1080, false, Image.FORMAT_RGBA8)
	for y in range(1080):
		for x in range(1920):
			big.set_pixel(x, y, Color(x / 1919.0, 0.0, 0.0))
	var naive_ms := (Time.get_ticks_usec() - t0) / 1000.0
	var t1 := Time.get_ticks_usec()
	var bytes := PackedByteArray()
	bytes.resize(1920 * 1080 * 4)
	var i := 0
	for y in range(1080):
		for x in range(1920):
			bytes[i] = int(255.0 * x / 1919.0)
			bytes[i + 3] = 255
			i += 4
	var packed_ms := (Time.get_ticks_usec() - t1) / 1000.0
	out("D-cpu-gradient-cost", {"pixels": 1920 * 1080, "naive_set_pixel_ms": naive_ms, "packed_array_loop_ms": packed_ms, "frame_budget_60fps_ms": 16.667})

	quit(0)
