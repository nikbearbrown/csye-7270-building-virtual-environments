extends Node
## All four event sounds and the music loop.
##
## Every player here is driven by a signal that the game emitted AFTER it had
## already changed state, so audio is purely a consequence: muting it, or
## shipping without the files, cannot change what the game does.
##
## Each event has exactly one player and each call is one play(), so one event
## produces one sound. The counters below exist so the automated check can
## assert that, and so a human can read the numbers during a playtest.

signal counted(event: String, total: int)

const PATHS := {
	"flip":    "res://assets/sfx/sfx_flip.ogg",
	"contact": "res://assets/sfx/sfx_contact.ogg",
	"frost":   "res://assets/sfx/sfx_frost.ogg",
	"correct": "res://assets/sfx/sfx_correct.ogg",
}
const MUSIC_PATH := "res://assets/music/mus_lullaby.ogg"

var counts := {"flip": 0, "contact": 0, "frost": 0, "correct": 0}
var music_muted := false
var sfx_muted := false
var missing: Array[String] = []

var _players := {}
var _music: AudioStreamPlayer


func _ready() -> void:
	for event in PATHS:
		var player := AudioStreamPlayer.new()
		player.name = "sfx_%s" % event
		player.bus = "Master"
		var stream := _load_or_note(PATHS[event])
		if stream:
			player.stream = stream
		add_child(player)
		_players[event] = player

	_music = AudioStreamPlayer.new()
	_music.name = "music"
	var music_stream := _load_or_note(MUSIC_PATH)
	if music_stream:
		_music.stream = music_stream
	add_child(_music)


func _load_or_note(path: String) -> AudioStream:
	if ResourceLoader.exists(path):
		return load(path)
	missing.append(path)
	return null


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("mute_music"):
		set_music_muted(not music_muted)
	elif event.is_action_pressed("mute_sfx"):
		set_sfx_muted(not sfx_muted)


## One event, one sound. Called from signal handlers only.
func play(event: String) -> void:
	if not _players.has(event):
		push_warning("audio: unknown event '%s'" % event)
		return
	counts[event] += 1
	counted.emit(event, counts[event])
	if sfx_muted:
		return
	var player: AudioStreamPlayer = _players[event]
	if player.stream:
		player.play()


func start_music() -> void:
	if _music.stream and not music_muted:
		_music.play()


## Predicted behaviour from CHANGE-BRIEF: the lullaby belongs to the remembered
## world only, and the flip hard-cuts it rather than crossfading, because the
## cut is what makes the flip feel like crossing a threshold.
func set_world_inverted(is_inverted: bool) -> void:
	if is_inverted:
		start_music()
	else:
		_music.stop()


func set_music_muted(value: bool) -> void:
	music_muted = value
	if music_muted:
		_music.stop()


func set_sfx_muted(value: bool) -> void:
	sfx_muted = value


## End of the slice: the lullaby is allowed to finish its phrase once and then
## stop. It is the only clean musical resolution in the slice, reserved for
## endings.
func finish_music() -> void:
	if not _music.playing:
		return
	var tween := create_tween()
	tween.tween_property(_music, "volume_db", -40.0, 2.5)
	await tween.finished
	_music.stop()
	_music.volume_db = 0.0
