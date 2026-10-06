extends SceneTree
func dump(n: Node, d: int) -> void:
	var extra := ""
	if n is CollisionShape3D and n.shape: extra = " shape=" + n.shape.get_class()
	if n is Node3D: extra += " scale=" + str((n as Node3D).scale)
	print("  ".repeat(d), n.get_class(), " [", n.name, "]", extra)
	for c in n.get_children(): dump(c, d + 1)
func _initialize() -> void:
	var inst: Node = (load("res://checkpoint_post.glb") as PackedScene).instantiate()
	dump(inst, 0)
	inst.free()
	quit()
