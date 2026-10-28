extends SceneTree
## Writes the hint-experiment texture (CHANGE-BRIEF section 3): res://assets/textures/hint/greys_3x1.png,
## three opaque texels with greys 64, 128, 192 (RGB8, so no alpha channel).
## From fall-2026/zhefan-z/assignment-5/:
##   Godot_v4.7.2-stable_win64_console.exe --headless --path walker-magic-zhefan --script res://tools/write_hint_png.gd

const OUT := "res://assets/textures/hint/greys_3x1.png"
const GREYS := [64, 128, 192]


func _initialize() -> void:
	var img := Image.create(3, 1, false, Image.FORMAT_RGB8)
	for x in GREYS.size():
		img.set_pixel(x, 0, Color8(GREYS[x], GREYS[x], GREYS[x]))
	var dir_err := DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT.get_base_dir()))
	var err := img.save_png(OUT)
	var back := Image.load_from_file(OUT)
	var texels := []
	for x in back.get_width():
		texels.append(back.get_pixel(x, 0).to_html(false))
	print("wrote %s: dir %s, save %s; read back %dx%d format %d texels %s" % [OUT, error_string(dir_err),
		error_string(err), back.get_width(), back.get_height(), back.get_format(), texels])
	quit(0 if err == OK else 1)
