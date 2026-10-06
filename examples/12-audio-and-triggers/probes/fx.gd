extends SceneTree
func _initialize():
	var c := AudioEffectCompressor.new()
	print("compressor sidechain prop=", "sidechain" in c, " value=", c.sidechain)
	print("AudioStreamPlayer max_polyphony default=", AudioStreamPlayer.new().max_polyphony)
	quit()
