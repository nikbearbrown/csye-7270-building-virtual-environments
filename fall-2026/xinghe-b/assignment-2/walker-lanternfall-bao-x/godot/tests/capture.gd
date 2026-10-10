extends SceneTree
const Session = preload("res://game/session.gd")
const Tuning = preload("res://features/tuning.gd")
var game

func _initialize() -> void:
	call_deferred("_main")

func shot(name: String) -> void:
	await process_frame
	await process_frame
	var dir := ProjectSettings.globalize_path("res://../evidence/screens")
	DirAccess.make_dir_recursive_absolute(dir)
	root.get_texture().get_image().save_png("%s/%s.png" % [dir, name])
	print("saved ", name)

func _main() -> void:
	game = Session.new()
	game.test_mode = true
	game.test_no_spawn = true
	root.add_child(game)
	await shot("sb-P1")
	game.start_run(21)
	for p in game.player.POSES:
		game.player.set_override(p)
		await shot("pose-" + p)
	game.player.set_override("")
	await shot("sb-P2")
	game.spawn_enemy("moth", Vector2(90, 0))
	game.test_axis = Vector2.RIGHT
	game.step_ticks(20)
	await shot("sb-P3")
	game.prog.add_xp(3)
	game.tick()
	await shot("sb-P4")
	game.choose_card(0)
	var w = game.spawn_enemy("wraith", game.player.position + Vector2(8, 0))
	w.hp = 9999
	game.tick()
	await shot("sb-P5")
	w.queue_free(); game.enemies.erase(w)
	for c in ["beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius"]:
		game.prog.apply(c)
	game.prog.add_xp(game.prog.xp_needed())
	game.tick()
	game.choose_card(game.offered.find("sunflare"))
	for i in 12:
		game.spawn_enemy("moth", Vector2.from_angle(i * TAU / 12) * 150)
	game.step_ticks(Tuning.SUNFLARE_FIRST_DELAY + 8)
	await shot("sb-P6")
	game.player.hp = 1
	var w2 = game.spawn_enemy("wraith", game.player.position)
	w2.hp = 9999
	game.step_ticks(60)
	await shot("sb-P7")
	game.start_run(22)
	game.step_ticks(2)
	await shot("sb-P8")
	game.start_run(22)
	game.tick_count = Tuning.RUN_SECONDS * Tuning.TICK_HZ - 1
	game.tick()
	await create_timer(2.2).timeout
	await shot("sb-P9")
	quit()
