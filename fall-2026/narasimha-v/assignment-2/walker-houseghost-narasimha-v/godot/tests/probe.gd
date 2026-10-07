extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var h = s.get_node("HUD")
	await create_timer(2.0).timeout
	print("waiting on line 1 -> prompt='", h._prompt.text, "' controllable=", p.controllable)
	# advance through each line the way a reader would
	for i in 4:
		_press(KEY_SPACE)
		await create_timer(0.5).timeout
		print("  after press %d -> lines shown: %d" % [i+1, h._opening.text.count("\n")+1])
	while not p.controllable: await create_timer(0.2).timeout
	print("control handed over after reading all four")
	# and I reopens it mid-game
	_press(KEY_I)
	await create_timer(0.5).timeout
	print("pressed I -> story open=", s._story_open, " controllable=", p.controllable, " prompt='", h._prompt.text, "'")
	_press(KEY_I)
	await create_timer(0.5).timeout
	print("pressed I again -> story open=", s._story_open, " controllable=", p.controllable)
	quit()

func _press(code):
	var e := InputEventKey.new(); e.keycode = code; e.physical_keycode = code; e.pressed = true
	Input.parse_input_event(e)
	var u := InputEventKey.new(); u.keycode = code; u.physical_keycode = code; u.pressed = false
	Input.parse_input_event(u)
