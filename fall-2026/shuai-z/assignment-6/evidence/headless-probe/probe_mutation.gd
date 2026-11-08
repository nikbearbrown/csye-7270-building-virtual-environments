extends SceneTree
## What the Step 2 mutation and the other Godot 3 names in CHANGE-BRIEF.md's
## failure 1 actually do to a scene file in Godot 4.7.2:
##   1. the order Godot saves initial_velocity_min/_max and scale_min/_max in;
##   2. godot3_mutations.tscn: a Godot 3 line before or after the _max line,
##      and the Godot 3 flag names flag_disable_z and flag_align_y;
##   3. godot3_class.tscn: a Godot 3 Particles2D node with a sub-resource of
##      the Godot 3 type ParticlesMaterial.
##
## From assignment-6/:
##   timeout 120 godot --headless --path evidence/headless-probe --script res://probe_mutation.gd

func _initialize() -> void:
	var m := ParticleProcessMaterial.new()
	m.initial_velocity_min = 260.0
	m.initial_velocity_max = 420.0
	m.scale_min = 0.7
	m.scale_max = 1.0
	ResourceSaver.save(m, "user://saved_order.tres")
	var lines := FileAccess.get_file_as_string("user://saved_order.tres").split("\n")
	var kept := Array(lines).filter(func(l): return l.begins_with("initial_velocity") or l.begins_with("scale"))
	printerr("PROBE 1 Godot saves them in this order: %s" % [kept])

	var scene := (load("res://godot3_mutations.tscn") as PackedScene).instantiate()
	for name in ["VelocityFirst", "VelocityLast"]:
		var pm := (scene.get_node(name) as GPUParticles2D).process_material as ParticleProcessMaterial
		printerr("PROBE 2 %s: initial_velocity_min/_max %s/%s" % [name, pm.initial_velocity_min, pm.initial_velocity_max])
	var sm := (scene.get_node("ScaleFirst") as GPUParticles2D).process_material as ParticleProcessMaterial
	printerr("PROBE 2 ScaleFirst: scale_min/_max %s/%s" % [sm.scale_min, sm.scale_max])
	var fm := (scene.get_node("Flags") as GPUParticles2D).process_material as ParticleProcessMaterial
	printerr("PROBE 2 Flags (flag_disable_z = true, flag_align_y = true): particle_flag_disable_z %s, particle_flag_align_y %s (defaults false)" % [fm.particle_flag_disable_z, fm.particle_flag_align_y])
	scene.free()

	var packed := load("res://godot3_class.tscn") as PackedScene
	printerr("PROBE 3 godot3_class.tscn loaded as a PackedScene: %s" % (packed != null))
	if packed:
		var node := packed.instantiate()
		printerr("PROBE 3 the Particles2D node loads as a %s" % node.get_class())
		var mat: Variant = node.get("process_material")
		if mat:
			printerr("PROBE 3 the ParticlesMaterial sub-resource loads as a %s, initial_velocity_min %s" % [mat.get_class(), mat.get("initial_velocity_min")])
		else:
			printerr("PROBE 3 the node has no process_material")
		node.free()
	printerr("PROBE done; quitting with code 0")
	quit(0)
