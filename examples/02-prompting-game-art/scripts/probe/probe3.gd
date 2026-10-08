extends SceneTree
func _initialize() -> void:
	var w: AudioStreamWAV = load("res://s.wav")
	print("loop_mode resource=", w.loop_mode, " begin=", w.loop_begin, " end=", w.loop_end)
	quit()
