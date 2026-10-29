extends SceneTree
## Puts the weathered stone materials on the waystone's Stone surface and the
## teleport circle's DarkStone surface of props_room.tscn, as surface material
## overrides on the instanced meshes (CHANGE-BRIEF.md section 5), and saves the
## scene as the editor would. The .glb files and their .import files are not
## touched, so check_props.gd still reads the imported colours. It stops without
## saving if a surface does not hold the imported material it expects. Run once,
## from assignment-5/:
##   timeout 120 godot --headless --path godot --script res://tools/add_stone_overrides.gd

const SCENE := "res://scenes/props_room.tscn"
## instance, the mesh inside it, surface, the imported material there, the override
const OVERRIDES := [
	["Waystone", "Waystone", 0, "Stone", "res://materials/waystone_stone.tres"],
	["TeleportCircle", "TeleportCircle", 1, "DarkStone", "res://materials/circle_darkstone.tres"],
]


func _init() -> void:
	var root := (load(SCENE) as PackedScene).instantiate(PackedScene.GEN_EDIT_STATE_MAIN)
	for entry: Array in OVERRIDES:
		var instance := root.get_node(entry[0] as String)
		var mesh_instance := instance.get_node(entry[1] as String) as MeshInstance3D
		var surface: int = entry[2]
		var imported := mesh_instance.mesh.surface_get_material(surface)
		if imported == null or imported.resource_name != entry[3]:
			printerr("STOP %s/%s surface %d holds %s, not %s; nothing saved" % [entry[0], entry[1], surface, imported.resource_name if imported else "nothing", entry[3]])
			root.free()
			quit(1)
			return
		root.set_editable_instance(instance, true)
		mesh_instance.set_surface_override_material(surface, load(entry[4] as String) as Material)
		print("SET %s/%s surface %d (%s): %s" % [entry[0], entry[1], surface, entry[3], entry[4]])
	var scene := PackedScene.new()
	var err := scene.pack(root)
	if err == OK:
		err = ResourceSaver.save(scene, SCENE)
	print("SAVED %s: %s" % [SCENE, error_string(err)])
	root.free()
	quit(0 if err == OK else 1)
