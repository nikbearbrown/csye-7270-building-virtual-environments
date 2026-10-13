extends SceneTree
func _initialize() -> void:
	for c in ["GLTFPhysicsShape", "GLTFPhysicsBody"]:
		print(c, " exists in Godot ", Engine.get_version_info()["string"], ": ", ClassDB.class_exists(c))
	quit()
