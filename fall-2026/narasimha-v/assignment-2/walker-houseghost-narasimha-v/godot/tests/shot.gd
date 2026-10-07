extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player")
	await create_timer(1.0).timeout
	Input.action_press("move_right")
	var seen := {}
	for shot in range(8):
		for i in 5: await physics_frame
		seen[p._walk_frame] = true
		root.get_viewport().get_texture().get_image().save_png("res://../evidence/w%d.png" % shot)
	Input.action_release("move_right")
	print("frames used: ", seen.keys())
	quit()
