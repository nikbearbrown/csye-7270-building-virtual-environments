extends SceneTree
func stats(path: String) -> void:
	var img := Image.load_from_file(ProjectSettings.globalize_path(path))
	img.convert(Image.FORMAT_RGB8)
	var w := img.get_width(); var h := img.get_height()
	var sum := Vector3.ZERO; var mn := Vector3(1,1,1); var mx := Vector3.ZERO
	var n := 0; var unit_ok := 0; var bz := 0
	for y in range(0, h, 4):
		for x in range(0, w, 4):
			var c := img.get_pixel(x, y)
			var v := Vector3(c.r, c.g, c.b)
			sum += v; mn = mn.min(v); mx = mx.max(v); n += 1
			var nv := v * 2.0 - Vector3.ONE
			if absf(nv.length() - 1.0) < 0.1: unit_ok += 1
			if c.b > 0.5: bz += 1
	print(path.get_file(), " size=", w, "x", h, " mean=", (sum / n).snapped(Vector3(0.001,0.001,0.001)), " min=", mn.snapped(Vector3(0.001,0.001,0.001)), " max=", mx.snapped(Vector3(0.001,0.001,0.001)), " unit_len_within_0.1=", snappedf(float(unit_ok)/n, 0.001), " blue_gt_half=", snappedf(float(bz)/n, 0.001))
func _initialize() -> void:
	for part in ["hull", "rigging", "sails"]:
		for kind in ["diff", "arm", "nor_gl"]:
			stats("res://polyhaven/textures/dutch_ship_medium_%s_%s_1k.jpg" % [part, kind])
	quit(0)
