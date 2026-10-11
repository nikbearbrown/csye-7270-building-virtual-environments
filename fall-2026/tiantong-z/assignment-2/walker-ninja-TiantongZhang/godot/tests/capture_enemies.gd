extends SceneTree
## Enemy captures for CHANGE-BRIEF revision 0.6.0 P16: enemies move every
## frame, so a missed repaint would leave them lethal while drawn where they
## used to be. That is the defect a playtest found in the traps (revision
## 0.5.1), and no state assertion can see it - only pixels can.
##
## Records each captured enemy's kind, live position and the camera, so
## scripts/check_enemy_visibility.py can look for its colour at the place the
## engine says it is, and confirm that place is NOT where it spawned.
const Game = preload("res://game/session.gd")
var game: Node2D
var output: String
var shots: Array = []

func _initialize() -> void:
	call_deferred("run")

func step() -> void:
	await physics_frame
	await process_frame

func capture(label: String, indices: Array) -> void:
	# The first version parked the player inside a patrol, so it died, respawned
	# at x=64 and reset every enemy - and the capture happily recorded a frame
	# of the spawn area. Assert the claim instead of trusting the setup.
	assert(game.state == Game.State.PLAYING,
		"%s: expected PLAYING, got state %d - the setup killed the player" % [label, game.state])
	assert(game.deaths == 0, "%s: %d death(s) before the capture" % [label, game.deaths])
	await RenderingServer.frame_post_draw
	var image := root.get_texture().get_image()
	assert(image.save_png(output + "/" + label + ".png") == OK)
	var listed: Array = []
	for i in indices:
		assert(game.enemy_alive[i], "%s: enemy %d is dead, nothing to see" % [label, i])
		listed.append({
			"index": i,
			"kind": game.enemy_kinds[i],
			"x": game.enemy_x[i],
			"y": game.enemy_anchor[i].y,
			"spawn_x": game.enemy_anchor[i].x,
			"size": [Game.enemy_size(game.enemy_kinds[i]).x, Game.enemy_size(game.enemy_kinds[i]).y],
		})
	shots.append({
		"label": label,
		"image_size": [image.get_width(), image.get_height()],
		"camera": [game.camera.position.x, game.camera.position.y],
		"enemies": listed,
	})
	print("captured %-18s camera=%.1f enemies=%s" % [label, game.camera.position.x, str(indices)])

## Park the player so the camera frames the section.
func settle_at(x: float, frames: int) -> void:
	game.player.position = Vector2(x, 320)
	game.player.test_axis = 0.0
	for i in range(frames):
		await step()

## Wait until the listed enemies are provably away from where they spawned.
## The checker needs this: an enemy sitting at its spawn x could be matched by
## a render frozen at startup, which is exactly the bug being tested for. The
## patrol is periodic, so without this the capture sometimes landed on a frame
## where an enemy had cycled back to within 1-2 px of its spawn.
func wait_until_moved(indices: Array, min_px: float) -> void:
	for attempt in range(600):
		var all_moved := true
		for i in indices:
			if absf(game.enemy_x[i] - game.enemy_anchor[i].x) < min_px:
				all_moved = false
		if all_moved:
			return
		await step()
	assert(false, "enemies never moved %.0f px from spawn" % min_px)

func run() -> void:
	output = ProjectSettings.globalize_path("res://../evidence/screens")
	DirAccess.make_dir_recursive_absolute(output)
	game = Game.new()
	game.test_mode = true
	root.add_child(game)
	for i in range(3):
		await step()
	game.start_session()
	game.player.test_control = true

	# Beat 04. x=1540 is on the same platform but LEFT of the slime's patrol
	# (1580..1690), so it frames both the slime and the horse without standing
	# in either one.
	await settle_at(1540.0, 45)
	await wait_until_moved([1, 2], 12.0)
	await capture("07-slime-and-horse", [1, 2])
	# Beat 05, viewed from the previous platform's right edge: 2040 is past the
	# 1850..1990 patrol and short of the 2132..2222 one.
	await settle_at(2040.0, 45)
	await wait_until_moved([5, 6], 12.0)
	await capture("08-contested-landings", [5, 6])
	# The slime riding the high-road plank. 1210 is the safe landing strip
	# between trap T1 and L1's edge, and its camera frames the plank.
	await settle_at(1210.0, 45)
	await wait_until_moved([0], 12.0)
	await capture("09-plank-slime", [0])

	var f := FileAccess.open(output + "/enemy-shots.json", FileAccess.WRITE)
	f.store_string(JSON.stringify({"engine": Engine.get_version_info().string, "shots": shots}, "  "))
	f.close()
	print("ENEMY CAPTURES: %d frames" % shots.size())
	game.queue_free()
	await process_frame
	quit()
