extends RefCounted
# capture_scenes.gd: the node setups of every CUSTOM capture in the Vertex Shaders film (the C-numbers of CAPTURE-PLAN.md).
# Each scene declares its own logical canvas (640 x 360 for the one-square scenes, 1280 x 720 for the flag scenes); the capture harness renders it at
# 3840 x 2160 through a SubViewport, as the pilot's plan says. Shaders are loaded from lab-shaders/ (shader_dir), never edited here.
#   build(id, parent, shader_dir, duration)  -> ctx   builds the nodes under `parent`; `duration` D is the beat's measured audio (seconds)
#   tick(ctx, t)                                       applies the scripted events at time t (seconds)
# An event is {t: seconds} or {f: fraction of D}; the fraction form lets the capture be re-recorded to land on the voice. All events are "scripted" on screen.
# Event kinds: {"shader": name} (assign a ShaderMaterial), {"param": name, "value": v} (material.set_shader_parameter), {"cuts": n}, {"size": v}, sweeps over a window.
const V = preload("res://vscene.gd")
const DOTS_SRC := "extends Node2D\nvar mesh: Mesh\nvar radius := 6.0\nfunc _draw():\n\tif mesh == null:\n\t\treturn\n\tvar arr := mesh.surface_get_arrays(0)\n\tfor v in arr[Mesh.ARRAY_VERTEX]:\n\t\tdraw_circle(Vector2(v.x, v.y), radius, Color('#D97757'))\n"
const RECT_SRC := "extends Node2D\nvar rect := Rect2()\nfunc _draw():\n\tdraw_rect(rect, Color('#8C877D'), false, 3.0)\n"
const POLE_GREY := Color("#8C877D")
const FLAG_W := 384
const FLAG_H := 168                                        # 16 x 7 cells of 24 px: an odd row count, so the checker looks the same upside down

static func flag_image(w: int, h: int) -> Image:
	return V.checker_image(w, h, int(w / 16))

static func mat(ctx: Dictionary, shader_name: String, uniforms: Dictionary = {}) -> ShaderMaterial:
	return V.material_from(ctx["dir"] + "/" + shader_name + ".gdshader", uniforms)

static func dots_for(mi: MeshInstance2D) -> Node2D:
	var d := Node2D.new()
	var s := GDScript.new()
	s.source_code = DOTS_SRC
	s.reload()
	d.set_script(s)
	d.mesh = mi.mesh
	mi.add_child(d)
	return d

static func polygon_outline(w: float, h: float, n: int) -> PackedVector2Array:
	var pts := PackedVector2Array()
	for i in range(n + 1):
		pts.append(Vector2(-w / 2 + w * i / n, -h / 2))
	for i in range(n, -1, -1):
		pts.append(Vector2(-w / 2 + w * i / n, h / 2))
	return pts

static func polygon_node(pts: PackedVector2Array, img: Image, w: float, h: float, pos: Vector2) -> Polygon2D:
	var pg := Polygon2D.new()
	pg.position = pos
	pg.polygon = pts
	var uvs := PackedVector2Array()
	for p in pts:
		uvs.append(Vector2(p.x + w / 2, p.y + h / 2))         # Polygon2D uv is in TEXTURE PIXELS; the shader's UV is that divided by the texture size
	pg.uv = uvs
	pg.texture = ImageTexture.create_from_image(img)
	pg.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	return pg

# A Polygon2D with a (cols x rows) grid of points AND its cells (the `polygons` list): it behaves like the subdivided mesh.
static func polygon_grid(cols: int, rows: int, w: float, h: float, img: Image, pos: Vector2) -> Polygon2D:
	var pts := PackedVector2Array()
	for j in range(rows):
		for i in range(cols):
			pts.append(Vector2(-w / 2 + w * i / (cols - 1), -h / 2 + h * j / (rows - 1)))
	var cells: Array = []
	for j in range(rows - 1):
		for i in range(cols - 1):
			var a := j * cols + i
			cells.append(PackedInt32Array([a, a + 1, a + 1 + cols, a + cols]))
	var pg := polygon_node(pts, img, w, h, pos)
	pg.polygons = cells
	return pg

static func pole(parent: Node, pos: Vector2) -> void:
	var r := ColorRect.new()
	r.color = POLE_GREY
	r.size = Vector2(8, 380)
	r.position = pos
	parent.add_child(r)

static func add(ctx: Dictionary, parent: Node, key: String, n: Node) -> Node:
	parent.add_child(n)
	ctx["nodes"][key] = n
	return n

# the mesh flag every flag scene uses: a MeshInstance2D with a QuadMesh 384 x 168 cut 31 x 7 (33 x 9 = 297 vertices), plus the pole it is pinned to
static func mesh_flag(ctx: Dictionary, parent: Node, key: String, pos: Vector2, sub_w: int = 31, sub_d: int = 7, with_pole: bool = true) -> MeshInstance2D:
	var m := V.quad(Vector2(FLAG_W, FLAG_H), sub_w, sub_d, flag_image(FLAG_W, FLAG_H), pos)
	if with_pole:
		pole(parent, Vector2(pos.x - FLAG_W / 2.0 - 8, pos.y - FLAG_H / 2.0 - 40))
	add(ctx, parent, key, m)
	return m

static func build(id: String, parent: Node, shader_dir: String, duration: float = 12.0) -> Dictionary:
	var ctx := {"id": id, "dir": shader_dir, "nodes": {}, "events": [], "sweeps": [], "duration": duration, "done": {}, "canvas": Vector2i(1280, 720)}
	var sq := V.checker_image(128, 128, 16)                    # the 128 px checker square (same as the Lab's "checker")
	var fl := flag_image(FLAG_W, FLAG_H)                       # the flag texture: cream and teal
	var c := Vector2(640, 360)
	match id:
		"slide", "squash", "lean":                              # B05, B07, B09
			var shader: String = {"slide": "01-slide", "squash": "02-squash", "lean": "03-lean"}[id]
			var when: float = {"slide": 0.22, "squash": 0.35, "lean": 0.72}[id]       # lands on the sentence that says it
			ctx["canvas"] = Vector2i(640, 360)
			add(ctx, parent, "A", V.sprite(sq, Vector2(320, 180), 1.0))
			ctx["events"] = [{"f": when, "node": "A", "shader": shader}]
		"local":                                                # B06: the same slide on a node at scale 1 and at scale 2
			ctx["canvas"] = Vector2i(640, 360)
			add(ctx, parent, "A", V.sprite(sq, Vector2(130, 180), 1.0))
			add(ctx, parent, "B", V.sprite(sq, Vector2(380, 180), 2.0))
			ctx["events"] = [{"f": 0.52, "node": "A", "shader": "01-slide"}, {"f": 0.52, "node": "B", "shader": "01-slide"}]
		"triptych":                                             # B11: slide, squash and lean on three squares at once
			ctx["canvas"] = Vector2i(640, 360)
			add(ctx, parent, "A", V.sprite(sq, Vector2(130, 180), 1.0))
			add(ctx, parent, "B", V.sprite(sq, Vector2(320, 180), 1.0))
			add(ctx, parent, "C", V.sprite(sq, Vector2(510, 180), 1.0))
			ctx["events"] = [{"f": 0.12, "node": "A", "shader": "01-slide"}, {"f": 0.12, "node": "B", "shader": "02-squash"}, {"f": 0.12, "node": "C", "shader": "03-lean"}]
		"tilt":                                                 # B12: the ripple on a four-vertex flag (a Sprite2D)
			add(ctx, parent, "A", V.sprite(fl, c, 1.0))
			ctx["events"] = [{"f": 0.58, "node": "A", "shader": "04-ripple"}]
		"mesh-recipe":                                          # B15: a QuadMesh 320 x 320 cut 0, then 1, then 3 times each way; terracotta dots mark its vertices
			var m := V.quad(Vector2(320, 320), 0, 0, sq, c)
			add(ctx, parent, "M", m)
			ctx["nodes"]["dots"] = dots_for(m)
			ctx["events"] = [{"f": 0.6, "node": "M", "cuts": 1}, {"f": 0.8, "node": "M", "cuts": 3}]
		"pair":                                                 # B17: the same ripple on four vertices and on 297
			add(ctx, parent, "A", V.sprite(fl, Vector2(340, 360), 1.0))
			add(ctx, parent, "B", V.quad(Vector2(FLAG_W, FLAG_H), 31, 7, fl, Vector2(940, 360)))
			ctx["events"] = [{"f": 0.1, "node": "A", "shader": "04-ripple"}, {"f": 0.1, "node": "B", "shader": "04-ripple"}]
		"densities":                                            # B18: 4, 10 and 32 straight pieces along the flag
			var f2 := flag_image(288, 126)
			add(ctx, parent, "A", V.quad(Vector2(288, 126), 3, 0, f2, Vector2(215, 360)))
			add(ctx, parent, "B", V.quad(Vector2(288, 126), 9, 0, f2, Vector2(640, 360)))
			add(ctx, parent, "C", V.quad(Vector2(288, 126), 31, 0, f2, Vector2(1065, 360)))
			ctx["events"] = [{"f": 0.1, "node": "A", "shader": "04-ripple"}, {"f": 0.1, "node": "B", "shader": "04-ripple"}, {"f": 0.1, "node": "C", "shader": "04-ripple"}]
		"cut-along":                                            # B19: the wave only runs along the flag, so rows of vertices change nothing
			add(ctx, parent, "A", V.quad(Vector2(FLAG_W, FLAG_H), 31, 7, fl, Vector2(340, 360)))
			add(ctx, parent, "B", V.quad(Vector2(FLAG_W, FLAG_H), 31, 0, fl, Vector2(940, 360)))
			ctx["events"] = [{"f": 0.1, "node": "A", "shader": "04-ripple"}, {"f": 0.1, "node": "B", "shader": "04-ripple"}]
		"polygon":                                              # B20: a Polygon2D with 66 outline points beside the 297-vertex mesh
			add(ctx, parent, "A", polygon_node(polygon_outline(FLAG_W, FLAG_H, 32), fl, FLAG_W, FLAG_H, Vector2(340, 360)))
			add(ctx, parent, "B", V.quad(Vector2(FLAG_W, FLAG_H), 31, 7, fl, Vector2(940, 360)))
			ctx["events"] = [{"f": 0.1, "node": "A", "shader": "04-ripple"}, {"f": 0.1, "node": "B", "shader": "04-ripple"}]
		"travel":                                               # B21: the static ripple starts to travel (04 -> 05, unpinned)
			mesh_flag(ctx, parent, "A", c)
			ctx["events"] = [{"t": 0.0, "node": "A", "shader": "04-ripple"}, {"f": 0.58, "node": "A", "shader": "05-flag-travelling"}]
		"pinned":                                               # B22: the travelling flag is pinned (05 -> 06): the left edge stops bobbing
			mesh_flag(ctx, parent, "A", c)
			ctx["events"] = [{"t": 0.0, "node": "A", "shader": "05-flag-travelling"}, {"f": 0.3, "node": "A", "shader": "06-flag-pinned"}]
		"dials-rest":                                           # B23, B26: the flag with its three uniforms at their defaults
			mesh_flag(ctx, parent, "A", c)
			ctx["events"] = [{"t": 0.0, "node": "A", "shader": "07-flag-dials"}]
		"sweeps":                                               # B24: each dial swept in turn (scripted), timed as fractions of D so each lands on its sentence
			mesh_flag(ctx, parent, "A", c)
			ctx["events"] = [{"t": 0.0, "node": "A", "shader": "07-flag-dials"}]
			ctx["sweeps"] = [{"node": "A", "uniform": "amplitude", "from": 24.0, "to": 40.0, "f0": 0.03, "f1": 0.10}, {"node": "A", "uniform": "amplitude", "from": 40.0, "to": 0.0, "f0": 0.10, "f1": 0.20},
				{"node": "A", "uniform": "amplitude", "from": 0.0, "to": 24.0, "f0": 0.20, "f1": 0.28},
				{"node": "A", "uniform": "frequency", "from": 8.0, "to": 16.0, "f0": 0.34, "f1": 0.42}, {"node": "A", "uniform": "frequency", "from": 16.0, "to": 2.0, "f0": 0.42, "f1": 0.52},
				{"node": "A", "uniform": "frequency", "from": 2.0, "to": 8.0, "f0": 0.52, "f1": 0.60},
				{"node": "A", "uniform": "speed", "from": 3.0, "to": 8.0, "f0": 0.66, "f1": 0.74}, {"node": "A", "uniform": "speed", "from": 8.0, "to": 0.0, "f0": 0.74, "f1": 0.84},
				{"node": "A", "uniform": "speed", "from": 0.0, "to": 3.0, "f0": 0.84, "f1": 0.92}]
		"wind":                                                 # B25: the game turns a dial while the flag is running: material.set_shader_parameter("amplitude", 40.0)
			mesh_flag(ctx, parent, "A", c)
			ctx["events"] = [{"t": 0.0, "node": "A", "shader": "07-flag-dials"}, {"f": 0.75, "node": "A", "param": "amplitude", "value": 40.0}]
		"lit":                                                  # B32: the flag, then the same flag with the folds lit through a varying (06 -> 10)
			mesh_flag(ctx, parent, "A", c)
			ctx["events"] = [{"t": 0.0, "node": "A", "shader": "06-flag-pinned"}, {"f": 0.62, "node": "A", "shader": "10-flag-lit"}]
		"final":                                                # B01 hook and B33: the finished flag (dials + color shading), from the first frame
			mesh_flag(ctx, parent, "A", c)
			ctx["events"] = [{"t": 0.0, "node": "A", "shader": "11-flag-final"}]
		"flat-mesh":                                            # B30: smooth against flat corner colours on a mesh cut 7 x 7
			var wh := V.white_image(128, 128)
			add(ctx, parent, "A", V.quad(Vector2(300, -300), 7, 7, wh, Vector2(340, 360)))      # size.y negative: UV.y runs down the screen, as on the sprite still
			add(ctx, parent, "B", V.quad(Vector2(300, -300), 7, 7, wh, Vector2(940, 360)))
			ctx["events"] = [{"t": 0.0, "node": "A", "shader": "08-corner-colors"}, {"t": 0.0, "node": "B", "shader": "09-corner-colors-flat"}]
		"stripes":                                              # B34: six stripes computed in vertex() against in fragment(), on two four-corner squares
			var wh2 := V.white_image(128, 128)
			add(ctx, parent, "A", V.sprite(wh2, Vector2(340, 360), 3.0))
			add(ctx, parent, "B", V.sprite(wh2, Vector2(940, 360), 3.0))
			ctx["events"] = [{"t": 0.0, "node": "A", "shader": "12-stripes-from-vertex"}, {"t": 0.0, "node": "B", "shader": "13-stripes-from-fragment"}]
		"flip":                                                 # B35: a QuadMesh draws upside down in 2D until its size.y is negative
			add(ctx, parent, "S", V.sprite(V.blob_image(128), Vector2(300, 360), 2.0))
			var q := V.quad(Vector2(256, 256), 0, 0, V.blob_image(128), Vector2(940, 360))
			add(ctx, parent, "M", q)
			ctx["events"] = [{"f": 0.6, "node": "M", "size": Vector2(256, -256)}]
		"vertex-two":                                           # B37: the colour from the corners travels with the sprite; the colour from the screen does not
			add(ctx, parent, "A", V.sprite(V.white_image(128, 128), Vector2(300, 230), 2.0))
			add(ctx, parent, "B", V.sprite(V.white_image(128, 128), Vector2(300, 510), 2.0))
			ctx["events"] = [{"t": 0.0, "node": "A", "shader": "15-position-from-vertex"}, {"t": 0.0, "node": "B", "shader": "14-position-from-fragment"}]
		"polygon-uv":                                           # B38: a Polygon2D only has UV when it has a texture
			var pa := polygon_grid(33, 9, FLAG_W, FLAG_H, fl, Vector2(340, 360))
			pa.texture = null                                  # no texture: UV is zero everywhere, so `* UV.x` removes the whole wave
			pa.color = V.TEAL
			var pb := polygon_grid(33, 9, FLAG_W, FLAG_H, fl, Vector2(940, 360))
			add(ctx, parent, "A", pa)
			add(ctx, parent, "B", pb)
			ctx["events"] = [{"f": 0.1, "node": "A", "shader": "06-flag-pinned"}, {"f": 0.1, "node": "B", "shader": "06-flag-pinned"}]
		"drawing-only":                                         # B39: the picture slides 200 px away, the node's own rectangle does not
			ctx["canvas"] = Vector2i(640, 360)
			var sp := V.sprite(sq, Vector2(320, 180), 1.0)
			add(ctx, parent, "A", sp)
			var r := Node2D.new()
			var rs := GDScript.new()
			rs.source_code = RECT_SRC
			rs.reload()
			r.set_script(rs)
			r.position = Vector2(320, 180)
			r.rect = sp.get_rect()                             # the node's real rectangle, from get_rect()
			parent.add_child(r)
			ctx["nodes"]["rect"] = r
			ctx["events"] = [{"f": 0.3, "node": "A", "shader": "16-slide-far"}]
		"equiv-lit-color":                                      # evidence only: the explicit-varying shading and the color shortcut draw the same picture
			add(ctx, parent, "A", V.quad(Vector2(FLAG_W, FLAG_H), 31, 7, fl, Vector2(340, 360)))
			add(ctx, parent, "B", V.quad(Vector2(FLAG_W, FLAG_H), 31, 7, fl, Vector2(940, 360)))
			ctx["events"] = [{"t": 0.0, "node": "A", "shader": "10-flag-lit"}, {"t": 0.0, "node": "B", "shader": "11-flag-final"}]
		"polygon-grid":                                         # evidence only: a Polygon2D given a grid of points AND its cells behaves like the mesh
			add(ctx, parent, "A", polygon_grid(33, 9, FLAG_W, FLAG_H, fl, Vector2(340, 360)))
			add(ctx, parent, "B", V.quad(Vector2(FLAG_W, FLAG_H), 31, 7, fl, Vector2(940, 360)))
			ctx["events"] = [{"t": 0.0, "node": "A", "shader": "04-ripple"}, {"t": 0.0, "node": "B", "shader": "04-ripple"}]
		_:
			push_error("unknown scene " + id)
	return ctx

static func event_time(ctx: Dictionary, e: Dictionary) -> float:
	return e["t"] if e.has("t") else float(e["f"]) * float(ctx["duration"])

static func tick(ctx: Dictionary, t: float) -> void:
	for i in range(ctx["events"].size()):
		var e: Dictionary = ctx["events"][i]
		if t >= event_time(ctx, e) and not ctx["done"].has(i):
			ctx["done"][i] = true
			var n: Node = ctx["nodes"][e["node"]]
			if e.has("param"):
				n.material.set_shader_parameter(e["param"], e["value"])      # the real call: material.set_shader_parameter(name, value)
			elif e.has("cuts"):
				(n.mesh as QuadMesh).subdivide_width = e["cuts"]
				(n.mesh as QuadMesh).subdivide_depth = e["cuts"]
			elif e.has("size"):
				(n.mesh as QuadMesh).size = e["size"]
			else:
				n.material = mat(ctx, e["shader"])
	for s in ctx["sweeps"]:
		var t0: float = s["t0"] if s.has("t0") else float(s["f0"]) * float(ctx["duration"])
		var t1: float = s["t1"] if s.has("t1") else float(s["f1"]) * float(ctx["duration"])
		if t >= t0 and t <= t1:
			var k := smoothstep(0.0, 1.0, (t - t0) / (t1 - t0))
			ctx["nodes"][s["node"]].material.set_shader_parameter(s["uniform"], lerpf(s["from"], s["to"], k))
	if ctx["id"] == "mesh-recipe":
		ctx["nodes"]["dots"].queue_redraw()
	elif ctx["id"] == "vertex-two":
		var x := lerpf(300.0, 1000.0, smoothstep(0.0, 1.0, clampf((t - 0.3 * ctx["duration"]) / (0.4 * ctx["duration"]), 0.0, 1.0)))
		ctx["nodes"]["A"].position.x = x
		ctx["nodes"]["B"].position.x = x
