extends "res://tests/harness.gd"

const GateScene = preload("res://a3/lantern_gate.tscn")
const RoomScene = preload("res://a3/lantern_gate_room.tscn")

func _all(node: Node, klass: String) -> Array:
	return node.find_children("*", klass, true, false)

func _unit_scale(meshes: Array) -> bool:
	for mesh in meshes:
		if not mesh.scale.is_equal_approx(Vector3.ONE):
			return false
	return true

func _layers_ok(bodies: Array) -> bool:
	for body in bodies:
		if body.collision_layer != 4 or body.collision_mask != 0:
			return false
	return bodies.size() == 2

func run() -> void:
	suite = "a3-lantern-gate"
	var gate = GateScene.instantiate()
	root.add_child(gate)
	await process_frame
	await physics_frame

	var meshes := _all(gate, "MeshInstance3D")
	var bodies := _all(gate, "StaticBody3D")
	var shapes := _all(gate, "CollisionShape3D")
	check("suffix-created-two-static-bodies", bodies.size() == 2 and shapes.size() == 2, {"bodies": bodies.size(), "shapes": shapes.size()})
	check("prop-layer-and-mask", _layers_ok(bodies), {"layers": bodies.map(func(b): return b.collision_layer), "masks": bodies.map(func(b): return b.collision_mask)})

	var bounds := AABB()
	var first := true
	var triangles := 0
	var materials := {}
	for item: MeshInstance3D in meshes:
		var box: AABB = item.global_transform * item.mesh.get_aabb()
		bounds = box if first else bounds.merge(box)
		first = false
		for surface in item.mesh.get_surface_count():
			var arrays = item.mesh.surface_get_arrays(surface)
			var indices = arrays[Mesh.ARRAY_INDEX]
			var vertices = arrays[Mesh.ARRAY_VERTEX]
			triangles += (indices.size() if indices != null and indices.size() > 0 else vertices.size()) / 3
			var mat = item.get_active_material(surface)
			if mat:
				materials[mat.resource_name] = true
	var size := bounds.size
	check("size-axis-and-origin", size.distance_to(Vector3(1.20, 2.85, 0.80)) <= 0.01 and absf(bounds.position.y) <= 0.01, {"position": str(bounds.position), "size": str(size)})
	check("unit-mesh-scale", _unit_scale(meshes), {"mesh_count": meshes.size()})
	check("six-visible-primitives", meshes.size() == 6, {"visible_primitives": meshes.size(), "budget": 6})
	check("triangle-budget", triangles <= 160, {"triangles": triangles, "budget": 160})
	var material_names: Array = materials.keys()
	material_names.sort()
	check("material-names", material_names == ["AgedBrass", "DarkWood", "EmberGlass"], {"materials": material_names})

	var shape_sizes: Array = []
	for collision: CollisionShape3D in shapes:
		var pts: PackedVector3Array = collision.shape.points
		var min_v := Vector3(INF, INF, INF)
		var max_v := Vector3(-INF, -INF, -INF)
		for p in pts:
			min_v = min_v.min(p)
			max_v = max_v.max(p)
		shape_sizes.append((max_v - min_v).snapped(Vector3(0.01, 0.01, 0.01)))
	shape_sizes.sort_custom(func(a, b): return a.y < b.y)
	var collider_fit: bool = shape_sizes.size() == 2
	if collider_fit:
		collider_fit = shape_sizes[0].distance_to(Vector3(0.8, 0.32, 0.8)) <= 0.01
		collider_fit = collider_fit and shape_sizes[1].distance_to(Vector3(0.42, 2.55, 0.42)) <= 0.01
	check("collider-fit", collider_fit, {"sizes": shape_sizes.map(func(v): return str(v)), "cross_arm_collision": false})

	# Ordinary CharacterBody3D motion into the blocker: 120 pinned physics ticks.
	var stand_in := CharacterBody3D.new()
	stand_in.collision_layer = 2
	stand_in.collision_mask = 4
	var collision := CollisionShape3D.new()
	var capsule := CapsuleShape3D.new()
	capsule.radius = 0.25
	capsule.height = 1.2
	collision.shape = capsule
	stand_in.add_child(collision)
	stand_in.position = Vector3(-2.0, 0.6, 0.0)
	root.add_child(stand_in)
	await physics_frame
	for i in 120:
		stand_in.velocity = Vector3(2.0, 0.0, 0.0)
		stand_in.move_and_slide()
		await physics_frame
	check("static-blocker-stops-stand-in", stand_in.position.x < -0.39 and stand_in.position.x > -0.75, {"x_after_120_ticks": stand_in.position.x})

	# Placement: ray away from the gate, excluding all prop RIDs, must hit room floor at y=0.
	var room = RoomScene.instantiate()
	root.add_child(room)
	await process_frame
	await physics_frame
	var query := PhysicsRayQueryParameters3D.create(Vector3(1.5, 2.0, 1.5), Vector3(1.5, -2.0, 1.5), 1)
	for body in _all(room.get_node("LanternGate"), "StaticBody3D"):
		query.exclude.append(body.get_rid())
	var hit: Dictionary = room.get_world_3d().direct_space_state.intersect_ray(query)
	check("placed-on-floor", not hit.is_empty() and hit.collider.name == "Floor" and absf(hit.position.y) <= 0.02, {"hit": hit.collider.name if not hit.is_empty() else "none", "y": hit.position.y if not hit.is_empty() else null})

	# Two deliberate in-memory mutations: prove the predicates fail, then restore.
	var saved_scale: Vector3 = meshes[0].scale
	meshes[0].scale = Vector3(2, 1, 1)
	check("mutation-unapplied-scale-caught", not _unit_scale(meshes))
	meshes[0].scale = saved_scale
	check("mutation-unapplied-scale-restored", _unit_scale(meshes))
	var saved_layer: int = bodies[0].collision_layer
	bodies[0].collision_layer = 1
	check("mutation-wrong-layer-caught", not _layers_ok(bodies))
	bodies[0].collision_layer = saved_layer
	check("mutation-wrong-layer-restored", _layers_ok(bodies))

	stand_in.queue_free()
	room.queue_free()
	gate.queue_free()
	completed = true
