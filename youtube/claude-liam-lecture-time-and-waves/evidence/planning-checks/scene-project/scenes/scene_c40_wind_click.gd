extends Node2D
# Capture C40 (beat B40): a calm banner (13-banner, wind 0). A scripted mouse click at frame 135 (4.5 s) sets wind to 1 and a tween brings it back to 0 over 4 s.
# 30 fps, 14 s (420 frames). Banner centred (0.50, 0.50) at 0.55 of the width. The label "scripted input" stays on screen (added by the ShaderLab overlay, not here).
# The GDScript the beat shows is the five lines of _unhandled_input below (up to the print), word for word.
const C = preload("res://scenes/scene_common.gd")
const CLICK_FRAME := 135
var frame := 0
var banner: Sprite2D

func _ready() -> void:
	C.stage()
	var vp := get_viewport_rect().size
	banner = C.shaded_sprite(C.banner_texture(), "13-banner.gdshader", Vector2(vp.x * 0.5, vp.y * 0.5), vp.x * 0.55 / 256.0)
	add_child(banner)
	if C.wants_verify():
		add_child(C.shaded_rect(C.ENCODER, Vector2(0, 0), Vector2(20, 20)))

func _unhandled_input(event):
	if event is InputEventMouseButton and event.pressed:
		var m = banner.material
		m.set_shader_parameter("wind", 1.0)
		create_tween().tween_property(m, "shader_parameter/wind", 0.0, 4.0)
		print("EVENT frame=%d click handled: wind 1.0, tween to 0.0 over 4.0 s" % frame)

func _process(_delta: float) -> void:
	frame += 1
	if frame == CLICK_FRAME:                       # the scripted input: one mouse click, logged
		var ev := InputEventMouseButton.new()
		ev.button_index = MOUSE_BUTTON_LEFT
		ev.pressed = true
		ev.position = get_viewport_rect().size * 0.5
		get_viewport().push_input(ev)
		print("EVENT frame=%d scripted click pushed" % frame)
