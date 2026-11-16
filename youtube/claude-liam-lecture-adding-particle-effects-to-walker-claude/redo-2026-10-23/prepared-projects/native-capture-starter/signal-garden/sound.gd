extends Node3D
# Temporary authored test tones, not Bear's future Assignment 2 assets.
var enabled := true
var counts := {"step": 0, "charge": 0, "gate": 0, "finish": 0, "reset": 0}
var players := {}
var ambience: AudioStreamPlayer
static func tone(frequency: float, duration: float, loop: bool = false) -> AudioStreamWAV:
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_16_BITS
	stream.mix_rate = 22050
	var size := int(duration * 22050)
	var bytes := PackedByteArray()
	bytes.resize(size * 2)
	for i in range(size):
		var t := float(i) / 22050.0
		var envelope := 0.25 if loop else minf(t / 0.01, 1.0) * minf((duration - t) / 0.04, 1.0)
		var sample := int(sin(TAU * frequency * t) * envelope * 11000.0)
		bytes.encode_s16(i * 2, sample)
	stream.data = bytes
	if loop:
		stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
		stream.loop_begin = 0
		stream.loop_end = size
	return stream
func _ready() -> void:
	process_mode = Node.PROCESS_MODE_PAUSABLE
	for bus in ["GardenSFX", "GardenAmbience"]:
		if AudioServer.get_bus_index(bus) < 0:
			AudioServer.add_bus()
			var index := AudioServer.bus_count - 1
			AudioServer.set_bus_name(index, bus)
			AudioServer.set_bus_send(index, "Master")
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("GardenSFX"), -6.0)
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("GardenAmbience"), -20.0)
	for pair in [["step", 180.0, 0.07], ["charge", 330.0, 0.6], ["gate", 520.0, 0.3], ["finish", 660.0, 0.5], ["reset", 220.0, 0.15]]:
		var p := AudioStreamPlayer3D.new()
		p.name = pair[0]
		p.bus = "GardenSFX"
		p.stream = tone(pair[1], pair[2])
		p.max_polyphony = 2 if pair[0] == "step" else 1
		p.unit_size = 10.0
		p.max_distance = 40.0
		add_child(p)
		players[pair[0]] = p
	ambience = AudioStreamPlayer.new()
	ambience.name = "Ambience"
	ambience.bus = "GardenAmbience"
	ambience.stream = tone(110.0, 2.0, true)
	ambience.max_polyphony = 1
	add_child(ambience)
func play_event(event: String, at: Vector3) -> void:
	counts[event] += 1
	if enabled:
		players[event].position = at
		players[event].play()
func start_ambience() -> void:
	if enabled: ambience.play()
func stop_all() -> void:
	for p in players.values(): p.stop()
	ambience.stop()
