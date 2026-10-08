extends SceneTree
## Captures in-engine evidence frames for TEST-REPORT.md.
##   godot --path . --script tests/capture_frames.gd
func _init():
	await process_frame
	var scene = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(scene)
	await create_timer(0.4).timeout
	_shot("01-upright-ghost")
	scene.flip()
	await create_timer(0.3).timeout
	_shot("02-midflip")
	await create_timer(0.8).timeout
	_shot("03-inverted-remembered")
	# Walk to the music box using the real input action, then contact it.
	var mb = scene.get_node("MusicBox")
	Input.action_press("move_right")
	for i in 300:
		await physics_frame
		if mb._player_inside: break
	Input.action_release("move_right")
	await create_timer(0.3).timeout
	_shot("04-at-the-music-box")
	mb._resolve(false)
	await create_timer(1.2).timeout
	_shot("05-after-contact")
	scene.get_node("Meters").spend(5, 0)
	await create_timer(1.8).timeout
	_shot("06-anniversary-end")
	quit()

func _shot(name):
	root.get_viewport().get_texture().get_image().save_png("res://../evidence/%s.png" % name)
	print("saved ", name)
