extends SceneTree
func _initialize() -> void:
	for p in ProjectSettings.get_property_list():
		if p.name == "rendering/textures/canvas_textures/default_texture_filter":
			print(p.name, " hint_string=", p.hint_string, " value=", ProjectSettings.get_setting(p.name))
	quit()
