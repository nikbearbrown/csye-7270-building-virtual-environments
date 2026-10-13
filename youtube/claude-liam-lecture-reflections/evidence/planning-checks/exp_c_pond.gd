extends SceneTree
# Experiment C (Reflections layout): the hidden-mask reflection in the pond scene (see pond_common.gd for the geometry).
#
# Tree (the good order):  LabelMap, BackBufferCopy(viewport), Ground, Player(+RemoteTransform2D -> Reflection), Reflection.
# What is checked, per case:
#   leak       how many pixels of the FINAL frame are mask-coloured (pure red, or the half green)        -> the mask must stay hidden
#   reflection the set of pixels the reflection changed (frame with it minus frame without it) against the set the mask says it should
#              change (reflection-sprite pixels that lie over water). mismatch = size of the difference of the two sets.
# Cases: the good order at three x positions; the wrong orders (copy after the ground; mask over the ground; no copy node at all);
#        a see-through ground (alpha 0.9); the copy in rect mode; 90 frames of walking (no flicker, no one-frame lag).
#
# Run: godot --path <scratch project> [--rendering-method gl_compatibility] --script res://exp_c_pond.gd
# Output: one RESULT line per case.

const P = preload("res://pond_common.gd")
const SHADERS := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-reflections/lab-shaders/"

var scene: Node2D
var mask_tex: ImageTexture
var ground_tex: ImageTexture
var char_img: Image
var char_tex: ImageTexture
var player: Sprite2D
var reflection: Sprite2D
var bbc: BackBufferCopy
var mask_node: Sprite2D

func _initialize() -> void:
	call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func out(id: String, data: Dictionary) -> void:
	data["case"] = id
	print("RESULT " + JSON.stringify(data))

func build(order: String, shader_file: String, x: float, ground_alpha: float = 1.0, copy_mode: int = BackBufferCopy.COPY_MODE_VIEWPORT) -> void:
	if scene != null:
		scene.queue_free()
		await process_frame
	scene = Node2D.new()
	root.add_child(scene)
	var mask := Sprite2D.new()
	mask.name = "LabelMap"
	mask.texture = mask_tex
	mask.centered = false
	mask_node = mask
	var ground := Sprite2D.new()
	ground.name = "Ground"
	ground.texture = ground_tex
	ground.centered = false
	ground.modulate.a = ground_alpha
	bbc = BackBufferCopy.new()
	bbc.name = "BackBufferCopy"
	bbc.copy_mode = copy_mode
	if copy_mode == BackBufferCopy.COPY_MODE_RECT:
		bbc.position = Vector2(100, 100)          # default 200 x 200 box: covers screen x 0..200, y 0..200 only
	player = Sprite2D.new()
	player.name = "Player"
	player.texture = char_tex
	player.position = Vector2(x, P.PLAYER_Y)
	var rt := RemoteTransform2D.new()
	rt.name = "RemoteTransform2D"
	rt.position = Vector2(0, P.REFLECT_OFFSET)
	player.add_child(rt)
	reflection = Sprite2D.new()
	reflection.name = "Reflection"
	reflection.texture = char_tex
	reflection.flip_v = true
	reflection.material = P.load_shader(shader_file, SHADERS)
	match order:
		"good":
			for n in [mask, bbc, ground, player, reflection]:
				scene.add_child(n)
		"copy_after_ground":
			for n in [mask, ground, bbc, player, reflection]:
				scene.add_child(n)
		"mask_over_ground":
			for n in [ground, mask, bbc, player, reflection]:
				scene.add_child(n)
		"no_copy_node":
			for n in [mask, ground, player, reflection]:
				scene.add_child(n)
	rt.remote_path = rt.get_path_to(reflection)

func is_mask_colour(c: Color) -> bool:
	var red := Vector3(c.r - 1.0, c.g, c.b).length() < 0.2
	var green := Vector3(c.r, c.g - 128.0 / 255.0, c.b).length() < 0.2
	return red or green

func mask_influence() -> Dictionary:
	# How much does the hidden label map change the FINAL picture? Hide the reflection (it reads the mask), then toggle only the mask.
	reflection.visible = false
	mask_node.visible = true
	await frames(2)
	var with_mask := grab()
	mask_node.visible = false
	await frames(2)
	var without_mask := grab()
	mask_node.visible = true
	reflection.visible = true
	await frames(1)
	var n := 0
	var worst := 0.0
	for y in range(0, P.H, 2):
		for x in range(0, P.W, 2):
			var a := with_mask.get_pixel(x, y)
			var b := without_mask.get_pixel(x, y)
			var d := maxf(absf(a.r - b.r), maxf(absf(a.g - b.g), absf(a.b - b.b)))
			if d > 0.004:
				n += 1
			worst = maxf(worst, d)
	return {"pixels_changed_by_mask": n * 4, "largest_channel_change": snappedf(worst, 0.001)}

func leak_count(img: Image) -> int:
	var n := 0
	for y in range(0, P.H, 2):
		for x in range(0, P.W, 2):
			if is_mask_colour(img.get_pixel(x, y)):
				n += 1
	return n * 4          # sampled every second pixel in each direction

func expected_set(x: float, with_coast: bool) -> Dictionary:
	# Pixels of the (flipped) reflection sprite that lie over the labels the shader accepts.
	var s := {}
	var left := int(round(x)) - P.SPRITE_N / 2
	var top := int(round(P.PLAYER_Y + P.REFLECT_OFFSET)) - P.SPRITE_N / 2
	for j in range(P.SPRITE_N):
		for i in range(P.SPRITE_N):
			if char_img.get_pixel(i, j).a < 0.5:
				continue
			var sx := left + i
			var sy := top + (P.SPRITE_N - 1 - j)
			if sx < 0 or sx >= P.W or sy < 0 or sy >= P.H:
				continue
			var k := P.kind(sx, sy)
			if k == P.KIND_WATER or (with_coast and k == P.KIND_COAST):
				s[Vector2i(sx, sy)] = true
	return s

func observed_set(img_with: Image, img_without: Image, x: float) -> Dictionary:
	var s := {}
	var left := int(round(x)) - P.SPRITE_N / 2
	var top := int(round(P.PLAYER_Y + P.REFLECT_OFFSET)) - P.SPRITE_N / 2
	for sy in range(top, top + P.SPRITE_N):
		for sx in range(left, left + P.SPRITE_N):
			if sx < 0 or sx >= P.W or sy < 0 or sy >= P.H:
				continue
			var a := img_with.get_pixel(sx, sy)
			var b := img_without.get_pixel(sx, sy)
			if absf(a.r - b.r) + absf(a.g - b.g) + absf(a.b - b.b) > 0.03:
				s[Vector2i(sx, sy)] = true
	return s

func sym_diff(a: Dictionary, b: Dictionary) -> int:
	var n := 0
	for k in a:
		if not b.has(k):
			n += 1
	for k in b:
		if not a.has(k):
			n += 1
	return n

func observe(id: String, x: float, with_coast: bool = false, extra: Dictionary = {}) -> Dictionary:
	player.position.x = x
	await frames(3)
	var img_with := grab()
	reflection.visible = false
	await frames(2)
	var img_without := grab()
	reflection.visible = true
	await frames(1)
	var exp_s := expected_set(x, with_coast)
	var obs_s := observed_set(img_with, img_without, x)
	var cx := int(round(x))
	var cy := int(round(P.PLAYER_Y + P.REFLECT_OFFSET))
	var c := img_with.get_pixel(cx, cy)
	var infl: Dictionary = await mask_influence()
	var d := {"x": x, "leak_pixels": leak_count(img_with), "mask_influence": infl, "expected_reflection_pixels": exp_s.size(), "observed_reflection_pixels": obs_s.size(),
		"mismatch": sym_diff(exp_s, obs_s), "pixel_at_reflection_centre": [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)],
		"renderer": RenderingServer.get_current_rendering_method()}
	d.merge(extra)
	out(id, d)
	return d

func run() -> void:
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(P.W, P.H)
	await frames(3)
	var t0 := Time.get_ticks_msec()
	mask_tex = ImageTexture.create_from_image(P.make_mask_image())
	ground_tex = ImageTexture.create_from_image(P.make_ground_image())
	char_img = P.make_character_image()
	char_tex = ImageTexture.create_from_image(char_img)
	var img0 := grab()
	out("env", {"engine": Engine.get_version_info()["string"], "image_size": [img0.get_width(), img0.get_height()], "renderer": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name(), "art_built_ms": Time.get_ticks_msec() - t0})

	# C1: the good order, three positions: over water, over the sandbar, over water again.
	for x in [300.0, 880.0, 1180.0, 640.0]:
		await build("good", "02-reflection.gdshader", x)
		await observe("C1-good-order-x%d" % int(x), x)

	# C2: wrong orders
	await build("copy_after_ground", "02-reflection.gdshader", 300.0)
	await observe("C2a-copy-AFTER-ground", 300.0, false, {"tree": "LabelMap Ground BackBufferCopy Player Reflection"})
	await build("mask_over_ground", "02-reflection.gdshader", 300.0)
	await observe("C2b-mask-OVER-ground", 300.0, false, {"tree": "Ground LabelMap BackBufferCopy Player Reflection"})
	await build("no_copy_node", "02-reflection.gdshader", 300.0)
	await observe("C2c-no-copy-node", 300.0, false, {"tree": "LabelMap Ground Player Reflection"})

	# C3: a see-through ground lets the mask show
	await build("good", "02-reflection.gdshader", 300.0, 0.9)
	await observe("C3-ground-alpha-0.9", 300.0)

	# C4 (rect mode) needs a FRESH process: see exp_c4_rect_fresh.gd. Here the back buffer already holds earlier frames, so it would look fine.

	# C5: 90 frames of walking, one pixel per frame step of 10: no flicker, no one-frame lag.
	await build("good", "02-reflection.gdshader", 150.0)
	await frames(3)
	var worst := 0
	var bad_frames: Array = []
	var total := 0
	for f in range(90):
		var x := 150.0 + 10.0 * f
		player.position.x = x
		await process_frame                # exactly one frame after the move: a lagging RemoteTransform2D would show here
		var iw := grab()
		reflection.visible = false
		await process_frame
		var iwo := grab()
		reflection.visible = true
		var m := sym_diff(expected_set(x, false), observed_set(iw, iwo, x))
		total += m
		if m > worst:
			worst = m
		if m > 0:
			bad_frames.append([f, m])
	out("C5-walk-90-frames", {"frames": 90, "x_from": 150, "x_to": 1040, "total_mismatch_pixels": total, "worst_frame_mismatch": worst, "frames_with_any_mismatch": bad_frames.slice(0, 12),
		"renderer": RenderingServer.get_current_rendering_method()})

	# C6: save four pictures for a look (final frame; mask only; mask over ground; no reflection)
	await build("good", "02-reflection.gdshader", 520.0)
	await frames(3)
	grab().save_png("/private/tmp/claude-501/godot-shaders-reflections/pond2-good-x520.png")
	await build("good", "02-reflection.gdshader", 700.0)
	await frames(3)
	grab().save_png("/private/tmp/claude-501/godot-shaders-reflections/pond2-good-x700.png")
	await build("mask_over_ground", "02-reflection.gdshader", 520.0)
	await frames(3)
	grab().save_png("/private/tmp/claude-501/godot-shaders-reflections/pond2-mask-over-ground.png")
	var mask_only := Sprite2D.new()
	mask_only.texture = mask_tex
	mask_only.centered = false
	var s2 := Node2D.new()
	root.add_child(s2)
	s2.add_child(mask_only)
	scene.visible = false
	await frames(3)
	grab().save_png("/private/tmp/claude-501/godot-shaders-reflections/pond2-mask-only.png")
	quit(0)
