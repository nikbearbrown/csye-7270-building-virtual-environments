extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var h = s.get_node("HUD"); var m = s.get_node("Meters")
	while not p.controllable: await create_timer(0.1).timeout
	s.flip(); await create_timer(1.4).timeout
	var relics = s.get_tree().get_nodes_in_group("relic")
	for i in relics.size():
		var r = relics[i]
		p.global_position = Vector2(r.global_position.x, 265)
		await create_timer(0.4).timeout
		r._resolve(false)
		await create_timer(0.5).timeout
		print("relic %d -> found=%d  note='%s'" % [i+1, m.recognition, h._note.text])
	quit()
