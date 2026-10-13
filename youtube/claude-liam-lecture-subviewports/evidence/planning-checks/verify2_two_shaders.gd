extends SceneTree
# SubViewports film, check 2: two shaders in a row, with the film's own shader files (../../lab-shaders/*.gdshader, read from disk).
#  F1  the inner shader's result is in the picture: a gradient by the SPRITE's own UV.y (teal at the top of the sprite, gold at the bottom)
#  F2  an outer pass-through (02-outer-passthrough) shows the picture exactly: every pixel of the 512 x 512 display equals the picture over the stage
#  F3  the outer fade (03-outer-fade) is x / 512 across the WHOLE picture (read on an opaque white picture, so every pixel can be read)
#  F4  turn the sprite inside the viewport by half a turn: the inner gradient flips with it; the outer fade does not move
# Run: godot --path <project> --fixed-fps 30 --script res://verify2_two_shaders.gd

const STAGE := Common.STAGE
const GOLD := Color(0.93, 0.76, 0.35)

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame
		RenderingServer.force_draw(false)   # one real draw per step: a covered window is not drawn on every frame (RESULTS.md, run X)

func main_img() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func channel(c: Color, i: int) -> float:
	return [c.r, c.g, c.b][i]

func implied_fade(screen: Color, picture: Color) -> float:
	# for an opaque picture pixel: screen = picture * f + stage * (1 - f). Solve f on the channel with the most contrast.
	var best := 0
	var gap := 0.0
	for i in 3:
		if absf(channel(picture, i) - channel(STAGE, i)) > gap:
			gap = absf(channel(picture, i) - channel(STAGE, i))
			best = i
	return (channel(STAGE, best) - channel(screen, best)) / (channel(STAGE, best) - channel(picture, best))

func run() -> void:
	root.size = Vector2i(1280, 720)
	Common.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	var stage_rect := ColorRect.new()
	stage_rect.color = STAGE
	stage_rect.size = Vector2(1280, 720)
	root.add_child(stage_rect)

	var sub := SubViewport.new()
	sub.size = Vector2i(512, 512)
	sub.transparent_bg = true
	root.add_child(sub)
	var inner := Sprite2D.new()
	inner.texture = ImageTexture.create_from_image(CaptureScene.blob_image(448, true))
	inner.position = Vector2(256, 256)
	inner.material = Common.material_from_file("01-inner-gradient.gdshader")
	sub.add_child(inner)
	var disp := Sprite2D.new()
	disp.centered = false
	disp.position = Vector2(384, 104)
	disp.texture = sub.get_texture()
	disp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(disp)
	var tex := sub.get_texture()

	# ---------------------------------------------------------------- F1
	disp.material = Common.material_from_file("02-outer-passthrough.gdshader")
	await frames(4)
	var pic := tex.get_image()
	var samples: Array = []
	for y: int in [150, 256, 362]:                # sprite spans y = 32 .. 480, so sprite UV.y = (y + 0.5 - 32) / 448
		var uvy: float = (y + 0.5 - 32.0) / 448.0
		var e_r: float = Common.TEAL.r * (1.0 - uvy) + GOLD.r * uvy
		var e_b: float = Common.TEAL.b * (1.0 - uvy) + GOLD.b * uvy
		var c := pic.get_pixel(256, y)
		samples.append({"y": y, "sprite_uv_y": snappedf(uvy, 0.001), "picture_rgb": Common.rgb(c), "expected_r": snappedf(e_r, 0.001), "expected_b": snappedf(e_b, 0.001)})
	Common.out("F1-inner-gradient-is-in-the-picture", {"samples_at_x_256": samples, "reading": "the picture holds the inner shader's colours: mix(teal, gold, UV.y) of the sprite"})

	# ---------------------------------------------------------------- F2: whole-image equality
	var img := main_img()
	pic = tex.get_image()
	var worst := 0.0
	var bad := 0
	for y in range(0, 512, 1):
		for x in range(0, 512, 1):
			var p := pic.get_pixel(x, y)
			# the picture stores premultiplied colour; over the stage, premultiplied blending gives p.rgb + stage * (1 - a)
			var expect := Color(p.r + STAGE.r * (1.0 - p.a), p.g + STAGE.g * (1.0 - p.a), p.b + STAGE.b * (1.0 - p.a))
			var d := Common.diff(expect, img.get_pixel(384 + x, 104 + y))
			worst = maxf(worst, d)
			if d > 0.006:
				bad += 1
	Common.out("F2-outer-passthrough-equals-the-picture", {"pixels_compared": 512 * 512, "pixels_off_by_more_than_one_8bit_step": bad, "largest_channel_difference": snappedf(worst, 0.0001), "reading": "the outer shader that copies TEXTURE shows the picture exactly (a difference of 0.0039 is one 8-bit step)"})

	# ---------------------------------------------------------------- F3: fade across the whole picture, on an opaque white picture
	var white := ColorRect.new()
	white.color = Color.WHITE
	white.size = Vector2(512, 512)
	sub.add_child(white)
	inner.visible = false
	disp.material = Common.material_from_file("03-outer-fade.gdshader")
	await frames(4)
	img = main_img()
	var fade: Array = []
	for x: int in [2, 128, 256, 384, 509]:
		var sc := img.get_pixel(384 + x, 104 + 256)
		fade.append({"picture_x": x, "expected_x_over_512": snappedf((x + 0.5) / 512.0, 0.001), "implied_fade": snappedf(implied_fade(sc, Color.WHITE), 0.001)})
	Common.out("F3-outer-fade-runs-across-the-whole-picture", {"samples": fade, "reading": "an opaque picture: the multiplier is x / 512 from the picture's left edge to its right edge, empty parts included"})
	white.queue_free()
	inner.visible = true

	# ---------------------------------------------------------------- F4: half a turn inside the viewport
	var offs := [Vector2i(-60, 40), Vector2i(-30, 40), Vector2i(0, 40), Vector2i(30, 40), Vector2i(60, 40)]
	var fade_rows: Dictionary = {}
	var grad_rows: Dictionary = {}
	for rot: float in [0.0, PI]:
		inner.rotation = rot
		await frames(4)
		pic = tex.get_image()
		img = main_img()
		var rows: Array = []
		for o: Vector2i in offs:
			var px := 256 + o.x
			var py := 256 + o.y
			var pc := pic.get_pixel(px, py)
			if pc.a < 0.99:
				continue
			rows.append({"picture_x": px, "expected_x_over_512": snappedf((px + 0.5) / 512.0, 0.001), "implied_fade": snappedf(implied_fade(img.get_pixel(384 + px, 104 + py), pc), 0.001)})
		fade_rows[str(snappedf(rot, 0.001))] = rows
		grad_rows[str(snappedf(rot, 0.001))] = {"red_100px_above_the_centre": snappedf(pic.get_pixel(256, 156).r, 0.001), "red_100px_below_the_centre": snappedf(pic.get_pixel(256, 356).r, 0.001)}
	Common.out("F4a-the-fade-does-not-turn", {"by_rotation_radians": fade_rows, "reading": "at both rotations the multiplier at a picture pixel is x / 512: the fade belongs to the picture and stays put"})
	Common.out("F4b-the-gradient-turns-with-the-sprite", {"by_rotation_radians": grad_rows, "reading": "gold has a high red value, teal a low one. Rotation 0: gold is below (below > above). After half a turn (3.142): gold is above (above > below): the sprite's own UV turned with it"})
	quit(0)
