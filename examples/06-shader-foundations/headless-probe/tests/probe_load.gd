extends SceneTree

func _initialize() -> void:
	print("RENDERING_METHOD=", RenderingServer.get_current_rendering_method())
	print("RENDERING_DRIVER=", RenderingServer.get_current_rendering_driver_name())
	print("VIDEO_ADAPTER=", RenderingServer.get_video_adapter_name())
	print("RD_GLOBAL=", RenderingServer.get_rendering_device())
	for name in ["good", "syntax_error", "type_error", "undeclared", "bad_builtin"]:
		print("---- ", name)
		var sh: Shader = load("res://shaders/%s.gdshader" % name)
		print("LOADED=", sh != null)
		if sh == null:
			continue
		print("MODE=", sh.get_mode())
		print("CODE_LEN=", sh.code.length())
		var uniforms := sh.get_shader_uniform_list()
		print("UNIFORMS=", uniforms)
		var mat := ShaderMaterial.new()
		mat.shader = sh
		print("PARAM flash_amount=", mat.get_shader_parameter("flash_amount"))
		print("DEFAULT flash_amount=", RenderingServer.shader_get_parameter_default(sh.get_rid(), "flash_amount"))
		var spr := Sprite2D.new()
		spr.material = mat
		root.add_child(spr)
	await process_frame
	await process_frame
	print("PROBE_DONE")
	quit(0)
