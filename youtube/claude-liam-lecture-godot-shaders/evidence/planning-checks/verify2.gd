extends SceneTree
# A2: is TIME one global clock? Two identical shader nodes, one present from the start, one added at ~3 s.
# E : GPU time for the same 1920x1080 gradient, measured by the engine.

const CODE_TIME := "shader_type canvas_item;\nvoid fragment() { float k = floor(UV.y * 32.0); COLOR = TIME >= (k + 1.0) * 0.25 ? vec4(1.0) : vec4(0.0, 0.0, 0.0, 1.0); }"

func _initialize() -> void: call_deferred("run")

func frames(n: int) -> void:
	for i in range(n): await process_frame

func grab() -> Image:
	RenderingServer.force_draw(false)
	return root.get_texture().get_image()

func out(id: String, data: Dictionary) -> void:
	data["id"] = id
	print("RESULT " + JSON.stringify(data))

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

func stripes_lit(img: Image, x: int) -> int:
	var n := 0
	for k in range(32):
		var y := 20 + int((k + 0.5) * 10.0)
		if img.get_pixel(x, y).r > 0.5: n += 1
	return n

func run() -> void:
	root.size = Vector2i(640, 360)
	var early := make_rect(CODE_TIME, Vector2(20, 20), Vector2(80, 320))
	root.add_child(early)
	var proc_sum := 0.0
	var t_start_ticks := Time.get_ticks_msec() / 1000.0
	# Run ~3 s of process time, accumulating the engine's own delta.
	while proc_sum < 3.0:
		await process_frame
		proc_sum += get_root().get_process_delta_time()
	var late := make_rect(CODE_TIME, Vector2(120, 20), Vector2(80, 320))
	root.add_child(late)
	await frames(2)
	var img := grab()
	var c_early := stripes_lit(img, 60)
	var c_late := stripes_lit(img, 160)
	out("A2-time-is-one-global-clock", {
		"process_seconds_before_late_node": proc_sum,
		"wall_seconds_since_script_start": Time.get_ticks_msec() / 1000.0 - t_start_ticks,
		"engine_ticks_s": Time.get_ticks_msec() / 1000.0,
		"frames_drawn": Engine.get_frames_drawn(),
		"early_node_TIME_quarter_seconds_lit": c_early,
		"late_node_TIME_quarter_seconds_lit": c_late,
		"reading": "each lit stripe = 0.25 s of TIME. Same count on both = one global clock. A per-node clock would give the late node ~0."})
	early.queue_free()
	late.queue_free()
	await frames(2)

	# E: GPU time for a 1920x1080 gradient, measured by the engine.
	var sub := SubViewport.new()
	sub.size = Vector2i(1920, 1080)
	sub.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(sub)
	var grad := make_rect("shader_type canvas_item;\nvoid fragment() { COLOR = vec4(UV.x, 0.0, 0.0, 1.0); }", Vector2.ZERO, Vector2(1920, 1080))
	sub.add_child(grad)
	var rid := sub.get_viewport_rid()
	RenderingServer.viewport_set_measure_render_time(rid, true)
	await frames(40)
	var gpu: Array = []
	var cpu: Array = []
	for i in range(120):
		await process_frame
		gpu.append(RenderingServer.viewport_get_measured_render_time_gpu(rid))
		cpu.append(RenderingServer.viewport_get_measured_render_time_cpu(rid))
	gpu.sort()
	cpu.sort()
	out("E-gpu-gradient-cost", {
		"target": "SubViewport 1920x1080",
		"gpu_ms_min": gpu[0], "gpu_ms_median": gpu[60], "gpu_ms_max": gpu[119],
		"cpu_submit_ms_median": cpu[60],
		"reading": "engine-measured time to render the shader gradient into a 1920x1080 target, per frame. 0 would mean the counter is unsupported."})
	quit(0)
