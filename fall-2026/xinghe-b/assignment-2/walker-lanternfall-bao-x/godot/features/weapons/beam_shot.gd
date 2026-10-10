extends Node2D
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

var dir := Vector2.RIGHT
var pierce := 1
var life: int = Tuning.BEAM_LIFE_TICKS
var hit_ids := {}
var dead := false
var tex: Texture2D

func setup(at: Vector2, d: Vector2, p: int) -> void:
	position = at
	dir = d
	pierce = p
	rotation = d.angle()
	tex = Art.texture(Art.BEAM)

func step() -> void:
	position += dir * Tuning.BEAM_SPEED / Tuning.TICK_HZ
	life -= 1

func _draw() -> void:
	if tex:
		draw_texture(tex, -tex.get_size() / 2)
	else:
		draw_rect(Rect2(-8, -2, 16, 4), Color("#FFF1C9"))
