extends RefCounted
const Tuning = preload("res://features/tuning.gd")

## Returns [{kind, angle}] to spawn this tick, driven only by the seeded rng.
func step(tick: int, rng: RandomNumberGenerator) -> Array:
	var sec := tick / Tuning.TICK_HZ
	var phase: Dictionary = Tuning.SPAWN_TABLE[-1]
	for p in Tuning.SPAWN_TABLE:
		if sec < int(p["until_s"]):
			phase = p
			break
	if tick % int(phase["interval_ticks"]) != 0:
		return []
	var out := []
	for i in int(phase["batch"]):
		var kind := "wraith" if rng.randf() < float(phase["wraith_chance"]) else "moth"
		out.append({"kind": kind, "angle": rng.randf() * TAU})
	return out
