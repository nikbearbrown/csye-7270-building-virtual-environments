extends SceneTree
## S7 — the slice's automated sound check (Assignment 2: "counting sound triggers per event during a
## scripted input sequence"; CHANGE-BRIEF predicted failure case 4).
##   Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_sound_triggers.gd
## Counts play requests through AudioDirector.played and checks each against the game event that
## should have caused it: exactly one sound per occurrence, including rapid repeats, a held input and
## same-frame duplicates. Headless uses a dummy audio driver: this proves the triggers, not what is heard.

const GROUND_TOP := 327.0

var main: Node
var player: Player
var audio: AudioDirector
var wolf: Wolf
var results: Array[Dictionary] = []
var failures := 0
var sounds := {}
var events := {}


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


func fresh(x: float, muted := false) -> void:
	if is_instance_valid(main):
		main.queue_free()
		await process_frame
	paused = false
	for b in ["Music", "SFX"]:
		AudioServer.set_bus_mute(AudioServer.get_bus_index(b), muted)
	main = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	sounds = {}
	events = {"cast": 0, "hurt": 0, "wolf_down": 0, "fail": 0, "clear": 0}
	root.add_child(main)
	player = main.player
	audio = main.audio
	wolf = main.get_node("Level/Wolf")
	player.use_scripted = true
	player.global_position = Vector2(x, GROUND_TOP)
	for id: String in AudioDirector.SFX_IDS + ["MUS-LOOP"]:
		sounds[id] = audio.plays[id]   # MUS-LOOP already started on load
	audio.played.connect(func(id: String) -> void: sounds[id] += 1)
	player.cast_fired.connect(func(_o: Vector2, _d: Vector2) -> void: events.cast += 1)
	player.hurt.connect(func(_hp: int) -> void: events.hurt += 1)
	player.failed.connect(func(_r: String) -> void: events.fail += 1)
	player.cleared.connect(func() -> void: events.clear += 1)
	wolf.defeated.connect(func() -> void: events.wolf_down += 1)
	await steps(2)


func shoot_wolf_point_blank() -> void:
	var fb: Fireball = Player.FIREBALL.instantiate()
	fb.direction = Vector2.RIGHT
	fb.position = wolf.global_position + Vector2(-40, -14)
	main.add_child(fb)


## The scripted route through the whole slice: run, jump the pit, shoot the (real, patrolling) wolf
## until it is defeated, walk into the exit. Returns the end state for the muted comparison.
func play_route(muted: bool) -> Dictionary:
	await fresh(60, muted)
	player.scripted.move = 1.0
	var frames := 0
	while player.global_position.x < 506.0 and frames < 600:
		await physics_frame
		frames += 1
	player.scripted.jump_pressed = true
	player.scripted.jump_held = true
	while (player.global_position.x < 620.0 or not player.is_on_floor()) and frames < 900:
		await physics_frame
		frames += 1
	player.scripted.move = 0.0
	player.scripted.jump_held = false
	while is_instance_valid(wolf) and not wolf.dead and frames < 1500:
		player.scripted.aim = wolf.global_position + Vector2(0, -14)
		player.scripted.cast_pressed = true
		await physics_frame
		frames += 1
	await steps(45)   # the down image is held, then the wolf disappears
	player.scripted.move = 1.0
	while not main.cleared and frames < 2400:
		await physics_frame
		frames += 1
	await steps(10)
	return {"frames": frames, "x": snappedf(player.global_position.x, 0.01), "hp": player.hp,
		"cleared": main.cleared, "failed": player.is_failing, "events": events.duplicate(), "sounds": sounds.duplicate()}


func one_per_event(tag: String, expect: Dictionary) -> void:
	# expect: sound id -> [game event key, expected count]
	var ok := true
	var table := {}
	for id: String in expect:
		var ev: String = expect[id][0]
		var want: int = expect[id][1]
		table[id] = {"sound_plays": sounds[id], "game_events": events[ev], "expected": want}
		ok = ok and sounds[id] == events[ev] and sounds[id] == want
	check(tag, ok, table)


func run() -> void:
	Controls.ensure()

	# 1. Full scripted route (sound on).
	var on := await play_route(false)
	var casts: int = on.events.cast
	one_per_event("route-one-sound-per-event", {
		"SFX-CAST": ["cast", casts], "SFX-WOLF-DOWN": ["wolf_down", 1], "SFX-HURT": ["hurt", 0],
		"SFX-FAIL": ["fail", 0], "SFX-CLEAR": ["clear", 1]})
	check("route-completes-music-started-once-then-stopped", on.cleared and not on.failed and sounds["MUS-LOOP"] == 1
		and not audio.music.playing and casts >= 2,
		{"cleared": on.cleared, "casts_needed": casts, "music_starts": sounds["MUS-LOOP"], "frames": on.frames})

	# 2. The same route with both buses muted: identical game state and identical trigger counts.
	var off := await play_route(true)
	check("muted-route-identical", JSON.stringify(on) == JSON.stringify(off), {"sound_on": on, "muted": off})
	for b in ["Music", "SFX"]:
		AudioServer.set_bus_mute(AudioServer.get_bus_index(b), false)

	# 3. SFX-CAST: a held button fires once; tapping every other frame is limited by the cooldown.
	await fresh(200)
	player.use_scripted = false
	Input.action_press("cast")
	await steps(120)
	Input.action_release("cast")
	await steps(5)
	one_per_event("cast-held-2s-plays-once", {"SFX-CAST": ["cast", 1]})
	await fresh(200)
	player.use_scripted = false
	for i in 120:
		if i % 2 == 0:
			Input.action_press("cast")
		else:
			Input.action_release("cast")
		await physics_frame
	Input.action_release("cast")
	one_per_event("cast-tapping-2s-cooldown-limited", {"SFX-CAST": ["cast", 6]})

	# 4. SFX-WOLF-DOWN: two fireballs into a 1 HP wolf in the same frame.
	await fresh(100)
	wolf.set_physics_process(false)
	wolf.hp = 1
	shoot_wolf_point_blank()
	shoot_wolf_point_blank()
	await steps(20)
	one_per_event("wolf-down-two-fireballs-same-frame", {"SFX-WOLF-DOWN": ["wolf_down", 1]})

	# 5. SFX-HURT: two hits in the same frame and one inside the invulnerability window -> one sound;
	#    then real lunges for 4 s: one sound per landed hit, never more.
	await fresh(200)
	wolf.set_physics_process(false)
	player.take_damage(1, 260)
	player.take_damage(1, 260)
	await steps(20)
	player.take_damage(1, 260)
	one_per_event("hurt-same-frame-and-invulnerable-plays-once", {"SFX-HURT": ["hurt", 1]})
	await fresh(780, false)
	wolf.global_position.x = 860.0
	await steps(240)
	var lost := Tuning.MAX_HP - player.hp
	check("hurt-real-lunges-one-sound-per-landed-hit", sounds["SFX-HURT"] == events.hurt and events.hurt == lost and lost >= 1,
		{"sound_plays": sounds["SFX-HURT"], "hurt_events": events.hurt, "hp_lost": lost})

	# 6. SFX-FAIL: pit kill zone entered twice plus a lethal hit in the same frame -> one sound.
	await fresh(200)
	wolf.set_physics_process(false)
	player.hp = 1
	var pit: Area2D = main.get_node("Level/PitKillZone")
	pit.body_entered.emit(player)
	pit.body_entered.emit(player)
	player.take_damage(1, 260)
	await steps(5)
	one_per_event("fail-pit-twice-and-hp0-same-frame-plays-once", {"SFX-FAIL": ["fail", 1]})
	check("fail-stops-music", not audio.music.playing, {"music_playing": audio.music.playing})

	# 7. SFX-CLEAR: the exit entered twice -> one sound.
	await fresh(1180)
	var exit: Area2D = main.get_node("Level/Exit")
	exit.body_entered.emit(player)
	exit.body_entered.emit(player)
	await steps(5)
	one_per_event("clear-exit-twice-plays-once", {"SFX-CLEAR": ["clear", 1]})

	paused = false
	print("SOUND TRIGGERS (route): " + JSON.stringify({"casts": casts, "sounds": on.sounds, "events": on.events}))
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)
