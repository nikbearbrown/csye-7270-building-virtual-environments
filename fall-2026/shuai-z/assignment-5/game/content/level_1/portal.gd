class_name Portal
extends Area2D
## The teleport circle (ENV-PORTAL) at the end of the level. Rudy stepping onto
## it ends the level; the level guards against a second time. Its art is the
## circle of pale gold runes lying on the ground, drawn at half scale from
## props.json's origin with its middle 6 px above the ground; it gets no
## outline, which would follow the glow. When Rudy arrives, a column of light,
## drawn by code, rises from it once: deep gold, brighter in the middle, soft at
## the sides and fading toward the top, so it shows against the pale sky. The
## origin is at the centre of the circle, on the ground.

signal reached

const LIGHT := Color("#F0A830") ## deep gold
const CORE := Color("#FFD76E") ## the bright middle
const LIGHT_HEIGHT := 640.0
const BASE_Y := -6.0 ## the circle's middle

var _light := 0.0 ## 0 before Rudy arrives; rises to 1


func _ready() -> void:
	body_entered.connect(_on_body_entered)


func light_up(duration: float) -> void:
	create_tween().tween_method(_set_light, 0.0, 1.0, duration)


func _on_body_entered(body: Node2D) -> void:
	if body is Rudy:
		reached.emit()


func _set_light(amount: float) -> void:
	_light = amount
	queue_redraw()


## The column of light, behind the circle's art: three nested beams, so it is
## soft at the sides and strongest in the middle.
func _draw() -> void:
	if _light <= 0.0:
		return
	var height := LIGHT_HEIGHT * _light
	_beam(150.0, height, Color(LIGHT, 0.3 * _light))
	_beam(100.0, height, Color(LIGHT, 0.35 * _light))
	_beam(45.0, height, Color(CORE, 0.6 * _light))


## A beam `half_width` either side of the middle, fading from `color` at the
## circle to nothing at its top.
func _beam(half_width: float, height: float, color: Color) -> void:
	var top := BASE_Y - height
	var clear := Color(color, 0.0)
	draw_polygon(
		PackedVector2Array([Vector2(-half_width, BASE_Y), Vector2(half_width, BASE_Y), Vector2(half_width, top), Vector2(-half_width, top)]),
		PackedColorArray([color, color, clear, clear]))
