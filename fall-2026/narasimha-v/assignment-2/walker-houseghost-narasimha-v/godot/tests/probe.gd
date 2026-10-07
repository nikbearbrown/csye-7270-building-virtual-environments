extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	await create_timer(0.1).timeout
	var a = s.get_node("Audio")
	var up = a.get_node("music_normal"); var inv = a.get_node("music_inverted")
	print("lengths: normal=", snapped(up.stream.get_length(),0.1), "s  inverted=", snapped(inv.stream.get_length(),0.1), "s")
	await create_timer(0.7).timeout
	print("start    -> normal playing=", up.playing, " pos=", snapped(up.get_playback_position(),0.01), " vol=", snapped(up.volume_db,0.1))
	s.flip(); await create_timer(0.7).timeout
	print("flipped  -> inverted playing=", inv.playing, " pos=", snapped(inv.get_playback_position(),0.01), " vol=", snapped(inv.volume_db,0.1), " | normal vol=", snapped(up.volume_db,0.1))
	s.flip(); await create_timer(0.8).timeout
	print("back     -> normal playing=", up.playing, " pos=", snapped(up.get_playback_position(),0.01), " (near 0 = restarted from the top)")
	quit()
