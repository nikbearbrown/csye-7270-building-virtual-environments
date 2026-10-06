extends SceneTree
# Reviewer probe: press Space (jump), then F (attack) while airborne. --fixed-fps 120.
func _initialize():
	call_deferred("run")
func key(code: int, down: bool):
	var e := InputEventKey.new()
	e.keycode = code
	e.pressed = down
	Input.parse_input_event(e)
func run():
	root.size = Vector2i(1280,720)
	var demo: Node = load("res://Demo.tscn").instantiate()
	root.add_child(demo)
	for i in 12: await process_frame
	var p: Node = demo.get_node("Player")
	var f: Node = p.get_node("StateMachine")
	var pivot: Node2D = p.get_node("BodyPivot")
	key(KEY_SPACE, true)
	for i in 160:
		await process_frame
		if i == 2: key(KEY_SPACE, false)
		if i == 20: key(KEY_F, true)
		if i == 22: key(KEY_F, false)
		var names := []
		for s in f.states_stack: names.append(s.name)
		if i % 4 == 0 or (i >= 18 and i <= 26):
			print("%3d state=%-8s stack=%-22s height=%.1f" % [i, f.current_state.name, ",".join(names), -pivot.position.y])
	demo.queue_free()
	await process_frame
	quit()
