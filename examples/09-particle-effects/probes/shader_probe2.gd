extends SceneTree
func _initialize() -> void:
	var s: Shader = load("res://shaders/drift.gdshader")
	print("mode=", s.get_mode(), " (MODE_PARTICLES=", Shader.MODE_PARTICLES, ") uniforms=", s.get_shader_uniform_list().map(func(u): return u.name))
	var g := GPUParticles2D.new()
	var m := ShaderMaterial.new(); m.shader = s
	g.process_material = m
	root.add_child(g)
	await process_frame
	print("assigned ok, emitting=", g.emitting)
	quit()
