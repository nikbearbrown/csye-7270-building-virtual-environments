extends SceneTree
# export_images.gd: saves the real images the film shows of Godot's own noise textures, and prints their numbers. CPU only, no window needed:
#   godot --headless --path water-project --script capture-scenes/export_images.gd -- /absolute/out/dir
# Writes normal_a.png (the first normal map, 512 x 512, 100 percent), tiles-not-seamless.png and tiles-seamless.png (the same normal map repeated 2 x 2),
# cell-texture.png (the baked cellular texture), and prints the seam numbers measured in evidence/planning-checks/RESULTS.md.
const CB := "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot/water-project/scripts/cove_builder.gd"

func _initialize() -> void:
	call_deferred("run")

func tile2x2(img: Image) -> Image:
	var w := img.get_width()
	var out := Image.create(w * 2, w * 2, false, img.get_format())
	for ty in 2:
		for tx in 2:
			out.blit_rect(img, Rect2i(0, 0, w, w), Vector2i(tx * w, ty * w))
	return out

func run() -> void:
	var dir := OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(dir)
	var cb = load(CB)
	var a: NoiseTexture2D = cb.normal_noise(1, 0.006)
	await a.changed
	var img := a.get_image()
	img.save_png(dir + "/normal_a.png")
	tile2x2(img).save_png(dir + "/tiles-seamless.png")
	var bad: NoiseTexture2D = cb.normal_noise(1, 0.006)
	bad.seamless = false
	await bad.changed
	tile2x2(bad.get_image()).save_png(dir + "/tiles-not-seamless.png")
	var c: NoiseTexture2D = cb.cell_noise()
	await c.changed
	c.get_image().save_png(dir + "/cell-texture.png")
	print("EXPORT normal map format ", img.get_format(), " size ", img.get_width(), "x", img.get_height(), " pixel(100,100)=", img.get_pixel(100, 100))
	quit()
