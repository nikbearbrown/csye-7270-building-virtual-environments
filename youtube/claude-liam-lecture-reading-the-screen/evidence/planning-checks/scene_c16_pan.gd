extends "res://rts_scene.gd"
# C16 (beat B29): the payoff. The meadow, the finished pool (12-pool) and the player all sit under one WorldRoot that scrolls down 110 px (u 0.54 to 0.74) and back (u 0.80 to 0.98).
# The pool scrolls with the world; its ripples use its own address, so they travel with it.
var pan_root: Node2D

func build() -> void:
	pan_root = Node2D.new()
	pan_root.name = "WorldRoot"
	add_child(pan_root)
	world = L.build_world(pan_root, canvas_size, 2)
	var pool := L.rect(pct(0.06, 0.52), pct(0.40, 0.40), Color.WHITE, "Pool")
	pool.material = L.mat_file("12-pool.gdshader")
	pan_root.add_child(pool)
	pan_root.add_child(L.make_player(pct(0.74, 0.62)))

func set_time(t: float) -> void:
	var u := u_of(t)
	pan_root.position.y = 110.0 * (ramp(u, 0.54, 0.74) - ramp(u, 0.80, 0.98))
