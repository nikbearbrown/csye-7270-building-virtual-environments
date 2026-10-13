class_name CaptureScene
extends RefCounted
# SubViewports film: every Godot capture the film shows, as one scene library. Each scene is built into a 1280 x 720 logical canvas (a Node2D)
# and driven by update(t), t = seconds since the first frame (the harness steps t by 1/30). Nothing here reads the wall clock.
# A capture harness renders the canvas at 3840 x 2160 (see CAPTURE-PLAN.md); the scene never changes for that.
#
# Ids: c01 hook | c02 texture appears | c03 size is resolution | c04a origin | c04b cut off | c05 transparent | c06 premultiplied |
#      c07 inner shader | c08 pass-through | c09 fade | c10 turn | c11 group | c12 per display pixel | c13 stripes dials |
#      c14 moving stripes | c15 hue strip + six swatches | c16 rainbow stripes | c17 plain vs grid | c18 wobble | c19 upside down | c20 four places | c21 update mode

const DEFAULT_SHADERS := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-subviewports/lab-shaders/"
const STAGE := Color("#D9D5CA")        # the Lab's warm light grey
const CLEAR := Color("#A8A090")        # default clear colour for the shots that must show the picture's box (the engine default is a dark grey)
const GRID := Color("#BDB6A4")
const TEAL := Color("#5FA391")
const GOLD := Color(0.93, 0.76, 0.35)
const PICTURE := 512                    # the picture size used everywhere (a new SubViewport is 512 x 512)
const BLOB := 448                       # the test sprite texture size (hard-edged blob, 0.30 radius), 87.5 percent of the picture

var id := ""
var duration := 12.0
var shaders_dir := DEFAULT_SHADERS
var canvas: Node2D
var n: Dictionary = {}                  # named nodes of the scene

func _init(scene_id: String, shaders_path: String = DEFAULT_SHADERS) -> void:
	id = scene_id
	shaders_dir = shaders_path

# ------------------------------------------------------------------ images
static func blob_image(size: int, bleed: bool = true) -> Image:
	# the series' test sprite: a teal blob with two cream eyes and transparent padding (hard edges, no anti-aliasing)
	var img := Image.create(size, size, false, Image.FORMAT_RGBA8)
	# bleed = true: the transparent padding still carries teal, so a filtered edge never mixes in black (for textures drawn with the default blend).
	# bleed = false: padding is transparent black, which a premultiplied blend needs (it adds the colour of every texel).
	img.fill(Color(TEAL.r, TEAL.g, TEAL.b, 0.0) if bleed else Color(0, 0, 0, 0))
	var c := Vector2(size / 2.0, size / 2.0)
	for y in size:
		for x in size:
			var p := Vector2(x + 0.5, y + 0.5)
			if p.distance_to(c) < size * 0.30:
				img.set_pixel(x, y, TEAL)
			if p.distance_to(c + Vector2(-size * 0.10, -size * 0.06)) < size * 0.035 or p.distance_to(c + Vector2(size * 0.10, -size * 0.06)) < size * 0.035:
				img.set_pixel(x, y, Color("#FAF9F5"))
	return img

static func glow_image(size: int) -> Image:
	# a gold disc with a soft edge: alpha falls from 1 to 0 over the outer 45 percent of the radius (many half-transparent pixels)
	var img := Image.create(size, size, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var c := Vector2(size / 2.0, size / 2.0)
	var r := size * 0.42
	for y in size:
		for x in size:
			var d := Vector2(x + 0.5, y + 0.5).distance_to(c)
			var a := clampf((r - d) / (r * 0.45), 0.0, 1.0)
			if a > 0.0:
				img.set_pixel(x, y, Color(GOLD.r, GOLD.g, GOLD.b, a))
	return img

# ------------------------------------------------------------------ helpers
func _mat(file: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(shaders_dir + file)
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

func _stage() -> void:
	var r := ColorRect.new()
	r.color = STAGE
	r.size = Vector2(1280, 720)
	canvas.add_child(r)

func _grid() -> void:
	for i in range(0, 1281, 64):
		var v := ColorRect.new()
		v.color = GRID
		v.position = Vector2(i - 1, 0)
		v.size = Vector2(2, 720)
		canvas.add_child(v)
	for j in range(0, 721, 64):
		var h := ColorRect.new()
		h.color = GRID
		h.position = Vector2(0, j - 1)
		h.size = Vector2(1280, 2)
		canvas.add_child(h)

func _viewport(size: Vector2i, transparent: bool) -> SubViewport:
	var vp := SubViewport.new()
	vp.size = size
	vp.transparent_bg = transparent
	canvas.add_child(vp)
	return vp

func _blob(parent: Node, pos: Vector2, size: int = BLOB, shader: String = "", bleed: bool = true) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = ImageTexture.create_from_image(blob_image(size, bleed))
	s.position = pos
	if shader != "":
		s.material = _mat(shader)
	parent.add_child(s)
	return s

func _display(vp: SubViewport, top_left: Vector2, shader: String = "", nearest := true) -> Sprite2D:
	var d := Sprite2D.new()
	d.centered = false
	d.position = top_left
	d.texture = vp.get_texture()
	if nearest:
		d.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	if shader != "":
		d.material = _mat(shader)
	canvas.add_child(d)
	return d

func _mesh_display(vp: SubViewport, centre: Vector2, size: Vector2, subdivide: int, shader: String) -> MeshInstance2D:
	var q := QuadMesh.new()
	q.size = size
	q.subdivide_width = subdivide
	q.subdivide_depth = subdivide
	var m := MeshInstance2D.new()
	m.mesh = q
	m.texture = vp.get_texture()
	m.position = centre
	if shader != "":
		m.material = _mat(shader)
	canvas.add_child(m)
	return m

static func smooth(a: float, b: float, t0: float, t1: float, t: float) -> float:
	var k := clampf((t - t0) / (t1 - t0), 0.0, 1.0)
	k = k * k * (3.0 - 2.0 * k)
	return lerpf(a, b, k)

func _centre_top_left(w: float, h: float) -> Vector2:
	return Vector2((1280.0 - w) / 2.0, (720.0 - h) / 2.0)

# ------------------------------------------------------------------ build
func build(parent: Node2D) -> void:
	canvas = parent
	RenderingServer.set_default_clear_color(CLEAR)
	_stage()
	match id:
		"c01":
			duration = 18.0
			var vp := _viewport(Vector2i(PICTURE, PICTURE), true)
			n["blob"] = _blob(vp, Vector2(256, 256), BLOB, "01-inner-gradient.gdshader")
			n["mesh"] = _mesh_display(vp, Vector2(640, 360), Vector2(512, -512), 31, "09-rainbow-wobble.gdshader")
			(n["mesh"] as MeshInstance2D).texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		"c02":
			duration = 14.0                      # the texture is handed over at 7.0 s (about the word "Give" of the narration)
			var vp2 := _viewport(Vector2i(PICTURE, PICTURE), false)
			n["blob"] = _blob(vp2, Vector2(256, 256))
			n["vp"] = vp2
			n["display"] = _display(vp2, _centre_top_left(512, 512))
			(n["display"] as Sprite2D).texture = null            # nothing to show until the texture is handed over
		"c03":
			duration = 19.0                      # Filter switches from Linear to Nearest at 12.5 s (the words "Filter to Nearest" of the narration, at 0.34 s per word)
			var big := _viewport(Vector2i(512, 512), false)
			_blob(big, Vector2(256, 256), 512)                       # the same blob, drawn natively at 512 px
			var small := _viewport(Vector2i(128, 128), false)
			_blob(small, Vector2(64, 64), 128)                       # the same blob, drawn natively at 128 px
			n["left"] = _display(big, Vector2(100, 104))
			n["right"] = _display(small, Vector2(668, 104))
			(n["right"] as Sprite2D).scale = Vector2(4, 4)
			(n["right"] as Sprite2D).texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		"c04a", "c04b":
			duration = 16.0
			var vp4 := _viewport(Vector2i(PICTURE, PICTURE), false)
			n["blob"] = _blob(vp4, Vector2(256, 256))
			n["display"] = _display(vp4, _centre_top_left(512, 512))
		"c05":
			duration = 15.0                      # Transparent BG is switched on at 8.0 s
			_grid()
			var vp5 := _viewport(Vector2i(PICTURE, PICTURE), false)
			n["vp"] = vp5
			n["blob"] = _blob(vp5, Vector2(256, 256))
			n["display"] = _display(vp5, _centre_top_left(512, 512))
		"c06":
			duration = 18.0                      # the blend mode goes from Mix to Premultiplied Alpha at 10.5 s
			_grid()
			var vp6 := _viewport(Vector2i(PICTURE, PICTURE), true)
			var g := Sprite2D.new()
			g.texture = ImageTexture.create_from_image(glow_image(512))
			g.position = Vector2(256, 256)
			vp6.add_child(g)
			var d6 := _display(vp6, _centre_top_left(512, 512))
			var cim := CanvasItemMaterial.new()
			cim.blend_mode = CanvasItemMaterial.BLEND_MODE_MIX
			d6.material = cim
			n["cim"] = cim
		"c07":
			duration = 17.0                      # the inner shader goes on at 7.0 s
			var vp7 := _viewport(Vector2i(PICTURE, PICTURE), true)
			n["blob"] = _blob(vp7, Vector2(256, 256))
			n["display"] = _display(vp7, _centre_top_left(512, 512), "02-outer-passthrough.gdshader")
		"c08":
			duration = 18.0
			var vp8 := _viewport(Vector2i(PICTURE, PICTURE), true)
			n["blob"] = _blob(vp8, Vector2(256, 256), BLOB, "01-inner-gradient.gdshader")
			# left: the picture shown directly (a sprite with Premultiplied Alpha, which a transparent picture needs); right: shown through the pass-through shader
			var plain := _display(vp8, Vector2(100, 104))
			var cim8 := CanvasItemMaterial.new()
			cim8.blend_mode = CanvasItemMaterial.BLEND_MODE_PREMULT_ALPHA
			plain.material = cim8
			_display(vp8, Vector2(668, 104), "02-outer-passthrough.gdshader")
			n["plain"] = plain
		"c09":
			duration = 19.0                      # the fade goes on at 4.5 s
			var vp9 := _viewport(Vector2i(PICTURE, PICTURE), true)
			n["blob"] = _blob(vp9, Vector2(256, 256), BLOB, "01-inner-gradient.gdshader")
			n["display"] = _display(vp9, _centre_top_left(512, 512), "02-outer-passthrough.gdshader")
		"c10":
			duration = 17.0                      # the sprite turns half a turn between 0.3 s and 3.3 s
			var vp10 := _viewport(Vector2i(PICTURE, PICTURE), true)
			n["blob"] = _blob(vp10, Vector2(256, 256), BLOB, "01-inner-gradient.gdshader")
			n["display"] = _display(vp10, _centre_top_left(512, 512), "03-outer-fade.gdshader")
		"c11":
			duration = 18.0
			_outline(Rect2(40, 210, 600, 300))
			_outline(Rect2(660, 210, 600, 300))
			n["left_sprites"] = []
			n["right_sprites"] = []
			# left: no viewport, each sprite carries its own fade. right: one viewport holding both sprites, one fade on the picture.
			for cx: float in [150.0, 450.0]:
				var s := _blob(canvas, Vector2(40 + cx, 210 + 150), BLOB, "", false)
				s.scale = Vector2(200.0 / float(BLOB), 200.0 / float(BLOB))
				s.material = _mat("03-outer-fade.gdshader")
				s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
				(n["left_sprites"] as Array).append(s)
			var vp11 := _viewport(Vector2i(600, 300), true)
			for cx2: float in [150.0, 450.0]:
				var s2 := _blob(vp11, Vector2(cx2, 150), BLOB, "")
				s2.scale = Vector2(200.0 / float(BLOB), 200.0 / float(BLOB))
				(n["right_sprites"] as Array).append(s2)
			n["vp"] = vp11
			n["display"] = _display(vp11, Vector2(660, 210), "03-outer-fade.gdshader")
		"c12":
			duration = 18.0
			var vp12 := _viewport(Vector2i(64, 64), true)
			var b12 := _blob(vp12, Vector2(32, 32), BLOB)
			b12.scale = Vector2(64.0 / float(BLOB), 64.0 / float(BLOB))
			var d12 := _display(vp12, _centre_top_left(512, 512), "05-stripes-moving.gdshader")
			d12.scale = Vector2(8, 8)
			n["display"] = d12
		"c13":
			duration = 16.0
			var vp13 := _viewport(Vector2i(PICTURE, PICTURE), true)
			n["blob"] = _blob(vp13, Vector2(256, 256), BLOB, "01-inner-gradient.gdshader")
			n["display"] = _display(vp13, _centre_top_left(512, 512), "04-stripes.gdshader")
		"c14":
			duration = 15.0
			var vp14 := _viewport(Vector2i(PICTURE, PICTURE), true)
			n["blob"] = _blob(vp14, Vector2(256, 256), BLOB, "01-inner-gradient.gdshader")
			n["display"] = _display(vp14, _centre_top_left(512, 512), "05-stripes-moving.gdshader")
		"c15":
			duration = 8.0
			var strip := ColorRect.new()
			strip.position = Vector2(140, 90)
			strip.size = Vector2(1000, 130)
			strip.material = _mat("06-hsv-strip.gdshader")
			canvas.add_child(strip)
			for k in 6:
				var sw := ColorRect.new()
				sw.position = Vector2(140 + k * 170, 330)
				sw.size = Vector2(160, 160)
				var m := _mat("06b-hsv-probe.gdshader")
				m.set_shader_parameter("hue", k / 6.0)
				sw.material = m
				canvas.add_child(sw)
		"c16":
			duration = 15.0
			var vp16 := _viewport(Vector2i(PICTURE, PICTURE), true)
			n["blob"] = _blob(vp16, Vector2(256, 256), BLOB, "01-inner-gradient.gdshader")
			n["display"] = _display(vp16, _centre_top_left(512, 512), "07-rainbow-stripes.gdshader")
		"c17", "c18":
			duration = 17.0
			var vp17 := _viewport(Vector2i(PICTURE, PICTURE), true)
			_card(vp17)
			n["blob"] = _blob(vp17, Vector2(256, 256), BLOB, "01-inner-gradient.gdshader")
			if id == "c17":
				n["left"] = _mesh_display(vp17, Vector2(330, 360), Vector2(480, -480), 0, "08-wobble.gdshader")
				n["right"] = _mesh_display(vp17, Vector2(950, 360), Vector2(480, -480), 31, "08-wobble.gdshader")
			else:
				n["right"] = _mesh_display(vp17, Vector2(640, 360), Vector2(512, -512), 31, "08-wobble.gdshader")
			for k: String in ["left", "right"]:
				if n.has(k):
					(n[k] as MeshInstance2D).texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		"c19":
			duration = 16.0                      # the mesh's height goes negative at 9.5 s
			var vp19 := _viewport(Vector2i(PICTURE, PICTURE), true)
			_card(vp19)
			n["blob"] = _blob(vp19, Vector2(256, 256), BLOB, "01-inner-gradient.gdshader")
			var q19 := QuadMesh.new()
			q19.size = Vector2(512, 512)
			var m19 := MeshInstance2D.new()
			m19.mesh = q19
			m19.texture = vp19.get_texture()
			m19.position = Vector2(640, 360)
			m19.material = _mat("02-outer-passthrough.gdshader")
			canvas.add_child(m19)
			n["mesh"] = m19
			n["quad"] = q19
		"c20":
			duration = 16.0
			var vp20 := _viewport(Vector2i(280, 280), false)
			var bg := ColorRect.new()
			bg.color = Color("#FAF9F5")
			bg.size = Vector2(280, 280)
			vp20.add_child(bg)
			var b20 := _blob(vp20, Vector2(140, 140), BLOB, "01-inner-gradient.gdshader")
			b20.scale = Vector2(280.0 / float(BLOB), 280.0 / float(BLOB))
			n["blob"] = b20
			n["sprite"] = _display(vp20, Vector2(40, 220))
			# interface panel
			var panel := PanelContainer.new()
			var sb := StyleBoxFlat.new()
			sb.bg_color = Color("#FAF9F5")
			sb.border_color = TEAL
			sb.set_border_width_all(8)
			sb.set_content_margin_all(8)
			panel.add_theme_stylebox_override("panel", sb)
			panel.position = Vector2(332, 212)       # 8 px border + 280 px picture + 8 px border = 296 px
			var tr := TextureRect.new()
			tr.texture = vp20.get_texture()
			tr.custom_minimum_size = Vector2(280, 280)
			panel.add_child(tr)
			canvas.add_child(panel)
			# a plane in a 3D scene, rendered by its own 3D viewport, shown here as a 2D picture
			var vp3 := SubViewport.new()
			vp3.size = Vector2i(280, 280)
			vp3.own_world_3d = true
			vp3.transparent_bg = true
			canvas.add_child(vp3)
			var cam := Camera3D.new()
			cam.position = Vector3(0, 0, 2.6)
			cam.fov = 40.0
			vp3.add_child(cam)
			var quad := MeshInstance3D.new()
			var qm := QuadMesh.new()
			qm.size = Vector2(1.6, 1.6)
			quad.mesh = qm
			var mat3 := StandardMaterial3D.new()
			mat3.albedo_texture = vp20.get_texture()
			mat3.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			quad.material_override = mat3
			vp3.add_child(quad)
			n["quad3d"] = quad
			var d3 := Sprite2D.new()
			d3.centered = false
			d3.position = Vector2(640, 220)
			d3.texture = vp3.get_texture()
			var pm := CanvasItemMaterial.new()
			pm.blend_mode = CanvasItemMaterial.BLEND_MODE_PREMULT_ALPHA
			d3.material = pm
			canvas.add_child(d3)
			# a ColorRect whose own shader reads the picture through a sampler uniform
			var cr := ColorRect.new()
			cr.position = Vector2(940, 220)
			cr.size = Vector2(280, 280)
			var sm := Shader.new()
			sm.code = "shader_type canvas_item;\nuniform sampler2D picture;\n\nvoid fragment() {\n\tCOLOR = texture(picture, UV);\n}\n"
			var smat := ShaderMaterial.new()
			smat.shader = sm
			smat.set_shader_parameter("picture", vp20.get_texture())
			cr.material = smat
			canvas.add_child(cr)
		"c21":
			duration = 18.0                      # the right-hand viewport is set to Once at 8.5 s
			# two identical viewports, one left on the default update mode, one set to Once; the sprite inside each keeps moving
			for k in 2:
				var vp21 := _viewport(Vector2i(512, 512), false)
				var b21 := _blob(vp21, Vector2(256, 256), BLOB)
				b21.scale = Vector2(0.6, 0.6)
				var d21 := _display(vp21, Vector2(100 + k * 568, 104))
				n["vp%d" % k] = vp21
				n["blob%d" % k] = b21
				n["disp%d" % k] = d21
		_:
			push_error("unknown capture scene " + id)

func _outline(r: Rect2, color: Color = GRID, w: float = 3.0) -> void:
	# a hairline frame drawn on the stage (never inside a picture)
	for rr: Rect2 in [Rect2(r.position.x, r.position.y, r.size.x, w), Rect2(r.position.x, r.end.y - w, r.size.x, w), Rect2(r.position.x, r.position.y, w, r.size.y), Rect2(r.end.x - w, r.position.y, w, r.size.y)]:
		var c := ColorRect.new()
		c.color = color
		c.position = rr.position
		c.size = rr.size
		canvas.add_child(c)

func _card(vp: SubViewport) -> void:
	# a cream card with a teal frame, so the picture's edges (and a bent mesh) are easy to see
	var frame := ColorRect.new()
	frame.color = TEAL
	frame.size = Vector2(512, 512)
	vp.add_child(frame)
	var inner := ColorRect.new()
	inner.color = Color("#FAF9F5")
	inner.position = Vector2(20, 20)
	inner.size = Vector2(472, 472)
	vp.add_child(inner)

# ------------------------------------------------------------------ update
func update(t: float) -> void:
	match id:
		"c01":
			(n["blob"] as Sprite2D).rotation = 0.9 * t
		"c02":
			if t >= 7.0 and (n["display"] as Sprite2D).texture == null:
				(n["display"] as Sprite2D).texture = (n["vp"] as SubViewport).get_texture()
		"c03":
			(n["right"] as Sprite2D).texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST if t >= 12.5 else CanvasItem.TEXTURE_FILTER_LINEAR
		"c04a":
			var p := smooth(256.0, 0.0, 6.4, 8.6, t)      # the sprite sits in the middle while the voice explains the origin, then slides to (0, 0) on "placed at zero, zero"
			(n["blob"] as Sprite2D).position = Vector2(p, p)
		"c04b":
			var x := 0.0
			var y := 0.0
			if t < 0.3:
				x = 0.0
				y = 0.0
			elif t < 4.0:
				x = smooth(0.0, 256.0, 0.3, 3.3, t)
				y = x
			else:
				x = smooth(256.0, 560.0, 4.0, 7.0, t)
				y = 256.0 if t > 4.0 else x
				if t < 4.0:
					y = x
			(n["blob"] as Sprite2D).position = Vector2(x, y)
		"c05":
			if t >= 8.0:
				(n["vp"] as SubViewport).transparent_bg = true
		"c06":
			if t >= 10.5:
				(n["cim"] as CanvasItemMaterial).blend_mode = CanvasItemMaterial.BLEND_MODE_PREMULT_ALPHA
		"c07":
			# the plain blob until 7.0 s, then the inner shader goes on (update(t) must be called with t rising frame by frame from 0: the flags below fire once)
			if t >= 7.0 and not n.get("shaded", false):
				(n["blob"] as Sprite2D).material = _mat("01-inner-gradient.gdshader")
				n["shaded"] = true
		"c08":
			(n["blob"] as Sprite2D).position = Vector2(256.0 + 60.0 * sin(t * 0.9), 256.0)
		"c09":
			# a pass-through until 4.5 s, then the fade goes on
			if t >= 4.5 and not n.get("faded", false):
				(n["display"] as Sprite2D).material = _mat("03-outer-fade.gdshader")
				n["faded"] = true
		"c10":
			(n["blob"] as Sprite2D).rotation = smooth(0.0, PI, 0.3, 3.3, t)
		"c11":
			# both sprites in both panels slide left and right by the same amount: the fade fixed to each sprite rides along with it; the fade fixed to the picture does not
			var dx := 70.0 * sin(0.8 * t)
			var i := 0
			for cx: float in [150.0, 450.0]:
				((n["left_sprites"] as Array)[i] as Sprite2D).position = Vector2(40.0 + cx + dx, 360.0)
				((n["right_sprites"] as Array)[i] as Sprite2D).position = Vector2(cx + dx, 150.0)
				i += 1
		"c12":
			pass
		"c13":
			var m := (n["display"] as Sprite2D).material as ShaderMaterial
			m.set_shader_parameter("width", smooth(0.08, 0.5, 0.5, 4.5, t))
			m.set_shader_parameter("count", smooth(6.0, 12.0, 8.0, 12.0, t))
		"c14":
			(n["blob"] as Sprite2D).rotation = 0.8 * t
		"c16":
			(n["blob"] as Sprite2D).rotation = 0.8 * t
		"c19":
			(n["quad"] as QuadMesh).size = Vector2(512, -512) if t >= 9.5 else Vector2(512, 512)
		"c20":
			(n["blob"] as Sprite2D).rotation = 0.7 * t
			(n["quad3d"] as MeshInstance3D).rotation.y = 0.7 * sin(t * 0.6)
		"c21":
			for k in 2:
				(n["blob%d" % k] as Sprite2D).position = Vector2(256.0 + 150.0 * sin(t * 0.9 + k * 0.0), 256.0 + 90.0 * cos(t * 0.7))
			if t >= 8.5 and not n.get("once_set", false):
				(n["vp1"] as SubViewport).render_target_update_mode = SubViewport.UPDATE_ONCE
				n["once_set"] = true
		_:
			pass
