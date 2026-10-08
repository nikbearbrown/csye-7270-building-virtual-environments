extends CharacterBody2D
## The boy. One static image per state, swapped when the world turns over —
## no animation, per the assignment's static-state rule. Everything that moves
## here is engine code: acceleration, gravity, a jump with coyote time and
## input buffering, a landing squash, a lean at speed, and a step bob while
## walking. Extra pose images, when they exist, are swapped in by state; they
## are never played as animation frames.

enum State { REMEMBERED, GHOST }

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
const STEP_PIXELS := 2.0      ## the eight frames already carry the rise and fall, so the code only adds a trace
const ROLL_RADIANS := 0.022   ## shoulder roll, synced to the same stride phase
const FLOAT_FPS := 2.2        ## a hanging body drifts slowly; faster reads as flapping
const STRIDE_PIXELS := 28.0   ## ground per frame; eight frames make a ~224 px cycle, about eleven frames a second at full speed
const LEAN_RADIANS := 0.10

signal landed(fall_speed: float)
## Fires on the two heel-strike frames of the cycle, so a footstep sounds when
## a foot actually lands rather than on a timer.
signal stepped
signal jumped

var state: State = State.REMEMBERED
var _facing := 1
## +1 pulls toward the bottom of the screen, -1 toward the top. Flipping the
## world inverts it, so the boy falls upward and lands on what was the ceiling.
var _gravity_dir := 1.0
## Held still during the opening, so the first thing the player sees is the
## house rather than their own input.
var controllable := true
var _coyote := 0.0
var _buffer := 0.0
var _was_on_floor := true
var _step_phase := 0.0
var _stride_distance := 0.0
var _walk_frame := 0
var _float_time := 0.0
var _landing_timer := 0.0
var _body_roll := 0.0
var _sprite_home_y := 0.0
var _drift_tween: Tween

@onready var _sprite: Sprite2D = $Sprite2D
@onready var _collision: CollisionShape2D = $CollisionShape2D
@onready var _tex_ghost: Texture2D = preload("res://assets/art/char_ghost.png")
@onready var _tex_remembered: Texture2D = preload("res://assets/art/char_remembered.png")

## The walk cycle belongs to the remembered boy alone. The ghost never walks —
## he drifts — which is both the truth of the character and the art we have.
@onready var _walk_frames: Array[Texture2D] = [
	preload("res://assets/art/char_walk_1.png"),   # contact, right heel down
	preload("res://assets/art/char_walk_2.png"),   # down, weight on the bent knee
	preload("res://assets/art/char_walk_3.png"),   # passing, legs together
	preload("res://assets/art/char_walk_4.png"),   # up, pushing off
	preload("res://assets/art/char_walk_5.png"),   # contact, left heel down
	preload("res://assets/art/char_walk_6.png"),
	preload("res://assets/art/char_walk_7.png"),
	preload("res://assets/art/char_walk_8.png"),
]

## The ghost does not walk. He drifts, so his cycle runs on a clock rather than
## on ground covered, and it keeps playing when he is standing still.
##
## These frames are drawn upside down, not mirrored: under reversed gravity his
## hair, sweater hem and the mist his legs dissolve into all stream toward the
## ceiling. A vertically flipped sprite would have all of that pointing the
## wrong way, which is what made the earlier version read as a boy standing on
## his head rather than something hanging in the air.
## Only the frames where his arms stay near his body. Three of the six have the
## arms flung wide, which upside down reads as hands thrown down rather than a
## body hanging, so they are left out and the cycle sways between the quiet
## ones instead.
@onready var _float_frames: Array[Texture2D] = [
	preload("res://assets/art/char_ghost_inv_1.png"),
	preload("res://assets/art/char_ghost_inv_6.png"),
	preload("res://assets/art/char_ghost_inv_5.png"),
	preload("res://assets/art/char_ghost_inv_6.png"),
]

## Jump poses: crouch, rising, falling, landing. Swapped by what the body is
## actually doing, not played as a timed animation.
@onready var _tex_crouch: Texture2D = preload("res://assets/art/char_jump_1.png")
@onready var _tex_rising: Texture2D = preload("res://assets/art/char_jump_2.png")
@onready var _tex_falling: Texture2D = preload("res://assets/art/char_jump_3.png")
@onready var _tex_landing: Texture2D = preload("res://assets/art/char_jump_4.png")

const LANDING_SECONDS := 0.18


func _ready() -> void:
	_sprite_home_y = _sprite.position.y
	_apply_state()
	_start_drift()


func _physics_process(delta: float) -> void:
	var direction := Input.get_axis("move_left", "move_right") if controllable else 0.0

	# Horizontal: accelerate toward the target, brake with friction when idle.
	if absf(direction) > 0.01:
		velocity.x = move_toward(velocity.x, direction * SPEED, ACCELERATION * delta)
		_facing = signi(int(signf(direction)))
		_sprite.flip_h = _facing < 0
	else:
		velocity.x = move_toward(velocity.x, 0.0, FRICTION * delta)

	# Vertical. Gravity and the jump both follow _gravity_dir, and up_direction
	# tells CharacterBody2D which surface counts as the floor.
	up_direction = Vector2(0, -_gravity_dir)
	if is_on_floor():
		_coyote = COYOTE_SECONDS
	else:
		_coyote = maxf(0.0, _coyote - delta)
		velocity.y += GRAVITY * _gravity_dir * delta
		velocity.y = clampf(velocity.y, -MAX_FALL, MAX_FALL)

	if controllable and Input.is_action_just_pressed("jump"):
		_buffer = BUFFER_SECONDS
	else:
		_buffer = maxf(0.0, _buffer - delta)

	if _buffer > 0.0 and _coyote > 0.0:
		velocity.y = JUMP_VELOCITY * _gravity_dir
		_buffer = 0.0
		_coyote = 0.0
		if state == State.REMEMBERED:
			_sprite.texture = _tex_crouch
		jumped.emit()

	# Releasing the key early cuts the hop short, so height is expressive.
	if Input.is_action_just_released("jump") and velocity.y * _gravity_dir < 0.0:
		velocity.y *= JUMP_CUT

	var fall_speed := velocity.y * _gravity_dir
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
	_sprite.rotation = lerpf(_sprite.rotation, target_lean + _body_roll, 14.0 * delta)

	var walking := is_on_floor() and absf(direction) > 0.01
	_update_walk_frame(delta, walking)

	if state == State.GHOST:
		_stop_drift()
		_sprite.position.y = _sprite_home_y
		_body_roll = 0.0
	elif walking:
		_stop_drift()
		# Weight. The cycle phase comes from the stride itself, so the body is
		# lowest on the two contact frames and highest on the two passing
		# frames — the same beat the legs are drawing — instead of bobbing on
		# an independent timer that slowly drifts out of step with the feet.
		var phase := (float(_walk_frame) + _stride_distance / STRIDE_PIXELS) / float(_walk_frames.size())
		var bob := -absf(sin(phase * TAU)) * STEP_PIXELS * speed_ratio
		_sprite.position.y = _sprite_home_y + bob * _gravity_dir
		# A small roll on the same phase, offset a quarter cycle, so the
		# shoulders lead the hips the way a real gait does.
		_body_roll = sin(phase * TAU - PI * 0.5) * ROLL_RADIANS * speed_ratio
	elif is_on_floor():
		_body_roll = 0.0
		if _drift_tween == null:
			_step_phase = 0.0
			_start_drift()


## Frames advance by ground covered, not by a clock, so the stride always
## matches the speed and the feet never slide. The cycle is only used in the
## remembered state; the ghost keeps his single drifting image.
func _update_walk_frame(delta: float, walking: bool) -> void:
	if state == State.GHOST:
		_update_float(delta)
		return

	# In the air, the body is doing something a walk frame cannot express.
	if not is_on_floor():
		_landing_timer = 0.0
		_sprite.texture = _tex_rising if velocity.y * _gravity_dir < 0.0 else _tex_falling
		return
	if _landing_timer > 0.0:
		_landing_timer = maxf(0.0, _landing_timer - delta)
		_sprite.texture = _tex_landing
		return
	if not walking:
		_stride_distance = 0.0
		_walk_frame = 0
		_apply_state()          # back to the idle image for this world
		return
	_stride_distance += absf(velocity.x) * delta
	while _stride_distance >= STRIDE_PIXELS:
		_stride_distance -= STRIDE_PIXELS
		_walk_frame = (_walk_frame + 1) % _walk_frames.size()
		# frames 0 and 4 are the contact poses: a heel meeting the floor
		if _walk_frame == 0 or _walk_frame == 4:
			stepped.emit()
	_sprite.texture = _walk_frames[_walk_frame]


## Always drifting, moving or not — a ghost has no still pose.
func _update_float(delta: float) -> void:
	_float_time += delta * FLOAT_FPS
	var frame := int(_float_time) % _float_frames.size()
	_sprite.texture = _float_frames[frame]
	# A drifting body has no heel strikes, so the stride beat is taken from
	# ground covered instead — the ghost still has a rhythm when he moves.
	if absf(velocity.x) > 10.0:
		_stride_distance += absf(velocity.x) * delta
		while _stride_distance >= STRIDE_PIXELS * 1.6:
			_stride_distance -= STRIDE_PIXELS * 1.6
			stepped.emit()
	else:
		_stride_distance = 0.0


func _land(fall_speed: float) -> void:
	landed.emit(fall_speed)
	_landing_timer = LANDING_SECONDS
	_stop_drift()
	var impact := clampf(fall_speed / 900.0, 0.0, 1.0)
	var squash := Vector2(1.0 + 0.22 * impact, 1.0 - 0.22 * impact)
	var tween := create_tween()
	_sprite.scale = squash
	tween.tween_property(_sprite, "scale", Vector2.ONE, 0.26).set_trans(Tween.TRANS_ELASTIC)
	await tween.finished
	if is_on_floor() and absf(velocity.x) < 1.0:
		_start_drift()


## Called by the world when it turns over. Gravity reverses, so the boy falls
## upward and lands on what was the ceiling — which, because the memory room is
## drawn rotated, is the floor of his own bedroom. The state image is swapped
## here too; no sound is played from this script, so audio can never drive state.
func set_inverted(is_inverted: bool) -> void:
	_gravity_dir = -1.0 if is_inverted else 1.0
	up_direction = Vector2(0, -_gravity_dir)
	velocity.y = 0.0
	# The sprite and the capsule are both centred on the node, so a flip only
	# turns the picture over; nothing moves. An earlier version shifted the
	# capsule instead, which dropped it inside the floor collider on the first
	# flip and squeezed the player out through the bottom of the room.
	# The ghost is NOT drawn upside down. Turning the sprite over made him read
	# as a boy standing on his head rather than something floating, so the
	# picture stays upright in both worlds; only gravity and the art change.
	_sprite.flip_v = false
	# Inverted is the truth: he stops looking like a living boy and becomes what
	# he actually is.
	state = State.GHOST if is_inverted else State.REMEMBERED
	_apply_state()


func _apply_state() -> void:
	match state:
		State.GHOST:
			_float_time = 0.0
			_sprite.texture = _float_frames[0]
			# Drained and see-through: the same boy, rendered as what he is.
			_sprite.modulate = Color(0.72, 0.80, 0.92, 0.82)
		State.REMEMBERED:
			# The idle is the cycle's own legs-together pose rather than a
			# separate standing drawing. The standing one is 340 px tall where
			# the walk frames are 303-317, so switching between them read as
			# the boy shrinking the moment he moved, even though their heads
			# measured the same size.
			_sprite.texture = _walk_frames[2]
			_sprite.modulate = Color(1, 1, 1, 1)


## A slow vertical bob while standing still, so the boy reads as hovering
## rather than planted.
func _start_drift() -> void:
	_stop_drift()
	_drift_tween = create_tween().set_loops()
	_drift_tween.tween_property(_sprite, "position:y", _sprite_home_y - DRIFT_PIXELS * _gravity_dir, DRIFT_SECONDS) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_drift_tween.tween_property(_sprite, "position:y", _sprite_home_y, DRIFT_SECONDS) \
		.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)


func _stop_drift() -> void:
	if _drift_tween:
		_drift_tween.kill()
		_drift_tween = null
