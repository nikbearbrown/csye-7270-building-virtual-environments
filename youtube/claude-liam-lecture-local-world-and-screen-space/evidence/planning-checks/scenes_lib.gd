extends RefCounted
# scenes_lib.gd: reference builders for the custom Godot scenes behind this film's captures (the build session's capture harness
# reproduces these; the numbers they print are in FACTCHECK.md). Logical canvas 1280 x 720, stage colour #D9D5CA (the Lab's),
# test sprite = the Lab's teal blob (128 px art with transparent padding), shaders loaded from the film's lab-shaders/ folder.

const SkyLib := preload("res://sky_lib.gd")
const SHADER_DIR := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-local-world-and-screen-space/lab-shaders/"
const STAGE := Color("#D9D5CA")
const TEAL := Color("#5FA391")
const CREAM := Color("#FAF9F5")

static var _sky_cache := {}


static func shader_dir() -> String:
	var e := OS.get_environment("LOCAL_WORLD_SHADERS")     # override: a folder holding the film's lab-shaders (trailing slash optional)
	if e == "":
		return SHADER_DIR
	return e if e.ends_with("/") else e + "/"


static func material(shader_file: String, params: Dictionary = {}) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(shader_dir() + shader_file)
	var mat := ShaderMaterial.new()
	mat.shader = sh
	for k in params.keys():
		mat.set_shader_parameter(k, params[k])
	return mat


static func sky_texture(n: int = 1536) -> ImageTexture:
	if not _sky_cache.has(n):
		_sky_cache[n] = ImageTexture.create_from_image(SkyLib.make_sky(n))
	return _sky_cache[n]


# the Lab's "sprite": a teal blob with two cream eyes and transparent padding, n x n.
# aa = true gives the edge of the body and the eyes a 1.5 px soft edge, so the blob stays smooth when the captures magnify it 3x (the 4K route).
static func blob_image(n: int = 128, aa: bool = false) -> Image:
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var c := Vector2(n / 2.0, n / 2.0)
	var soft := 1.5 if aa else 0.0
	for y in n:
		for x in n:
			var p := Vector2(x + 0.5, y + 0.5) if aa else Vector2(x, y)
			var d := p.distance_to(c)
			var rb := n * 0.30
			if aa:
				var a := clampf((rb - d) / soft + 0.5, 0.0, 1.0)
				if a > 0.0:
					img.set_pixel(x, y, Color(TEAL.r, TEAL.g, TEAL.b, a))
			elif d < rb:
				img.set_pixel(x, y, TEAL)
			var e1 := p.distance_to(c + Vector2(-n * 0.10, -n * 0.06))
			var e2 := p.distance_to(c + Vector2(n * 0.10, -n * 0.06))
			var re := n * 0.035
			if aa:
				var ae := clampf((re - minf(e1, e2)) / soft + 0.5, 0.0, 1.0)
				if ae > 0.0:
					var under := img.get_pixel(x, y)
					var out_a := maxf(under.a, ae)
					img.set_pixel(x, y, Color(under.r, under.g, under.b, under.a).lerp(Color(CREAM.r, CREAM.g, CREAM.b, out_a), ae))
			elif e1 < re or e2 < re:
				img.set_pixel(x, y, CREAM)
	return img


static func blob_texture(n: int = 128, aa: bool = false) -> ImageTexture:
	return ImageTexture.create_from_image(blob_image(n, aa))


static func white_texture(n: int = 128) -> ImageTexture:
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	img.fill(Color.WHITE)
	return ImageTexture.create_from_image(img)


# cream / teal checker, 8 x 8 squares (the Lab's "checker")
static func checker_texture(n: int = 256) -> ImageTexture:
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	for y in n:
		for x in n:
			var on := ((x / (n / 8)) + (y / (n / 8))) % 2 == 0
			img.set_pixel(x, y, CREAM if on else TEAL)
	return ImageTexture.create_from_image(img)


static func sprite(tex: Texture2D, pos: Vector2, scale: float, mat: Material = null) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = tex
	s.position = pos
	s.scale = Vector2(scale, scale)
	s.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	if mat:
		s.material = mat
	return s


# a ColorRect that shows the world sky through 02-sky-world (the faint backdrop and the stage-sized sky)
static func sky_rect(rect: Rect2, alpha: float, shader_file: String = "02-sky-world.gdshader") -> ColorRect:
	var cr := ColorRect.new()
	cr.position = rect.position
	cr.size = rect.size
	cr.modulate = Color(1, 1, 1, alpha)
	cr.material = material(shader_file, {"sky": sky_texture()})
	return cr
