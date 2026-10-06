extends Node2D
## Night 1 slice. Owns which way up the world is, wires the pieces together,
## and announces changes.
##
## The camera never rotates. Flipping reverses gravity, so the boy falls upward
## and stands on the ceiling, and the world changes what it is showing:
##
##   normal   - he looks like a living boy in the warm remembered room.
##              This is the comfortable lie, the way he still sees himself.
##   inverted - he is the ghost, and the room is the stripped empty one the
##              new family moved into. This is what is actually there.
##
## The world shows you what you expect; turn it over to see what is there.
##
## Ordering rule, applied everywhere below: state changes first, signal second,
## sound third. Audio is always a consequence, so a muted or missing sound can
## never alter what the game does.

signal world_flipped(is_inverted: bool)

const FLIP_SECONDS := 0.35   ## cross-dissolve between the two truths

var is_inverted := false
var _flipping := false

@onready var _world_root: Node2D = $WorldRoot
@onready var _room_upright: Sprite2D = $WorldRoot/RoomUpright
@onready var _room_memory: Sprite2D = $WorldRoot/RoomMemory
@onready var _player: CharacterBody2D = $Player
@onready var _contact: Area2D = $MusicBox
@onready var _meters: Node = $Meters
@onready var _audio: Node = $Audio
@onready var _hud: CanvasLayer = $HUD
@onready var _box_top: StaticBody2D = $BoxTop


func _ready() -> void:
	world_flipped.connect(_player.set_inverted)
	world_flipped.connect(_contact.set_inverted)
	world_flipped.connect(_audio.set_world_inverted)
	world_flipped.connect(_set_box_top_solid)
	world_flipped.connect(func(_inv): _refresh_hint())

	_contact.contact_landed.connect(_on_contact_landed)
	_meters.day_torn.connect(_on_day_torn)
	_meters.recognition_changed.connect(_on_recognition_changed)
	_meters.night_ended.connect(_on_night_ended)
	_audio.counted.connect(func(_e, _n): _hud.set_mutes(_audio.music_muted, _audio.sfx_muted))

	_room_memory.visible = true
	_room_upright.visible = false
	_hud.set_days(_meters.days_left, _meters.DAYS_AT_START)
	_hud.set_recognition(0, _meters.RECOGNITION_TO_WIN)
	_hud.set_frost(0.0)
	_hud.set_mutes(false, false)
	_refresh_hint()

	if not _audio.missing.is_empty():
		print("audio files not present yet, slice runs silent: ", _audio.missing)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("flip_world"):
		flip()
	elif event.is_action_pressed("restart"):
		get_tree().reload_current_scene()
	elif event.is_action_pressed("mute_music") or event.is_action_pressed("mute_sfx"):
		call_deferred("_sync_mute_label")


func _sync_mute_label() -> void:
	_hud.set_mutes(_audio.music_muted, _audio.sfx_muted)


## Turns the world over. Ignored while a flip is already running, so holding or
## mashing the key cannot emit world_flipped more than once per change.
func flip() -> void:
	if _flipping or _meters.ended:
		return
	_flipping = true
	is_inverted = not is_inverted

	world_flipped.emit(is_inverted)
	_audio.play("flip")

	# Both rooms stay upright and the camera never moves. The truth dissolves
	# in over the lie, which reads far more smoothly than turning the picture
	# over and never disorients the player.
	var appearing: Sprite2D = _room_upright if is_inverted else _room_memory
	var leaving: Sprite2D = _room_memory if is_inverted else _room_upright
	appearing.visible = true
	appearing.modulate.a = 0.0
	var tween := create_tween().set_parallel(true)
	tween.tween_property(appearing, "modulate:a", 1.0, FLIP_SECONDS)
	tween.tween_property(leaving, "modulate:a", 0.0, FLIP_SECONDS)
	await tween.finished
	leaving.visible = false
	leaving.modulate.a = 1.0
	_flipping = false


func _on_contact_landed(kind: String, days_cost: int) -> void:
	var gain: int = _contact.recognition_scary if kind == "scary" else _contact.recognition_kind
	_meters.spend(days_cost, gain)
	_audio.play("contact")
	if kind == "scary":
		# The loud way to be seen also wakes the house: the room corrects itself.
		_audio.play("correct")


func _on_day_torn(days_left: int) -> void:
	_hud.set_days(days_left, _meters.DAYS_AT_START)
	_hud.set_frost(_meters.frost_level())
	_audio.play("frost")


func _on_recognition_changed(recognition: int) -> void:
	_hud.set_recognition(recognition, _meters.RECOGNITION_TO_WIN)


func _on_night_ended(reason: String) -> void:
	if reason == "seen":
		_hud.show_banner("SHE SAW YOU.\n\nR to play again")
	else:
		_hud.show_banner("THE ANNIVERSARY ARRIVED FIRST.\n\nR to play again")
	_audio.finish_music()
	_refresh_hint()


## The stacked moving boxes are solid only in the upright world, because that
## is the only world they exist in. Level geometry obeys the same rule the art
## does: what you can stand on depends on which way up you are.
func _set_box_top_solid(is_inverted: bool) -> void:
	_box_top.get_node("CollisionShape2D").set_deferred("disabled", is_inverted)


func _refresh_hint() -> void:
	if _meters.ended:
		_hud.set_hint("")
	elif is_inverted:
		_hud.set_hint("You are falling upward  ·  walk the ceiling to the music box  ·  tap E to touch it gently, hold E to make it loud  ·  F to come back down")
	else:
		_hud.set_hint("Arrows or A/D to move  ·  SPACE to jump  ·  F to turn the world over")
