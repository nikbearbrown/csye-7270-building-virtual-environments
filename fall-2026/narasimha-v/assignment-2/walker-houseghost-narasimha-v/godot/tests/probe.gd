extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player")
	await create_timer(0.4).timeout
	var seen := {}
	Input.action_press("move_right")
	for i in 120: await physics_frame; seen[p._walk_frame] = true
	Input.action_release("move_right")
	print("normal walking frames: ", seen.keys())
	s.flip(); await create_timer(1.4).timeout
	var g := {}
	Input.action_press("move_right")
	for i in 120: await physics_frame; g[p._walk_frame] = true
	Input.action_release("move_right")
	print("ghost walking frames:  ", g.keys(), "   tint=", p._sprite.modulate)
	quit()
