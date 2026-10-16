extends Node
## Listens to session signals and plays sound. Never writes game state.

const SfxGate = preload("res://audio/sfx_gate.gd")
const GameState = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")

const SFX_PATHS := {
	"kill": "res://assets/sfx/sfx_01_kill.wav",
	"pickup": "res://assets/sfx/sfx_02_pickup.wav",
	"hurt": "res://assets/sfx/sfx_03_hurt.wav",
	"levelup": "res://assets/sfx/sfx_04_levelup.wav",
	"evolve": "res://assets/sfx/sfx_05_evolve.wav",
	"lose": "res://assets/sfx/sfx_06a_lose.wav",
	"win": "res://assets/sfx/sfx_06b_win.wav",
}
const MUSIC_BASE := "res://assets/music/mus_01_night_market.ogg"
const MUSIC_LAYER := "res://assets/music/mus_02_sunflare_layer.ogg"
const RULES := {
	"kill": {"cooldown_ms": 60, "max_voices": 3},
	"pickup": {"cooldown_ms": 80, "max_voices": 1},
	"hurt": {"cooldown_ms": 800, "max_voices": 1},
	"levelup": {"cooldown_ms": 0, "max_voices": 8},
	"evolve": {"once": true, "max_voices": 1},
	"lose": {"max_voices": 1},
	"win": {"max_voices": 1},
}
const VOICE_MS := 300
const PAUSE_DB := -10.0
const LEVELUP_DB := -6.0
const SILENT_DB := -80.0
const LOWPASS_HZ := 900.0

var gate = SfxGate.new(RULES)
var play_log: Array[Dictionary] = []
var disable_streams := false
var music_state := "stopped"
var session
var streams := {}
var pools := {}
var voice_end_ms := {}
var base: AudioStreamPlayer
var layer: AudioStreamPlayer
var _fade: Tween
var _layer_fade: Tween

func setup(s) -> void:
	session = s
	process_mode = Node.PROCESS_MODE_ALWAYS
	_ensure_buses()
	for id in SFX_PATHS:
		if ResourceLoader.exists(SFX_PATHS[id]):
			streams[id] = load(SFX_PATHS[id])
		var pool: Array = []
		for i in int(RULES[id].get("max_voices", 1)):
			var p := AudioStreamPlayer.new()
			p.bus = "SFX"
			add_child(p)
			pool.append(p)
		pools[id] = pool
	base = _music_player(MUSIC_BASE)
	layer = _music_player(MUSIC_LAYER)
	s.enemy_killed.connect(func(_p): sfx("kill"))
	s.gem_collected.connect(func(_v): sfx("pickup"))
	s.player_hurt.connect(func(_h): sfx("hurt"))
	s.evolved.connect(_on_evolved)
	s.run_started.connect(_on_run_started)
	s.state.changed.connect(_on_state_changed)

func _music_player(path: String) -> AudioStreamPlayer:
	var p := AudioStreamPlayer.new()
	p.bus = "Music"
	if ResourceLoader.exists(path):
		var st = load(path)
		if st is AudioStreamOggVorbis:
			st.loop = true
		p.stream = st
	add_child(p)
	return p

func now_ms() -> int:
	return int(session.tick_count * 1000.0 / Tuning.TICK_HZ)

func sfx(id: String) -> bool:
	var now := now_ms()
	var ends: Array = voice_end_ms.get(id, []).filter(func(t): return t > now)
	voice_end_ms[id] = ends
	if not gate.request(id, now, ends.size()):
		return false
	ends.append(now + VOICE_MS)
	play_log.append({"id": id, "ms": now, "tick": session.tick_count})
	var stream: AudioStream = null if disable_streams else streams.get(id)
	if stream:
		var pool: Array = pools[id]
		var player: AudioStreamPlayer = pool[0]
		for p in pool:
			if not p.playing:
				player = p
				break
		player.stream = stream
		player.pitch_scale = randf_range(0.95, 1.05) if id == "kill" else 1.0
		player.play()
	return true

func _on_run_started() -> void:
	_kill_tweens()
	# a fresh run starts clean: the previous run's lose/win stinger must not ring on into it
	for id in ["lose", "win"]:
		for p in pools[id]:
			p.stop()
	gate.reset()
	voice_end_ms.clear()
	_set_lowpass(false)
	_set_music_db(0.0)
	base.stop()
	layer.stop()
	base.volume_db = 0.0
	layer.volume_db = SILENT_DB
	if not disable_streams:
		if base.stream:
			base.play(0.0)
		if layer.stream:
			layer.play(0.0)
	music_state = "playing"

func _on_state_changed(from: int, to: int) -> void:
	match to:
		GameState.PAUSED:
			_set_lowpass(true)
			_set_music_db(PAUSE_DB)
			music_state = "paused"
		GameState.LEVELUP:
			# SFX-04 marks the card screen the player sees, not the XP threshold: several levels from one pickup
			# open one card screen each, one chime each, and a level gained on the final tick (no card) is silent.
			sfx("levelup")
			_set_music_db(LEVELUP_DB)
			music_state = "ducked"
		GameState.PLAYING:
			if from == GameState.PAUSED or from == GameState.LEVELUP:
				_set_lowpass(false)
				_set_music_db(0.0)
				music_state = "playing"
		GameState.LOST:
			_fade_out(0.5)
			sfx("lose")
		GameState.WON:
			_fade_out(1.0)
			sfx("win")

func _on_evolved() -> void:
	sfx("evolve")
	if _layer_fade:
		_layer_fade.kill()
	_layer_fade = create_tween()
	_layer_fade.tween_property(layer, "volume_db", 0.0, 2.0)

func _fade_out(seconds: float) -> void:
	_kill_tweens()
	music_state = "fading"
	_fade = create_tween().set_parallel(true)
	_fade.tween_property(base, "volume_db", SILENT_DB, seconds)
	_fade.tween_property(layer, "volume_db", SILENT_DB, seconds)
	_fade.chain().tween_callback(_stop_music)

func _stop_music() -> void:
	base.stop()
	layer.stop()
	music_state = "stopped"

func _kill_tweens() -> void:
	if _fade:
		_fade.kill()
		_fade = null
	if _layer_fade:
		_layer_fade.kill()
		_layer_fade = null

func _ensure_buses() -> void:
	for bus_name in ["Music", "SFX"]:
		if AudioServer.get_bus_index(bus_name) == -1:
			AudioServer.add_bus()
			var i := AudioServer.bus_count - 1
			AudioServer.set_bus_name(i, bus_name)
			AudioServer.set_bus_send(i, "Master")
	var mi := AudioServer.get_bus_index("Music")
	if AudioServer.get_bus_effect_count(mi) == 0:
		var lp := AudioEffectLowPassFilter.new()
		lp.cutoff_hz = LOWPASS_HZ
		AudioServer.add_bus_effect(mi, lp)
	AudioServer.set_bus_effect_enabled(mi, 0, false)

func _set_lowpass(on: bool) -> void:
	AudioServer.set_bus_effect_enabled(AudioServer.get_bus_index("Music"), 0, on)

func _set_music_db(db: float) -> void:
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Music"), db)

func toggle_bus(bus_name: String) -> void:
	var i := AudioServer.get_bus_index(bus_name)
	AudioServer.set_bus_mute(i, not AudioServer.is_bus_mute(i))

func is_bus_muted(bus_name: String) -> bool:
	return AudioServer.is_bus_mute(AudioServer.get_bus_index(bus_name))
