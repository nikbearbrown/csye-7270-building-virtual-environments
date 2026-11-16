extends SceneTree
# Written for the film's evidence run (not part of the example): curl ratio of three normal maps,
# both conventions, at strides 2, 4 and 8. Two implementations are run side by side:
#   A = the assignment's own listing (default stride 4), pasted verbatim into curl_ratio_assignment below
#   B = the example's helper (default stride 2), loaded from res://course-series/normal-calibration/normal-map-check.gd

# ---- assignment listing, verbatim ----
static func curl_ratio_assignment(source: Image, directx := false, stride := 4) -> float:
	var img := source.duplicate() as Image
	if img.is_compressed():
		img.decompress()
	var s: float = -1.0 if directx else 1.0
	var curl_sq := 0.0
	var terms_sq := 0.0
	for v in range(1, img.get_height() - 1, stride):
		for u in range(1, img.get_width() - 1, stride):
			var t1 := (_dh_du(img, u, v + 1) - _dh_du(img, u, v - 1)) * 0.5
			var t2 := (_dh_dv(img, u + 1, v, s) - _dh_dv(img, u - 1, v, s)) * 0.5
			curl_sq += (t1 - t2) * (t1 - t2)
			terms_sq += t1 * t1 + t2 * t2
	return curl_sq / maxf(terms_sq, 1e-12)

static func _normal(img: Image, u: int, v: int) -> Vector3:
	var c := img.get_pixel(u, v)
	return Vector3(c.r, c.g, c.b) * 2.0 - Vector3.ONE

static func _dh_du(img: Image, u: int, v: int) -> float:
	var n := _normal(img, u, v)
	return -n.x / maxf(n.z, 0.05)

static func _dh_dv(img: Image, u: int, v: int, s: float) -> float:
	var n := _normal(img, u, v)
	return s * n.y / maxf(n.z, 0.05)
# ---- end verbatim ----

func _initialize() -> void:
	var helper = load("res://course-series/normal-calibration/normal-map-check.gd")
	var files := {
		"polyhaven_gl": "res://course-series/normal-calibration/stone_floor_nor_gl_1k.png",
		"polyhaven_dx": "res://course-series/normal-calibration/stone_floor_nor_dx_1k.png",
		"analytic_gl": "res://course-series/material-textures/analytic-normal-gl.png",
	}
	var rows := []
	for key in files:
		var image := Image.load_from_file(files[key])
		for stride in [2, 4, 8]:
			var row := {
				"image": key,
				"size": [image.get_width(), image.get_height()],
				"stride": stride,
				"A_assignment_as_GL": curl_ratio_assignment(image, false, stride),
				"A_assignment_as_DX": curl_ratio_assignment(image, true, stride),
				"B_example_as_GL": helper.curl_ratio(image, false, stride),
				"B_example_as_DX": helper.curl_ratio(image, true, stride),
			}
			rows.append(row)
			print("CURL ", JSON.stringify(row))
	var out := OS.get_cmdline_user_args()[0] if OS.get_cmdline_user_args().size() else ""
	if out != "":
		var file := FileAccess.open(out, FileAccess.WRITE)
		file.store_string(JSON.stringify(rows, "\t"))
		file.close()
	print("RESULT curl strides done, rows=", rows.size())
	quit()
