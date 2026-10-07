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
	"flip":    "res://assets/sfx/sfx_flip.wav",
	"contact": "res://assets/sfx/sfx_contact.wav",
	"frost":   "res://assets/sfx/sfx_frost.wav",
	"correct": "res://assets/sfx/sfx_correct.wav",
	"land":    "res://assets/sfx/sfx_land.wav",
	"jump":    "res://assets/sfx/sfx_jump.wav",
	"fall":    "res://assets/sfx/sfx_fall.wav",
	"step":    "res://assets/sfx/sfx_step.wav",
	"ghoststep": "res://assets/sfx/sfx_ghoststep.wav",
}

## The mix. Every file is normalised to the same peak, so these numbers alone
## decide what sits forward and what sits under. Footsteps are deliberately
## quiet: they fire constantly and would exhaust the ear at story-beat level.
const LEVELS := {
	"flip":     0.0,
	"contact":  0.0,
	"frost":    0.0,
	"correct": -2.0,
	"land":    -8.0,
	"jump":    -10.0,
}

## How far the music steps back while a sound plays, and for how long. Without
## this the quieter story sounds sit underneath the score and are never heard.
const DUCK_DB := -15.0      ## the score steps well back, or short sounds are simply lost under it
const DUCK_HOLD := {"flip": 1.2, "contact": 1.4, "correct": 2.0, "frost": 0.6, "land": 0.25, "jump": 0.25, "fall": 1.6, "step": 0.0, "ghoststep": 0.0}
## One track per world. They share key and tempo, so the flip can cut straight
## from one to the other without a musical lurch: the two worlds sound like one
## piece of music turning over.
## The warm track belongs to the lie, the tense one to the truth.
const MUSIC_PATHS := {
	"normal":   "res://assets/music/mus_memory.wav",
	"inverted": "res://assets/music/mus_upright.wav",
}

var counts := {"flip": 0, "contact": 0, "frost": 0, "correct": 0, "land": 0, "jump": 0, "fall": 0, "step": 0, "ghoststep": 0}
var music_muted := false
var sfx_muted := false
var missing: Array[String] = []

const FADE_SECONDS := 0.45       ## crossfade on the flip
const SILENT_DB := -40.0

var _players := {}
var _music := {}                 ## world -> AudioStreamPlayer
var _current_world := "normal"
var _music_tweens := {}
var _duck_tween: Tween
var _heart: AudioStreamPlayer
var _drift: AudioStreamPlayer
var _heart_timer := 0.0
var _heart_rate := 1.0


func _ready() -> void:
	for event in PATHS:
		var player := AudioStreamPlayer.new()
		player.name = "sfx_%s" % event
		player.bus = "Master"
		player.volume_db = LEVELS.get(event, 0.0)
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

	# The ghost has no footsteps. He has displaced air, and it runs while he
	# moves and stops when he stops — the clearest statement in the game that
	# he is not touching anything.
	_drift = AudioStreamPlayer.new()
	_drift.name = "drift"
	if ResourceLoader.exists("res://assets/sfx/sfx_drift.wav"):
		var ds = load("res://assets/sfx/sfx_drift.wav")
		if ds is AudioStreamWAV:
			ds.loop_begin = 0
			ds.loop_end = int(ds.get_length() * ds.mix_rate)
			ds.loop_mode = AudioStreamWAV.LOOP_FORWARD
		_drift.stream = ds
	_drift.volume_db = -15.0
	add_child(_drift)

	_heart = AudioStreamPlayer.new()
	_heart.name = "heart"
	if ResourceLoader.exists("res://assets/sfx/sfx_heart.wav"):
		_heart.stream = load("res://assets/sfx/sfx_heart.wav")
	_heart.volume_db = -34.0
	add_child(_heart)

	_play_world_music(_current_world)


func _load_or_note(path: String) -> AudioStream:
	if ResourceLoader.exists(path):
		return load(path)
	missing.append(path)
	return null


## The heart. Inaudible at seven days, impossible to ignore at one: pressure
## the player feels before they can name it, and no timer on screen.
func set_days_left(days_left: int, total: int) -> void:
	var urgency := 1.0 - float(days_left) / float(maxi(1, total))
	if _heart == null:
		return
	_heart.volume_db = lerpf(-34.0, -9.0, urgency)
	_heart_rate = lerpf(0.95, 2.1, urgency)


func _process(delta: float) -> void:
	if _heart == null or _heart.stream == null or sfx_muted:
		return
	_heart_timer -= delta * _heart_rate
	if _heart_timer <= 0.0:
		_heart_timer = 1.25
		_heart.play()


## Air moving around something that has no feet. Only ever heard as the ghost.
func set_drifting(on: bool) -> void:
	if _drift == null or _drift.stream == null:
		return
	if on and not sfx_muted and not _drift.playing:
		_drift.play()
	elif (not on or sfx_muted) and _drift.playing:
		_drift.stop()


## A held breath. Used after a contact lands, because silence says more about
## being noticed than any sound could.
func hush(seconds: float) -> void:
	_duck(seconds)


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
		_duck(DUCK_HOLD.get(event, 0.5))


func start_music() -> void:
	_play_world_music(_current_world)


## Crossfades rather than cutting. Each track always starts from its own
## beginning rather than resuming mid-phrase, because a game that drops you
## into the middle of a bar sounds broken even when the mix is clean.
func _play_world_music(world: String) -> void:
	for w in _music:
		var player: AudioStreamPlayer = _music[w]
		if w == world:
			if player.stream and not music_muted:
				if not player.playing:
					player.volume_db = SILENT_DB
					player.play(0.0)
				_fade(player, 0.0)
		elif player.playing:
			_fade(player, SILENT_DB, true)


## Steps the music down under a sound effect and brings it back. The game is
## quiet by design, so without ducking the score simply covers the sounds that
## carry the story.
func _duck(hold: float) -> void:
	var player: AudioStreamPlayer = _music.get(_current_world)
	if player == null or not player.playing or music_muted:
		return
	if _duck_tween and is_instance_valid(_duck_tween):
		_duck_tween.kill()
	_duck_tween = create_tween()
	_duck_tween.tween_property(player, "volume_db", DUCK_DB, 0.08)
	_duck_tween.tween_interval(hold)
	_duck_tween.tween_property(player, "volume_db", 0.0, 0.5)


func _fade(player: AudioStreamPlayer, to_db: float, stop_after: bool = false) -> void:
	if _music_tweens.has(player) and is_instance_valid(_music_tweens[player]):
		_music_tweens[player].kill()
	var tween := create_tween()
	_music_tweens[player] = tween
	tween.tween_property(player, "volume_db", to_db, FADE_SECONDS)
	if stop_after:
		tween.tween_callback(player.stop)


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
			if _music[w].playing:
				_fade(_music[w], SILENT_DB, true)
	else:
		_play_world_music(_current_world)


func set_sfx_muted(value: bool) -> void:
	sfx_muted = value
	if sfx_muted and _drift and _drift.playing:
		_drift.stop()


## End of the slice: the lullaby is allowed to finish its phrase once and then
## stop. It is the only clean musical resolution in the slice, reserved for
## endings.
## End of the slice: a long, clean fade. The only musical resolution in the
## slice, reserved for endings.
func finish_music() -> void:
	for w in _music:
		var player: AudioStreamPlayer = _music[w]
		if player.playing:
			if _music_tweens.has(player) and is_instance_valid(_music_tweens[player]):
				_music_tweens[player].kill()
			var tween := create_tween()
			tween.tween_property(player, "volume_db", SILENT_DB, 2.5)
			tween.tween_callback(player.stop)
