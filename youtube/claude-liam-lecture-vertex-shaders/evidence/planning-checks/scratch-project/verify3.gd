extends SceneTree
# Check 3: the same one-line wave on four kinds of 256 x 128 flag, in one scene (so one shared TIME):
#   A Sprite2D (4 vertices)   B MeshInstance2D + QuadMesh 31 x 7 (33 x 9 vertices)
#   C Polygon2D, outline only: 33 points along the top edge and 33 along the bottom (66 points)
#   D Polygon2D with a grid of internal vertices (outline of 4 corners + interior points, internal_vertex_count set)
const V = preload("res://vscene.gd")

func _initialize() -> void:
	call_deferred("run")

func polygon_outline(w: float, h: float, n: int) -> PackedVector2Array:
	var pts := PackedVector2Array()
	for i in range(n + 1):
		pts.append(Vector2(-w / 2 + w * i / n, -h / 2))
	for i in range(n, -1, -1):
		pts.append(Vector2(-w / 2 + w * i / n, h / 2))
	return pts

func make_poly(pts: PackedVector2Array, internal: int, img: Image, w: float, h: float, pos: Vector2, mat: Material) -> Polygon2D:
	var pg := Polygon2D.new()
	pg.position = pos
	pg.polygon = pts
	var uvs := PackedVector2Array()
	for p in pts:
		uvs.append(Vector2(p.x + w / 2, p.y + h / 2))      # texture pixel coordinates (texture is w x h)
	pg.uv = uvs
	pg.internal_vertex_count = internal
	pg.texture = ImageTexture.create_from_image(img)
	pg.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	pg.material = mat
	return pg

func run() -> void:
	V.setup(root, 1280, 720)
	var mat := V.material_from(V.check_shader("c2-flag-draft"))
	var img := V.checker_image(256, 128, 16)
	var W := 256.0
	var H := 128.0
	root.add_child(V.sprite(img, Vector2(340, 200), 1.0, mat))                                     # A
	root.add_child(V.quad(Vector2(W, -H), 31, 7, img, Vector2(940, 200), mat))                     # B
	root.add_child(make_poly(polygon_outline(W, H, 32), 0, img, W, H, Vector2(340, 520), mat))     # C
	# D: 4 corners + a 17 x 5 grid of interior points
	var pts := PackedVector2Array([Vector2(-W / 2, -H / 2), Vector2(W / 2, -H / 2), Vector2(W / 2, H / 2), Vector2(-W / 2, H / 2)])
	var n_int := 0
	for j in range(1, 5):
		for i in range(1, 16):
			pts.append(Vector2(-W / 2 + W * i / 16.0, -H / 2 + H * j / 5.0))
			n_int += 1
	root.add_child(make_poly(pts, n_int, img, W, H, Vector2(940, 520), mat))                       # D
	await V.frames(self, 30)
	for k in range(4):
		var im := V.grab(root)
		im.save_png(V.png_dir() + "/verify3-flags-%d.png" % k)
		await V.frames(self, 8)
	V.out("3-flags", {"A_sprite_vertices": 4, "B_mesh_vertices": 33 * 9, "C_polygon_points": polygon_outline(W, H, 32).size(), "D_polygon_points": pts.size(), "D_internal": n_int})
	quit(0)
