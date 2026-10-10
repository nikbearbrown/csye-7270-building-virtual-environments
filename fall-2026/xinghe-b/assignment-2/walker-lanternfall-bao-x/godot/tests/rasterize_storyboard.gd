extends SceneTree
## Rasterises the storyboard SVGs with Godot's own SVG loader (ThorVG) so they can sit next to game captures.
func _initialize() -> void:
	var src := ProjectSettings.globalize_path("res://../design/storyboard")
	var out := ProjectSettings.globalize_path("res://../evidence/storyboard-png")
	DirAccess.make_dir_recursive_absolute(out)
	for f in DirAccess.get_files_at(src):
		if f.ends_with(".svg"):
			var img := Image.new()
			var err := img.load_svg_from_buffer(FileAccess.get_file_as_bytes(src + "/" + f), 0.25)
			if err == OK:
				img.save_png(out + "/" + f.get_basename() + ".png")
				print("rasterised ", f, " ", img.get_size())
	quit()
