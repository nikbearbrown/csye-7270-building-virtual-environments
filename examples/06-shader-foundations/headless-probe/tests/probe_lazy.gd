extends SceneTree

func _initialize() -> void:
	print("STEP load")
	var sh: Shader = load("res://shaders/syntax_error.gdshader")
	print("STEP after_load")
	var mat := ShaderMaterial.new()
	mat.shader = sh
	print("STEP after_assign_to_material")
	var spr := Sprite2D.new()
	spr.material = mat
	root.add_child(spr)
	print("STEP after_add_child")
	await process_frame
	await process_frame
	print("STEP after_two_frames")
	var rid := sh.get_rid()
	print("STEP after_get_rid valid=", rid.is_valid())
	print("---- defaults on good shader")
	var good: Shader = load("res://shaders/good.gdshader")
	var gm := ShaderMaterial.new()
	gm.shader = good
	print("get_shader_parameter=", gm.get_shader_parameter("flash_amount"))
	print("get(prop)=", gm.get("shader_parameter/flash_amount"))
	print("can_revert=", gm.property_can_revert("shader_parameter/flash_amount"))
	print("revert=", gm.property_get_revert("shader_parameter/flash_amount"))
	print("revert color=", gm.property_get_revert("shader_parameter/flash_color"))
	print("RS default=", RenderingServer.shader_get_parameter_default(good.get_rid(), "flash_amount"))
	gm.set_shader_parameter("flash_amount", 0.75)
	print("after set=", gm.get_shader_parameter("flash_amount"))
	gm.set_shader_parameter("flash_amount", 7.0)
	print("after set out of hint range=", gm.get_shader_parameter("flash_amount"))
	print("---- rendering device")
	print("RS.get_rendering_device=", RenderingServer.get_rendering_device())
	var lrd := RenderingServer.create_local_rendering_device()
	print("RS.create_local_rendering_device=", lrd)
	print("---- viewport readback")
	var vp := SubViewport.new()
	vp.size = Vector2i(8, 8)
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	await process_frame
	await process_frame
	var tex := vp.get_texture()
	print("vp texture=", tex)
	var img := tex.get_image()
	print("vp image=", img)
	print("PROBE_DONE")
	quit(0)
