extends SceneTree
func _initialize() -> void:
	run.call_deferred()
func run() -> void:
	var holder := Node2D.new(); root.add_child(holder)
	var tex := PlaceholderTexture2D.new(); tex.size = Vector2(16,16)
	for i in 5000:
		var s := Sprite2D.new(); s.texture = tex; s.position = Vector2(randf()*640, randf()*480)
		holder.add_child(s)
	var t_start := Time.get_ticks_usec()
	var frames := 0
	var last := Time.get_ticks_usec()
	var worst := 0
	while Time.get_ticks_usec() - t_start < 3_500_000:
		await process_frame
		var now := Time.get_ticks_usec()
		worst = max(worst, now - last)
		last = now
		frames += 1
		for s in holder.get_children():
			s.position.x -= 1.0
		if frames % 50 == 0:
			pass
	var secs := (Time.get_ticks_usec() - t_start) / 1e6
	print("frames=", frames, " in ", secs, "s => ", frames / secs, " fps (own count); worst frame gap ms=", worst / 1000.0)
	print("TIME_PROCESS=", Performance.get_monitor(Performance.TIME_PROCESS), " TIME_PHYSICS_PROCESS=", Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS), " TIME_FPS=", Performance.get_monitor(Performance.TIME_FPS), " Engine fps=", Engine.get_frames_per_second())
	quit(0)
