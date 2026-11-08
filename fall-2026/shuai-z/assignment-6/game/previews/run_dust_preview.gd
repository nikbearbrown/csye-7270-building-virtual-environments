extends Node2D
## A fixture, not the game: Effect B over Level 1 at in-game camera scale, for
## the frame strip (CHANGE-BRIEF.md, section 6). Every capture of it is a
## fixture capture.
## The real level is the background, with its gameplay objects frozen. A
## sprite of Rudy, drawn as rudy.tscn draws him, stands idle at x = 1950 on the
## walk line. From frame 10 the condition holds: he runs right at 560 px/s
## (18.67 px a frame at 30 fps) in his run frames, RUN-A then RUN-B every
## 0.125 s as rudy.gd picks them, with the emitter at his soles + (0, -4) and
## the camera following his x, as in the game. On frame 40 the condition ends:
## he stands idle at x = 2510 and the emitter stops emitting. RunDust sits
## before Rudy in the tree, so it draws behind him; its fixed seed is set on
## this instance in the scene. Frames are counted from 0, one per _process(),
## which is one Movie Maker frame. Capture at 30 fps with --quit-after 70.

const START_FRAME := 10
const STOP_FRAME := 40
const START_X := 1950.0
const WALK_Y := 840.0
const FEET_OFFSET := Vector2(0, -4)
const RUN_SPEED := 560.0 ## px/s, rudy.gd's run_speed
const RUN_FRAME_TIME := 0.125 ## s, rudy.gd's run_frame_time
const FPS := 30.0
const IDLE := preload("res://content/rudy/frames/CHAR-IDLE.png")
const RUN_A := preload("res://content/rudy/frames/CHAR-RUN-A.png")
const RUN_B := preload("res://content/rudy/frames/CHAR-RUN-B.png")
## Level 1's gameplay objects, held still so the background does not change.
const FROZEN: Array[NodePath] = [^"Level1/Enemies", ^"Level1/Hazards", ^"Level1/SwordPickup",
	^"Level1/Waystone", ^"Level1/Portal"]

var _frame := 0

@onready var _dust: GPUParticles2D = $RunDust
@onready var _rudy: Node2D = $Rudy
@onready var _sprite: Sprite2D = $Rudy/Sprite
@onready var _camera: Camera2D = $Camera


func _ready() -> void:
	for path in FROZEN:
		get_node(path).process_mode = Node.PROCESS_MODE_DISABLED


func _process(_delta: float) -> void:
	var running := _frame >= START_FRAME and _frame < STOP_FRAME
	var run_frames := clampi(_frame - START_FRAME, 0, STOP_FRAME - START_FRAME)
	_rudy.position = Vector2(START_X + run_frames * RUN_SPEED / FPS, WALK_Y)
	_dust.global_position = _rudy.global_position + FEET_OFFSET
	_camera.position.x = _rudy.position.x
	if running:
		var run_clock := (_frame - START_FRAME) / FPS
		_sprite.texture = RUN_B if fmod(run_clock, RUN_FRAME_TIME * 2.0) >= RUN_FRAME_TIME else RUN_A
	else:
		_sprite.texture = IDLE
	if _dust.emitting != running:
		_dust.emitting = running
		print("PREVIEW frame %d: emitting %s at %s" % [_frame, running, _dust.global_position])
	_frame += 1
