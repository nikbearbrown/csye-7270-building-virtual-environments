extends SceneTree

func tone(freq: float, secs: float, rate := 22050) -> AudioStreamWAV:
	var w := AudioStreamWAV.new()
	w.format = AudioStreamWAV.FORMAT_16_BITS
	w.mix_rate = rate
	w.stereo = false
	var n := int(secs * rate)
	var data := PackedByteArray()
	data.resize(n * 2)
	for i in n:
		var s := int(sin(TAU * freq * i / rate) * 0.5 * 32767.0)
		data.encode_s16(i * 2, s)
	w.data = data
	return w

func _initialize() -> void:
	run.call_deferred()

func run() -> void:
	print("audio driver=", AudioServer.get_driver_name() if AudioServer.has_method("get_driver_name") else "?", " mix_rate=", AudioServer.get_mix_rate(), " output_latency=", AudioServer.get_output_latency())
	print("output devices=", AudioServer.get_output_device_list(), " current=", AudioServer.output_device)
	# bus layout
	AudioServer.add_bus(1)
	AudioServer.set_bus_name(1, "SFX")
	AudioServer.set_bus_send(1, "Master")
	var cap := AudioEffectCapture.new()
	AudioServer.add_bus_effect(1, cap)
	print("bus_count=", AudioServer.bus_count, " SFX idx=", AudioServer.get_bus_index("SFX"))
	var p := AudioStreamPlayer.new()
	p.stream = tone(440, 1.0)
	p.bus = &"SFX"
	root.add_child(p)
	var finished_at := [-1]
	p.finished.connect(func(): finished_at[0] = Time.get_ticks_msec())
	await process_frame
	var t0 := Time.get_ticks_msec()
	p.play()
	print("after play(): playing=", p.playing, " pos=", p.get_playback_position())
	await create_timer(0.3).timeout
	var peakL := AudioServer.get_bus_peak_volume_left_db(1, 0)
	var frames := cap.get_frames_available()
	var buf := cap.get_buffer(frames)
	var maxabs := 0.0
	for f in buf:
		maxabs = max(maxabs, abs(f.x))
	print("at 0.3s wall: playing=", p.playing, " pos=", p.get_playback_position(), " SFX peakL_db=", peakL, " capture_frames=", frames, " captured_max_abs=", maxabs)
	await create_timer(1.2).timeout
	print("1s tone finished signal at ms=", finished_at[0] - t0 if finished_at[0] > 0 else -1, " playing=", p.playing)
	# Ogg: loop flag and position drift
	var ogg := load("res://song.ogg") as AudioStreamOggVorbis
	print("ogg loop=", ogg.loop, " length=", ogg.get_length(), " bpm=", ogg.bpm, " beat_count=", ogg.beat_count)
	var m := AudioStreamPlayer.new()
	m.stream = ogg
	root.add_child(m)
	m.play()
	var w0 := Time.get_ticks_usec()
	await create_timer(3.0).timeout
	var wall := (Time.get_ticks_usec() - w0) / 1e6
	print("ogg after wall ", wall, "s: pos=", m.get_playback_position(), " since_last_mix=", AudioServer.get_time_since_last_mix())
	# pause behaviour
	paused = true
	var pp := m.get_playback_position()
	await create_timer(1.0, true).timeout
	print("tree paused 1s: pos before=", pp, " after=", m.get_playback_position(), " playing=", m.playing, " stream_paused=", m.stream_paused)
	paused = false
	await create_timer(0.5).timeout
	print("unpaused 0.5s: pos=", m.get_playback_position())
	# polyphony
	var q := AudioStreamPlayer.new()
	q.stream = tone(880, 0.5)
	q.max_polyphony = 1
	root.add_child(q)
	q.play(); await process_frame; q.play(); await process_frame; q.play()
	await process_frame
	print("polyphony=1 after 3 plays: playing=", q.playing, " pos=", q.get_playback_position())
	q.max_polyphony = 4
	q.play(); await process_frame; q.play(); await process_frame; q.play()
	await process_frame
	print("polyphony=4 after 3 plays: playing=", q.playing, " has_stream_playback=", q.has_stream_playback())
	# bus mute / volume
	AudioServer.set_bus_mute(1, true)
	p.play()
	await create_timer(0.2).timeout
	print("muted SFX bus: playing=", p.playing, " peakL_db=", AudioServer.get_bus_peak_volume_left_db(1, 0))
	AudioServer.set_bus_mute(1, false)
	AudioServer.set_bus_volume_db(1, -12.0)
	await create_timer(0.2).timeout
	print("SFX at -12 dB: peakL_db=", AudioServer.get_bus_peak_volume_left_db(1, 0))
	m.stop(); p.stop(); q.stop()
	await create_timer(0.25).timeout
	quit(0)
