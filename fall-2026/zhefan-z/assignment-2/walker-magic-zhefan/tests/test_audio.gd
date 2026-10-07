extends SceneTree
## Headless checks for S6: buses, routing, placeholders, the five event sounds, music behaviour on
## pause / fail / clear, and M / N mute. Headless uses a dummy audio driver: these checks count play
## requests and player state, not what a listener hears.
##   Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_audio.gd

const GROUND_TOP := 327.0

var main: Node
var player: Player
var audio: AudioDirector
var results: Array[Dictionary] = []
var failures := 0


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


func steps(n: int) -> void:
	for i in n:
		await physics_frame


func fresh(x: float) -> void:
	if is_instance_valid(main):
		main.queue_free()
		await process_frame
	paused = false
	main = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	player = main.player
	audio = main.audio
	player.use_scripted = true
	player.global_position = Vector2(x, GROUND_TOP)
	await steps(3)


func press(action: String) -> void:
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = true
	main.get_node("SessionInput")._unhandled_input(ev)


func counts() -> Dictionary:
	return audio.plays.duplicate()


func run() -> void:
	Controls.ensure()
	for b in ["Music", "SFX"]:
		AudioServer.set_bus_mute(AudioServer.get_bus_index(b), false)

	await fresh(200)
	check("buses-music-and-sfx", AudioServer.get_bus_index("Music") > 0 and AudioServer.get_bus_index("SFX") > 0,
		{"music_bus": AudioServer.get_bus_index("Music"), "sfx_bus": AudioServer.get_bus_index("SFX")})
	var routing := {}
	for p: AudioStreamPlayer in audio.get_children():
		routing[p.name] = String(p.bus)
	check("players-routed-to-buses", routing["MUS-LOOP"] == "Music" and routing["SFX-CAST"] == "SFX" and routing["SFX-CLEAR"] == "SFX",
		{"routing": routing})
	check("placeholders-in-use-until-oggs-exist", audio.placeholder.size() == 6
		and (audio.music.stream as AudioStreamWAV).loop_mode == AudioStreamWAV.LOOP_FORWARD,
		{"placeholders": audio.placeholder.keys(), "music_loop": (audio.music.stream as AudioStreamWAV).loop_mode})
	var fail_len := (audio.get_node("SFX-FAIL") as AudioStreamPlayer).stream.get_length()
	check("fail-sound-shorter-than-reload", fail_len < main.RELOAD_DELAY, {"sfx_fail_s": fail_len, "reload_s": main.RELOAD_DELAY})
	check("music-starts-on-load", audio.music.playing and audio.plays["MUS-LOOP"] == 1, {"playing": audio.music.playing})

	# Each event -> its own sound, once.
	player.scripted.aim = Vector2(400, 260)
	player.scripted.cast_pressed = true
	await steps(2)
	player.take_damage(1, 260)
	await steps(2)
	var c := counts()
	check("cast-and-hurt-each-play-once", c["SFX-CAST"] == 1 and c["SFX-HURT"] == 1 and c["SFX-WOLF-DOWN"] == 0,
		{"counts": c})
	var wolf: Wolf = main.get_node("Level/Wolf")
	wolf.take_damage(2)
	await steps(2)
	check("wolf-defeat-plays-once", counts()["SFX-WOLF-DOWN"] == 1, {"counts": counts()})

	# Pause: music pauses and resumes from the same point.
	press("pause")
	await steps(5)
	var paused_flag := audio.music.stream_paused
	press("pause")
	await steps(5)
	check("pause-pauses-and-resumes-music", paused_flag and not audio.music.stream_paused and audio.music.playing,
		{"paused_during": paused_flag, "playing_after": audio.music.playing})

	# Fail: music stops, SFX-FAIL once.
	player.fail("Fell into the dark", true)
	player.fail("again", true)
	await steps(2)
	check("fail-stops-music-plays-fail-once", not audio.music.playing and counts()["SFX-FAIL"] == 1, {"counts": counts()})

	# Clear: music stops, SFX-CLEAR once, then silence.
	await fresh(1180)
	player.scripted.move = 1.0
	await steps(90)
	player.win()
	check("clear-stops-music-plays-clear-once", main.cleared and not audio.music.playing and counts()["SFX-CLEAR"] == 1,
		{"counts": counts()})

	# Mute: M -> Music bus, N -> SFX bus; HUD note; bus mutes do not touch game state.
	await fresh(200)
	press("mute_music")
	var m_music: bool = main.is_bus_muted("Music")
	var m_sfx: bool = main.is_bus_muted("SFX")
	var text_m: String = main.hud.mute_text()
	press("mute_sfx")
	var text_both: String = main.hud.mute_text()
	check("m-mutes-music-n-mutes-sfx", m_music and not m_sfx and main.is_bus_muted("SFX")
		and text_m == "music off (M)" and text_both == "music off (M)  sfx off (N)",
		{"after_M": [m_music, m_sfx], "hud_after_M": text_m, "hud_after_N": text_both})
	press("mute_music")
	press("mute_sfx")
	check("m-and-n-toggle-back", not main.is_bus_muted("Music") and not main.is_bus_muted("SFX") and main.hud.mute_text() == "",
		{"music_muted": main.is_bus_muted("Music"), "sfx_muted": main.is_bus_muted("SFX")})

	# Same scripted run with both buses muted and unmuted: identical game state.
	var outcomes := []
	for muted in [false, true]:
		await fresh(400)
		for b in ["Music", "SFX"]:
			AudioServer.set_bus_mute(AudioServer.get_bus_index(b), muted)
		player.scripted.move = 1.0
		player.scripted.aim = Vector2(900, 300)
		for i in 180:
			if i % 25 == 0:
				player.scripted.cast_pressed = true
			if i == 60:
				player.scripted.jump_pressed = true
				player.scripted.jump_held = true
			await physics_frame
		var w := main.get_node_or_null("Level/Wolf")
		outcomes.append({"x": snappedf(player.global_position.x, 0.01), "hp": player.hp, "failed": player.is_failing,
			"wolf_hp": w.hp if w else -1, "casts": audio.plays["SFX-CAST"]})
	for b in ["Music", "SFX"]:
		AudioServer.set_bus_mute(AudioServer.get_bus_index(b), false)
	check("muted-run-identical-state", outcomes[0] == outcomes[1], {"unmuted": outcomes[0], "muted": outcomes[1]})

	paused = false
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)
