extends "res://rts_scene.gd"
# C12 (beat B24): the travelling ripple window while `amount` is swept: 0.002 -> 0.01 by u = 0.30 (reads as water), held to u = 0.60,
# then 0.01 -> 0.06 by u = 0.95 (the picture tears). Readouts in the lane: "0.01" at u = 0.45, "0.06" at u = 0.93.
var w: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	w = win(0.20, 0.08, 0.56, 0.52, "10-ripple.gdshader", "RippleWindow")

func amount_at(u: float) -> float:
	return 0.002 + 0.008 * ramp(u, 0.0, 0.30) + 0.050 * ramp(u, 0.60, 0.95)

func set_time(t: float) -> void:
	uni(w, "amount", amount_at(u_of(t)))
