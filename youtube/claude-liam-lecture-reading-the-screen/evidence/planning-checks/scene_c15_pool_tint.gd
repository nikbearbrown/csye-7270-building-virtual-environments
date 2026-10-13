extends "res://rts_scene.gd"
# C15 (beat B27): the pool (11-water): bend + tint, a plain rectangle (no wavy edge yet), live. At the end the water_color uniform is changed
# from code, the way an artist would with the colour picker: blue -> violet between u = 0.78 and 0.94.
var pool: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	pool = win(0.06, 0.52, 0.40, 0.40, "11-water.gdshader", "Pool", false)
	add_child(L.make_player(pct(0.74, 0.62)))

func set_time(t: float) -> void:
	var k := ramp(u_of(t), 0.78, 0.94)
	uni(pool, "water", Color(0.2, 0.5, 0.8).lerp(Color(0.6, 0.3, 0.8), k))
