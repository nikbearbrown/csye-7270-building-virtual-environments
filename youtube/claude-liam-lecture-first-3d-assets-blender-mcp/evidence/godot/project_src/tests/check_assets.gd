# check_assets.gd - headless check of the three assets against the brief. Prints, per asset: bounding-box size, node scale,
# the longest axis, and the world-space gap between the lowest point of the bounding box and the floor.
#   godot --headless --path <project> --script res://tests/check_assets.gd --fixed-fps 60
# Failure demos pass a glb instead of the good asset (arguments after the "--" go to this script):
#   ... --fixed-fps 60 -- crate=res://variants/crate_origin_centre.glb@0,0.4,0
#   key = crate | lantern | coin (which brief row to compare with); @x,y,z = where the asset is placed (default 0,0,0 on the floor)
# The extra argument +origin also checks where the asset's own origin sits relative to its lowest point (the brief says: the base).
# Without it the check measures the lowest point of the bounding box only, which is what the first version of the film's check did.
extends SceneTree

const TOL := 0.001                      # metres
# The brief, as Godot sees it: X = width, Y = height (Godot is Y-up), Z = depth. Origin = centre of the underside.
const BRIEF := {
	"crate": Vector3(0.8, 0.8, 0.8),
	"lantern": Vector3(0.3, 0.5, 0.3),
	"coin": Vector3(0.3, 0.04, 0.3),
}
var failures := 0
var check_origin := false
var frames := 0
var scene: Node
var jobs: Array = []          # [key, label, node]


func _initialize() -> void:
	scene = (load("res://showcase.tscn") as PackedScene).instantiate()    # floor, one light, a camera
	root.add_child(scene)
	var args := Array(OS.get_cmdline_user_args())
	if args.has("+origin"):
		check_origin = true
		args.erase("+origin")
	if args.is_empty():
		for key in BRIEF:
			jobs.append([key, key, scene.get_node(key.capitalize())])      # the assets as placed in showcase.tscn
	else:
		for a in args:
			var key: String = a.get_slice("=", 0)
			var rest: String = a.get_slice("=", 1)
			var path: String = rest.get_slice("@", 0)
			var pos := Vector3.ZERO
			if rest.contains("@"):
				var p := rest.get_slice("@", 1).split(",")
				pos = Vector3(float(p[0]), float(p[1]), float(p[2]))
			var inst: Node3D = (load(path) as PackedScene).instantiate()
			scene.add_child(inst)
			inst.position = pos
			jobs.append([key, path.get_file(), inst])


func _process(_delta: float) -> bool:
	frames += 1
	if frames < 3:                       # let the scene enter the tree so global transforms are real
		return false
	var floor_y: float = (scene.get_node("Floor") as Node3D).global_position.y    # a PlaneMesh: its top is its position
	print("floor top at y = ", snappedf(floor_y, 0.0001), " | tolerance ", TOL, " m | Godot ", Engine.get_version_info().string)
	for j in jobs:
		_check(j[0], j[1], j[2], floor_y)
	if failures == 0:
		print("check passes: %d of %d assets match the brief" % [jobs.size(), jobs.size()])
	else:
		print("CHECK FAILS: %d of %d assets do not match the brief" % [failures, jobs.size()])
	quit(1 if failures > 0 else 0)
	return true


func _fmt(v: Vector3) -> String:
	return "(%s, %s, %s)" % [snappedf(v.x, 0.0001), snappedf(v.y, 0.0001), snappedf(v.z, 0.0001)]


func _axis(size: Vector3) -> String:
	var m := maxf(size.x, maxf(size.y, size.z))
	var names: Array = []
	for i in 3:
		if absf(size[i] - m) < TOL:
			names.append("XYZ"[i])
	return "=".join(names)


func _check(key: String, label: String, node: Node3D, floor_y: float) -> void:
	var meshes := node.find_children("*", "MeshInstance3D", true, false)
	var box := AABB()
	var first := true
	var scales: Array = []
	var node_list: Array = [node]
	node_list.append_array(meshes)
	for n in node_list:
		var sv := _fmt((n as Node3D).scale)
		if not scales.has(sv):
			scales.append(sv)
	for m in meshes:
		var mi := m as MeshInstance3D
		var wb: AABB = mi.global_transform * mi.get_aabb()
		box = wb if first else box.merge(wb)
		first = false
	var size := box.size
	var low := box.position.y
	var gap := low - floor_y
	var brief: Vector3 = BRIEF[key]
	var mesh_local := (meshes[0] as MeshInstance3D).get_aabb().size
	print("%s  [%s]" % [label, key])
	print("  bounding box size (x y z) = ", _fmt(size), " m | longest axis ", _axis(size), " | height (Y) ", snappedf(size.y, 0.0001), " m")
	print("  node scale = ", " ".join(scales), " | mesh size before node scale = ", _fmt(mesh_local))
	print("  lowest point y = ", snappedf(low, 0.0001), " | gap to floor = ", snappedf(gap, 0.0001), " m (0 sits on it; negative sinks; positive floats)")
	var origin_above := node.global_position.y - low
	if check_origin:
		print("  origin of the asset is ", snappedf(origin_above, 0.0001), " m above its lowest point (the brief says 0: the origin is the centre of the underside)")
	var why: Array = []
	var diff := (size - brief).abs()
	if maxf(diff.x, maxf(diff.y, diff.z)) > TOL:
		why.append("size %s is not the brief %s" % [_fmt(size), _fmt(brief)])
		var ratio := Vector3(size.x / brief.x, size.y / brief.y, size.z / brief.z)
		if absf(ratio.x - ratio.y) < 0.01 and absf(ratio.x - ratio.z) < 0.01:
			why.append("every axis is x%s the brief: a scale error" % snappedf(ratio.x, 0.01))
		elif absf(size.z - brief.y) < TOL and absf(size.y - brief.z) < TOL:
			why.append("the height is on Z, not Y: it stands along the wrong axis")
	for sv in scales:
		if sv != "(1.0, 1.0, 1.0)":
			why.append("node scale %s is not 1, 1, 1: the scale was not applied" % sv)
			break
	if check_origin and absf(origin_above) > TOL:
		why.append("the origin is %s m above the base: it sits on the floor only because the node was moved" % snappedf(origin_above, 0.0001))
	if absf(gap) > TOL:
		why.append("lowest point is %s m %s the floor: the origin is not at the base" % [snappedf(absf(gap), 0.0001), "below" if gap < 0.0 else "above"])
	if why.is_empty():
		print("  PASS ", label, ": size, scale 1, upright and sitting on the floor")
	else:
		failures += 1
		print("  FAIL ", label, ": ", "; ".join(why))
