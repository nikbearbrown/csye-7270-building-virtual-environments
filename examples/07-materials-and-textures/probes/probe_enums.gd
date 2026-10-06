extends SceneTree
func _initialize() -> void:
	print("TONE_MAPPER LINEAR=", Environment.TONE_MAPPER_LINEAR, " REINHARDT=", Environment.TONE_MAPPER_REINHARDT, " FILMIC=", Environment.TONE_MAPPER_FILMIC, " ACES=", Environment.TONE_MAPPER_ACES, " AGX=", Environment.TONE_MAPPER_AGX)
	var ctl: Node = (load("res://control.tscn") as PackedScene).instantiate()
	var we: WorldEnvironment = ctl.find_children("*", "WorldEnvironment", true, false)[0]
	print("control.tscn tonemap_mode=", we.environment.tonemap_mode, " ssao=", we.environment.ssao_enabled, " ssil=", we.environment.ssil_enabled, " sdfgi=", we.environment.sdfgi_enabled, " ambient_source=", we.environment.ambient_light_source, " background_mode=", we.environment.background_mode)
	ctl.free()
	for f in ["hull_nor_gl", "hull_diff", "hull_arm"]:
		var t: Texture2D = load("res://polyhaven/textures/dutch_ship_medium_%s_1k.jpg" % f)
		var img := t.get_image()
		print(f, " class=", t.get_class(), " size=", t.get_size(), " image=", img != null, " format=", img.get_format() if img else -1, " mipmaps=", img.has_mipmaps() if img else "n/a")
	print("FORMAT RGB8=", Image.FORMAT_RGB8, " RGBA8=", Image.FORMAT_RGBA8, " RG8=", Image.FORMAT_RG8, " RGTC_RG=", Image.FORMAT_RGTC_RG)
	quit(0)
