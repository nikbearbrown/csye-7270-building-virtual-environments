extends SceneTree
# Check 9: a vertex shader changes the DRAWING, not the node. A checker Sprite2D is drawn 200 px to the right by `VERTEX.x += 200.0`.
#   9a. Sprite2D.get_rect() and the global transform before and after the material is assigned
#   9b. an Area2D with a 128 x 128 collision shape on the same node: which of two small probe areas does it overlap?
#       probe_home sits where the node IS (0, 0); probe_drawn sits where the shader DRAWS the picture (200, 0)
#   9c. the picture's measured position in the rendered frame
const V = preload("res://vscene.gd")

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	V.setup(root, 640, 360)
	var holder := Node2D.new()
	holder.position = Vector2(220, 180)
	root.add_child(holder)
	var sp := V.sprite(V.checker_image(128, 128, 16), Vector2.ZERO, 1.0)
	holder.add_child(sp)
	var area := Area2D.new()
	var cs := CollisionShape2D.new()
	var shape := RectangleShape2D.new()
	shape.size = Vector2(128, 128)
	cs.shape = shape
	area.add_child(cs)
	holder.add_child(area)
	var probes := {}
	for nm in [["probe_home", Vector2.ZERO], ["probe_drawn", Vector2(200, 0)]]:
		var pa := Area2D.new()
		var pc := CollisionShape2D.new()
		var ps := RectangleShape2D.new()
		ps.size = Vector2(10, 10)
		pc.shape = ps
		pa.add_child(pc)
		pa.position = nm[1]
		holder.add_child(pa)
		probes[nm[0]] = pa
	await V.frames(self, 6)
	var rect_before := sp.get_rect()
	var xform_before := sp.global_position
	var img0 := V.grab(root)
	sp.material = V.material_from(V.lab_shader("16-slide-far"))
	await V.frames(self, 6)
	var rect_after := sp.get_rect()
	V.out("9a-rect-and-position", {"get_rect_before": [rect_before.position.x, rect_before.position.y, rect_before.size.x, rect_before.size.y],
		"get_rect_after": [rect_after.position.x, rect_after.position.y, rect_after.size.x, rect_after.size.y], "global_position_before": [xform_before.x, xform_before.y], "global_position_after": [sp.global_position.x, sp.global_position.y]})
	var names := []
	for a in area.get_overlapping_areas():
		for k in probes:
			if probes[k] == a:
				names.append(k)
	V.out("9b-collision-overlaps", {"collision_area_overlaps": names, "expected": "probe_home overlaps (the node is still there); probe_drawn does not (the picture is, the node is not)"})
	var img := V.grab(root)
	img.save_png(V.png_dir() + "/verify9-drawing-only.png")
	# measured position of the picture: the checker's leftmost non-stage pixel on the centre row
	var stage := V.STAGE
	var left := -1
	for x in range(0, 640):
		var c := img.get_pixel(x, 180)
		if absf(c.r - stage.r) > 0.05 or absf(c.g - stage.g) > 0.05:
			left = x
			break
	V.out("9c-picture-position", {"picture_left_edge_x": left, "node_left_edge_x_before": 220 - 64, "note": "the node's rect starts at x = 156; the picture was drawn 200 px further right"})
	quit(0)
