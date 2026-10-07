extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var m = s.get_node("Meters"); var a = s.get_node("Audio")
	await create_timer(0.6).timeout
	var relics = s.get_tree().get_nodes_in_group("relic")
	print("relics found: ", relics.size())
	for r in relics:
		print("   ", r.name, " at x=", round(r.global_position.x))
	s.flip(); await create_timer(1.5).timeout
	for r in relics:
		p.global_position = Vector2(r.global_position.x, 265)
		await create_timer(0.5).timeout
		var ok = r._available()
		if ok: r._resolve(false)
		await create_timer(0.4).timeout
		print("   touched ", r.name, " -> reachable=", ok, "  seen=", m.recognition, "/", m.RECOGNITION_TO_WIN, "  days=", m.days_left)
	print("ended=", m.ended, "   heart volume now ", snapped(a._heart.volume_db,0.1), " dB")
	quit()
