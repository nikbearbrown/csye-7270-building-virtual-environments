## test_checkpoint_post.gd  — headless SceneTree test
##
## Run:  godot --headless --path godot --script tests/test_checkpoint_post.gd
## Exit 0 = all PASS, non-zero = failure count.
##
extends SceneTree

# ─── constants ───────────────────────────────────────────────────────────────

const POST_GLB     := "res://props/checkpoint_post.glb"
const GAME_TSCN    := "res://game.tscn"
const PLAYER_TSCN  := "res://player/player.tscn"

# Expected dimensions from Blender build script (Blender Z → Godot Y after Y-up export)
const EXPECT_HEIGHT := 1.80    # Blender Z 0→1.80  = Godot Y extent
const EXPECT_DEPTH  := 0.60    # Blender Y ±0.30   = Godot Z extent
const EXPECT_WIDTH  := 0.78    # Blender X −0.30→0.48 (base + pennant)
const TOL           := 0.01    # 1 cm tolerance

const PENNANT_ROOT_X := 0.08
const PENNANT_TIP_X  := 0.48
const PENNANT_MIN_Y  := 1.55
const FLOOR_TOL      := 0.02

# ─── state ───────────────────────────────────────────────────────────────────

var _fails      := 0
var _phys_frame := 0

# ─── entry ───────────────────────────────────────────────────────────────────

func _initialize() -> void:
	# Defer so nodes are fully in-tree before we inspect them.
	call_deferred("_start")


func _start() -> void:
	_test_prop_scene()

	var game := preload(GAME_TSCN).instantiate()
	root.add_child(game)
	physics_frame.connect(_on_physics_frame)


func _on_physics_frame() -> void:
	_phys_frame += 1
	if _phys_frame < 10:
		return
	physics_frame.disconnect(_on_physics_frame)
	_test_game_scene()
	quit(_fails)


# ─── helpers ─────────────────────────────────────────────────────────────────

func _pass(msg: String) -> void:
	print("PASS  ", msg)


func _fail(msg: String) -> void:
	print("FAIL  ", msg)
	_fails += 1


func _check(ok: bool, msg: String) -> void:
	if ok: _pass(msg)
	else:  _fail(msg)


func _approx(a: float, b: float, tol: float) -> bool:
	return abs(a - b) <= tol


# Collect all nodes of a given class under root_node (recursive).
func _collect(root_node: Node, cls) -> Array:
	var result := []
	for child in root_node.get_children():
		if is_instance_of(child, cls):
			result.append(child)
		result.append_array(_collect(child, cls))
	return result


# Return the transform of node relative to ancestor (walk the parent chain).
func _rel_transform(node: Node3D, ancestor: Node3D) -> Transform3D:
	var t := Transform3D.IDENTITY
	var cur: Node = node
	while cur != ancestor and cur != null:
		if cur is Node3D:
			t = (cur as Node3D).transform * t
		cur = cur.get_parent()
	return t


# Compute the merged AABB (in scene-root local space) of all MeshInstance3D
# nodes under root_node. Uses local-transform chain to avoid global_transform
# which requires the node to be inside the tree.
func _merged_aabb(root_node: Node3D) -> AABB:
	var meshes: Array = _collect(root_node, MeshInstance3D)
	var merged := AABB()
	var first  := true
	for mi: MeshInstance3D in meshes:
		if mi.mesh == null:
			continue
		var local_aabb: AABB = mi.get_aabb()
		var t := _rel_transform(mi, root_node)
		var p := local_aabb.position
		var s := local_aabb.size
		var corners := [
			t * p,
			t * Vector3(p.x + s.x, p.y,       p.z),
			t * Vector3(p.x,       p.y + s.y,  p.z),
			t * Vector3(p.x,       p.y,        p.z + s.z),
			t * Vector3(p.x + s.x, p.y + s.y,  p.z),
			t * Vector3(p.x + s.x, p.y,        p.z + s.z),
			t * Vector3(p.x,       p.y + s.y,  p.z + s.z),
			t * (p + s),
		]
		if first:
			merged = AABB(corners[0], Vector3.ZERO)
			first = false
		for c in corners:
			merged = merged.expand(c)
	return merged


# ─── part 1: prop scene static tests ─────────────────────────────────────────

func _test_prop_scene() -> void:
	print("\n--- Part 1: prop scene static tests ---")

	var ps  := preload(POST_GLB)
	var inst := ps.instantiate()
	root.add_child(inst)

	# ── Visual AABB ──────────────────────────────────────────────────────────
	var aabb := _merged_aabb(inst)
	print("  merged AABB size: ", aabb.size)

	_check(
		_approx(aabb.size.y, EXPECT_HEIGHT, TOL),
		"visual height (Godot Y = Blender Z) ≈ %.2f m  [got %.4f]" % [EXPECT_HEIGHT, aabb.size.y]
	)
	_check(
		_approx(aabb.size.z, EXPECT_DEPTH, TOL),
		"visual depth  (Godot Z = Blender Y) ≈ %.2f m  [got %.4f]" % [EXPECT_DEPTH, aabb.size.z]
	)
	_check(
		_approx(aabb.size.x, EXPECT_WIDTH, TOL),
		"visual width  (Godot X = Blender X) ≈ %.2f m  [got %.4f]" % [EXPECT_WIDTH, aabb.size.x]
	)

	# ── Unit scale on every MeshInstance3D ───────────────────────────────────
	var meshes: Array = _collect(inst, MeshInstance3D)
	var all_unit := true
	for mi: MeshInstance3D in meshes:
		if not (_approx(mi.scale.x, 1.0, 0.001) and
		        _approx(mi.scale.y, 1.0, 0.001) and
		        _approx(mi.scale.z, 1.0, 0.001)):
			all_unit = false
			print("  non-unit scale on: ", mi.name, " scale=", mi.scale)
	_check(all_unit, "all MeshInstance3D have unit scale  [%d meshes checked]" % meshes.size())

	# ── Materials: only PostMetal and FlagCloth (skip unnamed) ───────────────
	var mat_names: Dictionary = {}
	for mi: MeshInstance3D in meshes:
		for i in range(mi.mesh.get_surface_count()):
			var mat := mi.mesh.surface_get_material(i)
			if mat and mat.resource_name != "":
				mat_names[mat.resource_name] = true
	print("  named materials: ", mat_names.keys())
	_check(mat_names.has("PostMetal"), "PostMetal material present")
	_check(mat_names.has("FlagCloth"), "FlagCloth material present")
	var only_expected := true
	for nm in mat_names:
		if nm != "PostMetal" and nm != "FlagCloth":
			only_expected = false
	_check(only_expected, "no unexpected named materials  %s" % str(mat_names.keys()))

	# ── StaticBody3D with ConvexPolygonShape3D ────────────────────────────────
	var bodies: Array = _collect(inst, StaticBody3D)
	_check(bodies.size() >= 1, "at least one StaticBody3D present  [found %d]" % bodies.size())

	var found_convex := false
	var pts          := PackedVector3Array()
	for body: StaticBody3D in bodies:
		for child in body.get_children():
			if child is CollisionShape3D:
				var shape := (child as CollisionShape3D).shape
				if shape is ConvexPolygonShape3D:
					found_convex = true
					pts          = (shape as ConvexPolygonShape3D).points
					break
		if found_convex:
			break
	_check(found_convex, "StaticBody3D has a ConvexPolygonShape3D")

	if found_convex and pts.size() > 0:
		var cx_min := INF; var cx_max := -INF
		var cy_min := INF; var cy_max := -INF
		var cz_min := INF; var cz_max := -INF
		for pt in pts:
			cx_min = min(cx_min, pt.x); cx_max = max(cx_max, pt.x)
			cy_min = min(cy_min, pt.y); cy_max = max(cy_max, pt.y)
			cz_min = min(cz_min, pt.z); cz_max = max(cz_max, pt.z)
		print("  convex hull  X[%.3f,%.3f]  Y[%.3f,%.3f]  Z[%.3f,%.3f]"
			  % [cx_min, cx_max, cy_min, cy_max, cz_min, cz_max])

		# Covers base bottom (Y≈0) and pole top (Y≈1.8)
		_check(cy_min <= 0.02,  "collision Y_min ≤ 0.02 (covers base floor)")
		_check(
			cy_max >= EXPECT_HEIGHT - 0.05,
			"collision Y_max ≥ %.2f (covers pole top)  [got %.3f]" % [EXPECT_HEIGHT - 0.05, cy_max]
		)
		# Collision X should NOT reach the pennant tip (0.48); base is ±0.30
		var collider_x_at_pennant := -INF
		for pt in pts:
			if pt.y >= PENNANT_MIN_Y - TOL:
				collider_x_at_pennant = max(collider_x_at_pennant, pt.x)
		var pennant_length_inside := maxf(
			0.0,
			minf(PENNANT_TIP_X, collider_x_at_pennant) - PENNANT_ROOT_X
		)
		print("  pennant length inside collider: %.4f m" % pennant_length_inside)
		_check(
			pennant_length_inside <= TOL,
			"no pennant length lies inside collider  [overlap %.4f m]" % pennant_length_inside
		)

	# ── Prop shorter than player capsule ─────────────────────────────────────
	var player := preload(PLAYER_TSCN).instantiate()
	var capsule_height := -1.0
	for collision_shape in _collect(player, CollisionShape3D):
		var shape := (collision_shape as CollisionShape3D).shape
		if shape is CapsuleShape3D:
			capsule_height = (shape as CapsuleShape3D).height
			break
	_check(capsule_height > 0.0, "player scene has a capsule collision shape")
	_check(
		EXPECT_HEIGHT < capsule_height,
		"prop height %.2f m < player capsule %.2f m" % [EXPECT_HEIGHT, capsule_height]
	)
	player.free()

	inst.queue_free()
	print()


# ─── part 2: game.tscn physics + ray test ────────────────────────────────────

func _test_game_scene() -> void:
	print("--- Part 2: game.tscn physics + ray test ---")

	var space_state := root.get_world_3d().direct_space_state
	if space_state == null:
		_fail("could not get physics space state")
		return

	var game := root.get_child(root.get_child_count() - 1)
	var post := game.get_node_or_null("CheckpointPost") as Node3D
	if post == null:
		_fail("game scene has a CheckpointPost")
		return
	var post_world := post.global_position
	var exclusions: Array[RID] = []
	for body in _collect(post, StaticBody3D):
		exclusions.append((body as StaticBody3D).get_rid())

	# Start just above the base and exclude the post itself, so only the
	# supporting level geometry can satisfy this check.
	var from := post_world + Vector3(0.0, 0.5, 0.0)
	var to   := post_world + Vector3(0.0, -2.0, 0.0)
	var qry  := PhysicsRayQueryParameters3D.create(from, to)
	qry.exclude = exclusions
	var hit  := space_state.intersect_ray(qry)

	print("  ray from=%s  to=%s" % [str(from), str(to)])

	_check(not hit.is_empty(), "downward ray hits supporting floor with post excluded")

	if not hit.is_empty():
		var hit_y: float = hit.position.y
		print("  ray hit at y=%.4f  (post base y=%.4f)" % [hit_y, post_world.y])
		_check(
			absf(hit_y - post_world.y) <= FLOOR_TOL,
			"floor is within %.2f m of post base  [distance %.4f m]"
			% [FLOOR_TOL, absf(hit_y - post_world.y)]
		)

	print()
	print("Failures: %d" % _fails)
