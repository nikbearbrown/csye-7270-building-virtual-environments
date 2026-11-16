extends SceneTree
# facts2: NoiseTexture2D numbers (CPU only). seamless on/off: how big is the jump across the tile edge compared with a normal neighbouring column?
# as_normal_map: what are the pixels (flat = 0.5, 0.5, 1.0), how far do they lean, and what does bump_strength do.
func make(seed_v: int, freq: float, seamless: bool, normal: bool, bump := 6.0) -> NoiseTexture2D:
	var fn := FastNoiseLite.new()
	fn.noise_type = FastNoiseLite.TYPE_SIMPLEX_SMOOTH
	fn.seed = seed_v
	fn.frequency = freq
	fn.fractal_octaves = 3
	var t := NoiseTexture2D.new()
	t.width = 512
	t.height = 512
	t.seamless = seamless
	t.as_normal_map = normal
	t.bump_strength = bump
	t.noise = fn
	return t

func col_diff(img: Image, x0: int, x1: int) -> float:
	var s := 0.0
	for y in img.get_height():
		s += absf(img.get_pixel(x0, y).r - img.get_pixel(x1, y).r)
	return s / img.get_height()

func seam(img: Image) -> Dictionary:
	var w := img.get_width()
	var adj := 0.0
	for x in range(0, w - 1):
		adj += col_diff(img, x, x + 1)
	adj /= (w - 1)
	return {"edge_jump": snappedf(col_diff(img, w - 1, 0), 0.0001), "avg_neighbour_step": snappedf(adj, 0.0001)}

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	print("ENGINE ", Engine.get_version_info()["string"])
	for sm in [false, true]:
		var t := make(1, 0.006, sm, false)
		await t.changed
		var img := t.get_image()
		print("SEAM seamless=%s grey 512x512 (red channel, 0..1): %s" % [sm, seam(img)])
	for bump in [2.0, 6.0, 12.0]:
		var t := make(1, 0.006, true, true, bump)
		await t.changed
		var img := t.get_image()
		var n := 0
		var sr := 0.0; var sg := 0.0; var sb := 0.0; var lean := 0.0; var maxlean := 0.0
		for y in range(0, 512):
			for x in range(0, 512):
				var c := img.get_pixel(x, y)
				sr += c.r; sg += c.g; sb += c.b
				var v := Vector3(c.r * 2.0 - 1.0, c.g * 2.0 - 1.0, c.b * 2.0 - 1.0).normalized()
				var ang := rad_to_deg(acos(clampf(v.z, -1.0, 1.0)))
				lean += ang
				maxlean = maxf(maxlean, ang)
				n += 1
		print("NORMALMAP seamless as_normal_map bump_strength=%.0f: mean rgb = (%.3f, %.3f, %.3f); mean lean from straight up = %.1f deg; max lean = %.1f deg; format=%d" % [bump, sr / n, sg / n, sb / n, lean / n, maxlean, img.get_format()])
		if bump == 6.0:
			print("   pixel (100,100) = ", img.get_pixel(100, 100), " pixel (300,200) = ", img.get_pixel(300, 200))
	var ts := make(1, 0.006, true, true, 6.0)
	await ts.changed
	var seam_n := ts.get_image()
	var sn := seam(seam_n)
	print("SEAM normal map seamless: ", sn)
	var tn := make(1, 0.006, false, true, 6.0)
	await tn.changed
	print("SEAM normal map NOT seamless: ", seam(tn.get_image()))
	quit()
