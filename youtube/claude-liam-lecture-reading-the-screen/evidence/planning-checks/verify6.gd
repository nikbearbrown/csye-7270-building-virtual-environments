extends SceneTree
# verify6: what the Inspector is told about a uniform. The Inspector builds its widget from the property's hint (the same list the Shader reports).
#  R1 hint_range -> a range hint (a slider); source_color on a vec3 -> a colour hint without alpha (a colour picker); a plain float -> no hint
#  R2 a screen-texture uniform is not in the list at all (so there is nothing to show and nothing to set)
#  R3 there is no built-in overlay(): a call to it does not compile (the source course's "overlay" blend has to be written out)
# Run: ./run.sh verify6 [forward_plus|gl_compatibility]
const L = preload("res://rts_lib.gd")

func _initialize() -> void: call_deferred("run")

func run() -> void:
	L.out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method(), "adapter": RenderingServer.get_video_adapter_name()})
	var consts := {"RANGE": PROPERTY_HINT_RANGE, "COLOR_NO_ALPHA": PROPERTY_HINT_COLOR_NO_ALPHA, "NONE": PROPERTY_HINT_NONE, "ENUM": PROPERTY_HINT_ENUM}
	for n in ["05-gray.gdshader", "11-water.gdshader", "12-pool.gdshader", "07-spotlight.gdshader", "14-blur.gdshader"]:
		var sh := Shader.new()
		sh.code = L.shader_text(n)
		var rows: Array = []
		for u in sh.get_shader_uniform_list():
			var named := "other"
			for k in consts.keys():
				if int(u["hint"]) == int(consts[k]):
					named = k
			rows.append({"name": u["name"], "type": u["type"], "hint": u["hint"], "hint_is": named, "hint_string": u["hint_string"], "usage": u["usage"]})
		L.out("R1-uniform-list-" + n, {"uniforms": rows, "constants": consts})
	# R3: overlay()
	print("NOTE compiling a shader that calls overlay(); an engine error line should follow")
	var bad := Shader.new()
	bad.code = "shader_type canvas_item;\nvoid fragment() { COLOR.rgb = overlay(vec3(0.5), vec3(0.25)); }\n"
	var r := ColorRect.new()
	r.size = Vector2(100, 100)
	var m := ShaderMaterial.new()
	m.shader = bad
	r.material = m
	root.add_child(r)
	for i in 3:
		await process_frame
	print("NOTE end of the overlay() compile")
	quit(0)
