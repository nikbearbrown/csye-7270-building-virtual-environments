extends CharacterBody2D
## The boy. One static image per state, swapped when the world turns over —
## no animation, per the assignment's static-state rule. All motion here is
## engine code: walking, facing, and a slow idle drift in the ghost state.

enum State { GHOST, REMEMBERED }

const SPEED := 260.0
const DRIFT_PIXELS := 6.0
const DRIFT_SECONDS := 2.2

var state: State = State.GHOST
var _facing := 1

@onready var _sprite: Sprite2D = $Sprite2D
@onready var _tex_ghost: Texture2D = preload("res://assets/art/char_ghost.png")
@onready var _tex_remembered: Texture2D = preload("res://assets/art/char_remembered.png")

var _sprite_home_y := 0.0


func _ready() -> void:
	_sprite_home_y = _sprite.position.y
	_apply_state()
	_start_drift()


func _physics_process(_delta: float) -> void:
	var direction := Input.get_axis("move_left", "move_right")
	velocity.x = direction * SPEED
	velocity.y = 0.0
	move_and_slide()

	if direction != 0.0:
		_facing = signi(int(direction))
		_sprite.flip_h = _facing < 0


## Called by the world when it turns over. The state is set here and the image
## swapped; no sound is played from this script, so audio can never drive state.
func set_inverted(is_inverted: bool) -> void:
	state = State.REMEMBERED if is_inverted else State.GHOST
	_apply_state()


func _apply_state() -> void:
	match state:
		State.GHOST:
			_sprite.texture = _tex_ghost
			_sprite.modulate = Color(1, 1, 1, 0.85)
		State.REMEMBERED:
			_sprite.texture = _tex_remembered
			_sprite.modulate = Color(1, 1, 1, 1)


## A slow vertical bob so the boy reads as hovering rather than standing.
func _start_drift() -> void:
	var tween := create_tween().set_loops()
	tween.tween_property(_sprite, "position:y", _sprite_home_y - DRIFT_PIXELS, DRIFT_SECONDS) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(_sprite, "position:y", _sprite_home_y, DRIFT_SECONDS) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
