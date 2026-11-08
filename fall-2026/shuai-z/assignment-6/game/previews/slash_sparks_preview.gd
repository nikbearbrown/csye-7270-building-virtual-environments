extends Node2D
## A fixture, not the game: Effect A over Level 1 at in-game camera scale, for
## the frame strip (CHANGE-BRIEF.md, section 6). Every capture of it is a
## fixture capture.
## The real level is the background, with its gameplay objects frozen; a
## frozen sprite of Rudy in CHAR-SWORD-SLASH, drawn as rudy.tscn draws him,
## stands at x = 2200 facing right, so his hitbox is at (2250, 764), where both
## bursts sit. Burst1 fires on frame 10; with `retrigger` on, Burst2 fires on
## frame 20, 0.333 s later at 30 fps, and Burst1 runs on. The two bursts are
## separate instances, as the overlap rule asks (A3), each with its own fixed
## seed, set in the scene. Frames are counted from 0, one per _process(), which
## is one Movie Maker frame. Capture at 30 fps with --quit-after 60.

const FIRST_FRAME := 10
const SECOND_FRAME := 20
## Level 1's gameplay objects, held still so the background does not change.
const FROZEN: Array[NodePath] = [^"Level1/Enemies", ^"Level1/Hazards", ^"Level1/SwordPickup",
	^"Level1/Waystone", ^"Level1/Portal"]

@export var retrigger := true

var _frame := 0


func _ready() -> void:
	for path in FROZEN:
		get_node(path).process_mode = Node.PROCESS_MODE_DISABLED


func _process(_delta: float) -> void:
	if _frame == FIRST_FRAME:
		_fire($Burst1)
	elif _frame == SECOND_FRAME and retrigger:
		_fire($Burst2)
	_frame += 1


func _fire(burst: Node2D) -> void:
	for emitter: GPUParticles2D in burst.get_children():
		emitter.emitting = true
	print("PREVIEW frame %d: %s fired at %s" % [_frame, burst.name, burst.global_position])
