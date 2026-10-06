extends SceneTree
func _initialize() -> void:
	print("default_texture_filter=", ProjectSettings.get_setting("rendering/textures/canvas_textures/default_texture_filter"))
	var w: AudioStreamWAV = load("res://s.wav")
	print("wav loop_mode=", w.loop_mode, " mix_rate=", w.mix_rate, " format=", w.format, " len=", w.get_length())
	print("LOOP_FORWARD=", AudioStreamWAV.LOOP_FORWARD, " FORMAT_QOA=", AudioStreamWAV.FORMAT_QOA)
	var o: AudioStreamOggVorbis = load("res://m.ogg")
	print("ogg loop=", o.loop, " offset=", o.loop_offset)
	var sf := SpriteFrames.new()
	print("SpriteFrames default anims=", sf.get_animation_names(), " speed=", sf.get_animation_speed("default"), " loop=", sf.get_animation_loop("default"))
	quit()
