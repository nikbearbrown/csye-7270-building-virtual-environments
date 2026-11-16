extends SceneTree
# Shader capture harness (built 2026-10-14 in the Godot Shaders pilot build). Extends runner.gd (same targets, same test textures).
# Renders ONE shader (or a scene script) to a PNG sequence at the film's frame rate, or to one PNG. Use capture_shader.sh: it takes the Lab lock,
# passes the arguments after "--", runs ffmpeg and prints the harness report.
#
# Route: SubViewport NATIVE-SIZE (proven for Signal Garden): a 3840x2160 SubViewport over a 1280x720 logical canvas (size_2d_override),
#        so nodes are laid out in 1280x720 units and drawn at 3x. Shaders that read window pixels (FRAGCOORD, SCREEN_PIXEL_SIZE,
#        LIGHT_POSITION, LIGHT_VERTEX) use --native instead: a 1920x1080 SubViewport at scale 1 (their numbers depend on the size shown).
# Time: offline at a fixed tick rate. Run with --fixed-fps (capture_shader.sh does), the render loop is switched off and every captured frame is
#        one process_frame plus RenderingServer.force_draw(false, 1/fps). Shader TIME advances only inside a draw, by that draw's step, so TIME
#        rises exactly 1.0 per fps frames. This says NOTHING about real-time frame rate.
#
# Options (all after "--"):
#   --shader <abs path>        the .gdshader (omit when --scene builds everything)
#   --kind rect|sprite         rect: ColorRect fills the canvas | sprite: Sprite2D with a test texture      (default rect)
#   --scene <abs path.gd>      a scene script (extends Node). Added to the stage; optional harness_setup(ctx: Dictionary), where ctx has
#                              stage, shader (Shader or null), shader_code, logical (Vector2), and the script may fill ctx["materials"] (name -> ShaderMaterial)
#   --out <dir>                frames directory (frame_00000.png ...)      --png <abs path>  one still instead (the last frame)
#   --length <s>               clip length in seconds (default 1.0)        --fps 30
#   --native                   1920x1080 SubViewport at scale 1 (window-pixel shaders)       --size WxH  override the capture size
#   --set name=value           uniform at t=0 (cast by the shader's own declared type)
#   --animate name:t0:v0,t1:v1,...   piecewise-linear schedule of a float uniform; "name:from:to" sweeps linearly across the clip.
#                              A time written with a trailing f (0.5f) is a fraction of --length. A panel name is "panel.name".
#   --steps name:t0:v0,t1:v1,...     stepped schedule: v0 from t0 until t1, then v1 (no ramp); the frame at t1 already shows v1
#   --set-at T:name=value      set a uniform at time T          --call-at T:method   call a method on the scene script at time T
#   --material-at T[:SHADER_B] assign the run's shader at T to a node that started with no material (sprite kind), or swap A for B (abs path)
#   --key-at T:KEYNAME         one physical key press (and release 3 frames later) pushed into the stage at time T, logged: scripted input
#   --tex name=kind            sampler2D uniform from a test texture: gradient|checker|noise|sprite|white|black|swatches|ramp_grey|tiny_f
#   --sprite-tex kind          the sprite node's own texture (128 px)     --sprite-scale 1.0   (default: fit 80% of the canvas height)
#   --time-origin S            advance the shader clock by S seconds before the first captured frame (a loop that is on a pose at 50%)
#   --probe-at T:x,y           print the pixel (0..1 floats) at normalized x,y of the frame nearest T (repeatable); the report is the RESULT line
#   --tail S                  extra seconds of frames after --length (events stay fractions of --length); the film's player never runs off the end
#   --hold-clock S            the shader clock stays at 0 for the first S seconds of the clip (draws with step 0): TIME then starts at S, as if
#                              the scene had just loaded; used so an event that depends on TIME lands on a chosen moment of the beat
#   --warmup 6                 draws before frame 0 (step 0, so TIME does not move); frame 0 of a SubViewport recording lacks pictures otherwise
#   --sprite-res N            the sprite texture's size in px (default 128: the Lab's) with --linear for linear filtering (a smooth blob at 4K)
#   --kind quad3d             the Lab's quad3d target (a frame-sized quad, orthographic camera, white ambient) for spatial shaders
#   scene scripts may define harness_frame(t) (called before every draw with the capture time in seconds)
#   a --renderer is passed by capture_shader.sh (forward_plus | gl_compatibility)
# Prints one line:  RESULT {json}

var A := {"set": [], "tex": [], "probe_at": [], "animate": [], "steps": [], "set_at": [], "call_at": [], "key_at": [],
	"kind": "rect", "scene": "", "shader": "", "out": "", "png": "", "length": 1.0, "fps": 30, "native": false, "size": "",
	"sprite_tex": "sprite", "sprite_scale": 0.0, "material_at": "", "time_origin": 0.0, "warmup": 6, "hold_clock": 0.0, "tail": 0.0, "sprite_res": 128, "linear": false}

var stage: SubViewport
var materials := {}
var node_for_material: Node = null
var scene_node: Node = null
var shader_a: Shader = null
var log_lines: Array = []

func _initialize() -> void:
	call_deferred("run")

func parse() -> void:
	var a := OS.get_cmdline_user_args()
	var i := 0
	while i < a.size():
		var k: String = a[i]
		var v: String = a[i + 1] if i + 1 < a.size() else ""
		match k:
			"--shader": A["shader"] = v; i += 2
			"--kind": A["kind"] = v; i += 2
			"--scene": A["scene"] = v; i += 2
			"--out": A["out"] = v; i += 2
			"--png": A["png"] = v; i += 2
			"--length": A["length"] = float(v); i += 2
			"--fps": A["fps"] = int(v); i += 2
			"--size": A["size"] = v; i += 2
			"--native": A["native"] = true; i += 1
			"--set": A["set"].append(v); i += 2
			"--animate": A["animate"].append(v); i += 2
			"--steps": A["steps"].append(v); i += 2
			"--set-at": A["set_at"].append(v); i += 2
			"--call-at": A["call_at"].append(v); i += 2
			"--key-at": A["key_at"].append(v); i += 2
			"--tex": A["tex"].append(v); i += 2
			"--probe-at": A["probe_at"].append(v); i += 2
			"--sprite-tex", "--texture": A["sprite_tex"] = v; i += 2
			"--sprite-scale": A["sprite_scale"] = float(v); i += 2
			"--material-at": A["material_at"] = v; i += 2
			"--time-origin": A["time_origin"] = float(v); i += 2
			"--warmup": A["warmup"] = int(v); i += 2
			"--hold-clock": A["hold_clock"] = float(v); i += 2
			"--tail": A["tail"] = float(v); i += 2
			"--sprite-res": A["sprite_res"] = int(v); i += 2
			"--linear": A["linear"] = true; i += 1
			_: i += 1

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
		"ramp_grey":
			for y in n:
				for x in n:
					var g := x / float(n - 1)
					img.set_pixel(x, y, Color(g, g, g, 1.0))
		_: # "sprite": a teal blob with two cream eyes and transparent padding (same as runner.gd)
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

func tnum(s: String, length: float) -> float:
	# "2.5" seconds, or "0.5f" a fraction of the clip
	if s.ends_with("f"):
		return float(s.substr(0, s.length() - 1)) * length
	return float(s)

# a schedule: {"target": "main"|panel, "name": uniform, "pts": [[t, v], ...], "stepped": bool}
func parse_schedule(spec: String, stepped: bool, length: float) -> Dictionary:
	var parts := spec.split(":")
	var full := parts[0]
	var target := "main"
	var name := full
	if full.contains("."):
		target = full.get_slice(".", 0)
		name = full.get_slice(".", 1)
	var pts: Array = []
	if parts.size() == 3 and not parts[1].ends_with("f") and not parts[2].contains(","):
		# name:from:to = linear sweep across the whole clip
		pts = [[0.0, float(parts[1])], [length, float(parts[2])]]
	else:
		# name:t0:v0,t1:v1,...  (re-join the pieces after the name: t0 : v0,t1 : v1 ...)
		var rest := spec.substr(parts[0].length() + 1)
		for pair in rest.split(","):
			var tv := pair.split(":")
			pts.append([tnum(tv[0], length), float(tv[1])])
	return {"target": target, "name": name, "pts": pts, "stepped": stepped}

func sample(sch: Dictionary, t: float) -> float:
	var pts: Array = sch["pts"]
	if t <= pts[0][0]:
		return pts[0][1]
	for i in range(1, pts.size()):
		if t <= pts[i][0] + 1e-9:
			if sch["stepped"]:
				# the frame at pts[i].t already shows pts[i].v
				return pts[i][1] if t >= pts[i][0] - 1e-9 else pts[i - 1][1]
			var t0: float = pts[i - 1][0]
			var t1: float = pts[i][0]
			if t1 <= t0:
				return pts[i][1]
			return lerpf(pts[i - 1][1], pts[i][1], (t - t0) / (t1 - t0))
	return pts[pts.size() - 1][1]

func set_param(target: String, name: String, value: Variant) -> void:
	if materials.has(target):
		(materials[target] as ShaderMaterial).set_shader_parameter(name, value)
	else:
		log_lines.append("WARNING no material named " + target + " for uniform " + name)

func key_event(code_name: String, down: bool) -> void:
	var code := OS.find_keycode_from_string(code_name)
	var ev := InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.pressed = down
	stage.push_input(ev)
	log_lines.append("scripted key %s %s" % [code_name, "down" if down else "up"])

func run() -> void:
	parse()
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))   # the Lab stage: warm light grey, far from ink
	var fps: int = A["fps"]
	var length: float = A["length"]
	var frames := maxi(1, int(round((length + float(A["tail"])) * fps)))
	var cap := Vector2i(3840, 2160)
	var logical := Vector2(1280, 720)
	if A["native"]:
		cap = Vector2i(1920, 1080)
		logical = Vector2(1920, 1080)
	if String(A["size"]) != "":
		var wh := String(A["size"]).split("x")
		cap = Vector2i(int(wh[0]), int(wh[1]))
		if not A["native"]:
			logical = Vector2(1280, 1280.0 * cap.y / cap.x)
		else:
			logical = Vector2(cap)

	stage = SubViewport.new()
	stage.set_script(load("res://capture_stage.gd"))   # content_scale_size shim (Window-only property)
	stage.size = cap
	if not A["native"]:
		stage.size_2d_override = Vector2i(logical)
		stage.size_2d_override_stretch = true
	stage.own_world_3d = true                          # 3D scenes get their own world inside the capture viewport
	stage.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	stage.handle_input_locally = true
	root.add_child(stage)
	var preview := TextureRect.new()
	preview.texture = stage.get_texture()
	preview.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	preview.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	preview.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	root.add_child(preview)
	DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_ALWAYS_ON_TOP, true)

	# ---- the shader and its material
	var code := ""
	if String(A["shader"]) != "":
		code = FileAccess.get_file_as_string(A["shader"])
		if code == "":
			print("RESULT " + JSON.stringify({"ok": false, "error": "cannot read shader " + String(A["shader"])}))
			quit(2)
			return
	var mat: ShaderMaterial = null
	if code != "":
		shader_a = Shader.new()
		shader_a.code = code
		mat = ShaderMaterial.new()
		mat.shader = shader_a
		for u in shader_a.get_shader_uniform_list():
			for s in A["set"]:
				var kv := String(s).split("=", true, 1)
				if kv[0] == String(u["name"]):
					mat.set_shader_parameter(kv[0], cast(kv[1], int(u["type"])))
		for t in A["tex"]:
			var kv := String(t).split("=", true, 1)
			mat.set_shader_parameter(kv[0], ImageTexture.create_from_image(make_image(kv[1])))
		materials["main"] = mat

	var material_at := -1.0
	var shader_b: Shader = null
	if String(A["material_at"]) != "":
		var ma := String(A["material_at"])
		material_at = tnum(ma.get_slice(":", 0), length)
		if ma.contains(":"):
			shader_b = Shader.new()
			shader_b.code = FileAccess.get_file_as_string(ma.substr(ma.find(":") + 1))

	var kind: String = A["kind"]
	if String(A["scene"]) != "":
		var scr: GDScript = load(A["scene"])
		scene_node = Node.new()
		scene_node.set_script(scr)
		var ctx := {"stage": stage, "shader": shader_a, "shader_code": code, "logical": logical, "materials": materials}
		stage.add_child(scene_node)
		if scene_node.has_method("harness_setup"):
			scene_node.call("harness_setup", ctx)
	elif kind == "quad3d":
		# the Lab's quad3d target: a quad the size of the frame in front of an orthographic camera (spatial shaders), ambient light white
		var s3 := Node3D.new()
		var cam3 := Camera3D.new()
		cam3.projection = Camera3D.PROJECTION_ORTHOGONAL
		cam3.size = 2.0
		cam3.position = Vector3(0, 0, 3)
		s3.add_child(cam3)
		cam3.current = true
		var q3 := QuadMesh.new()
		q3.size = Vector2(2.0 * logical.x / logical.y, 2.0)
		var mi3 := MeshInstance3D.new()
		mi3.mesh = q3
		mi3.material_override = mat
		s3.add_child(mi3)
		var env3 := Environment.new()
		env3.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
		env3.ambient_light_color = Color.WHITE
		env3.ambient_light_energy = 1.0
		var we3 := WorldEnvironment.new()
		we3.environment = env3
		s3.add_child(we3)
		stage.add_child(s3)
	elif kind == "sprite":
		var sp := Sprite2D.new()
		sp.texture = ImageTexture.create_from_image(make_image(A["sprite_tex"], int(A["sprite_res"])))
		sp.position = logical / 2.0
		var sc := minf(logical.x, logical.y) * 0.8 / float(A["sprite_res"])
		if float(A["sprite_scale"]) > 0.0:
			sc = float(A["sprite_scale"])
		sp.scale = Vector2(sc, sc)
		sp.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR if A["linear"] else CanvasItem.TEXTURE_FILTER_NEAREST
		if material_at < 0.0:
			sp.material = mat
		node_for_material = sp
		stage.add_child(sp)
	else:
		var cr := ColorRect.new()
		cr.size = logical
		if material_at < 0.0:
			cr.material = mat
		node_for_material = cr
		stage.add_child(cr)

	# ---- schedules
	var schedules: Array = []
	for s in A["animate"]:
		schedules.append(parse_schedule(s, false, length))
	for s in A["steps"]:
		schedules.append(parse_schedule(s, true, length))
	var set_ats: Array = []
	for s in A["set_at"]:
		var t := tnum(String(s).get_slice(":", 0), length)
		var rest := String(s).substr(String(s).find(":") + 1)
		var tgt := "main"
		var nm := rest.get_slice("=", 0)
		if nm.contains("."):
			tgt = nm.get_slice(".", 0)
			nm = nm.get_slice(".", 1)
		set_ats.append({"t": t, "target": tgt, "name": nm, "val": rest.get_slice("=", 1), "done": false})
	var call_ats: Array = []
	for s in A["call_at"]:
		call_ats.append({"t": tnum(String(s).get_slice(":", 0), length), "method": String(s).get_slice(":", 1), "done": false})
	var key_ats: Array = []
	for s in A["key_at"]:
		key_ats.append({"t": tnum(String(s).get_slice(":", 0), length), "key": String(s).get_slice(":", 1), "down_done": false, "up_done": false})
	var probes: Array = []
	for s in A["probe_at"]:
		var t := tnum(String(s).get_slice(":", 0), length)
		var xy := String(s).get_slice(":", 1).split(",")
		probes.append({"t": t, "frame": clampi(int(round(t * fps)), 0, frames - 1), "x": float(xy[0]), "y": float(xy[1])})

	# ---- run: render loop off; one process_frame + one force_draw per step
	RenderingServer.render_loop_enabled = false
	for i in range(int(A["warmup"])):
		await process_frame
		RenderingServer.force_draw(false, 0.0)
	if float(A["time_origin"]) > 0.0:
		await process_frame
		RenderingServer.force_draw(false, float(A["time_origin"]))
	var out_dir: String = A["out"]
	if out_dir != "":
		DirAccess.make_dir_recursive_absolute(out_dir)
	var step := 1.0 / fps
	var last_img: Image = null
	var probe_out: Array = []
	var applied_material := false
	var tween_checks: Array = []
	for f in range(frames):
		var t := f * step
		# uniform schedules
		if scene_node != null and scene_node.has_method("harness_frame"):
			scene_node.call("harness_frame", t)   # a scene's own motion (a swing, a turn) is computed from this clock, never from real time
		for sch in schedules:
			set_param(sch["target"], sch["name"], sample(sch, t))
		for sa in set_ats:
			if not sa["done"] and t >= sa["t"] - 1e-9:
				sa["done"] = true
				var tgt: String = sa["target"]
				if materials.has(tgt):
					var m: ShaderMaterial = materials[tgt]
					var typ := TYPE_FLOAT
					for u in m.shader.get_shader_uniform_list():
						if String(u["name"]) == sa["name"]:
							typ = int(u["type"])
					m.set_shader_parameter(sa["name"], cast(sa["val"], typ))
					log_lines.append("set-at %.2f %s=%s" % [t, sa["name"], sa["val"]])
		# material assignment / swap
		if material_at >= 0.0 and t >= material_at - 1e-9 and not applied_material and node_for_material != null:
			applied_material = true
			if shader_b != null:
				var mb := ShaderMaterial.new()
				mb.shader = shader_b
				node_for_material.material = mb
				materials["main"] = mb
			else:
				node_for_material.material = mat
			log_lines.append("material assigned at %.2f s" % t)
		for ca in call_ats:
			if not ca["done"] and t >= ca["t"] - 1e-9 and scene_node != null:
				ca["done"] = true
				scene_node.call(ca["method"])
				log_lines.append("call-at %.2f %s" % [t, ca["method"]])
		for ka in key_ats:
			if not ka["down_done"] and t >= ka["t"] - 1e-9:
				ka["down_done"] = true
				ka["down_frame"] = f
				key_event(ka["key"], true)
			elif ka["down_done"] and not ka["up_done"] and f >= int(ka["down_frame"]) + 3:
				ka["up_done"] = true
				key_event(ka["key"], false)
		await process_frame
		RenderingServer.force_draw(false, 0.0 if t < float(A["hold_clock"]) - 1e-9 else step)
		var need_img := out_dir != "" or f == frames - 1
		for p in probes:
			if p["frame"] == f:
				need_img = true
		if need_img:
			var img := stage.get_texture().get_image()
			if out_dir != "":
				img.save_png("%s/frame_%05d.png" % [out_dir, f])
			for p in probes:
				if p["frame"] == f:
					var px := clampi(int(p["x"] * (img.get_width() - 1)), 0, img.get_width() - 1)
					var py := clampi(int(p["y"] * (img.get_height() - 1)), 0, img.get_height() - 1)
					var c := img.get_pixel(px, py)
					probe_out.append({"t": snappedf(f * step, 0.001), "at": [p["x"], p["y"]], "rgba": [snappedf(c.r, 0.0001), snappedf(c.g, 0.0001), snappedf(c.b, 0.0001), snappedf(c.a, 0.0001)]})
			if f == frames - 1:
				last_img = img
	if String(A["png"]) != "" and last_img != null:
		DirAccess.make_dir_recursive_absolute(String(A["png"]).get_base_dir())
		last_img.save_png(A["png"])
	print("RESULT " + JSON.stringify({"ok": true, "engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(),
		"kind": kind, "scene": A["scene"], "capture_size": [cap.x, cap.y], "logical": [logical.x, logical.y], "fps": fps, "frames": frames,
		"native": A["native"], "probes": probe_out, "events": log_lines, "out": out_dir, "png": A["png"],
		"note": "offline at a fixed tick rate; says nothing about real-time frame rate"}))
	quit(0)
