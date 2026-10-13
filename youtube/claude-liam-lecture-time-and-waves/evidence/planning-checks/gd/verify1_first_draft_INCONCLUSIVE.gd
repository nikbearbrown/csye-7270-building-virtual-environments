extends SceneTree
# Time and Waves, planning check 1: what TIME really is.
# TIME is read back from a pixel: the ENCODER shader packs TIME into the red, green and blue channels
# (whole seconds / 255, then two 8-bit digits of the fraction: about 0.00001 s of resolution).
# Checks, in order:
#   A  the clock origin: TIME against Time.get_ticks_usec() on the same frame (are they the same zero?)
#   B  a node added late reads the same TIME as one present from the start
#   C  Engine.time_scale = 0.5: how fast does TIME advance, and the delta a node's _process receives
#   D  SceneTree.paused = true: does TIME keep advancing, and does a pausable node's _process keep running
#   E  a start time taken from the other clock (Time.get_ticks_msec) versus an age counted from delta
#   F  rendering/limits/time/time_rollover_secs changed at runtime: does TIME wrap?
# Run: godot --path <scratch project> --script res://verify1.gd

const ENCODER := "shader_type canvas_item;\nvoid fragment() {\n\tfloat whole = floor(TIME);\n\tfloat part = (TIME - whole) * 255.0;\n\tfloat p1 = floor(part);\n\tCOLOR = vec4(whole / 255.0, p1 / 255.0, part - p1, 1.0);\n}\n"
const ENC_START := "shader_type canvas_item;\nuniform float start;\nvoid fragment() {\n\tfloat v = TIME - start + 8.0;\n\tfloat whole = floor(v);\n\tfloat part = (v - whole) * 255.0;\n\tfloat p1 = floor(part);\n\tCOLOR = vec4(whole / 255.0, p1 / 255.0, part - p1, 1.0);\n}\n"
const ENC_AGE := "shader_type canvas_item;\nuniform float age;\nvoid fragment() {\n\tfloat v = age;\n\tfloat whole = floor(v);\n\tfloat part = (v - whole) * 255.0;\n\tfloat p1 = floor(part);\n\tCOLOR = vec4(whole / 255.0, p1 / 255.0, part - p1, 1.0);\n}\n"
const COUNTER := "extends Node\nvar n := 0\nvar last_delta := 0.0\nfunc _process(d):\n\tn += 1\n\tlast_delta = d\n"

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

func make_rect(code: String, pos: Vector2) -> ColorRect:
	var rect := ColorRect.new()
	rect.position = pos
	rect.size = Vector2(20, 20)
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
	var whole := roundf(c.r * 255.0)
	var p1 := roundf(c.g * 255.0)
	return whole + (p1 + c.b) / 255.0

func read_time() -> float:
	return decode(grab(), enc_a)

# advance for `secs` of REAL time (Time.get_ticks_usec), whatever the engine time scale says
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

func run() -> void:
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
		"time_scale_default": Engine.time_scale, "paused_default": paused})

	# A: the clock origin. 30 samples over about half a second.
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
	out("A-clock-origin", {"samples": diffs.size(), "ticks_minus_TIME_min_s": snappedf(diffs[0], 0.001), "median_s": snappedf(diffs[diffs.size() / 2], 0.001),
		"max_s": snappedf(diffs[diffs.size() - 1], 0.001), "first_TIME_read_s": snappedf(first_time, 0.001),
		"reading": "ticks - TIME on the same frame. If TIME and Time.get_ticks_usec shared a zero this would be about one frame (0.017 s) or less."})

	# B: a node added late reads the same TIME. Run to 3.0 s of TIME, then add a second encoder.
	while read_time() < 3.0:
		await process_frame
	var enc_b := make_rect(ENCODER, Vector2(60, 10))
	root.add_child(enc_b)
	await frames(2)
	var img := grab()
	var ta := decode(img, enc_a)
	var tb := decode(img, enc_b)
	out("B-late-node", {"early_node_TIME_s": snappedf(ta, 0.0001), "late_node_TIME_s": snappedf(tb, 0.0001), "difference_s": snappedf(absf(ta - tb), 0.00001),
		"reading": "two nodes, one added at about 3 s: the same TIME in the same frame."})

	# C: time scale 0.5. Real wall time against TIME, and the delta a node receives.
	var k0 := ticks(); var t0 := read_time()
	counter_pausable.n = 0
	Engine.time_scale = 0.5
	await run_real(1.0)
	var k1 := ticks(); var t1 := read_time()
	out("C-time-scale-half", {"real_elapsed_s": snappedf(k1 - k0, 0.001), "TIME_elapsed_s": snappedf(t1 - t0, 0.001), "ratio": snappedf((t1 - t0) / (k1 - k0), 0.001),
		"process_calls_in_that_second": counter_pausable.n, "last_delta_received": snappedf(counter_pausable.last_delta, 0.0001),
		"reading": "TIME advances at about half the speed of the wall clock, and _process delta is halved too."})
	Engine.time_scale = 1.0
	await frames(3)

	# D: pause the tree. TIME should keep advancing; a pausable node's _process should stop; an ALWAYS node's should not.
	var k2 := ticks(); var t2 := read_time()
	var np0: int = counter_pausable.n
	var na0: int = counter_always.n
	paused = true
	await run_real(1.0)
	var k3 := ticks(); var t3 := read_time()
	out("D-paused", {"real_elapsed_s": snappedf(k3 - k2, 0.001), "TIME_elapsed_s": snappedf(t3 - t2, 0.001), "ratio": snappedf((t3 - t2) / (k3 - k2), 0.001),
		"pausable_node_process_calls_while_paused": counter_pausable.n - np0, "always_node_process_calls_while_paused": counter_always.n - na0,
		"reading": "TIME keeps running while the tree is paused; the pausable node's _process stops."})
	paused = false
	await frames(3)

	# E: a per-node clock. A node is created now. Option 1 takes a start time from Time.get_ticks_msec and the shader computes TIME - start.
	#    Option 2 keeps an age that _process advances by delta and passes in as a uniform.
	var start_rect := make_rect(ENC_START, Vector2(110, 10))
	var age_rect := make_rect(ENC_AGE, Vector2(160, 10))
	var start_val := Time.get_ticks_msec() / 1000.0
	(start_rect.material as ShaderMaterial).set_shader_parameter("start", start_val)
	var age := 0.0
	(age_rect.material as ShaderMaterial).set_shader_parameter("age", age)
	root.add_child(start_rect)
	root.add_child(age_rect)
	var samples: Array = []
	var prev := ticks()
	for i in range(40):
		await process_frame
		var now := ticks()
		age += now - prev
		prev = now
		(age_rect.material as ShaderMaterial).set_shader_parameter("age", age)
		await frames(1)
		var im := grab()
		samples.append([snappedf(now - start_val, 0.001), snappedf(decode(im, start_rect) - 8.0, 0.001), snappedf(decode(im, age_rect), 0.001)])
	out("E-per-node-clock", {"start_value_from_ticks_s": snappedf(start_val, 0.001), "samples_real_elapsed_shader_TIME_minus_start_age": [samples[0], samples[10], samples[25], samples[39]],
		"reading": "columns: real seconds since the node was made, (TIME - start) the shader computed, the age counted from delta. The middle column starts below zero by the clock offset (A) and stays offset."})

	# F: roll-over. Change the project setting at runtime and see whether TIME wraps.
	ProjectSettings.set_setting("rendering/limits/time/time_rollover_secs", 2.0)
	var seq: Array = []
	for i in range(60):
		await process_frame
		seq.append(snappedf(read_time(), 0.01))
		await create_timer(0.05).timeout
	var wrapped := false
	for i in range(1, seq.size()):
		if seq[i] < seq[i - 1] - 0.5: wrapped = true
	out("F-rollover-runtime-setting", {"wrapped": wrapped, "TIME_samples_every_50ms": seq,
		"reading": "if the runtime change took effect, TIME falls back near 0 when it passes 2.0"})
	quit(0)
