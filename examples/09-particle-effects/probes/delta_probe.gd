extends SceneTree
# Records process delta for the first frames of a headless run, and how long a
# 0.5 s one-shot CPUParticles2D takes to emit `finished` when started on frame 1
# versus after 60 warm-up frames.
func _initialize() -> void:
	run.call_deferred()
func one_shot() -> CPUParticles2D:
	var c := CPUParticles2D.new()
	c.amount = 16; c.lifetime = 0.5; c.one_shot = true; c.explosiveness = 1.0; c.emitting = false
	root.add_child(c)
	return c
func time_to_finish(c: CPUParticles2D) -> Array:
	var sim := 0.0
	var t0 := Time.get_ticks_usec()
	var done := [false]
	c.finished.connect(func(): done[0] = true)
	c.emitting = true
	while not done[0]:
		await process_frame
		sim += get_root().get_process_delta_time()
	return [(Time.get_ticks_usec() - t0) / 1000.0, sim * 1000.0]
func run() -> void:
	var c1 := one_shot()
	var deltas := []
	var r1 = await time_to_finish(c1)
	print("started at frame 1: wall_ms=%.1f summed_delta_ms=%.1f" % [r1[0], r1[1]])
	for i in 60:
		await process_frame
		if i < 5: deltas.append(snappedf(get_root().get_process_delta_time() * 1000.0, 0.01))
	var c2 := one_shot()
	await process_frame
	var r2 = await time_to_finish(c2)
	print("started after warm-up: wall_ms=%.1f summed_delta_ms=%.1f" % [r2[0], r2[1]])
	print("sample deltas after warm-up (ms): ", deltas)
	quit()
