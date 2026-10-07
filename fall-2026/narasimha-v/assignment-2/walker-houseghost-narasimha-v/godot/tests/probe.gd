extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player")
	# read the opening like a player
	var guard := 0
	while not p.controllable and guard < 30:
		guard += 1
		_press(KEY_SPACE)
		await create_timer(0.3).timeout
	print("controllable=", p.controllable, "  story_open=", s._story_open, "  awaiting_key=", s._awaiting_key)
	Input.action_press("move_right")
	for n in 3:
		await create_timer(0.4).timeout
		print("   x=%d  vel=%d  direction_axis=%.1f" % [p.global_position.x, p.velocity.x, Input.get_axis("move_left","move_right")])
	Input.action_release("move_right")
	quit()

func _press(code):
	var e := InputEventKey.new(); e.keycode=code; e.physical_keycode=code; e.pressed=true
	Input.parse_input_event(e)
	var u := InputEventKey.new(); u.keycode=code; u.physical_keycode=code; u.pressed=false
	Input.parse_input_event(u)
