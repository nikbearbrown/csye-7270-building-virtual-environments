extends SceneTree
## Headless checks for S5: HUD hearts, fail texts, the exit and Cleared screen, R restart, Esc pause.
##   Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_flow.gd
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.

const GROUND_TOP := 327.0

var main: Node
var player: Player
var hud: Control
var results: Array[Dictionary] = []
var failures := 0
var clears := 0


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
	hud = main.hud
	player.use_scripted = true
	player.global_position = Vector2(x, GROUND_TOP)
	(main.get_node("Level/Wolf") as Node).set_physics_process(false)
	clears = 0
	player.cleared.connect(func() -> void: clears += 1)
	await steps(3)


func press(action: String) -> void:
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = true
	main.get_node("SessionInput")._unhandled_input(ev)


func run() -> void:
	Controls.ensure()

	await fresh(200)
	check("hud-starts-with-5-hearts", hud.hp == 5 and hud.max_hp == 5 and hud.message_text() == "", {"hp": hud.hp})
	player.take_damage(1, 260)
	await steps(1)
	check("hud-loses-a-heart-on-hit", hud.hp == 4, {"hud_hp": hud.hp, "player_hp": player.hp})

	await fresh(470)
	player.scripted.move = 1.0
	await steps(120)
	check("pit-fail-shows-reason", hud.message_text() == "Fell into the dark", {"text": hud.message_text()})

	await fresh(200)
	for i in 5:
		player.invulnerable = 0.0
		player.take_damage(1, 260)
	await steps(1)
	check("hp-zero-shows-reason-and-empty-hearts", hud.message_text() == "Out of HP" and hud.hp == 0,
		{"text": hud.message_text(), "hud_hp": hud.hp})

	# Exit: walk in -> win image, input stops, Cleared screen; entering again does nothing.
	await fresh(1180)
	player.scripted.move = 1.0
	var frames := 0
	while clears == 0 and frames < 120:
		await physics_frame
		frames += 1
	var x_at_clear := player.global_position.x
	await steps(30)
	check("exit-clears-once-with-win-image", clears == 1 and player.is_cleared and main.cleared
		and player.sprite.texture == Player.TEXTURES[Player.State.WIN] and hud.message_text() == "CLEARED",
		{"clears": clears, "text": hud.message_text(), "frames_to_exit": frames})
	check("input-stops-after-clear", absf(player.global_position.x - x_at_clear) < 0.5,
		{"moved_px": player.global_position.x - x_at_clear})
	player.win()
	main.get_node("Level/Exit").body_entered.emit(player)
	check("second-exit-entry-ignored", clears == 1, {"clears": clears})
	player.take_damage(1, 1300)
	player.fail("late")
	check("no-hurt-or-fail-after-clear", player.hp == 5 and not player.is_failing, {"hp": player.hp})
	press("pause")
	check("no-pause-after-clear", not paused and hud.message_text() == "CLEARED", {"paused": paused})
	press("restart")
	check("r-restarts-after-clear", main.restart_requested, {"restart_requested": main.restart_requested})

	# R does nothing before the end.
	await fresh(200)
	press("restart")
	check("r-ignored-during-play", not main.restart_requested, {"restart_requested": main.restart_requested})

	# Esc pause: tree paused, overlay shown, nothing moves; Esc again resumes.
	await fresh(200)
	player.scripted.move = 1.0
	press("pause")
	var x0 := player.global_position.x
	await steps(30)
	check("esc-pauses-and-freezes-play", paused and hud.message_text() == "PAUSED" and absf(player.global_position.x - x0) < 0.01,
		{"paused": paused, "text": hud.message_text(), "moved_px": player.global_position.x - x0})
	press("pause")
	await steps(30)
	check("esc-resumes", not paused and hud.message_text() == "" and player.global_position.x > x0 + 20.0,
		{"paused": paused, "moved_px": snappedf(player.global_position.x - x0, 0.1)})

	await fresh(470)
	player.scripted.move = 1.0
	await steps(120)
	press("pause")
	check("no-pause-after-fail", not paused, {"paused": paused})

	paused = false
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)
