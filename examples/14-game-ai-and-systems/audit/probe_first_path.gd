extends SceneTree
## Chapter-author probe: after a same-frame set_target(), on which physics_frame
## signal does the guard's agent first have a non-empty path, and when does it
## first move? Repeats 5 times in one process.
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	root.size = Vector2i(1280, 720)
	for trial in 5:
		var arena: Node = load("res://npc/guard_arena.tscn").instantiate()
		root.add_child(arena)
		var guard: CharacterBody2D = arena.get_node("Guard")
		var agent: NavigationAgent2D = guard.get_node("NavigationAgent2D")
		var start := guard.global_position
		guard.set_target(Vector2(1080, 360))
		var first_path := -1
		var first_move := -1
		for f in range(1, 61):
			await physics_frame
			if first_path == -1 and agent.get_current_navigation_path().size() > 0:
				first_path = f
			if first_move == -1 and guard.global_position.distance_to(start) > 0.01:
				first_move = f
			if first_move != -1:
				break
		print("trial=", trial, " first_path_frame=", first_path, " first_move_frame=", first_move)
		arena.queue_free()
		await process_frame
	quit(0)
