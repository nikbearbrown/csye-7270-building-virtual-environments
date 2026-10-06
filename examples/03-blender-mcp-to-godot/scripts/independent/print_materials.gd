extends SceneTree
func _initialize() -> void:
	var inst: Node = (load("res://checkpoint_post.glb") as PackedScene).instantiate()
	for mi in inst.find_children("*", "MeshInstance3D", true, false):
		for i in mi.mesh.get_surface_count():
			var m: Material = mi.mesh.surface_get_material(i)
			print(mi.name, " surface ", i, ": ", m.get_class(), " resource_name=", m.resource_name, " cull_mode=", m.get("cull_mode"))
	inst.free()
	quit()
