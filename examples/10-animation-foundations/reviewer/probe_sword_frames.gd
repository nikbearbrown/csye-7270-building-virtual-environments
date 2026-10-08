extends SceneTree
# Independent reviewer probe (not given to the agent). Run with --fixed-fps 120.
func _initialize():
	call_deferred("run")
func key(down: bool):
	var e := InputEventKey.new()
	e.keycode = KEY_F
	e.pressed = down
	Input.parse_input_event(e)
func row(i: int, sw: Node, ap: AnimationPlayer, f: Node) -> String:
	return "%3d anim=%-14s pos=%.4f vis=%s mon=%s input=%d ready=%s combo=%d state=%s rot=%.1f" % [i, ap.current_animation, ap.current_animation_position if ap.is_playing() else -1.0, sw.visible, sw.monitoring, sw.attack_input_state, sw.ready_for_next_attack, sw.combo_count, f.current_state.name, sw.rotation_degrees]
func run():
	root.size = Vector2i(1280,720)
	var demo: Node = load("res://Demo.tscn").instantiate()
	root.add_child(demo)
	for i in 12: await process_frame
	var f: Node = demo.get_node("Player/StateMachine")
	var sw: Node = demo.get_node("Player/BodyPivot/WeaponPivot/Offset/Sword")
	var ap: AnimationPlayer = sw.get_node("AnimationPlayer")
	print("PHASE single tap")
	key(true)
	for i in 70:
		await process_frame
		if i == 1: key(false)
		print(row(i, sw, ap, f))
	print("PHASE combo: tap at frame 20 of each swing")
	key(true)
	var t := 0
	for i in 200:
		await process_frame
		if i in [1, 21, 41]: key(false)
		if i in [20, 40]: key(true)
		print(row(i, sw, ap, f))
	demo.queue_free()
	await process_frame
	quit()
