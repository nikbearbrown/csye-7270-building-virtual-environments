class_name Player
extends CharacterBody2D
## The mage. One static image per state, swapped when the state changes (no animation).
## Facing follows movement. Art and collision line up per CHARACTER-SHEET: the sprite's anchor
## (canvas 31,67) is the body origin at the feet, and the 14x44 rectangle spans canvas x 24-38, y 23-67.

signal failed(reason: String)

enum State { IDLE, RUN, RISE, FALL, CAST, HURT, FAIL, WIN }

const TEXTURES := {
	State.IDLE: preload("res://assets/sprites/mage/mage_idle.png"),
	State.RUN: preload("res://assets/sprites/mage/mage_run_contact.png"),
	State.RISE: preload("res://assets/sprites/mage/mage_rise.png"),
	State.FALL: preload("res://assets/sprites/mage/mage_fall.png"),
	State.CAST: preload("res://assets/sprites/mage/mage_cast.png"),
	State.HURT: preload("res://assets/sprites/mage/mage_hurt.png"),
	State.FAIL: preload("res://assets/sprites/mage/mage_fail.png"),
	State.WIN: preload("res://assets/sprites/mage/mage_win.png"),
}

var state: State = State.IDLE
var facing := 1                 # 1 = right (as drawn), -1 = left (flip_h)
var is_failing := false

## Headless tests drive the player through `scripted` instead of the keyboard:
## {"move": -1..1, "jump_pressed": bool (one frame), "jump_held": bool}
var use_scripted := false
var scripted := {"move": 0.0, "jump_pressed": false, "jump_held": false}

var _coyote := 0.0
var _jump_buffer := 0.0

@onready var sprite: Sprite2D = $Sprite2D


func _ready() -> void:
	_set_state(State.IDLE)


func _physics_process(delta: float) -> void:
	var move := _read_move()
	var jump_pressed := _read_jump_pressed()
	var jump_held := _read_jump_held()

	if is_on_floor():
		_coyote = Tuning.COYOTE_TIME
	else:
		_coyote = maxf(_coyote - delta, 0.0)
		velocity.y = minf(velocity.y + Tuning.GRAVITY * delta, Tuning.MAX_FALL_SPEED)

	_jump_buffer = Tuning.JUMP_BUFFER if jump_pressed else maxf(_jump_buffer - delta, 0.0)
	if _jump_buffer > 0.0 and _coyote > 0.0:
		velocity.y = Tuning.JUMP_VELOCITY
		_jump_buffer = 0.0
		_coyote = 0.0
	if not jump_held and velocity.y < Tuning.JUMP_CUT_VELOCITY:
		velocity.y = Tuning.JUMP_CUT_VELOCITY

	var accel := Tuning.GROUND_ACCEL if is_on_floor() else Tuning.AIR_ACCEL
	velocity.x = move_toward(velocity.x, move * Tuning.RUN_SPEED, accel * delta)
	if move != 0.0:
		facing = 1 if move > 0.0 else -1

	move_and_slide()
	_update_state()


func _update_state() -> void:
	if state in [State.FAIL, State.WIN]:
		return
	var next: State
	if is_on_floor():
		next = State.IDLE if absf(velocity.x) < 5.0 else State.RUN
	else:
		next = State.RISE if velocity.y < 0.0 else State.FALL
	_set_state(next)


func _set_state(next: State) -> void:
	state = next
	sprite.texture = TEXTURES[next]
	sprite.flip_h = facing < 0


## Pit kill zone (by_pit = true, shows the fall image) or HP 0 (kneeling fail image).
## The `is_failing` flag makes a second call in the same or a later frame a no-op.
func fail(reason: String, by_pit := false) -> void:
	if is_failing:
		return
	is_failing = true
	velocity = Vector2.ZERO
	set_physics_process(false)
	state = State.FAIL
	sprite.texture = TEXTURES[State.FALL if by_pit else State.FAIL]
	sprite.flip_h = facing < 0
	failed.emit(reason)


## For tests/capture_scene.gd only: place the player and show one state's image.
func capture_pose(pos: Vector2, state_name: String, face: int) -> void:
	set_physics_process(false)
	global_position = pos
	facing = face
	_set_state(State[state_name.to_upper()])


func _read_move() -> float:
	if use_scripted:
		return float(scripted.move)
	return Input.get_axis("move_left", "move_right")


func _read_jump_pressed() -> bool:
	if use_scripted:
		var pressed: bool = scripted.jump_pressed
		scripted.jump_pressed = false
		return pressed
	return Input.is_action_just_pressed("jump")


func _read_jump_held() -> bool:
	if use_scripted:
		return bool(scripted.jump_held)
	return Input.is_action_pressed("jump")
