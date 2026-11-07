extends SceneTree
## Prints, for every rock surface, which material it ends up with: rock.glb itself, the Rock in
## showcase3d/prop_room.tscn, and both rocks in showcase3d/material_compare.tscn (CHANGE-BRIEF revision
## 2026-10-27). One JSON line per surface; prints only, asserts nothing. Headless: this shows which resource
## is assigned, not what it looks like.
##   ./scripts/run-test.sh inspect_rock_surfaces.gd 60   (from fall-2026/zhefan-z/assignment-5/)

const TARGETS := [
	["res://assets/models/rock.glb", "."],
	["res://showcase3d/prop_room.tscn", "Rock"],
	["res://showcase3d/material_compare.tscn", "RockDry"],
	["res://showcase3d/material_compare.tscn", "RockFrosted"],
]


func _initialize() -> void:
	call_deferred("run")


func describe(m: Material) -> Dictionary:
	if m == null:
		return {}
	var d := {"class": m.get_class(), "name": m.resource_name, "path": m.resource_path}
	if m is ShaderMaterial:
		d["shader"] = (m as ShaderMaterial).shader.resource_path
	return d


func run() -> void:
	await process_frame
	for t: Array in TARGETS:
		var scene: Node = load(t[0]).instantiate()
		var node := scene.get_node(t[1])
		for mi: MeshInstance3D in node.find_children("*", "MeshInstance3D", true, false):
			for s in mi.mesh.get_surface_count():
				print(JSON.stringify({"scene": t[0].get_file(), "instance": t[1], "mesh_node": mi.name, "surface": s,
					"surface_name": mi.mesh.surface_get_name(s), "imported": describe(mi.mesh.surface_get_material(s)),
					"override": describe(mi.get_surface_override_material(s)), "active": describe(mi.get_active_material(s))}))
		scene.free()
	quit(0)
