extends SceneTree

func _initialize() -> void:
	for name in ["good", "broken"]:
		var f: RDShaderFile = load("res://compute/%s.glsl" % name)
		print(name, " LOADED=", f != null)
		if f == null:
			continue
		var spirv := f.get_spirv()
		print(name, " COMPILE_ERROR=", spirv.compile_error_compute.strip_edges())
		print(name, " SPIRV_BYTES=", spirv.bytecode_compute.size())
	print("LOCAL_RD=", RenderingServer.create_local_rendering_device())
	quit(0)
