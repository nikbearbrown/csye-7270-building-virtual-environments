extends SceneTree
# Shader Lab runner. Renders ONE shader on ONE target in a real (windowed) Godot, saves a PNG, prints pixel probes.
# Use check_shader.sh; it passes the arguments after "--".
#
#   --shader <abs path>      the .gdshader file
#   --kind rect|sprite|quad3d   rect: ColorRect fills the view (canvas_item) | sprite: Sprite2D with a test texture (canvas_item)
#                               | quad3d: a 16:9 quad in front of an orthographic camera (spatial)
#   --size 640x360           window size in pixels
#   --set name=value         a uniform: 0.5 | 3 | true | 0.1,0.2,0.3 | #d97757   (cast by the shader's own declared type)
#   --tex name=kind          a sampler2D uniform: gradient | checker | noise | sprite | white | black
#   --sprite-tex kind        the node's own texture for --kind sprite (default sprite): gradient | checker | noise | sprite | white
#   --sprite-scale 1.0       scale of the 128 px sprite (default: fit the view; use 1.0 when pixel distances must be literal)
#   --wait 0.3               seconds of process time to run before the frame is read (TIME advances while it runs)
#   --probe x,y              normalized 0..1 position to read (repeatable); x right, y down
#   --png <abs path>         save the frame
# Prints exactly one line:  RESULT {json}.  Shader compile errors appear in the log as SHADER ERROR (check_shader.sh greps them).

var A := {"set": [], "tex": [], "probe": [], "kind": "rect", "size": "640x360", "wait": 0.3, "png": "", "shader": "", "sprite_tex": "sprite", "sprite_scale": 0.0}

func _initialize() -> void:
	call_deferred("run")

func parse() -> void:
	var a := OS.get_cmdline_user_args()
	var i := 0
	while i < a.size():
		var k: String = a[i]
		if k == "--shader": A["shader"] = a[i + 1]; i += 2
		elif k == "--kind": A["kind"] = a[i + 1]; i += 2
		elif k == "--size": A["size"] = a[i + 1]; i += 2
		elif k == "--set": A["set"].append(a[i + 1]); i += 2
		elif k == "--tex": A["tex"].append(a[i + 1]); i += 2
		elif k == "--probe": A["probe"].append(a[i + 1]); i += 2
		elif k == "--wait": A["wait"] = float(a[i + 1]); i += 2
		elif k == "--png": A["png"] = a[i + 1]; i += 2
		elif k == "--sprite-tex": A["sprite_tex"] = a[i + 1]; i += 2
		elif k == "--sprite-scale": A["sprite_scale"] = float(a[i + 1]); i += 2
		else: i += 1

func make_image(kind: String, n: int = 256) -> Image:
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	match kind:
		"gradient":
			for y in n:
				for x in n:
					img.set_pixel(x, y, Color(x / float(n - 1), y / float(n - 1), 0.0, 1.0))
		"checker":
			for y in n:
				for x in n:
					var on := ((x / (n / 8)) + (y / (n / 8))) % 2 == 0
					img.set_pixel(x, y, Color("#FAF9F5") if on else Color("#5FA391"))
		"noise":
			var fn := FastNoiseLite.new()
			fn.seed = 7
			fn.frequency = 0.02
			img = fn.get_image(n, n)
			img.convert(Image.FORMAT_RGBA8)
		"white":
			img.fill(Color.WHITE)
		"black":
			img.fill(Color.BLACK)
		_: # "sprite": a plain teal blob with two cream eyes, transparent padding all round (outline/edge tests need padding)
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

func cast(value: String, type: int) -> Variant:
	var parts := value.split(",")
	if type == TYPE_FLOAT: return float(value)
	if type == TYPE_INT: return int(value)
	if type == TYPE_BOOL: return value == "true"
	if type == TYPE_COLOR:
		if value.begins_with("#"): return Color(value)
		return Color(float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]) if parts.size() > 3 else 1.0)
	if type == TYPE_VECTOR2: return Vector2(float(parts[0]), float(parts[1]))
	if type == TYPE_VECTOR3: return Vector3(float(parts[0]), float(parts[1]), float(parts[2]))
	if type == TYPE_VECTOR4: return Vector4(float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]))
	return value

func run() -> void:
	parse()
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))   # warm light grey: far from ink, so GATE T does not read the stage as text
	var wh := String(A["size"]).split("x")
	var W := int(wh[0])
	var H := int(wh[1])
	root.size = Vector2i(W, H)
	var code := FileAccess.get_file_as_string(A["shader"])
	if code == "":
		print("RESULT " + JSON.stringify({"ok": false, "error": "cannot read shader " + String(A["shader"])}))
		quit(2)
		return
	var shader := Shader.new()
	shader.code = code
	var mat := ShaderMaterial.new()
	mat.shader = shader
	var unis := shader.get_shader_uniform_list()
	var uni_names: Array = []
	for u in unis:
		uni_names.append(String(u["name"]) + ":" + str(u["type"]))
		for s in A["set"]:
			var kv := String(s).split("=", true, 1)
			if kv[0] == String(u["name"]):
				mat.set_shader_parameter(kv[0], cast(kv[1], int(u["type"])))
	for t in A["tex"]:
		var kv := String(t).split("=", true, 1)
		mat.set_shader_parameter(kv[0], ImageTexture.create_from_image(make_image(kv[1])))

	var stage: Node
	var kind: String = A["kind"]
	if kind == "quad3d":
		var s3 := Node3D.new()
		var cam := Camera3D.new()
		cam.projection = Camera3D.PROJECTION_ORTHOGONAL
		cam.size = 2.0
		cam.position = Vector3(0, 0, 3)
		s3.add_child(cam)
		cam.current = true
		var q := QuadMesh.new()
		q.size = Vector2(2.0 * W / H, 2.0)
		var mi := MeshInstance3D.new()
		mi.mesh = q
		mi.material_override = mat
		s3.add_child(mi)
		var env := Environment.new()
		env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
		env.ambient_light_color = Color.WHITE
		env.ambient_light_energy = 1.0
		var we := WorldEnvironment.new()
		we.environment = env
		s3.add_child(we)
		stage = s3
	elif kind == "sprite":
		var sp := Sprite2D.new()
		sp.texture = ImageTexture.create_from_image(make_image(A["sprite_tex"], 128))
		sp.position = Vector2(W / 2.0, H / 2.0)
		var sc := minf(W, H) * 0.8 / 128.0
		if float(A["sprite_scale"]) > 0.0:
			sc = float(A["sprite_scale"])
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
	while elapsed < float(A["wait"]):
		await process_frame
		elapsed += root.get_process_delta_time()
	await process_frame
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var probes: Array = []
	for p in A["probe"]:
		var xy := String(p).split(",")
		var px := clampi(int(float(xy[0]) * (img.get_width() - 1)), 0, img.get_width() - 1)
		var py := clampi(int(float(xy[1]) * (img.get_height() - 1)), 0, img.get_height() - 1)
		var c := img.get_pixel(px, py)
		probes.append({"at": [float(xy[0]), float(xy[1])], "px": [px, py], "rgba": [snappedf(c.r, 0.0001), snappedf(c.g, 0.0001), snappedf(c.b, 0.0001), snappedf(c.a, 0.0001)]})
	if String(A["png"]) != "":
		DirAccess.make_dir_recursive_absolute(String(A["png"]).get_base_dir())
		img.save_png(A["png"])
	print("RESULT " + JSON.stringify({"ok": true, "engine": Engine.get_version_info()["string"], "kind": kind, "size": [img.get_width(), img.get_height()],
		"renderer": RenderingServer.get_current_rendering_method(), "uniforms": uni_names, "waited_s": snappedf(elapsed, 0.001), "probes": probes, "png": A["png"]}))
	quit(0)
