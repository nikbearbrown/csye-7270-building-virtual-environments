extends SceneTree
# Check 2: VERTEX and UV as the vertex stage sees them, for the three nodes the film uses (Sprite2D, MeshInstance2D+QuadMesh, Polygon2D),
# and what a Polygon2D delivers for UV. Each node is 128 x 128 px at scale 1.0, drawn with c1-vertex-local.gdshader.
#   red   = VERTEX.x/128 + 0.5   (0 at -64, 1 at +64)      green = VERTEX.y/128 + 0.5      blue = UV.x
const V = preload("res://vscene.gd")

func _initialize() -> void:
	call_deferred("run")

func px(img: Image, x: int, y: int) -> Array:
	var c := img.get_pixel(x, y)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]

func corners(img: Image, cx: int, cy: int) -> Dictionary:
	# probe 2 px inside each corner of the 128 px node centred at (cx, cy), plus the middle
	var o := 62
	return {"top_left": px(img, cx - o, cy - o), "top_right": px(img, cx + o, cy - o), "bottom_left": px(img, cx - o, cy + o),
		"bottom_right": px(img, cx + o, cy + o), "middle": px(img, cx, cy)}

func run() -> void:
	V.setup(root, 640, 360)
	var mat := V.material_from(V.check_shader("c1-vertex-local"))
	var img := V.checker_image(128, 128)
	# Sprite2D at 110,180 ; MeshInstance2D (size -128 y so it is upright) at 320,180 ; Polygon2D at 530,180
	root.add_child(V.sprite(img, Vector2(110, 180), 1.0, mat))
	root.add_child(V.quad(Vector2(128, -128), 0, 0, img, Vector2(320, 180), mat))
	var pg := Polygon2D.new()
	pg.position = Vector2(530, 180)
	pg.polygon = PackedVector2Array([Vector2(-64, -64), Vector2(64, -64), Vector2(64, 64), Vector2(-64, 64)])
	pg.texture = ImageTexture.create_from_image(img)
	pg.uv = PackedVector2Array([Vector2(0, 0), Vector2(128, 0), Vector2(128, 128), Vector2(0, 128)])   # texture pixel coordinates
	pg.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	pg.material = mat
	root.add_child(pg)
	await V.frames(self, 4)
	var im := V.grab(root)
	im.save_png(V.png_dir() + "/verify2-nodes.png")
	V.out("2a-sprite2d", corners(im, 110, 180))
	V.out("2b-meshinstance2d-quadmesh-y-negative", corners(im, 320, 180))
	V.out("2c-polygon2d-4-points", corners(im, 530, 180))
	quit(0)
