extends SceneTree
const Game = preload("res://game/session.gd")
const Route = preload("res://tests/route_driver.gd")
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var game = Game.new()
	root.add_child(game)
	game.start_session()
	game.player.test_control = true
	for i in 3:
		await physics_frame
	var route := Route.new()
	var ticks := 0
	while game.state == Game.State.PLAYING and ticks < 900:
		route.step(game.player)
		await physics_frame
		await process_frame
		ticks += 1
	print("STATE ", game.state, " SAVED ", FileAccess.file_exists("user://best_time.json"), " TMP ", FileAccess.file_exists("user://best_time.json.tmp"), " BEST ", game.best_seconds)
	game.queue_free()
	await process_frame
	quit.call_deferred(0)
