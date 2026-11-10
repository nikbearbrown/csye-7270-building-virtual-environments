extends Node2D
## Frame-strip fixture for Effect A (CHANGE-BRIEF "Frame strips"): the real cave background and ground from
## game/main.tscn at in-game camera scale, the impact on the ground cap next to the pit. Triggers at frame
## `trigger_frame` (process frames from scene start); with `retrigger` on (or the user argument `retrigger`), a second
## impact `retrigger_after_frames` later at the same spot. Only these preview instances use a fixed seed, one per spawn.
## From fall-2026/zhefan-z/assignment-6/, windowed:
##   Godot_v4.7.2-stable_win64_console.exe --path walker-magic-zhefan res://previews/fireball_impact_preview.tscn [-- retrigger]

const IMPACT := preload("res://effects/fireball_impact.tscn")
## Seeds 1 apart gave the second impact nearly the first one's random draws (r0-retrigger strip).
const SEED_SPACING := 1000

@export var impact_position := Vector2(510, 327)
@export var trigger_frame := 10
@export var retrigger := false
@export var retrigger_after_frames := 6
@export var first_seed := 1

var _frame := 0
var _spawned := 0


func _ready() -> void:
	if "retrigger" in OS.get_cmdline_user_args():
		retrigger = true


func _process(_delta: float) -> void:
	if _frame == trigger_frame or (retrigger and _frame == trigger_frame + retrigger_after_frames):
		_spawn()
	_frame += 1


func _spawn() -> void:
	var fx: Node2D = IMPACT.instantiate()
	for child in fx.get_children():
		if child is GPUParticles2D:
			child.use_fixed_seed = true
			child.seed = first_seed + SEED_SPACING * _spawned
	fx.position = impact_position
	add_child(fx)
	_spawned += 1
	print(JSON.stringify({"preview": "impact", "frame": _frame, "spawn": _spawned, "position": impact_position}))
