class_name Wolf
extends CharacterBody2D
## One wolf. Its AnimationPlayer (features/wolf/wolf.tscn) shows each state: patrol (run image), growl, lunge and
## recover (one clip, `lunge`, started on GROWL entry and left running through LUNGE and RECOVER: the cutout rig under
## Facing), dead (down image). Code never writes what the clips key; it keeps the facing (Facing.scale.x, the whole
## sprite's flip_h) and the hitbox. 2 HP; each hit flashes white; on death: flash, down image, then removed (no corpse).

## SFX-WOLF-DOWN listens to this. Emitted once: `dead` is set before it, and the body leaves the
## enemy layer with set_deferred, so a second fireball in the same frame is ignored.
signal defeated

enum State { PATROL, GROWL, LUNGE, RECOVER, DEAD }

const TEX_RUN := preload("res://assets/sprites/wolf/wolf_run.png")
const TEX_LUNGE := preload("res://assets/sprites/wolf/wolf_lunge.png")
const TEX_DOWN := preload("res://assets/sprites/wolf/wolf_down.png")

## The clip each state shows. GROWL starts `lunge`; LUNGE and RECOVER leave it running (CHANGE-BRIEF Clip 2).
const CLIPS := {
	State.PATROL: &"patrol", State.GROWL: &"lunge", State.LUNGE: &"lunge", State.RECOVER: &"lunge", State.DEAD: &"dead",
}

## The first frame of the recovery section of `lunge` (CHANGE-BRIEF revision 2026-11-10 phase table).
const RECOVER_FRAME := 53

const MAX_HP := 2
const PATROL_SPEED := 45.0
const SIGHT_X := 120.0          # sees the player this far ahead (and behind, see _sees_player)
const SIGHT_Y := 40.0
const GROWL_TIME := 0.5         # CHANGE-BRIEF tuning: 0.5 s growl
const LUNGE_SPEED := 220.0
const LUNGE_TIME := 0.35
const RECOVER_TIME := 0.6
const DAMAGE := 1
const FLASH_TIME := 0.1
const DOWN_TIME := 0.6          # down image shown this long before the wolf disappears

@export var patrol_left := 760.0
@export var patrol_right := 960.0
## Never lunge past these (keeps the wolf on its ground strip, away from the pit).
@export var min_x := 600.0
@export var max_x := 1260.0

var hp := MAX_HP
var dead := false
var state: State = State.PATROL
var facing := -1
var target: Node2D               # the player; set by Main
var _timer := 0.0
var _hit_this_lunge := false

@onready var sprite: Sprite2D = $Sprite2D
@onready var body_shape: CollisionShape2D = $CollisionShape2D
@onready var lunge_hitbox: Area2D = $LungeHitbox
@onready var facing_node: Node2D = $Facing
@onready var anim: AnimationPlayer = $AnimationPlayer


func _ready() -> void:
	collision_layer = 1 << 2   # enemy (fireballs mask it)
	collision_mask = 1 << 0    # world
	lunge_hitbox.collision_layer = 0
	lunge_hitbox.collision_mask = 1 << 1   # player
	lunge_hitbox.monitoring = false
	sprite.material = sprite.material.duplicate()
	facing_node.material = sprite.material   # one flash material for the whole sprite and every rig part
	_play(CLIPS[State.PATROL])


func _physics_process(delta: float) -> void:
	_timer = maxf(_timer - delta, 0.0)
	match state:
		State.PATROL:
			if global_position.x <= patrol_left:
				facing = 1
			elif global_position.x >= patrol_right:
				facing = -1
			velocity.x = PATROL_SPEED * facing
			if _sees_player():
				_enter(State.GROWL)
		State.GROWL:
			velocity.x = 0.0
			_face_target()
			if _timer == 0.0:
				_enter(State.LUNGE)
		State.LUNGE:
			velocity.x = LUNGE_SPEED * facing
			if not _hit_this_lunge:
				for body in lunge_hitbox.get_overlapping_bodies():
					if body.has_method("take_damage"):
						body.take_damage(DAMAGE, global_position.x)
						_hit_this_lunge = true
			if _timer == 0.0:
				_enter(State.RECOVER)
		State.RECOVER:
			velocity.x = 0.0
			if _timer == 0.0:
				_enter(State.PATROL)
		State.DEAD:
			velocity.x = 0.0
	velocity.y = 0.0
	move_and_slide()
	global_position.x = clampf(global_position.x, min_x, max_x)
	_apply_facing()


func _enter(next: State) -> void:
	state = next
	match next:
		State.PATROL:
			_play(CLIPS[State.PATROL])
		State.GROWL:
			_timer = GROWL_TIME
			_play(CLIPS[State.GROWL])
		State.LUNGE:
			_timer = LUNGE_TIME
			_hit_this_lunge = false
			lunge_hitbox.monitoring = true
		State.RECOVER:
			_timer = RECOVER_TIME
			lunge_hitbox.set_deferred("monitoring", false)


func _sees_player() -> bool:
	if target == null or not is_instance_valid(target) or target.get("is_failing") or target.get("is_cleared"):
		return false
	var d := target.global_position - global_position
	return absf(d.x) <= SIGHT_X and absf(d.y) <= SIGHT_Y


func _face_target() -> void:
	if target and is_instance_valid(target):
		facing = 1 if target.global_position.x >= global_position.x else -1


func _apply_facing() -> void:
	sprite.flip_h = facing < 0        # the art faces right
	facing_node.scale.x = facing
	body_shape.position.x = 8.0 * facing
	lunge_hitbox.position.x = 8.0 * facing


## From the clip's first frame, applied at once, on the physics callback from then on.
func _play(clip: StringName) -> void:
	anim.play(clip)
	anim.seek(0.0, true)


## Called by a fireball. A dead wolf ignores further hits. A hit that leaves HP during GROWL cancels the lunge: the wolf
## goes straight to RECOVER and the clip jumps to the recovery section (CHANGE-BRIEF "Behaviour change"). Hits in
## LUNGE, RECOVER and PATROL change only HP; the last HP kills in every phase.
func take_damage(amount: int) -> void:
	if dead:
		return
	hp -= amount
	_flash()
	if hp > 0:
		if state == State.GROWL:
			_enter(State.RECOVER)
			# The hit is resolved before this tick's update, and the clip advances one frame in that update: seeking one
			# frame early makes the hit tick show frame 53, as a normal RECOVER entry does (tests/test_anim_edges.gd).
			anim.seek((RECOVER_FRAME - 1) / 60.0, true)
		return
	dead = true
	state = State.DEAD
	set_deferred("collision_layer", 0)
	lunge_hitbox.set_deferred("monitoring", false)
	_play(CLIPS[State.DEAD])
	defeated.emit()
	await get_tree().create_timer(DOWN_TIME, false).timeout
	queue_free()


func _flash() -> void:
	var mat := sprite.material as ShaderMaterial
	mat.set_shader_parameter("flash", 1.0)
	await get_tree().create_timer(FLASH_TIME, false).timeout
	if is_instance_valid(self):
		mat.set_shader_parameter("flash", 0.0)
