extends SceneTree
## Assignment 3 headless check: the three .glb assets against CHANGE-BRIEF.md, and the prop room scene.
##   timeout 120 Godot_v4.7.2-stable_win64_console.exe --headless --path . --script res://tests/test_a3_assets.gd --fixed-fps 60
## Prints one JSON line per check and "A3 ASSET CHECK: N checks / F failures"; exit code 1 on any failure.
## Brief values are copied by hand from fall-2026/zhefan-z/assignment-3/CHANGE-BRIEF.md (version 1); the
## script does not read the Markdown. Godot X = width, Y = height, Z = depth (glTF +Y Up export).

const TOL := 0.02
const ASSETS := {
	"rock": {"path": "res://assets/models/rock.glb", "size": Vector3(1.0, 0.7, 0.8), "tris": 200,
		"albedo": {"Rock_Main": "343539", "Rock_Top": "797069"}},
	"crystal": {"path": "res://assets/models/crystal.glb", "size": Vector3(0.35, 0.6, 0.35), "tris": 100,
		"albedo": {"Crystal": "3558c8"}},
	"chest": {"path": "res://assets/models/chest.glb", "size": Vector3(0.8, 0.6, 0.5), "tris": 150,
		"albedo": {"Chest_Wood": "8a5a2b", "Chest_Gold": "d4a73a"}},
}
const SCENE := "res://showcase3d/prop_room.tscn"
const MAGE_HEIGHT := 1.45
const MAGE_VISIBLE_ROWS := 64      # mage_idle.png: opaque rows 3..66 of 69 (alpha >= 128), measured 2026-10-14
const MAGE_ROWS_BELOW_FEET := 2

var count := 0
var failures := 0


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	count += 1
	if not passed:
		failures += 1
	print(JSON.stringify({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed}))


func v3(v: Vector3) -> Array:
	return [snappedf(v.x, 0.0001), snappedf(v.y, 0.0001), snappedf(v.z, 0.0001)]


func meshes_of(node: Node) -> Array[MeshInstance3D]:
	var out: Array[MeshInstance3D] = []
	if node is MeshInstance3D:
		out.append(node)
	for c in node.get_children():
		out.append_array(meshes_of(c))
	return out


## Exact world-space vertex bounds, optionally only for surfaces using one material.
func world_bounds(node: Node, material_name := "") -> AABB:
	var box := AABB()
	var have := false
	for mi: MeshInstance3D in meshes_of(node):
		for s in mi.mesh.get_surface_count():
			if material_name != "" and mi.get_active_material(s).resource_name != material_name:
				continue
			for v in mi.mesh.surface_get_arrays(s)[Mesh.ARRAY_VERTEX]:
				var p: Vector3 = mi.global_transform * v
				box = box.expand(p) if have else AABB(p, Vector3.ZERO)
				have = true
	return box


func triangles(node: Node) -> int:
	var n := 0
	for mi: MeshInstance3D in meshes_of(node):
		for s in mi.mesh.get_surface_count():
			var idx: int = mi.mesh.surface_get_array_index_len(s)
			n += (idx if idx > 0 else mi.mesh.surface_get_array_len(s)) / 3
	return n


func is_clean(t: Transform3D) -> bool:
	return t.basis.is_equal_approx(Basis.IDENTITY)


func check_asset(key: String, spec: Dictionary) -> void:
	var inst: Node3D = load(spec.path).instantiate()
	root.add_child(inst)
	var box := world_bounds(inst)
	var want: Vector3 = spec.size
	var d := (box.size - want).abs()
	check(key + ".size", d.x <= TOL and d.y <= TOL and d.z <= TOL,
		{"size_xyz": v3(box.size), "brief_xyz": v3(want), "tolerance": TOL})
	# The axis whose extent is closest to the brief's height is the one the asset stands along.
	var diffs := [absf(box.size.x - want.y), absf(box.size.y - want.y), absf(box.size.z - want.y)]
	var stands: String = ["X", "Y", "Z"][diffs.find(diffs.min())]
	check(key + ".upright", stands == "Y" and absf(box.position.y) <= TOL,
		{"height_axis": stands, "lowest_y": snappedf(box.position.y, 0.0001)})

	var scales := {inst.name: v3(inst.scale)}
	var clean := is_clean(inst.transform)
	for mi: MeshInstance3D in meshes_of(inst):
		scales[mi.name] = v3(mi.scale)
		clean = clean and is_clean(mi.transform)
	check(key + ".node_scale", clean, {"scales": scales, "identity_basis": clean})

	var tris := triangles(inst)
	check(key + ".triangles", tris <= spec.tris, {"triangles": tris, "budget": spec.tris})

	var albedo := {}
	var albedo_ok := true
	for mi: MeshInstance3D in meshes_of(inst):
		for s in mi.mesh.get_surface_count():
			var mat := mi.get_active_material(s) as StandardMaterial3D
			var want_c := Color.html(spec.albedo.get(mat.resource_name, "000000"))
			var got: Color = mat.albedo_color
			albedo[mat.resource_name] = {"got": got.to_html(false), "brief": want_c.to_html(false),
				"metallic": snappedf(mat.metallic, 0.001), "roughness": snappedf(mat.roughness, 0.001)}
			albedo_ok = albedo_ok and mat.resource_name in spec.albedo and absf(got.r - want_c.r) <= 2.0 / 255.0 \
				and absf(got.g - want_c.g) <= 2.0 / 255.0 and absf(got.b - want_c.b) <= 2.0 / 255.0
	check(key + ".albedo", albedo_ok, albedo)

	if key == "crystal":
		var mat := meshes_of(inst)[0].get_active_material(0) as StandardMaterial3D
		check(key + ".emission", mat.emission_enabled and mat.emission != Color.BLACK,
			{"enabled": mat.emission_enabled, "emission": mat.emission.to_html(false),
				"energy": snappedf(mat.emission_energy_multiplier, 0.001)})
	if key == "chest":
		var gold := world_bounds(inst, "Chest_Gold")
		var wood := world_bounds(inst, "Chest_Wood")
		check(key + ".front_plus_z", gold.end.z > wood.end.z,
			{"gold_max_z": snappedf(gold.end.z, 0.0001), "wood_max_z": snappedf(wood.end.z, 0.0001)})
	inst.queue_free()


func count_lights(node: Node) -> int:
	var n := 1 if node is Light3D else 0
	for c in node.get_children():
		n += count_lights(c)
	return n


func check_scene() -> void:
	var scene: Node3D = load(SCENE).instantiate()
	root.add_child(scene)
	check("scene.one_light", count_lights(scene) == 1, {"lights": count_lights(scene)})
	for n in ["Rock", "Crystal", "Chest"]:
		var box := world_bounds(scene.get_node(n))
		check("scene." + n.to_lower() + "_on_floor", absf(box.position.y) <= TOL,
			{"lowest_y": snappedf(box.position.y, 0.0001), "node_position": v3(scene.get_node(n).position)})
	var mage: Sprite3D = scene.get_node("Mage")
	var px := mage.pixel_size * mage.scale.y
	var tex_h := mage.texture.get_height()
	var height := MAGE_VISIBLE_ROWS * px
	var feet := mage.global_position.y - (tex_h / 2.0 - MAGE_ROWS_BELOW_FEET) * px
	check("scene.mage_height", absf(height - MAGE_HEIGHT) <= TOL and absf(feet) <= TOL,
		{"visible_height": snappedf(height, 0.0001), "feet_y": snappedf(feet, 0.0001), "pixel_size": mage.pixel_size,
			"texture_px": [mage.texture.get_width(), tex_h], "note": "computed from pixel size and measured rows, not rendered"})
	var cam: Camera3D = scene.get_node("Camera")
	print(JSON.stringify({"info": "camera", "position": v3(cam.global_position), "forward": v3(-cam.global_basis.z)}))
	scene.queue_free()


func run() -> void:
	for key in ASSETS:
		check_asset(key, ASSETS[key])
	check_scene()
	print("A3 ASSET CHECK: %d checks / %d failures" % [count, failures])
	quit(1 if failures > 0 else 0)
