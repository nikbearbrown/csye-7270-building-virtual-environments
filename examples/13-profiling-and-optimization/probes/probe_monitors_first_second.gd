extends SceneTree
var frames := 0
func _initialize() -> void:
	run.call_deferred()
func run() -> void:
	var holder := Node2D.new(); root.add_child(holder)
	var tex := PlaceholderTexture2D.new(); tex.size = Vector2(16,16)
	for i in 5000:
		var s := Sprite2D.new(); s.texture = tex; s.position = Vector2(randf()*640, randf()*480)
		holder.add_child(s)
	RenderingServer.viewport_set_measure_render_time(root.get_viewport_rid(), true)
	var proc := []; var phys := []; var fps := []
	for i in 120:
		await process_frame
		for s in holder.get_children():
			s.position.x -= 1.0
		proc.append(Performance.get_monitor(Performance.TIME_PROCESS))
		phys.append(Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS))
		fps.append(Performance.get_monitor(Performance.TIME_FPS))
	print("TIME_PROCESS last=", proc[-1], " TIME_PHYSICS_PROCESS last=", phys[-1], " FPS=", fps[-1])
	print("OBJECT_COUNT=", Performance.get_monitor(Performance.OBJECT_COUNT), " NODE_COUNT=", Performance.get_monitor(Performance.OBJECT_NODE_COUNT), " ORPHAN=", Performance.get_monitor(Performance.OBJECT_ORPHAN_NODE_COUNT))
	print("RENDER draw_calls=", Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME), " objects=", Performance.get_monitor(Performance.RENDER_TOTAL_OBJECTS_IN_FRAME), " prims=", Performance.get_monitor(Performance.RENDER_TOTAL_PRIMITIVES_IN_FRAME), " vram=", Performance.get_monitor(Performance.RENDER_VIDEO_MEM_USED))
	print("measured render cpu ms=", RenderingServer.viewport_get_measured_render_time_cpu(root.get_viewport_rid()), " gpu ms=", RenderingServer.viewport_get_measured_render_time_gpu(root.get_viewport_rid()), " total cpu=", RenderingServer.get_frame_setup_time_cpu())
	print("MEMORY_STATIC=", Performance.get_monitor(Performance.MEMORY_STATIC), " MEMORY_STATIC_MAX=", Performance.get_monitor(Performance.MEMORY_STATIC_MAX))
	print("PHYSICS_2D_ACTIVE_OBJECTS=", Performance.get_monitor(Performance.PHYSICS_2D_ACTIVE_OBJECTS), " PAIRS=", Performance.get_monitor(Performance.PHYSICS_2D_COLLISION_PAIRS))
	print("Engine.get_frames_per_second=", Engine.get_frames_per_second(), " max_fps=", Engine.max_fps, " physics_ticks=", Engine.physics_ticks_per_second)
	quit(0)
