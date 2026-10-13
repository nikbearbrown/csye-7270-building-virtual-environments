extends Node2D
# Capture C28 (beat B28): the 07-travel stripes slide right at speed 0.5 (frequency 3); at frame 330 (11.0 s) the speed becomes -0.5 and they slide left.
# 30 fps, 13 s (390 frames). The Lab rect: the shader fills the whole frame. A step in speed shows no pop at 11.0 s because 2 x speed x frequency x TIME
# = 2 x 0.5 x 3 x 11.0 = 33 whole cycles (the picture is the same just before and just after the change); the label 'speed -0.5' is an overlay.
const C = preload("res://scenes/scene_common.gd")
var frame := 0
var rect: ColorRect

func _ready() -> void:
	C.stage()
	var vp := get_viewport_rect().size
	rect = C.shaded_rect(C.shader_text("07-travel.gdshader"), Vector2.ZERO, vp)
	add_child(rect)
	if C.wants_verify():
		var enc := C.shaded_rect(C.ENCODER, Vector2(0, 0), Vector2(20, 20))
		add_child(enc)

func _process(_delta: float) -> void:
	frame += 1
	if frame == 330:
		(rect.material as ShaderMaterial).set_shader_parameter("speed", -0.5)
		print("EVENT frame=%d speed -0.5" % frame)
