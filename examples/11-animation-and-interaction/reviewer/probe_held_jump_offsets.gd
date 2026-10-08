extends SceneTree
# Reviewer trace: hold jump; print every physics tick around each landing. --fixed-fps 60.
func _initialize():
	call_deferred("run")
func run():
	var game = load("res://game.tscn").instantiate()
	root.add_child(game)
	current_scene = game
	var p = game.get_node("Player")
	var at: AnimationTree = p.get_node("AnimationTree")
	var offset := int(OS.get_cmdline_user_args()[0]) if OS.get_cmdline_user_args().size() > 0 else 0
	for i in 80 + offset: await physics_frame
	var pb = at.get("parameters/motion/playback")
	Input.action_press("jump")
	var land := -100
	for f in 440:
		await physics_frame
		var fl: bool = p.is_on_floor()
		if fl: land = f
		if f - land <= 16 and f > 5:
			print("%3d pframe=%d floor=%s vy=%6.2f current=%s fading_from=%s" % [f, Engine.get_process_frames(), fl, p.velocity.y, pb.get_current_node(), pb.get_fading_from_node()])
	Input.action_release("jump")
	game.process_mode = Node.PROCESS_MODE_DISABLED
	current_scene = null
	game.queue_free()
	await process_frame
	quit()
