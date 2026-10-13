extends SceneTree
# SubViewports film, check 3: stripes and hue, with the film's own shader files (../../lab-shaders/*.gdshader).
#  S1  04-stripes on a plain rectangle: the number of saws across the top edge is `count`, and the stripe is on for `width` of each saw
#  H1  the film's hsv_to_rgb (06-hsv-strip.gdshader) against the engine's own Color.from_hsv over 65,536 pixels (hue x saturation) and 65,536 (hue x value)
#  H1b the six exact hues (a probe rectangle per hue) give pure red, yellow, green, cyan, blue, magenta
#  H2  05-stripes-moving on the picture: every probe pixel matches the stripe formula in PICTURE space at three sprite rotations (TIME read in the same draw)
#  H3  control: the same stripe shader ON the sprite itself: the stripes follow the sprite's own UV and turn with it
#  H4  07-rainbow-stripes: the colour of a stripe pixel is hsv(fract(diagonal), 1, 1); the gaps show the inner gradient
# Run: godot --path <project> --fixed-fps 30 --script res://verify3_stripes_hue.gd

const STAGE := Common.STAGE

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n):
		await process_frame
		RenderingServer.force_draw(false)   # one real draw per step: a covered window is not drawn on every frame (RESULTS.md, run X)

func main_img() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func saw_of(d: float, count: float) -> float:
	var x := d * count
	return x - floorf(x)

func clear_all() -> void:
	for c in root.get_children():
		c.queue_free()

func run() -> void:
	root.size = Vector2i(1280, 720)
	Common.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})

	# ---------------------------------------------------------------- S1: count and width on a plain rectangle (TEXTURE is white there)
	var stage_rect := ColorRect.new()
	stage_rect.color = STAGE
	stage_rect.size = Vector2(1280, 720)
	root.add_child(stage_rect)
	var s1: Dictionary = {}
	for cfg: Array in [[6.0, 0.5], [10.0, 0.25], [3.0, 0.8]]:
		var r := ColorRect.new()
		r.position = Vector2(0, 0)
		r.size = Vector2(1000, 200)
		var m := Common.material_from_file("04-stripes.gdshader")
		m.set_shader_parameter("count", cfg[0])
		m.set_shader_parameter("width", cfg[1])
		r.material = m
		root.add_child(r)
		await frames(3)
		var img := main_img()
		var on_px := 0
		var runs := 0
		var prev := false
		var full_runs := 0
		var run_len := 0
		for x in range(0, 1000):
			var on := Common.diff(img.get_pixel(x, 0), STAGE) > 0.03
			if on: on_px += 1
			if on and not prev:
				runs += 1
				run_len = 0
			if on: run_len += 1
			if prev and not on and run_len > 8:
				full_runs += 1
			prev = on
		s1["count %s width %s" % [cfg[0], cfg[1]]] = {"on_fraction_of_the_top_row": snappedf(on_px / 1000.0, 0.001), "stripes_on_the_top_row": runs, "of_which_complete": full_runs}
		r.queue_free()
		await frames(2)
	Common.out("S1-count-and-width", {"measured": s1, "reading": "the on-fraction equals width; the top row holds `count` complete stripes (plus a sliver at the right edge where UV.x reaches 1)"})

	# ---------------------------------------------------------------- H1: hsv function against the engine
	var funcs := Common.shader_text("06-hsv-strip.gdshader").split("void fragment()")[0]
	for pair: Array in [["hue x saturation", funcs + "void fragment() { COLOR = vec4(hsv_to_rgb(UV.x, UV.y, 1.0), 1.0); }\n", 0], ["hue x value", funcs + "void fragment() { COLOR = vec4(hsv_to_rgb(UV.x, 1.0, UV.y), 1.0); }\n", 1]]:
		var rr := ColorRect.new()
		rr.size = Vector2(256, 256)
		rr.material = Common.material_from_code(pair[1])
		root.add_child(rr)
		await frames(3)
		var img := main_img()
		var worst := 0.0
		var at := Vector2i.ZERO
		for y in 256:
			for x in 256:
				var h := (x + 0.5) / 256.0
				var t := (y + 0.5) / 256.0
				var expect: Color = Color.from_hsv(h, t, 1.0) if pair[2] == 0 else Color.from_hsv(h, 1.0, t)
				var d := Common.diff(expect, img.get_pixel(x, y))
				if d > worst:
					worst = d
					at = Vector2i(x, y)
		Common.out("H1-hsv-vs-engine-" + String(pair[0]).replace(" ", "-"), {"pixels_compared": 65536, "largest_channel_difference": snappedf(worst, 0.0001), "at_pixel": [at.x, at.y], "reading": "0.0039 is one 8-bit step: the film's function and the engine's Color.from_hsv agree to within half a step"})
		rr.queue_free()
		await frames(2)

	# ---------------------------------------------------------------- H1b: six exact hues
	var six: Dictionary = {}
	var names := ["red", "yellow", "green", "cyan", "blue", "magenta"]
	var want := [Color(1, 0, 0), Color(1, 1, 0), Color(0, 1, 0), Color(0, 1, 1), Color(0, 0, 1), Color(1, 0, 1)]
	for k in 6:
		var sw := ColorRect.new()
		sw.position = Vector2(20 + k * 30, 300)
		sw.size = Vector2(24, 24)
		var m := Common.material_from_file("06b-hsv-probe.gdshader")
		m.set_shader_parameter("hue", k / 6.0)
		sw.material = m
		root.add_child(sw)
	await frames(3)
	var img6 := main_img()
	var all_exact := true
	for k in 6:
		var c := img6.get_pixel(20 + k * 30 + 12, 312)
		six[names[k] + " (hue %d/6)" % k] = Common.rgb(c)
		if Common.diff(c, want[k]) > 0.002:
			all_exact = false
	Common.out("H1b-six-exact-hues", {"rgb_at_each_hue": six, "all_six_exact": all_exact, "reading": "red, yellow, green, cyan, blue and magenta at hue 0, 1/6, 2/6, 3/6, 4/6, 5/6 (saturation 1, value 1)"})
	clear_all()
	await frames(2)

	# ---------------------------------------------------------------- scene for H2, H3, H4
	var st := ColorRect.new()
	st.color = STAGE
	st.size = Vector2(1280, 720)
	root.add_child(st)
	var tprobe := ColorRect.new()
	tprobe.size = Vector2(12, 12)
	tprobe.material = Common.material_from_code(Common.TIME_PROBE_CODE)
	root.add_child(tprobe)
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
	disp.material = Common.material_from_file("05-stripes-moving.gdshader")
	root.add_child(disp)
	var count := 6.0
	var width := 0.5
	var speed := 0.12

	# ---------------------------------------------------------------- H2
	var h2: Dictionary = {}
	for rot: float in [0.0, 0.7854, 1.5708]:
		inner.rotation = rot
		await frames(4)
		var img := main_img()
		var T := Common.time_of(img)
		var pic := sub.get_texture().get_image()
		var checked := 0
		var mism := 0
		for py in range(130, 390, 4):
			for px in range(130, 390, 4):
				if pic.get_pixel(px, py).a < 0.99:
					continue
				var d := (px + 0.5) / 512.0 + (py + 0.5) / 512.0 - T * speed
				var s := saw_of(d, count)
				if absf(s - width) < 0.05 or s < 0.03 or s > 0.97:
					continue
				var on_got := Common.diff(img.get_pixel(384 + px, 104 + py), STAGE) > 0.03
				checked += 1
				if (s < width) != on_got:
					mism += 1
		h2[str(rot)] = {"TIME_read": snappedf(T, 0.001), "pixels_checked": checked, "mismatches": mism}
	Common.out("H2-stripes-live-in-picture-space", {"by_sprite_rotation_radians": h2, "reading": "0 mismatches at every rotation: the stripes are painted on the picture, so they do not turn with the sprite, and the formula with the TIME the shader saw predicts every probe"})

	# ---------------------------------------------------------------- H3: control, the same shader on the sprite itself (no viewport); a sprite texture with transparent-black padding, as a premultiplied blend needs
	disp.visible = false
	sub.render_target_update_mode = SubViewport.UPDATE_DISABLED
	var direct := Sprite2D.new()
	direct.texture = ImageTexture.create_from_image(CaptureScene.blob_image(448, false))
	direct.position = Vector2(640, 360)
	direct.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	direct.material = Common.material_from_file("05-stripes-moving.gdshader")
	root.add_child(direct)
	var tex_img := CaptureScene.blob_image(448, false)
	var h3: Dictionary = {}
	for rot: float in [0.0, 0.7854, 1.5708]:
		direct.rotation = rot
		await frames(4)
		var img := main_img()
		var T := Common.time_of(img)
		var m_pic := 0
		var m_own := 0
		var checked := 0
		for py in range(-80, 80, 4):
			for px in range(-80, 80, 4):
				var local := Vector2(px, py).rotated(-rot)
				var tx := int(224 + local.x)
				var ty := int(224 + local.y)
				if tx < 0 or ty < 0 or tx > 447 or ty > 447 or tex_img.get_pixel(tx, ty).a < 0.99:
					continue
				var s_own := saw_of((tx + 0.5) / 448.0 + (ty + 0.5) / 448.0 - T * speed, count)
				var s_fix := saw_of((px + 224 + 0.5) / 448.0 + (py + 224 + 0.5) / 448.0 - T * speed, count)
				if absf(s_own - width) < 0.06 or s_own < 0.04 or s_own > 0.96 or absf(s_fix - width) < 0.06 or s_fix < 0.04 or s_fix > 0.96:
					continue
				var on_got := Common.diff(img.get_pixel(640 + px, 360 + py), STAGE) > 0.03
				checked += 1
				if (s_own < width) != on_got: m_own += 1
				if (s_fix < width) != on_got: m_pic += 1
		h3[str(rot)] = {"pixels_checked": checked, "mismatches_against_the_sprites_own_UV": m_own, "mismatches_against_fixed_coordinates": m_pic}
	Common.out("H3-control-the-same-stripes-on-the-sprite-itself", {"by_sprite_rotation_radians": h3, "reading": "own-UV mismatches stay 0 at every rotation (the stripes turn WITH the sprite); fixed-coordinate mismatches appear as soon as it turns (at rotation 0 the two agree)"})
	direct.queue_free()

	# ---------------------------------------------------------------- H4: rainbow stripes
	disp.visible = true
	sub.render_target_update_mode = SubViewport.UPDATE_WHEN_VISIBLE
	inner.rotation = 0.0
	disp.material = Common.material_from_file("07-rainbow-stripes.gdshader")
	await frames(5)
	var img4 := main_img()
	var T4 := Common.time_of(img4)
	var pic4 := sub.get_texture().get_image()
	var worst4 := 0.0
	var n4 := 0
	var gaps := 0
	var gaps_ok := 0
	for py in range(130, 390, 3):
		for px in range(130, 390, 3):
			var pc := pic4.get_pixel(px, py)
			if pc.a < 0.99:
				continue
			var d := (px + 0.5) / 512.0 + (py + 0.5) / 512.0 - T4 * speed
			var s := saw_of(d, count)
			var got := img4.get_pixel(384 + px, 104 + py)
			if s < width - 0.06 and s > 0.04:
				var expect := Color.from_hsv(d - floorf(d), 1.0, 1.0)
				var dd := Common.diff(expect, got)
				n4 += 1
				worst4 = maxf(worst4, dd)
			elif s > width + 0.06 and s < 0.96:
				gaps += 1
				if Common.diff(Color(pc.r + STAGE.r * (1.0 - pc.a), pc.g + STAGE.g * (1.0 - pc.a), pc.b + STAGE.b * (1.0 - pc.a)), got) < 0.008:
					gaps_ok += 1
	Common.out("H4-rainbow-stripes", {"TIME_read": snappedf(T4, 0.001), "stripe_pixels_compared": n4, "largest_channel_difference_to_hsv_of_the_diagonal": snappedf(worst4, 0.0001), "gap_pixels_compared": gaps, "gap_pixels_equal_to_the_picture": gaps_ok, "reading": "inside a stripe the colour is hsv(fract(diagonal), 1, 1); in the gaps the picture (the inner gradient) shows through unchanged"})
	quit(0)
