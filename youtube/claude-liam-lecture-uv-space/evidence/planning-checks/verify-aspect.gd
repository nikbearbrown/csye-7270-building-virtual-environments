extends SceneTree
# UV Space planning check A: where does a shader get the shape's proportions?
# One teal disc, drawn from UV, measured in pixels, on four kinds of node and with four sources of "aspect".
# Run: godot --path <project dir> --script res://verify-aspect.gd
# Every RESULT line: the teal bounding box (width x height in pixels). Round = width equals height.

const TEAL := Color(0.373, 0.639, 0.569)

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func disc_code(kind: String, radius: String = "0.8") -> String:
	var decl := ""
	var aspect := "1.0"
	if kind == "screenpx": aspect = "SCREEN_PIXEL_SIZE.y / SCREEN_PIXEL_SIZE.x"
	elif kind == "texpx": aspect = "TEXTURE_PIXEL_SIZE.y / TEXTURE_PIXEL_SIZE.x"
	elif kind == "uniform":
		decl = "uniform float aspect = 1.0;\n"
		aspect = "aspect"
	return "shader_type canvas_item;\n" + decl + "void fragment() {\n\tfloat a = " + aspect + ";\n\tvec2 p = UV * 2.0 - 1.0;\n\tp.x *= a;\n\tif (length(p) < " + radius + ") { COLOR = vec4(0.373, 0.639, 0.569, 1.0); } else { COLOR = vec4(0.0); }\n}\n"

func mat_of(code: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = code
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

func teal_box(img: Image) -> Dictionary:
	var x0 := 99999
	var x1 := -1
	var y0 := 99999
	var y1 := -1
	var n := 0
	for y in img.get_height():
		for x in img.get_width():
			var c := img.get_pixel(x, y)
			if absf(c.r - TEAL.r) < 0.03 and absf(c.g - TEAL.g) < 0.03 and absf(c.b - TEAL.b) < 0.03:
				n += 1
				x0 = mini(x0, x)
				x1 = maxi(x1, x)
				y0 = mini(y0, y)
				y1 = maxi(y1, y)
	if n == 0: return {"count": 0}
	return {"count": n, "width": x1 - x0 + 1, "height": y1 - y0 + 1}

func solid_texture(w: int, h: int) -> ImageTexture:
	var im := Image.create(w, h, false, Image.FORMAT_RGBA8)
	im.fill(Color.WHITE)
	return ImageTexture.create_from_image(im)

func run() -> void:
	root.size = Vector2i(640, 360)
	await frames(3)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name(), "root": [root.size.x, root.size.y]})

	# ---- A: a 400x200 ColorRect (2:1) sitting inside a 640x360 window (16:9). Four ways to get the aspect.
	var rect := ColorRect.new()
	rect.position = Vector2(120, 80)
	rect.size = Vector2(400, 200)
	root.add_child(rect)
	for kind in ["raw", "screenpx", "texpx", "uniform"]:
		var m := mat_of(disc_code(kind))
		if kind == "uniform": m.set_shader_parameter("aspect", rect.size.x / rect.size.y)
		rect.material = m
		await frames(3)
		var b := teal_box(grab())
		b["rect"] = [rect.size.x, rect.size.y]
		b["expected_if_round"] = "width == height"
		out("A-colorrect-400x200-in-640x360-" + kind, b)

	# ---- A5: the uniform follows the shape if the script updates it when the node is resized.
	# This is the exact text shown on screen in the film (beat B34), so the displayed code is the verified code.
	var code := "extends ColorRect\n\nfunc _update_aspect():\n\tmaterial.set_shader_parameter(\"aspect\", size.x / size.y)\n\nfunc _ready():\n\tresized.connect(_update_aspect)\n\t_update_aspect()\n"
	var scr := GDScript.new()
	scr.source_code = code
	var err := scr.reload()
	rect.set_script(scr)
	rect.material = mat_of(disc_code("uniform", "0.4"))
	rect.position = Vector2(120, 80)
	rect.size = Vector2(400, 200)
	rect.call("_ready")
	await frames(3)
	var b1 := teal_box(grab())
	b1["rect"] = [rect.size.x, rect.size.y]
	b1["script_reload_error"] = err
	out("A5-script-updates-aspect-2to1", b1)
	rect.position = Vector2(220, 20)
	rect.size = Vector2(200, 320)     # 5:8, taller than wide; fires `resized`
	await frames(3)
	var b2 := teal_box(grab())
	b2["rect"] = [rect.size.x, rect.size.y]
	out("A5-script-updates-aspect-after-resize-to-200x320", b2)
	# same size change, but the script does not update the uniform (stale aspect = 2.0)
	rect.material.set_shader_parameter("aspect", 2.0)
	await frames(3)
	var b3 := teal_box(grab())
	b3["rect"] = [rect.size.x, rect.size.y]
	b3["note"] = "uniform left stale at 2.0 while the shape is now 200x320"
	out("A5-stale-aspect-after-resize", b3)
	rect.queue_free()
	await frames(2)

	# ---- B: a ColorRect that fills the whole 640x360 window: SCREEN_PIXEL_SIZE is then right.
	var full := ColorRect.new()
	full.size = Vector2(640, 360)
	full.material = mat_of(disc_code("screenpx"))
	root.add_child(full)
	await frames(3)
	var bb := teal_box(grab())
	bb["rect"] = [640, 360]
	out("B-colorrect-fills-window-screenpx", bb)
	full.queue_free()
	await frames(2)

	# ---- C: a Sprite2D with a 256x128 texture, at scale 1: TEXTURE_PIXEL_SIZE is that texture's proportions.
	var spr := Sprite2D.new()
	spr.texture = solid_texture(256, 128)
	spr.position = Vector2(320, 180)
	root.add_child(spr)
	for kind2 in ["raw", "texpx", "screenpx", "uniform"]:
		var m2 := mat_of(disc_code(kind2))
		if kind2 == "uniform": m2.set_shader_parameter("aspect", 256.0 / 128.0)
		spr.material = m2
		await frames(3)
		var bc := teal_box(grab())
		bc["sprite_texture"] = [256, 128]
		out("C-sprite-256x128-" + kind2, bc)
	# C2: the same sprite scaled (3, 1) on screen: TEXTURE_PIXEL_SIZE still reports the texture, not the on-screen shape.
	spr.scale = Vector2(3.0, 1.0)
	spr.material = mat_of(disc_code("texpx", "0.8"))
	await frames(3)
	var bc2 := teal_box(grab())
	bc2["on_screen_size"] = [768, 128]
	bc2["note"] = "Sprite2D scale (3,1): on screen 768x128 (6:1); texture is 2:1"
	out("C2-sprite-scaled-3x1-texpx", bc2)
	spr.queue_free()
	await frames(2)

	# ---- D: a TextureRect (stretch) 400x300 showing a 256x128 texture: TEXTURE_PIXEL_SIZE is the texture's, not the rect's.
	var tr := TextureRect.new()
	tr.texture = solid_texture(256, 128)
	tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	tr.stretch_mode = TextureRect.STRETCH_SCALE
	tr.position = Vector2(120, 30)
	tr.size = Vector2(400, 300)
	root.add_child(tr)
	for kind3 in ["raw", "texpx", "uniform"]:
		var m3 := mat_of(disc_code(kind3))
		if kind3 == "uniform": m3.set_shader_parameter("aspect", tr.size.x / tr.size.y)
		tr.material = m3
		await frames(3)
		var bd := teal_box(grab())
		bd["texturerect"] = [400, 300]
		bd["texture"] = [256, 128]
		out("D-texturerect-400x300-of-256x128-" + kind3, bd)
	tr.queue_free()
	await frames(2)
	quit(0)
