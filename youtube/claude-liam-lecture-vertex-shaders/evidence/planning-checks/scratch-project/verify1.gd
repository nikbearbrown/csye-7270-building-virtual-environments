extends SceneTree
# Check 1 (no shader): how many vertices do the nodes give a vertex shader, and which way up does a QuadMesh draw in 2D?
#  1a. QuadMesh vertex and index counts for several subdivisions (read from the mesh's own arrays)
#  1b. QuadMesh in a MeshInstance2D: is a texture upright or upside down, and does a negative y size fix it?
# Run: godot --path <proj> --script res://verify1.gd
const V = preload("res://vscene.gd")

func _initialize() -> void:
	call_deferred("run")

func eye_rows(img: Image, cx: int, cy: int, half: int) -> Dictionary:
	# the blob has cream eyes ABOVE the middle (-0.06 of the size) when drawn upright. Find the rows of cream pixels.
	var ys: Array = []
	for y in range(cy - half, cy + half):
		for x in range(cx - half, cx + half):
			var c := img.get_pixel(x, y)
			if c.r > 0.97 and c.g > 0.96 and c.b > 0.94 and absf(c.r - V.STAGE.r) > 0.08:
				ys.append(y)
	if ys.is_empty():
		return {"found": false}
	var s := 0.0
	for y in ys:
		s += y
	return {"found": true, "mean_eye_row_minus_centre": snappedf(s / ys.size() - cy, 0.1), "n": ys.size()}

func run() -> void:
	V.setup(root, 640, 360)
	await V.frames(self, 3)
	var env := {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()}
	V.out("env", env)

	# 1a: counts
	for sub in [[0, 0], [1, 1], [3, 3], [7, 0], [0, 7], [19, 19], [31, 7]]:
		var q := QuadMesh.new()
		q.size = Vector2(128, 128)
		q.subdivide_width = sub[0]
		q.subdivide_depth = sub[1]
		var arr := q.surface_get_arrays(0)
		var verts: PackedVector3Array = arr[Mesh.ARRAY_VERTEX]
		var idx: PackedInt32Array = arr[Mesh.ARRAY_INDEX]
		var xs := {}
		var ys := {}
		for v in verts:
			xs[snappedf(v.x, 0.001)] = true
			ys[snappedf(v.y, 0.001)] = true
		V.out("1a-quad-counts", {"subdivide_width": sub[0], "subdivide_depth": sub[1], "vertices": verts.size(), "indices": idx.size(), "triangles": idx.size() / 3,
			"distinct_x": xs.size(), "distinct_y": ys.size(), "expected_(w+2)*(d+2)": (sub[0] + 2) * (sub[1] + 2),
			"first_vertex": [verts[0].x, verts[0].y, verts[0].z], "last_vertex": [verts[verts.size() - 1].x, verts[verts.size() - 1].y, verts[verts.size() - 1].z]})
	var q0 := QuadMesh.new()
	var arr0 := q0.surface_get_arrays(0)
	var uvs: PackedVector2Array = arr0[Mesh.ARRAY_TEX_UV]
	var vv: PackedVector3Array = arr0[Mesh.ARRAY_VERTEX]
	var rows: Array = []
	for i in vv.size():
		rows.append({"vertex": [vv[i].x, vv[i].y, vv[i].z], "uv": [uvs[i].x, uvs[i].y]})
	V.out("1a-default-quad-vertices-and-uv", {"size": [q0.size.x, q0.size.y], "orientation": q0.orientation, "rows": rows})

	# 1b: orientation in 2D. Sprite2D for reference, then QuadMesh with +128 and -128 y size.
	var blob := V.blob_image(128)
	var sp := V.sprite(blob, Vector2(110, 180), 1.0)
	root.add_child(sp)
	var m1 := V.quad(Vector2(128, 128), 0, 0, blob, Vector2(320, 180))
	root.add_child(m1)
	var m2 := V.quad(Vector2(128, -128), 0, 0, blob, Vector2(530, 180))
	root.add_child(m2)
	await V.frames(self, 4)
	var img := V.grab(root)
	img.save_png(V.png_dir() + "/verify1-orientation.png")
	V.out("1b-orientation", {
		"sprite2d": eye_rows(img, 110, 180, 64),
		"quad_size_y_positive": eye_rows(img, 320, 180, 64),
		"quad_size_y_negative": eye_rows(img, 530, 180, 64),
		"reading": "mean_eye_row_minus_centre < 0 means the eyes are above the middle (upright); > 0 means upside down"})
	quit(0)
