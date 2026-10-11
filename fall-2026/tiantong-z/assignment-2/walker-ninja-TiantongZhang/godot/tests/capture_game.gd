extends SceneTree
const Game = preload("res://game/session.gd")
const Route = preload("res://tests/route_driver.gd")
var game: Node2D
var output: String

func _initialize() -> void:
	call_deferred("run")

func step() -> void:
	await physics_frame
	await process_frame

func capture(label: String) -> void:
	await RenderingServer.frame_post_draw
	var error := root.get_texture().get_image().save_png(output + "/" + label + ".png")
	assert(error == OK)
	print("Captured rendered game viewport: " + label)

func run() -> void:
	output = ProjectSettings.globalize_path("res://../evidence/screens")
	DirAccess.make_dir_recursive_absolute(output)
	game = Game.new()
	game.test_mode = true
	root.add_child(game)
	for i in range(3): await step()
	await capture("01-menu")
	game.start_session()
	game.player.test_control = true
	game.player.test_axis = 1
	# Walk from a safe landing into the spike trigger, not an invented failure card.
	game.player.position = Vector2(275, 320)
	for i in range(90):
		await step()
		if game.state == Game.State.DYING: break
	assert(game.state == Game.State.DYING)
	await capture("02-failure")
	game.state = Game.State.MENU
	game.start_session()
	var route = Route.new()
	var gap_captured := false
	# 1400, not 900: the route needs 1219 ticks now that the level is 3072 px.
	for i in range(1400):
		route.step(game)
		await step()
		if not gap_captured and game.player.position.x > 463 and game.player.position.y < 300:
			await capture("03-jump")
			gap_captured = true
		if game.state != Game.State.PLAYING: break
	assert(game.state == Game.State.COMPLETE, "Input route did not complete")
	await capture("04-complete")
	# Trap visibility, at a FIXED camera position so the two frames differ only
	# by the spike. The trigger is one-way, so walking right to arm trap 0 and
	# then back to the same x leaves it risen. Added after a playtest found the
	# spike was lethal while still drawn underground.
	game.state = Game.State.MENU
	game.start_session()
	game.player.test_control = true
	game.player.position = Vector2(1020, 320)
	game.player.test_axis = 0.0
	for i in range(20):
		await step()
		if game.player.is_on_floor():
			break
	assert(game.trap_risen[0] == 0, "trap 0 should still be buried at x=1020")
	await capture("05-trap-buried")
	game.player.test_axis = 1.0
	for i in range(120):
		await step()
		if game.trap_risen[0] >= Game.TRAP_RISE_TICKS:
			break
	assert(game.trap_risen[0] == Game.TRAP_RISE_TICKS, "trap 0 never finished rising")
	game.player.test_axis = -1.0
	for i in range(120):
		await step()
		if game.player.position.x <= 1020.0:
			break
	game.player.test_axis = 0.0
	await step()
	assert(absf(game.player.position.x - 1020.0) < 6.0, "did not return to the capture spot")
	await capture("06-trap-risen")
	print("trap frames: buried and risen captured at camera x=%.1f" % game.camera.position.x)

	# C6 evidence. The assignment requires the slice to stay understandable with
	# all sound muted; that claim is only checkable if the player can SEE which
	# state they are in, so the indicator and the control line that advertises
	# the key are captured rather than asserted in prose.
	game.state = Game.State.MENU
	game.start_session()
	game.set_muted(true)
	for i in range(3):
		await step()
	await capture("10-muted")
	game.set_muted(false)

	print("VISUAL ROUTE: completed with %d deaths" % game.deaths)
	game.queue_free()
	await process_frame
	quit()
