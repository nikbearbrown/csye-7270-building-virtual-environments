extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var mb = s.get_node("MusicBox")
	await create_timer(0.4).timeout
	s.flip(); await create_timer(1.4).timeout
	p.global_position = Vector2(5340, 265)
	await create_timer(0.6).timeout
	print("player=", p.global_position, " layer=", p.collision_layer)
	print("box=", mb.global_position, " mask=", mb.collision_mask, " monitoring=", mb.monitoring)
	print("shape disabled=", mb.get_node("CollisionShape2D").disabled, " radius=", mb.get_node("CollisionShape2D").shape.radius)
	print("overlapping=", mb.get_overlapping_bodies(), " inside=", mb._player_inside)
	quit()
