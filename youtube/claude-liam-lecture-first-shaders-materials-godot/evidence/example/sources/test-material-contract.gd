extends SceneTree
var failures := 0
var count := 0
func check(label: String, ok: bool) -> void:
	count += 1
	print(("PASS " if ok else "FAIL ") + label)
	if not ok: failures += 1
func _initialize() -> void:
	var mode := OS.get_cmdline_user_args()[0] if OS.get_cmdline_user_args().size() else "baseline"
	var signal_shader := Shader.new()
	signal_shader.code = FileAccess.get_file_as_string("res://course-series/shaders/signal.gdshader")
	if mode == "parse": signal_shader.code = signal_shader.code.replace("shader_type spatial;","shader_type spatial")
	if mode == "rename": signal_shader.code = signal_shader.code.replace("activation","renamed_activation")
	var signal_names := {}
	for u in signal_shader.get_shader_uniform_list(): signal_names[str(u.name)] = u.type
	print("UNIFORM_TYPES ",JSON.stringify(signal_names))
	check("declared activation is float",signal_names.get("activation",-1)==TYPE_FLOAT)
	check("declared quiet_color is vec4",signal_names.get("quiet_color",-1)==TYPE_COLOR)
	check("declared active_color is vec4",signal_names.get("active_color",-1)==TYPE_COLOR)
	check("declared stripe_count is float",signal_names.get("stripe_count",-1)==TYPE_FLOAT)
	check("texture-free signal",not signal_shader.code.contains("sampler"))
	var paths := ["matte","coated"]
	var expected := [[Color(1,1,1,1),0.9,1.0,0.0],[Color(.45,.95,.72,1),.25,2.0,.4]]
	for i in range(2):
		var material: ShaderMaterial = load("res://course-series/materials/"+paths[i]+".tres")
		check(paths[i]+" shared shader",material.shader.resource_path=="res://course-series/shaders/surface.gdshader")
		var source := material.shader.code
		if mode=="color-hint": source=source.replace("color_map : source_color,","color_map :")
		check(paths[i]+" color hint",source.contains("color_map : source_color,"))
		check(paths[i]+" data without color hint",source.contains("roughness_map : filter_nearest;"))
		check(paths[i]+" two groups",source.count("group_uniforms")==2)
		var names := {}
		for u in material.shader.get_shader_uniform_list(): names[str(u.name)] = u.type
		for p in ["tint","roughness_gain","uv_scale","metallic_gain"]:
			check(paths[i]+" declared "+p,names.get(p,-1)==(TYPE_COLOR if p=="tint" else TYPE_FLOAT))
		for j in range(4):
			var p: String = ["tint","roughness_gain","uv_scale","metallic_gain"][j]
			var actual = material.get_shader_parameter(p)
			check(paths[i]+" value "+p,actual.is_equal_approx(expected[i][j]) if actual is Color else is_equal_approx(actual,expected[i][j]))
		for sampler in ["color_map","roughness_map"]:
			var texture: Texture2D = material.get_shader_parameter(sampler)
			var expected_path := "res://course-series/material-textures/" + ("gate-color.png" if sampler=="color_map" else "gate-roughness.png")
			check(paths[i]+" texture path "+sampler,texture.resource_path==expected_path)
			var config := ConfigFile.new(); check(paths[i]+" import readable "+sampler,config.load(expected_path+".import")==OK)
			for key in ["compress/mode","compress/normal_map","mipmaps/generate","detect_3d/compress_to"]:
				var wanted = {"compress/mode":0,"compress/normal_map":2,"mipmaps/generate":false,"detect_3d/compress_to":0}[key]
				check(paths[i]+" "+sampler+" "+key,config.get_value("params",key)==wanted)
			print("FORMAT ",sampler," ",texture.get_image().get_format()," dimensions ",texture.get_size())
	var helper=load("res://course-series/normal-calibration/normal-map-check.gd")
	var normal_image:=Image.load_from_file("res://course-series/material-textures/analytic-normal-gl.png")
	print("ANALYTIC_NORMAL ",JSON.stringify({"GL":helper.curl_ratio(normal_image,false),"DX":helper.curl_ratio(normal_image,true)}))
	print("RESULT %d checks / %d failures / %s" % [count,failures,mode])
	quit(1 if failures else 0)
