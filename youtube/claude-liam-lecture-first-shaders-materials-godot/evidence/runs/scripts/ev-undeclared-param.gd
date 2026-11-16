extends SceneTree
# Written for the film: set_shader_parameter with a name the shader does not declare.
# Run while signal.gdshader declares renamed_activation instead of activation.
func _initialize() -> void:
	var m := ShaderMaterial.new()
	m.shader = load("res://course-series/shaders/signal.gdshader")
	var names := []
	for u in m.shader.get_shader_uniform_list(): names.append(str(u.name))
	print("DECLARED ", names)
	m.set_shader_parameter("activation", 0.7)
	print("READBACK activation = ", m.get_shader_parameter("activation"))
	print("READBACK renamed_activation = ", m.get_shader_parameter("renamed_activation"))
	quit()
