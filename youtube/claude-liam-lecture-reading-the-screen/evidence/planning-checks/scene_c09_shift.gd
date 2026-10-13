extends "res://rts_scene.gd"
# C09 (beat B21): a window (08-shift) over the meadow. The `shift` uniform sweeps from 0 to 0.10 between u = 0.56 and 0.90: every pixel
# in the window shows what lies a little further to the right (0.10 of 1280 px = 128 px), so the picture inside slides against the picture outside.
const SHIFT_FROM := 0.56
const SHIFT_TO := 0.90
var w: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	w = win(0.20, 0.12, 0.52, 0.42, "08-shift.gdshader", "ShiftWindow")

func set_time(t: float) -> void:
	uni(w, "shift", 0.10 * ramp(u_of(t), SHIFT_FROM, SHIFT_TO))
