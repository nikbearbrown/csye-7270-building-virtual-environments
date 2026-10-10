extends RefCounted
## Pure throttle for sound events: per-id cooldown, voice cap and once-per-run.
## Uses the simulation clock supplied by the caller, never wall time.

var rules: Dictionary
var _last_ms := {}
var _fired := {}

func _init(r: Dictionary) -> void:
	rules = r

func request(id: String, now_ms: int, active_voices: int) -> bool:
	var r: Dictionary = rules.get(id, {})
	var once: bool = r.get("once", false)
	if once and _fired.get(id, false):
		return false
	if _last_ms.has(id) and now_ms - int(_last_ms[id]) < int(r.get("cooldown_ms", 0)):
		return false
	if active_voices >= int(r.get("max_voices", 1)):
		return false
	_last_ms[id] = now_ms
	if once:
		_fired[id] = true
	return true

func reset() -> void:
	_last_ms.clear()
	_fired.clear()
