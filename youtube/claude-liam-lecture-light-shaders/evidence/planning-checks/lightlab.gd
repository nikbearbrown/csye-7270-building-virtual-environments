extends RefCounted
# lightlab.gd: helpers shared by the Light Shaders planning checks (Godot 4.7.2).
# Not a film asset. It builds small 2D scenes (a sprite, a dark CanvasModulate, one or more lights) so a light() function can be measured.

static func solid_tex(c: Color, n: int = 128) -> ImageTexture:
	var im := Image.create(n, n, false, Image.FORMAT_RGBA8)
	im.fill(c)
	return ImageTexture.create_from_image(im)

static func radial_tex(n: int = 256) -> GradientTexture2D:
	# the docs' own recipe for a light texture: a radial GradientTexture2D, opaque white in the middle, transparent white at the edge
	var g := Gradient.new()
	g.set_color(0, Color(1, 1, 1, 1))
	g.set_color(1, Color(1, 1, 1, 0))
	var t := GradientTexture2D.new()
	t.gradient = g
	t.fill = GradientTexture2D.FILL_RADIAL
	t.fill_from = Vector2(0.5, 0.5)
	t.fill_to = Vector2(1.0, 0.5)
	t.width = n
	t.height = n
	return t

static func point_light(pos: Vector2, tex: Texture2D, tex_scale: float = 1.0, energy: float = 1.0, color: Color = Color.WHITE, height: float = 0.0) -> PointLight2D:
	var l := PointLight2D.new()
	l.texture = tex
	l.texture_scale = tex_scale
	l.energy = energy
	l.color = color
	l.position = pos
	l.height = height
	return l

static func dir_light(rot_deg: float, energy: float = 1.0, color: Color = Color.WHITE) -> DirectionalLight2D:
	var l := DirectionalLight2D.new()
	l.rotation_degrees = rot_deg
	l.energy = energy
	l.color = color
	return l

static func shader_mat(code: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = code
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

static func sprite(tex: Texture2D, pos: Vector2, scl: Vector2 = Vector2.ONE, mat: Material = null) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = tex
	s.position = pos
	s.scale = scl
	s.material = mat
	return s

static func canvas_mod(c: Color) -> CanvasModulate:
	var m := CanvasModulate.new()
	m.color = c
	return m

static func px(img: Image, x: int, y: int) -> Array:
	var c := img.get_pixel(x, y)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]
