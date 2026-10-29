class_name Rudy
extends CharacterBody2D
## Rudy's controller. It moves him and picks the pose that shows his state,
## named by the pose's asset ID in CHARACTER-SHEET.md; his Look shows that ID's
## generated frame. The origin is at his soles.
##
## In the air he shows the rising pose, and the falling pose only if he was
## moving sideways when the fall began. The falling pose leaps forward, so a
## jump straight up keeps the rising pose all the way down; the pose changes
## at most once in the air, at the top.
##
## On the ground, pressing the other direction turns him in place at once, with
## no slide; he moves that way only if the key is still held after
## turn_hold_time, so a tap turns him without moving him or the camera.
##
## Gear: the sword-and-shield pickup gives him the sword form, with its own
## poses (CHAR-SWORD-*). A fresh press of slash swings the sword once; its
## hitbox in front of him is live for part of the swing, and one cut defeats a
## goblin. No new swing starts until the last one ends.
##
## Damage (CHANGE-BRIEF.md): a hit knocks his gear away if he carries it, and
## otherwise costs one of his hearts. Either way it turns him toward the hit,
## knocks him back and makes him invulnerable for a moment, flashing; hits
## during that window are ignored. A fall below a cliff costs a heart too. At
## zero hearts he is defeated, and the level starts over from the opening, with
## his hearts full. He can only be hit by the collision capsule, so a hit that
## grazes his hair, his sword or his shield is a miss.
##
## The level also takes control away when he falls out of the level, while he
## gets back up after a respawn (always without gear), and while he celebrates
## on the teleport circle.
##
## The feel numbers are tuned by playtesting.

signal respawned ## he has got back up after a respawn, and control returns
signal hit ## a hit has just cost him his gear or a heart
signal hearts_changed(hearts: int)
signal defeated ## a hit took his last heart

enum Mode {
	WAITING, ## on the title, before play starts (CHAR-IDLE); no control
	PLAY, ## under the player's control
	HURT, ## knocked back by a hit (CHAR-HURT); no control for hurt_time
	DEFEATED, ## his last heart is gone (CHAR-DEFEAT); no control
	FALLEN, ## fell below a cliff; no control
	RESPAWNING, ## getting back up at a checkpoint (CHAR-RESPAWN); no control
	CELEBRATING, ## on the teleport circle (CHAR-CELEBRATE); no control
}

enum Gear { NONE, SWORD }

const ENEMY_LAYER := 4 ## the Enemy physics layer, for the sword's hitbox

@export_group("Feel")
@export var run_speed := 560.0 ## px/s
@export var run_accel := 5600.0 ## px/s²: full speed, or a stop, in 0.1 s
@export var turn_hold_time := 0.12 ## s the key is held after a turn on the ground before he moves
@export var gravity := 4000.0 ## px/s² on the way up
@export var fall_gravity := 6400.0 ## px/s² on the way down, so the fall is quicker than the rise
@export var jump_velocity := 1500.0 ## px/s; at 60 physics ticks/s the apex is 294 px, the rise takes 0.38 s and the fall 0.32 s
@export var run_frame_time := 0.125 ## seconds per run frame (RUN-A, then RUN-B)
@export var respawn_time := 0.7 ## s in CHAR-RESPAWN before control returns
@export var stomp_bounce := 600.0 ## px/s upward after he lands on an enemy

@export_group("Sword")
@export var slash_time := 0.3 ## s a swing lasts (CHAR-SWORD-SLASH); no new swing until it ends
@export var slash_live_from := 0.03 ## s into the swing when the hitbox goes live
@export var slash_live_to := 0.18 ## s into the swing when it goes dead again
@export var slash_reach := 50.0 ## px from his centre to the centre of the hitbox, in front of him

@export_group("Damage")
@export var max_hearts := 3
@export var knockback := Vector2(350, 400) ## px/s: away from the hit, and up
@export var hurt_time := 0.35 ## s without control after a hit
@export var invulnerable_time := 1.2 ## s after a hit or a respawn in which hits are ignored
@export var flash_period := 0.12 ## s; he is see-through for half of each period while invulnerable

var facing := 1 ## 1 faces right, -1 faces left
var pose: StringName = &"CHAR-IDLE"
var mode := Mode.PLAY ## the level sets WAITING while the title shows
var hearts := 3
var gear := Gear.NONE

var _run_clock := 0.0
var _turn_time_left := 0.0
var _respawn_time_left := 0.0
var _hurt_time_left := 0.0
var _invulnerable_left := 0.0
var _bounce_pending := false
var _was_falling := false
var _falls_sideways := false ## whether he was moving sideways when this fall began
var _slash_clock := -1.0 ## s into the current swing; below 0 when he is not swinging
var _slash_query := PhysicsShapeQueryParameters2D.new()

@onready var _look: RudyLook = $Look
@onready var _sword_box: CollisionShape2D = $SwordHitbox/Shape


func _ready() -> void:
	hearts = max_hearts
	_slash_query.shape = _sword_box.shape
	_slash_query.collision_mask = ENEMY_LAYER
	_slash_query.collide_with_areas = true
	_slash_query.collide_with_bodies = false


## True while enemies and hazards can touch him: in play, or knocked back.
func can_be_touched() -> bool:
	return mode == Mode.PLAY or mode == Mode.HURT


func is_invulnerable() -> bool:
	return _invulnerable_left > 0.0


func is_slashing() -> bool:
	return _slash_clock >= 0.0


## The pickup gives him the sword and shield.
func equip_sword() -> void:
	gear = Gear.SWORD


## A hit from something at `from`. It knocks his gear away if he has any, and
## otherwise costs a heart, unless he cannot be touched or is still
## invulnerable; returns whether it did.
func take_hit(from: Vector2) -> bool:
	if not can_be_touched() or is_invulnerable():
		return false
	var away := signf(global_position.x - from.x)
	if away == 0.0:
		away = -facing
	var lost_gear := gear != Gear.NONE
	if lost_gear:
		_drop_gear(away)
	else:
		hearts -= 1
		hearts_changed.emit(hearts)
	Sfx.play(&"hurt")
	facing = -int(away) # he turns toward the hit
	_turn_time_left = 0.0
	_slash_clock = -1.0
	_invulnerable_left = invulnerable_time
	hit.emit()
	if not lost_gear and hearts <= 0:
		mode = Mode.DEFEATED
		velocity.x = 0.0
		defeated.emit()
	else:
		mode = Mode.HURT
		_hurt_time_left = hurt_time
		velocity = Vector2(away * knockback.x, -knockback.y)
	return true


## He landed on an enemy from above. The bounce starts on his next tick, so
## every enemy he lands on in the same tick sees him still falling.
func bounce() -> void:
	_bounce_pending = true


## He fell below a cliff: he keeps falling, out of the player's control, and
## the fall costs a heart (with no knockback; the level plays the hurt sound as
## he crosses the kill line). Returns whether it was his last heart.
func fall_out() -> bool:
	mode = Mode.FALLEN
	_slash_clock = -1.0
	hearts = maxi(hearts - 1, 0)
	hearts_changed.emit(hearts)
	return hearts == 0


## Puts him back on his feet at a checkpoint, without gear, facing right,
## getting back up, and invulnerable for a moment. After a defeat his hearts are
## full again; after a fall he keeps the ones he has left.
func respawn_at(spot: Vector2, refill_hearts: bool) -> void:
	global_position = spot
	velocity = Vector2.ZERO
	facing = 1
	gear = Gear.NONE
	_slash_clock = -1.0
	_turn_time_left = 0.0
	_bounce_pending = false
	if refill_hearts:
		hearts = max_hearts
		hearts_changed.emit(hearts)
	_invulnerable_left = invulnerable_time
	mode = Mode.RESPAWNING
	_respawn_time_left = respawn_time


func celebrate() -> void:
	mode = Mode.CELEBRATING
	_slash_clock = -1.0


func _physics_process(delta: float) -> void:
	if _bounce_pending:
		_bounce_pending = false
		velocity.y = -stomp_bounce
	var in_control := mode == Mode.PLAY
	var dir := _input_direction() if in_control else 0
	if dir != 0 and dir != facing:
		facing = dir
		if is_on_floor():
			velocity.x = 0.0
			_turn_time_left = turn_hold_time
	if dir == 0 or not is_on_floor():
		_turn_time_left = 0.0
	_turn_time_left = maxf(_turn_time_left - delta, 0.0)
	if not (mode == Mode.HURT and not is_on_floor()):
		# A knockback carries him until he lands; otherwise run, or slow down.
		var target_speed := 0.0 if _turn_time_left > 0.0 else dir * run_speed
		velocity.x = move_toward(velocity.x, target_speed, run_accel * delta)

	if not is_on_floor():
		velocity.y += (fall_gravity if velocity.y >= 0.0 else gravity) * delta
	elif in_control and Input.is_action_just_pressed(&"jump"):
		# A fresh press with ground underfoot: holding the key cannot jump again.
		velocity.y = -jump_velocity
		Sfx.play(&"jump")
	if in_control and gear == Gear.SWORD and not is_slashing() and Input.is_action_just_pressed(&"slash"):
		# A fresh press, and not while a swing is under way: one sound per swing.
		_slash_clock = 0.0
		Sfx.play(&"slash")
	move_and_slide()

	_swing(delta)
	_count_down(delta)
	_look.scale.x = facing
	_look.modulate.a = 0.35 if is_invulnerable() and fmod(_invulnerable_left, flash_period) < flash_period / 2.0 else 1.0
	pose = _pick_pose(delta)
	_look.show_pose(pose)


## Moves the swing on and, while its hitbox is live, defeats every goblin in it.
## It asks the physics space directly, so the cut lands on the tick it reaches.
func _swing(delta: float) -> void:
	_sword_box.position.x = slash_reach * facing
	var live := is_slashing() and _slash_clock >= slash_live_from and _slash_clock <= slash_live_to
	_sword_box.disabled = not live
	if live:
		_slash_query.transform = _sword_box.global_transform
		for contact in get_world_2d().direct_space_state.intersect_shape(_slash_query, 8):
			if contact.collider is Goblin:
				(contact.collider as Goblin).defeat(&"slash")
	if is_slashing():
		_slash_clock += delta
		if _slash_clock >= slash_time:
			_slash_clock = -1.0


## The gear flies off, up and away from the hit, and fades.
func _drop_gear(away: float) -> void:
	gear = Gear.NONE
	var flying := FlyingGear.new()
	flying.position = global_position + Vector2(0, -80)
	flying.velocity = Vector2(away * 220.0, -420.0)
	get_parent().add_child(flying)


func _count_down(delta: float) -> void:
	_invulnerable_left = maxf(_invulnerable_left - delta, 0.0)
	if mode == Mode.HURT:
		_hurt_time_left -= delta
		if _hurt_time_left <= 0.0:
			mode = Mode.PLAY
	elif mode == Mode.RESPAWNING:
		_respawn_time_left -= delta
		if _respawn_time_left <= 0.0:
			mode = Mode.PLAY
			respawned.emit()


func _input_direction() -> int:
	var axis := Input.get_axis(&"move_left", &"move_right")
	if axis > 0.0:
		return 1
	if axis < 0.0:
		return -1
	return 0


func _pick_pose(delta: float) -> StringName:
	match mode:
		Mode.CELEBRATING:
			return &"CHAR-CELEBRATE"
		Mode.RESPAWNING:
			return &"CHAR-RESPAWN"
		Mode.DEFEATED:
			return &"CHAR-DEFEAT"
		Mode.HURT:
			return &"CHAR-HURT"
	if is_slashing():
		return &"CHAR-SWORD-SLASH"
	var form := "CHAR-SWORD-" if gear == Gear.SWORD else "CHAR-"
	if not is_on_floor():
		_run_clock = 0.0
		var falling := velocity.y >= 0.0
		if falling and not _was_falling:
			_falls_sideways = absf(velocity.x) > 1.0
		_was_falling = falling
		return StringName(form + ("FALL" if falling and _falls_sideways else "RISE"))
	_was_falling = false
	if absf(velocity.x) > 1.0:
		_run_clock += delta
		var second_frame := fmod(_run_clock, run_frame_time * 2.0) >= run_frame_time
		return StringName(form + ("RUN-B" if second_frame else "RUN-A"))
	_run_clock = 0.0
	return StringName(form + "IDLE")
