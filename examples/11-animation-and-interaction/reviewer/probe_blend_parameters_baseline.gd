extends SceneTree
# Reviewer probe (not given to the agent): records the AnimationTree parameters the
# player writes each physics frame, under normal scripted input. --fixed-fps 60.
var actions = ["move_forward", "move_back", "move_left", "move_right", "jump", "shoot", "reset_position"]
func _initialize():
	call_deferred("run")
func hold(desired: Array):
	for a in actions:
		if a in desired: Input.action_press(a)
		else: Input.action_release(a)
func run():
	var game = load("res://game.tscn").instantiate()
	root.add_child(game)
	current_scene = game
	var p = game.get_node("Player")
	var at: AnimationTree = p.get_node("AnimationTree")
	var plan := {}
	# frames are physics frames
	for f in range(0, 90): plan[f] = []
	for f in range(90, 150): plan[f] = ["move_forward"]
	for f in range(150, 210): plan[f] = ["move_back"]            # reversal
	for f in range(210, 330): plan[f] = ["jump"]                 # hold jump: re-jump on landing?
	for f in range(330, 360): plan[f] = []
	for f in range(360, 380): plan[f] = ["jump"]
	for f in range(380, 390): plan[f] = ["reset_position"]       # interrupt mid-jump
	for f in range(390, 480): plan[f] = []
	for f in range(480): 
		hold(plan[f])
		await physics_frame
		print("%3d in=%-16s floor=%s vy=%6.2f hs=%5.2f state=%.0f air_dir=%.2f run=%.2f speed=%.2f gun=%.2f" % [f, ",".join(plan[f]), p.is_on_floor(), p.velocity.y, Vector2(p.velocity.x, p.velocity.z).length(), at.get("parameters/state/blend_amount"), at.get("parameters/air_dir/blend_amount"), at.get("parameters/run/blend_amount"), at.get("parameters/speed/blend_amount"), at.get("parameters/gun/blend_amount")])
	hold([])
	game.process_mode = Node.PROCESS_MODE_DISABLED
	current_scene = null
	game.queue_free()
	await process_frame
	quit()
