extends "res://rts_scene.gd"
# C22 (beat B36): a window flush with the right edge of the screen, reading with 15-edge-clamp (the docs' declaration: hint_screen_texture,
# repeat_disable, filter_nearest). `shift` grows from 0 to 0.30 between u = 0.28 and 0.62: the window reads past the edge of the screen and gets
# the edge pixel, repeated, instead of the far side.
var w: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	w = win(0.60, 0.20, 0.40, 0.44, "15-edge-clamp.gdshader", "EdgeWindow")

func set_time(t: float) -> void:
	uni(w, "shift", 0.30 * ramp(u_of(t), 0.28, 0.62))
