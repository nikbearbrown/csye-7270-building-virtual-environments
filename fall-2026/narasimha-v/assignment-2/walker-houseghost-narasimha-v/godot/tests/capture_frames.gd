extends SceneTree
func _init():
	await process_frame
	var scene = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(scene)
	for i in 15: await process_frame
	_shot("01-upright-ghost")
	scene.flip()
	for i in 20: await process_frame
	_shot("02-midflip")
	for i in 50: await process_frame
	_shot("03-inverted-remembered")
	print("player state after flip: ", scene.get_node("Player").state)
	quit()

func _shot(name):
	root.get_viewport().get_texture().get_image().save_png("res://../evidence/%s.png" % name)
	print("saved ", name)
