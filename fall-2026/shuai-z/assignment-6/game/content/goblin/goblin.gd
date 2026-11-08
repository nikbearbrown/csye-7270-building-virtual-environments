class_name Goblin
extends Area2D
## A patrolling goblin (ENEMY-GOBLIN). It walks back and forth between where it
## starts and `patrol_distance` px to its right. Landing on it from above
## defeats it, with one stomp sound, and bounces Rudy up; touching it any other
## way costs him a heart. After Rudy dies the level calls reset(), and the
## goblin is back where it started, even if it was defeated.
## It asks the physics space each tick whether its box touches Rudy, instead of
## reading the area's overlap list, which reports a contact two ticks late: by
## then a fast fall has sunk his soles too deep to tell a stomp from a side hit.
## Its art (ENEMY-GOBLIN) is two walk frames and a squashed frame, generated
## facing right and mirrored when it walks left, drawn at half scale from
## props.json's origin (its feet) with the outer outline. The box that hurts
## and that Rudy stomps is 40 x 118 px: its body up to the top of its head, not
## its ears, its nose, its swinging arms or the wisps of its hair.
## The origin is at its feet.

const WALK_A := preload("res://content/goblin/frames/ENEMY-GOBLIN-WALK-A.png")
const WALK_B := preload("res://content/goblin/frames/ENEMY-GOBLIN-WALK-B.png")
const SQUASH := preload("res://content/goblin/frames/ENEMY-GOBLIN-SQUASH.png")
const HEIGHT := 118.0 ## the box's height: the top of its head
const WIDTH := 40.0 ## the box's width: its body
const STOMP_MARGIN := 14.0 ## px: Rudy's soles must have been at most this far below its top before his last move
const WALK_FRAME_TIME := 0.18
const SQUASH_TIME := 0.4 ## s the squashed frame shows before it disappears

@export var patrol_distance := 400.0 ## px to the right of where it starts
@export var speed := 100.0 ## px/s

var dead := false
var facing := 1

var _start_x := 0.0
var _walk_clock := 0.0
var _squash_left := 0.0
var _query := PhysicsShapeQueryParameters2D.new()

@onready var _box: CollisionShape2D = $Shape
@onready var _art: Sprite2D = $Art


func _ready() -> void:
	_start_x = position.x
	_query.shape = _box.shape
	_query.collision_mask = 2 # the Player layer
	_query.collide_with_areas = false


func _physics_process(delta: float) -> void:
	if dead:
		if _squash_left > 0.0:
			_squash_left -= delta
			if _squash_left <= 0.0:
				visible = false
		return
	_patrol(delta)
	_query.transform = _box.global_transform
	for contact in get_world_2d().direct_space_state.intersect_shape(_query, 4):
		if contact.collider is Rudy:
			_touch(contact.collider as Rudy, delta)


## Defeats it once. It stops touching anything before the sound plays, so a
## defeated goblin ignores every later hit.
func defeat(cause: StringName) -> void:
	if dead:
		return
	dead = true
	set_deferred("monitorable", false)
	_squash_left = SQUASH_TIME
	_show_frame()
	if cause == &"stomp":
		Sfx.play(&"stomp")


## Back where it started, alive, walking right.
func reset() -> void:
	dead = false
	position.x = _start_x
	facing = 1
	_walk_clock = 0.0
	_squash_left = 0.0
	visible = true
	set_deferred("monitorable", true)
	_show_frame()


func _patrol(delta: float) -> void:
	position.x += facing * speed * delta
	# Turn at each end. It only turns, so a goblin placed outside its patrol
	# walks back into it instead of jumping there.
	if position.x >= _start_x + patrol_distance:
		facing = -1
	elif position.x <= _start_x:
		facing = 1
	_walk_clock += delta
	_show_frame()


func _touch(rudy: Rudy, delta: float) -> void:
	if not rudy.can_be_touched():
		return
	var top := global_position.y - HEIGHT
	var soles_before := rudy.global_position.y - rudy.velocity.y * delta
	if rudy.velocity.y > 0.0 and soles_before <= top + STOMP_MARGIN:
		defeat(&"stomp")
		rudy.bounce()
	else:
		rudy.take_hit(global_position)


func _walk_frame() -> int:
	return int(_walk_clock / WALK_FRAME_TIME) % 2


## The frame for its state, facing the way it walks.
func _show_frame() -> void:
	_art.texture = SQUASH if dead else (WALK_B if _walk_frame() == 1 else WALK_A)
	_art.flip_h = facing < 0
