extends SceneTree
func _initialize():
	var p: Node = load("res://player/player.tscn").instantiate()
	root.add_child(p)
	var ap: AnimationPlayer = p.get_node("Player/AnimationPlayer")
	for lib in ap.get_animation_library_list():
		for n in ap.get_animation_library(lib).get_animation_list():
			var a: Animation = ap.get_animation(n if lib == "" else lib + "/" + n)
			print("anim '%s' lib='%s' length=%.3f loop=%d tracks=%d" % [n, lib, a.length, a.loop_mode, a.get_track_count()])
	var at: AnimationTree = p.get_node("AnimationTree")
	print("tree_root=", at.tree_root.get_class(), " callback_mode_process=", at.callback_mode_process, " root_motion_track=", at.root_motion_track)
	var bt: AnimationNodeBlendTree = at.tree_root
	for n in bt.get_node_list():
		var node = bt.get_node(n)
		var extra := ""
		if node is AnimationNodeAnimation: extra = str(node.animation)
		print("  node ", n, " : ", node.get_class(), " ", extra)
	p.queue_free()
	quit()
