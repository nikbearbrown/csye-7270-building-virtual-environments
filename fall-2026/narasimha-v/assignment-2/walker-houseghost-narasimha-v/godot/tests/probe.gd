extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var c = s.get_node("Child")
	await create_timer(1.0).timeout
	print("opening   -> child visible=", c.visible)
	while not p.controllable: await create_timer(0.2).timeout
	print("in memory -> child visible=", c.visible, " (false: she is not in his memory)")
	s.flip(); await create_timer(1.4).timeout
	print("in truth  -> child visible=", c.visible)
	quit()
