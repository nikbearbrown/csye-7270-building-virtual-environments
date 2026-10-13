extends SceneTree
# SubViewports film, check 6: three shaders in a row, where each shader runs, and input.
#  X3  viewport 1 (inner gradient) -> viewport 2 (fade) -> the screen (stripes): the final pixels follow stripes x fade x gradient
#  X4  the outer shader runs once per pixel of the DISPLAY: a 64 px picture shown 8x has blocky silhouette edges but stripe edges at single display pixels
#  X5  mouse input does not reach a standalone SubViewport; a SubViewportContainer forwards it (docs: "InputEvents are not passed to a standalone SubViewport by default")
# Run: godot --path <project> --fixed-fps 30 --script res://verify6_chain_resolution_input.gd

const STAGE := Common.STAGE

var pressed_flag := false

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame
		RenderingServer.force_draw(false)   # one real draw per step: a covered window is not drawn on every frame (RESULTS.md, run X)

func main_img() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func clear_all() -> void:
	for c in root.get_children():
		c.queue_free()

func stage() -> void:
	var r := ColorRect.new()
	r.color = STAGE
	r.size = Vector2(1280, 720)
	root.add_child(r)

func blob(pos: Vector2, size: int = 448, bleed: bool = true) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = ImageTexture.create_from_image(CaptureScene.blob_image(size, bleed))
	s.position = pos
	return s

func run() -> void:
	root.size = Vector2i(1280, 720)
	Common.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})

	# ---------------------------------------------------------------- X3
	stage()
	var vp1 := SubViewport.new()
	vp1.size = Vector2i(512, 512)
	vp1.transparent_bg = true
	root.add_child(vp1)
	var b1 := blob(Vector2(256, 256))
	b1.material = Common.material_from_file("01-inner-gradient.gdshader")
	vp1.add_child(b1)
	var vp2 := SubViewport.new()
	vp2.size = Vector2i(512, 512)
	vp2.transparent_bg = true
	root.add_child(vp2)
	var d1 := Sprite2D.new()
	d1.centered = false
	d1.texture = vp1.get_texture()
	d1.material = Common.material_from_file("03-outer-fade.gdshader")
	vp2.add_child(d1)
	var d2 := Sprite2D.new()
	d2.centered = false
	d2.position = Vector2(384, 104)
	d2.texture = vp2.get_texture()
	d2.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	d2.material = Common.material_from_file("04-stripes.gdshader")
	root.add_child(d2)
	await frames(6)
	var img := main_img()
	var pic1 := vp1.get_texture().get_image()
	var mism := 0
	var checked := 0
	var worst := 0.0
	for py in range(130, 390, 4):
		for px in range(130, 390, 4):
			var pc := pic1.get_pixel(px, py)
			if pc.a < 0.99:
				continue
			var u := (px + 0.5) / 512.0
			var v := (py + 0.5) / 512.0
			var s := fmod(u + v, 1.0 / 6.0) * 6.0
			if absf(s - 0.5) < 0.05 or s < 0.03 or s > 0.97:
				continue
			var sc := img.get_pixel(384 + px, 104 + py)
			var on_got := Common.diff(sc, STAGE) > 0.01
			checked += 1
			if (s < 0.5) != on_got:
				mism += 1
			if s < 0.5 and on_got:
				var expect := Color(pc.r * u + STAGE.r * (1.0 - u), pc.g * u + STAGE.g * (1.0 - u), pc.b * u + STAGE.b * (1.0 - u))
				worst = maxf(worst, Common.diff(expect, sc))
	Common.out("X3-three-shaders-in-a-row", {"pixels_checked": checked, "stripe_on_off_mismatches": mism, "largest_colour_error_on_stripe_pixels": snappedf(worst, 0.001), "reading": "viewport 1 (inner gradient) -> viewport 2 (fade) -> screen (stripes): the final pixels follow stripes x fade x gradient (an error of 0.004 is one 8-bit step)"})

	# ---------------------------------------------------------------- X4
	clear_all()
	await frames(2)
	stage()
	var vp := SubViewport.new()
	vp.size = Vector2i(64, 64)
	vp.transparent_bg = true
	root.add_child(vp)
	var bb := blob(Vector2(32, 32))
	bb.scale = Vector2(64.0 / 448.0, 64.0 / 448.0)
	vp.add_child(bb)
	var dd := Sprite2D.new()
	dd.centered = false
	dd.position = Vector2(384, 104)
	dd.scale = Vector2(8, 8)
	dd.texture = vp.get_texture()
	dd.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	dd.material = Common.material_from_file("04-stripes.gdshader")
	root.add_child(dd)
	await frames(5)
	img = main_img()
	var row_y := 104 + 8 * 34
	var edges: Array = []
	var prev := false
	for x in range(384 + 8 * 10, 384 + 8 * 54):
		var on := Common.diff(img.get_pixel(x, row_y), STAGE) > 0.01
		if x > 384 + 8 * 10 and on != prev:
			edges.append(x - 384)
		prev = on
	dd.material = Common.material_from_file("02-outer-passthrough.gdshader")
	await frames(3)
	img = main_img()
	var blob_edges: Array = []
	prev = false
	for x in range(384, 384 + 8 * 64):
		var on2 := Common.diff(img.get_pixel(x, row_y), STAGE) > 0.01
		if x > 384 and on2 != prev:
			blob_edges.append(x - 384)
		prev = on2
	var res_stripe: Array = []
	for e: int in edges:
		res_stripe.append(e % 8)
	var res_blob: Array = []
	for e: int in blob_edges:
		res_blob.append(e % 8)
	Common.out("X4-the-outer-shader-runs-per-display-pixel", {"stripe_edge_x_in_the_display": edges, "stripe_edges_mod_8": res_stripe, "blob_silhouette_edge_x_in_the_display": blob_edges, "blob_edges_mod_8": res_blob, "reading": "the picture is 64 px drawn 8x: the blob's edges always fall on a multiple of 8 display pixels (picture pixels); the stripe edges do not (the first stripe 'edge' is the blob's own edge): the outer shader works on display pixels"})

	# ---------------------------------------------------------------- X5
	clear_all()
	await frames(2)
	stage()
	var psub := SubViewport.new()
	psub.size = Vector2i(200, 100)
	root.add_child(psub)
	var btn := Button.new()
	btn.text = "press"
	btn.size = Vector2(200, 100)
	pressed_flag = false
	btn.pressed.connect(func(): pressed_flag = true)
	psub.add_child(btn)
	var pd := Sprite2D.new()
	pd.centered = false
	pd.position = Vector2(300, 100)
	pd.texture = psub.get_texture()
	root.add_child(pd)
	await frames(4)
	for pressed in [true, false]:
		var ev := InputEventMouseButton.new()
		ev.button_index = MOUSE_BUTTON_LEFT
		ev.position = Vector2(350, 150)
		ev.global_position = ev.position
		ev.pressed = pressed
		root.push_input(ev)
		await frames(2)
	var standalone_pressed := pressed_flag
	pressed_flag = false
	var cont := SubViewportContainer.new()
	cont.position = Vector2(700, 100)
	var csub := SubViewport.new()
	csub.size = Vector2i(200, 100)
	cont.add_child(csub)
	var btn2 := Button.new()
	btn2.text = "press"
	btn2.size = Vector2(200, 100)
	btn2.pressed.connect(func(): pressed_flag = true)
	csub.add_child(btn2)
	root.add_child(cont)
	await frames(4)
	for pressed in [true, false]:
		var ev2 := InputEventMouseButton.new()
		ev2.button_index = MOUSE_BUTTON_LEFT
		ev2.position = Vector2(750, 150)
		ev2.global_position = ev2.position
		ev2.pressed = pressed
		root.push_input(ev2)
		await frames(2)
	Common.out("X5-input", {"button_pressed_with_a_standalone_SubViewport": standalone_pressed, "button_pressed_inside_a_SubViewportContainer": pressed_flag, "reading": "false then true: a standalone SubViewport does not receive the click; inside a SubViewportContainer it does"})
	quit(0)
