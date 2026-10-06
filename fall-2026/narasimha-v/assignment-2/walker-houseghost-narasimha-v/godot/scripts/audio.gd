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
## One track per world. They share key and tempo, so the flip can cut straight
## from one to the other without a musical lurch: the two worlds sound like one
## piece of music turning over.
## The warm track belongs to the lie, the tense one to the truth.
const MUSIC_PATHS := {
	"normal":   "res://assets/music/mus_memory.wav",
	"inverted": "res://assets/music/mus_upright.wav",
}

var counts := {"flip": 0, "contact": 0, "frost": 0, "correct": 0}
var music_muted := false
var sfx_muted := false
var missing: Array[String] = []

var _players := {}
var _music := {}                 ## world -> AudioStreamPlayer
var _current_world := "normal"


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

	for world in MUSIC_PATHS:
		var player := AudioStreamPlayer.new()
		player.name = "music_%s" % world
		var stream := _load_or_note(MUSIC_PATHS[world])
		if stream:
			# Loop forward over the whole file. Set here rather than relying on
			# the import setting, which does not survive a reimport reliably,
			# and with loop_end given explicitly because it defaults to zero,
			# which produces a zero-length loop that stops instantly. Each file
			# was cut with two seconds of its own tail crossfaded back over its
			# head, so the seam is inaudible wherever the playhead wraps.
			if stream is AudioStreamWAV:
				stream.loop_begin = 0
				stream.loop_end = int(stream.get_length() * stream.mix_rate)
				stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
			player.stream = stream
		add_child(player)
		_music[world] = player

	_play_world_music(_current_world)


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
	_play_world_music(_current_world)


func _play_world_music(world: String) -> void:
	for w in _music:
		var player: AudioStreamPlayer = _music[w]
		if w == world:
			if player.stream and not music_muted and not player.playing:
				player.play()
		elif player.playing:
			player.stop()


## Predicted behaviour from CHANGE-BRIEF: the lullaby belongs to the remembered
## world only, and the flip hard-cuts it rather than crossfading, because the
## cut is what makes the flip feel like crossing a threshold.
func set_world_inverted(is_inverted: bool) -> void:
	_current_world = "inverted" if is_inverted else "normal"
	_play_world_music(_current_world)


func set_music_muted(value: bool) -> void:
	music_muted = value
	if music_muted:
		for w in _music:
			_music[w].stop()
	else:
		_play_world_music(_current_world)


func set_sfx_muted(value: bool) -> void:
	sfx_muted = value


## End of the slice: the lullaby is allowed to finish its phrase once and then
## stop. It is the only clean musical resolution in the slice, reserved for
## endings.
func finish_music() -> void:
	for w in _music:
		var player: AudioStreamPlayer = _music[w]
		if player.playing:
			var tween := create_tween()
			tween.tween_property(player, "volume_db", -40.0, 2.5)
			await tween.finished
			player.stop()
			player.volume_db = 0.0
