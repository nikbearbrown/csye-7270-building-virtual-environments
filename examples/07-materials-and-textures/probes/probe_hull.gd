extends SceneTree
func _initialize() -> void:
	var path := "res://materials/dutch_ship_medium_hull.tres"
	var id := ResourceLoader.get_resource_uid(path)
	print("tres uid registered=", ResourceUID.id_to_text(id) if id != ResourceUID.INVALID_ID else "INVALID")
	for t in ["uid://b7r5mqhdf3j9k", "uid://b7r5mqhdf3kak"]:
		var i := ResourceUID.text_to_id(t)
		print(t, " has_id=", ResourceUID.has_id(i), " path=", ResourceUID.get_id_path(i) if ResourceUID.has_id(i) else "-")
	var ship: Node = (load("res://polyhaven/dutch_ship_medium_1k.gltf") as PackedScene).instantiate()
	for mi in ship.find_children("*", "MeshInstance3D", true, false):
		var m: BaseMaterial3D = mi.mesh.surface_get_material(0)
		print(mi.name, " class=", m.get_class(), " path=", m.resource_path, " ao_enabled=", m.ao_enabled, " metallic=", m.metallic, " roughness=", m.roughness, " cull=", m.cull_mode, " transparency=", m.transparency)
		if m is ORMMaterial3D:
			print("   orm_texture=", m.orm_texture.resource_path if m.orm_texture else "none", " ao_texture=", m.ao_texture.resource_path if m.ao_texture else "none")
	ship.free()
	quit(0)
