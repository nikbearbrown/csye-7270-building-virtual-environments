extends "res://rts_scene.gd"
# C04 (beat B09): one 16:9 window with 03-invert (1.0 - what is behind). It sits still for the first half of the beat, then slides diagonally.
# The flipped picture inside stays pinned to the screen; only the opening moves.
const SLIDE_FROM := 0.56
const SLIDE_TO := 0.96
var w: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	w = win(0.08, 0.10, 0.28, 0.28, "03-invert.gdshader", "InvertWindow")

func set_time(t: float) -> void:
	var k := ramp(u_of(t), SLIDE_FROM, SLIDE_TO)
	w.position = Vector2(lerpf(0.08, 0.62, k) * canvas_size.x, lerpf(0.10, 0.58, k) * canvas_size.y)
