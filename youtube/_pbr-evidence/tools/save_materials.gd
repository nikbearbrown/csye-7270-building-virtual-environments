extends SceneTree
## Saves the three demo materials (the same values the "three" capture uses) as Godot text resources.
func _init() -> void:
	var specs := {"plastic": [Color("#D97757"), 0.0, 0.35], "gold": [Color(1.0, 0.78, 0.34), 1.0, 0.2], "rubber": [Color("#2E2C2A"), 0.0, 0.9]}
	for k in specs:
		var m := StandardMaterial3D.new()
		m.resource_name = k
		m.albedo_color = specs[k][0]; m.metallic = specs[k][1]; m.roughness = specs[k][2]
		var err := ResourceSaver.save(m, "res://evidence/materials/%s.tres" % k)
		print("SAVED %s err=%d" % [k, err])
	quit(0)
