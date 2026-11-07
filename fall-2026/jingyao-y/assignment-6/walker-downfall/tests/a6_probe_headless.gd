extends SceneTree
## A6 headless facts (agent probe, 2026-11-07). Prints what Godot 4.7.2 reports
## headlessly about particle classes and node state; asserts nothing about the
## look. Run: ./scripts/run-test.sh a6_probe_headless.gd 60

func has_prop(c: String, p: String) -> bool:
	for d in ClassDB.class_get_property_list(c):
		if d.name == p: return true
	return false

func _init() -> void:
	print("version ", Engine.get_version_info().string)
	print("renderer ", RenderingServer.get_current_rendering_method(), " driver ", RenderingServer.get_current_rendering_driver_name(), " adapter '", RenderingServer.get_video_adapter_name(), "'")
	var props := {
		"GPUParticles3D": ["amount", "amount_ratio", "one_shot", "explosiveness", "randomness", "lifetime", "preprocess", "fixed_fps", "interpolate", "local_coords", "use_fixed_seed", "seed", "visibility_aabb", "draw_pass_1", "trail_enabled", "process_material", "speed_scale"],
		"CPUParticles3D": ["amount_ratio", "use_fixed_seed"],
		"ParticleProcessMaterial": ["emission_shape", "emission_sphere_radius", "direction", "spread", "initial_velocity_min", "initial_velocity_max", "initial_velocity", "gravity", "damping_min", "damping_max", "scale_min", "scale_max", "scale", "scale_random", "scale_curve", "color_ramp", "alpha_curve", "hue_variation_min", "hue_variation_max", "angle_min", "angle_max", "turbulence_enabled", "turbulence_noise_strength", "turbulence_noise_scale", "turbulence_influence_min", "turbulence_influence_max", "particle_flag_disable_z", "anim_speed_min"],
		"StandardMaterial3D": ["billboard_mode", "blend_mode", "transparency", "vertex_color_use_as_albedo", "disable_fog", "shading_mode", "albedo_texture", "use_particle_trails"],
		"GradientTexture2D": ["fill", "fill_from", "fill_to", "width", "height", "gradient"],
	}
	for c in props:
		for p in props[c]:
			print("prop ", c, ".", p, " ", has_prop(c, p))
	print("class ParticlesMaterial ", ClassDB.class_exists("ParticlesMaterial"))
	print("enum BILLBOARD_PARTICLES ", BaseMaterial3D.BILLBOARD_PARTICLES, " BLEND_MODE_MIX ", BaseMaterial3D.BLEND_MODE_MIX, " BLEND_MODE_ADD ", BaseMaterial3D.BLEND_MODE_ADD)
	print("enum EMISSION_SHAPE_POINT ", ParticleProcessMaterial.EMISSION_SHAPE_POINT, " SPHERE ", ParticleProcessMaterial.EMISSION_SHAPE_SPHERE, " FILL_RADIAL ", GradientTexture2D.FILL_RADIAL)
	# What the compatibility names do when set.
	var m := ParticleProcessMaterial.new()
	m.set("initial_velocity", Vector2(3.0, 6.0))
	print("compat initial_velocity type ", typeof(m.get("initial_velocity")), " -> min ", m.initial_velocity_min, " max ", m.initial_velocity_max)
	m.set("scale", Vector2(0.6, 1.2))
	print("compat scale -> min ", m.scale_min, " max ", m.scale_max)
	_run_nodes()

func _run_nodes() -> void:
	await process_frame
	var root3d := Node3D.new()
	root.add_child(root3d)
	var p := GPUParticles3D.new()
	p.one_shot = true
	p.amount = 14
	p.lifetime = 0.35
	p.process_material = ParticleProcessMaterial.new()
	p.draw_pass_1 = QuadMesh.new()
	var finished := [-1]
	var frame := [0]
	p.finished.connect(func() -> void: finished[0] = frame[0])
	root3d.add_child(p)
	p.emitting = true
	var t0 := Time.get_ticks_usec()
	for i in range(60):
		await process_frame
		frame[0] = i + 1
		if i in [0, 10, 20, 21, 22, 25, 30, 59]:
			print("frame ", i + 1, " emitting ", p.emitting, " finished_at ", finished[0])
	print("one_shot finished signal at frame ", finished[0], " (lifetime 0.35 s = 21 frames at 60)")
	print("60 frames wall ", (Time.get_ticks_usec() - t0) / 1000.0, " ms")
	p.amount_ratio = 0.5
	print("amount_ratio set 0.5 -> ", p.amount_ratio, " amount ", p.amount)
	paused = true
	await process_frame
	print("paused: can_process ", p.can_process(), " emitting ", p.emitting)
	paused = false
	quit(0)
