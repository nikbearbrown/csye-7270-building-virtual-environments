class_name AudioDirector
extends Node
## The only place that plays sound. It listens to game signals and never changes game state, so a
## missing or muted sound changes nothing (CHANGE-BRIEF event-to-sound map).
## Uses res://assets/audio/sfx/<ID>.ogg and res://assets/audio/music/MUS-LOOP.ogg when present,
## otherwise code-made placeholders (audio/placeholder_tones.gd).

signal played(id: String)

const SFX_IDS := ["SFX-CAST", "SFX-WOLF-DOWN", "SFX-HURT", "SFX-FAIL", "SFX-CLEAR"]
const SFX_DIR := "res://assets/audio/sfx/"
const MUSIC_PATH := "res://assets/audio/music/MUS-LOOP.ogg"

var plays := {}                   # id -> count, for tests and the S7 check
var placeholder := {}             # id -> true when the code-made placeholder is in use
var music: AudioStreamPlayer
var _sfx := {}


func _ready() -> void:
	for id: String in SFX_IDS:
		var p := AudioStreamPlayer.new()
		p.name = id
		p.bus = &"SFX"
		p.stream = _load(SFX_DIR + id + ".ogg", id)
		add_child(p)
		_sfx[id] = p
		plays[id] = 0
	music = AudioStreamPlayer.new()
	music.name = "MUS-LOOP"
	music.bus = &"Music"
	music.stream = _load(MUSIC_PATH, "MUS-LOOP")
	if music.stream is AudioStreamOggVorbis:
		(music.stream as AudioStreamOggVorbis).loop = true
	add_child(music)
	plays["MUS-LOOP"] = 0


## Main calls this once the level is ready. Music starts from the top on every scene load.
func connect_game(player: Node, wolves: Array) -> void:
	player.cast_fired.connect(func(_o: Vector2, _d: Vector2) -> void: _play("SFX-CAST"))
	player.hurt.connect(func(_hp: int) -> void: _play("SFX-HURT"))
	player.failed.connect(func(_r: String) -> void:
		music.stop()
		_play("SFX-FAIL"))
	player.cleared.connect(func() -> void:
		music.stop()
		_play("SFX-CLEAR"))
	for wolf: Node in wolves:
		wolf.defeated.connect(func() -> void: _play("SFX-WOLF-DOWN"))
	music.play()
	plays["MUS-LOOP"] += 1
	played.emit("MUS-LOOP")


## Pause resumes from the same point (CHANGE-BRIEF music behavior).
func set_paused(on: bool) -> void:
	music.stream_paused = on
	for p: AudioStreamPlayer in _sfx.values():
		p.stream_paused = on


func _play(id: String) -> void:
	_sfx[id].play()
	plays[id] += 1
	played.emit(id)


func _load(path: String, id: String) -> AudioStream:
	if ResourceLoader.exists(path):
		return load(path)
	placeholder[id] = true
	return PlaceholderTones.music_loop() if id == "MUS-LOOP" else PlaceholderTones.for_event(id)
