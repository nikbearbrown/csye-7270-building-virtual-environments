extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var mb = s.get_node("MusicBox")
	while not p.controllable: await create_timer(0.1).timeout
	p.global_position = Vector2(mb.global_position.x, 815); await create_timer(0.4).timeout
	print("memory, floor  -> available=", mb._available())
	s.flip(); await create_timer(1.5).timeout
	p.global_position = Vector2(mb.global_position.x, 265); await create_timer(0.4).timeout
	print("truth, ceiling -> available=", mb._available())
	quit()
