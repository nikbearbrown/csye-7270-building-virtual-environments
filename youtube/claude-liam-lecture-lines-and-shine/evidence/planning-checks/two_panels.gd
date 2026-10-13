extends SceneTree
# two_panels.gd: renders one or two shader panels side by side on the Lab stage color and saves a PNG, printing probe colors.
# Run (windowed, as the Lab does):  godot --path <scratch project> --script res://two_panels.gd -- --cfg /abs/path/config.json
# Config JSON:
#   {"out": "/abs/out.png",
#    "panels": [{"shader": "/abs/x.gdshader", "kind": "card|blob|wide", "center": [cx, cy], "size": [w, h], "uniforms": {"angle": 30.0, "center": [0.5, 0.0]}}, ...],
#    "probes": [[x_px, y_px], ...],            # frame pixels (640 x 360 logical frame)
#    "wait_frames": 4}
# kind card = a Sprite2D with a plain white 128 px texture (the shader assigns COLOR itself); blob = the Lab's teal test sprite with
# transparent padding; wide = a ColorRect of the given size (UV runs 0 to 1 over a wide shape). Same stage color as lab/runner.gd.

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func make_tex(kind: String, n: int = 128) -> ImageTexture:
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	if kind == "blob":
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
	else:
		img.fill(Color.WHITE)
	return ImageTexture.create_from_image(img)

func run() -> void:
	var cfg_path := ""
	var a := OS.get_cmdline_user_args()
	var i := 0
	while i < a.size():
		if a[i] == "--cfg":
			cfg_path = a[i + 1]
			i += 2
		else:
			i += 1
	var cfg = JSON.parse_string(FileAccess.get_file_as_string(cfg_path))
	if cfg == null:
		print("RESULT " + JSON.stringify({"ok": false, "error": "cannot read config " + cfg_path}))
		quit(2)
		return
	root.size = Vector2i(640, 360)
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	for pn in cfg["panels"]:
		var sh := Shader.new()
		sh.code = FileAccess.get_file_as_string(pn["shader"])
		var mat := ShaderMaterial.new()
		mat.shader = sh
		var uni: Dictionary = pn.get("uniforms", {})
		for k in uni:
			var v = uni[k]
			if v is Array:
				mat.set_shader_parameter(k, Vector2(v[0], v[1]))
			else:
				mat.set_shader_parameter(k, float(v))
		var kind: String = pn["kind"]
		var ctr := Vector2(pn["center"][0], pn["center"][1])
		var sz := Vector2(pn["size"][0], pn["size"][1])
		if kind == "wide":
			var cr := ColorRect.new()
			cr.size = sz
			cr.position = ctr - sz / 2.0
			cr.material = mat
			root.add_child(cr)
		else:
			var sp := Sprite2D.new()
			sp.texture = make_tex(kind)
			sp.position = ctr
			sp.scale = Vector2(sz.x / 128.0, sz.y / 128.0)
			sp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
			sp.material = mat
			root.add_child(sp)
	await frames(int(cfg.get("wait_frames", 4)))
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	if cfg.has("out"):
		DirAccess.make_dir_recursive_absolute(String(cfg["out"]).get_base_dir())
		img.save_png(cfg["out"])
	var probes: Array = []
	for pr in cfg.get("probes", []):
		var px := clampi(int(pr[0]), 0, img.get_width() - 1)
		var py := clampi(int(pr[1]), 0, img.get_height() - 1)
		var c := img.get_pixel(px, py)
		probes.append({"px": [px, py], "rgba": [snappedf(c.r, 0.0001), snappedf(c.g, 0.0001), snappedf(c.b, 0.0001), snappedf(c.a, 0.0001)]})
	print("RESULT " + JSON.stringify({"ok": true, "engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(),
		"size": [img.get_width(), img.get_height()], "out": cfg.get("out", ""), "probes": probes}))
	quit(0)
