extends SceneTree
func _initialize() -> void: call_deferred("run")
func run() -> void:
	root.size = Vector2i(1280,720)
	var game = load("res://signal-garden/main.tscn").instantiate()
	game.audio_enabled = false
	root.add_child(game)
	game.set_physics_process(false)
	game.burst.one_shot = false
	game.burst.position = Vector3(-2,0.4,0)
	var rid := root.get_viewport_rid()
	RenderingServer.viewport_set_measure_render_time(rid, true)
	for repeat in range(3):
		for mode in ["off","burst-loop-upper-bound","ambient"]:
			game.burst.visible = mode.begins_with("burst")
			game.burst.emitting = mode.begins_with("burst")
			game.ambient.visible = mode == "ambient"
			game.ambient.emitting = mode == "ambient"
			for i in range(60): await process_frame
			var cpu := 0.0
			var gpu := 0.0
			var draws := 0.0
			for i in range(60):
				await process_frame
				cpu += RenderingServer.viewport_get_measured_render_time_cpu(rid) + RenderingServer.get_frame_setup_time_cpu()
				gpu += RenderingServer.viewport_get_measured_render_time_gpu(rid)
				draws += RenderingServer.viewport_get_render_info(rid, RenderingServer.VIEWPORT_RENDER_INFO_TYPE_VISIBLE, RenderingServer.VIEWPORT_RENDER_INFO_DRAW_CALLS_IN_FRAME)
			print(JSON.stringify({"repeat":repeat,"mode":mode,"render_cpu_ms":cpu/60.0,"render_gpu_ms":gpu/60.0,"draw_calls":draws/60.0,"window":[1280,720],"adapter":RenderingServer.get_video_adapter_name(),"measurement":"RenderingServer viewport timers; zero means unavailable, not free"}))
	game.queue_free()
	await process_frame
	quit()
