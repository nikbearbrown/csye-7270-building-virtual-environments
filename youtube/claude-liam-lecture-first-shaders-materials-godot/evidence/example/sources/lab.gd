extends "res://signal-garden/garden.gd"
func _ready() -> void:
	super._ready()
	pad_material.shader = load("res://course-series/shaders/signal.gdshader")
	var ambient_position: Vector3 = ambient.position
	remove_child(burst)
	burst.queue_free()
	remove_child(ambient)
	ambient.queue_free()
	burst = load("res://course-series/effects/burst.tscn").instantiate()
	ambient = load("res://course-series/effects/ambient.tscn").instantiate()
	add_child(burst)
	add_child(ambient)
	ambient.position = ambient_position
	var observer: Node = load("res://course-series/verification.gd").new()
	observer.name = "Verification"
	add_child(observer)
	# Two decorative specimen blocks are source-evidence, not extra collision rules.
	for index in range(2):
		var specimen := make_box("MaterialSpecimen" + str(index), Vector3(0.65, 0.65, 0.65), Vector3(2.6 + index * 1.1, 0.35, -2), Color.WHITE, false)
		specimen.material_override = load("res://course-series/materials/" + ("matte.tres" if index == 0 else "coated.tres"))
	if FileAccess.file_exists("res://course-series/animations/idle.tres"):
		var library := AnimationLibrary.new()
		for state_name in ["idle", "walk", "charge", "celebrate"]:
			library.add_animation(state_name, load("res://course-series/animations/" + state_name + ".tres"))
		rig.animator.remove_animation_library("")
		rig.animator.add_animation_library("", library)
		rig.animator.play("idle")
