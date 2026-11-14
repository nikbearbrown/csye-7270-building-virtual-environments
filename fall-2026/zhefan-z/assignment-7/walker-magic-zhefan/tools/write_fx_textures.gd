extends SceneTree
## Writes the two Effect A particle textures (CHANGE-BRIEF Effect A settings), white so the colour ramps tint them:
##   res://assets/textures/fx/spark.png  4x4, opaque with the four corners at alpha 0.35 (a rounded dot)
##   res://assets/textures/fx/smoke.png  12x12 soft disc, alpha falling from 1 at the centre to 0 at radius 6
## From fall-2026/zhefan-z/assignment-6/:
##   Godot_v4.7.2-stable_win64_console.exe --headless --path walker-magic-zhefan --script res://tools/write_fx_textures.gd

const SPARK := "res://assets/textures/fx/spark.png"
const SMOKE := "res://assets/textures/fx/smoke.png"
const SPARK_CORNER_ALPHA := 0.35
const SMOKE_SIZE := 12


func _initialize() -> void:
	var dir_err := DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(SPARK.get_base_dir()))

	var spark := Image.create(4, 4, false, Image.FORMAT_RGBA8)
	spark.fill(Color.WHITE)
	for c: Vector2i in [Vector2i(0, 0), Vector2i(3, 0), Vector2i(0, 3), Vector2i(3, 3)]:
		spark.set_pixelv(c, Color(1, 1, 1, SPARK_CORNER_ALPHA))

	var smoke := Image.create(SMOKE_SIZE, SMOKE_SIZE, false, Image.FORMAT_RGBA8)
	var centre := Vector2(SMOKE_SIZE, SMOKE_SIZE) / 2.0
	for y in SMOKE_SIZE:
		for x in SMOKE_SIZE:
			var d := (Vector2(x, y) + Vector2(0.5, 0.5)).distance_to(centre) / (SMOKE_SIZE / 2.0)
			smoke.set_pixel(x, y, Color(1, 1, 1, smoothstep(1.0, 0.0, d)))

	var errs := [spark.save_png(SPARK), smoke.save_png(SMOKE)]
	for path: String in [SPARK, SMOKE]:
		var back := Image.load_from_file(path)
		var alphas := []
		for x in back.get_width():
			alphas.append(snappedf(back.get_pixel(x, back.get_height() / 2).a, 0.01))
		print("wrote %s: dir %s, save %s; read back %dx%d format %d, middle-row alpha %s" % [path, error_string(dir_err),
			error_string(errs[[SPARK, SMOKE].find(path)]), back.get_width(), back.get_height(), back.get_format(), alphas])
	quit(0 if errs.all(func(e: int) -> bool: return e == OK) else 1)
