extends SceneTree
# How fast do bus peak meters see a SHORT sound under the Dummy driver?
func pk(i: int) -> float:
	return snappedf(AudioServer.get_bus_peak_volume_left_db(i, 0), 0.01)
func tone(secs: float) -> AudioStreamWAV:
	var w := AudioStreamWAV.new(); w.format = AudioStreamWAV.FORMAT_16_BITS; w.mix_rate = 44100
	var n := int(secs * 44100); var d := PackedByteArray(); d.resize(n * 2)
	for i in n: d.encode_s16(i * 2, int(sin(TAU * 1500.0 * i / 44100.0) * 0.5 * 32767.0))
	w.data = d; return w
func _initialize() -> void:
	run.call_deferred()
func play_and_sample(p: AudioStreamPlayer, label: String) -> void:
	p.play()
	var t1 := Time.get_ticks_msec(); var log := []
	var mx := -200.0
	while Time.get_ticks_msec() - t1 < int(OS.get_cmdline_user_args()[0]):
		await process_frame
		var v := pk(1); mx = max(mx, v)
		log.append("%d:%s%s" % [Time.get_ticks_msec() - t1, v, "P" if p.playing else "-"])
	print(label, " max_seen=", mx, " | ", " ".join(log.filter(func(s): return not s.contains("-200.0")).slice(0, 6)))
func run() -> void:
	AudioServer.add_bus(1); AudioServer.set_bus_name(1, "SFX"); AudioServer.set_bus_send(1, "Master")
	var p := AudioStreamPlayer.new(); p.bus = &"SFX"; root.add_child(p)
	await create_timer(0.5).timeout
	p.stream = load("res://click.wav")
	await play_and_sample(p, "click.wav 60 ms (imported):")
	p.stream = tone(0.06)
	await play_and_sample(p, "generated 60 ms tone:     ")
	p.stream = tone(1.0)
	await play_and_sample(p, "generated 1 s tone:       ")
	p.stop(); await create_timer(0.2).timeout
	quit()
