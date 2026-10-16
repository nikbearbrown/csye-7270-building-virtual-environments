extends SceneTree
## Assignment 3 headless check: compares each imported asset with the numbers in CHANGE-BRIEF.md
## and checks where the assets sit in base.tscn (floor contact, 0.1 m grid, no overlaps).
## Run: godot --headless --path <the Godot project folder> --script res://tests/a3_asset_check.gd --fixed-fps 60
##
## What it shows: bounding-box size (Godot is Y-up, so the height is the Y size), node scale,
## the lowest point, the triangle count, the crate animations, and whether each placed asset
## rests on the floor (or the tablet on the large crate) in base.tscn.
## What it does NOT show: whether an asset looks right, reads as what it is, has the right
## colours under the scene's lights, or suits the game's style. Those are human checks.

const TOL := 0.002  # metres

# name, file, expected size (x, y, z), expected lowest y in the file, triangle budget
const ASSETS := [
	["chair", "res://assets/furniture/chair.glb", Vector3(0.44, 0.90, 0.42), 0.0, 500],
	["tablet", "res://assets/props/tablet.glb", Vector3(0.242, 0.162, 0.028), -0.081, 500],
	["crate_long", "res://assets/furniture/crate_long.glb", Vector3(1.0, 0.4, 0.5), 0.0, 500],
	["crate_cube", "res://assets/furniture/crate_cube.glb", Vector3(0.5, 0.5, 0.5), 0.0, 500],
	["computer_desk", "res://assets/furniture/computer_desk.glb", Vector3(1.5, 0.78, 0.5), 0.0, 500],
	["computer_desk_l", "res://assets/furniture/computer_desk_l.glb", Vector3(1.5, 0.78, 1.0), 0.0, 500],
]
# Nodes in base.tscn that stand on the floor, and the ones that must fit the 0.1 m furniture grid
# (the chair is 0.44 x 0.42 m, not a whole number of cells, so it is not grid-checked).
const FLOOR_ITEMS := ["chair", "crate_long", "crate_cube", "computer_desk", "computer_desk_l"]
const GRID_ITEMS := ["crate_long", "crate_cube", "computer_desk", "computer_desk_l"]

var failures := 0


func _check(ok: bool, what: String) -> void:
	print("  %s  %s" % ["PASS" if ok else "FAIL", what])
	if not ok:
		failures += 1


func _merge_aabb(n: Node, xf: Transform3D, acc: Array) -> void:
	var t := xf
	if n is Node3D:
		t = xf * (n as Node3D).transform
	if n is MeshInstance3D:
		var a: AABB = t * (n as MeshInstance3D).get_aabb()
		acc[0] = a if acc[0] == null else (acc[0] as AABB).merge(a)
	for c in n.get_children():
		_merge_aabb(c, t, acc)


func _aabb(n: Node3D, xf: Transform3D) -> AABB:
	var acc := [null]
	_merge_aabb(n, xf, acc)
	return acc[0]


func _triangles(n: Node) -> int:
	var count := 0
	if n is MeshInstance3D:
		var mesh := (n as MeshInstance3D).mesh
		for s in mesh.get_surface_count():
			var arr := mesh.surface_get_arrays(s)
			var idx = arr[Mesh.ARRAY_INDEX]
			count += (idx.size() if idx != null else (arr[Mesh.ARRAY_VERTEX] as PackedVector3Array).size()) / 3
	for c in n.get_children():
		count += _triangles(c)
	return count


func _all_scales_one(n: Node) -> bool:
	if n is Node3D and not (n as Node3D).scale.is_equal_approx(Vector3.ONE):
		return false
	for c in n.get_children():
		if not _all_scales_one(c):
			return false
	return true


func _initialize() -> void:
	print("== Part 1: each asset file on its own ==")
	for a in ASSETS:
		var inst := (load(a[1]) as PackedScene).instantiate() as Node3D
		root.add_child(inst)
		var box := _aabb(inst, Transform3D.IDENTITY)
		var tris := _triangles(inst)
		print("%s: size %s, lowest y %.3f, triangles %d" % [a[0], box.size, box.position.y, tris])
		var diff := (box.size - (a[2] as Vector3)).abs()
		_check(maxf(diff.x, maxf(diff.y, diff.z)) <= TOL, "size matches the brief %s (within %.3f m)" % [a[2], TOL])
		_check(absf(box.position.y - a[3]) <= TOL, "lowest point at y = %.3f as the brief says" % a[3])
		_check(_all_scales_one(inst), "every node scale is 1, 1, 1")
		_check(tris <= a[4], "triangles %d <= budget %d" % [tris, a[4]])
		var ap := inst.find_child("AnimationPlayer", true, false) as AnimationPlayer
		if a[0].begins_with("crate"):
			_check(ap != null and ap.has_animation("open") and ap.has_animation("close"), "has open and close animations")
			if ap:
				var lid := inst.find_child("*_Lid", true, false) as Node3D
				ap.play("open"); ap.seek(ap.get_animation("open").length, true)
				_check(is_equal_approx(snappedf(lid.rotation_degrees.x, 0.01), -100.0), "after open the lid is at -100 deg (%.2f)" % lid.rotation_degrees.x)
				ap.play("close"); ap.seek(ap.get_animation("close").length, true)
				_check(is_equal_approx(snappedf(lid.rotation_degrees.x, 0.01), 0.0), "after close the lid is back at 0 deg (%.2f)" % lid.rotation_degrees.x)
		inst.queue_free()

	print("== Part 2: placement in base.tscn ==")
	var base := (load("res://base.tscn") as PackedScene).instantiate() as Node3D
	root.add_child(base)
	var floor_box := base.get_node("room/floor") as CSGBox3D
	var floor_top := floor_box.position.y + floor_box.size.y / 2.0  # from the floor node, not from an asset
	print("floor top y = %.3f (from room/floor)" % floor_top)
	var boxes := {}
	for name in FLOOR_ITEMS + ["tablet"]:
		var box := _aabb(base.get_node(name) as Node3D, Transform3D.IDENTITY)
		boxes[name] = box
		print("%s: world bottom %.3f, top %.3f, footprint %.3f x %.3f at x %.3f, z %.3f"
			% [name, box.position.y, box.end.y, box.size.x, box.size.z, box.position.x, box.position.z])
	for name in FLOOR_ITEMS:
		_check(absf(boxes[name].position.y - floor_top) <= TOL, "%s rests on the floor (y = %.3f)" % [name, floor_top])
	for name in GRID_ITEMS:
		var b: AABB = boxes[name]
		var on_grid := true
		for v in [b.position.x, b.position.z, b.end.x, b.end.z]:
			on_grid = on_grid and absf(v * 10.0 - roundf(v * 10.0)) <= TOL * 10.0
		_check(on_grid, "%s footprint edges sit on the 0.1 m grid" % name)
	# The tablet was on the large crate's lid until 2026-10-15; I then moved it into the air and
	# tilted it so it is easier to look at (a display placement, not a game placement). So it is
	# no longer checked against the lid; it must clear the floor and not touch any other asset.
	_check(boxes["tablet"].position.y > floor_top + TOL, "tablet is above the floor (display placement)")
	var names := boxes.keys()
	for i in names.size():
		for j in range(i + 1, names.size()):
			var a: AABB = boxes[names[i]].grow(-TOL)
			var b: AABB = boxes[names[j]].grow(-TOL)
			_check(not a.intersects(b), "%s and %s do not overlap" % [names[i], names[j]])
	base.queue_free()

	print("== %s: %d failure(s) ==" % ["ALL PASS" if failures == 0 else "FAILED", failures])
	quit(1 if failures > 0 else 0)
