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
	# A kind contact: recognition up, a day torn, frost deepens.
	var contact = scene.get_node("WorldRoot/MusicBox")
	contact._player_inside = true
	contact._resolve(false)
	await create_timer(1.4).timeout
	_shot("04-after-contact")
	# Spend the rest of the calendar to show the end state and heavy frost.
	scene.get_node("Meters").spend(5, 0)
	await create_timer(1.6).timeout
	_shot("05-anniversary-end")
	quit()

func _shot(name):
	root.get_viewport().get_texture().get_image().save_png("res://../evidence/%s.png" % name)
	print("saved ", name)
