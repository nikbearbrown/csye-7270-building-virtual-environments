extends SceneTree
# Check 8: does a Polygon2D with points only around its outline fill itself with the triangles Geometry2D.triangulate_polygon returns?
# A: the outline polygon as is. B: the same points with `polygons` set to exactly those triangles. If the two renders match pixel for pixel, yes.
const V = preload("res://vscene.gd")
const CS = preload("res://capture_scenes.gd")

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	V.setup(root, 1280, 720)
	var fl := CS.flag_image(CS.FLAG_W, CS.FLAG_H)
	var pts := CS.polygon_outline(CS.FLAG_W, CS.FLAG_H, 32)
	var a := CS.polygon_node(pts, fl, CS.FLAG_W, CS.FLAG_H, Vector2(340, 360))
	var b := CS.polygon_node(pts, fl, CS.FLAG_W, CS.FLAG_H, Vector2(940, 360))
	var idx := Geometry2D.triangulate_polygon(pts)
	var tris: Array = []
	for i in range(idx.size() / 3):
		tris.append(PackedInt32Array([idx[i * 3], idx[i * 3 + 1], idx[i * 3 + 2]]))
	b.polygons = tris
	var mat := V.material_from(V.lab_shader("04-ripple"))
	a.material = mat
	b.material = mat
	root.add_child(a)
	root.add_child(b)
	await V.frames(self, 5)
	var im := V.grab(root)
	im.save_png(V.png_dir() + "/verify8-triangulation.png")
	var diff := 0
	for y in range(720):
		for x in range(-200, 200):
			var ca := im.get_pixel(340 + x, y)
			var cb := im.get_pixel(940 + x, y)
			if ca != cb:
				diff += 1
	V.out("8-polygon-default-vs-explicit-triangles", {"triangles": tris.size(), "pixels_that_differ": diff})
	quit(0)
