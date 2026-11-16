extends Node2D
## Frame-strip fixture for clip 2, the wolf lunge rig (CHANGE-BRIEF Clip 2, revision 2026-11-10, "Watching and
## evidence"): the real cave background and ground at in-game camera scale, two wolf scenes standing still (their physics
## off, so the AI never runs), one facing right and one facing left (Facing.scale.x and the Sprite2D's flip_h, the two
## things code owns), both starting `lunge` on physics tick `start_tick`. Fixture only: the game does not wire the clips.
## The label (debug only, this preview only) shows the clip frame = clip position x 60 and the phase from the table.
## Run with --fixed-fps 60 so strip frame n is physics tick n. From fall-2026/zhefan-z/assignment-7/, windowed:
##   Godot_v4.7.2-stable_win64_console.exe --path walker-magic-zhefan --fixed-fps 60 res://previews/lunge_preview.tscn

@export var start_tick := 10

var _tick := 0

@onready var wolves: Array[Node2D] = [$WolfRight, $WolfLeft]
@onready var label: Label = $Debug/ClipFrame


func _ready() -> void:
	for wolf in wolves:
		wolf.set_physics_process(false)   # no state machine: only the clip moves the rig
	_face($WolfRight, 1)
	_face($WolfLeft, -1)


func _face(wolf: Node2D, dir: int) -> void:
	wolf.get_node("Facing").scale.x = dir
	wolf.get_node("Sprite2D").flip_h = dir < 0


func _physics_process(_delta: float) -> void:
	if _tick == start_tick:
		for wolf in wolves:
			wolf.get_node("AnimationPlayer").play("lunge")
	_tick += 1


func _process(_delta: float) -> void:
	var anim: AnimationPlayer = $WolfRight/AnimationPlayer
	if anim.current_animation != "lunge" and _tick <= start_tick:
		label.text = "tick %d  lunge not started" % _tick
		return
	var f := roundi(anim.current_animation_position * 60.0)
	var phase := "startup" if f < 31 else ("active" if f < 53 else ("recovery" if f < 89 else "end"))
	label.text = "tick %d  lunge frame %d  %s" % [_tick, f, phase]
