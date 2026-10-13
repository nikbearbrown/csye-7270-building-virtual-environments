extends SceneTree
# Experiment G (Reflections layout): the film's limit beat says "mirroring the whole screen is a different technique".
# Check that it exists and works: a rect over the water reads the screen texture with a flipped address, so the scenery AND the
# character appear mirrored. Same pond art, no mask, no per-pixel label: the screen is read as a PICTURE.
# Run: godot --path <scratch project> --script res://exp_g_mirror_the_screen.gd
const P = preload("res://pond_common.gd")

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func rgb(c: Color) -> Array:
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(P.W, P.H)
	await frames(3)
	var layers := P.make_layers(1)
	var scene := Node2D.new()
	root.add_child(scene)
	var ground := Sprite2D.new()
	ground.texture = ImageTexture.create_from_image(layers["ground"])
	ground.centered = false
	var player := Sprite2D.new()
	player.texture = ImageTexture.create_from_image(P.make_character_image())
	player.position = Vector2(300, P.PLAYER_Y)
	var bbc := BackBufferCopy.new()
	bbc.copy_mode = BackBufferCopy.COPY_MODE_VIEWPORT
	var water := ColorRect.new()
	water.position = Vector2(0, P.SHORE_Y)
	water.size = Vector2(P.W, P.H - P.SHORE_Y)
	var sh := Shader.new()
	sh.code = "shader_type canvas_item;\nuniform sampler2D screen_texture : hint_screen_texture;\nvoid fragment() {\n\tvec2 uv = SCREEN_UV;\n\tuv.y = 2.0 * %f - uv.y;\n\tCOLOR = vec4(texture(screen_texture, uv).rgb, 1.0);\n}\n" % (float(P.SHORE_Y) / float(P.H))
	var mat := ShaderMaterial.new()
	mat.shader = sh
	water.material = mat
	for n in [ground, player, bbc, water]:
		scene.add_child(n)
	await frames(4)
	var img := grab()
	# the character's centre is (300, 278); its mirror about y = 350 is (300, 422). Grass at (100, 320) mirrors to (100, 380).
	var d := {"character_centre_pixel": rgb(img.get_pixel(300, 278)), "mirrored_pixel_at_300_422": rgb(img.get_pixel(300, 422)),
		"grass_pixel_at_100_320": rgb(img.get_pixel(100, 320)), "mirrored_pixel_at_100_380": rgb(img.get_pixel(100, 380)),
		"sky_pixel_at_100_150": rgb(img.get_pixel(100, 150)), "mirrored_pixel_at_100_550": rgb(img.get_pixel(100, 550)),
		"renderer": RenderingServer.get_current_rendering_method()}
	print("RESULT " + JSON.stringify(d))
	img.save_png("/private/tmp/claude-501/godot-shaders-reflections/mirror-the-screen.png")
	quit(0)
