class_name Wolf
extends CharacterBody2D
## One wolf, one static image per state: patrol (run), growl telegraph (lunge image, standing),
## lunge (lunge image, moving, hitbox on), recover (run image, standing), dead (down image).
## 2 HP; each hit flashes white; on death: flash, down image, then removed (no corpse).

## SFX-WOLF-DOWN listens to this. Emitted once: `dead` is set before it, and the body leaves the
## enemy layer with set_deferred, so a second fireball in the same frame is ignored.
signal defeated

enum State { PATROL, GROWL, LUNGE, RECOVER, DEAD }

const TEX_RUN := preload("res://assets/sprites/wolf/wolf_run.png")
const TEX_LUNGE := preload("res://assets/sprites/wolf/wolf_lunge.png")
const TEX_DOWN := preload("res://assets/sprites/wolf/wolf_down.png")

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


func _ready() -> void:
	collision_layer = 1 << 2   # enemy (fireballs mask it)
	collision_mask = 1 << 0    # world
	lunge_hitbox.collision_layer = 0
	lunge_hitbox.collision_mask = 1 << 1   # player
	lunge_hitbox.monitoring = false
	sprite.material = sprite.material.duplicate()
	_show(TEX_RUN)


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
			_show(TEX_RUN)
		State.GROWL:
			_timer = GROWL_TIME
			_show(TEX_LUNGE)
		State.LUNGE:
			_timer = LUNGE_TIME
			_hit_this_lunge = false
			lunge_hitbox.monitoring = true
			_show(TEX_LUNGE)
		State.RECOVER:
			_timer = RECOVER_TIME
			lunge_hitbox.set_deferred("monitoring", false)
			_show(TEX_RUN)


func _sees_player() -> bool:
	if target == null or not is_instance_valid(target) or target.get("is_failing"):
		return false
	var d := target.global_position - global_position
	return absf(d.x) <= SIGHT_X and absf(d.y) <= SIGHT_Y


func _face_target() -> void:
	if target and is_instance_valid(target):
		facing = 1 if target.global_position.x >= global_position.x else -1


func _apply_facing() -> void:
	sprite.flip_h = facing < 0        # the art faces right
	body_shape.position.x = 8.0 * facing
	lunge_hitbox.position.x = 8.0 * facing


func _show(tex: Texture2D) -> void:
	sprite.texture = tex


## Called by a fireball. A dead wolf ignores further hits.
func take_damage(amount: int) -> void:
	if dead:
		return
	hp -= amount
	_flash()
	if hp > 0:
		return
	dead = true
	state = State.DEAD
	set_deferred("collision_layer", 0)
	lunge_hitbox.set_deferred("monitoring", false)
	_show(TEX_DOWN)
	defeated.emit()
	await get_tree().create_timer(DOWN_TIME, false).timeout
	queue_free()


func _flash() -> void:
	var mat := sprite.material as ShaderMaterial
	mat.set_shader_parameter("flash", 1.0)
	await get_tree().create_timer(FLASH_TIME, false).timeout
	if is_instance_valid(self):
		mat.set_shader_parameter("flash", 0.0)
