extends SceneTree
var mode := "nodes"
var count := 48
var markers: Node3D
func _initialize() -> void: call_deferred("run")
func run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--mode="): mode = arg.get_slice("=", 1)
		if arg.begins_with("--count="): count = int(arg.get_slice("=", 1))
	markers = load("res://signal-garden/markers.gd").new()
	markers.mode = mode
	markers.count = count
	root.add_child(markers)
	Performance.add_custom_monitor("garden/marker_count", func(): return count)
	for i in range(60): await process_frame
	var times: Array[float] = []
	var previous := Time.get_ticks_usec()
	for i in range(300):
		await process_frame
		var now := Time.get_ticks_usec()
		times.append((now - previous) / 1000.0)
		previous = now
	times.sort()
	var total := 0.0
	for v in times: total += v
	print("BENCH,"+JSON.stringify({"mode":mode,"count":count,"mean_ms":total/times.size(),"p95_ms":times[284],"max_ms":times[-1],"objects":Performance.get_monitor(Performance.OBJECT_COUNT),"nodes":Performance.get_monitor(Performance.OBJECT_NODE_COUNT),"custom_count":Performance.get_custom_monitor("garden/marker_count"),"renderer":RenderingServer.get_video_adapter_name(),"note":"headless CPU wall time per simulated frame; no GPU draw measurement"}))
	Performance.remove_custom_monitor("garden/marker_count")
	markers.queue_free()
	await process_frame
	quit()
