extends SceneTree
func _initialize() -> void:
	for name in ["modes_spatial", "modes_particles", "modes_sky", "modes_fog", "screen_tex", "screen_tex_old"]:
		var sh: Shader = load("res://shaders/%s.gdshader" % name)
		var u := sh.get_shader_uniform_list()
		print(name, " MODE=", sh.get_mode(), " UNIFORMS=", u.map(func(d): return "%s:type%d:hint%d" % [d.name, d.type, d.hint]))
	# VisualShader built in code
	var vs := VisualShader.new()
	vs.set_mode(VisualShader.MODE_CANVAS_ITEM)
	var p := VisualShaderNodeFloatParameter.new()
	p.parameter_name = "flash_amount"
	vs.add_node(VisualShader.TYPE_FRAGMENT, p, Vector2(0, 0), 2)
	var c := VisualShaderNodeColorConstant.new()
	c.constant = Color(1, 0, 0, 1)
	vs.add_node(VisualShader.TYPE_FRAGMENT, c, Vector2(0, 100), 3)
	var mix := VisualShaderNodeMix.new()
	mix.op_type = VisualShaderNodeMix.OP_TYPE_VECTOR_3D_SCALAR
	vs.add_node(VisualShader.TYPE_FRAGMENT, mix, Vector2(200, 0), 4)
	print("connect c->mix.b err=", vs.connect_nodes(VisualShader.TYPE_FRAGMENT, 3, 0, 4, 1))
	print("connect p->mix.weight err=", vs.connect_nodes(VisualShader.TYPE_FRAGMENT, 2, 0, 4, 2))
	print("connect mix->output.color err=", vs.connect_nodes(VisualShader.TYPE_FRAGMENT, 4, 0, 0, 0))
	print("VISUAL_SHADER_CODE_BEGIN")
	print(vs.code)
	print("VISUAL_SHADER_CODE_END")
	print("VS UNIFORMS=", vs.get_shader_uniform_list())
	quit(0)
