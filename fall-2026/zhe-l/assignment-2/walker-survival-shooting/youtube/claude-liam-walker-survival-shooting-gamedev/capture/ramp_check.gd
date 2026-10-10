extends SceneTree
## Film-time re-check of the stair ramp (the 2026-10-08 raycast command was not
## saved, so this is a new check, not a replay). Loads the unmodified base.tscn,
## casts rays straight down at each step's front edge (nose) and records which
## collider is hit first and at what height. Exits nonzero if any nose height
## and ramp-surface height differ by more than 1 cm.

var base: Node3D
var waited := 0

func _initialize() -> void:
	base = load("res://base.tscn").instantiate()
	root.add_child(base)

func _physics_process(_d: float) -> bool:
	waited += 1
	if waited < 3:
		return false
	var space := base.get_world_3d().direct_space_state
	var ok := true
	for k in range(1, 7):
		var step: CSGBox3D = base.get_node("stairs/step_%d" % k)
		var top := step.position.y + step.size.y / 2.0
		var nose_z := step.position.z - step.size.z / 2.0
		var q := PhysicsRayQueryParameters3D.create(Vector3(-5.0, 3.0, nose_z + 0.001), Vector3(-5.0, -1.0, nose_z + 0.001))
		var hit := space.intersect_ray(q)
		var who: String = hit.collider.get_parent().name + "/" + hit.collider.name if hit else "none"
		var d := absf(hit.position.y - top) if hit else 999.0
		print("RAMP_CHECK step_%d nose_z=%.3f step_top_y=%.3f first_hit=%s hit_y=%.4f diff_m=%.4f" % [k, nose_z, top, who, hit.position.y if hit else -1.0, d])
		if d > 0.01:
			ok = false
	print("RAMP_CHECK result=", "PASS" if ok else "FAIL")
	quit(0 if ok else 1)
	return true
