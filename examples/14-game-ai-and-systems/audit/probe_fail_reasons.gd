extends SceneTree
## Chapter-author probe: why do Lab B levels fail? Counts first-failure reasons.
func _initialize() -> void:
	var gen = load("res://pcg/level_generator.gd").new()
	var val = load("res://pcg/level_validator.gd").new()
	var counts := {"gap": 0, "step": 0, "no landing": 0, "other": 0}
	for s in range(1, 201):
		var r: Dictionary = val.validate(gen.generate(s, 40))
		if r.is_empty():
			continue
		var reason: String = r["reason"]
		if reason.contains("no landing"): counts["no landing"] += 1
		elif reason.contains("gap"): counts["gap"] += 1
		elif reason.contains("step"): counts["step"] += 1
		else: counts["other"] += 1
	print("FAIL_REASONS ", counts)
	quit()
