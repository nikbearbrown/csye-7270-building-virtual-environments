extends SceneTree
# Scratch verification C for "Drawing Shapes with Math" (not shown in the film): what the engine reports about the uniforms of the two shaders that
# have sliders, the data the Inspector builds its controls from. Run: godot --path <scratch project> --script res://verify-c.gd -- <film folder>
var film := ""
func _initialize() -> void: call_deferred("run")
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))
func run() -> void:
	var args := OS.get_cmdline_user_args()
	film = args[0] if args.size() > 0 else ""
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	for f in ["03-circle-slider.gdshader", "17-crosshair.gdshader"]:
		var sh := Shader.new()
		sh.code = FileAccess.get_file_as_string(film + "/lab-shaders/" + f)
		var n := 0
		for u in sh.get_shader_uniform_list():
			n += 1
			out("uniform", {"file": f, "name": u["name"], "type": u["type"], "type_is_float": u["type"] == TYPE_FLOAT, "hint": u["hint"],
				"hint_is_range": u["hint"] == PROPERTY_HINT_RANGE, "hint_string": u["hint_string"]})
		out("count", {"file": f, "uniforms": n})
	quit(0)
