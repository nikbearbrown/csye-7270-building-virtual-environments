extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var a = s.get_node("Audio")
	await create_timer(0.6).timeout
	print("missing: ", a.missing)

	# walking in the memory: footsteps, no drift
	var s0 = a.counts["step"]
	Input.action_press("move_right"); await create_timer(1.6).timeout; Input.action_release("move_right")
	await create_timer(0.3).timeout
	print("memory, walked 1.6s -> footsteps=", a.counts["step"] - s0, "  drift playing=", a._drift.playing)

	# as the ghost: no footsteps at all, air instead
	s.flip(); await create_timer(1.5).timeout
	var s1 = a.counts["step"]
	Input.action_press("move_right"); await create_timer(1.2).timeout
	print("ghost, moving      -> footsteps=", a.counts["step"] - s1, "  drift playing=", a._drift.playing)
	Input.action_release("move_right"); await create_timer(0.6).timeout
	print("ghost, stopped     -> drift playing=", a._drift.playing, " (false = air stops with him)")
	quit()
