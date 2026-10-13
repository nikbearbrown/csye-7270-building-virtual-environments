extends SceneTree
# SubViewports film, check 5: a transparent SubViewport picture holds PREMULTIPLIED colour, so it must be shown (and faded) with premultiplied blending.
# Ground truth: the same half-transparent sprite drawn straight onto the stage, no viewport.
#  P1  what the picture stores for a pixel that is teal at alpha 0.5
#  P2  the screen colour of that pixel: default blend vs Premultiplied Alpha (CanvasItemMaterial and render_mode blend_premul_alpha), against the ground truth
#  P3  fading it by a half: alpha only vs the whole colour, under both blends (the film's 03-outer-fade is "whole colour + blend_premul_alpha")
#  X1  setting alpha (COLOR.a = UV.x) on a transparent picture turns the EMPTY parts into a dark haze; multiplying the whole colour does not
#  G1  the film's gold glow (soft edge) shown with Mix and with Premultiplied Alpha: the ring pixel against the same glow drawn directly (capture C06's numbers)
# Run: godot --path <project> --fixed-fps 30 --script res://verify5_premultiplied.gd   (and with --rendering-method gl_compatibility)

const STAGE := Common.STAGE
const TEAL := Common.TEAL

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame
		RenderingServer.force_draw(false)   # one real draw per step: a covered window is not drawn on every frame (RESULTS.md, run X)

func main_img() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func half_texture() -> ImageTexture:
	var img := Image.create(64, 64, false, Image.FORMAT_RGBA8)
	img.fill(Color(TEAL.r, TEAL.g, TEAL.b, 0.5))
	return ImageTexture.create_from_image(img)

func run() -> void:
	root.size = Vector2i(1280, 720)
	Common.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	var stage_rect := ColorRect.new()
	stage_rect.color = STAGE
	stage_rect.size = Vector2(1280, 720)
	root.add_child(stage_rect)

	var direct := Sprite2D.new()
	direct.texture = half_texture()
	direct.centered = false
	direct.position = Vector2(20, 20)
	root.add_child(direct)
	var sub := SubViewport.new()
	sub.size = Vector2i(64, 64)
	sub.transparent_bg = true
	root.add_child(sub)
	var inner := Sprite2D.new()
	inner.texture = half_texture()
	inner.centered = false
	sub.add_child(inner)

	var add_display := func(pos: Vector2, mat: Material) -> Sprite2D:
		var d := Sprite2D.new()
		d.centered = false
		d.position = pos
		d.texture = sub.get_texture()
		d.material = mat
		root.add_child(d)
		return d
	var cim_mix := CanvasItemMaterial.new()
	var cim_pre := CanvasItemMaterial.new()
	cim_pre.blend_mode = CanvasItemMaterial.BLEND_MODE_PREMULT_ALPHA
	add_display.call(Vector2(120, 20), null)
	add_display.call(Vector2(220, 20), cim_mix)
	add_display.call(Vector2(320, 20), cim_pre)
	add_display.call(Vector2(420, 20), Common.material_from_code("shader_type canvas_item;\nrender_mode blend_premul_alpha;\nvoid fragment() { COLOR = texture(TEXTURE, UV); }\n"))
	var variants := {
		"alpha only, default blend": "shader_type canvas_item;\nvoid fragment() { COLOR = texture(TEXTURE, UV); COLOR.a *= 0.5; }\n",
		"whole colour, default blend": "shader_type canvas_item;\nvoid fragment() { COLOR = texture(TEXTURE, UV) * 0.5; }\n",
		"alpha only, premultiplied blend": "shader_type canvas_item;\nrender_mode blend_premul_alpha;\nvoid fragment() { COLOR = texture(TEXTURE, UV); COLOR.a *= 0.5; }\n",
		"whole colour, premultiplied blend (the film's 03-outer-fade form)": "shader_type canvas_item;\nrender_mode blend_premul_alpha;\nvoid fragment() { COLOR = texture(TEXTURE, UV) * 0.5; }\n",
	}
	var i := 0
	var fade_pos: Dictionary = {}
	for k: String in variants:
		var pos := Vector2(20 + i * 100, 120)
		add_display.call(pos, Common.material_from_code(variants[k]))
		fade_pos[k] = pos
		i += 1
	var direct_fade := Sprite2D.new()
	direct_fade.texture = half_texture()
	direct_fade.centered = false
	direct_fade.position = Vector2(520, 120)
	direct_fade.modulate = Color(1, 1, 1, 0.5)
	root.add_child(direct_fade)
	await frames(6)
	var img := main_img()
	var pic := sub.get_texture().get_image()
	var p := pic.get_pixel(32, 32)
	Common.out("P1-what-a-transparent-picture-stores", {"picture_pixel_rgba": Common.rgba(p), "teal": Common.rgb(TEAL), "half_of_teal": [snappedf(TEAL.r * 0.5, 0.001), snappedf(TEAL.g * 0.5, 0.001), snappedf(TEAL.b * 0.5, 0.001)], "reading": "a pixel that is teal at alpha 0.5 is stored as half of teal with alpha about 0.5: already multiplied by its alpha"})
	var truth := img.get_pixel(20 + 32, 20 + 32)
	var rows := {
		"default sprite material": Common.rgb(img.get_pixel(120 + 32, 20 + 32)),
		"CanvasItemMaterial, Blend Mode Mix": Common.rgb(img.get_pixel(220 + 32, 20 + 32)),
		"CanvasItemMaterial, Blend Mode Premultiplied Alpha": Common.rgb(img.get_pixel(320 + 32, 20 + 32)),
		"shader with render_mode blend_premul_alpha": Common.rgb(img.get_pixel(420 + 32, 20 + 32)),
	}
	Common.out("P2-screen-colour-of-a-half-transparent-pixel", {"ground_truth_the_sprite_drawn_directly": Common.rgb(truth), "through_the_picture": rows, "reading": "the right answer is the ground truth; the default blend darkens every half-transparent pixel, Premultiplied Alpha matches (to one 8-bit step)"})
	var tf := img.get_pixel(520 + 32, 120 + 32)
	var fades := {}
	for k: String in fade_pos:
		var pos2: Vector2 = fade_pos[k]
		fades[k] = Common.rgb(img.get_pixel(int(pos2.x) + 32, int(pos2.y) + 32))
	Common.out("P3-fading-a-half-transparent-pixel-by-a-half", {"ground_truth_drawn_directly_with_modulate_alpha_0.5": Common.rgb(tf), "variants": fades, "reading": "only the whole colour with premultiplied blending matches the ground truth"})

	# ---------------------------------------------------------------- X1: set alpha vs multiply the whole colour, on a transparent picture with an empty part
	for c in root.get_children():
		if c != stage_rect:
			c.queue_free()
	await frames(2)
	var sub2 := SubViewport.new()
	sub2.size = Vector2i(512, 512)
	sub2.transparent_bg = true
	root.add_child(sub2)
	var blob := Sprite2D.new()
	blob.texture = ImageTexture.create_from_image(CaptureScene.blob_image(448, true))
	blob.position = Vector2(256, 256)
	sub2.add_child(blob)
	var x1 := {
		"COLOR.a = UV.x (set alpha, default blend)": "shader_type canvas_item;\nvoid fragment() {\n\tCOLOR = texture(TEXTURE, UV);\n\tCOLOR.a = UV.x;\n}\n",
		"COLOR.a *= UV.x (multiply alpha, default blend)": "shader_type canvas_item;\nvoid fragment() {\n\tCOLOR = texture(TEXTURE, UV);\n\tCOLOR.a *= UV.x;\n}\n",
		"the film's 03-outer-fade (whole colour * UV.x, premultiplied blend)": Common.shader_text("03-outer-fade.gdshader"),
	}
	var j := 0
	for k: String in x1:
		var d := Sprite2D.new()
		d.centered = false
		d.scale = Vector2(0.4, 0.4)
		d.position = Vector2(20 + j * 220, 20)
		d.texture = sub2.get_texture()
		d.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		d.material = Common.material_from_code(x1[k])
		root.add_child(d)
		j += 1
	await frames(5)
	img = main_img()
	j = 0
	var xr := {}
	for k: String in x1:
		var c := img.get_pixel(int(20 + j * 220 + 256 * 0.4), int(20 + 20 * 0.4))      # an EMPTY picture pixel at the top middle, UV.x 0.5
		xr[k] = {"screen_at_an_empty_picture_pixel": Common.rgb(c), "difference_from_the_stage": snappedf(Common.diff(c, STAGE), 0.001)}
		j += 1
	Common.out("X1-set-alpha-turns-the-empty-parts-into-haze", {"stage": Common.rgb(STAGE), "results": xr, "reading": "an empty picture pixel must show the stage. Setting alpha makes it a visible dark haze (the empty pixels' colour is black, their alpha is not zero any more)"})

	# ---------------------------------------------------------------- G1: the gold glow of capture C06
	for c in root.get_children():
		if c != stage_rect:
			c.queue_free()
	await frames(2)
	var glow_tex := ImageTexture.create_from_image(CaptureScene.glow_image(512))
	var truth_sprite := Sprite2D.new()
	truth_sprite.texture = glow_tex
	truth_sprite.centered = false
	truth_sprite.position = Vector2(20, 100)
	root.add_child(truth_sprite)
	var sub3 := SubViewport.new()
	sub3.size = Vector2i(512, 512)
	sub3.transparent_bg = true
	root.add_child(sub3)
	var gs := Sprite2D.new()
	gs.texture = glow_tex
	gs.position = Vector2(256, 256)
	sub3.add_child(gs)
	var dm := Sprite2D.new()
	dm.centered = false
	dm.position = Vector2(560, 100)
	dm.texture = sub3.get_texture()
	var c_mix := CanvasItemMaterial.new()
	dm.material = c_mix
	root.add_child(dm)
	await frames(5)
	img = main_img()
	# the glow's alpha is 1 inside 0.55 * r, falling to 0 at r = 215: alpha 0.5 where d = 215 * (1 - 0.45 * 0.5) = 166.6 px from the centre
	var gx := 256 + 167
	var gy := 256
	var truth_c := img.get_pixel(20 + gx, 100 + gy)
	var mix_c := img.get_pixel(560 + gx, 100 + gy)
	c_mix.blend_mode = CanvasItemMaterial.BLEND_MODE_PREMULT_ALPHA
	await frames(4)
	img = main_img()
	var pre_c := img.get_pixel(560 + gx, 100 + gy)
	Common.out("G1-the-gold-glow-of-capture-c06", {"ring_pixel_at_picture_x_423_y_256": {"drawn_directly (the right answer)": Common.rgb(truth_c), "through_the_picture_with_Mix": Common.rgb(mix_c), "through_the_picture_with_Premultiplied_Alpha": Common.rgb(pre_c)}, "glow_alpha_at_that_pixel": snappedf(sub3.get_texture().get_image().get_pixel(gx, gy).a, 0.01), "reading": "at a half-transparent ring pixel Mix is visibly darker than the right answer; Premultiplied Alpha matches it"})
	quit(0)
