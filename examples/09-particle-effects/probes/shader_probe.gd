extends SceneTree
func _initialize() -> void:
	var good := Shader.new()
	good.code = "shader_type particles;\nuniform float speed = 200.0;\nvoid start() {\n\tif (RESTART_VELOCITY) {\n\t\tVELOCITY = vec3(speed, 0.0, 0.0);\n\t}\n}\nvoid process() {\n\tCOLOR.a = 1.0 - clamp(CUSTOM.y / LIFETIME, 0.0, 1.0);\n}\n"
	print("good mode=", good.get_mode(), " uniforms=", good.get_shader_uniform_list())
	var bad := Shader.new()
	bad.code = "shader_type particles;\nvoid process() {\n\tVELOCITY = vec2(1.0);\n\tNOT_A_BUILTIN = 3.0;\n}\n"
	print("bad mode=", bad.get_mode(), " uniforms=", bad.get_shader_uniform_list())
	quit()
