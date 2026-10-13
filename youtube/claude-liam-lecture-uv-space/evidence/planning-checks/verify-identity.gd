extends SceneTree
# UV Space planning check D: is "texture(TEXTURE, UV)" really "the picture comes out exactly as it went in"?
# A Sprite2D draws the Lab's test sprite with no material; then the three-line lookup shader (lab-shaders/03-lookup.gdshader) is assigned;
# both frames are grabbed in the same window and compared pixel by pixel. Also: the same with the copy-bend-look template (04) unbent.
# Run: godot --path <project dir> --script res://verify-identity.gd

const LOOKUP := "shader_type canvas_item;\n\nvoid fragment() {\n\tCOLOR = texture(TEXTURE, UV);\n}\n"
const TEMPLATE := "shader_type canvas_item;\n\nvoid fragment() {\n\tvec2 uv = UV;\n\t// bend uv here\n\tCOLOR = texture(TEXTURE, uv);\n}\n"

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func sprite_image(n: int) -> Image:
	# the same picture as lab/runner.gd's "sprite" kind: a plain teal blob with two cream eyes, transparent padding all round
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
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

func diff(a: Image, b: Image) -> Dictionary:
	var worst := 0.0
	var n := 0
	for y in a.get_height():
		for x in a.get_width():
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			var d := maxf(maxf(absf(ca.r - cb.r), absf(ca.g - cb.g)), maxf(absf(ca.b - cb.b), absf(ca.a - cb.a)))
			if d > 0.0: n += 1
			worst = maxf(worst, d)
	return {"pixels_that_differ": n, "largest_channel_difference": snappedf(worst, 0.0001), "pixels": a.get_width() * a.get_height()}

func mat_of(code: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = code
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

func run() -> void:
	root.size = Vector2i(640, 360)
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	var spr := Sprite2D.new()
	spr.texture = ImageTexture.create_from_image(sprite_image(128))
	spr.position = Vector2(320, 180)
	spr.scale = Vector2(2.25, 2.25)
	spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(spr)
	await frames(4)
	var plain := grab()
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "image": [plain.get_width(), plain.get_height()]})
	spr.material = mat_of(LOOKUP)
	await frames(4)
	out("D1-lookup-shader-against-no-material", diff(plain, grab()))
	spr.material = mat_of(TEMPLATE)
	await frames(4)
	out("D2-copy-bend-look-unbent-against-no-material", diff(plain, grab()))
	spr.material = null
	await frames(4)
	out("D3-no-material-again-against-first-frame", diff(plain, grab()))
	quit(0)
