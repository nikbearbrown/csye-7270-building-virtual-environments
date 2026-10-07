extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	await create_timer(0.5).timeout
	var a = s.get_node("Audio")
	print("missing files: ", a.missing)
	print("master bus volume: ", AudioServer.get_bus_volume_db(0), "  muted: ", AudioServer.is_bus_mute(0))
	for e in ["flip","contact","frost","correct","land","jump"]:
		var pl = a.get_node("sfx_%s" % e)
		a.play(e)
		await create_timer(0.12).timeout
		print("  %-8s stream=%s  vol=%.1f dB  playing=%s" % [e, pl.stream != null, pl.volume_db, pl.playing])
	quit()
