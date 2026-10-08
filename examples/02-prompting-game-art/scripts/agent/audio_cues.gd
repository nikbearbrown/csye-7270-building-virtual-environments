extends Node
## Observer-only audio manager.  Reads session state and player.jumps; never
## writes game state.  Add as a child of the WalkerJumpman session node.

const _Session = preload("res://game/session.gd")

# Play-call counters — readable by tests.
var jump_plays: int = 0
var fail_plays: int = 0
var music_plays: int = 0

var _session
var _player
var _prev_jumps: int = 0
var _prev_state: int = -1

var _jump_stream: AudioStreamPlayer
var _fail_stream: AudioStreamPlayer
var _music_stream: AudioStreamPlayer

func _ready() -> void:
	_session = get_parent()

	_jump_stream = AudioStreamPlayer.new()
	_jump_stream.stream = load("res://audio/placeholder/jump.wav")
	add_child(_jump_stream)

	_fail_stream = AudioStreamPlayer.new()
	_fail_stream.stream = load("res://audio/placeholder/fail.wav")
	add_child(_fail_stream)

	_music_stream = AudioStreamPlayer.new()
	_music_stream.stream = load("res://audio/placeholder/music_loop.wav")
	add_child(_music_stream)

func _physics_process(_delta: float) -> void:
	# Lazy-bind player: session creates it in its own _ready(), which runs
	# after this node's _ready() when added as a scene child.
	if _player == null:
		_player = _session.get("player")
		if _player == null:
			return

	# One jump cue per increment of player.jumps.
	var cur_jumps: int = _player.jumps
	var delta_j: int = cur_jumps - _prev_jumps
	if delta_j > 0:
		for _i in range(delta_j):
			_jump_stream.play()
			jump_plays += 1
	_prev_jumps = cur_jumps

	# State-change cues.
	var cur_state: int = _session.state
	if cur_state == _prev_state:
		return

	match cur_state:
		_Session.State.PLAYING:
			if _music_stream.stream_paused:
				_music_stream.stream_paused = false
			elif not _music_stream.playing:
				_music_stream.play()
				music_plays += 1
		_Session.State.PAUSED:
			_music_stream.stream_paused = true
		_Session.State.DYING:
			_fail_stream.play()
			fail_plays += 1
		_Session.State.COMPLETE:
			_music_stream.stop()

	_prev_state = cur_state
