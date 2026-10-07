extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var a = s.get_node("Audio")
	await create_timer(0.6).timeout
	var relics = s.get_tree().get_nodes_in_group("relic")
	print("relics lit at the start: ", relics.filter(func(r): return r.get_node("Glow").visible).size(), " of ", relics.size())
	# ghost keeps a rhythm now
	s.flip(); await create_timer(1.5).timeout
	var g0 = a.counts["ghoststep"]
	Input.action_press("move_right"); await create_timer(1.5).timeout; Input.action_release("move_right")
	print("ghost moving 1.5s -> ghost strides=", a.counts["ghoststep"] - g0, "  real footsteps=", a.counts["step"])
	# answering one puts its light out
	var r = relics[0]
	p.global_position = Vector2(r.global_position.x, 265); await create_timer(0.5).timeout
	r._resolve(false); await create_timer(0.4).timeout
	print("after answering one -> lit relics remaining: ", relics.filter(func(x): return x.get_node("Glow").visible).size())
	quit()
