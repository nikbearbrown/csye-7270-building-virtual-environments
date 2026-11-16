extends Node2D
## Frame-strip fixture for Effect B (CHANGE-BRIEF "Frame strips"): the real cave background and ground from
## game/main.tscn at in-game camera scale. At frame `start_frame` (process frames from scene start) a trail is added to
## a carrier that moves right at the fireball's speed, 260 px/s, on physics ticks like a fireball. At `stop_frame` the
## condition ends as at an impact: the carrier stops, the fireball sprite is hidden and the trail stops emitting where
## it is. Only this preview instance uses a fixed seed.
## From fall-2026/zhefan-z/assignment-6/, windowed:
##   Godot_v4.7.2-stable_win64_console.exe --path walker-magic-zhefan --resolution 1280x720 res://previews/fireball_trail_preview.tscn

const TRAIL := preload("res://effects/fireball_trail.tscn")
const SPEED := 260.0   # features/fireball/fireball.gd SPEED

@export var start_position := Vector2(150, 267)
@export var start_frame := 10
@export var stop_frame := 40
@export var trail_seed := 1

var _frame := 0
var _moving := false
var _trail: GPUParticles2D

@onready var carrier: Node2D = $Carrier
@onready var fireball_sprite: Sprite2D = $Carrier/FireballSprite


func _ready() -> void:
	carrier.visible = false


func _physics_process(delta: float) -> void:
	if _moving:
		carrier.position.x += SPEED * delta


func _process(_delta: float) -> void:
	if _frame == start_frame:
		carrier.position = start_position
		carrier.visible = true
		_trail = TRAIL.instantiate()
		_trail.use_fixed_seed = true
		_trail.seed = trail_seed
		carrier.add_child(_trail)
		_moving = true
		_log("start")
	elif _frame == stop_frame:
		_moving = false
		fireball_sprite.visible = false
		_trail.emitting = false
		_log("stop")
	_frame += 1


func _log(event: String) -> void:
	print(JSON.stringify({"preview": "trail", "event": event, "frame": _frame, "position": carrier.position}))
