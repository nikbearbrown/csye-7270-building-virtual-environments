extends Node2D
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

var kind := "moth"
var hp := 1.0
var speed := 0.0
var radius := 6.0
var hit_half := Vector2(6, 6)
var damage := 1
var xp := 1
var flash := 0
var dead := false
var anim := 0
var frame := 24
var tex: Texture2D
var flip := false

func setup(k: String, at: Vector2) -> void:
	kind = k
	position = at
	var d: Dictionary = Tuning.ENEMIES[k]
	hp = float(d["hp"]); speed = d["speed"]; radius = d["radius"]; damage = d["damage"]; xp = d["xp"]; frame = d["frame"]
	hit_half = Vector2(d["hit_half"][0], d["hit_half"][1])
	tex = Art.texture(Art.MOTH if k == "moth" else Art.WRAITH)

## True when a point (grown by pad) is inside the visible sprite's box.
func touches(p: Vector2, pad: float) -> bool:
	var q := (p - position).abs()
	return q.x <= hit_half.x + pad and q.y <= hit_half.y + pad

## True when any part of the segment a-b (grown by pad) touches the visible sprite's box.
func touches_segment(a: Vector2, b: Vector2, pad: float) -> bool:
	var n := maxi(2, ceili(a.distance_to(b) / 2.0) + 1)
	for i in n:
		if touches(a.lerp(b, float(i) / (n - 1)), pad):
			return true
	return false

func step(target: Vector2) -> void:
	var to := target - position
	if to.length() > 0.5:
		position += to.normalized() * speed / Tuning.TICK_HZ
	flip = to.x < 0
	anim += 1
	if flash > 0:
		flash -= 1
	modulate = Color(2.5, 2.5, 2.5) if flash > 0 else Color.WHITE
	queue_redraw()

func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(-1 if flip else 1, 1))
	if tex:
		var f := (anim / 10) % 2
		draw_texture_rect_region(tex, Rect2(-frame / 2.0, -frame / 2.0, frame, frame), Rect2(f * frame, 0, frame, frame))
	else:
		draw_circle(Vector2.ZERO, radius, Color("#C7D0E0") if kind == "moth" else Color("#3B4A6B"))
		draw_arc(Vector2.ZERO, radius, 0, TAU, 16, Color("#14121C"), 1.0)
