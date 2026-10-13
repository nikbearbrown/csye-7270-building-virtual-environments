extends SceneTree
# runner_plus.gd: the Shader Lab's runner.gd (series folder lab/) extended for the planning checks of the "Textures and Color" film ONLY.
# The Lab itself is unchanged. Added: more texture kinds (tiny4, tiny4b, burn_ramp, noise2d, mid_grey), --hdr2d, --bg, --size, --modulate, --probe-px.
# Usage (through the scratch project): godot --path <proj> [--rendering-method forward_plus|mobile|gl_compatibility] --script res://runner_plus.gd -- --shader <abs path> [options]
#   --kind rect|sprite|quad3d     --set name=value     --tex name=kind     --sprite-tex kind     --sprite-scale S     --wait SECONDS
#   --probe x,y (0..1)            --png <abs path>     --size 640x360       --hdr2d   (Viewport.use_hdr_2d = true; probes/PNG are converted to what the screen shows)
# Prints one line: RESULT {json}.

var A := {"set": [], "tex": [], "probe": [], "kind": "rect", "size": "640x360", "wait": 0.3, "png": "", "shader": "", "sprite_tex": "sprite", "sprite_scale": 0.0, "hdr2d": false, "modulate": "", "rect_color": ""}

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
		elif k == "--modulate": A["modulate"] = a[i + 1]; i += 2
		elif k == "--rect-color": A["rect_color"] = a[i + 1]; i += 2
		elif k == "--hdr2d": A["hdr2d"] = true; i += 1
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
		"mid_grey":
			img.fill(Color(0.5, 0.5, 0.5, 1.0))
		"tiny_f":
			# 6 x 6 texels: a cream letter F on teal, with a one-texel teal margin (an F is asymmetric, so a flip or a mirror is obvious). x across, y down:
			#   . . . . . .
			#   . C C C C .
			#   . C . . . .
			#   . C C C . .
			#   . C . . . .
			#   . . . . . .      (C = cream, . = teal)
			img = Image.create(6, 6, false, Image.FORMAT_RGBA8)
			img.fill(Color("#5FA391"))
			for c in [[1, 1], [2, 1], [3, 1], [4, 1], [1, 2], [1, 3], [2, 3], [3, 3], [1, 4]]:
				img.set_pixel(c[0], c[1], Color("#FAF9F5"))
		"swatches":
			# 2 x 2 flat patches, all mid-tones (so the effects keep a mid-tone floor): rose, leaf green / sky blue, sand (no channel below 0.34; no patch near the terracotta accent)
			img = Image.create(n, n, false, Image.FORMAT_RGBA8)
			var sw := [Color("#E6598C"), Color("#66A659"), Color("#6680D9"), Color("#E0B04A")]
			for y in n:
				for x in n:
					img.set_pixel(x, y, sw[(1 if x >= n / 2 else 0) + (2 if y >= n / 2 else 0)])
		"ramp_grey":
			# 256 x 256: a grey ramp left to right, value = x / 255 (the same number in red, green and blue)
			for y in n:
				for x in n:
					var v := x / float(n - 1)
					img.set_pixel(x, y, Color(v, v, v, 1.0))
		"tiny4b":
			# 4 x 4 greyscale ramp left to right: texel centres at 0.125, 0.375, 0.625, 0.875 of the width
			img = Image.create(4, 4, false, Image.FORMAT_RGBA8)
			for y in 4:
				for x in 4:
					var v := float(x) / 3.0
					img.set_pixel(x, y, Color(v, v, v, 1.0))
		"burn_ramp":
			# the burning-edge colour table: 256 x 1, dark red -> orange -> yellow (built from a Gradient, like a GradientTexture1D)
			var g := Gradient.new()
			g.offsets = PackedFloat32Array([0.0, 0.5, 1.0])
			g.colors = PackedColorArray([Color("#8A2A12"), Color("#F08A2C"), Color("#F7D46B")])
			img = Image.create(256, 1, false, Image.FORMAT_RGBA8)
			for x in 256:
				img.set_pixel(x, 0, g.sample(x / 255.0))
		_: # "sprite": a plain teal blob with two cream eyes, transparent padding all round
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

func make_texture(kind: String) -> Texture2D:
	if kind == "noise2d":
		var nt := NoiseTexture2D.new()
		var fn := FastNoiseLite.new()
		fn.seed = 7
		fn.frequency = 0.02
		nt.noise = fn
		nt.width = 256
		nt.height = 256
		return nt          # generated on a thread; the caller waits for `changed`
	if kind == "burn_ramp_tex":
		var g := Gradient.new()
		g.offsets = PackedFloat32Array([0.0, 0.5, 1.0])
		g.colors = PackedColorArray([Color("#8A2A12"), Color("#F08A2C"), Color("#F7D46B")])
		var gt := GradientTexture1D.new()
		gt.gradient = g
		gt.width = 256
		return gt
	return ImageTexture.create_from_image(make_image(kind))

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
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	var wh := String(A["size"]).split("x")
	var W := int(wh[0])
	var H := int(wh[1])
	root.size = Vector2i(W, H)
	if A["hdr2d"]:
		root.use_hdr_2d = true
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
	var pending_noise: Array = []
	for t in A["tex"]:
		var kv := String(t).split("=", true, 1)
		var tx := make_texture(kv[1])
		mat.set_shader_parameter(kv[0], tx)
		if kv[1] == "noise2d":
			pending_noise.append(tx)

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
		if String(A["modulate"]) != "":
			sp.modulate = Color(String(A["modulate"]))
		sp.material = mat
		stage = sp
	else:
		var cr := ColorRect.new()
		cr.size = Vector2(W, H)
		if String(A["rect_color"]) != "":
			cr.color = Color(String(A["rect_color"]))
		cr.material = mat
		stage = cr
	root.add_child(stage)

	for nt in pending_noise:
		var guard := 0
		while nt.get_image() == null and guard < 600:
			await process_frame
			guard += 1
	var elapsed := 0.0
	await process_frame
	while elapsed < float(A["wait"]):
		await process_frame
		elapsed += root.get_process_delta_time()
	await process_frame
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var raw_fmt := img.get_format()
	if A["hdr2d"]:
		# Viewport.get_texture() is LINEAR with HDR 2D; the screen shows linear_to_srgb(value). Convert so probes and PNG are "what the screen shows".
		img.convert(Image.FORMAT_RGBAF)
		for yy in img.get_height():
			for xx in img.get_width():
				var cc := img.get_pixel(xx, yy)
				img.set_pixel(xx, yy, cc.linear_to_srgb())
		img.convert(Image.FORMAT_RGBA8)
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
		"renderer": RenderingServer.get_current_rendering_method(), "hdr2d": A["hdr2d"], "raw_image_format": raw_fmt, "uniforms": uni_names, "waited_s": snappedf(elapsed, 0.001), "probes": probes, "png": A["png"]}))
	quit(0)
