extends SceneTree
## Loads imported textures the way a material does and prints what the import
## produced: the resource class, the size, the image format by name, and the
## mipmaps. It reads the textures and writes nothing.
##
## From assignment-5/, with the project's folder and the textures' res:// paths:
##   timeout 120 godot --headless --path godot --script "$PWD/evidence/headless-probe/probe_textures.gd" -- res://assets/textures/rock_01/rock_01_diff_1k.png


func _init() -> void:
	var formats := ClassDB.class_get_enum_constants(&"Image", &"Format")
	var paths := OS.get_cmdline_user_args()
	if paths.is_empty():
		printerr("PROBE usage: godot --headless --path <project> --script <this file> -- res://<texture> ...")
		quit(2)
		return
	for path in paths:
		var texture := load(path) as Texture2D
		if texture == null:
			printerr("PROBE %s: not loaded as a Texture2D" % path)
			continue
		var image := texture.get_image()
		if image == null:
			printerr("PROBE %s: %s %dx%d, no image readable here" % [path, texture.get_class(), texture.get_width(), texture.get_height()])
			continue
		var format: int = image.get_format()
		printerr("PROBE %s: %s %dx%d, format %s (%d), mipmaps %s (%d levels)" % [path.get_file(), texture.get_class(), image.get_width(), image.get_height(), formats[format] if format < formats.size() else "?", format, image.has_mipmaps(), image.get_mipmap_count()])
	printerr("PROBE done")
	quit(0)
