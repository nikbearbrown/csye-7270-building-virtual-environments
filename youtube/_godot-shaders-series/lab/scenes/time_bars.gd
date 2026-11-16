extends Node
# C15 scene: two ColorRects side by side with the same time-bar shader. The left one is present from the start; add_right() is called by --call-at.
var logical: Vector2
var code: String
func harness_setup(ctx: Dictionary) -> void:
	logical = ctx["logical"]
	code = ctx["shader_code"]
	make_bar(Vector2(80, 60), "Left")
func make_bar(pos: Vector2, nm: String) -> void:
	var r := ColorRect.new()
	r.name = nm
	r.position = pos
	r.size = Vector2(520, 600)
	var sh := Shader.new()
	sh.code = code
	var m := ShaderMaterial.new()
	m.shader = sh
	r.material = m
	add_child(r)
func add_right() -> void:
	make_bar(Vector2(680, 60), "Right")
