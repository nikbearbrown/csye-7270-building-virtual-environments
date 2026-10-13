extends SceneTree
# Claims about driving the flip from the game and about the "Your turn" checks, in a real window of Godot 4.7.2 (non-headless):
#  D1: set_shader_parameter("flip", 0.125) on the sprite's material from GDScript turns the 128 px card into a 90 px wide one (128 * cos 45 degrees);
#      0.5 mirrors it (gradient texture); the uniform is then read back unchanged.
#  D2: with flip = 0 the door shader (11-door.gdshader) draws exactly the same pixels as the sprite with NO shader, for any pivot (the identity check).
#  D3: with the pivot on the left edge (-64, 0) the left edge stays at x = -64 for every flip from 0 to 0.2 (the hinge check).
# Run: godot --path <project dir> --script res://verify3-from-the-game.gd   (the shader text is read from lab-shaders/11-door.gdshader via the DOOR_PATH constant)
const DOOR_PATH := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-matrices-and-fake-3d/lab-shaders/11-door.gdshader"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func gradient_texture() -> ImageTexture:
	var img := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	for y in 128:
		for x in 128:
			img.set_pixel(x, y, Color(x / 127.0, y / 127.0, 0.0, 1.0))
	return ImageTexture.create_from_image(img)

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func sprite_extent(img: Image) -> Array:
	var stage := Color("#D9D5CA")
	var x0 := 100000
	var x1 := -1
	var y0 := 100000
	var y1 := -1
	for y in img.get_height():
		for x in img.get_width():
			var c := img.get_pixel(x, y)
			if absf(c.r - stage.r) + absf(c.g - stage.g) + absf(c.b - stage.b) > 0.05:
				x0 = mini(x0, x)
				x1 = maxi(x1, x + 1)
				y0 = mini(y0, y)
				y1 = maxi(y1, y + 1)
	return [x0 - 320, x1 - 320, y0 - 180, y1 - 180]

func run() -> void:
	root.size = Vector2i(640, 360)
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	var tex := gradient_texture()
	var spr := Sprite2D.new()
	spr.texture = tex
	spr.position = Vector2(320, 180)
	root.add_child(spr)
	await frames(3)
	var plain := grab()                                     # the sprite with NO shader

	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(DOOR_PATH)
	var mat := ShaderMaterial.new()
	mat.shader = sh
	spr.material = mat
	await frames(3)

	# D2: identity at flip 0 for three pivots (the uniform's default is never read back as a number: it is null until set, so each is set explicitly)
	var diffs := {}
	for pv in [Vector2(-64, 0), Vector2(64, 0), Vector2(0, 0)]:
		mat.set_shader_parameter("pivot", pv)
		mat.set_shader_parameter("flip", 0.0)
		await frames(2)
		var img := grab()
		var maxd := 0.0
		for y in range(100, 260):
			for x in range(240, 400):
				var a := plain.get_pixel(x, y)
				var b := img.get_pixel(x, y)
				maxd = maxf(maxd, maxf(maxf(absf(a.r - b.r), absf(a.g - b.g)), absf(a.b - b.b)))
		diffs[str(pv)] = snappedf(maxd, 0.0001)
	out("D2-flip-zero-is-the-identity", {"max_channel_difference_from_the_sprite_with_no_shader_by_pivot": diffs, "reading": "0.0 means the pictures are identical, whatever the pivot"})

	# D1: drive the flip from GDScript
	mat.set_shader_parameter("pivot", Vector2(0, 0))
	mat.set_shader_parameter("flip", 0.125)
	await frames(2)
	var e45 := sprite_extent(grab())
	mat.set_shader_parameter("flip", 0.5)
	await frames(2)
	var half := grab()
	var tl := half.get_pixel(260, 119)
	var tr := half.get_pixel(378, 119)
	out("D1-set-shader-parameter-drives-the-flip", {"width_at_flip_0.125": e45[1] - e45[0], "expected_width": snappedf(128.0 * cos(TAU * 0.125), 0.1), "read_back": mat.get_shader_parameter("flip"),
		"top_left_pixel_at_0.5_is_red_like": [snappedf(tl.r, 0.01), snappedf(tl.g, 0.01), snappedf(tl.b, 0.01)], "top_right_pixel_at_0.5_is_black_like": [snappedf(tr.r, 0.01), snappedf(tr.g, 0.01), snappedf(tr.b, 0.01)],
		"reading": "the gradient's top left is black and its top right is red; at 0.5 they swap, so the card is mirrored"})

	# D3: the hinge check
	mat.set_shader_parameter("pivot", Vector2(-64, 0))
	var lefts: Array = []
	for f in [0.0, 0.05, 0.1, 0.15, 0.2]:
		mat.set_shader_parameter("flip", f)
		await frames(2)
		lefts.append([f, sprite_extent(grab())[0]])
	out("D3-hinge-edge-stays-put", {"left_edge_x_by_flip": lefts, "reading": "-64 every time: the hinge edge does not move while the card swings"})
	quit(0)
