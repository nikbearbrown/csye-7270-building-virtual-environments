extends SceneTree
## Assignment 6 headless CPU price of the two effects (CHANGE-BRIEF "Price predictions and budget"). Not a pass/fail
## test: it prints one JSON line per measurement and a summary, and exits 0 unless the load was not what it claims.
## From fall-2026/zhefan-z/assignment-6/:
##   ./scripts/run-test.sh cost_effects.gd 60 300
## Cases, each in its own fresh scene:
##   control  - an empty scene: only this script's measuring loop and the engine's idle frame;
##   off      - the game scene (game/main.tscn), no effect;
##   a6       - the game scene plus Effect A at its bound, 6 impacts alive (previews/effect_load.gd, mode A);
##   b_heavy  - the game scene plus Effect B at its heaviest: 6 flying full trails, about 6 detached fading trails
##              and 6 refilling ones (an upper bound; previews/effect_load.gd, mode B);
##   a6_dry, b_dry - the same driver with bare Node2D placeholders instead of the effects: a6 - a6_dry and
##              b_heavy - b_dry are the effects' own price, without the driver's.
## Method: --fixed-fps gives every frame the same delta and lets frames run as fast as the CPU does, so the wall time
## between two process frames is the main thread's CPU time for one frame. The clock starts right before each await and
## stops right after it; this script's own bookkeeping (monitors, load counts) runs outside that window. Each case warms up for WARMUP frames (the
## load reaches its steady state, caches fill), then MEASURE frames are timed. The cases run in ROUNDS rounds in a
## rotating order, so slow drift (clock boost, heat) does not land on one case. Reported per case: mean, standard
## deviation, median, 5th and 95th percentile of the per-frame wall time, the engine's own process and physics times
## (Performance monitors), and the round means; for the driven cases also split into frames in which the driver created
## an instance (instantiate cost, as explode() pays) and the rest (the live effect's steady price). Headless runs a dummy renderer: no GPU particle process, nothing drawn,
## so a GPU effect's price here is only its nodes' CPU work.

const MAIN := "res://game/main.tscn"
const LOAD := preload("res://previews/effect_load.gd")
const CASES := ["control", "off", "a6_dry", "a6", "b_dry", "b_heavy"]
const ROUNDS := 3
const WARMUP := 180      # 3 s of game time at 60 fps: A is at 6 after 0.75 s, B is full after 0.3 s
const MEASURE := 1200    # 20 s of game time at 60 fps, per case per round
const PLAYER_X := 200.0
const GROUND_TOP := 327.0

var samples := {}        # case -> Array of per-frame wall us
var process_us := {}     # case -> Array of Performance.TIME_PROCESS in us
var physics_us := {}     # case -> Array of Performance.TIME_PHYSICS_PROCESS in us
var round_means := {}    # case -> Array of per-round mean wall us
var spawn_frames := {}   # case -> Array of wall us of frames in which an instance was created
var steady_frames := {}  # case -> Array of wall us of the other frames
var loads := {}          # case -> {key: [min, max]} of the load counts while measuring
var load_ok := true


func _initialize() -> void:
	call_deferred("run")


func emit(d: Dictionary) -> void:
	print(JSON.stringify(d))


func stats(a: Array) -> Dictionary:
	var s := a.duplicate()
	s.sort()
	var n := s.size()
	var total := 0.0
	for v: float in s:
		total += v
	var mean := total / n
	var sq := 0.0
	for v: float in s:
		sq += (v - mean) * (v - mean)
	var sd := sqrt(sq / maxi(n - 1, 1))
	return {"n": n, "mean": snappedf(mean, 0.01), "sd": snappedf(sd, 0.01), "median": snappedf(s[n / 2], 0.01),
		"p5": snappedf(s[int(n * 0.05)], 0.01), "p95": snappedf(s[int(n * 0.95)], 0.01),
		"se": snappedf(sd / sqrt(n), 0.001)}


func setup(case: String) -> Dictionary:
	if case == "control":
		var empty := Node2D.new()
		root.add_child(empty)
		return {"scene": empty, "load": null}
	var main: Node = load(MAIN).instantiate()
	main.test_mode = true
	root.add_child(main)
	main.player.global_position = Vector2(PLAYER_X, GROUND_TOP)
	var fx: Node = null
	if case != "off":
		fx = LOAD.new()
		fx.target = main
		main.add_child(fx)
		fx.dry = case.ends_with("_dry")
		fx.set_mode(LOAD.Mode.A if case.begins_with("a6") else LOAD.Mode.B)
	return {"scene": main, "load": fx}


func run() -> void:
	for c: String in CASES:
		samples[c] = []
		process_us[c] = []
		physics_us[c] = []
		round_means[c] = []
		spawn_frames[c] = []
		steady_frames[c] = []
		loads[c] = {}
	emit({"cost": "setup", "rounds": ROUNDS, "warmup_frames": WARMUP, "measured_frames_per_round": MEASURE,
		"physics_ticks_per_second": Engine.physics_ticks_per_second, "renderer": RenderingServer.get_video_adapter_name()})

	for r in ROUNDS:
		for k in CASES.size():
			var case: String = CASES[(k + r) % CASES.size()]
			var s := setup(case)
			for i in WARMUP:
				await process_frame
			var wall := []
			for i in MEASURE:
				var sp0: int = s.load.spawns if s.load else 0
				var t0 := Time.get_ticks_usec()
				await process_frame
				var us := float(Time.get_ticks_usec() - t0)
				wall.append(us)
				if s.load:
					(spawn_frames[case] if s.load.spawns != sp0 else steady_frames[case]).append(us)
				process_us[case].append(Performance.get_monitor(Performance.TIME_PROCESS) * 1e6)
				physics_us[case].append(Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS) * 1e6)
				if s.load:
					var cnt: Dictionary = s.load.counts()
					for key: String in cnt:
						var mm: Array = loads[case].get(key, [cnt[key], cnt[key]])
						loads[case][key] = [mini(mm[0], cnt[key]), maxi(mm[1], cnt[key])]
			samples[case].append_array(wall)
			var st := stats(wall)
			round_means[case].append(st.mean)
			emit({"cost": "round", "round": r + 1, "case": case, "wall_us_per_frame": st,
				"nodes_in_tree": root.get_tree().get_node_count()})
			(s.scene as Node).queue_free()
			for i in 5:
				await process_frame

	# The load must be what the case says, or the comparison means nothing.
	var checks := {}
	for c: String in ["a6", "a6_dry"]:
		var l: Dictionary = loads[c]
		checks[c] = l.get("impacts", [0, 0])[1] == 6 and l.impacts[0] >= 5
	for c: String in ["b_heavy", "b_dry"]:
		var l: Dictionary = loads[c]
		checks[c] = l.get("flying_trails", [0, 0])[0] == 6 and l.get("detached_trails", [0, 0])[1] >= 6 \
			and l.detached_trails[0] >= 5
	load_ok = checks.values().all(func(v: bool) -> bool: return v)
	emit({"cost": "load-check", "loads": loads, "ok": checks})

	var summary := {}
	for c: String in CASES:
		summary[c] = {"wall_us_per_frame": stats(samples[c]), "engine_process_us": stats(process_us[c]),
			"engine_physics_us": stats(physics_us[c]), "round_means_us": round_means[c]}
		if not spawn_frames[c].is_empty():
			summary[c]["spawn_frames_us"] = stats(spawn_frames[c])
			summary[c]["steady_frames_us"] = stats(steady_frames[c])
		emit({"cost": "case", "case": c, "summary": summary[c]})

	# Differences against the right reference, with two yardsticks: 2 standard errors of the difference (frame noise)
	# and the round-to-round spread of the means (drift between rounds), whichever is larger.
	for pair: Array in [["off", "control"], ["a6_dry", "off"], ["a6", "a6_dry"], ["a6", "off"], ["b_dry", "off"],
			["b_heavy", "b_dry"], ["b_heavy", "off"]]:
		var x: Dictionary = summary[pair[0]].wall_us_per_frame
		var y: Dictionary = summary[pair[1]].wall_us_per_frame
		var diff: float = x.mean - y.mean
		var se := sqrt(x.se * x.se + y.se * y.se)
		var spread: float = maxf(range_of(round_means[pair[0]]), range_of(round_means[pair[1]]))
		var bar := maxf(2.0 * se, spread)
		var row := {"cost": "difference", "case": pair[0], "minus": pair[1], "diff_us": snappedf(diff, 0.01),
			"two_se_us": snappedf(2.0 * se, 0.01), "round_spread_us": snappedf(spread, 0.01),
			"distinguishable": absf(diff) > bar}
		if summary[pair[0]].has("steady_frames_us") and summary[pair[1]].has("steady_frames_us"):
			row["steady_diff_us"] = snappedf(summary[pair[0]].steady_frames_us.mean - summary[pair[1]].steady_frames_us.mean, 0.01)
			row["spawn_diff_us"] = snappedf(summary[pair[0]].spawn_frames_us.mean - summary[pair[1]].spawn_frames_us.mean, 0.01)
		emit(row)
	# The engine's own monitors cannot be a per-frame CPU time if they exceed the wall time of the whole frame, or if two
	# different cases report the same distribution.
	var monitor_bad := []
	for c: String in CASES:
		if summary[c].engine_process_us.mean > summary[c].wall_us_per_frame.mean:
			monitor_bad.append(c)
	var same_pairs := []
	for i in CASES.size():
		for j in range(i + 1, CASES.size()):
			var x: Dictionary = summary[CASES[i]].engine_process_us
			var y: Dictionary = summary[CASES[j]].engine_process_us
			if x.median == y.median and x.p5 == y.p5 and x.p95 == y.p95:
				same_pairs.append([CASES[i], CASES[j]])
	if not monitor_bad.is_empty() or not same_pairs.is_empty():
		emit({"cost": "warning", "text": "Performance TIME_PROCESS / TIME_PHYSICS_PROCESS are not this frame's CPU time here "
			+ "(above the frame's wall time, or identical for different cases); use wall_us_per_frame",
			"monitor_above_wall_time": monitor_bad, "identical_monitor_distributions": same_pairs})
	var c_off: float = summary.off.wall_us_per_frame.mean - summary.control.wall_us_per_frame.mean
	if absf(c_off) <= maxf(range_of(round_means.off), range_of(round_means.control)):
		emit({"cost": "warning", "text": "control and off report the same value: the script may be measuring itself"})

	print("COST EFFECTS: %d cases x %d rounds x %d frames; load %s" % [CASES.size(), ROUNDS, MEASURE,
		"as claimed" if load_ok else "NOT as claimed"])
	quit(0 if load_ok else 1)


func range_of(a: Array) -> float:
	return (a.max() - a.min()) if a.size() > 0 else 0.0
