extends SceneTree
## Headless check of the three imported props against CHANGE-BRIEF.md
## (revision 1, with revision 2 for the waystone's budget).
##
## Run from the repository's assignment-3 folder:
##   timeout 120 /Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --script res://tests/check_props.gd --fixed-fps 60
##
## Part 1 loads each .glb on its own and prints its bounding box, the scale of
## every node in it, the axis its brief height lies along, its triangles and
## its material colours. Part 2 loads res://scenes/props_room.tscn and checks
## each prop's lowest point against the floor's own height.
##
## What it does not show: whether the props look right, read as what they
## are, or suit the game. Those are human checks (TEST-REPORT.md).

const TOL := 0.005 ## m

## name, file, width X, depth Z, height Y (m), triangle budget, colours (sRGB hex by material name)
const BRIEF := [
	["Waystone", "res://assets/props/waystone.glb", 0.70, 0.40, 0.84, 130,
		{"Stone": "8C8A80", "Moss": "6E7F3C", "Rune": "99E0FF"}],
	["TeleportCircle", "res://assets/props/teleport_circle.glb", 2.25, 2.25, 0.08, 300,
		{"Gold": "F0A830", "DarkStone": "4A4440", "PaleGold": "FFD76E"}],
	["Spikes", "res://assets/props/spikes.glb", 0.80, 0.30, 0.47, 100,
		{"Wood": "7A5838", "Iron": "5C6168"}],
]

var failures := 0


func _init() -> void:
	print("== Part 1: each .glb on its own")
	for b in BRIEF:
		_check_asset(b)
	print("\n== Part 2: res://scenes/props_room.tscn")
	_check_scene()
	print("\n%s: %d failed check(s)" % ["FAIL" if failures else "PASS", failures])
	quit(1 if failures else 0)


func _check_asset(b: Array) -> void:
	var name: String = b[0]
	var root: Node3D = load(b[1]).instantiate()
	print("\n-- %s (%s)" % [name, b[1]])

	var meshes := _mesh_instances(root)
	_expect(meshes.size() > 0, "has a mesh", "%d MeshInstance3D" % meshes.size())

	# Every node from the root down must have scale 1, 1, 1 and no rotation.
	for n in [root] + _descendants(root):
		if n is Node3D:
			var ok: bool = n.scale.is_equal_approx(Vector3.ONE) and n.rotation.is_zero_approx()
			_expect(ok, "node '%s' scale 1 and rotation 0" % n.name, "scale %s rotation %s" % [n.scale, n.rotation_degrees])

	var box := _aabb_in(root, root)
	var size := box.size
	print("   bounding box: position %s size %s" % [_v(box.position), _v(size)])
	_expect(absf(size.x - b[2]) <= TOL, "width X = %.2f m" % b[2], "%.4f" % size.x)
	_expect(absf(size.z - b[3]) <= TOL, "depth Z = %.2f m" % b[3], "%.4f" % size.z)
	_expect(absf(size.y - b[4]) <= TOL, "height Y = %.2f m" % b[4], "%.4f" % size.y)

	# Which axis carries the brief's height? Upright means only Y does.
	var axes := []
	for i in 3:
		if absf(size[i] - b[4]) <= TOL:
			axes.append("XYZ"[i])
	_expect(axes == ["Y"] or (axes.has("Y") and b[4] == b[2]), "stands along Y", "height %.2f m found on %s" % [b[4], axes])

	# Origin: the centre of the underside, at the node's origin.
	var under := Vector3(box.get_center().x, box.position.y, box.get_center().z)
	_expect(under.length() <= TOL, "origin at the centre of the underside", "underside centre %s" % _v(under))

	var tris := 0
	for mi: MeshInstance3D in meshes:
		for s in mi.mesh.get_surface_count():
			var arr: Array = mi.mesh.surface_get_arrays(s)
			var idx: PackedInt32Array = arr[Mesh.ARRAY_INDEX]
			tris += (idx.size() if idx.size() else (arr[Mesh.ARRAY_VERTEX] as PackedVector3Array).size()) / 3
	_expect(tris <= b[5], "triangles within budget %d" % b[5], "%d" % tris)

	var want: Dictionary = b[6]
	var seen := {}
	for mi: MeshInstance3D in meshes:
		for s in mi.mesh.get_surface_count():
			var mat: Material = mi.get_active_material(s)
			if mat is BaseMaterial3D:
				seen[mat.resource_name] = mat.albedo_color.to_html(false).to_upper()
	for m in want:
		_expect(seen.get(m, "") == want[m], "colour %s = #%s" % [m, want[m]], "#%s" % seen.get(m, "missing"))
	root.free()


func _check_scene() -> void:
	var scene: Node3D = load("res://scenes/props_room.tscn").instantiate()
	var floor := scene.get_node("Floor") as MeshInstance3D
	var floor_box := _aabb_in(floor, scene)
	var floor_y := floor_box.position.y + floor_box.size.y # the floor's top surface
	print("   floor top at Y = %.4f, X %.2f to %.2f, Z %.2f to %.2f" % [floor_y, floor_box.position.x,
		floor_box.end.x, floor_box.position.z, floor_box.end.z])
	for b in BRIEF:
		var prop := scene.get_node(b[0]) as Node3D
		var box := _aabb_in(prop, scene)
		var gap := box.position.y - floor_y
		_expect(absf(gap) <= TOL, "%s sits on the floor" % b[0], "lowest point %.4f m above the floor's top" % gap)
		var inside := box.position.x >= floor_box.position.x and box.end.x <= floor_box.end.x \
			and box.position.z >= floor_box.position.z and box.end.z <= floor_box.end.z
		_expect(inside, "%s is over the floor" % b[0], "X %.2f to %.2f" % [box.position.x, box.end.x])
		_expect(prop.scale.is_equal_approx(Vector3.ONE), "%s node scale 1, 1, 1 in the scene" % b[0], "%s" % prop.scale)
	scene.free()


## The bounding box of every mesh under `node`, in the space of `space`.
func _aabb_in(node: Node3D, space: Node3D) -> AABB:
	var box := AABB()
	var first := true
	for mi in ([node] if node is MeshInstance3D else []) + _mesh_instances(node):
		var xf := _transform_to(mi, space)
		var b: AABB = xf * mi.mesh.get_aabb()
		box = b if first else box.merge(b)
		first = false
	return box


func _transform_to(node: Node3D, space: Node3D) -> Transform3D:
	var xf := Transform3D.IDENTITY
	var n: Node = node
	while n != space and n is Node3D:
		xf = (n as Node3D).transform * xf
		n = n.get_parent()
	return xf


func _mesh_instances(node: Node) -> Array:
	return _descendants(node).filter(func(n): return n is MeshInstance3D)


func _descendants(node: Node) -> Array:
	var out := []
	for c in node.get_children():
		out.append(c)
		out.append_array(_descendants(c))
	return out


func _expect(ok: bool, what: String, got: String) -> void:
	print("   %s  %s  (%s)" % ["ok  " if ok else "FAIL", what, got])
	if not ok:
		failures += 1


func _v(v: Vector3) -> String:
	return "(%.4f, %.4f, %.4f)" % [v.x, v.y, v.z]
