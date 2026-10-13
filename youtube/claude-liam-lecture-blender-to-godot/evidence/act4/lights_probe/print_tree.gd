extends SceneTree
func dump(n: Node, d: int) -> void:
	print("  ".repeat(d), n.get_class(), " [", n.name, "]")
	for c in n.get_children(): dump(c, d + 1)
func _initialize() -> void:
	for f in ["probe_lights_off", "probe_lights_on"]:
		print("== ", f, ".glb (fresh import)")
		dump((load("res://" + f + ".glb") as PackedScene).instantiate(), 0)
	quit()
