extends SceneTree
func _initialize() -> void:
	for n in ["yup_on", "yup_off"]:
		var inst: Node = (load("res://box_%s.glb" % n) as PackedScene).instantiate()
		var mi: MeshInstance3D = inst.find_children("*", "MeshInstance3D", true, false)[0]
		print(n, ": Godot extents X, Y, Z = ", mi.mesh.get_aabb().size)
		inst.free()
	quit()
