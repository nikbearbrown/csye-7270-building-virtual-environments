extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var h = s.get_node("HUD")
	await create_timer(11.0).timeout
	print("control after the safety window: ", p.controllable, "  at ", p.global_position)
	Input.action_press("move_right"); await create_timer(0.6).timeout
	print("moving: x=", round(p.global_position.x), " vel=", round(p.velocity.x))
	print("cue on screen at x=", round(h._cue.position.x), " (should be roughly 800-1100, i.e. in view)")
	Input.action_release("move_right")
	quit()
