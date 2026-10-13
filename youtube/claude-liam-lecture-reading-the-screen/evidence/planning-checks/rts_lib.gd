extends RefCounted
# rts_lib.gd: helpers shared by every planning check and capture scene of "Reading the Screen".
# The meadow is the film's test world. It is built in code from fractions of the window size, so any size works.
# Colours were chosen so that the meadow, its inversion and its grayscale all keep a mid-tone floor (see palette-check.py).

const TEAL := Color("#5FA391")
const CREAM := Color("#FAF9F5")
const GRASS_A := Color("#8CBD73")
const GRASS_B := Color("#9ECC80")
const SAND := Color("#E0CC9E")
const ROSE := Color("#D9738C")
const MUSTARD := Color("#E6B840")
const VIOLET := Color("#8C73CC")
const TREE := Color("#55916B")
const STAGE := Color("#D9D5CA")

static func mat_from(code: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = code
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

static func shader_text(name: String) -> String:
	# The film's tested shader files, copied next to the project as res://lab-shaders/. A missing file is an ERROR line in the log, never a silent empty shader.
	if not FileAccess.file_exists("res://lab-shaders/" + name):
		push_error("ERROR: missing shader file res://lab-shaders/" + name)
		print("ERROR: missing shader file res://lab-shaders/" + name)
	return FileAccess.get_file_as_string("res://lab-shaders/" + name)

static func mat_file(name: String) -> ShaderMaterial:
	return mat_from(shader_text(name))

static func blob_texture(n: int = 128) -> ImageTexture:
	# The series' test sprite: a teal blob with two cream eyes and transparent padding (same drawing as lab/runner.gd).
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var c := Vector2(n / 2.0, n / 2.0)
	for y in n:
		for x in n:
			var d := Vector2(x, y).distance_to(c)
			if d < n * 0.30:
				img.set_pixel(x, y, TEAL)
			var e1 := Vector2(x, y).distance_to(c + Vector2(-n * 0.10, -n * 0.06))
			var e2 := Vector2(x, y).distance_to(c + Vector2(n * 0.10, -n * 0.06))
			if e1 < n * 0.035 or e2 < n * 0.035:
				img.set_pixel(x, y, CREAM)
	return ImageTexture.create_from_image(img)

static func poly_circle(center: Vector2, radius: float, color: Color, n: int = 40) -> Polygon2D:
	var p := Polygon2D.new()
	var pts := PackedVector2Array()
	for i in n:
		var a := TAU * i / n
		pts.append(center + Vector2(cos(a), sin(a)) * radius)
	p.polygon = pts
	p.color = color
	return p

static func poly_quad(a: Vector2, b: Vector2, c: Vector2, d: Vector2, color: Color) -> Polygon2D:
	var p := Polygon2D.new()
	p.polygon = PackedVector2Array([a, b, c, d])
	p.color = color
	return p

static func rect(pos: Vector2, size: Vector2, color: Color, name: String = "Rect") -> ColorRect:
	var r := ColorRect.new()
	r.name = name
	r.position = pos
	r.size = size
	r.color = color
	return r

static func add_frame(r: Control, color: Color = CREAM, width: float = 6.0) -> ReferenceRect:
	# A cream picture frame drawn just inside a rectangle (a child, so it draws after its parent). It is not a reader: it changes nothing
	# the screen texture sees. It is there so a window that shows exactly what is behind it can still be seen.
	var fr := ReferenceRect.new()
	fr.name = "Frame"
	fr.editor_only = false
	fr.border_color = color
	fr.border_width = width
	fr.mouse_filter = Control.MOUSE_FILTER_IGNORE
	r.add_child(fr)
	fr.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	return fr

static func build_world(parent: Node, size: Vector2, bleed_cells: int = 0) -> Node2D:
	# The meadow: a 16 x 9 checker of two greens, a sand path, three trees, twelve flowers. Draws first, so it is
	# always "behind" everything else. bleed_cells > 0 grows the checker and the path past the screen on every side (for scenes that scroll).
	# Returns the Node2D that holds it.
	var world := Node2D.new()
	world.name = "World"
	parent.add_child(world)
	var cols := 16
	var rows := 9
	var b := bleed_cells
	var img := Image.create(cols + 2 * b, rows + 2 * b, false, Image.FORMAT_RGBA8)
	for y in rows + 2 * b:
		for x in cols + 2 * b:
			img.set_pixel(x, y, GRASS_A if (x + y) % 2 == 0 else GRASS_B)
	var cell := Vector2(size.x / cols, size.y / rows)
	var ground := Sprite2D.new()
	ground.name = "Ground"
	ground.texture = ImageTexture.create_from_image(img)
	ground.centered = false
	ground.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	ground.scale = cell
	ground.position = -cell * float(b)
	world.add_child(ground)
	var u := size.x
	var v := size.y
	var ext := cell.x * float(b)
	# the path is the band between two straight lines: top (0, 0.60v) -> (u, 0.26v), bottom (0, 0.74v) -> (u, 0.40v)
	var slope := -0.34 * v / u
	var path := poly_quad(Vector2(-ext, 0.60 * v - slope * ext), Vector2(-ext, 0.74 * v - slope * ext), Vector2(u + ext, 0.40 * v + slope * ext), Vector2(u + ext, 0.26 * v + slope * ext), SAND)
	path.name = "Path"
	world.add_child(path)
	var trees := [[0.10, 0.20, 0.075], [0.86, 0.18, 0.070], [0.92, 0.80, 0.065]]
	for i in trees.size():
		var t: Array = trees[i]
		var tr := poly_circle(Vector2(t[0] * u, t[1] * v), t[2] * v, TREE)
		tr.name = "Tree%d" % (i + 1)
		world.add_child(tr)
	var flowers := [
		[0.30, 0.30, ROSE], [0.62, 0.16, ROSE], [0.44, 0.47, ROSE], [0.75, 0.56, ROSE],
		[0.52, 0.30, MUSTARD], [0.34, 0.63, MUSTARD], [0.70, 0.84, MUSTARD], [0.08, 0.52, MUSTARD],
		[0.25, 0.12, VIOLET], [0.80, 0.40, VIOLET], [0.58, 0.72, VIOLET], [0.20, 0.86, VIOLET]]
	for i in flowers.size():
		var f: Array = flowers[i]
		var fl := poly_circle(Vector2(f[0] * u, f[1] * v), 0.022 * v, f[2], 24)
		fl.name = "Flower%d" % (i + 1)
		world.add_child(fl)
	return world

static func make_player(pos: Vector2, scale_px: float = 1.0) -> Sprite2D:
	var p := Sprite2D.new()
	p.name = "Player"
	p.texture = blob_texture()
	p.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	p.position = pos
	p.scale = Vector2(scale_px, scale_px)
	return p

static func make_hud(size: Vector2) -> Node2D:
	# A small health bar, top left: a pale violet backing and a mustard fill. Used to show what an effect does NOT touch.
	var hud := Node2D.new()
	hud.name = "Hud"
	var pad := 0.03 * size.y
	var back := rect(Vector2(pad, pad), Vector2(0.20 * size.x, 0.05 * size.y), Color("#CFC6E8"), "HudBack")
	hud.add_child(back)
	var fill := rect(Vector2(pad * 1.3, pad * 1.3), Vector2(0.20 * size.x - pad * 0.6, 0.05 * size.y - pad * 0.6), MUSTARD, "HudFill")
	hud.add_child(fill)
	return hud

static func grab(root: Window) -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

static func px(img: Image, fx: float, fy: float) -> Array:
	# Reads the pixel at normalized (fx, fy); returns [r, g, b] as 0..1 floats rounded to 4 places.
	var x := clampi(int(fx * (img.get_width() - 1)), 0, img.get_width() - 1)
	var y := clampi(int(fy * (img.get_height() - 1)), 0, img.get_height() - 1)
	var c := img.get_pixel(x, y)
	return [snappedf(c.r, 0.0001), snappedf(c.g, 0.0001), snappedf(c.b, 0.0001)]

static func px_abs(img: Image, x: int, y: int) -> Array:
	var c := img.get_pixel(clampi(x, 0, img.get_width() - 1), clampi(y, 0, img.get_height() - 1))
	return [snappedf(c.r, 0.0001), snappedf(c.g, 0.0001), snappedf(c.b, 0.0001)]

static func close(a: Array, b: Array, tol: float = 0.01) -> bool:
	for i in 3:
		if absf(float(a[i]) - float(b[i])) > tol:
			return false
	return true

static func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

static func note(text: String) -> void:
	print("NOTE " + text)
