extends "res://rts_scene.gd"
# C11 (beat B23): the same window with 10-ripple: TIME is inside the sine, so the ripples travel. amount stays at 0.01.
var w: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	w = win(0.20, 0.08, 0.56, 0.52, "10-ripple.gdshader", "RippleWindow")
	uni(w, "amount", 0.01)

func set_time(_t: float) -> void:
	pass
