extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var mb = s.get_node("MusicBox")
	await create_timer(0.5).timeout
	print("upright rest y=", round(p.global_position.y), " (815 = feet on the floor at 940)")
	s.flip(); await create_timer(1.8).timeout
	print("inverted rest y=", round(p.global_position.y), " (265 = feet on the ceiling at 140)")
	p.global_position.x = 1400
	await create_timer(0.5).timeout
	print("at the box, inverted -> inside=", mb._player_inside, " available=", mb._available())
	s.flip(); await create_timer(1.8).timeout
	print("flipped back, upright -> y=", round(p.global_position.y), " available=", mb._available(), " (false: the box is out of reach down here)")
	quit()
