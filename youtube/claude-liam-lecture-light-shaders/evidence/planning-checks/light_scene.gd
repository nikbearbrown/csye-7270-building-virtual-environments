extends Node2D
# light_scene.gd: the capture scenes of the Light Shaders film. 1920x1080 canvas, scale 1 (screen-space shader numbers are PHYSICAL pixels, see CAPTURE-PLAN.md).
# One script, every capture. The captures are data: captures.json (id -> scene description + timeline). Nothing here is film narration.
#
#   as a child of a SubViewport (verification):
#       var s = load("res://light_scene.gd").new(); s.manual = true; s.setup("C05", shader_dir, captures_json_path); viewport.add_child(s); s.step(1.0/30.0) ...
#   as the main scene under Movie Maker (the build session's recording, offline at a fixed tick rate):
#       godot --path <project> --write-movie out.png --fixed-fps 30 --quit-after N -- --id C05 --shaders <abs lab-shaders dir> --captures <abs captures.json>
#
# The cast (same in every scene): a tiled floor (dusk-tinted), the teal test sprite ("blob"), a pale bulb disc that marks a lamp, PointLight2D lamps with the docs' own
# soft texture (a radial GradientTexture2D, opaque white to transparent white). Everything that moves is a function of the capture clock t (30 steps a second).

const W := 1920
const H := 1080
const DUSK := Color(0.50, 0.55, 0.72)
const WARM := Color(1.0, 0.86, 0.55)

var cid := ""
var cfg: Dictionary = {}
var shader_dir := ""
var t := 0.0
var manual := false
var nodes: Dictionary = {}          # name -> Node
var lamps: Array = []               # PointLight2D
var mods: CanvasModulate
var cam: Camera2D
var applied: Dictionary = {}        # shader switch index -> true once fired
var shader_cache: Dictionary = {}

func setup(id: String, shaders: String, captures_path: String) -> void:
	cid = id
	shader_dir = shaders
	var all = JSON.parse_string(FileAccess.get_file_as_string(captures_path))
	cfg = all[id]

func _ready() -> void:
	if cfg.is_empty():
		var a := OS.get_cmdline_user_args()
		var cp := ""
		for i in range(a.size()):
			if a[i] == "--id": cid = a[i + 1]
			if a[i] == "--shaders": shader_dir = a[i + 1]
			if a[i] == "--captures": cp = a[i + 1]
		setup(cid, shader_dir, cp)
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	build()

func _process(delta: float) -> void:
	if not manual:
		step(delta)

# ---------------------------------------------------------------- textures
static func tiles_texture(width: int = W) -> ImageTexture:
	var im := Image.create(width, H, false, Image.FORMAT_RGBA8)
	im.fill(Color(0.72, 0.70, 0.64))                      # grout
	var tile := 120
	for ty in range(0, H, tile):
		for tx in range(0, width, tile):
			var odd := ((tx / tile) + (ty / tile)) % 2 == 1
			var c := Color(0.80, 0.78, 0.72) if odd else Color(0.87, 0.85, 0.79)
			im.fill_rect(Rect2i(tx + 2, ty + 2, tile - 4, tile - 4), c)
	return ImageTexture.create_from_image(im)

static func plain_texture(c: Color, n: int = 64) -> ImageTexture:
	var im := Image.create(n, n, false, Image.FORMAT_RGBA8)
	im.fill(c)
	return ImageTexture.create_from_image(im)

static func blob_texture(n: int = 128) -> ImageTexture:
	var im := Image.create(n, n, false, Image.FORMAT_RGBA8)
	im.fill(Color(0, 0, 0, 0))
	var c := Vector2(n / 2.0, n / 2.0)
	for y in n:
		for x in n:
			var d := Vector2(x, y).distance_to(c)
			if d < n * 0.30:
				im.set_pixel(x, y, Color("#5FA391"))
			var e1 := Vector2(x, y).distance_to(c + Vector2(-n * 0.10, -n * 0.06))
			var e2 := Vector2(x, y).distance_to(c + Vector2(n * 0.10, -n * 0.06))
			if e1 < n * 0.035 or e2 < n * 0.035:
				im.set_pixel(x, y, Color("#FAF9F5"))
	return ImageTexture.create_from_image(im)

static func disc_texture(c: Color, n: int = 64) -> ImageTexture:
	var im := Image.create(n, n, false, Image.FORMAT_RGBA8)
	im.fill(Color(0, 0, 0, 0))
	var ctr := Vector2(n / 2.0 - 0.5, n / 2.0 - 0.5)
	for y in n:
		for x in n:
			if Vector2(x, y).distance_to(ctr) < n * 0.48:
				im.set_pixel(x, y, c)
	return ImageTexture.create_from_image(im)

static func radial_texture(n: int = 256) -> GradientTexture2D:
	var g := Gradient.new()
	g.set_color(0, Color(1, 1, 1, 1))
	g.set_color(1, Color(1, 1, 1, 0))
	var tx := GradientTexture2D.new()
	tx.gradient = g
	tx.fill = GradientTexture2D.FILL_RADIAL
	tx.fill_from = Vector2(0.5, 0.5)
	tx.fill_to = Vector2(1.0, 0.5)
	tx.width = n
	tx.height = n
	return tx

# ---------------------------------------------------------------- helpers
func col(v: Variant) -> Color:
	if v is String:
		match String(v):
			"dusk": return DUSK
			"warm": return WARM
			"white", "off": return Color.WHITE
			_: return Color(String(v))
	if v is Array:
		return Color(v[0], v[1], v[2], v[3] if v.size() > 3 else 1.0)
	return Color.WHITE

func shader_material(file: String) -> ShaderMaterial:
	if file == "" or file == "none":
		return null
	if not shader_cache.has(file):
		var sh := Shader.new()
		sh.code = FileAccess.get_file_as_string(file if file.begins_with("/") else shader_dir.path_join(file))
		shader_cache[file] = sh
	var m := ShaderMaterial.new()
	m.shader = shader_cache[file]
	return m

func unshaded_material() -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = "shader_type canvas_item;\nrender_mode unshaded;\n"
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

func make_lamp(d: Dictionary) -> PointLight2D:
	var l := PointLight2D.new()
	l.texture = radial_texture(256) if String(d.get("texture", "radial")) == "radial" else plain_texture(Color.WHITE, 128)
	l.texture_scale = float(d.get("scale", 4.0))
	l.energy = float(d.get("energy", 1.0))
	l.color = col(d.get("color", "warm"))
	l.position = Vector2(float(d["x"]), float(d["y"]))
	l.height = float(d.get("height", 0.0))
	l.enabled = not d.has("appear")
	return l

# ---------------------------------------------------------------- build
func build() -> void:
	mods = CanvasModulate.new()
	mods.color = col(cfg.get("ambient", "dusk"))
	add_child(mods)
	nodes["mods"] = mods
	var floor_kind := String(cfg.get("floor", "tiles"))
	var extra := int(cfg.get("floor_extra", 0))                  # extra floor width on each side, for scenes where the floor slides
	var surf: Texture2D
	match floor_kind:
		"grey": surf = plain_texture(col(cfg.get("floor_color", [0.5, 0.5, 0.5])), 64)
		_: surf = tiles_texture(W + 2 * extra)
	if bool(cfg.get("split", false)):
		# two halves of one floor, so one half can wear a shader and the other the default; the seam must be invisible
		for i in range(2):
			var s := Sprite2D.new()
			s.texture = surf
			s.centered = false
			s.region_enabled = true
			s.region_rect = Rect2(i * W / 2, 0, W / 2, H)
			s.position = Vector2(i * W / 2, 0)
			add_child(s)
			nodes["floor_left" if i == 0 else "floor_right"] = s
		nodes["floor"] = nodes["floor_right"]
	else:
		var f := Sprite2D.new()
		f.texture = surf
		f.centered = false
		f.position = Vector2(-extra, 0)
		if floor_kind == "grey":
			f.scale = Vector2(W / 64.0, H / 64.0)
		add_child(f)
		nodes["floor"] = f
	if cfg.has("card"):
		var c: Dictionary = cfg["card"]
		var s2 := Sprite2D.new()
		s2.texture = plain_texture(col(c.get("color", "white")), 64)
		s2.position = Vector2(c.get("x", 960), c.get("y", 540))
		s2.scale = Vector2(c.get("w", 640) / 64.0, c.get("h", 400) / 64.0)
		add_child(s2)
		nodes["card"] = s2
	for p in cfg.get("props", []):
		var d: Dictionary = p
		match String(d["kind"]):
			"blob":
				var b := Sprite2D.new()
				b.texture = blob_texture(128)
				b.position = Vector2(d["x"], d["y"])
				b.scale = Vector2(d.get("scale", 2.0), d.get("scale", 2.0))
				add_child(b)
				nodes[String(d.get("name", "blob"))] = b
			"bulb":
				var bu := Sprite2D.new()
				bu.texture = disc_texture(col(d.get("color", [1.0, 0.93, 0.62])), 64)
				bu.position = Vector2(d["x"], d["y"])
				bu.scale = Vector2(d.get("scale", 0.9), d.get("scale", 0.9))
				bu.z_index = 5
				if bool(d.get("unshaded", false)):
					bu.material = unshaded_material()
				add_child(bu)
				nodes[String(d.get("name", "bulb"))] = bu
			"outline":
				var ln := Line2D.new()
				ln.width = float(d.get("width", 6.0))
				ln.default_color = col(d.get("color", [0.42, 0.42, 0.42, 1.0]))
				ln.z_index = 6
				ln.material = unshaded_material()
				add_child(ln)
				nodes[String(d.get("name", "outline"))] = ln
	for ld in cfg.get("lamps", []):
		var l := make_lamp(ld)
		add_child(l)
		lamps.append(l)
	if bool(cfg.get("lamp_bulbs", false)):
		for i in range(lamps.size()):
			var bu2 := Sprite2D.new()
			bu2.texture = disc_texture(Color(1.0, 0.95, 0.7), 64)
			bu2.scale = Vector2(0.5, 0.5)
			bu2.z_index = 5
			bu2.material = unshaded_material()
			add_child(bu2)
			nodes["lamp_bulb_%d" % i] = bu2
	cam = Camera2D.new()
	cam.position = Vector2(W / 2.0, H / 2.0)
	add_child(cam)
	cam.make_current()
	var idx := 0
	for e in cfg.get("shader", []):
		var d2: Dictionary = e
		if float(d2.get("at", 0.0)) <= 0.0:
			assign(d2)
			applied["sh%d" % idx] = true
		idx += 1
	step(0.0)

func assign(d: Dictionary) -> void:
	var n: Node = nodes.get(String(d["node"]))
	if n == null:
		return
	var m := shader_material(String(d.get("file", "")))
	(n as CanvasItem).material = m
	if m != null and d.has("uniforms"):
		for k in d["uniforms"]:
			m.set_shader_parameter(k, d["uniforms"][k])

# ---------------------------------------------------------------- the clock
func ramp(a: float, b: float, t0: float, t1: float, mode: String = "linear") -> float:
	var u := clampf((t - t0) / maxf(t1 - t0, 0.0001), 0.0, 1.0)
	if mode == "smooth":
		u = u * u * (3.0 - 2.0 * u)
	return lerpf(a, b, u)

func step(dt: float) -> void:
	t += dt
	for i in range(lamps.size()):
		var d: Dictionary = cfg["lamps"][i]
		var l: PointLight2D = lamps[i]
		if d.has("appear"):
			l.enabled = t >= float(d["appear"])
		for sw in d.get("sweeps", []):
			var s: Dictionary = sw
			if t < float(s["t0"]):
				continue
			var v := ramp(float(s["from"]), float(s["to"]), float(s["t0"]), float(s["t1"]), String(s.get("ease", "linear")))
			match String(s["prop"]):
				"energy": l.energy = v
				"scale": l.texture_scale = v
				"x": l.position.x = v
				"y": l.position.y = v
		if d.has("color_sweep"):
			var cs: Dictionary = d["color_sweep"]
			if t >= float(cs["t0"]):
				var u := clampf((t - float(cs["t0"])) / maxf(float(cs["t1"]) - float(cs["t0"]), 0.0001), 0.0, 1.0)
				l.color = col(cs["from"]).lerp(col(cs["to"]), u)
	if bool(cfg.get("lamp_bulbs", false)):
		for i in range(lamps.size()):
			var bu: Sprite2D = nodes["lamp_bulb_%d" % i]
			bu.position = lamps[i].position
			bu.visible = lamps[i].enabled
	if cfg.has("ambient_to"):
		var a: Dictionary = cfg["ambient_to"]
		if t >= float(a["t0"]):
			mods.color = col(a["from"]).lerp(col(a["to"]), clampf((t - float(a["t0"])) / maxf(float(a["t1"]) - float(a["t0"]), 0.0001), 0.0, 1.0))
	var idx := 0
	for e in cfg.get("shader", []):
		var d3: Dictionary = e
		var at := float(d3.get("at", 0.0))
		var key := "sh%d" % idx
		if t >= at and not applied.has(key):
			assign(d3)
			applied[key] = true
		idx += 1
	for u in cfg.get("uniform_sweeps", []):
		var us: Dictionary = u
		if t < float(us["t0"]):
			continue
		var n: Node = nodes.get(String(us["node"]))
		if n != null and (n as CanvasItem).material is ShaderMaterial:
			(n.material as ShaderMaterial).set_shader_parameter(String(us["name"]), ramp(float(us["from"]), float(us["to"]), float(us["t0"]), float(us["t1"]), String(us.get("ease", "linear"))))
	if cfg.has("zoom"):
		var z: Dictionary = cfg["zoom"]
		var zz := ramp(float(z["from"]), float(z["to"]), float(z["t0"]), float(z["t1"]), "smooth")
		cam.zoom = Vector2(zz, zz)
	for mv in cfg.get("moves", []):
		var m: Dictionary = mv
		if t < float(m["t0"]):
			continue
		var n2: Node2D = nodes.get(String(m["node"]))
		if n2 != null:
			var mode := String(m.get("ease", "linear"))
			var ex := float(cfg.get("floor_extra", 0)) if String(m["node"]) == "floor" else 0.0
			n2.position = Vector2(ramp(float(m["x0"]), float(m["x1"]), float(m["t0"]), float(m["t1"]), mode) - ex, ramp(float(m["y0"]), float(m["y1"]), float(m["t0"]), float(m["t1"]), mode))
	for vz in cfg.get("visible", []):
		var vv: Dictionary = vz
		var n3: CanvasItem = nodes.get(String(vv["node"]))
		if n3 != null:
			n3.visible = t >= float(vv.get("from", 0.0)) and t < float(vv.get("to", 1e9))
	# an outline square that follows a lamp's texture (the lamp's reach)
	for k in nodes:
		if k.begins_with("outline") and nodes[k] is Line2D:
			var li := int(cfg.get("outline_lamp", 0))
			if li < lamps.size():
				var l2: PointLight2D = lamps[li]
				var hs := 128.0 * l2.texture_scale
				var c2 := l2.position
				(nodes[k] as Line2D).points = PackedVector2Array([c2 + Vector2(-hs, -hs), c2 + Vector2(hs, -hs), c2 + Vector2(hs, hs), c2 + Vector2(-hs, hs), c2 + Vector2(-hs, -hs)])

func state() -> Dictionary:
	var d := {"t": snappedf(t, 0.001), "ambient": mods.color.to_html(false)}
	var ls := []
	for l in lamps:
		ls.append({"enabled": l.enabled, "energy": snappedf(l.energy, 0.001), "scale": snappedf(l.texture_scale, 0.001), "pos": [l.position.x, l.position.y], "color": l.color.to_html(false)})
	d["lamps"] = ls
	var fl: Node = nodes.get("floor")
	if fl != null and (fl as CanvasItem).material is ShaderMaterial:
		var sm := fl.material as ShaderMaterial
		for u in sm.shader.get_shader_uniform_list():
			d["u_" + String(u["name"])] = sm.get_shader_parameter(String(u["name"]))
		d["floor_shader"] = "set"
	elif fl != null:
		d["floor_shader"] = "default lighting"
	d["zoom"] = cam.zoom.x
	return d
