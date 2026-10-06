extends SceneTree
# Is AudioEffectCapture pre- or post-fader? Capture on SFX and on Master, with SFX muted.
func maxabs(cap: AudioEffectCapture) -> float:
	var b := cap.get_buffer(cap.get_frames_available()); var m := 0.0
	for f in b: m = maxf(m, absf(f.x))
	return m
func _initialize() -> void:
	run.call_deferred()
func run() -> void:
	AudioServer.add_bus(1); AudioServer.set_bus_name(1, "SFX"); AudioServer.set_bus_send(1, "Master")
	var cap_sfx := AudioEffectCapture.new(); AudioServer.add_bus_effect(1, cap_sfx)
	var cap_master := AudioEffectCapture.new(); AudioServer.add_bus_effect(0, cap_master)
	var p := AudioStreamPlayer.new(); p.bus = &"SFX"; p.stream = load("res://click.wav"); root.add_child(p)
	await create_timer(0.3).timeout
	for muted in [false, true]:
		for vol in [0.0, -12.0]:
			AudioServer.set_bus_mute(1, muted); AudioServer.set_bus_volume_db(1, vol)
			cap_sfx.clear_buffer(); cap_master.clear_buffer()
			p.play()
			var t := Time.get_ticks_msec()
			while Time.get_ticks_msec() - t < 250: await process_frame
			var s := maxabs(cap_sfx); var m := maxabs(cap_master)
			print("SFX muted=", muted, " SFX vol=", vol, " dB -> capture on SFX max=", snappedf(s, 0.0001), " (", snappedf(linear_to_db(s), 0.01), " dB), capture on Master max=", snappedf(m, 0.0001), " (", snappedf(linear_to_db(m) if m > 0 else -200.0, 0.01), " dB)")
	p.stop(); await create_timer(0.2).timeout
	quit()
