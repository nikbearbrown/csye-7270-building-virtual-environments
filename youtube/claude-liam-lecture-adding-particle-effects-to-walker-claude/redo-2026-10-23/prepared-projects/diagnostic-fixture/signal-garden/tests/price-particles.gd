extends SceneTree
func _initialize() -> void: call_deferred("run")
func run() -> void:
	for mode in ["empty", "burst-loop-upper-bound", "ambient"]:
		var effect: CPUParticles3D
		if mode != "empty":
			effect = load("res://signal-garden/effects/"+("burst" if mode.begins_with("burst") else "ambient")+".tscn").instantiate()
			effect.one_shot = false
			root.add_child(effect)
			effect.emitting = true
		for repeat in range(3):
			for i in range(60): await process_frame
			var samples: Array[float] = []
			var previous := Time.get_ticks_usec()
			for i in range(300):
				await process_frame
				var now := Time.get_ticks_usec()
				samples.append((now-previous)/1000.0)
				previous = now
			var total := 0.0
			for v in samples: total += v
			print(JSON.stringify({"mode":mode,"repeat":repeat,"mean_ms":total/300.0,"min_ms":samples.min(),"max_ms":samples.max(),"gpu_measured":false,"renderer":RenderingServer.get_video_adapter_name()}))
		if effect:
			effect.queue_free()
			await process_frame
	quit()
