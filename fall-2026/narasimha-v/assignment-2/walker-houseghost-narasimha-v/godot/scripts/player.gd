extends CharacterBody2D
## The boy. One static image per state, swapped when the world turns over —
## no animation, per the assignment's static-state rule. Everything that moves
## here is engine code: acceleration, gravity, a jump with coyote time and
## input buffering, a landing squash, a lean at speed, and a step bob while
## walking. Extra pose images, when they exist, are swapped in by state; they
## are never played as animation frames.

enum State { GHOST, REMEMBERED }

const SPEED := 300.0
const ACCELERATION := 2200.0
const FRICTION := 2600.0
const GRAVITY := 2400.0
const JUMP_VELOCITY := -1100.0   ## ~250 px of rise, enough to reach the boxes
const JUMP_CUT := 0.45          ## releasing early shortens the hop
const COYOTE_SECONDS := 0.12    ## still jumpable just after walking off an edge
const BUFFER_SECONDS := 0.12    ## a jump pressed just before landing still fires
const MAX_FALL := 2000.0

const DRIFT_PIXELS := 6.0
const DRIFT_SECONDS := 2.2
const STEP_PIXELS := 4.0
const LEAN_RADIANS := 0.10

signal landed(fall_speed: float)
signal jumped

var state: State = State.GHOST
var _facing := 1
var _coyote := 0.0
var _buffer := 0.0
var _was_on_floor := true
var _step_phase := 0.0
var _sprite_home_y := 0.0
var _drift_tween: Tween

@onready var _sprite: Sprite2D = $Sprite2D
@onready var _tex_ghost: Texture2D = preload("res://assets/art/char_ghost.png")
@onready var _tex_remembered: Texture2D = preload("res://assets/art/char_remembered.png")


func _ready() -> void:
	_sprite_home_y = _sprite.position.y
	_apply_state()
	_start_drift()


func _physics_process(delta: float) -> void:
	var direction := Input.get_axis("move_left", "move_right")

	# Horizontal: accelerate toward the target, brake with friction when idle.
	if absf(direction) > 0.01:
		velocity.x = move_toward(velocity.x, direction * SPEED, ACCELERATION * delta)
		_facing = signi(int(signf(direction)))
		_sprite.flip_h = _facing < 0
	else:
		velocity.x = move_toward(velocity.x, 0.0, FRICTION * delta)

	# Vertical.
	if is_on_floor():
		_coyote = COYOTE_SECONDS
	else:
		_coyote = maxf(0.0, _coyote - delta)
		velocity.y = minf(velocity.y + GRAVITY * delta, MAX_FALL)

	if Input.is_action_just_pressed("jump"):
		_buffer = BUFFER_SECONDS
	else:
		_buffer = maxf(0.0, _buffer - delta)

	if _buffer > 0.0 and _coyote > 0.0:
		velocity.y = JUMP_VELOCITY
		_buffer = 0.0
		_coyote = 0.0
		jumped.emit()

	# Releasing the key early cuts the hop short, so height is expressive.
	if Input.is_action_just_released("jump") and velocity.y < 0.0:
		velocity.y *= JUMP_CUT

	var fall_speed := velocity.y
	move_and_slide()

	if is_on_floor() and not _was_on_floor:
		_land(fall_speed)
	_was_on_floor = is_on_floor()

	_update_body(delta, direction)


## A boy who is being carried by his own weight: he leans into a run, bobs on
## each step, and squashes when he hits the floor. None of this is animation —
## it is the one static image being moved by code.
func _update_body(delta: float, direction: float) -> void:
	var speed_ratio := clampf(absf(velocity.x) / SPEED, 0.0, 1.0)

	var target_lean := -LEAN_RADIANS * speed_ratio * _facing
	if not is_on_floor():
		target_lean = -LEAN_RADIANS * 1.4 * signf(velocity.x) * speed_ratio
	_sprite.rotation = lerpf(_sprite.rotation, target_lean, 10.0 * delta)

	if is_on_floor() and absf(direction) > 0.01:
		_stop_drift()
		_step_phase += delta * 9.0 * speed_ratio
		_sprite.position.y = _sprite_home_y - absf(sin(_step_phase)) * STEP_PIXELS
	elif is_on_floor() and _drift_tween == null:
		_step_phase = 0.0
		_start_drift()


func _land(fall_speed: float) -> void:
	landed.emit(fall_speed)
	_stop_drift()
	var impact := clampf(fall_speed / 900.0, 0.0, 1.0)
	var squash := Vector2(1.0 + 0.22 * impact, 1.0 - 0.22 * impact)
	var tween := create_tween()
	_sprite.scale = squash
	tween.tween_property(_sprite, "scale", Vector2.ONE, 0.26).set_trans(Tween.TRANS_ELASTIC)
	await tween.finished
	if is_on_floor() and absf(velocity.x) < 1.0:
		_start_drift()


## Called by the world when it turns over. The state is set here and the image
## swapped; no sound is played from this script, so audio can never drive state.
func set_inverted(is_inverted: bool) -> void:
	state = State.REMEMBERED if is_inverted else State.GHOST
	_apply_state()


func _apply_state() -> void:
	match state:
		State.GHOST:
			_sprite.texture = _tex_ghost
			_sprite.modulate = Color(1, 1, 1, 0.9)
		State.REMEMBERED:
			_sprite.texture = _tex_remembered
			_sprite.modulate = Color(1, 1, 1, 1)


## A slow vertical bob while standing still, so the boy reads as hovering
## rather than planted.
func _start_drift() -> void:
	_stop_drift()
	_drift_tween = create_tween().set_loops()
	_drift_tween.tween_property(_sprite, "position:y", _sprite_home_y - DRIFT_PIXELS, DRIFT_SECONDS) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_drift_tween.tween_property(_sprite, "position:y", _sprite_home_y, DRIFT_SECONDS) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)


func _stop_drift() -> void:
	if _drift_tween:
		_drift_tween.kill()
		_drift_tween = null
