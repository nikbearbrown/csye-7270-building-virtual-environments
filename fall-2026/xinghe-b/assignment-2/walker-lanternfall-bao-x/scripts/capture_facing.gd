extends SceneTree
## In-engine screenshots of every pose facing LEFT, plain and with the F3 hurtbox drawn (player.show_collision),
## for the character-sheet comparison (TEST-REPORT §6, CHARACTER-SHEET R4).
##
## Lives outside godot/ so the slice's source stays at the film's revision. Copy it into an isolated copy of the
## project and run it there with a window (it reads the rendered frame):
##   git archive 8a6f988 godot | tar -x -C /tmp/lf && cp scripts/capture_facing.gd /tmp/lf/godot/
##   godot --headless --path /tmp/lf/godot --import --quit
##   godot --always-on-top --path /tmp/lf/godot --script res://capture_facing.gd
## Screens land in /tmp/lf/evidence/screens/ (pose-<pose>-left.png, pose-<pose>-left-hurtbox.png).
const Session = preload("res://game/session.gd")
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
	game.start_run(21)          # same seed and setup as godot/tests/capture.gd, so the shots line up with pose-*.png
	game.player.facing = -1     # what a left input sets (player.gd step(), FACING_DEADZONE)
	for p in game.player.POSES:
		game.player.set_override(p)
		await shot("pose-%s-left" % p)
		game.player.show_collision = true
		game.player.queue_redraw()
		await shot("pose-%s-left-hurtbox" % p)
		game.player.show_collision = false
	quit()
