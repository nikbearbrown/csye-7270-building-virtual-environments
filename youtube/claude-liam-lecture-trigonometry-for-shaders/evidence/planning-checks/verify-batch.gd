extends SceneTree
# Batch renderer for the Trigonometry for Shaders layout checks. ONE Godot process renders many cases, so the many-variant sweeps do not
# have to queue for the shared Shader Lab (lab/check_shader.sh, one job at a time) dozens of times. It mimics lab/runner.gd:
# same clear colour (#D9D5CA), same stage kinds (a ColorRect that fills the view, or a Sprite2D with the 128 px test texture scaled to 0.8 of the view),
# same probe rule (pixel int(u * (w - 1)), int(v * (h - 1))), and it renders the shader files in ../../lab-shaders/ unchanged.
# Run (windowed, Forward+):  godot --path <scratch project> --script res://verify-batch.gd -- --cases <cases.json> --out <batch-results.json>
# A case: {label, shader (absolute path), kind rect|sprite, size [w, h], set {uniform: float}, waits [seconds...], probes [[u, v]...], png (path prefix or "")}
# For every wait in the list the frame is read once (TIME advances while it runs, as in the Lab); elapsed_s is the accumulated process time.

var out_path := ""
var results: Array = []

func _initialize() -> void:
	call_deferred("run")

func make_image(kind: String, n: int = 128) -> Image:
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	match kind:
		"white":
			img.fill(Color.WHITE)
		"checker":
			for y in n:
				for x in n:
					var on := ((x / (n / 8)) + (y / (n / 8))) % 2 == 0
					img.set_pixel(x, y, Color("#FAF9F5") if on else Color("#5FA391"))
		_:
			img.fill(Color(0, 0, 0, 0))
			var c := Vector2(n / 2.0, n / 2.0)
			for y in n:
				for x in n:
					var d := Vector2(x, y).distance_to(c)
					if d < n * 0.30:
						img.set_pixel(x, y, Color("#5FA391"))
					var e1 := Vector2(x, y).distance_to(c + Vector2(-n * 0.10, -n * 0.06))
					var e2 := Vector2(x, y).distance_to(c + Vector2(n * 0.10, -n * 0.06))
					if e1 < n * 0.035 or e2 < n * 0.035:
						img.set_pixel(x, y, Color("#FAF9F5"))
	return img

func run() -> void:
	var cases_path := ""
	var a := OS.get_cmdline_user_args()
	var i := 0
	while i < a.size():
		if a[i] == "--cases":
			cases_path = a[i + 1]
			i += 2
		elif a[i] == "--out":
			out_path = a[i + 1]
			i += 2
		else:
			i += 1
	var cases: Array = JSON.parse_string(FileAccess.get_file_as_string(cases_path))
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	print("RESULT " + JSON.stringify({"id": "env", "engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(), "cases": cases.size()}))
	for c in cases:
		await run_case(c)
	var f := FileAccess.open(out_path, FileAccess.WRITE)
	f.store_string(JSON.stringify(results, "  "))
	f.close()
	print("RESULT " + JSON.stringify({"id": "done", "cases": results.size()}))
	quit(0)

func run_case(c: Dictionary) -> void:
	var W := int(c["size"][0])
	var H := int(c["size"][1])
	root.size = Vector2i(W, H)
	for k in 3:
		await process_frame
	var shader := Shader.new()
	shader.code = FileAccess.get_file_as_string(c["shader"])
	var mat := ShaderMaterial.new()
	mat.shader = shader
	for k in c.get("set", {}).keys():
		mat.set_shader_parameter(k, float(c["set"][k]))
	var stage: Node
	if c["kind"] == "sprite":
		var sp := Sprite2D.new()
		sp.texture = ImageTexture.create_from_image(make_image(c.get("sprite_tex", "sprite"), 128))
		sp.position = Vector2(W / 2.0, H / 2.0)
		var sc := minf(W, H) * 0.8 / 128.0
		sp.scale = Vector2(sc, sc)
		sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		sp.material = mat
		stage = sp
	else:
		var cr := ColorRect.new()
		cr.size = Vector2(W, H)
		cr.material = mat
		stage = cr
	root.add_child(stage)
	var elapsed := 0.0
	await process_frame
	var captures: Array = []
	var idx := 0
	for w in c.get("waits", [0.0]):
		while elapsed < float(w):
			await process_frame
			elapsed += root.get_process_delta_time()
		await process_frame
		elapsed += root.get_process_delta_time()
		RenderingServer.force_draw(false)
		var img := root.get_texture().get_image()
		var probes: Array = []
		for p in c.get("probes", []):
			var px := clampi(int(float(p[0]) * (img.get_width() - 1)), 0, img.get_width() - 1)
			var py := clampi(int(float(p[1]) * (img.get_height() - 1)), 0, img.get_height() - 1)
			var col := img.get_pixel(px, py)
			probes.append({"at": [p[0], p[1]], "px": [px, py], "rgba": [snappedf(col.r, 0.0001), snappedf(col.g, 0.0001), snappedf(col.b, 0.0001), snappedf(col.a, 0.0001)]})
		var png := ""
		if String(c.get("png", "")) != "":
			png = "%s_w%d.png" % [c["png"], idx]
			DirAccess.make_dir_recursive_absolute(png.get_base_dir())
			img.save_png(png)
		captures.append({"wait": w, "elapsed_s": snappedf(elapsed, 0.0001), "probes": probes, "png": png, "size": [img.get_width(), img.get_height()]})
		idx += 1
	results.append({"label": c["label"], "captures": captures})
	stage.queue_free()
	await process_frame
