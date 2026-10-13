extends SceneTree
# UV Space planning check B: what happens when the address leaves 0..1, and what controls it.
# The picture is a 256x256 "address picture": red = how far across (x/255), green = how far down (y/255), so the colour we READ
# is the address we LOOKED UP. Shader: texture(TEXTURE, UV * 2.0). Probed at output pixels whose address is 1.254 / 1.574 etc.
# Run: godot --path <project dir> --script res://verify-repeat.gd

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func addr_picture() -> ImageTexture:
	var im := Image.create(256, 256, false, Image.FORMAT_RGBA8)
	for y in 256:
		for x in 256:
			im.set_pixel(x, y, Color(x / 255.0, y / 255.0, 0.0, 1.0))
	return ImageTexture.create_from_image(im)

func rg(img: Image, x: int, y: int) -> Array:
	var c := img.get_pixel(x, y)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001)]

func mat_of(code: String) -> ShaderMaterial:
	var sh := Shader.new()
	sh.code = code
	var m := ShaderMaterial.new()
	m.shader = sh
	return m

const NODE_CODE := "shader_type canvas_item;\nvoid fragment() {\n\tvec2 uv = UV * 2.0;\n\tCOLOR = texture(TEXTURE, uv);\n}\n"

func run() -> void:
	root.size = Vector2i(256, 256)
	await frames(3)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "root": [root.size.x, root.size.y],
		"enum_values": {"PARENT_NODE": CanvasItem.TEXTURE_REPEAT_PARENT_NODE, "DISABLED": CanvasItem.TEXTURE_REPEAT_DISABLED, "ENABLED": CanvasItem.TEXTURE_REPEAT_ENABLED, "MIRROR": CanvasItem.TEXTURE_REPEAT_MIRROR}})
	var tex := addr_picture()

	# ---- R1: Sprite2D, the node's own TEXTURE, every texture_repeat mode.
	# Probes (output px -> address after UV*2): (64,64) -> 0.504 (inside the first copy); (160,64) -> (1.254, 0.504); (200,200) -> (1.574, 1.574).
	var spr := Sprite2D.new()
	spr.texture = tex
	spr.centered = false
	spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	spr.material = mat_of(NODE_CODE)
	root.add_child(spr)
	for mode in [CanvasItem.TEXTURE_REPEAT_PARENT_NODE, CanvasItem.TEXTURE_REPEAT_DISABLED, CanvasItem.TEXTURE_REPEAT_ENABLED, CanvasItem.TEXTURE_REPEAT_MIRROR]:
		spr.texture_repeat = mode
		await frames(3)
		var img := grab()
		out("R1-sprite-texture_repeat-%d" % mode, {"mode": mode, "read_at_addr_0.504": rg(img, 64, 64), "read_at_addr_1.254_0.504": rg(img, 160, 64), "read_at_addr_1.574_1.574": rg(img, 200, 200)})
	spr.queue_free()
	await frames(2)

	# ---- R2: TextureRect, same shader, texture_repeat enabled. The docs say TextureRect is not affected by texture_repeat.
	var tr := TextureRect.new()
	tr.texture = tex
	tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	tr.stretch_mode = TextureRect.STRETCH_SCALE
	tr.size = Vector2(256, 256)
	tr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	tr.material = mat_of(NODE_CODE)
	root.add_child(tr)
	for mode2 in [CanvasItem.TEXTURE_REPEAT_DISABLED, CanvasItem.TEXTURE_REPEAT_ENABLED, CanvasItem.TEXTURE_REPEAT_MIRROR]:
		tr.texture_repeat = mode2
		await frames(3)
		var img2 := grab()
		out("R2-textureRect-texture_repeat-%d" % mode2, {"mode": mode2, "read_at_addr_0.504": rg(img2, 64, 64), "read_at_addr_1.254_0.504": rg(img2, 160, 64), "read_at_addr_1.574_1.574": rg(img2, 200, 200)})
	tr.queue_free()
	await frames(2)

	# ---- R3: a texture declared as a uniform: no hint, repeat_enable, repeat_disable.
	for hint in ["", " : repeat_enable", " : repeat_disable"]:
		var code: String = "shader_type canvas_item;\nuniform sampler2D pic" + str(hint) + ";\nvoid fragment() {\n\tvec2 uv = UV * 2.0;\n\tCOLOR = texture(pic, uv);\n}\n"
		var cr := ColorRect.new()
		cr.size = Vector2(256, 256)
		var m := mat_of(code)
		m.set_shader_parameter("pic", tex)
		cr.material = m
		root.add_child(cr)
		await frames(3)
		var img3 := grab()
		out("R3-sampler-uniform-hint[%s]" % str(hint).strip_edges(), {"hint": str(hint).strip_edges(), "read_at_addr_0.504": rg(img3, 64, 64), "read_at_addr_1.254_0.504": rg(img3, 160, 64), "read_at_addr_1.574_1.574": rg(img3, 200, 200)})
		cr.queue_free()
		await frames(2)
	quit(0)
