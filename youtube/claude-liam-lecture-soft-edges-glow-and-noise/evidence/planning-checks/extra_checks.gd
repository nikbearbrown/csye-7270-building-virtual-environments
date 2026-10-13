extends SceneTree
# extra_checks.gd: small claims that need a script, not a picture. Prints one RESULT line per check.
#   godot --path <scratch project> --script res://extra_checks.gd -- --film <abs path of the film folder>
#   U  what Godot reports for each kind of uniform: type, hint, hint string (a vec4 with source_color is a COLOR; a plain vec4 is not)
#   H  a hint_range does not clamp a value set from code, and the guarded softness shader survives a zero
#   M  the guard: max(0.0, 0.01) and max(0.15, 0.01) (arithmetic, run in GDScript for the record)

var FILM := ""

func _initialize() -> void:
	call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n):
		await process_frame

func run() -> void:
	var a := OS.get_cmdline_user_args()
	for i in range(a.size()):
		if a[i] == "--film":
			FILM = a[i + 1]
	root.size = Vector2i(320, 180)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})
	# U: uniform reflection
	var plain := Shader.new()
	plain.code = "shader_type canvas_item;\nuniform vec4 plain_vec4 = vec4(1.0);\nuniform vec4 hinted : source_color = vec4(1.0);\nuniform vec3 hinted3 : source_color = vec3(1.0);\nuniform vec3 plain_vec3 = vec3(1.0);\nuniform float ranged : hint_range(0.02, 0.4) = 0.15;\nuniform sampler2D tex : repeat_enable;\nvoid fragment() { COLOR = hinted * plain_vec4 * vec4(hinted3 * plain_vec3, 1.0) * ranged * texture(tex, UV); }\n"
	var lst: Array = []
	for u in plain.get_shader_uniform_list():
		lst.append({"name": u["name"], "type": u["type"], "type_name": type_string(u["type"]), "hint": u["hint"], "hint_string": u["hint_string"]})
	out("U-uniform-reflection", {"uniforms": lst, "reading": "type 20 = Color (the editor's colour picker), type 9 = Vector3, type 12 = Vector4 (number boxes), type 3 = float; hint 1 = range; a vec3 with source_color is a Color with the no-alpha hint"})
	# H: the hint does not clamp
	var sh := Shader.new()
	sh.code = FileAccess.get_file_as_string(FILM + "/lab-shaders/03-soft-width.gdshader")
	var mat := ShaderMaterial.new()
	mat.shader = sh
	var rect := ColorRect.new()
	rect.size = Vector2(160, 160)
	rect.material = mat
	root.add_child(rect)
	await frames(3)
	mat.set_shader_parameter("softness", 0.0)
	await frames(2)
	var stored0: Variant = mat.get_shader_parameter("softness")
	mat.set_shader_parameter("softness", 7.0)
	var stored7: Variant = mat.get_shader_parameter("softness")
	out("H-hint-does-not-clamp", {"hint": "hint_range(0.02, 0.4)", "stored_after_set_0": stored0, "stored_after_set_7": stored7,
		"reading": "the stored values come back unchanged: the range only guards the slider in the editor"})
	out("M-guard", {"max(0.0, 0.01)": maxf(0.0, 0.01), "max(0.15, 0.01)": maxf(0.15, 0.01)})
	quit(0)
