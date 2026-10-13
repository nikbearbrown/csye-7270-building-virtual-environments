extends RefCounted
# Test textures and small helpers shared by the outline film's scratch checks (verify_*.gd).
# blob() reproduces the Shader Lab's "sprite" texture exactly (lab/runner.gd): teal disc radius 0.30*n, two cream eyes, transparent padding.

const TEAL := Color("#5FA391")
const CREAM := Color("#FAF9F5")
const STAGE := Color("#D9D5CA")

static func blob(n: int = 128) -> Image:
	var img := Image.create_empty(n, n, false, Image.FORMAT_RGBA8)
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
	return img

# The same disc with an antialiased rim: alpha ramps from 1 to 0 across about one pixel, so the rim has half-transparent pixels.
static func blob_soft(n: int = 128) -> Image:
	var img := Image.create_empty(n, n, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var c := Vector2(n / 2.0, n / 2.0)
	var r := n * 0.30
	for y in n:
		for x in n:
			var d := Vector2(x, y).distance_to(c)
			var a := clampf(r - d + 0.5, 0.0, 1.0)
			if a > 0.0:
				img.set_pixel(x, y, Color(TEAL.r, TEAL.g, TEAL.b, a))
	return img

# A square sprite: a teal square (half the image wide) with the same two cream eyes as the disc, transparent padding all round.
static func crate(n: int = 128) -> Image:
	var img := Image.create_empty(n, n, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var c := Vector2(n / 2.0, n / 2.0)
	var half := int(n * 0.25)
	for y in range(int(c.y) - half, int(c.y) + half):
		for x in range(int(c.x) - half, int(c.x) + half):
			img.set_pixel(x, y, TEAL)
	for y in n:
		for x in n:
			var e1 := Vector2(x, y).distance_to(c + Vector2(-n * 0.10, -n * 0.06))
			var e2 := Vector2(x, y).distance_to(c + Vector2(n * 0.10, -n * 0.06))
			if e1 < n * 0.035 or e2 < n * 0.035:
				img.set_pixel(x, y, CREAM)
	return img

# A wide pill (rounded bar) for the animation frames.
static func pill(n: int = 128) -> Image:
	var img := Image.create_empty(n, n, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var c := Vector2(n / 2.0, n / 2.0)
	for y in n:
		for x in n:
			var d := Vector2(maxf(absf(x - c.x) - n * 0.20, 0.0), absf(y - c.y)).length()
			if d < n * 0.14:
				img.set_pixel(x, y, TEAL)
	return img

# A plus sign: arms with half-length 24 and half-width 8 image pixels in a 64 x 64 image (the bigger-copy check).
static func plus(n: int = 64, white: bool = false) -> Image:
	var img := Image.create_empty(n, n, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var c := n / 2
	var col := Color.WHITE if white else TEAL
	for y in range(c - 8, c + 8):
		for x in range(c - 24, c + 24):
			img.set_pixel(x, y, col)
	for y in range(c - 24, c + 24):
		for x in range(c - 8, c + 8):
			img.set_pixel(x, y, col)
	return img

# A packed two-frame sprite sheet, 128 x 64: frame 0 (left) is a solid teal square with two eyes that touches all four of its edges, frame 1 (right) is the disc, padded.
static func sheet() -> Image:
	var img := Image.create_empty(128, 64, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	for y in 64:
		for x in 64:
			img.set_pixel(x, y, TEAL)
	for e in [Vector2(20, 24), Vector2(44, 24)]:
		for y in 64:
			for x in 64:
				if Vector2(x, y).distance_to(e) < 4.5:
					img.set_pixel(x, y, CREAM)
	var c := Vector2(96, 32)
	for y in 64:
		for x in range(64, 128):
			if Vector2(x, y).distance_to(c) < 18.0:
				img.set_pixel(x, y, TEAL)
	for e in [c + Vector2(-6, -4), c + Vector2(6, -4)]:
		for y in 64:
			for x in range(64, 128):
				if Vector2(x, y).distance_to(e) < 2.6:
					img.set_pixel(x, y, CREAM)
	return img

# Texture factory for the scene player: {"kind": "blob" | "blob_soft" | "mascot" | "crate" | "plus" | "pill" | "sheet", "size": 128, "crop": false, "pad": 0}
static func make_texture(t: Dictionary, pad_script: Object = null) -> ImageTexture:
	var kind: String = t.get("kind", "blob")
	var size := int(t.get("size", 128))
	var img: Image
	match kind:
		"blob": img = blob(size)
		"blob_soft": img = blob_soft(size)
		"mascot": img = mascot(size)
		"speck": img = blob_speck(size)
		"crate": img = crate(size)
		"plus": img = plus(int(t.get("size", 64)), bool(t.get("white", false)))
		"pill": img = pill(size)
		"sheet": img = sheet()
		_: img = blob(size)
	if t.get("crop", false):
		img = crop_to_content(img)
	if t.has("cut"):                                   # a rectangle [x, y, w, h] of the image (a zoomed look at part of the rim)
		var r: Array = t["cut"]
		img = img.get_region(Rect2i(int(r[0]), int(r[1]), int(r[2]), int(r[3])))
	var tex := ImageTexture.create_from_image(img)
	var pad := int(t.get("pad", 0))
	if pad > 0 and pad_script != null:
		tex = pad_script.add_padding(tex, pad)
	return tex

# The disc plus one isolated opaque pixel (a stray speck) far from it: an opaque pixel whose neighbors are all empty.
static func blob_speck(n: int = 128) -> Image:
	var img := blob(n)
	img.set_pixel(104, 30, TEAL)
	return img

# A thin part: the disc plus a three-pixel-wide stem ending in a small ball (hard edges, like pixel art). The stem is the thin part.
static func mascot(n: int = 128) -> Image:
	var img := blob(n)
	var c := Vector2(n / 2.0, n / 2.0)
	for y in range(16, 28):                     # stem: rows 16 to 27, columns 63 to 65 (three pixels wide), joins the disc at its top (row 26)
		for x in range(int(c.x) - 1, int(c.x) + 2):
			img.set_pixel(x, y, TEAL)
	var ball := Vector2(c.x, 13.0)
	for y in n:
		for x in n:
			if Vector2(x, y).distance_to(ball) < 3.6:
				img.set_pixel(x, y, TEAL)
	return img

static func opaque_rect(img: Image) -> Rect2i:
	var minx := img.get_width(); var miny := img.get_height(); var maxx := -1; var maxy := -1
	for y in img.get_height():
		for x in img.get_width():
			if img.get_pixel(x, y).a > 0.0:
				minx = mini(minx, x); miny = mini(miny, y); maxx = maxi(maxx, x); maxy = maxi(maxy, y)
	return Rect2i(minx, miny, maxx - minx + 1, maxy - miny + 1)

static func crop_to_content(img: Image) -> Image:
	var r := opaque_rect(img)
	return img.get_region(r)

# Shader files are read from the film folder: OUTLINE_FILM_DIR (absolute path of claude-liam-lecture-outlines) must be set in the environment.
static func film_dir() -> String:
	var d := OS.get_environment("OUTLINE_FILM_DIR")
	return d if d != "" else ProjectSettings.globalize_path("res://")

static func shader_code(shader_name: String) -> String:
	for sub in ["lab-shaders/", "evidence/planning-checks/shaders/", ""]:
		var p := film_dir().path_join(sub + shader_name)
		if FileAccess.file_exists(p):
			return FileAccess.get_file_as_string(p)
	push_error("shader not found: " + shader_name)
	return ""

static func material(shader_name: String, params: Dictionary = {}) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = shader_code(shader_name)
	var m := ShaderMaterial.new()
	m.shader = sh
	for k in params:
		m.set_shader_parameter(k, params[k])
	return m

static func snap(win: Window) -> Image:
	RenderingServer.force_draw(false)
	return win.get_texture().get_image()

static func save(img: Image, path: String) -> void:
	DirAccess.make_dir_recursive_absolute(path.get_base_dir())
	img.save_png(path)
