extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player")
	var start := Time.get_ticks_msec()
	await create_timer(1.5).timeout
	# a player pressing a key 1.5s in, as they would
	var ev := InputEventKey.new()
	ev.keycode = KEY_RIGHT
	ev.pressed = true
	Input.parse_input_event(ev)
	while not p.controllable: await create_timer(0.05).timeout
	print("pressed a key at 1.5s -> control at %.1fs" % ((Time.get_ticks_msec()-start)/1000.0))
	# and he moves straight away
	Input.action_press("move_right")
	var x0 = p.global_position.x
	await create_timer(0.8).timeout
	Input.action_release("move_right")
	print("then moved ", round(p.global_position.x - x0), " px")
	quit()
