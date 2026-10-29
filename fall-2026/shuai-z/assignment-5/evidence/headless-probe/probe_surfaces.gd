extends SceneTree
## Lists every MeshInstance3D under props_room.tscn's Waystone and
## TeleportCircle, with each surface's imported material, to settle the
## surface indices and node names the CLAUDE.md draft left unconfirmed.
##
## From assignment-5/, against the godot/ project:
##   timeout 120 godot --headless --path godot --script "$PWD/evidence/headless-probe/probe_surfaces.gd"

func _init() -> void:
	var scene := (load("res://scenes/props_room.tscn") as PackedScene).instantiate()
	for prop: String in ["Waystone", "TeleportCircle"]:
		for node in _descendants(scene.get_node(prop)):
			if node is MeshInstance3D:
				var mesh := (node as MeshInstance3D).mesh
				var surfaces: PackedStringArray = []
				for i in mesh.get_surface_count():
					var material := mesh.surface_get_material(i)
					surfaces.append("%d %s (%s)" % [i, material.resource_name if material else "none", material.get_class() if material else "-"])
				print("PROBE %s: mesh '%s', surfaces %s" % [scene.get_path_to(node), mesh.resource_name, ", ".join(surfaces)])
	scene.free()
	quit(0)


func _descendants(node: Node) -> Array[Node]:
	var out: Array[Node] = [node]
	for child in node.get_children():
		out.append_array(_descendants(child))
	return out
