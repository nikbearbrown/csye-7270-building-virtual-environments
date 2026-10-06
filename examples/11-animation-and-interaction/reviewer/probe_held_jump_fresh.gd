extends SceneTree
# Reviewer trace: hold jump for three hops; print every physics tick. --fixed-fps 60.
func _initialize():
	call_deferred("run")
func run():
	var game = load("res://game.tscn").instantiate()
	root.add_child(game)
	current_scene = game
	var p = game.get_node("Player")
	var at: AnimationTree = p.get_node("AnimationTree")
	for i in 80: await physics_frame
	var pb = at.get("parameters/motion/playback")
	Input.action_press("jump")
	var prev_floor := true
	for f in 320:
		await physics_frame
		var fl: bool = p.is_on_floor()
		var s = pb.get_current_node() if pb else "n/a"
		var mark := ""
		if fl != prev_floor: mark = "  <-- floor " + ("contact" if fl else "left")
		if fl or (p.velocity.y > 0 and s == "fall") or mark != "" or f % 10 == 0:
			print("%3d frame=%d floor=%s vy=%6.2f state=%s%s" % [f, Engine.get_process_frames(), fl, p.velocity.y, s, mark])
		prev_floor = fl
	Input.action_release("jump")
	game.process_mode = Node.PROCESS_MODE_DISABLED
	current_scene = null
	game.queue_free()
	await process_frame
	quit()
