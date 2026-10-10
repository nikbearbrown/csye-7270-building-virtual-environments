extends "res://tests/harness.gd"
const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")
var game

func fresh(seed_value: int, no_spawn: bool, silent: bool) -> void:
	if is_instance_valid(game):
		game.free()
	for bus in ["Master", "Music", "SFX"]:
		var i := AudioServer.get_bus_index(bus)
		if i >= 0:
			AudioServer.set_bus_mute(i, false)
	game = Session.new()
	game.test_mode = true
	game.test_no_spawn = no_spawn
	root.add_child(game)
	game.audio.disable_streams = silent
	if silent:
		AudioServer.set_bus_mute(AudioServer.get_bus_index("Master"), true)
	game.start_run(seed_value)

func autoplay(ticks: int) -> Dictionary:
	var counts := {"kill": 0, "pickup": 0, "hurt": 0, "levelup": 0, "evolve": 0}
	game.enemy_killed.connect(func(_p): counts["kill"] += 1)
	game.gem_collected.connect(func(_v): counts["pickup"] += 1)
	game.player_hurt.connect(func(_h): counts["hurt"] += 1)
	game.state.changed.connect(func(_f, t):
		if t == GS.LEVELUP:
			counts["levelup"] += 1)
	game.evolved.connect(func(): counts["evolve"] += 1)
	for t in ticks:
		if game.state.is_terminal():
			break
		if game.state.current == GS.LEVELUP:
			var pick: int = game.offered.find("sunflare")
			game.choose_card(maxi(pick, 0))
		var a := float(t) / 90.0
		game.test_axis = Vector2(cos(a), sin(a))
		game.tick()
	return counts

func summary() -> Dictionary:
	return {"state": GS.NAMES[game.state.current], "tick": game.tick_count, "kills": game.kills,
		"level": game.prog.level, "hp": game.player.hp, "x": snappedf(game.player.position.x, 0.01),
		"y": snappedf(game.player.position.y, 0.01), "enemies": game.enemies.size(), "evolved": game.prog.evolved_sunflare}

func plays(id: String) -> Array:
	return game.audio.play_log.filter(func(e): return e["id"] == id)

func min_gap_ms(id: String) -> int:
	var p := plays(id)
	var gap := 1 << 30
	for i in range(1, p.size()):
		gap = mini(gap, int(p[i]["ms"]) - int(p[i - 1]["ms"]))
	return gap

func run() -> void:
	suite = "audio"
	var ticks := Tuning.RUN_SECONDS * Tuning.TICK_HZ + 10
	fresh(11, false, false)
	var counts := autoplay(ticks)
	var loud := summary()
	check("once-levelup", plays("levelup").size() == counts["levelup"], {"plays": plays("levelup").size(), "events": counts["levelup"]})
	check("once-hurt", plays("hurt").size() == counts["hurt"], {"plays": plays("hurt").size(), "events": counts["hurt"]})
	check("once-evolve", plays("evolve").size() == counts["evolve"] and counts["evolve"] <= 1)
	check("kill-throttled", plays("kill").size() <= counts["kill"] and min_gap_ms("kill") >= 60, {"plays": plays("kill").size(), "kills": counts["kill"], "min_gap": min_gap_ms("kill")})
	check("pickup-merged", plays("pickup").size() <= counts["pickup"] and min_gap_ms("pickup") >= 80, {"plays": plays("pickup").size(), "events": counts["pickup"]})
	var stingers := plays("lose").size() + plays("win").size()
	check("one-stinger", stingers == (1 if game.state.is_terminal() else 0), {"state": loud["state"], "stingers": stingers})
	fresh(11, false, true)
	autoplay(ticks)
	var silent := summary()
	check("independence", loud == silent, {"with_sound": loud, "silent": silent})

	fresh(1, true, false)
	for c in ["beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius"]:
		game.prog.apply(c)
	game.prog.add_xp(3)
	game.tick()
	game.choose_card(game.offered.find("sunflare"))
	game.step_ticks(5)
	check("evolve-sfx-once", plays("evolve").size() == 1 and plays("levelup").size() == 1, {"evolve": plays("evolve").size()})

	# SFX-04 belongs to the card screen, not to the XP threshold (review finding)
	fresh(1, true, false)
	var opens: Array = []
	game.state.changed.connect(func(_f, t):
		if t == GS.LEVELUP:
			opens.append(game.tick_count))
	game.prog.add_xp(3 + 5)
	for i in 4:
		game.tick()
		if game.state.current == GS.LEVELUP:
			game.choose_card(0)
	var chimes: Array = plays("levelup").map(func(e): return e["tick"])
	check("levelup-sfx-on-card-screen", opens.size() == 2 and chimes == opens, {"card_screens_at": opens, "chimes_at": chimes})
	fresh(1, true, false)
	game.prog.xp = game.prog.xp_needed() - 1
	game.drop_gem(game.player.position, 1)
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 1
	game.tick()
	check("no-levelup-chime-when-run-ends", game.state.current == GS.WON and plays("levelup").is_empty() and plays("win").size() == 1, {"state": GS.NAMES[game.state.current], "levelup": plays("levelup").size()})

	# a restart must not carry the previous run's lose/win stinger into the new run (review finding)
	fresh(1, true, false)
	game.player.hp = 1
	var ws = game.spawn_enemy("wraith", game.player.position)
	ws.hp = 9999
	game.tick()
	var lose_ringing: bool = game.audio.pools["lose"].any(func(pl): return pl.playing)
	game.start_run(2)
	var still_ringing: bool = game.audio.pools["lose"].any(func(pl): return pl.playing) or game.audio.pools["win"].any(func(pl): return pl.playing)
	check("restart-silences-stingers", (lose_ringing or game.audio.streams.get("lose") == null) and not still_ringing, {"stinger_was_playing": lose_ringing, "after_restart": still_ringing})

	fresh(1, true, false)
	for i in 20:
		game.spawn_enemy("moth", Vector2(30 + i, 0))
	for e in game.enemies.duplicate():
		game.damage(e, 99)
	check("burst-20-kills-one-sfx", plays("kill").size() == 1, {"plays": plays("kill").size()})

	fresh(1, true, false)
	game.test_axis = Vector2.RIGHT
	game.audio.play_log.clear()
	game.step_ticks(100)
	check("hold-input-no-sfx", game.audio.play_log.is_empty())
	for i in 20:
		game.toggle_pause()
		game.tick()
	check("rapid-pause-no-sfx", game.audio.play_log.is_empty() and game.state.current == GS.PLAYING)

	var music := AudioServer.get_bus_index("Music")
	game.toggle_pause()
	check("pause-lowpass-and-duck", AudioServer.is_bus_effect_enabled(music, 0) and is_equal_approx(AudioServer.get_bus_volume_db(music), -10.0) and game.audio.music_state == "paused")
	game.toggle_pause()
	check("resume-restores", not AudioServer.is_bus_effect_enabled(music, 0) and is_equal_approx(AudioServer.get_bus_volume_db(music), 0.0) and game.audio.music_state == "playing")
	game.prog.add_xp(3)
	game.tick()
	check("levelup-duck", is_equal_approx(AudioServer.get_bus_volume_db(music), -6.0))
	game.choose_card(0)
	check("levelup-unduck", is_equal_approx(AudioServer.get_bus_volume_db(music), 0.0))

	var before := [game.state.current, game.tick_count]
	for bus in ["Master", "Music", "SFX"]:
		game.audio.toggle_bus(bus)
	check("mute-flags", game.audio.is_bus_muted("Master") and game.audio.is_bus_muted("Music") and game.audio.is_bus_muted("SFX"))
	check("mute-no-state-change", before == [game.state.current, game.tick_count])
	for bus in ["Master", "Music", "SFX"]:
		game.audio.toggle_bus(bus)

	game.player.hp = 1
	var w = game.spawn_enemy("wraith", game.player.position)
	w.hp = 9999
	game.tick()
	check("lost-fades", game.state.current == GS.LOST and game.audio.music_state == "fading" and plays("lose").size() == 1)
	await create_timer(0.8).timeout
	check("lost-stops", game.audio.music_state == "stopped")

	game.start_run(2)
	game.player.hp = 1
	var w2 = game.spawn_enemy("wraith", game.player.position)
	w2.hp = 9999
	game.tick()
	game.start_run(3)
	await create_timer(0.8).timeout
	check("restart-during-fade", game.audio.music_state == "playing" and is_equal_approx(AudioServer.get_bus_volume_db(music), 0.0) and (game.audio.base.stream == null or game.audio.base.volume_db > -1.0))

	game.toggle_pause()
	game.start_run(4)
	check("restart-from-pause", not AudioServer.is_bus_effect_enabled(music, 0) and is_equal_approx(AudioServer.get_bus_volume_db(music), 0.0) and game.audio.music_state == "playing")
	check("music-loop-flag", game.audio.base.stream == null or game.audio.base.stream.loop)
	completed = true
