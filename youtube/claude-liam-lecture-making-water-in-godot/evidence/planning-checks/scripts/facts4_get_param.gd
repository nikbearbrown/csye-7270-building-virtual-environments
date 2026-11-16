extends SceneTree
# facts4: what does ShaderMaterial.get_shader_parameter return for a uniform that was never set from code? (CPU only)
func _initialize() -> void:
	var sh := Shader.new()
	sh.code = "shader_type spatial;\nuniform float wave_height : hint_range(0.0, 0.4) = 0.12;\nvoid fragment() { ALBEDO = vec3(wave_height); }\n"
	var m := ShaderMaterial.new()
	m.shader = sh
	print("never set: get_shader_parameter(wave_height) = ", m.get_shader_parameter("wave_height"), "  (typeof ", typeof(m.get_shader_parameter("wave_height")), ", TYPE_NIL = ", TYPE_NIL, ")")
	m.set_shader_parameter("wave_height", 0.2)
	print("after set_shader_parameter(0.2): ", m.get_shader_parameter("wave_height"))
	quit()
