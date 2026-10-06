extends SceneTree

func tone(freq: float, secs: float, rate := 22050) -> AudioStreamWAV:
	var w := AudioStreamWAV.new()
	w.format = AudioStreamWAV.FORMAT_16_BITS
	w.mix_rate = rate
	var n := int(secs * rate)
	var data := PackedByteArray(); data.resize(n * 2)
	for i in n:
		data.encode_s16(i * 2, int(sin(TAU * freq * i / rate) * 0.5 * 32767.0))
	w.data = data
	w.loop_mode = AudioStreamWAV.LOOP_FORWARD
	w.loop_end = n
	return w

func _initialize() -> void:
	run.call_deferred()

func peak() -> float:
	return max(AudioServer.get_bus_peak_volume_left_db(0, 0), AudioServer.get_bus_peak_volume_right_db(0, 0))

func run() -> void:
	root.size = Vector2i(640, 480)
	var p2 := AudioStreamPlayer2D.new()
	p2.stream = tone(440, 1.0)
	p2.max_distance = 500
	root.add_child(p2)
	for pos in [Vector2(320, 240), Vector2(320 + 250, 240), Vector2(320 + 480, 240), Vector2(320 + 2000, 240)]:
		p2.position = pos
		if not p2.playing: p2.play()
		await create_timer(0.25).timeout
		print("2D at ", pos, " (dist from centre ", pos.distance_to(Vector2(320,240)), ") master peak L/R dB=", AudioServer.get_bus_peak_volume_left_db(0,0), " / ", AudioServer.get_bus_peak_volume_right_db(0,0))
	p2.stop()
	await create_timer(0.2).timeout
	var cam := Camera3D.new()
	root.add_child(cam)
	cam.make_current()
	var p3 := AudioStreamPlayer3D.new()
	p3.stream = tone(440, 1.0)
	p3.max_distance = 30
	root.add_child(p3)
	for z in [-2.0, -10.0, -29.0, -40.0]:
		p3.position = Vector3(0, 0, z)
		if not p3.playing: p3.play()
		await create_timer(0.25).timeout
		print("3D at z=", z, " master peak L/R dB=", AudioServer.get_bus_peak_volume_left_db(0,0), " / ", AudioServer.get_bus_peak_volume_right_db(0,0))
	p3.position = Vector3(5, 0, -5)
	await create_timer(0.25).timeout
	print("3D right of camera (5,0,-5): L/R dB=", AudioServer.get_bus_peak_volume_left_db(0,0), " / ", AudioServer.get_bus_peak_volume_right_db(0,0))
	p3.stop()
	await create_timer(0.25).timeout
	quit(0)
