extends SceneTree
func _initialize() -> void:
	for n in ["good", "no_yup", "no_apply"]:
		var inst: Node = (load("res://column_%s.glb" % n) as PackedScene).instantiate()
		var mi: MeshInstance3D = inst.find_children("*", "MeshInstance3D", true, false)[0]
		var a: AABB = mi.transform * mi.mesh.get_aabb()
		print(n, ": node scale ", mi.scale, "  mesh AABB size ", mi.mesh.get_aabb().size, "  AABB in scene ", a.size)
		inst.free()
	quit()
