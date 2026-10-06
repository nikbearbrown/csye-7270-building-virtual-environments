class_name Player
extends CharacterBody2D
## The mage. One static image per state, swapped when the state changes (no animation).
## Facing follows movement. Art and collision line up per CHARACTER-SHEET: the sprite's anchor
## (canvas 31,67) is the body origin at the feet, and the 14x44 rectangle spans canvas x 24-38, y 23-67.

signal failed(reason: String)
## SFX-CAST listens to this. Emitted once per cast, after the cooldown check and the spawn.
signal cast_fired(origin: Vector2, direction: Vector2)
## SFX-HURT listens to this. Emitted only when a hit lands (not while invulnerable).
signal hurt(hp: int)

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

const FIREBALL := preload("res://features/fireball/fireball.tscn")
## The crystal in the cast image, relative to the feet (canvas 42,7 minus anchor 31,67); mirrored with facing.
const STAFF_TIP := Vector2(11, -60)

var state: State = State.IDLE
var facing := 1                 # 1 = right (as drawn), -1 = left (flip_h)
var is_failing := false
var hp := Tuning.MAX_HP
var invulnerable := 0.0         # seconds left

## Headless tests drive the player through `scripted` instead of the keyboard and mouse:
## {"move": -1..1, "jump_pressed": bool (one frame), "jump_held": bool,
##  "cast_pressed": bool (one frame), "aim": global position}
var use_scripted := false
var scripted := {"move": 0.0, "jump_pressed": false, "jump_held": false, "cast_pressed": false, "aim": Vector2.ZERO}

var _coyote := 0.0
var _jump_buffer := 0.0
var _cast_cooldown := 0.0
var _cast_hold := 0.0
var _hurt_hold := 0.0

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
	if _jump_buffer > 0.0 and _coyote > 0.0 and _hurt_hold == 0.0:
		velocity.y = Tuning.JUMP_VELOCITY
		_jump_buffer = 0.0
		_coyote = 0.0
	if not jump_held and velocity.y < Tuning.JUMP_CUT_VELOCITY and _hurt_hold == 0.0:
		velocity.y = Tuning.JUMP_CUT_VELOCITY

	_cast_cooldown = maxf(_cast_cooldown - delta, 0.0)
	_cast_hold = maxf(_cast_hold - delta, 0.0)
	_hurt_hold = maxf(_hurt_hold - delta, 0.0)
	invulnerable = maxf(invulnerable - delta, 0.0)
	sprite.visible = invulnerable == 0.0 or int(invulnerable / Tuning.BLINK_PERIOD) % 2 == 0

	var cast_pressed := _read_cast_pressed()
	if _hurt_hold > 0.0:
		# Knocked back: no control until the hold ends.
		velocity.x = move_toward(velocity.x, 0.0, Tuning.AIR_ACCEL * 0.5 * delta)
	else:
		var accel := Tuning.GROUND_ACCEL if is_on_floor() else Tuning.AIR_ACCEL
		velocity.x = move_toward(velocity.x, move * Tuning.RUN_SPEED, accel * delta)
		# Facing follows movement, except while the cast image is up (she faces where she cast).
		if move != 0.0 and _cast_hold == 0.0:
			facing = 1 if move > 0.0 else -1
		if cast_pressed and _cast_cooldown == 0.0:
			cast(_read_aim())

	move_and_slide()
	_update_state()


## One fireball from the crystal toward `aim`. Turns to face the aim point first.
func cast(aim: Vector2) -> void:
	facing = 1 if aim.x >= global_position.x else -1
	var origin := global_position + Vector2(STAFF_TIP.x * facing, STAFF_TIP.y)
	var dir := aim - origin
	dir = dir.normalized() if dir.length() > 1.0 else Vector2(facing, 0)
	var fireball: Fireball = FIREBALL.instantiate()
	fireball.direction = dir
	fireball.position = origin
	get_parent().add_child(fireball)
	_cast_cooldown = Tuning.CAST_COOLDOWN
	_cast_hold = Tuning.CAST_HOLD
	cast_fired.emit(origin, dir)


func _update_state() -> void:
	if state in [State.FAIL, State.WIN]:
		return
	var next: State
	if _hurt_hold > 0.0:
		next = State.HURT
	elif _cast_hold > 0.0:
		next = State.CAST
	elif is_on_floor():
		next = State.IDLE if absf(velocity.x) < 5.0 else State.RUN
	else:
		next = State.RISE if velocity.y < 0.0 else State.FALL
	_set_state(next)


func _set_state(next: State) -> void:
	state = next
	sprite.texture = TEXTURES[next]
	sprite.flip_h = facing < 0


## A wolf lunge. Ignored while invulnerable or failing; the invulnerability starts in the same call
## (CHANGE-BRIEF guard for SFX-HURT). HP 0 fails with the kneeling image.
func take_damage(amount: int, from_x: float) -> void:
	if is_failing or invulnerable > 0.0:
		return
	hp = maxi(hp - amount, 0)
	invulnerable = Tuning.INVULNERABLE_TIME
	_hurt_hold = Tuning.HURT_HOLD
	_cast_hold = 0.0
	var away := 1.0 if global_position.x >= from_x else -1.0
	velocity = Vector2(Tuning.KNOCKBACK.x * away, Tuning.KNOCKBACK.y)
	facing = -int(away)   # she faces what hit her
	hurt.emit(hp)
	if hp == 0:
		fail("Out of HP")
	else:
		_set_state(State.HURT)


## Pit kill zone (by_pit = true, shows the fall image) or HP 0 (kneeling fail image).
## The `is_failing` flag makes a second call in the same or a later frame a no-op.
func fail(reason: String, by_pit := false) -> void:
	if is_failing:
		return
	is_failing = true
	velocity = Vector2.ZERO
	sprite.visible = true
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


## Just-pressed only: holding the button does not repeat (CHANGE-BRIEF guard for SFX-CAST).
func _read_cast_pressed() -> bool:
	if use_scripted:
		var pressed: bool = scripted.cast_pressed
		scripted.cast_pressed = false
		return pressed
	return Input.is_action_just_pressed("cast")


func _read_aim() -> Vector2:
	if use_scripted:
		return scripted.aim
	return get_global_mouse_position()
