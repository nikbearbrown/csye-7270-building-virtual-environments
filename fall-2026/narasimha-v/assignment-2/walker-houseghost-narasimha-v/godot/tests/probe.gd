extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player")
	await create_timer(0.3).timeout
	var floor_y = p.global_position.y

	# jump height from a standstill
	Input.action_press("jump")
	await create_timer(0.35).timeout
	Input.action_release("jump")
	var peak = floor_y
	for i in 120:
		await physics_frame
		peak = minf(peak, p.global_position.y)
		if p.is_on_floor() and i > 10: break
	print("floor y=", floor_y, "  peak y=", round(peak), "  rise=", round(floor_y - peak), " px")

	# can he land on the boxes?
	p.global_position = Vector2(1125, 940)
	await physics_frame
	Input.action_press("jump")
	await create_timer(0.35).timeout
	Input.action_release("jump")
	await create_timer(1.2).timeout
	print("after jump at box x: y=", round(p.global_position.y), " on_floor=", p.is_on_floor(), " (730 = standing on boxes)")

	# same spot once the world is inverted: the boxes should not be there
	s.flip(); await create_timer(1.0).timeout
	p.global_position = Vector2(1125, 600)
	await create_timer(1.0).timeout
	print("inverted, dropped at box x: y=", round(p.global_position.y), " (940 = fell through to the floor)")
	quit()
