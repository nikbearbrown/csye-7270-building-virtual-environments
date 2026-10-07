extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var m = s.get_node("Meters"); var c = s.get_node("Child")
	while not p.controllable: await create_timer(0.2).timeout
	print("in the memory  -> child visible=", c.visible, " (false: she does not live in his memory)")
	s.flip(); await create_timer(1.3).timeout
	print("in the truth   -> child visible=", c.visible, "  pose=", c.texture.resource_path.get_file())
	m.spend(0,1); await create_timer(0.8).timeout
	print("one relic      -> pose=", c.texture.resource_path.get_file(), " (child_2 = she looked up)")
	m.spend(0,2); await create_timer(0.8).timeout
	print("all three      -> pose=", c.texture.resource_path.get_file(), " (child_3 = she sees you)")
	quit()
