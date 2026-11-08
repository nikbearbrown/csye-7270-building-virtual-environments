extends Node
## The Level 1 theme (MUS-LOOP) on the Music bus, and how loud it plays as the
## game goes (CHANGE-BRIEF.md, music behavior). It is an autoload, so a level
## that reloads does not cut it off, and it keeps processing while the game is
## paused, so it plays on under the pause.
##
## The level starts it on the title; Enter, a death and a start-over from the
## opening never restart it. The level asks for dips by name: the pause
## (PAUSE_DIP, until it ends), a hit (HURT_DIP for HURT_TIME, under SFX-HURT)
## and a death (DEATH_DIP, through the fade and the respawn). The music plays
## at the deepest dip in force, so dips never add up: a hit that takes his last
## heart dips 9 dB, not 15. Each change ramps over RAMP_TIME, so it never
## clicks. On the teleport circle it fades out over FADE_OUT_TIME and stops;
## the end card is silent, and playing again starts it from the top.
##
## Nothing in the game reads the music back. `starts` counts the starts from
## the top, for the checks: a headless run's audio driver never moves the
## playback position on.

const LOOP := preload("res://systems/audio/music/MUS-LOOP.ogg")
const BUS := &"Music"
const PAUSE_DIP := -12.0 ## dB
const HURT_DIP := -6.0 ## dB...
const HURT_TIME := 0.6 ## ...for this many s
const DEATH_DIP := -9.0 ## dB
const RAMP_TIME := 0.15 ## s for every change of level
const FADE_OUT_TIME := 1.5 ## s
const SILENCE := -60.0 ## dB at the end of the fade, where it stops

var starts := 0

var _dips: Dictionary[StringName, float] = {} ## dB for each reason in force
var _dip_left: Dictionary[StringName, float] = {} ## s left of each timed dip
var _fading_out := false
var _player := AudioStreamPlayer.new()
var _tween: Tween


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_player.name = "Loop"
	_player.stream = LOOP
	_player.bus = BUS
	add_child(_player)


## Plays the theme from the top at full level. If it is already playing, it
## keeps its place, and any dips end.
func start() -> void:
	_dips.clear()
	_dip_left.clear()
	if is_playing():
		_ramp()
		return
	_fading_out = false
	_kill_tween()
	_player.volume_db = 0.0
	_player.play()
	starts += 1


## Dips the music `db` (below 0) for `reason`, until end_dip(reason), or for
## `seconds` if given. The same reason again replaces its dip.
func dip(reason: StringName, db: float, seconds := INF) -> void:
	_dips[reason] = db
	if is_finite(seconds):
		_dip_left[reason] = seconds
	else:
		_dip_left.erase(reason)
	_ramp()


func end_dip(reason: StringName) -> void:
	_dips.erase(reason)
	_dip_left.erase(reason)
	_ramp()


## Fades out over FADE_OUT_TIME, then stops.
func fade_out() -> void:
	_dips.clear()
	_dip_left.clear()
	_fading_out = true
	_kill_tween()
	_tween = create_tween()
	_tween.tween_property(_player, "volume_db", SILENCE, FADE_OUT_TIME)
	_tween.tween_callback(_player.stop)


## Playing, and not fading out.
func is_playing() -> bool:
	return _player.playing and not _fading_out


## The level it is heading for, in dB: the deepest dip in force, or SILENCE
## while it fades out.
func target_db() -> float:
	if _fading_out:
		return SILENCE
	var level := 0.0
	for db: float in _dips.values():
		level = minf(level, db)
	return level


## The level it plays at now, in dB.
func volume_db() -> float:
	return _player.volume_db


## The player, for the checks and the capture.
func player() -> AudioStreamPlayer:
	return _player


func _process(delta: float) -> void:
	for reason: StringName in _dip_left.keys():
		_dip_left[reason] -= delta
		if _dip_left[reason] <= 0.0:
			end_dip(reason)


func _ramp() -> void:
	if _fading_out:
		return
	_kill_tween()
	_tween = create_tween()
	_tween.tween_property(_player, "volume_db", target_db(), RAMP_TIME)


func _kill_tween() -> void:
	if _tween:
		_tween.kill()
