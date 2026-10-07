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
@onready var _rooms_memory: Array = _tiles("RoomMemory")
@onready var _rooms_empty: Array = _tiles("RoomEmpty")
@onready var _player: CharacterBody2D = $Player
@onready var _relics: Array = get_tree().get_nodes_in_group("relic")
@onready var _meters: Node = $Meters
@onready var _audio: Node = $Audio
@onready var _hud: CanvasLayer = $HUD
@onready var _lost_above: Area2D = $LostAbove



## The background is tiled across the level, one copy of each room per screen.
func _tiles(prefix: String) -> Array:
	var out := []
	for child in $WorldRoot.get_children():
		if child.name.begins_with(prefix):
			out.append(child)
	return out


func _ready() -> void:
	world_flipped.connect(_player.set_inverted)
	for relic in _relics:
		world_flipped.connect(relic.set_inverted)
		relic.contact_landed.connect(_on_contact_landed)
	world_flipped.connect(_audio.set_world_inverted)
	world_flipped.connect(_apply_world_geometry)
	world_flipped.connect(func(_inv): _refresh_hint())

	_lost_above.body_entered.connect(_on_fell_out_of_the_truth)
	# Movement has its own voice now. Both fire from signals the player emits
	# after the physics has already happened, so they report rather than cause.
	_player.jumped.connect(func(): _audio.play("jump"))
	_player.landed.connect(func(_speed): _audio.play("land"))
	# Footsteps belong to the boy who was alive here. The ghost gets none.
	# He keeps a rhythm in both worlds, because movement that makes no sound
	# reads as broken rather than weightless. What changes is what the rhythm
	# is made of: a foot on carpet, or a breath of displaced air.
	_player.stepped.connect(func(): _audio.play("ghoststep" if is_inverted else "step"))
	_meters.day_torn.connect(_on_day_torn)
	_meters.recognition_changed.connect(_on_recognition_changed)
	_meters.night_ended.connect(_on_night_ended)
	_audio.counted.connect(func(_e, _n): _hud.set_mutes(_audio.music_muted, _audio.sfx_muted))
	# the number flinches on every heartbeat, so the sound and the counter are
	# visibly the same thing
	_audio.heart_beat.connect(_hud.pulse_days)

	_show_rooms(false)
	_apply_world_geometry(false)
	_hud.set_days(_meters.days_left, _meters.DAYS_AT_START)
	_hud.set_recognition(0, _meters.RECOGNITION_TO_WIN)
	_hud.set_frost(0.0)
	_hud.set_mutes(false, false)
	_audio.set_days_left(_meters.days_left, _meters.DAYS_AT_START)
	_refresh_hint()

	# The box calls with its own contact sound, so the player hears what the
	# thing they are walking toward will do when they reach it.
	# Every relic calls with the contact sound, so the player hears where the
	# next one is without being told.
	if ResourceLoader.exists("res://assets/sfx/sfx_contact.wav"):
		var chime := load("res://assets/sfx/sfx_contact.wav")
		for relic in _relics:
			relic.set_beacon_stream(chime)

	if not _audio.missing.is_empty():
		print("audio files not present yet, slice runs silent: ", _audio.missing)

	_open()


## The opening. It explains nothing about how to play; it establishes who the
## player is, which is the thing the slice was failing to do. The house is shown
## as it really is first — grey, emptied, with a ghost in it — and only then
## becomes the warm room he remembers. By the time control is handed over, the
## player knows the grey is true, the warm is memory, and which one he belongs
## to.
func _open() -> void:
	_player.controllable = false
	_hud.set_hint("")

	# start in the truth
	is_inverted = true
	_show_rooms(true)
	_apply_world_geometry(true)
	_player.set_inverted(true)
	_audio.set_world_inverted(true)
	_player.global_position = Vector2(620.0, 265.0)
	await get_tree().create_timer(2.2).timeout

	await _hud.show_opening([
		"They told everyone I ran away.",
		"A new family sleeps in my room now.",
		"I need one of them to see me.",
	])

	# and then the memory closes over it
	await get_tree().create_timer(0.5).timeout
	is_inverted = false
	_show_rooms(false)
	_apply_world_geometry(false)
	_player.set_inverted(false)
	_audio.set_world_inverted(false)
	_audio.play("flip")
	_player.global_position = Vector2(620.0, 815.0)
	_player.velocity = Vector2.ZERO
	await get_tree().create_timer(0.8).timeout

	_player.controllable = true
	_refresh_hint()


func _unhandled_input(event: InputEvent) -> void:
	if not _player.controllable:
		return
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

	# Both rooms stay upright and the camera never rotates. The truth dissolves
	# in over the lie, which reads far more smoothly than turning the picture
	# over and never disorients the player.
	var appearing: Array = _rooms_empty if is_inverted else _rooms_memory
	var leaving: Array = _rooms_memory if is_inverted else _rooms_empty
	var tween := create_tween().set_parallel(true)
	for r in appearing:
		r.visible = true
		r.modulate.a = 0.0
		tween.tween_property(r, "modulate:a", 1.0, FLIP_SECONDS)
	for r in leaving:
		tween.tween_property(r, "modulate:a", 0.0, FLIP_SECONDS)
	await tween.finished
	for r in leaving:
		r.visible = false
		r.modulate.a = 1.0
	_flipping = false


## The floor of this house has been pulled apart. Falling through it costs a
## day, which is the only currency the night has — so a missed jump is paid for
## out of the same meter that being seen is paid for.
func _on_fell_out_of_the_truth(_body: Node) -> void:
	if _meters.ended:
		return
	_audio.play("fall")
	_meters.spend(1, 0)
	# back into the lie, standing where the floor still is
	if is_inverted:
		is_inverted = false
		_show_rooms(false)
		world_flipped.emit(false)
	_player.velocity = Vector2.ZERO
	# set down again on the nearest solid stretch of floor
	_player.global_position = Vector2(clampf(_player.global_position.x, 120.0, 1100.0), 815.0)
	_refresh_hint()


func _on_contact_landed(kind: String, days_cost: int) -> void:
	var gain: int = 2 if kind == "scary" else 1
	_meters.spend(days_cost, gain)
	_audio.play("contact")
	# a beat of held silence: the room has noticed, and is listening back
	_audio.hush(1.8)
	if kind == "scary":
		# The loud way to be seen also wakes the house: the room corrects itself.
		_audio.play("correct")


func _on_day_torn(days_left: int) -> void:
	_hud.set_days(days_left, _meters.DAYS_AT_START)
	_audio.set_days_left(days_left, _meters.DAYS_AT_START)
	_hud.set_frost(_meters.frost_level())
	_audio.play("frost")


func _on_recognition_changed(recognition: int) -> void:
	_hud.set_recognition(recognition, _meters.RECOGNITION_TO_WIN)


func _on_night_ended(reason: String) -> void:
	if reason == "seen":
		_hud.show_banner("SHE SAW YOU.\n\nSomeone in this house knows you were here.\n\nR to play again")
	else:
		_hud.show_banner("THE DAY CAME, AND NOBODY SAW YOU.\n\nEvery touch, and every fall, cost you one.\n\nR to play again")
	_audio.finish_music()
	_refresh_hint()


## What you can stand on depends on which world you are in. Furniture that only
## the memory has is solid only while normal; clutter that only the emptied
## house has is solid only while inverted. A blocker you cannot pass on one side
## is clear on the other, so the route alternates between the two worlds.
func _apply_world_geometry(is_inverted: bool) -> void:
	# Things that exist only in his memory are solid only while the memory is
	# what the player is standing in; things that belong to the real house are
	# solid only in the truth.
	for node in get_tree().get_nodes_in_group("solid_in_memory"):
		_set_solid(node, not is_inverted)
	for node in get_tree().get_nodes_in_group("solid_in_truth"):
		_set_solid(node, is_inverted)


func _set_solid(body: Node, on: bool) -> void:
	body.get_node("Shape").set_deferred("disabled", not on)
	body.get_node("Art").visible = on


func _show_rooms(is_inverted: bool) -> void:
	for r in _rooms_memory:
		r.visible = not is_inverted
		r.modulate.a = 1.0
	for r in _rooms_empty:
		r.visible = is_inverted
		r.modulate.a = 1.0


func _process(_delta: float) -> void:
	_audio.set_drifting(is_inverted and absf(_player.velocity.x) > 10.0)


func _refresh_hint() -> void:
	if _meters.ended:
		_hud.set_hint("")
	elif is_inverted:
		_hud.set_hint("You are falling upward  ·  walk the ceiling to the music box  ·  tap E to touch it gently, hold E to make it loud  ·  F to come back down")
	else:
		_hud.set_hint("Arrows or A/D to move  ·  SPACE to jump  ·  F to turn the world over")
