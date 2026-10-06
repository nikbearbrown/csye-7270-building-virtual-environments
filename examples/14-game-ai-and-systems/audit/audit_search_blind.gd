extends SceneTree
## Chapter-author probe (hand-written): while the guard is in Search, put the
## player in plain sight, 120 px away. Does either brain notice before Search
## ends? The prompt's spec said only "go to the last known position, wait 1.0 s,
## then return to Patrol"; it never said what to do if the player reappears.
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	root.size = Vector2i(1280, 720)
	for b in [0, 1]:
		var arena: Node = load("res://npc/guard_arena.tscn").instantiate()
		arena.get_node("Guard").brain = b
		root.add_child(arena)
		var guard: Node2D = arena.get_node("Guard")
		var player: Node2D = arena.get_node("Player")
		for i in 4:
			await physics_frame
		player.global_position = Vector2(280, 360)
		var f := 0
		while guard.mode != "Chase" and f < 240:
			await physics_frame
			f += 1
		player.global_position = Vector2(800, 600)
		f = 0
		while guard.mode != "Search" and f < 240:
			await physics_frame
			f += 1
		var entered: String = guard.mode
		# player steps back into plain sight, 120 px from the guard
		var frames_in_search_with_player_visible := 0
		var sequence: Array[String] = [guard.mode]
		for i in 360:
			player.global_position = guard.global_position + Vector2(0, 120)
			await physics_frame
			if guard.mode != sequence[-1]:
				sequence.append(guard.mode)
			if guard.mode == "Search":
				frames_in_search_with_player_visible += 1
			if guard.mode == "Chase":
				break
		print("brain=", ["FSM", "BT"][b], " entered=", entered, " mode_sequence_after_player_reappears=", sequence, " physics_frames_in_Search_with_player_120px_away=", frames_in_search_with_player_visible)
		arena.queue_free()
		await process_frame
	quit(0)
