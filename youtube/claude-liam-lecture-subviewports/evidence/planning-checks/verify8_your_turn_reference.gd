extends SceneTree
# SubViewports film, check 8: the "Your turn" prompt, solved by hand (not by a model) as a reference, to prove that its two checks are meaningful.
# Prompt: a 512 px SubViewport with a transparent background holds a sprite whose own shader paints its lower half red; a second sprite shows the
# viewport's texture with Premultiplied Alpha and a shader that keeps only vertical stripes (fract of UV.x times eight).
# The test blob stands in for the Godot icon (the icon is not available to a script-only scratch project).
#  Y1  check one: with the outer shader off (display shown with Premultiplied Alpha only), the picture holds the sprite with its lower half red and NO box around it
#  Y2  check two: turn the sprite by half a turn: the red half moves with it; the vertical stripes do not move (every probe matches the formula at both rotations)
# Run: godot --path <project> --fixed-fps 30 --script res://verify8_your_turn_reference.gd

const STAGE := Common.STAGE

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame
		RenderingServer.force_draw(false)   # one real draw per step: a covered window is not drawn on every frame (RESULTS.md, run X)

func main_img() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func run() -> void:
	root.size = Vector2i(1280, 720)
	Common.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	var st := ColorRect.new()
	st.color = STAGE
	st.size = Vector2(1280, 720)
	root.add_child(st)
	var sub := SubViewport.new()
	sub.size = Vector2i(512, 512)
	sub.transparent_bg = true
	root.add_child(sub)
	var icon := Sprite2D.new()
	icon.texture = ImageTexture.create_from_image(CaptureScene.blob_image(448, true))
	icon.position = Vector2(256, 256)
	icon.material = Common.material_from_file("10-your-turn-inner.gdshader")
	sub.add_child(icon)
	var disp := Sprite2D.new()
	disp.centered = false
	disp.position = Vector2(384, 104)
	disp.texture = sub.get_texture()
	disp.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	var cim := CanvasItemMaterial.new()
	cim.blend_mode = CanvasItemMaterial.BLEND_MODE_PREMULT_ALPHA
	disp.material = cim
	root.add_child(disp)
	await frames(5)
	var img := main_img()
	Common.out("Y1-check-one-outer-shader-off", {"screen_100px_above_the_icon_centre": Common.rgb(img.get_pixel(640, 260)), "screen_100px_below_the_icon_centre": Common.rgb(img.get_pixel(640, 460)), "screen_in_an_empty_corner_of_the_picture": Common.rgb(img.get_pixel(384 + 20, 104 + 20)), "stage": Common.rgb(STAGE), "reading": "teal above, red (0.85, 0.22, 0.2) below, and the empty corner is the stage colour: no box"})
	disp.material = Common.material_from_file("11-your-turn-outer.gdshader")
	var out: Dictionary = {}
	for rot: float in [0.0, PI]:
		icon.rotation = rot
		await frames(4)
		img = main_img()
		var pic := sub.get_texture().get_image()
		var mism := 0
		var n := 0
		for py in range(130, 390, 4):
			for px in range(130, 390, 4):
				if pic.get_pixel(px, py).a < 0.99:
					continue
				var s := ((px + 0.5) / 512.0) * 8.0
				s = s - floorf(s)
				if absf(s - 0.5) < 0.05 or s < 0.03 or s > 0.97:
					continue
				var on_got := Common.diff(img.get_pixel(384 + px, 104 + py), STAGE) > 0.03
				n += 1
				if (s < 0.5) != on_got:
					mism += 1
		out[str(snappedf(rot, 0.001))] = {"red_half_is_at": "bottom" if pic.get_pixel(256, 356).r > pic.get_pixel(256, 156).r else "top", "pixels_checked": n, "stripe_mismatches": mism}
	Common.out("Y2-check-two-turn-the-icon", {"by_rotation_radians": out, "reading": "the red half is at the bottom, then at the top after half a turn; the vertical stripes have zero mismatches at both rotations: they stay still"})
	quit(0)
