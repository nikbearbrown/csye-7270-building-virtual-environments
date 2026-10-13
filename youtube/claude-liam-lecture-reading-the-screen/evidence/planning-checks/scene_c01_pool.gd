extends "res://rts_scene.gd"
# C01 (beats B01 and B28): the finished pool in the meadow, live. Nothing moves except the water (TIME).
# Tree order: World, Pool, Player. The pool reads the screen: the meadow behind it.

func build() -> void:
	world = L.build_world(self, canvas_size)
	var pool := win(0.06, 0.52, 0.40, 0.40, "12-pool.gdshader", "Pool")
	pool.name = "Pool"
	add_child(L.make_player(pct(0.74, 0.62)))

func set_time(_t: float) -> void:
	pass
