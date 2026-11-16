extends SceneTree
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var variants: Array = []
	for mode in ["nodes", "cached"]:
		var item = load("res://signal-garden/markers.gd").new()
		item.mode = mode
		item.count = 1000
		root.add_child(item)
		item.set_physics_process(false)
		variants.append(item)
	var max_error := 0.0
	for time in [0.0, 0.37, 1.8, 20.0]:
		for item in variants: item.update_markers(time)
		for i in range(1000):
			var expected := Vector3(-5.5 + fmod(i * 0.47, 11.0), 0.25 + sin(time * 2.0 + i) * 0.06, -2.65 if i % 2 else 2.65)
			for item in variants: max_error = maxf(max_error, item.observed_position(i).distance_to(expected))
	print(JSON.stringify({"id":"marker-position-parity","pass":max_error < 0.00001,"positions_checked":8000,"max_error_metres":max_error}))
	for item in variants: item.queue_free()
	await process_frame
	quit(0 if max_error < 0.00001 else 1)
