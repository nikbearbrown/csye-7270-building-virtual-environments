extends SceneTree
# Does light() run once per light? A light() that outputs a constant 0.2 red, under 0, 1, 2, 3 identical overlapping PointLight2D.
# If it runs once per light and the results add, the red channel reads ~0.2, ~0.4, ~0.6. Also: does an EMPTY light() remove default lighting?
# Run: godot --path <project dir> --script res://verify4.gd

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func center_rgb() -> Array:
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var c := img.get_pixel(img.get_width() / 2, img.get_height() / 2)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]

func make_light(pos: Vector2) -> PointLight2D:
	var l := PointLight2D.new()
	var im := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	im.fill(Color.WHITE)
	l.texture = ImageTexture.create_from_image(im)
	l.texture_scale = 4.0
	l.energy = 1.0
	l.position = pos
	return l

func run() -> void:
	root.size = Vector2i(320, 180)
	# A dark CanvasModulate makes lights matter: unlit sprites are black, lit ones show only what the lights add.
	var dark := CanvasModulate.new()
	dark.color = Color(0, 0, 0, 1)
	root.add_child(dark)
	var im := Image.create(100, 100, false, Image.FORMAT_RGBA8)
	im.fill(Color.WHITE)
	var spr := Sprite2D.new()
	spr.texture = ImageTexture.create_from_image(im)
	spr.position = Vector2(160, 90)
	root.add_child(spr)
	await frames(3)
	out("L0-dark-canvas-no-lights", {"center_rgb": center_rgb(), "note": "no light() written, no lights, CanvasModulate black"})
	var base_light := make_light(Vector2(160, 90))
	root.add_child(base_light)
	await frames(3)
	out("L0b-default-lighting-one-light", {"center_rgb": center_rgb(), "note": "no light() written, one white light: default lighting"})
	base_light.queue_free()
	await frames(2)

	var sh := Shader.new()
	sh.code = "shader_type canvas_item;\nvoid light() { LIGHT = vec4(0.2, 0.0, 0.0, 1.0); }\n"
	var mat := ShaderMaterial.new()
	mat.shader = sh
	spr.material = mat
	await frames(3)
	out("L1-light-defined-no-lights", {"center_rgb": center_rgb(), "note": "light() written, zero lights"})

	var lights: Array = []
	for n in range(1, 4):
		var l := make_light(Vector2(160, 90))
		root.add_child(l)
		lights.append(l)
		await frames(3)
		out("L2-light-count-%d" % n, {"lights": n, "center_rgb": center_rgb()})

	# An EMPTY light() replaces the built-in lighting.
	for l in lights:
		l.queue_free()
	await frames(2)
	var l1 := make_light(Vector2(160, 90))
	root.add_child(l1)
	var sh2 := Shader.new()
	sh2.code = "shader_type canvas_item;\nvoid light() { }\n"
	var mat2 := ShaderMaterial.new()
	mat2.shader = sh2
	spr.material = mat2
	await frames(3)
	var empty_with_light := center_rgb()
	spr.material = null
	await frames(3)
	var default_with_light := center_rgb()
	out("L3-empty-light-function", {"with_empty_light_fn_and_one_light": empty_with_light, "with_no_light_fn_and_one_light": default_with_light})
	quit(0)
