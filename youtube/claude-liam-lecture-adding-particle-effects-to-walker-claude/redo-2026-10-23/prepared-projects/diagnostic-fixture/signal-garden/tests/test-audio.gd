extends SceneTree
var game: Node3D
var cap: AudioEffectCapture
var master: AudioEffectCapture
var failures := 0
var sfx: int
var amb: int
func _initialize() -> void: call_deferred("run")
func wait(seconds: float) -> void: await create_timer(seconds, true).timeout
func check(id: String, ok: bool, observed: Variant = "") -> void:
	print(JSON.stringify({"id":id,"pass":ok,"observed":observed}))
	if not ok: failures += 1
func peak(effect: AudioEffectCapture) -> float:
	var samples := effect.get_buffer(effect.get_frames_available())
	var result := 0.0
	for sample in samples: result = maxf(result, maxf(absf(sample.x), absf(sample.y)))
	return result
func clear() -> void:
	cap.clear_buffer()
	master.clear_buffer()
func event_check(name: String) -> void:
	await wait(0.3)
	var bus_peak := peak(cap)
	var master_peak := peak(master)
	check("captured-"+name, bus_peak > 0.0001, bus_peak)
	check("master-"+name, master_peak > 0.0001, master_peak)
func run() -> void:
	game = load("res://signal-garden/main.tscn").instantiate()
	root.add_child(game)
	sfx = AudioServer.get_bus_index("GardenSFX")
	amb = AudioServer.get_bus_index("GardenAmbience")
	AudioServer.set_bus_mute(amb, true)
	cap = AudioEffectCapture.new()
	cap.buffer_length = 4
	master = AudioEffectCapture.new()
	master.buffer_length = 4
	AudioServer.add_bus_effect(sfx, cap)
	AudioServer.add_bus_effect(0, master)
	await wait(0.3)
	clear()
	Input.action_press("garden_action")
	await wait(0.1)
	Input.action_release("garden_action")
	await wait(0.3)
	check("near-event-silent", peak(cap) == 0 and game.sound.counts.charge == 0)
	clear()
	Input.action_press("garden_right")
	await wait(0.66)
	Input.action_release("garden_right")
	await event_check("step")
	check("on-pad-via-input", absf(game.player.position.x + 2) < 0.3, game.player.position.x)
	clear()
	Input.action_press("garden_action")
	await event_check("charge")
	clear()
	await wait(0.4)
	await event_check("gate")
	Input.action_release("garden_action")
	check("held-action-once", game.sound.counts.charge == 1 and game.sound.counts.gate == 1, game.sound.counts)
	clear()
	Input.action_press("garden_right")
	await wait(2.15)
	Input.action_release("garden_right")
	await event_check("finish")
	check("finish-event-once", game.sound.counts.finish == 1)
	await wait(0.6)
	clear()
	AudioServer.set_bus_mute(sfx, true)
	Input.action_press("garden_reset")
	await wait(0.05)
	Input.action_release("garden_reset")
	await wait(0.4)
	check("muted-master-silent", peak(master) == 0)
	AudioServer.set_bus_mute(sfx, false)
	clear()
	Input.action_press("garden_reset")
	await wait(0.05)
	Input.action_release("garden_reset")
	await event_check("reset")
	AudioServer.set_bus_mute(amb, false)
	await wait(0.3)
	paused = true
	await wait(0.2)
	var pos: float = game.sound.ambience.get_playback_position()
	await wait(0.3)
	check("pause-freezes-long-loop", absf(game.sound.ambience.get_playback_position() - pos) < 0.01)
	paused = false
	await wait(0.3)
	check("resume-advances-loop", absf(game.sound.ambience.get_playback_position() - pos) > 0.05)
	for p in game.sound.players.values():
		check("routing-"+p.name, p.bus == "GardenSFX" and p.max_polyphony >= 1)
	game.sound.stop_all()
	await wait(0.3)
	check("stop-clears-all-events", not game.sound.ambience.playing and not game.sound.players.finish.playing)
	AudioServer.remove_bus_effect(sfx, 0)
	AudioServer.remove_bus_effect(0, 0)
	cap = null
	master = null
	game.queue_free()
	await wait(0.3)
	print("AUDIO FAILURES ", failures)
	quit(1 if failures else 0)
