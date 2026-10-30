extends SceneTree
## A5 (agent-written): renders res://tests/normal_map_check.tscn (CHANGE-BRIEF.md
## F8) under the review fixture's light: one cargo_panel material per normal map,
## GL, DX as imported, DX with Invert Y. Needs a real renderer (no --headless):
##   ../Godot_v4.7.2-stable_win64_console.exe --path . --script res://tests/a5_capture_normals.gd
## The three-panel frame is kept for eyes. The numbers come from one panel at one
## place: Panel_GL's mesh wears each material in turn, so sampling phase and
## position are the same in all three frames and only the normal map differs.

const OUT := "res://evidence/a5/normal-map-check/"

func _initialize() -> void: call_deferred("run")

func face_rect(camera: Camera3D, panel: MeshInstance3D) -> Rect2i:
	# The front face (z = +0.05), shrunk by 10% so edges and bevels stay out.
	var a := camera.unproject_position(panel.global_transform * Vector3(-0.54, 0.54, 0.05))
	var b := camera.unproject_position(panel.global_transform * Vector3(0.54, -0.54, 0.05))
	return Rect2i(Vector2i(ceili(a.x), ceili(a.y)), Vector2i(floori(b.x - a.x), floori(b.y - a.y)))

func run() -> void:
	var scene := (load("res://tests/normal_map_check.tscn") as PackedScene).instantiate()
	root.add_child(scene)
	for i in range(30): await process_frame
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	img.convert(Image.FORMAT_RGB8)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT))
	img.save_png(OUT + "normal-map-check.png")
	var camera := scene.get_node("Camera3D") as Camera3D
	var rects := {}
	for n in ["GL", "DX_raw", "DX_fixed"]:
		rects[n] = face_rect(camera, scene.get_node("Panel_" + n))
		img.get_region(rects[n]).save_png(OUT + "panel-%s.png" % n)
	var panel := scene.get_node("Panel_GL") as MeshInstance3D
	var rect: Rect2i = rects.GL
	var frames := {}
	for n in ["GL", "DX_raw", "DX_fixed"]:
		panel.material_override = (scene.get_node("Panel_" + n) as MeshInstance3D).material_override
		for i in range(10): await process_frame
		await RenderingServer.frame_post_draw
		var frame := root.get_texture().get_image()
		frame.convert(Image.FORMAT_RGB8)
		frames[n] = frame.get_region(rect)
		frames[n].save_png(OUT + "same-place-%s.png" % n)
	var result := {"renderer": RenderingServer.get_current_rendering_method(), "driver": RenderingServer.get_current_rendering_driver_name(),
		"adapter": RenderingServer.get_video_adapter_name(), "image_size": str(img.get_size()), "rect": str(rect), "mean_abs_delta_vs_gl": {}, "max_abs_delta_vs_gl": {}}
	for n in ["GL", "DX_raw", "DX_fixed"]:
		var a: Image = frames.GL
		var b: Image = frames[n]
		var total := 0.0
		var worst := 0.0
		for y in range(rect.size.y):
			for x in range(rect.size.x):
				var p := a.get_pixel(x, y)
				var q := b.get_pixel(x, y)
				var d := maxf(absf(p.r - q.r), maxf(absf(p.g - q.g), absf(p.b - q.b))) * 255.0
				total += (absf(p.r - q.r) + absf(p.g - q.g) + absf(p.b - q.b)) * 255.0 / 3.0
				worst = maxf(worst, d)
		result.mean_abs_delta_vs_gl[n] = total / float(rect.size.x * rect.size.y)
		result.max_abs_delta_vs_gl[n] = worst
		print("SAME PLACE %s vs GL: mean |delta| %.3f levels, max %.0f, over %s" % [n, result.mean_abs_delta_vs_gl[n], worst, rect.size])
	var f := FileAccess.open(OUT + "measurement.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(result, "	"))
	f.close()
	var raw: float = result.mean_abs_delta_vs_gl.DX_raw
	var fixed: float = result.mean_abs_delta_vs_gl.DX_fixed
	var same: float = result.mean_abs_delta_vs_gl.GL
	# Fixed DX may differ from GL only by what the imports differ by (about one
	# level); the raw DX map must differ by more somewhere.
	var fixed_max: float = result.max_abs_delta_vs_gl.DX_fixed
	var raw_max: float = result.max_abs_delta_vs_gl.DX_raw
	var ok := same == 0.0 and fixed_max <= 2.0 and raw_max > fixed_max and fixed < raw
	print("NORMAL CAPTURE: GL repeat %.3f, fixed mean %.3f max %.0f, raw mean %.3f max %.0f -> %s" % [same, fixed, fixed_max, raw, raw_max, "PASS" if ok else "FAIL"])
	quit(0 if ok else 1)
