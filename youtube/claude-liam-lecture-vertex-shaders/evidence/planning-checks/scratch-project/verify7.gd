extends SceneTree
# Check 7: what UV does a Polygon2D deliver, with and without a texture? (A flag shader multiplies by UV.x, so this matters.)
const V = preload("res://vscene.gd")

func _initialize() -> void:
	call_deferred("run")

func rgb(img: Image, x: int, y: int) -> Array:
	var c := img.get_pixel(x, y)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001)]

func run() -> void:
	V.setup(root, 640, 360)
	var mat := V.material_from(V.check_shader("c11-uv-colors"))
	var pts := PackedVector2Array([Vector2(-64, -64), Vector2(64, -64), Vector2(64, 64), Vector2(-64, 64)])
	# A: no texture, no uv   B: texture and uv (pixels)   C: no texture, but uv set
	var a := Polygon2D.new()
	a.position = Vector2(110, 180)
	a.polygon = pts
	a.material = mat
	root.add_child(a)
	var b := Polygon2D.new()
	b.position = Vector2(320, 180)
	b.polygon = pts
	b.texture = ImageTexture.create_from_image(V.white_image(128, 128))
	b.uv = PackedVector2Array([Vector2(0, 0), Vector2(128, 0), Vector2(128, 128), Vector2(0, 128)])
	b.material = mat
	root.add_child(b)
	var c := Polygon2D.new()
	c.position = Vector2(530, 180)
	c.polygon = pts
	c.uv = PackedVector2Array([Vector2(0, 0), Vector2(128, 0), Vector2(128, 128), Vector2(0, 128)])
	c.material = mat
	root.add_child(c)
	await V.frames(self, 4)
	var im := V.grab(root)
	im.save_png(V.png_dir() + "/verify7-polygon-uv.png")
	for item in [["A_no_texture_no_uv", 110], ["B_texture_and_uv", 320], ["C_no_texture_but_uv_set", 530]]:
		var cx: int = item[1]
		V.out("7-polygon-uv", {"case": item[0], "red_green_at_left_edge": rgb(im, cx - 62, 180), "at_right_edge": rgb(im, cx + 62, 180), "at_top_edge": rgb(im, cx, 118), "at_bottom_edge": rgb(im, cx, 241)})
	quit(0)
