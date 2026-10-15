extends "res://tests/harness.gd"

const ASSETS := [
	{
		"name": "Lantern Gate", "path": "res://a3/lantern_gate.tscn",
		"size": Vector3(1.20, 2.85, 0.80), "primitives": 6, "triangles": 160,
		"materials": ["AgedBrass", "DarkWood", "EmberGlass"],
	},
	{
		"name": "Supply Stack", "path": "res://a3/supply_stack.glb",
		"size": Vector3(1.20, 1.10, 0.80), "primitives": 3, "triangles": 180,
		"materials": ["CrateBrass", "MarketTimber"],
	},
	{
		"name": "Lamp-oil Shrine", "path": "res://a3/oil_shrine.glb",
		"size": Vector3(0.80, 1.45, 0.80), "primitives": 3, "triangles": 120,
		"materials": ["OilGlow", "ShrineBrass", "ShrineStone"],
	},
]


func _meshes(node: Node) -> Array:
	return node.find_children("*", "MeshInstance3D", true, false)


func _measure(node: Node) -> Dictionary:
	var first := true
	var bounds := AABB()
	var triangles := 0
	var materials := {}
	var unit_scale := true
	for item: MeshInstance3D in _meshes(node):
		var box: AABB = item.global_transform * item.mesh.get_aabb()
		bounds = box if first else bounds.merge(box)
		first = false
		unit_scale = unit_scale and item.scale.is_equal_approx(Vector3.ONE)
		for surface in item.mesh.get_surface_count():
			var arrays = item.mesh.surface_get_arrays(surface)
			var indices = arrays[Mesh.ARRAY_INDEX]
			var vertices = arrays[Mesh.ARRAY_VERTEX]
			triangles += (indices.size() if indices != null and indices.size() > 0 else vertices.size()) / 3
			var mat = item.get_active_material(surface)
			if mat:
				materials[mat.resource_name] = true
	var names: Array = materials.keys()
	names.sort()
	return {"bounds": bounds, "triangles": triangles, "materials": names, "unit_scale": unit_scale}


func run() -> void:
	suite = "a3-assets"
	var observed_sizes := {}
	for spec in ASSETS:
		var packed: PackedScene = load(spec.path)
		var asset = packed.instantiate()
		root.add_child(asset)
		await process_frame
		var measured := _measure(asset)
		var bounds: AABB = measured.bounds
		var id: String = spec.name.to_lower().replace(" ", "-")
		check(id + "-size-upright-origin", bounds.size.distance_to(spec.size) <= 0.011 and absf(bounds.position.y) <= 0.011, {"position": str(bounds.position), "size": str(bounds.size), "expected": str(spec.size)})
		check(id + "-unit-scale", measured.unit_scale, {"mesh_count": _meshes(asset).size()})
		check(id + "-shape-and-triangle-budget", _meshes(asset).size() <= spec.primitives and measured.triangles <= spec.triangles, {"primitives": _meshes(asset).size(), "primitive_budget": spec.primitives, "triangles": measured.triangles, "triangle_budget": spec.triangles})
		check(id + "-materials", measured.materials == spec.materials, {"materials": measured.materials})
		observed_sizes[spec.name] = str(bounds.size)
		asset.queue_free()
		await process_frame

	var room = load("res://a3/lantern_gate_room.tscn").instantiate()
	root.add_child(room)
	await process_frame
	await physics_frame
	check("room-has-floor-light-camera", room.has_node("Floor") and room.has_node("Moon") and room.has_node("Camera3D"), {})
	var world_boxes: Array[AABB] = []
	for node_name in ["LanternGate", "SupplyStack", "OilShrine"]:
		var measured := _measure(room.get_node(node_name))
		world_boxes.append(measured.bounds)
	var on_floor := world_boxes.all(func(box): return absf(box.position.y) <= 0.011)
	var separated := world_boxes[0].end.x < world_boxes[1].position.x and world_boxes[1].end.x < world_boxes[2].position.x
	check("three-assets-on-floor-and-separated", on_floor and separated, {"boxes": world_boxes.map(func(box): return str(box))})
	check("three-assets-import-and-appear", observed_sizes.size() == 3 and world_boxes.size() == 3, {"sizes": observed_sizes})

	# Mutation: prove the scale predicate can fail, then restore it.
	var sample: MeshInstance3D = _meshes(room.get_node("SupplyStack"))[0]
	var saved := sample.scale
	sample.scale = Vector3(2.0, 1.0, 1.0)
	check("mutation-unapplied-scale-caught", not _measure(room.get_node("SupplyStack")).unit_scale)
	sample.scale = saved
	check("mutation-unapplied-scale-restored", _measure(room.get_node("SupplyStack")).unit_scale)

	room.queue_free()
	completed = true
