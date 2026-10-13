extends SceneTree
# Time and Waves, planning check 3: curves, the breathing logo and the wind tween.
#   A  CurveTexture lookup: texture(curve, vec2(t, 0.0)).r against Curve.sample_baked(t) (all 256 pixels, plus probes)
#   B  texture_mode RGB and RED both give the curve in .r
#   C  a curve that goes above 1: is it stored?
#   D  05-curve-loop with the real TIME against the curve value for fract(TIME * 0.5)
#   E  a curve fed from a sine plays forward then backward; fed from fract it plays one way (sequences over one cycle)
#   F  12-breath with the real CurveTexture and the real TIME: blob width against 76.8 px * (1 + 0.25 k)
#   G  13-banner: wind 1 tweened to 0 (set first), and the tween on a uniform never set (expected to fail)
# Run: godot --path <scratch> --always-on-top --script res://verify3.gd -- --film <abs film dir>
const ENCODER := "shader_type canvas_item;\nvoid fragment() {\n\tfloat whole = floor(TIME);\n\tfloat part = (TIME - whole) * 255.0;\n\tfloat p1 = floor(part);\n\tCOLOR = vec4(whole / 255.0, p1 / 255.0, part - p1, 1.0);\n}\n"
const TAU_F := 6.283185307179586
const TEAL := Vector3(0.37, 0.64, 0.57)
const CREAM := Vector3(0.98, 0.97, 0.96)

var film := ""
var enc: ColorRect

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func shader_text(name: String) -> String:
	return FileAccess.get_file_as_string(film + "/lab-shaders/" + name)

func make_rect(code: String, pos: Vector2, size: Vector2) -> ColorRect:
	var rect := ColorRect.new()
	rect.position = pos
	rect.size = size
	var sh := Shader.new()
	sh.code = code
	var mat := ShaderMaterial.new()
	mat.shader = sh
	rect.material = mat
	return rect

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func decode_time(img: Image) -> float:
	var c := img.get_pixel(int(enc.position.x + 10), int(enc.position.y + 10))
	return roundf(c.r * 255.0) + (roundf(c.g * 255.0) + c.b) / 255.0

func mixv(a: Vector3, b: Vector3, t: float) -> Vector3:
	return a * (1.0 - t) + b * t

func steps(c: Color, v: Vector3) -> float:
	return maxf(maxf(absf(c.r - v.x), absf(c.g - v.y)), absf(c.b - v.z)) * 255.0

func breath_curve() -> Curve:
	# a slow rise, a short hold, a long fall: flat tangents at every point give smooth ease-in and ease-out
	var c := Curve.new()
	c.add_point(Vector2(0.0, 0.0))
	c.add_point(Vector2(0.40, 1.0))
	c.add_point(Vector2(0.55, 1.0))
	c.add_point(Vector2(1.0, 0.0))
	return c

func curve_texture(c: Curve, mode: int = CurveTexture.TEXTURE_MODE_RGB) -> CurveTexture:
	var ct := CurveTexture.new()
	ct.curve = c
	ct.texture_mode = mode
	return ct

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--film": film = a[i + 1]
	root.size = Vector2i(640, 360)
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	enc = make_rect(ENCODER, Vector2(0, 0), Vector2(20, 20))
	root.add_child(enc)
	var curve := breath_curve()
	var ct := curve_texture(curve)
	out("env", {"curve_points": curve.point_count, "texture_width_default": ct.width, "texture_mode_default": ct.texture_mode, "bake_resolution_default": curve.bake_resolution,
		"y_at_0.2": snappedf(curve.sample_baked(0.2), 0.0001), "y_at_0.47": snappedf(curve.sample_baked(0.47), 0.0001), "y_at_0.75": snappedf(curve.sample_baked(0.75), 0.0001)})

	# ---- A: the lookup, across all 256 pixels
	var lookup := make_rect("shader_type canvas_item;\nuniform sampler2D curve;\nvoid fragment() {\n\tfloat k = texture(curve, vec2(UV.x, 0.0)).r;\n\tCOLOR = vec4(vec3(k), 1.0);\n}\n", Vector2(0, 40), Vector2(256, 20))
	(lookup.material as ShaderMaterial).set_shader_parameter("curve", ct)
	root.add_child(lookup)
	await frames(3)
	var img := grab()
	var maxA := 0.0
	for x in range(256):
		var u := (x + 0.5) / 256.0
		var want := curve.sample_baked(u)
		maxA = maxf(maxA, absf(img.get_pixel(x, 50).r - want) * 255.0)
	# probes with a uniform t on a 1-pixel-wide read
	var probe := make_rect("shader_type canvas_item;\nuniform sampler2D curve;\nuniform float t = 0.0;\nvoid fragment() {\n\tfloat k = texture(curve, vec2(t, 0.0)).r;\n\tCOLOR = vec4(vec3(k), 1.0);\n}\n", Vector2(300, 40), Vector2(20, 20))
	(probe.material as ShaderMaterial).set_shader_parameter("curve", ct)
	root.add_child(probe)
	var probes: Array = []
	var max_probe := 0.0
	for t in [0.0, 0.1, 0.25, 0.4, 0.47, 0.55, 0.75, 0.9, 1.0]:
		(probe.material as ShaderMaterial).set_shader_parameter("t", t)
		await frames(2)
		var g := grab().get_pixel(310, 50).r
		var want2 := curve.sample(t)
		probes.append([t, snappedf(g, 0.0001), snappedf(want2, 0.0001)])
		max_probe = maxf(max_probe, absf(g - want2) * 255.0)
	out("A-curve-lookup", {"max_error_8bit_steps_all_256_pixels": snappedf(maxA, 0.01), "probes_t_texture_curve": probes, "max_probe_error_8bit_steps": snappedf(max_probe, 0.01),
		"reading": "texture(curve, vec2(t, 0.0)).r returns the curve's value at t (to about one 8-bit step; the strip is 256 pixels wide)"})

	# ---- B: RED mode
	var ct_red := curve_texture(curve, CurveTexture.TEXTURE_MODE_RED)
	(probe.material as ShaderMaterial).set_shader_parameter("curve", ct_red)
	(probe.material as ShaderMaterial).set_shader_parameter("t", 0.47)
	await frames(3)
	var red_val := grab().get_pixel(310, 50).r
	out("B-red-mode", {"value_at_0.47_RED_mode": snappedf(red_val, 0.0001), "curve_value": snappedf(curve.sample(0.47), 0.0001), "reading": ".r works in RED mode as well"})
	(probe.material as ShaderMaterial).set_shader_parameter("curve", ct)

	# ---- C: above 1
	var big := Curve.new()
	big.max_value = 2.0
	big.add_point(Vector2(0.0, 0.0))
	big.add_point(Vector2(0.5, 2.0))
	big.add_point(Vector2(1.0, 0.0))
	var half := make_rect("shader_type canvas_item;\nuniform sampler2D curve;\nuniform float t = 0.5;\nvoid fragment() {\n\tCOLOR = vec4(vec3(texture(curve, vec2(t, 0.0)).r * 0.5), 1.0);\n}\n", Vector2(340, 40), Vector2(20, 20))
	(half.material as ShaderMaterial).set_shader_parameter("curve", curve_texture(big))
	root.add_child(half)
	await frames(3)
	var gh := grab().get_pixel(350, 50).r
	out("C-curve-above-one", {"curve_max_value": big.max_value, "curve_value_at_0.5": big.sample(0.5), "texture_r_times_half_read_back": snappedf(gh, 0.0001),
		"reading": "if the strip stores 2.0 the read-back is 1.0; if it clamps at 1.0 the read-back is 0.5"})
	half.queue_free()

	# ---- D: 05-curve-loop with the real TIME
	var loop := make_rect(shader_text("05-curve-loop.gdshader"), Vector2(40, 100), Vector2(60, 60))
	(loop.material as ShaderMaterial).set_shader_parameter("curve", ct)
	root.add_child(loop)
	# ---- E: sine-fed and saw-fed
	var fed_sine := make_rect("shader_type canvas_item;\nuniform sampler2D curve;\nvoid fragment() {\n\tfloat v = 0.5 - 0.5 * cos(TAU * TIME * 0.5);\n\tfloat k = texture(curve, vec2(v, 0.0)).r;\n\tCOLOR = vec4(vec3(k), 1.0);\n}\n", Vector2(120, 100), Vector2(60, 60))
	(fed_sine.material as ShaderMaterial).set_shader_parameter("curve", ct)
	root.add_child(fed_sine)
	var fed_saw := make_rect("shader_type canvas_item;\nuniform sampler2D curve;\nvoid fragment() {\n\tfloat v = fract(TIME * 0.5);\n\tfloat k = texture(curve, vec2(v, 0.0)).r;\n\tCOLOR = vec4(vec3(k), 1.0);\n}\n", Vector2(200, 100), Vector2(60, 60))
	(fed_saw.material as ShaderMaterial).set_shader_parameter("curve", ct)
	root.add_child(fed_saw)
	await frames(3)
	var maxD := 0.0
	var maxE1 := 0.0
	var maxE2 := 0.0
	var seq_sine: Array = []
	var seq_saw: Array = []
	var t_first := -1.0
	for f in range(240):
		await process_frame
		var im := grab()
		var t := decode_time(im)
		if t_first < 0.0: t_first = t
		var c := fmod(t * 0.5, 1.0)
		var kD := curve.sample_baked(c)
		maxD = maxf(maxD, steps(im.get_pixel(70, 130), mixv(TEAL, CREAM, kD)))
		var vs := 0.5 - 0.5 * cos(TAU_F * t * 0.5)
		maxE1 = maxf(maxE1, absf(im.get_pixel(150, 130).r - curve.sample_baked(vs)) * 255.0)
		maxE2 = maxf(maxE2, absf(im.get_pixel(230, 130).r - curve.sample_baked(c)) * 255.0)
	out("D-curve-loop-real-time", {"frames": 240, "max_error_8bit_steps": snappedf(maxD, 0.01), "reading": "05-curve-loop pixel against mix(teal, cream, curve(fract(TIME * 0.5))); curve = rise, hold, fall"})
	out("E-fed-by-sine-or-ramp-pixels", {"frames": 240, "sine_fed_max_error_steps": snappedf(maxE1, 0.01), "saw_fed_max_error_steps": snappedf(maxE2, 0.01)})
	# the sequences over one cycle, from the curve itself (what the pixels were checked against)
	for i in range(0, 21):
		var c2 := i / 20.0
		var vs2 := 0.5 - 0.5 * cos(TAU_F * c2)
		seq_sine.append(snappedf(curve.sample_baked(vs2), 0.001))
		seq_saw.append(snappedf(curve.sample_baked(c2), 0.001))
	var pal_sine := true
	var pal_saw := true
	for i in range(0, 21):
		if absf(float(seq_sine[i]) - float(seq_sine[20 - i])) > 0.01: pal_sine = false
		if absf(float(seq_saw[i]) - float(seq_saw[20 - i])) > 0.01: pal_saw = false
	out("E-palindrome", {"sine_fed_sequence_over_one_cycle": seq_sine, "ramp_fed_sequence_over_one_cycle": seq_saw, "sine_fed_is_palindromic": pal_sine, "ramp_fed_is_palindromic": pal_saw,
		"reading": "a sine-fed curve plays forward then backward (the sequence reads the same both ways); a ramp-fed curve plays one way"})
	loop.queue_free(); fed_sine.queue_free(); fed_saw.queue_free(); lookup.queue_free(); probe.queue_free()
	await frames(2)

	# ---- F: 12-breath with the real curve and the real TIME
	var tex_img := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	tex_img.fill(Color(0, 0, 0, 0))
	var cen := Vector2(64, 64)
	for y in range(128):
		for x in range(128):
			var d := Vector2(x, y).distance_to(cen)
			if d < 128 * 0.30:
				tex_img.set_pixel(x, y, Color("#5FA391"))
			var e1 := Vector2(x, y).distance_to(cen + Vector2(-12.8, -7.68))
			var e2 := Vector2(x, y).distance_to(cen + Vector2(12.8, -7.68))
			if e1 < 4.48 or e2 < 4.48:
				tex_img.set_pixel(x, y, Color("#FAF9F5"))
	var spr := Sprite2D.new()
	spr.texture = ImageTexture.create_from_image(tex_img)
	spr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	spr.position = Vector2(400, 200)
	var sh10 := Shader.new()
	sh10.code = shader_text("12-breath.gdshader")
	var m10 := ShaderMaterial.new()
	m10.shader = sh10
	m10.set_shader_parameter("curve", ct)
	spr.material = m10
	root.add_child(spr)
	await frames(3)
	var maxF := 0.0
	var widths: Array = []
	for f in range(300):
		await process_frame
		var im2 := grab()
		var t2 := decode_time(im2)
		var k := curve.sample_baked(fmod(t2 * 0.4, 1.0))
		var want_w := 76.8 * (1.0 + 0.25 * k)
		var xs0 := 9999
		var xs1 := -1
		for x in range(300, 500):
			var p := im2.get_pixel(x, 200)
			if absf(p.r - 0.373) < 0.03 and absf(p.g - 0.639) < 0.03 and absf(p.b - 0.569) < 0.03:
				xs0 = mini(xs0, x)
				xs1 = maxi(xs1, x)
		var w := float(xs1 - xs0 + 1)
		maxF = maxf(maxF, absf(w - want_w))
		if f % 60 == 0: widths.append([snappedf(k, 0.01), w, snappedf(want_w, 0.1)])
	out("F-breath", {"frames": 300, "max_width_error_px": snappedf(maxF, 0.1), "samples_k_measured_expected_px": widths, "reading": "the logo's width follows 76.8 px * (1 + 0.25 k) with k from the real CurveTexture"})
	spr.queue_free()
	await frames(2)

	# ---- G: banner, wind, and the tween
	var ban_img := Image.create(256, 128, false, Image.FORMAT_RGBA8)
	ban_img.fill(Color(0, 0, 0, 0))
	for y in range(16, 112):
		var stripe := ((y - 16) / 24) % 2 == 0
		for x in range(256):
			ban_img.set_pixel(x, y, Color("#5FA391") if stripe else Color("#FAF9F5"))
	var ban_tex := ImageTexture.create_from_image(ban_img)
	var ban_shader := Shader.new()
	ban_shader.code = shader_text("13-banner.gdshader")
	var make_banner := func(pos: Vector2) -> Sprite2D:
		var s := Sprite2D.new()
		s.texture = ban_tex
		s.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		s.centered = false
		s.position = pos
		var m := ShaderMaterial.new()
		m.shader = ban_shader
		s.material = m
		return s
	var live: Sprite2D = make_banner.call(Vector2(20, 120))
	var ref: Sprite2D = make_banner.call(Vector2(300, 120))    # always wind 0, the flat reference
	root.add_child(live)
	root.add_child(ref)
	await frames(3)
	var diff_fn := func() -> float:
		var im3 := grab()
		var total := 0.0
		for y in range(0, 128, 2):
			for x in range(0, 256, 2):
				var p1 := im3.get_pixel(20 + x, 120 + y)
				var p2 := im3.get_pixel(300 + x, 120 + y)
				total += absf(p1.r - p2.r) + absf(p1.g - p2.g) + absf(p1.b - p2.b)
		return total
	var d_default: float = diff_fn.call()
	var uniform_before = (live.material as ShaderMaterial).get_shader_parameter("wind")
	# a tween on a uniform never set from code (expected to fail, as the pilot found for another uniform)
	var tween_fail := create_tween()
	tween_fail.tween_property(live.material, "shader_parameter/wind", 0.0, 0.5)
	await frames(3)
	(live.material as ShaderMaterial).set_shader_parameter("wind", 1.0)
	await frames(2)
	var d_one: float = diff_fn.call()
	var tw := create_tween()
	tw.tween_property(live.material, "shader_parameter/wind", 0.0, 1.0)
	var series: Array = []
	for i in range(5):
		await create_timer(0.25).timeout
		series.append(snappedf(diff_fn.call(), 0.1))
	await frames(3)
	var d_end: float = diff_fn.call()
	out("G-wind-tween", {"wind_before_any_set": str(uniform_before), "difference_from_flat_at_default_wind_0": snappedf(d_default, 0.01), "difference_just_after_set_wind_1": snappedf(d_one, 0.1),
		"difference_every_quarter_second_while_tweening_1_to_0": series, "difference_after_tween": snappedf(d_end, 0.01),
		"reading": "the banner is flat at the default, moves when wind is set to 1, and settles to flat as the tween reaches 0 (the tween on a never-set uniform printed an error, kept in the log)"})
	quit(0)
