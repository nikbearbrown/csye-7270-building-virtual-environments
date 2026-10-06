extends Node2D
## Night 1 slice. Owns which way up the world is and announces changes.
##
## The room turns over; the boy does not. He stays upright and his controls
## never reverse, so after a flip he is walking the ceiling of the room as he
## remembers it — which is what the concept describes a ghost doing.
##
## Sound never decides state here: every audio cue listens to a signal that is
## emitted after the state has already changed, so a muted or missing sound
## cannot alter what the game does.

signal world_flipped(is_inverted: bool)

const FLIP_SECONDS := 0.6

var is_inverted := false
var _flipping := false

@onready var _world_root: Node2D = $WorldRoot
@onready var _room_upright: Sprite2D = $WorldRoot/RoomUpright
@onready var _room_memory: Sprite2D = $WorldRoot/RoomMemory
@onready var _player: CharacterBody2D = $Player


func _ready() -> void:
	world_flipped.connect(_player.set_inverted)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("flip_world"):
		flip()
	elif event.is_action_pressed("restart"):
		get_tree().reload_current_scene()


## Turns the world over. Ignored while a flip is already running, so holding or
## mashing the key cannot emit world_flipped more than once per change.
func flip() -> void:
	if _flipping:
		return
	_flipping = true
	is_inverted = not is_inverted

	_room_upright.visible = not is_inverted
	_room_memory.visible = is_inverted
	world_flipped.emit(is_inverted)

	var target_rotation := PI if is_inverted else 0.0
	var tween := create_tween()
	tween.tween_property(_world_root, "rotation", target_rotation, FLIP_SECONDS) \
		.set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN_OUT)
	await tween.finished
	_flipping = false
