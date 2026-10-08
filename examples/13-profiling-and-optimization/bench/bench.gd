extends SceneTree
# Headless benchmark. Run as:
#   godot --headless --fixed-fps 60 --path godot \
#         --script res://bench/bench.gd -- \
#         --mode=servers --count=500 --frames=600
#
# --mode   : "servers" (PhysicsServer2D path) or "nodes" (Area2D node path)
# --count  : bullet count
# --frames : measured frames after the warm-up window


func _initialize() -> void:
	run_benchmark.call_deferred()


func run_benchmark() -> void:
	var user_args := OS.get_cmdline_user_args()
	var mode := "servers"
	var count := 500
	var frames := 600
	var warmup := 120
	for arg in user_args:
		if arg.begins_with("--mode="):
			mode = arg.substr(7)
		elif arg.begins_with("--count="):
			count = int(arg.substr(8))
		elif arg.begins_with("--frames="):
			frames = int(arg.substr(9))

	var scene_path := "res://shower.tscn" if mode == "servers" else "res://bench/shower_nodes.tscn"
	var scene := (load(scene_path) as PackedScene).instantiate()
	(scene.get_node("Bullets") as Node).set("bullet_count", count)
	root.add_child(scene)
	current_scene = scene

	for _i in warmup:
		await physics_frame

	var frame_times: Array[float] = []
	frame_times.resize(frames)
	for i in frames:
		var t0 := Time.get_ticks_usec()
		await physics_frame
		frame_times[i] = (Time.get_ticks_usec() - t0) / 1000.0  # ms

	var sorted := frame_times.duplicate()
	sorted.sort()
	var total := 0.0
	for t in sorted:
		total += t
	var mean_ms: float = total / sorted.size()
	var p95_ms: float = sorted[int(sorted.size() * 0.95)]
	var max_ms: float = sorted[-1]

	var object_count := int(Performance.get_monitor(Performance.OBJECT_COUNT))
	var node_count := int(Performance.get_monitor(Performance.OBJECT_NODE_COUNT))
	var static_memory_mb: float = Performance.get_monitor(Performance.MEMORY_STATIC) / 1048576.0

	# TIME_PHYSICS_PROCESS: cumulative seconds spent in _physics_process callbacks
	# across all nodes for the most-recently completed physics tick.
	# TIME_PROCESS: same but for _process callbacks.
	var time_physics_ms: float = Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS) * 1000.0
	var time_process_ms: float = Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0

	print("mode,count,frames,mean_ms,p95_ms,max_ms,object_count,node_count,static_memory_mb")
	print("%s,%d,%d,%.3f,%.3f,%.3f,%d,%d,%.2f" % [
		mode, count, frames,
		mean_ms, p95_ms, max_ms,
		object_count, node_count, static_memory_mb
	])
	print("# TIME_PROCESS=%.3f ms — seconds all nodes spent in _process last frame" % time_process_ms)
	print("# TIME_PHYSICS_PROCESS=%.3f ms — seconds all nodes spent in _physics_process last physics tick" % time_physics_ms)

	scene.queue_free()
	await process_frame
	await process_frame
	quit(0)
