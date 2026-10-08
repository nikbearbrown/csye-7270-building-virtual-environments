extends SceneTree
# Instructor's independent level probe for Chapter 12 (not written by the agent).
# Loads the real main scene, reads the bus layout, and measures what the SFX bus
# and Master actually carry when the real note_hit signal fires. Uses two
# AudioEffectCapture effects added at runtime (never saved). Run in REAL TIME:
#   godot --headless --path godot --script res://tests/verify_levels.gd

var cap_sfx := AudioEffectCapture.new()
var cap_master := AudioEffectCapture.new()

func db(x: float) -> float:
	return snappedf(linear_to_db(x), 0.01) if x > 0.0 else -200.0

func peak_of(cap: AudioEffectCapture) -> float:
	var m := 0.0
	for f in cap.get_buffer(cap.get_frames_available()):
		m = maxf(m, maxf(absf(f.x), absf(f.y)))
	return m

func meter(bus: String) -> float:
	var i := AudioServer.get_bus_index(bus)
	return snappedf(maxf(AudioServer.get_bus_peak_volume_left_db(i, 0), AudioServer.get_bus_peak_volume_right_db(i, 0)), 0.01)

func wait_ms(ms: int) -> void:
	var end := Time.get_ticks_msec() + ms
	while Time.get_ticks_msec() < end:
		await process_frame

func _initialize() -> void:
	run.call_deferred()

func run() -> void:
	print("driver=", AudioServer.get_driver_name())
	for i in AudioServer.bus_count:
		print("  bus ", i, " ", AudioServer.get_bus_name(i), " -> '", AudioServer.get_bus_send(i), "' volume_db=", AudioServer.get_bus_volume_db(i))
	var scene: Node = load("res://scenes/main/main.tscn").instantiate()
	root.add_child(scene)
	current_scene = scene
	root.get_node("GlobalSettings").enable_metronome = false
	var sfx := AudioServer.get_bus_index("SFX")
	var music := AudioServer.get_bus_index("Music")
	AudioServer.add_bus_effect(sfx, cap_sfx)
	AudioServer.add_bus_effect(0, cap_master)
	await wait_ms(1500)
	var song: AudioStreamPlayer = scene.get_node("Player")
	print("song on bus ", song.bus, ": playing=", song.playing, " position=", snappedf(song.get_playback_position(), 0.001), " s; Music meter=", meter("Music"), " dB")
	var hit: AudioStreamPlayer = scene.get_node("HitSound")
	print("HitSound: bus=", hit.bus, " max_polyphony=", hit.max_polyphony, " stream length=", snappedf(hit.stream.get_length(), 0.0001), " s")
	AudioServer.set_bus_mute(music, true)  # Master now carries SFX only
	await wait_ms(200)
	for muted in [false, true]:
		AudioServer.set_bus_mute(sfx, muted)
		cap_sfx.clear_buffer(); cap_master.clear_buffer()
		scene.get_node("Notes").note_hit.emit(0.0, 2, 0.0)  # 2 == Enums.HitType.PERFECT
		var meter_max := -200.0
		var t := Time.get_ticks_msec()
		while Time.get_ticks_msec() - t < 250:
			await process_frame
			meter_max = maxf(meter_max, meter("SFX"))
		print("SFX muted=", muted, ": SFX capture peak ", db(peak_of(cap_sfx)), " dBFS, Master capture peak ", db(peak_of(cap_master)), " dBFS, SFX meter max seen ", meter_max, " dB")
	for miss in [0, 4]:  # MISS_EARLY, MISS_LATE
		AudioServer.set_bus_mute(sfx, false)
		cap_sfx.clear_buffer()
		scene.get_node("Notes").note_hit.emit(0.0, miss, 0.2)
		await wait_ms(250)
		print("note_hit type ", miss, " (miss): SFX capture peak ", db(peak_of(cap_sfx)), " dBFS")
	AudioServer.set_bus_mute(music, false)
	AudioServer.remove_bus_effect(0, AudioServer.get_bus_effect_count(0) - 1)
	AudioServer.remove_bus_effect(sfx, AudioServer.get_bus_effect_count(sfx) - 1)
	scene.get_node("Conductor").stop()
	hit.stop()
	await wait_ms(200)
	scene.queue_free()
	await process_frame
	await process_frame
	quit(0)
