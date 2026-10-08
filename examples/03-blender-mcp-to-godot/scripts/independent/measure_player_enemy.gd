extends SceneTree
func merged_aabb(n: Node, xf: Transform3D, acc: Array) -> void:
	var t := xf
	if n is Node3D:
		t = xf * (n as Node3D).transform
	if n is MeshInstance3D and (n as MeshInstance3D).mesh:
		var a: AABB = t * (n as MeshInstance3D).mesh.get_aabb()
		if acc.is_empty(): acc.append(a)
		else: acc[0] = acc[0].merge(a)
	for c in n.get_children():
		merged_aabb(c, t, acc)
func _initialize() -> void:
	for p in ["res://player/player.glb", "res://enemy/enemy.glb", "res://player/player.tscn", "res://coin/coin.tscn"]:
		var s: PackedScene = load(p)
		var inst := s.instantiate()
		var acc := []
		merged_aabb(inst, Transform3D.IDENTITY, acc)
		print(p, " aabb=", acc[0] if not acc.is_empty() else "none")
		inst.free()
	var pl: Node = (load("res://player/player.tscn") as PackedScene).instantiate()
	for c in pl.find_children("*", "CollisionShape3D", true, false):
		print("player collider ", c.name, " ", c.shape, " ", c.shape.get("radius"), " ", c.shape.get("height"), " pos ", c.position)
	pl.free()
	quit()
