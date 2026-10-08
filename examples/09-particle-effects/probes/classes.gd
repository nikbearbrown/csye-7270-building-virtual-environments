extends SceneTree
func has_prop(c: String, p: String) -> bool:
	for d in ClassDB.class_get_property_list(c):
		if d.name == p: return true
	return false
func _initialize() -> void:
	for c in ["GPUParticles2D", "CPUParticles2D", "GPUParticles3D", "CPUParticles3D"]:
		var out := []
		for p in ["process_material", "sub_emitter", "trail_enabled", "collision_base_size", "turbulence_enabled", "emission_shape", "fixed_fps", "interpolate", "fract_delta", "preprocess", "explosiveness", "randomness", "local_coords", "draw_order", "amount_ratio", "visibility_rect", "visibility_aabb", "use_fixed_seed", "seed"]:
			out.append(p + "=" + str(has_prop(c, p)))
		print(c, ": ", ", ".join(out))
	for p in ["sub_emitter_mode", "sub_emitter_frequency", "sub_emitter_amount_at_end", "sub_emitter_amount_at_collision", "sub_emitter_amount_at_start", "sub_emitter_keep_velocity", "turbulence_enabled", "collision_mode", "attractor_interaction_enabled", "scale_curve", "color_ramp", "spread", "gravity", "initial_velocity_min", "emission_shape"]:
		print("ParticleProcessMaterial.", p, "=", has_prop("ParticleProcessMaterial", p))
	var m := ParticleProcessMaterial.new()
	print("SubEmitterMode enum: DISABLED=", ParticleProcessMaterial.SUB_EMITTER_DISABLED, " CONSTANT=", ParticleProcessMaterial.SUB_EMITTER_CONSTANT, " AT_END=", ParticleProcessMaterial.SUB_EMITTER_AT_END, " AT_COLLISION=", ParticleProcessMaterial.SUB_EMITTER_AT_COLLISION, " AT_START=", ParticleProcessMaterial.SUB_EMITTER_AT_START)
	print("defaults: spread=", m.spread, " gravity=", m.gravity, " GPUParticles2D amount default=", GPUParticles2D.new().amount, " lifetime=", GPUParticles2D.new().lifetime, " emitting=", GPUParticles2D.new().emitting, " fixed_fps=", GPUParticles2D.new().fixed_fps)
	quit(0)
