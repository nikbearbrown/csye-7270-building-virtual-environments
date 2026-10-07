extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var h = s.get_node("HUD")
	var mb = s.get_node("MusicBox")
	while not p.controllable: await create_timer(0.1).timeout
	await create_timer(0.4).timeout
	print("A before moving    -> ", _c(h))
	Input.action_press("move_right"); await create_timer(0.6).timeout; Input.action_release("move_right")
	p.global_position.x = mb.global_position.x
	await create_timer(0.6).timeout
	print("B under the relic  -> ", _c(h), "   (F = it is up there, you are down here)")
	s.flip(); await create_timer(1.6).timeout
	print("C flipped, in reach-> ", _c(h), "   (E = take it)")
	mb._resolve(false); await create_timer(0.8).timeout
	print("D after taking it  -> ", _c(h), "   (gone, or pointing at the next one)")
	quit()

func _c(h):
	return "cue='%s' visible=%s alpha=%.2f" % [h._cue.text, h._cue.visible, h._cue.modulate.a]
