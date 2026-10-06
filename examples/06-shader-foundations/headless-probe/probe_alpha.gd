extends SceneTree
func _initialize() -> void:
	for f in ["sails_diff", "hull_diff", "rigging_diff"]:
		var img := Image.load_from_file(ProjectSettings.globalize_path("res://polyhaven/textures/dutch_ship_medium_%s_1k.jpg" % f))
		print(f, " format=", img.get_format(), " (FORMAT_RGB8=", Image.FORMAT_RGB8, ") detect_alpha=", img.detect_alpha(), " (ALPHA_NONE=", Image.ALPHA_NONE, ")")
	var ship: Node = (load("res://polyhaven/dutch_ship_medium_1k.gltf") as PackedScene).instantiate()
	for mi in ship.find_children("*", "MeshInstance3D", true, false):
		var m: BaseMaterial3D = mi.mesh.surface_get_material(0)
		if m.resource_name.ends_with("sails"):
			print("sails transparency=", m.transparency, " (ALPHA_SCISSOR=", BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR, ") threshold=", m.alpha_scissor_threshold, " albedo_color.a=", m.albedo_color.a)
	ship.free()
	quit(0)
