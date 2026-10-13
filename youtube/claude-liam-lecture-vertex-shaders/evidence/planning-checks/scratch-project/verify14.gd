extends SceneTree
# Check 14: the Polygon2D border artifact named in the brief (checked for the record; not narrated: the UV film owns it).
# A 128 px checker texture on a 160 px Polygon2D whose uv runs from -16 to 144 texture pixels (UV -0.125 to 1.125): outside 0..1 the
# texture is clamped, so the border pixels repeat outward. The fix is four steps on UV in fragment().
#   A: no shader   B: c12-border-mask.gdshader
# We read a pixel 8 px outside the texture on the left (x = 88 for A) and compare it with the pixel just inside (x = 100), and the same for B.
const V = preload("res://vscene.gd")

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	V.setup(root, 640, 360)
	var img := V.checker_image(128, 128, 16)
	var pts := PackedVector2Array([Vector2(-80, -80), Vector2(80, -80), Vector2(80, 80), Vector2(-80, 80)])
	var nodes: Array = []
	for i in range(2):
		var pg := Polygon2D.new()
		pg.position = Vector2(160 + 320 * i, 180)
		pg.polygon = pts
		pg.texture = ImageTexture.create_from_image(img)
		pg.uv = PackedVector2Array([Vector2(-16, -16), Vector2(144, -16), Vector2(144, 144), Vector2(-16, 144)])
		pg.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		if i == 1:
			pg.material = V.material_from(V.check_shader("c12-border-mask"))
		root.add_child(pg)
		nodes.append(pg)
	await V.frames(self, 4)
	var im := V.grab(root)
	im.save_png(V.png_dir() + "/verify14-border.png")
	var out := {}
	for i in range(2):
		var cx := 160 + 320 * i
		var band := im.get_pixel(cx - 72, 150)        # 8 px outside the texture's left edge (texture left edge is at cx - 64)
		var inside := im.get_pixel(cx - 60, 150)      # 4 px inside it
		var band_top := im.get_pixel(cx, 180 - 72)    # 8 px above the texture's top edge
		var inside_top := im.get_pixel(cx, 180 - 60)
		out["AB"[i]] = {"band_left": [snappedf(band.r, 0.001), snappedf(band.g, 0.001), snappedf(band.b, 0.001)], "inside_left": [snappedf(inside.r, 0.001), snappedf(inside.g, 0.001), snappedf(inside.b, 0.001)],
			"band_top": [snappedf(band_top.r, 0.001), snappedf(band_top.g, 0.001), snappedf(band_top.b, 0.001)], "inside_top": [snappedf(inside_top.r, 0.001), snappedf(inside_top.g, 0.001), snappedf(inside_top.b, 0.001)]}
	V.out("14-polygon-border", {"A_no_shader": out["A"], "B_masked": out["B"], "stage": [snappedf(V.STAGE.r, 0.001), snappedf(V.STAGE.g, 0.001), snappedf(V.STAGE.b, 0.001)],
		"reading": "A: the band pixel equals the pixel just inside (the border repeats). B: the band pixel is the stage colour (hidden by the four steps)."})
	quit(0)
