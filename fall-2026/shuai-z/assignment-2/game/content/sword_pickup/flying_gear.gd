class_name FlyingGear
extends Sprite2D
## The sword and shield flying off Rudy when a hit takes them (STORYBOARD.md
## panel 4): the pickup's art (PROP-SWORDSHIELD), thrown up and away from the
## hit, spinning about its middle, fading out. It is only a picture and touches
## nothing.

const ART := preload("res://content/level_1/art/PROP-SWORDSHIELD.png")
const ORIGIN := Vector2(92, 92) ## the art's middle, in texture px (props.json)
const DENSITY := 2.0 ## texture px per game px
const LIFETIME := 0.6 ## s until it has faded out
const GRAVITY := 1800.0 ## px/s²

var velocity := Vector2.ZERO

var _age := 0.0


func _init() -> void:
	texture = ART
	centered = false
	offset = -ORIGIN
	scale = Vector2.ONE / DENSITY
	texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS


func _process(delta: float) -> void:
	_age += delta
	velocity.y += GRAVITY * delta
	position += velocity * delta
	rotation += 9.0 * delta * signf(velocity.x)
	modulate.a = clampf(1.0 - _age / LIFETIME, 0.0, 1.0)
	if _age >= LIFETIME:
		queue_free()
