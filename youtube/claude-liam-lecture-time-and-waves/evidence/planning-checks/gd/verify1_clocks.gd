extends SceneTree
# Time and Waves, planning check 1 (final order): what TIME is, measured by reading it back from a pixel.
# The ENCODER shader packs TIME into red, green and blue (whole seconds / 255, then two 8-bit digits of the fraction: about 0.00001 s).
# Every phase below prints one RESULT line. The window MUST keep being drawn (run with --always-on-top): TIME only advances on drawn frames.
#   A  the clock origin: Time.get_ticks_usec() minus TIME on the same frame
#   B  a node added late: the same TIME as the first, and the real 02-pulse shader pixels equal for 60 frames
#   C  a per-node clock: age counted from _process delta, against (TIME - start) with start taken from Time.get_ticks_msec()
#   D  Engine.time_scale = 0.5 for one second: TIME rate, the delta a node receives, the age rate
#   E  the clocks after D: how far apart ticks and TIME have drifted
#   F  SceneTree.paused for one second: TIME rate, a pausable node's _process, an always-processing node's _process, a pausable age
#   G  rendering/limits/time/time_rollover_secs set at run time: does TIME wrap?
# Run: godot --path <scratch> --always-on-top --script res://verify1_clocks.gd -- --film <abs film dir>

const ENCODER := "shader_type canvas_item;\nvoid fragment() {\n\tfloat whole = floor(TIME);\n\tfloat part = (TIME - whole) * 255.0;\n\tfloat p1 = floor(part);\n\tCOLOR = vec4(whole / 255.0, p1 / 255.0, part - p1, 1.0);\n}\n"
const ENC_START := "shader_type canvas_item;\nuniform float start;\nvoid fragment() {\n\tfloat v = TIME - start + 8.0;\n\tfloat whole = floor(v);\n\tfloat part = (v - whole) * 255.0;\n\tfloat p1 = floor(part);\n\tCOLOR = vec4(whole / 255.0, p1 / 255.0, part - p1, 1.0);\n}\n"
const COUNTER := "extends Node\nvar n := 0\nvar age := 0.0\nvar last_delta := 0.0\nfunc _process(d):\n\tn += 1\n\tage += d\n\tlast_delta = d\n"

var film := ""
var enc_a: ColorRect
var counter_pausable: Node
var counter_always: Node

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func ticks() -> float:
	return Time.get_ticks_usec() / 1000000.0

func shader_text(name: String) -> String:
	return FileAccess.get_file_as_string(film + "/lab-shaders/" + name)

func make_rect(code: String, pos: Vector2, size := Vector2(20, 20)) -> ColorRect:
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

func decode(img: Image, rect: ColorRect) -> float:
	var c := img.get_pixel(int(rect.position.x + 10), int(rect.position.y + 10))
	return roundf(c.r * 255.0) + (roundf(c.g * 255.0) + c.b) / 255.0

func read_time() -> float:
	return decode(grab(), enc_a)

func run_real(secs: float) -> void:
	var t0 := ticks()
	while ticks() - t0 < secs:
		await process_frame

func make_counter(always: bool) -> Node:
	var n := Node.new()
	var s := GDScript.new()
	s.source_code = COUNTER
	s.reload()
	n.set_script(s)
	if always:
		n.process_mode = Node.PROCESS_MODE_ALWAYS
	return n

func mixc(p: float) -> Color:
	var a := Vector3(0.37, 0.64, 0.57)
	var b := Vector3(0.98, 0.97, 0.96)
	var m := a * (1.0 - p) + b * p
	return Color(m.x, m.y, m.z)

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--film": film = a[i + 1]
	root.size = Vector2i(320, 180)
	enc_a = make_rect(ENCODER, Vector2(10, 10))
	root.add_child(enc_a)
	counter_pausable = make_counter(false)
	counter_always = make_counter(true)
	root.add_child(counter_pausable)
	root.add_child(counter_always)
	var probe := grab()
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name(), "image_size": [probe.get_width(), probe.get_height()],
		"time_scale_default": Engine.time_scale, "paused_default": paused, "window_always_on_top": DisplayServer.window_get_flag(DisplayServer.WINDOW_FLAG_ALWAYS_ON_TOP)})

	# ---- A: the clock origin, 30 samples over about half a second
	await frames(2)
	var diffs: Array = []
	var first_time := -1.0
	for i in range(30):
		await process_frame
		var k := ticks()
		var t := read_time()
		if first_time < 0.0: first_time = t
		diffs.append(k - t)
		await create_timer(0.016).timeout
	diffs.sort()
	var offset_A: float = diffs[diffs.size() / 2]
	out("A-clock-origin", {"samples": diffs.size(), "ticks_minus_TIME_min_s": snappedf(diffs[0], 0.001), "median_s": snappedf(offset_A, 0.001),
		"max_s": snappedf(diffs[diffs.size() - 1], 0.001), "first_TIME_read_s": snappedf(first_time, 0.001),
		"reading": "ticks minus TIME on the same frame, 30 frames. One frame is about 0.01 s. If both counted from the same zero this would be 0.01 or less."})

	# ---- B: a late node. Run to 3 s of TIME, add a second encoder and a second real pulse next to the first.
	var pulse_src := shader_text("02-pulse.gdshader")
	var pulse_early := make_rect(pulse_src, Vector2(60, 10), Vector2(40, 40))
	root.add_child(pulse_early)
	while read_time() < 3.0:
		await process_frame
	var enc_b := make_rect(ENCODER, Vector2(110, 10))
	var pulse_late := make_rect(pulse_src, Vector2(160, 10), Vector2(40, 40))
	root.add_child(enc_b)
	root.add_child(pulse_late)
	await frames(2)
	var img := grab()
	var ta := decode(img, enc_a)
	var tb := decode(img, enc_b)
	var worst := 0.0
	var worst_vs_formula := 0.0
	for f in range(60):
		await process_frame
		var im := grab()
		var pe := im.get_pixel(80, 30)
		var pl := im.get_pixel(180, 30)
		worst = maxf(worst, maxf(maxf(absf(pe.r - pl.r), absf(pe.g - pl.g)), absf(pe.b - pl.b)) * 255.0)
		var tt := decode(im, enc_a)
		var want := mixc(0.5 + 0.5 * sin(TAU * tt))
		worst_vs_formula = maxf(worst_vs_formula, maxf(maxf(absf(pl.r - want.r), absf(pl.g - want.g)), absf(pl.b - want.b)) * 255.0)
	out("B-late-node", {"early_node_TIME_s": snappedf(ta, 0.0001), "late_node_TIME_s": snappedf(tb, 0.0001), "TIME_difference_s": snappedf(absf(ta - tb), 0.00001),
		"pulse_pixel_max_difference_8bit_steps_over_60_frames": snappedf(worst, 0.01), "late_pulse_vs_formula_max_error_steps": snappedf(worst_vs_formula, 0.01),
		"reading": "two nodes running 02-pulse, the second added at about 3 s of TIME: the same TIME, and the same pixels frame after frame."})
	pulse_early.queue_free(); pulse_late.queue_free(); enc_b.queue_free()
	await frames(2)

	# ---- C: a per-node clock, created now
	var start_rect := make_rect(ENC_START, Vector2(110, 10))
	var age_src := shader_text("01-age.gdshader")
	var age_rect := make_rect(age_src, Vector2(160, 10), Vector2(40, 40))
	var start_val := Time.get_ticks_msec() / 1000.0
	(start_rect.material as ShaderMaterial).set_shader_parameter("start", start_val)
	var age := 0.0
	(age_rect.material as ShaderMaterial).set_shader_parameter("age", age)
	root.add_child(start_rect)
	root.add_child(age_rect)
	var samples: Array = []
	var prev := ticks()
	var worst_age := 0.0
	for i in range(60):
		await process_frame
		var now := ticks()
		age += now - prev
		prev = now
		(age_rect.material as ShaderMaterial).set_shader_parameter("age", age)
		await frames(1)
		var im2 := grab()
		var shader_elapsed := decode(im2, start_rect) - 8.0
		var want_age := mixc(0.5 + 0.5 * sin(TAU * age))
		var pa := im2.get_pixel(180, 30)
		worst_age = maxf(worst_age, maxf(maxf(absf(pa.r - want_age.r), absf(pa.g - want_age.g)), absf(pa.b - want_age.b)) * 255.0)
		if i in [0, 20, 40, 59]:
			samples.append([snappedf(now - start_val, 0.001), snappedf(shader_elapsed, 0.001), snappedf(age, 0.001)])
	out("C-per-node-clock", {"start_value_from_Time_get_ticks_msec_s": snappedf(start_val, 0.001), "samples_[real_s_since_node_made, shader_TIME_minus_start, age_from_delta]": samples,
		"age_pulse_pixel_vs_formula_max_error_steps": snappedf(worst_age, 0.01),
		"reading": "TIME minus a start taken from the tick counter begins below zero by the clock offset (A). The age counted from delta starts at zero with the node, and the 01-age pixel follows 0.5 + 0.5 sin(TAU age)."})
	start_rect.queue_free(); age_rect.queue_free()
	await frames(2)

	# ---- D: time scale 0.5 for one real second
	var k0 := ticks(); var t0 := read_time()
	var n0: int = counter_pausable.n
	var age0: float = counter_pausable.age
	Engine.time_scale = 0.5
	await run_real(1.0)
	var k1 := ticks(); var t1 := read_time()
	out("D-time-scale-half", {"real_elapsed_s": snappedf(k1 - k0, 0.001), "TIME_elapsed_s": snappedf(t1 - t0, 0.001), "TIME_rate": snappedf((t1 - t0) / (k1 - k0), 0.001),
		"age_from_delta_rate": snappedf((float(counter_pausable.age) - age0) / (k1 - k0), 0.001), "process_calls": counter_pausable.n - n0,
		"last_delta_received": snappedf(counter_pausable.last_delta, 0.0001),
		"reading": "at a time scale of one half TIME advances at about half the real rate, and so does an age counted from delta."})
	Engine.time_scale = 1.0
	await frames(3)

	# ---- E: drift after D
	var diffs2: Array = []
	for i in range(20):
		await process_frame
		diffs2.append(ticks() - read_time())
	diffs2.sort()
	out("E-clocks-after-time-scale", {"ticks_minus_TIME_median_s": snappedf(diffs2[diffs2.size() / 2], 0.001), "before_D_median_s": snappedf(offset_A, 0.001),
		"drift_s": snappedf(diffs2[diffs2.size() / 2] - offset_A, 0.001),
		"reading": "one second at half speed leaves the tick counter half a second ahead of TIME for good: the two clocks do not share a speed."})

	# ---- F: pause for one real second
	var k2 := ticks(); var t2 := read_time()
	var np0: int = counter_pausable.n
	var na0: int = counter_always.n
	var age_p0: float = counter_pausable.age
	var age_a0: float = counter_always.age
	paused = true
	await run_real(1.0)
	var k3 := ticks(); var t3 := read_time()
	out("F-paused", {"real_elapsed_s": snappedf(k3 - k2, 0.001), "TIME_elapsed_s": snappedf(t3 - t2, 0.001), "TIME_rate": snappedf((t3 - t2) / (k3 - k2), 0.001),
		"pausable_node_process_calls": counter_pausable.n - np0, "always_node_process_calls": counter_always.n - na0,
		"pausable_age_gain_s": snappedf(float(counter_pausable.age) - age_p0, 0.001), "always_age_gain_s": snappedf(float(counter_always.age) - age_a0, 0.001),
		"reading": "TIME keeps its full rate while the tree is paused; a pausable node's _process stops (so its age stops); an always-processing node carries on."})
	paused = false
	await frames(3)

	# ---- G: rollover set at run time
	ProjectSettings.set_setting("rendering/limits/time/time_rollover_secs", 2.0)
	var seq: Array = []
	for i in range(60):
		await process_frame
		seq.append(snappedf(read_time(), 0.01))
		await create_timer(0.05).timeout
	var wraps := 0
	for i in range(1, seq.size()):
		if seq[i] < seq[i - 1] - 0.5: wraps += 1
	var peak := 0.0
	for v in seq: peak = maxf(peak, float(v))
	out("G-rollover-runtime-setting", {"wraps_seen": wraps, "highest_TIME_seen_s": peak, "TIME_every_50ms": seq,
		"reading": "with the limit set to 2.0 s, TIME falls back near 0 each time it passes 2.0 (the project setting is read every frame). The default limit is 3600 s."})
	quit(0)
