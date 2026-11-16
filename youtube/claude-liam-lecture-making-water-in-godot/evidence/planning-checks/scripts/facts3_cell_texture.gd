extends SceneTree
# facts3: what does a Cellular FastNoiseLite look like as a NoiseTexture2D, for each return type? Saves PNGs and prints min / max / the value on a cell border.
const CB := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot/water-project/scripts/cove_builder.gd"
const OUT := "/private/tmp/claude-501/water-scratch/"
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var cb = load(CB)
	for rt in [1, 4]:
		var fn := FastNoiseLite.new()
		fn.noise_type = FastNoiseLite.TYPE_CELLULAR
		fn.cellular_return_type = rt
		fn.frequency = 0.02
		fn.seed = 5
		fn.fractal_type = FastNoiseLite.FRACTAL_NONE if OS.get_environment("NOFRACTAL") == "1" else FastNoiseLite.FRACTAL_FBM
		var t := NoiseTexture2D.new()
		t.width = 512; t.height = 512; t.seamless = true; t.noise = fn
		await t.changed
		var img := t.get_image()
		img.convert(Image.FORMAT_L8) if false else null
		var mn := 1.0; var mx := 0.0; var s := 0.0
		for y in range(0, 512, 2):
			for x in range(0, 512, 2):
				var v := img.get_pixel(x, y).r
				mn = minf(mn, v); mx = maxf(mx, v); s += v
		print("return type %d: texture value min %.3f max %.3f mean %.3f; raw noise at (10,10) = %.3f" % [rt, mn, mx, s / (256.0 * 256.0), fn.get_noise_2d(10, 10)])
		img.save_png(OUT + "cell-texture-rt%d.png" % rt)
	quit()
