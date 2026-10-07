extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var mb = s.get_node("MusicBox")
	await create_timer(0.6).timeout
	print("spawn x=", round(p.global_position.x), "   music box x=", round(mb.global_position.x),
	      "   distance=", round(abs(mb.global_position.x - p.global_position.x)), "px")
	print("glow visible from spawn: ", mb.get_node("Glow").visible)
	s.flip(); await create_timer(1.4).timeout
	Input.action_press("move_right")
	var reached := false
	for i in 400:
		await physics_frame
		if mb._player_inside: reached = true; break
	Input.action_release("move_right")
	print("reached the box while inverted: ", reached, "  at x=", round(p.global_position.x))
	quit()
