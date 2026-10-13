extends RefCounted
# sky_lib.gd: the procedural "sky" the captures sample. Tileable (everything wraps), deterministic (seed 7), no external art.
# make_sky(n) -> n x n RGBA image. Drawn at n/512 x detail so a 1536 px image still maps one tile to 512 world pixels at 3x sharpness.

const BASE := Color("#5B6AA3")      # mid-tone indigo (stays far from ink, so the type gate does not read it as text)
const HAZE := Color("#8794C9")      # lighter nebula
const STAR := Color("#FAF9F5")      # the cream of the palette
const STAR_COOL := Color("#DCE4F8")


static func make_sky(n: int, seed_value: int = 7) -> Image:
	var k := float(n) / 512.0
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	# nebula: seamless noise, thresholded gently so it reads as soft clouds
	var fn := FastNoiseLite.new()
	fn.seed = seed_value
	fn.frequency = 0.012 / k
	fn.fractal_octaves = 3
	var haze := fn.get_seamless_image(n, n)
	haze.convert(Image.FORMAT_RGBA8)
	for y in n:
		for x in n:
			var v := haze.get_pixel(x, y).r
			var t := clampf((v - 0.45) * 1.6, 0.0, 1.0) * 0.55
			img.set_pixel(x, y, BASE.lerp(HAZE, t))
	# stars: small dots with wrap-around; a few bigger ones
	var rng := RandomNumberGenerator.new()
	rng.seed = seed_value
	var count := 650
	for i in count:
		var cx := rng.randi_range(0, n - 1)
		var cy := rng.randi_range(0, n - 1)
		var big := rng.randf() < 0.06
		var r := (3.2 if big else rng.randf_range(1.0, 2.2)) * k
		var col := STAR if rng.randf() < 0.7 else STAR_COOL
		var ri := int(ceil(r)) + 1
		for dy in range(-ri, ri + 1):
			for dx in range(-ri, ri + 1):
				var d := sqrt(float(dx * dx + dy * dy))
				if d <= r + 0.5:
					var a := clampf(r + 0.5 - d, 0.0, 1.0)
					var px := posmod(cx + dx, n)
					var py := posmod(cy + dy, n)
					var under := img.get_pixel(px, py)
					img.set_pixel(px, py, under.lerp(col, a))
	_planet(img, Vector2(340.0, 240.0) * k, 36.0 * k, k)
	return img


# one distinctive landmark per tile, so a viewer can follow the pattern: a pale planet with a ring (not terracotta, not near ink)
static func _planet(img: Image, c: Vector2, r: float, k: float) -> void:
	var body_light := Color("#F2E6CF")
	var body_dark := Color("#BDB394")
	var ring := Color("#EFE3C6")
	var n := img.get_width()
	var box := int(r * 2.2)
	for dy in range(-box, box + 1):
		for dx in range(-box, box + 1):
			var p := Vector2(dx, dy)
			var px := int(c.x) + dx
			var py := int(c.y) + dy
			if px < 0 or py < 0 or px >= n or py >= n:
				continue
			# ring: an ellipse (tilted) seen as a thin band, drawn first so the body overlaps its near half
			var q := p.rotated(-0.35)
			var e := sqrt(pow(q.x / (r * 2.0), 2.0) + pow(q.y / (r * 0.55), 2.0))
			var under := img.get_pixel(px, py)
			if abs(e - 1.0) < 0.07 and p.length() > r * 0.98:
				img.set_pixel(px, py, under.lerp(ring, clampf(1.0 - abs(e - 1.0) / 0.07, 0.0, 1.0) * 0.9))
			var d := p.length()
			if d <= r + 0.5:
				var shade := clampf((p.x * 0.5 + p.y * 0.7) / (r * 1.2) * 0.5 + 0.5, 0.0, 1.0)
				var col := body_light.lerp(body_dark, shade)
				img.set_pixel(px, py, img.get_pixel(px, py).lerp(col, clampf(r + 0.5 - d, 0.0, 1.0)))
