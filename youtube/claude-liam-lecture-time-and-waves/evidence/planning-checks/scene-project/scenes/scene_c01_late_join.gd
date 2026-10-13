extends Node2D
# Capture C01 (beat B01): two squares run the same 02-pulse shader; the second is added late and is already in step with the first.
# 30 fps, 15 s (450 frames). The second square is added at frame 300 (10.0 s), where the narration says "Watch."
# Layout (fractions of the viewport): left square centred (0.30, 0.50), right square centred (0.70, 0.50), each 0.30 of the height square.
const C = preload("res://scenes/scene_common.gd")
const JOIN_FRAME := 300
var frame := 0
var late_square: ColorRect

func _ready() -> void:
	C.stage()
	var vp := get_viewport_rect().size
	var side := vp.y * 0.30
	var code := C.shader_text("02-pulse.gdshader")
	add_child(C.shaded_rect(code, Vector2(vp.x * 0.30 - side / 2, vp.y * 0.5 - side / 2), Vector2(side, side)))
	late_square = C.shaded_rect(code, Vector2(vp.x * 0.70 - side / 2, vp.y * 0.5 - side / 2), Vector2(side, side))
	if C.wants_verify():
		add_child(C.shaded_rect(C.ENCODER, Vector2(0, 0), Vector2(20, 20)))

func _process(_delta: float) -> void:
	frame += 1
	if frame == JOIN_FRAME:
		add_child(late_square)
		print("EVENT frame=%d second square added" % frame)
