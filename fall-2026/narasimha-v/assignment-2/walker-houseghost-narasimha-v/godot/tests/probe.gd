extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player")
	var guard := 0
	while not p.controllable and guard < 40:
		guard += 1
		_press(KEY_SPACE)
		await create_timer(0.3).timeout
	print("control handed over: ", p.controllable, "  alpha=", p.modulate.a, "  pos=", p.global_position)
	Input.action_press("move_right"); await create_timer(0.8).timeout
	print("moving -> x=", round(p.global_position.x), " vel=", round(p.velocity.x))
	Input.action_release("move_right")
	quit()
func _press(c):
	var e := InputEventKey.new(); e.keycode=c; e.physical_keycode=c; e.pressed=true; Input.parse_input_event(e)
	var u := InputEventKey.new(); u.keycode=c; u.physical_keycode=c; u.pressed=false; Input.parse_input_event(u)
