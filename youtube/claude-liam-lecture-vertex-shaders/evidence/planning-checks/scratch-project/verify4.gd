extends SceneTree
# Check 4: VERTEX_ID (the vertex stage's own vertex counter) for Sprite2D, QuadMesh 3x3 (25 vertices) and a 6-point Polygon2D.
# red = VERTEX_ID / id_scale blended across the shape (id_scale 16 for the sprite and the polygon, 32 for the 25-vertex mesh); we read the colour 2 px inside each corner and in the middle.
const V = preload("res://vscene.gd")

func _initialize() -> void:
	call_deferred("run")

func px(img: Image, x: int, y: int, scale: float) -> float:
	return snappedf(img.get_pixel(x, y).r * scale, 0.05)   # back to "vertex id" units (8-bit colour: coarse)

func run() -> void:
	V.setup(root, 640, 360)
	var mat := V.material_from(V.check_shader("c3-vertex-id"))
	var img := V.white_image(128, 128)
	root.add_child(V.sprite(img, Vector2(110, 180), 1.0, mat))
	var mat32 := V.material_from(V.check_shader("c3-vertex-id"), {"id_scale": 32.0})
	root.add_child(V.quad(Vector2(128, -128), 3, 3, img, Vector2(320, 180), mat32))
	var pg := Polygon2D.new()
	pg.position = Vector2(530, 180)
	pg.polygon = PackedVector2Array([Vector2(-64, -64), Vector2(0, -64), Vector2(64, -64), Vector2(64, 64), Vector2(0, 64), Vector2(-64, 64)])
	pg.texture = ImageTexture.create_from_image(img)
	pg.uv = PackedVector2Array([Vector2(0, 0), Vector2(64, 0), Vector2(128, 0), Vector2(128, 128), Vector2(64, 128), Vector2(0, 128)])
	pg.material = mat
	root.add_child(pg)
	await V.frames(self, 4)
	var im := V.grab(root)
	im.save_png(V.png_dir() + "/verify4-ids.png")
	for item in [["sprite2d", 110, 16.0], ["quadmesh-3x3", 320, 32.0], ["polygon2d-6-points", 530, 16.0]]:
		var cx: int = item[1]
		var sc: float = item[2]
		var o := 62
		V.out("4-" + item[0], {"top_left": px(im, cx - o, 180 - o, sc), "top_right": px(im, cx + o, 180 - o, sc), "bottom_left": px(im, cx - o, 180 + o, sc),
			"bottom_right": px(im, cx + o, 180 + o, sc), "middle": px(im, cx, 180, sc), "top_middle": px(im, cx, 180 - o, sc), "bottom_middle": px(im, cx, 180 + o, sc)})
	quit(0)
