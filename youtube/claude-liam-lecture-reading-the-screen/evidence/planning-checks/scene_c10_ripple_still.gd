extends "res://rts_scene.gd"
# C10 (beat B22): a window (09-ripple-still): each row is pushed sideways by amount * sin(60 * SCREEN_UV.y). No TIME: the ripples hold still.
# `amount` grows from 0 to 0.012 between u = 0.44 and 0.92, so straight lines start to ripple as the voice says it.
const GROW_FROM := 0.44
const GROW_TO := 0.92
var w: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	w = win(0.20, 0.08, 0.56, 0.52, "09-ripple-still.gdshader", "RippleWindow")

func set_time(t: float) -> void:
	uni(w, "amount", 0.012 * ramp(u_of(t), GROW_FROM, GROW_TO))
