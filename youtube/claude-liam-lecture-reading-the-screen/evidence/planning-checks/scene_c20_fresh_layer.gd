extends "res://rts_scene.gd"
# C20 (beat B34): the pool (12-pool) and the player live on the game layer (0). The gray filter (05-gray) sits on its OWN canvas layer (1),
# with no BackBufferCopy anywhere. It takes its own copy, so it sees the pool and the player too: everything turns gray together.
var filter_rect: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	var pool := L.rect(pct(0.06, 0.52), pct(0.40, 0.40), Color.WHITE, "Pool")
	pool.material = L.mat_file("12-pool.gdshader")
	add_child(pool)
	add_child(L.make_player(pct(0.74, 0.62)))
	filter_rect = add_filter_layer("05-gray.gdshader")
	uni(filter_rect, "amount", 0.0)

func set_time(t: float) -> void:
	uni(filter_rect, "amount", ramp(u_of(t), 0.72, 0.90))
