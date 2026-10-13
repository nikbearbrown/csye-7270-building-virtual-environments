extends SceneTree
# Noise facts for the dissolve beats (Godot 4.7.2):
#  N1: NoiseTexture2D (FastNoiseLite seed 7, frequency 0.02, 256 x 256, default settings) holds the same pixels as FastNoiseLite.get_image(256, 256), the Lab's "noise" texture.
#  N2: the noise image is grey (r = g = b) and spans 0..1 once normalised (default normalize = true): min, max, mean, and the share of texels below 0.25/0.5/0.75.
#  N3: the same numbers inside the test sprite's disc (radius 0.3 of the texture, centre 0.5, 0.5) - the part of the noise a dissolving sprite actually sees.
#  N4: Texture2D.get_image() on a fresh NoiseTexture2D is null until `changed` fires (docs: generation uses threads).
# Run: godot --path <proj dir> --script res://verify-noise.gd

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func stats(img: Image, disc_only: bool) -> Dictionary:
	var n := img.get_width()
	var mn := 2.0
	var mx := -1.0
	var sum := 0.0
	var cnt := 0
	var below := {0.25: 0, 0.5: 0, 0.75: 0}
	var grey_ok := true
	for y in n:
		for x in n:
			if disc_only and Vector2((x + 0.5) / n, (y + 0.5) / n).distance_to(Vector2(0.5, 0.5)) >= 0.3:
				continue
			var c := img.get_pixel(x, y)
			if absf(c.r - c.g) > 0.0001 or absf(c.r - c.b) > 0.0001: grey_ok = false
			mn = minf(mn, c.r)
			mx = maxf(mx, c.r)
			sum += c.r
			cnt += 1
			for k in below.keys():
				if c.r < k: below[k] += 1
	return {"texels": cnt, "min": snappedf(mn, 0.0001), "max": snappedf(mx, 0.0001), "mean": snappedf(sum / cnt, 0.0001), "grey_r_eq_g_eq_b": grey_ok,
		"share_below_0.25": snappedf(float(below[0.25]) / cnt, 0.001), "share_below_0.5": snappedf(float(below[0.5]) / cnt, 0.001), "share_below_0.75": snappedf(float(below[0.75]) / cnt, 0.001)}

func run() -> void:
	var fn := FastNoiseLite.new()
	fn.seed = 7
	fn.frequency = 0.02
	var nt := NoiseTexture2D.new()
	nt.noise = fn
	nt.width = 256
	nt.height = 256
	out("N4-get_image-before-generation", {"image_is_null_right_after_creation": nt.get_image() == null})
	var frames := 0
	while nt.get_image() == null and frames < 600:
		await process_frame
		frames += 1
	out("N4b-generation-finished", {"frames_waited": frames, "format": nt.get_image().get_format(), "format_note": "Image.FORMAT_L8 = 0"})
	var a: Image = nt.get_image()
	var b: Image = fn.get_image(256, 256)
	a.convert(Image.FORMAT_RGBA8)
	b.convert(Image.FORMAT_RGBA8)
	var diff := 0
	var maxd := 0.0
	for y in 256:
		for x in 256:
			var d := absf(a.get_pixel(x, y).r - b.get_pixel(x, y).r)
			if d > 0.0: diff += 1
			maxd = maxf(maxd, d)
	out("N1-NoiseTexture2D-equals-FastNoiseLite-get_image", {"texels_that_differ": diff, "max_difference": maxd})
	out("N2-whole-texture", stats(b, false))
	out("N3-inside-sprite-disc", stats(b, true))
	quit(0)
