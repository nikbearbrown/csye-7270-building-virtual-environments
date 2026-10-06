extends SceneTree
# Does a short sound reach the bus at all under the Dummy driver? Capture the bus.
func tone(secs: float) -> AudioStreamWAV:
	var w := AudioStreamWAV.new(); w.format = AudioStreamWAV.FORMAT_16_BITS; w.mix_rate = 44100
	var n := int(secs * 44100); var d := PackedByteArray(); d.resize(n * 2)
	for i in n: d.encode_s16(i * 2, int(sin(TAU * 1500.0 * i / 44100.0) * 0.5 * 32767.0))
	w.data = d; return w
func _initialize() -> void:
	run.call_deferred()
func trial(p: AudioStreamPlayer, cap: AudioEffectCapture, s: AudioStream, label: String) -> void:
	cap.clear_buffer()
	p.stream = s
	p.play()
	var t := Time.get_ticks_msec(); var peaks := []
	while Time.get_ticks_msec() - t < 300:
		await process_frame
		peaks.append(AudioServer.get_bus_peak_volume_left_db(1, 0))
	var n := cap.get_frames_available(); var b := cap.get_buffer(n); var mx := 0.0; var nz := 0
	for f in b:
		mx = maxf(mx, absf(f.x))
		if absf(f.x) > 0.001: nz += 1
	print(label, " captured_frames=", n, " nonzero=", nz, " (", snappedf(nz / 44.1, 0.1), " ms) max_abs=", snappedf(mx, 0.0001), " max_peak_meter_db=", snappedf(peaks.max(), 0.01), " time_to_next_mix=", snappedf(AudioServer.get_time_to_next_mix(), 0.0001))
func run() -> void:
	AudioServer.add_bus(1); AudioServer.set_bus_name(1, "SFX"); AudioServer.set_bus_send(1, "Master")
	var cap := AudioEffectCapture.new(); cap.buffer_length = 1.0
	AudioServer.add_bus_effect(1, cap)
	var p := AudioStreamPlayer.new(); p.bus = &"SFX"; root.add_child(p)
	await create_timer(0.3).timeout
	await trial(p, cap, load("res://click.wav"), "click.wav 60 ms:")
	await trial(p, cap, tone(0.06), "tone 60 ms:     ")
	await trial(p, cap, tone(0.2), "tone 200 ms:    ")
	await trial(p, cap, tone(1.0), "tone 1 s:       ")
	p.stop(); await create_timer(0.2).timeout
	quit()
