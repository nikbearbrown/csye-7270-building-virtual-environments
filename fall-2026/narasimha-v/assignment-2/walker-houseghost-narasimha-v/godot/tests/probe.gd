extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player")
	await create_timer(0.3).timeout
	s.flip(); await create_timer(1.0).timeout   # remembered state
	Input.action_press("move_right")
	var seen := {}
	for i in 240:
		await physics_frame
		seen[p._walk_frame] = true
	Input.action_release("move_right")
	print("walk frames used while moving: ", seen.keys())
	await create_timer(0.4).timeout
	print("frame when stopped: ", p._walk_frame)
	s.flip(); await create_timer(1.0).timeout   # back to ghost
	Input.action_press("move_left")
	var ghost_frames := {}
	for i in 120:
		await physics_frame
		ghost_frames[p._walk_frame] = true
	Input.action_release("move_left")
	print("ghost state frame stays: ", ghost_frames.keys(), " (should be [0] - ghosts drift, they do not walk)")
	quit()
