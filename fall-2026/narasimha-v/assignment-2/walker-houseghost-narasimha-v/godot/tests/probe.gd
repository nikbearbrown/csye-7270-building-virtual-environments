extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player")
	await create_timer(0.6).timeout
	p.global_position = Vector2(1900, 815); await create_timer(0.5).timeout
	print("A normal, walking at the shelf   -> stopped at x=", await _run(p, 200), " (2125 = blocked by the memory)")
	s.flip(); await create_timer(1.5).timeout
	print("B inverted, same place           -> reached x=", await _run(p, 320), " (past 2200 = the memory is gone)")
	p.global_position = Vector2(3100, 265); await create_timer(0.6).timeout
	print("C inverted, at the boxes         -> stopped at x=", await _run(p, 200), " (3290 = blocked by the present)")
	s.flip(); await create_timer(1.5).timeout
	p.global_position = Vector2(3100, 815); await create_timer(0.5).timeout
	print("D normal, same place             -> reached x=", await _run(p, 260), " (past 3400 = the boxes are not there)")
	quit()

func _run(p, frames):
	Input.action_press("move_right")
	for i in frames: await physics_frame
	Input.action_release("move_right"); await create_timer(0.2).timeout
	return round(p.global_position.x)
