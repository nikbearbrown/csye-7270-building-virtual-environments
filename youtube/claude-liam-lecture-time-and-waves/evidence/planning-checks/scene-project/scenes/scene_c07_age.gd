extends Node2D
# Capture C07 (beat B07): the left square pulses on TIME (02-pulse). A second square is added late and pulses on an age that its own _process counts (01-age).
# 30 fps, 14 s (420 frames). The late square is added at frame 324 (10.8 s), where the narration says "Now the late square starts its pulse from the beginning."
# Layout: left square centred (0.30, 0.50), right square centred (0.70, 0.50), each 0.30 of the height square.
const C = preload("res://scenes/scene_common.gd")
const JOIN_FRAME := 324
const AGE_SCRIPT := "extends ColorRect\nvar age := 0.0\nfunc _process(delta):\n\tage += delta\n\tmaterial.set_shader_parameter(\"age\", age)\n"
var frame := 0
var late_square: ColorRect

func _ready() -> void:
	C.stage()
	var vp := get_viewport_rect().size
	var side := vp.y * 0.30
	add_child(C.shaded_rect(C.shader_text("02-pulse.gdshader"), Vector2(vp.x * 0.30 - side / 2, vp.y * 0.5 - side / 2), Vector2(side, side)))
	late_square = C.shaded_rect(C.shader_text("01-age.gdshader"), Vector2(vp.x * 0.70 - side / 2, vp.y * 0.5 - side / 2), Vector2(side, side))
	(late_square.material as ShaderMaterial).set_shader_parameter("age", 0.0)      # set once from code before the first draw
	var s := GDScript.new()
	s.source_code = AGE_SCRIPT
	s.reload()
	late_square.set_script(s)
	if C.wants_verify():
		add_child(C.shaded_rect(C.ENCODER, Vector2(0, 0), Vector2(20, 20)))

func _process(_delta: float) -> void:
	frame += 1
	if frame == JOIN_FRAME:
		add_child(late_square)
		print("EVENT frame=%d late square added (age starts at 0)" % frame)
