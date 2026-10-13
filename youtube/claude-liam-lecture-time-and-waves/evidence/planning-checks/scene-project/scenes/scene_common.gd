extends RefCounted
# Shared helpers for the Time and Waves capture scenes. Every scene positions things as fractions of the viewport, so any capture size works.
# FILM is the layout folder; the shaders come from its lab-shaders/. Nothing here is drawn from memory: the scenes only load tested files.
const FILM := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-time-and-waves"
const TEAL := Color("#5FA391")
const CREAM := Color("#FAF9F5")
# verification only: packs TIME into red/green/blue so a planning script can read it back from a saved frame; never part of a capture
const ENCODER := "shader_type canvas_item;\nvoid fragment() {\n\tfloat whole = floor(TIME);\n\tfloat part = (TIME - whole) * 255.0;\n\tfloat p1 = floor(part);\n\tCOLOR = vec4(whole / 255.0, p1 / 255.0, part - p1, 1.0);\n}\n"

static func shader_text(name: String) -> String:
	return FileAccess.get_file_as_string(FILM + "/lab-shaders/" + name)

static func shaded_rect(code: String, pos: Vector2, size: Vector2) -> ColorRect:
	var rect := ColorRect.new()
	rect.position = pos
	rect.size = size
	var sh := Shader.new()
	sh.code = code
	var mat := ShaderMaterial.new()
	mat.shader = sh
	rect.material = mat
	return rect

static func plain_rect(color: Color, pos: Vector2, size: Vector2) -> ColorRect:
	var rect := ColorRect.new()
	rect.color = color
	rect.position = pos
	rect.size = size
	return rect

static func wants_verify() -> bool:
	return OS.get_cmdline_user_args().has("--verify")

const STAGE := Color("#D9D5CA")        # the Shader Lab's warm light grey: far from ink, so GATE T does not read the stage as text

static func stage() -> void:
	RenderingServer.set_default_clear_color(STAGE)

# the test sprite: a teal blob with two cream eyes and transparent padding all round (the series cast, same as lab/runner.gd's "sprite")
static func blob_texture() -> ImageTexture:
	var img := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	var cen := Vector2(64, 64)
	for y in range(128):
		for x in range(128):
			if Vector2(x, y).distance_to(cen) < 38.4:
				img.set_pixel(x, y, TEAL)
			if Vector2(x, y).distance_to(cen + Vector2(-12.8, -7.68)) < 4.48 or Vector2(x, y).distance_to(cen + Vector2(12.8, -7.68)) < 4.48:
				img.set_pixel(x, y, CREAM)
	return ImageTexture.create_from_image(img)

# the banner: four stripes in the middle 96 rows of a 256 x 128 picture, 16 empty rows above and below so a ripple has room to move into
static func banner_texture() -> ImageTexture:
	var img := Image.create(256, 128, false, Image.FORMAT_RGBA8)
	img.fill(Color(0, 0, 0, 0))
	for y in range(16, 112):
		var stripe := ((y - 16) / 24) % 2 == 0
		for x in range(256):
			img.set_pixel(x, y, TEAL if stripe else CREAM)
	return ImageTexture.create_from_image(img)

# the breath: a slow rise, a short hold, a long fall; flat tangents at every point make smooth ease-in and ease-out
static func breath_curve_texture() -> CurveTexture:
	var c := Curve.new()
	c.add_point(Vector2(0.0, 0.0))
	c.add_point(Vector2(0.40, 1.0))
	c.add_point(Vector2(0.55, 1.0))
	c.add_point(Vector2(1.0, 0.0))
	var ct := CurveTexture.new()
	ct.curve = c
	return ct

static func shaded_sprite(tex: Texture2D, shader_file: String, pos: Vector2, scale: float) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = tex
	s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	s.position = pos
	s.scale = Vector2(scale, scale)
	var sh := Shader.new()
	sh.code = shader_text(shader_file)
	var m := ShaderMaterial.new()
	m.shader = sh
	s.material = m
	return s
