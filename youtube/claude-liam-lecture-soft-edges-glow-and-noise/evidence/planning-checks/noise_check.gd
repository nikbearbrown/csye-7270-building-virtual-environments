extends SceneTree
# noise_check.gd: the noise claims of the film, checked with REAL NoiseTexture2D resources in a real Godot 4.7.2 window.
# The Lab (lab/runner.gd) can only bind a plain, NON-seamless image to a sampler2D (--tex noise=noise), so the seamless switch, the scroll and the
# wrap-around need this scratch route. Prints one RESULT line per check.
#
#   godot --path <scratch project> --script res://noise_check.gd -- --film <abs path of the film folder> [--png-dir <abs dir>]
#
# Checks (ids):
#   T  texture seam metrics: NoiseTexture2D, FastNoiseLite defaults, 512 x 512, seamless false vs true: how different is the last column from the
#      first (the wrap), against how different neighbouring columns normally are; contrast (standard deviation) of each.
#   C  clamp vs repeat: a raw greyscale shader reads texture(noise, UV + vec2(0.5, 0.0)): the right half looks up past 1.0. With the default (no hint)
#      the lookup returns the edge column (rows are constant along x); with repeat_enable it wraps (rows keep changing).
#   S  seam in the render: the film's scroll shader with repeat_enable, seamless false vs true, offset 0.5: where does the biggest column jump sit?
#   D  scroll direction: offset 0 vs 0.125 with the same texture; the best circular shift of the picture.
#   R  noise reveal coverage: the film's reveal shader at progress 0.25 / 0.5 / 0.75: fraction of the disc interior that is shown.
#   Z  the scroll shader's sampling (raw greyscale, the same UV + vec2(TIME * 0.1, 0.0)) rendered twice about 3 s apart, with the shader's own TIME read
#      back through a small decoder rectangle in the same frame: the seam sits at 1 - 0.1 * TIME (mod 1) and moves LEFT.
#   Y  the shader TIME against the engine's tick counter (is TIME the plain seconds the narration says it is?).

var FILM := ""
var PNGDIR := ""

func _initialize() -> void:
	call_deferred("run")

func parse() -> void:
	var a := OS.get_cmdline_user_args()
	var i := 0
	while i < a.size():
		if a[i] == "--film": FILM = a[i + 1]; i += 2
		elif a[i] == "--png-dir": PNGDIR = a[i + 1]; i += 2
		else: i += 1

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func make_noise(seamless: bool) -> NoiseTexture2D:
	var t := NoiseTexture2D.new()
	t.noise = FastNoiseLite.new()          # defaults: simplex smooth, frequency 0.01, fractal fbm
	t.seamless = seamless                  # width and height stay at the 512 default
	return t

func texture_metrics(img: Image) -> Dictionary:
	var w := img.get_width()
	var h := img.get_height()
	var typ_x := 0.0
	var n_x := 0
	for y in range(0, h, 4):
		for x in range(0, w - 1, 2):
			typ_x += absf(img.get_pixel(x + 1, y).r - img.get_pixel(x, y).r)
			n_x += 1
	var typ_y := 0.0
	var n_y := 0
	for x in range(0, w, 4):
		for y in range(0, h - 1, 2):
			typ_y += absf(img.get_pixel(x, y + 1).r - img.get_pixel(x, y).r)
			n_y += 1
	var wrap_x := 0.0
	for y in range(h):
		wrap_x += absf(img.get_pixel(0, y).r - img.get_pixel(w - 1, y).r)
	wrap_x /= h
	var wrap_y := 0.0
	for x in range(w):
		wrap_y += absf(img.get_pixel(x, 0).r - img.get_pixel(x, h - 1).r)
	wrap_y /= w
	var sum := 0.0
	var sum2 := 0.0
	var n := 0
	var lo := 1.0
	var hi := 0.0
	for y in range(0, h, 2):
		for x in range(0, w, 2):
			var v := img.get_pixel(x, y).r
			sum += v
			sum2 += v * v
			n += 1
			lo = minf(lo, v)
			hi = maxf(hi, v)
	var mean := sum / n
	var sd := sqrt(maxf(sum2 / n - mean * mean, 0.0))
	var hist: Array = []
	for b in range(20):
		hist.append(0)
	for y in range(0, h, 2):
		for x in range(0, w, 2):
			hist[mini(int(img.get_pixel(x, y).r * 20.0), 19)] += 1
	for b in range(20):
		hist[b] = snappedf(float(hist[b]) / n, 0.0001)
	typ_x /= n_x
	typ_y /= n_y
	# far apart: random pairs of pixels more than 200 px apart (fixed seed)
	var rng := RandomNumberGenerator.new()
	rng.seed = 1
	var far_sum := 0.0
	var far_n := 0
	while far_n < 20000:
		var p := Vector2i(rng.randi_range(0, w - 1), rng.randi_range(0, h - 1))
		var q := Vector2i(rng.randi_range(0, w - 1), rng.randi_range(0, h - 1))
		if Vector2(p - q).length() > 200.0:
			far_sum += absf(img.get_pixel(p.x, p.y).r - img.get_pixel(q.x, q.y).r)
			far_n += 1
	return {"size": [w, h], "neighbour_diff_x": snappedf(typ_x, 0.0001), "wrap_diff_x": snappedf(wrap_x, 0.0001), "wrap_over_neighbour_x": snappedf(wrap_x / typ_x, 0.01),
		"neighbour_diff_y": snappedf(typ_y, 0.0001), "wrap_diff_y": snappedf(wrap_y, 0.0001), "wrap_over_neighbour_y": snappedf(wrap_y / typ_y, 0.01),
		"far_pair_diff": snappedf(far_sum / far_n, 0.0001), "histogram_20_bins_of_0.05": hist, "mean": snappedf(mean, 0.0001), "std_dev": snappedf(sd, 0.0001), "min": snappedf(lo, 0.0001), "max": snappedf(hi, 0.0001)}

func make_rect(code: String, tex: Texture2D, extra: Dictionary = {}) -> ColorRect:
	var sh := Shader.new()
	sh.code = code
	var mat := ShaderMaterial.new()
	mat.shader = sh
	mat.set_shader_parameter("noise", tex)
	for k in extra:
		mat.set_shader_parameter(k, extra[k])
	var r := ColorRect.new()
	r.size = Vector2(256, 256)
	r.position = Vector2(192, 52)
	r.material = mat
	return r

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func crop_rect(img: Image) -> Image:
	return img.get_region(Rect2i(192, 52, 256, 256))

# mean over rows of |p(x+1) - p(x)|, per column x (rows 70..186 of the 256 square: inside the disc, away from the soft edge)
func column_jumps(sq: Image, r0: int = 70, r1: int = 186) -> Array:
	var jumps: Array = []
	for x in range(255):
		var s := 0.0
		for y in range(r0, r1):
			s += absf(sq.get_pixel(x + 1, y).r - sq.get_pixel(x, y).r)
		jumps.append(s / (r1 - r0))
	return jumps

func argmax(a: Array) -> int:
	var best := 0
	for i in range(a.size()):
		if a[i] > a[best]:
			best = i
	return best

func median(a: Array) -> float:
	var b := a.duplicate()
	b.sort()
	return b[b.size() / 2]

func rowstd_in_range(sq: Image, x0: int, x1: int) -> float:
	# mean over rows of the standard deviation along x within [x0, x1)
	var total := 0.0
	for y in range(256):
		var s := 0.0
		var s2 := 0.0
		for x in range(x0, x1):
			var v := sq.get_pixel(x, y).r
			s += v
			s2 += v * v
		var n := float(x1 - x0)
		var m := s / n
		total += sqrt(maxf(s2 / n - m * m, 0.0))
	return total / 256.0

func best_shift(a: Image, b: Image) -> Dictionary:
	# circular shift s (in px, to the RIGHT is positive) that makes row-averaged b best match a shifted by s
	var best_s := 0
	var best_err := 1e9
	for s in range(-60, 61):
		var err := 0.0
		for y in range(0, 256, 8):
			for x in range(0, 256, 2):
				var xs := ((x - s) % 256 + 256) % 256
				err += absf(b.get_pixel(x, y).r - a.get_pixel(xs, y).r)
		if err < best_err:
			best_err = err
			best_s = s
	return {"shift_px": best_s, "err": snappedf(best_err, 0.01)}

func make_decoder(expr: String, pos: Vector2) -> ColorRect:
	var shd := Shader.new()
	shd.code = "shader_type canvas_item;\nvoid fragment() { COLOR = vec4(" + expr + ", 0.0, 0.0, 1.0); }\n"
	var mt := ShaderMaterial.new()
	mt.shader = shd
	var r := ColorRect.new()
	r.size = Vector2(16, 16)
	r.position = pos
	r.material = mt
	return r

# shader TIME from the two decoder rectangles: R of the first is TIME / 16 (mod 1), R of the second TIME / 256 (mod 1): TIME = 16 * block + 16 * r
func read_time(img: Image) -> float:
	var r1: float = img.get_pixel(508, 18).r
	var r2: float = img.get_pixel(528, 18).r
	var block := roundf(r2 * 16.0 - r1)
	return 16.0 * block + 16.0 * r1

func run() -> void:
	parse()
	DisplayServer.window_move_to_foreground()   # a covered window is not drawn, and TIME then stands still
	RenderingServer.set_default_clear_color(Color("#D9D5CA"))
	root.size = Vector2i(640, 360)
	var shaders := FILM + "/lab-shaders/"
	var scroll_code := FileAccess.get_file_as_string(shaders + "11-noise-scroll.gdshader")
	var reveal_code := FileAccess.get_file_as_string(shaders + "13-noise-reveal.gdshader")
	var raw_repeat := "shader_type canvas_item;\nuniform sampler2D noise : repeat_enable;\nuniform float offset = 0.5;\nvoid fragment() { float n = texture(noise, UV + vec2(offset, 0.0)).r; COLOR = vec4(n, n, n, 1.0); }\n"
	var raw_default := "shader_type canvas_item;\nuniform sampler2D noise;\nuniform float offset = 0.5;\nvoid fragment() { float n = texture(noise, UV + vec2(offset, 0.0)).r; COLOR = vec4(n, n, n, 1.0); }\n"
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()})

	# ---- T: the textures themselves
	var tex_plain := make_noise(false)
	await tex_plain.changed
	var tex_seam := make_noise(true)
	await tex_seam.changed
	out("T-plain", texture_metrics(tex_plain.get_image()))
	out("T-seamless", texture_metrics(tex_seam.get_image()))

	# ---- C: clamp (default) vs repeat_enable, raw greyscale, lookups from UV.x + 0.5 (the right half is past 1.0)
	for pair in [["default-no-hint", raw_default], ["repeat_enable", raw_repeat]]:
		var r := make_rect(pair[1], tex_seam, {"offset": 0.5})
		root.add_child(r)
		await frames(6)
		var sq := crop_rect(grab())
		out("C-" + pair[0], {"row_std_left_half_x0_to_120": snappedf(rowstd_in_range(sq, 4, 120), 0.0001), "row_std_right_half_x136_to_252": snappedf(rowstd_in_range(sq, 136, 252), 0.0001),
			"reading": "right half looks up past 1.0. std 0 along every row = the edge column repeated; std > 0 = the texture wrapped round"})
		if PNGDIR != "":
			sq.save_png(PNGDIR + "/noise-C-" + pair[0] + ".png")
		r.queue_free()
		await frames(2)

	# ---- S: the seam in the render (raw greyscale, offset 0.5: the wrap boundary sits at UV.x = 0.5, pixel column 128)
	for pair in [["plain", tex_plain], ["seamless", tex_seam]]:
		var r2 := make_rect(raw_repeat, pair[1], {"offset": 0.5})
		root.add_child(r2)
		await frames(6)
		var sq2 := crop_rect(grab())
		var jumps := column_jumps(sq2)
		var am := argmax(jumps)
		var med := median(jumps)
		out("S-" + pair[0], {"largest_column_jump_at_px": am, "largest_jump": snappedf(jumps[am], 0.0001), "median_jump": snappedf(med, 0.0001), "ratio": snappedf(jumps[am] / med, 0.1),
			"expected_seam_px": 127, "reading": "the wrap boundary is at pixel column 127/128. A ratio near 1 = no outlier = no visible seam"})
		if PNGDIR != "":
			sq2.save_png(PNGDIR + "/noise-S-" + pair[0] + ".png")
		r2.queue_free()
		await frames(2)

	# ---- D: scroll direction. Same texture, offset 0 then 0.125: the picture moves by -32 px (to the LEFT) if adding to UV moves the picture left.
	var rd := make_rect(raw_repeat, tex_seam, {"offset": 0.0})
	root.add_child(rd)
	await frames(6)
	var img0 := crop_rect(grab())
	rd.material.set_shader_parameter("offset", 0.125)
	await frames(6)
	var img1 := crop_rect(grab())
	var bs := best_shift(img0, img1)
	out("D-direction", {"offset_added_to_UV_x": 0.125, "best_shift_of_picture_px": bs["shift_px"], "err": bs["err"],
		"reading": "negative = the picture moved LEFT. -32 px would be exactly 0.125 of the 256 px width"})
	rd.queue_free()
	await frames(2)

	# ---- R: the reveal shader (the film's file), coverage of the disc interior
	for p in [0.25, 0.5, 0.75]:
		var rr := make_rect(reveal_code, tex_seam, {"progress": p})
		root.add_child(rr)
		await frames(6)
		var sq3 := crop_rect(grab())
		var shown := 0
		var total := 0
		for y in range(256):
			for x in range(256):
				var dx := (x + 0.5) / 256.0 - 0.5
				var dy := (y + 0.5) / 256.0 - 0.5
				if sqrt(dx * dx + dy * dy) < 0.2:
					total += 1
					if sq3.get_pixel(x, y).r < 0.6:   # teal red is 0.37, stage red is 0.85: below 0.6 = shown
						shown += 1
		out("R-reveal-" + str(p), {"progress": p, "fraction_of_disc_interior_shown": snappedf(float(shown) / total, 0.001)})
		if PNGDIR != "":
			sq3.save_png(PNGDIR + "/noise-R-" + str(p) + ".png")
		rr.queue_free()
		await frames(2)

	# ---- R-curve: the whole coverage curve of the reveal (the film's shader, seamless texture), progress 0.05 to 0.95
	var curve: Array = []
	var rc := make_rect(reveal_code, tex_seam, {"progress": 0.05})
	root.add_child(rc)
	for k in range(1, 20):
		var pv := k * 0.05
		rc.material.set_shader_parameter("progress", pv)
		await frames(4)
		var sqc := crop_rect(grab())
		var shown_c := 0
		var total_c := 0
		for y in range(256):
			for x in range(256):
				var dx2 := (x + 0.5) / 256.0 - 0.5
				var dy2 := (y + 0.5) / 256.0 - 0.5
				if sqrt(dx2 * dx2 + dy2 * dy2) < 0.2:
					total_c += 1
					if sqc.get_pixel(x, y).r < 0.6:
						shown_c += 1
		curve.append([snappedf(pv, 0.01), snappedf(float(shown_c) / total_c, 0.001)])
	out("R-curve", {"progress_and_fraction_shown": curve})
	rc.queue_free()
	await frames(2)

	# ---- F, Z, Y: the film's TIME shaders. The shader clock is global and only moves forward, and Godot skips drawing when its window is fully
	# covered by another window (TIME then stands still: run-noise-15-14-FROZEN-TIME-inconclusive.log). So these checks step the clock EXPLICITLY with
	# force_draw(false, seconds), one frame with that step, which is how the engine advances TIME on a normal draw, and read the shader's own TIME back
	# from the same frame through two small decoder rectangles (TIME / 16 and TIME / 256, one colour channel each; resolution about 0.06 s).
	var raw_time := "shader_type canvas_item;\nuniform sampler2D noise : repeat_enable;\nvoid fragment() { float n = texture(noise, UV + vec2(TIME * 0.1, 0.0)).r; COLOR = vec4(n, n, n, 1.0); }\n"
	var film_scroll := FileAccess.get_file_as_string(shaders + "11-noise-scroll.gdshader")
	var film_norepeat := FileAccess.get_file_as_string(shaders + "12-noise-no-repeat.gdshader")
	var dec_a := make_decoder("fract(TIME / 16.0)", Vector2(500, 10))
	var dec_b := make_decoder("fract(TIME / 256.0)", Vector2(520, 10))
	root.add_child(dec_a)
	root.add_child(dec_b)
	await frames(3)
	# F1: the film's no-hint shader (clamped lookups) at TIME about 4.5 s and 9.5 s: half the disc, then all of it, is streaks. Seamless texture.
	var rf1 := make_rect(film_norepeat, tex_seam)
	root.add_child(rf1)
	await frames(2)
	for target in [4.5, 9.5]:
		var cur := read_time(grab())
		RenderingServer.force_draw(false, maxf(target - cur, 0.01))
		var imgf := grab()
		var tf := read_time(imgf)
		var nm1: String = "noise-F-norepeat-seamless-t" + str(snappedf(tf, 0.1)) + ".png"
		if PNGDIR != "":
			crop_rect(imgf).save_png(PNGDIR + "/" + nm1)
		out("F-norepeat-seamless", {"shader_TIME_s": snappedf(tf, 0.01), "png": nm1})
	rf1.queue_free()
	await frames(2)
	# F2: the film's scroll shader at TIME about 4.5 s modulo 10 (the picture repeats every 10 s): the plain texture shows its seam, the seamless one does not.
	for spec in [["scroll-plain", tex_plain], ["scroll-seamless", tex_seam]]:
		var rf2 := make_rect(film_scroll, spec[1])
		root.add_child(rf2)
		await frames(2)
		var cur2 := read_time(grab())
		var next_t := cur2 + 0.5
		next_t = next_t + fposmod(4.5 - next_t, 10.0)
		RenderingServer.force_draw(false, next_t - cur2)
		var imgf2 := grab()
		var tf2 := read_time(imgf2)
		var nm2: String = "noise-F-" + str(spec[0]) + "-t" + str(snappedf(tf2, 0.1)) + ".png"
		if PNGDIR != "":
			crop_rect(imgf2).save_png(PNGDIR + "/" + nm2)
		out("F-" + str(spec[0]), {"shader_TIME_s": snappedf(tf2, 0.01), "png": nm2})
		rf2.queue_free()
		await frames(2)
	# Z: raw greyscale sampling, the same UV + vec2(TIME * 0.1, 0.0); the seam against the decoded TIME. Plain texture 3 reads, seamless texture 2.
	for pair in [["plain", tex_plain, 3], ["seamless", tex_seam, 2]]:
		var rz := make_rect(raw_time, pair[1])
		root.add_child(rz)
		await frames(3)
		var reads: Array = []
		for k in range(int(pair[2])):
			if k > 0:
				RenderingServer.force_draw(false, 3.0)     # TIME += 3.0
			var full := grab()
			var t_shader := read_time(full)
			var sq4 := full.get_region(Rect2i(192, 52, 256, 256))
			var jumps4 := column_jumps(sq4, 20, 236)
			var am4 := argmax(jumps4)
			reads.append({"step": k, "shader_TIME_s": snappedf(t_shader, 0.01), "seam_px": am4, "seam_ratio": snappedf(jumps4[am4] / median(jumps4), 0.1),
				"expected_seam_px_from_shader_TIME": int(round((1.0 - fposmod(0.1 * t_shader, 1.0)) * 256.0)) % 256})
			if PNGDIR != "":
				sq4.save_png(PNGDIR + "/noise-Z-" + str(pair[0]) + "-" + str(k) + ".png")
		var adv: Array = []
		for k in range(1, reads.size()):
			adv.append(snappedf(float(reads[k]["shader_TIME_s"]) - float(reads[k - 1]["shader_TIME_s"]), 0.01))
		out("Z-scroll-" + str(pair[0]), {"mode": "TIME stepped by force_draw(false, 3.0)", "shader_TIME_advance_s": adv, "reads": reads,
			"reading": "a 3.0 s step moves the decoded shader TIME by 3.0 s; the seam sits at 1 - 0.1 * TIME (mod 1) and so moves LEFT 0.3 of the width per step. Only the plain texture has a real seam (ratio well above 1)"})
		rz.queue_free()
		await frames(2)
	# Y: the natural clock, once: does TIME follow the engine's tick counter when the window is drawn?
	var ry := make_rect(raw_time, tex_plain)
	root.add_child(ry)
	await frames(3)
	var natural: Array = []
	for k in range(2):
		if k == 1:
			await create_timer(3.0).timeout
			await frames(2)
		natural.append({"engine_ticks_s": snappedf(Time.get_ticks_msec() / 1000.0, 0.01), "shader_TIME_s": snappedf(read_time(grab()), 0.01)})
	var dy := float(natural[1]["shader_TIME_s"]) - float(natural[0]["shader_TIME_s"])
	var dticks := float(natural[1]["engine_ticks_s"]) - float(natural[0]["engine_ticks_s"])
	out("Y-natural-clock", {"reads": natural, "shader_TIME_advance_s": snappedf(dy, 0.01), "engine_ticks_advance_s": snappedf(dticks, 0.01), "window_was_drawn": dy > 2.5,
		"reading": "window_was_drawn false means Godot skipped normal draws (the window was covered) and TIME stood still: then this check says nothing about the natural clock"})
	quit(0)
