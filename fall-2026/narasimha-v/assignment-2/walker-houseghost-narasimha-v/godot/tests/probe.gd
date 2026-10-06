extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	await create_timer(0.6).timeout
	var a = s.get_node("Audio")
	var up = a.get_node("music_upright"); var mem = a.get_node("music_memory")
	print("missing: ", a.missing)
	print("start      -> upright=", up.playing, " memory=", mem.playing)
	s.flip(); await create_timer(1.2).timeout
	print("inverted   -> upright=", up.playing, " memory=", mem.playing)
	s.flip(); await create_timer(1.2).timeout
	print("back up    -> upright=", up.playing, " memory=", mem.playing)
	a.set_music_muted(true); await create_timer(0.4).timeout
	print("M muted    -> upright=", up.playing, " memory=", mem.playing)
	a.set_music_muted(false); await create_timer(0.6).timeout
	print("M unmuted  -> upright=", up.playing, " memory=", mem.playing)
	quit()
