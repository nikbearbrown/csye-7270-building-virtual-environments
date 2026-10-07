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

## Lines of his, placed where they mean something and shown once each. They are
## not instructions; nothing here tells the player what to press. They are what
## he thinks when he passes a particular spot in his own house.
const NOTES := [
	{ "x":  980, "world": "memory",   "text": "They took my name off the door." },
	{ "x": 1548, "world": "truth",    "text": "My mother wound this one. It still turns for me." },
	{ "x": 2200, "world": "memory",   "text": "None of this is here any more. Only I can still see it." },
	{ "x": 3150, "world": "truth",    "text": "My shoes. Still by the door. I never put them on." },
	{ "x": 3400, "world": "truth",    "text": "These are theirs. I cannot move anything of theirs." },
	{ "x": 5120, "world": "truth",    "text": "Under this board is my name, where I scratched it." },
]

## What he thinks the moment after a relic answers him. The whole causal chain
## the game was missing lives in these three lines: he moves a thing of his,
## she experiences it, and the third one carries his name.
const AFTER_CONTACT := [
	"She heard that. She will say the house is settling.",
	"Twice now. She has stopped saying it.",
	"She is looking at where I am.",
]
var _notes_shown := {}

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
@onready var _child: Sprite2D = $Child

## Her posture is the recognition meter. She is only in the real house, because
## that is the only house she lives in.
const CHILD_POSES := [
	preload("res://assets/art/child_1.png"),   # playing, absorbed, has not heard anything
	preload("res://assets/art/child_2.png"),   # looking up: something made a sound
	preload("res://assets/art/child_3.png"),   # facing you, eyes wide: she has seen
]



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
	world_flipped.connect(func(inv): _child.visible = inv)
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
## The words the game opens with, and the same words the player can call back
## at any time with I. Kept in one place so the two can never say different
## things.
const STORY := [
	"They told everyone I ran away.",
	"I never left this house.",
	"I cannot touch her. Only my own things still move for me.",
	"If she sees them move, she will know I was here.",
]

var _skip_opening := false
var _awaiting_key := false
var _story_open := false
var _control_before_story := false
var _has_moved := false
var _has_flipped := false
var _has_contacted := false


## Blocks until the player presses something. The opening advances at their
## reading speed, not at a speed I guessed.
func wait_for_key() -> void:
	_awaiting_key = true
	while _awaiting_key:
		await get_tree().process_frame


func _open() -> void:
	_player.controllable = false
	# The opening waits for the player rather than for a clock, so there is no
	# timeout here: it cannot overrun, only wait.
	_hud.set_hint("")

	# start in the truth
	is_inverted = true
	_show_rooms(true)
	_apply_world_geometry(true)
	_player.set_inverted(true)
	_audio.set_world_inverted(true)
	_child.visible = true
	_player.global_position = Vector2(620.0, 265.0)
	await get_tree().create_timer(1.1).timeout

	await _hud.show_opening(STORY, self)

	# The memory closes over the truth rather than replacing it. He fades out of
	# the ceiling as a ghost and fades in on the floor as a boy, with the rooms
	# dissolving across the same two seconds, so the change reads as one world
	# becoming another rather than as two pictures being swapped.
	await get_tree().create_timer(0.35).timeout
	_audio.play("flip")

	# Timed from one clock rather than by awaiting several tweens in turn.
	# Awaiting `finished` on a tween that has already finished waits forever,
	# and whether it has depends on frame timing, so the previous version handed
	# over control on some machines and stranded the player on others.
	var fade_out := create_tween()
	fade_out.tween_property(_player, "modulate:a", 0.0, 0.7)
	for r in _rooms_memory:
		r.visible = true
		r.modulate.a = 0.0
	var bloom := create_tween().set_parallel(true)
	for r in _rooms_memory:
		bloom.tween_property(r, "modulate:a", 1.0, 1.6)
	for r in _rooms_empty:
		bloom.tween_property(r, "modulate:a", 0.0, 1.6)

	await get_tree().create_timer(0.7).timeout

	is_inverted = false
	_apply_world_geometry(false)
	_player.set_inverted(false)
	_audio.set_world_inverted(false)
	_player.global_position = Vector2(620.0, 815.0)
	_player.velocity = Vector2.ZERO
	_child.visible = false

	var fade_in := create_tween()
	fade_in.tween_property(_player, "modulate:a", 1.0, 0.9)

	await get_tree().create_timer(1.0).timeout
	for r in _rooms_empty:
		r.visible = false
		r.modulate.a = 1.0

	_finish_opening()


## Everything that must be true once the player has the controls, in one place
## so the safety net and the normal path cannot drift apart.
func _finish_opening() -> void:
	if _player.controllable:
		return
	_hud.hide_opening()
	is_inverted = false
	_show_rooms(false)
	_apply_world_geometry(false)
	_player.set_inverted(false)
	_audio.set_world_inverted(false)
	_child.visible = false
	_player.modulate.a = 1.0
	if _player.global_position.y < 500.0:
		_player.global_position = Vector2(620.0, 815.0)
	_player.velocity = Vector2.ZERO
	_player.controllable = true
	for relic in _relics:
		relic.start_calling()
	_audio.set_days_left(_meters.days_left, _meters.DAYS_AT_START)
	_refresh_hint()


func _unhandled_input(event: InputEvent) -> void:
	# I reopens the story at any time, including while it is open.
	if event.is_action_pressed("story"):
		if _story_open:
			_story_open = false
			_hud.hide_story()
			_player.controllable = _control_before_story
		elif _player.controllable:
			_story_open = true
			_control_before_story = true
			_player.controllable = false
			_hud.show_story(STORY)
		return

	if _story_open:
		return

	if not _player.controllable:
		# During the opening a key press means "I have read this line", so it
		# advances rather than skipping.
		if event is InputEventKey and event.pressed and not event.echo:
			_awaiting_key = false
		return
	if event.is_action_pressed("flip_world"):
		_has_flipped = true
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
	_has_contacted = true
	var found: int = mini(_meters.recognition, AFTER_CONTACT.size()) - 1
	if found >= 0:
		_hud.show_note(AFTER_CONTACT[found])
	_refresh_hint()
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
	# She hears before she sees. One relic and she looks up; all three and she
	# is looking straight at where you are.
	var pose := 0
	if recognition >= _meters.RECOGNITION_TO_WIN:
		pose = 2
	elif recognition > 0:
		pose = 1
	if _child.texture != CHILD_POSES[pose]:
		_child.texture = CHILD_POSES[pose]
		var tween := create_tween()
		_child.modulate.a = 0.25
		tween.tween_property(_child, "modulate:a", 1.0, 0.6)


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
	_check_notes()
	_update_cue()


## A note appears when he reaches the spot it belongs to, in the world it
## belongs to, and never again.
## Teaching by obstruction rather than by a list of keys. The cue appears only
## where it can be acted on: beside the relic you cannot reach, and only once
## you are standing under it. It stops appearing once you have used it.
func _update_cue() -> void:
	if not _player.controllable or _meters.ended:
		_hud.hide_cue()
		return
	if absf(_player.velocity.x) > 10.0:
		_has_moved = true

	var nearest = null
	var best := 420.0
	for relic in _relics:
		if relic.is_answered():
			continue
		var d: float = absf(relic.global_position.x - _player.global_position.x)
		if d < best:
			best = d
			nearest = relic

	var cam_x: float = _player.get_node("Camera").get_screen_center_position().x
	if not _has_moved:
		# screen space, not world space: the HUD lives on a CanvasLayer
		_hud.show_cue("\u2190  \u2192", Vector2(960.0 + _player.global_position.x - cam_x, 560.0))
		return
	if nearest == null:
		_hud.hide_cue()
		return

	var on_screen := Vector2(960.0 + nearest.global_position.x - cam_x, nearest.global_position.y)
	if nearest._available():
		_hud.show_cue("E", on_screen)                 # in reach: take it
	elif not is_inverted:
		_hud.show_cue("F", on_screen)                 # visible but out of reach: turn the world over
	else:
		_hud.hide_cue()


func _check_notes() -> void:
	if not _player.controllable or _meters.ended:
		return
	var here := "truth" if is_inverted else "memory"
	for i in NOTES.size():
		if _notes_shown.has(i):
			continue
		var note: Dictionary = NOTES[i]
		if note["world"] != here:
			continue
		if absf(_player.global_position.x - float(note["x"])) < 180.0:
			_notes_shown[i] = true
			_hud.show_note(note["text"])
			return


func _refresh_hint() -> void:
	if _meters.ended:
		_hud.set_hint("")
	elif is_inverted and not _has_contacted:
		_hud.set_hint("tap E to touch it gently  ·  hold E to make it loud")
	else:
		_hud.set_hint("")
