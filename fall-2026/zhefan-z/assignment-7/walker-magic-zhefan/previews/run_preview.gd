extends Node2D
## Frame-strip fixture for clip 1, the mage run cycle (CHANGE-BRIEF Clip 1 and "Watching and evidence"): the real cave
## background and ground at in-game camera scale, the player scene standing still (its physics off, so the state machine
## never runs), and its AnimationPlayer starting `run` on physics tick `start_tick`. Fixture only: the game does not wire
## the clips yet. From fall-2026/zhefan-z/assignment-7/, windowed:
##   Godot_v4.7.2-stable_win64_console.exe --path walker-magic-zhefan res://previews/run_preview.tscn

@export var start_tick := 10

var _tick := 0

@onready var player: Node2D = $Player
@onready var anim: AnimationPlayer = $Player/AnimationPlayer


func _ready() -> void:
	player.set_physics_process(false)   # no state machine: only the clip changes the sprite


func _physics_process(_delta: float) -> void:
	if _tick == start_tick:
		anim.play("run")
	_tick += 1
