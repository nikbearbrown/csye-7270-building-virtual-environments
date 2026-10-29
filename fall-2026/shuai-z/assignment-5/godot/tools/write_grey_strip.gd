extends SceneTree
## Writes the hint experiment's texture (CHANGE-BRIEF.md section 4):
## assets/hint_experiment/grey_strip_3x1.png, three opaque grey texels with the
## values 64, 128 and 192 in every channel. It then reads the file back and
## prints each texel's 8-bit values, so the log shows what was written. Run
## once, from assignment-5/:
##   timeout 120 godot --headless --path godot --script res://tools/write_grey_strip.gd

const OUT := "res://assets/hint_experiment/grey_strip_3x1.png"
const VALUES := [64, 128, 192]


func _init() -> void:
	var image := Image.create_empty(VALUES.size(), 1, false, Image.FORMAT_RGB8)
	for x in VALUES.size():
		image.set_pixel(x, 0, Color8(VALUES[x], VALUES[x], VALUES[x]))
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT.get_base_dir()))
	var err := image.save_png(ProjectSettings.globalize_path(OUT))
	print("SAVED %s: %s" % [OUT, error_string(err)])
	var back := Image.load_from_file(ProjectSettings.globalize_path(OUT))
	if err != OK or back == null:
		quit(1)
		return
	for x in back.get_width():
		var c := back.get_pixel(x, 0)
		print("TEXEL %d: %d, %d, %d, alpha %d" % [x, c.r8, c.g8, c.b8, c.a8])
	quit(0)
