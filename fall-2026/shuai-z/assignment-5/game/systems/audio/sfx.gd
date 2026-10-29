extends Node
## The one entry point for sound effects (CHANGE-BRIEF.md, event-to-sound map).
## Gameplay calls play(id) right after the code that represents the event has
## changed the game state. Nothing reads a sound back, so a missing or muted
## sound changes nothing.
##
## Each of the six sounds (CHANGE-BRIEF.md revision, six sounds) has its own
## player on the SFX bus, with room for POLYPHONY at once, so two goblins
## stomped on the same tick play two stomps and a new sound never cuts off the
## last one. The players pause with the game. play() also counts plays per ID;
## the checks compare the counts with the events that actually happened.

const STREAMS: Dictionary[StringName, AudioStream] = {
	&"jump": preload("res://systems/audio/sfx/SFX-JUMP.wav"),
	&"stomp": preload("res://systems/audio/sfx/SFX-STOMP.wav"),
	&"hurt": preload("res://systems/audio/sfx/SFX-HURT.wav"),
	&"portal": preload("res://systems/audio/sfx/SFX-PORTAL.wav"),
	&"slash": preload("res://systems/audio/sfx/SFX-SLASH.wav"),
	&"pickup": preload("res://systems/audio/sfx/SFX-PICKUP.wav"),
}
## dB added to each sound, for the mix; set by ear in the playtest. Every file
## peaks at −1 dBFS, and their loudest 100 ms are within 4.3 dB of each other.
const TRIM: Dictionary[StringName, float] = {
	&"jump": 0.0,
	&"stomp": 0.0,
	&"hurt": 0.0,
	&"portal": 0.0,
	&"slash": 0.0,
	&"pickup": 0.0,
}
const BUS := &"SFX"
const POLYPHONY := 4

var counts: Dictionary[StringName, int] = {}

var _players: Dictionary[StringName, AudioStreamPlayer] = {}


func _ready() -> void:
	for id: StringName in STREAMS:
		var player := AudioStreamPlayer.new()
		player.name = String(id)
		player.stream = STREAMS[id]
		player.volume_db = TRIM.get(id, 0.0)
		player.bus = BUS
		player.max_polyphony = POLYPHONY
		add_child(player)
		_players[id] = player


func play(id: StringName) -> void:
	counts[id] = count(id) + 1
	var player: AudioStreamPlayer = _players.get(id)
	if player == null:
		push_warning("Sfx: no sound for %s" % id)
		return
	player.play()


func count(id: StringName) -> int:
	return counts.get(id, 0)


func reset_counts() -> void:
	counts.clear()


## The player for a sound ID, or null; for the checks.
func player(id: StringName) -> AudioStreamPlayer:
	return _players.get(id)


## "jump 2  stomp 1", for the debug line.
func summary() -> String:
	if counts.is_empty():
		return "none yet"
	var parts: PackedStringArray = []
	for id: StringName in counts:
		parts.append("%s %d" % [id, counts[id]])
	return "  ".join(parts)
