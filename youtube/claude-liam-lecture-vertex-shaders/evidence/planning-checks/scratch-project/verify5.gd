extends SceneTree
# Check 5: counting vertices.
#  5a. the one-line count a viewer can run on a mesh (and on a polygon)
#  5b. VERTEX_ID, the vertex stage's own counter, on a QuadMesh cut 19 x 19: the largest id seen should be 440 (441 vertices)
#  5c. how Godot triangulates a Polygon2D that has points only around its outline (66 points)
const V = preload("res://vscene.gd")
const CS = preload("res://capture_scenes.gd")

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	V.setup(root, 640, 360)
	# 5a
	var mesh := QuadMesh.new()
	mesh.size = Vector2(CS.FLAG_W, CS.FLAG_H)
	mesh.subdivide_width = 31
	mesh.subdivide_depth = 7
	V.out("5a-count-mesh", {"code": "mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX].size()", "result": mesh.surface_get_arrays(0)[Mesh.ARRAY_VERTEX].size()})
	var pg := Polygon2D.new()
	pg.polygon = CS.polygon_outline(CS.FLAG_W, CS.FLAG_H, 32)
	V.out("5a-count-polygon", {"code": "polygon.size()", "result": pg.polygon.size()})
	# 5b: a 19 x 19 QuadMesh coloured by VERTEX_ID / 512; read the last corner
	var mat := V.material_from(V.check_shader("c3-vertex-id"), {"id_scale": 512.0})
	var q := V.quad(Vector2(256, -256), 19, 19, V.white_image(128, 128), Vector2(320, 180), mat)
	root.add_child(q)
	await V.frames(self, 4)
	var im := V.grab(root)
	# the mesh covers x 192..447, y 52..307; sample 1 px in from each corner
	var out := {}
	for nm in [["top_left", 193, 53], ["top_right", 446, 53], ["bottom_left", 193, 306], ["bottom_right", 446, 306]]:
		out[nm[0]] = snappedf(im.get_pixel(nm[1], nm[2]).r * 512.0, 1.0)
	V.out("5b-vertex-id-19x19", {"ids_read_at_corners": out, "vertices_in_array": (q.mesh as QuadMesh).surface_get_arrays(0)[Mesh.ARRAY_VERTEX].size()})
	# 5c: triangulation of the outline-only polygon
	var pts := CS.polygon_outline(CS.FLAG_W, CS.FLAG_H, 32)
	var idx := Geometry2D.triangulate_polygon(pts)
	var tri := idx.size() / 3
	var longest := 0.0
	var centre_counts := {}
	for i in range(tri):
		var a := pts[idx[i * 3]]
		var b := pts[idx[i * 3 + 1]]
		var c2 := pts[idx[i * 3 + 2]]
		longest = maxf(longest, maxf(a.distance_to(b), maxf(b.distance_to(c2), c2.distance_to(a))))
		for k in range(3):
			centre_counts[idx[i * 3 + k]] = centre_counts.get(idx[i * 3 + k], 0) + 1
	var top_degree := 0
	var top_vertex := -1
	for k in centre_counts:
		if centre_counts[k] > top_degree:
			top_degree = centre_counts[k]
			top_vertex = k
	V.out("5c-polygon-outline-triangulation", {"points": pts.size(), "triangles": tri, "longest_edge_px": snappedf(longest, 0.1), "flag_size_px": [CS.FLAG_W, CS.FLAG_H],
		"vertex_used_by_most_triangles": top_vertex, "that_vertex_is_in_n_triangles": top_degree, "note": "a fan: a few vertices are shared by many long thin triangles"})
	quit(0)
