extends Node2D
# Capture C18 (beat B18): five squares share ONE ShaderMaterial (03-dials: amplitude 0.5, speed 0.5) and differ only by an instance uniform, offset = 0, 0.2, 0.4, 0.6, 0.8.
# 30 fps, 12 s (360 frames). Squares are 0.13 of the width, centred at x = 0.18, 0.34, 0.50, 0.66, 0.82 and y = 0.50.
# The GDScript the beat shows is exactly the loop in _ready below (two lines).
const C = preload("res://scenes/scene_common.gd")

func _ready() -> void:
	C.stage()
	var vp := get_viewport_rect().size
	var side := vp.x * 0.13
	var shader := Shader.new()
	shader.code = C.shader_text("03-dials.gdshader")
	var mat := ShaderMaterial.new()
	mat.shader = shader
	for i in 5:
		var r := ColorRect.new()
		r.size = Vector2(side, side)
		r.position = Vector2(vp.x * (0.18 + 0.16 * i) - side / 2, vp.y * 0.5 - side / 2)
		r.material = mat
		add_child(r)
	for i in 5:
		get_child(i).set_instance_shader_parameter("offset", i / 5.0)
	if C.wants_verify():
		add_child(C.shaded_rect(C.ENCODER, Vector2(0, 0), Vector2(20, 20)))
