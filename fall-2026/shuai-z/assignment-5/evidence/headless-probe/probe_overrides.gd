extends SceneTree
## Loads props_room.tscn as the game does and lists, for every surface of every
## mesh under the three props, the imported material, the scene's override if
## any, and the material that is actually used. It reads the scene and writes
## nothing.
##
## From assignment-5/, against the godot/ project:
##   timeout 120 godot --headless --path godot --script "$PWD/evidence/headless-probe/probe_overrides.gd"


func _init() -> void:
	var scene := (load("res://scenes/props_room.tscn") as PackedScene).instantiate()
	for prop: String in ["Spikes", "Waystone", "TeleportCircle"]:
		for node in _descendants(scene.get_node(prop)):
			if node is MeshInstance3D:
				var mesh_instance := node as MeshInstance3D
				for i in mesh_instance.mesh.get_surface_count():
					var imported := mesh_instance.mesh.surface_get_material(i)
					var override := mesh_instance.get_surface_override_material(i)
					var active := mesh_instance.get_active_material(i)
					print("PROBE %s surface %d: imported %s; override %s; active %s %s" % [
						scene.get_path_to(node), i,
						imported.resource_name if imported else "none",
						override.resource_path if override else "none",
						active.get_class() if active else "none",
						active.resource_path if active and active.resource_path != "" else (active.resource_name if active else "")])
	scene.free()
	quit(0)


func _descendants(node: Node) -> Array[Node]:
	var out: Array[Node] = [node]
	for child in node.get_children():
		out.append_array(_descendants(child))
	return out
