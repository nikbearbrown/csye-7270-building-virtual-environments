extends SceneTree
func _init():
	await process_frame
	var s = load("res://scenes/Bedroom.tscn").instantiate()
	root.add_child(s)
	var p = s.get_node("Player"); var a = s.get_node("Audio"); var m = s.get_node("Meters")
	await create_timer(0.5).timeout
	print("idle texture height check:")
	var idle_h = _h(p._sprite.texture)
	Input.action_press("move_right"); await create_timer(0.6).timeout
	var walk_h = _h(p._sprite.texture)
	Input.action_release("move_right")
	print("   idle=", idle_h, "  walking=", walk_h, "  difference=", abs(idle_h-walk_h), "px")
	print("heart at 7 days: ", snapped(a._heart.volume_db,0.1), " dB  rate=", a._heart_rate)
	m.spend(3,0); await create_timer(0.3).timeout
	print("heart at 4 days: ", snapped(a._heart.volume_db,0.1), " dB  rate=", snapped(a._heart_rate,0.01))
	m.spend(3,0); await create_timer(0.3).timeout
	print("heart at 1 day : ", snapped(a._heart.volume_db,0.1), " dB  rate=", snapped(a._heart_rate,0.01))
	quit()

func _h(tex):
	var im = tex.get_image(); var top=-1; var bot=-1
	for y in im.get_height():
		for x in im.get_width():
			if im.get_pixel(x,y).a > 0.35:
				if top < 0: top = y
				bot = y
				break
	return bot-top
