extends SceneTree
# Two small claims: (J) uniform names are case-sensitive; (K) get_shader_parameter returns null for a uniform never set from code
# (which is why a tween on it fails: see run-5a). Run: godot --path <project dir> --script res://verify6.gd
func _initialize() -> void: call_deferred("run")
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))
func frames(n: int) -> void:
	for i in range(n): await process_frame
func red() -> float:
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	return snappedf(img.get_pixel(img.get_width() / 2, img.get_height() / 2).r, 0.001)
func run() -> void:
	root.size = Vector2i(320, 180)
	var rect := ColorRect.new()
	rect.size = Vector2(320, 180)
	var sh := Shader.new()
	sh.code = "shader_type canvas_item;\nuniform float red : hint_range(0.0, 1.0) = 0.2;\nvoid fragment() { COLOR = vec4(red, 0.0, 0.0, 1.0); }\n"
	var mat := ShaderMaterial.new()
	mat.shader = sh
	rect.material = mat
	root.add_child(rect)
	await frames(3)
	out("K-never-set-reads-null", {"get_shader_parameter_red_before_any_set": str(mat.get_shader_parameter("red")), "pixel_red_is_default": red()})
	mat.set_shader_parameter("Red", 0.9)
	await frames(2)
	out("J-case-sensitive", {"after_set_Red_capital": red(), "expected_if_ignored": 0.2})
	mat.set_shader_parameter("red", 0.9)
	await frames(2)
	out("J2-exact-name-works", {"after_set_red": red()})
	quit(0)
