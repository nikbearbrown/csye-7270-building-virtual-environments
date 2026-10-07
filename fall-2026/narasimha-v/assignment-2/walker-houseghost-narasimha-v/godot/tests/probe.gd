extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var m = s.get_node("Meters")
	await create_timer(0.6).timeout
	# run at the gap and jump near the edge, the way a player would
	p.global_position = Vector2(820, 815); await create_timer(0.4).timeout
	var d0 = m.days_left
	Input.action_press("move_right")
	for i in 400:
		await physics_frame
		if p.global_position.x > 1120:
			Input.action_press("jump"); break
	await create_timer(0.45).timeout
	Input.action_release("jump")
	await create_timer(1.4).timeout
	Input.action_release("move_right")
	print("jump at the edge -> x=", round(p.global_position.x), " days lost=", d0 - m.days_left, " (0 lost and past 1350 = cleared)")
	quit()
