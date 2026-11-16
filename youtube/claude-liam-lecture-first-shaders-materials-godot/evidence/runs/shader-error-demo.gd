# Written for the film (not part of Assignment 5's example). Run raw: Godot prints a SHADER ERROR and exits 0.
# Through scripts/run-test.sh the same script exits 1. The 6 lines below are exactly what was run.
extends SceneTree
func _initialize() -> void:
	var shader := Shader.new()
	shader.code = "shader_type spatial\nuniform float activation = 0.0;"
	print("UNIFORMS ", shader.get_shader_uniform_list().size())
	quit()
