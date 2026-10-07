extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player")
	await create_timer(0.6).timeout
	p.global_position = Vector2(1900, 815); await create_timer(0.5).timeout
	Input.action_press("move_right"); for i in 200: await physics_frame
	Input.action_release("move_right"); await create_timer(0.2).timeout
	print("memory  -> blocked at x=", round(p.global_position.x))
	s.flip(); await create_timer(1.5).timeout
	Input.action_press("move_right"); for i in 200: await physics_frame
	Input.action_release("move_right"); await create_timer(0.2).timeout
	print("truth   -> reached x=", round(p.global_position.x), " (past 2200 = the memory furniture is gone)")
	quit()
