extends Node2D
# Capture C23 (beat B23): a square whose color follows a CurveTexture (a slow rise, a short hold, a long fall) read by the restarting ramp fract(TIME * 0.5): 05-curve-loop.
# 30 fps, 12 s (360 frames), one loop every 2 s. Square centred (0.5, 0.5), 0.5 of the height square.
const C = preload("res://scenes/scene_common.gd")

func _ready() -> void:
	C.stage()
	var vp := get_viewport_rect().size
	var side := vp.y * 0.5
	var sq := C.shaded_rect(C.shader_text("05-curve-loop.gdshader"), Vector2(vp.x * 0.5 - side / 2, vp.y * 0.5 - side / 2), Vector2(side, side))
	(sq.material as ShaderMaterial).set_shader_parameter("curve", C.breath_curve_texture())
	add_child(sq)
	if C.wants_verify():
		add_child(C.shaded_rect(C.ENCODER, Vector2(0, 0), Vector2(20, 20)))
