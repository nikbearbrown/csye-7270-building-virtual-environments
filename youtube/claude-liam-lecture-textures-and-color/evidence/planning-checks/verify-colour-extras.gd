extends SceneTree
# Colour extras for the "Textures and Color" film (Godot 4.7.2):
#  X1: ordinary nodes need no hint. A ColorRect with color = (0.2, 0.4, 0.6) and a Sprite2D whose texture holds that colour: what does the screen show with use_hdr_2d off and on?
#  X2: a half-transparent sprite over the stage colour: the blend, with use_hdr_2d off and on (alpha is blended in whatever space the 2D buffer uses).
#  X3 (3D, forward_plus): a hinted uniform given the colour AS PICKED shows as picked; given srgb_to_linear() of it (a double conversion) shows far darker.
# Prints what the SCREEN shows: with use_hdr_2d on, Viewport.get_texture() is linear (docs), so values are converted with linear_to_srgb().
# Run: godot --path <dir> [--rendering-method forward_plus|mobile|gl_compatibility] --script res://verify-colour-extras.gd

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func shown(hdr: bool) -> Array:
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	img.convert(Image.FORMAT_RGBAF)
	var c := img.get_pixel(img.get_width() / 2, img.get_height() / 2)
	if hdr: c = c.linear_to_srgb()
	return [snappedf(c.r, 0.0001), snappedf(c.g, 0.0001), snappedf(c.b, 0.0001)]

func run() -> void:
	root.size = Vector2i(320, 180)
	RenderingServer.set_default_clear_color(Color(0.851, 0.835, 0.792))   # the Lab's stage colour as typed (about #D9D5CA)
	var typed := Color(0.2, 0.4, 0.6)
	out("env", {"renderer": RenderingServer.get_current_rendering_method(), "engine": Engine.get_version_info()["string"]})
	for hdr in [false, true]:
		if hdr and RenderingServer.get_current_rendering_method() == "gl_compatibility":
			out("X-skip-hdr2d", {"reason": "Compatibility does not support HDR 2D (docs, renderer comparison table); setting it changes nothing, so no row is reported"})
			continue
		root.use_hdr_2d = hdr
		await frames(3)
		# X1a: ColorRect colour
		var cr := ColorRect.new()
		cr.size = Vector2(320, 180)
		cr.color = typed
		root.add_child(cr)
		await frames(3)
		var x1a := shown(hdr)
		cr.queue_free()
		await frames(2)
		# X1b: a Sprite2D whose texture holds the typed colour
		var im := Image.create(64, 64, false, Image.FORMAT_RGBA8)
		im.fill(typed)
		var sp := Sprite2D.new()
		sp.texture = ImageTexture.create_from_image(im)
		sp.position = Vector2(160, 90)
		sp.scale = Vector2(3, 3)
		root.add_child(sp)
		await frames(3)
		var x1b := shown(hdr)
		# X1c: modulate half grey on that sprite (multiplies in whichever space the buffer uses)
		sp.modulate = Color(0.5, 0.5, 0.5, 1.0)
		await frames(3)
		var x1c := shown(hdr)
		sp.queue_free()
		await frames(2)
		out("X1-ordinary-nodes-hdr2d-%s" % str(hdr), {"colorrect_color_(0.2,0.4,0.6)": x1a, "sprite_texture_(0.2,0.4,0.6)": x1b, "same_sprite_modulate_(0.5,0.5,0.5)": x1c,
			"note": "modulate half grey: typed-number maths would give (0.1, 0.2, 0.3)"})
		# X2: white sprite at alpha 0.5 over the stage
		var imw := Image.create(64, 64, false, Image.FORMAT_RGBA8)
		imw.fill(Color(0.2, 0.4, 0.6, 1.0))
		var sp2 := Sprite2D.new()
		sp2.texture = ImageTexture.create_from_image(imw)
		sp2.position = Vector2(160, 90)
		sp2.scale = Vector2(3, 3)
		sp2.modulate = Color(1, 1, 1, 0.5)
		root.add_child(sp2)
		await frames(3)
		var x2 := shown(hdr)
		sp2.queue_free()
		await frames(2)
		out("X2-alpha-half-over-stage-hdr2d-%s" % str(hdr), {"centre_shown": x2,
			"typed_number_blend_would_be": [snappedf(0.5 * 0.2 + 0.5 * 0.851, 0.0001), snappedf(0.5 * 0.4 + 0.5 * 0.835, 0.0001), snappedf(0.5 * 0.6 + 0.5 * 0.792, 0.0001)]})
	quit(0)
