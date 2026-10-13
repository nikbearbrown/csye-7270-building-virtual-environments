extends "res://rts_scene.gd"
# C23 (beat B37): everything at once. Game layer 0: meadow, the pool (12-pool), the player walking a wide flat ellipse. Layer 1: the spotlight filter
# (07-spotlight; its own layer, so it sees the pool). Layer 2: the health bar, untouched. The player passes the pool: the pool turns to colour as the light arrives.
const CENTER := Vector2(0.50, 0.62)
const LAP := Vector2(0.34, 0.10)
var player: Sprite2D
var filter_rect: ColorRect

func build() -> void:
	world = L.build_world(self, canvas_size)
	var pool := L.rect(pct(0.06, 0.52), pct(0.40, 0.40), Color.WHITE, "Pool")
	pool.material = L.mat_file("12-pool.gdshader")
	add_child(pool)
	player = L.make_player(pct(CENTER.x, CENTER.y))
	player.name = "Player"
	add_child(player)
	filter_rect = add_filter_layer("07-spotlight.gdshader")
	uni(filter_rect, "radius", 0.25)
	var hud_layer := CanvasLayer.new()
	hud_layer.layer = 2
	add_child(hud_layer)
	hud_layer.add_child(L.make_hud(canvas_size))

func set_time(t: float) -> void:
	var a := TAU * u_of(t) + PI
	player.position = pct(CENTER.x + LAP.x * cos(a), CENTER.y + LAP.y * sin(a))

func _process(_delta: float) -> void:
	uni(filter_rect, "player", player.get_global_transform_with_canvas().origin / get_viewport_rect().size)
