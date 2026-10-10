extends Node2D
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

var value := 1
var pulled := false
var tex: Texture2D

func setup(at: Vector2, v: int) -> void:
	position = at
	value = v
	tex = Art.texture(Art.GEM)

## True when collected this tick. Once inside the magnet it keeps flying to the courier.
func step(target: Vector2, magnet: float) -> bool:
	var d := position.distance_to(target)
	if d <= Tuning.COLLECT_RADIUS:
		return true
	if pulled or d <= magnet:
		pulled = true
		position = position.move_toward(target, Tuning.GEM_PULL_SPEED / Tuning.TICK_HZ)
	return false

func _draw() -> void:
	if tex:
		draw_texture(tex, -tex.get_size() / 2)
	else:
		draw_colored_polygon(PackedVector2Array([Vector2(0, -5), Vector2(4, 0), Vector2(0, 5), Vector2(-4, 0)]), Color("#F2B84B"))
