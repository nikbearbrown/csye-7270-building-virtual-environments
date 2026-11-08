extends SceneTree
## Headless CPU price of the two A6 particle effects (CHANGE-BRIEF.md "Price
## predictions and budget"; Predicted failure F8). Adapted from Chapter 9's
## build/example09/particle_cost.gd, whose recorded mistake was that it timed
## the engine's own frame sleep (6.90 ms for every case, an empty scene included)
## because headless Godot without --fixed-fps sleeps low_processor_usage_mode_sleep_usec
## per frame. This script therefore:
##   - prints the sleep settings and the command line, and expects --fixed-fps;
##   - reports the wall clock between consecutive process_frame signals (one
##     whole main-loop iteration: physics, process, the dummy RenderingServer
##     sync, and any sleep), checks one engine frame and one physics tick passed
##     per sample, and warns if the empty scene's frame is near the sleep or reads
##     like the game scene. Performance TIME_PROCESS / TIME_PHYSICS_PROCESS were
##     tried as a cross-check and are not per-frame here (their sum exceeded the
##     wall frame), so they are printed for reference only;
##   - keeps an empty-scene control (a bare Node) and a game-scene control
##     (both effects off), and interleaves the game cases round by round so slow
##     drift in the live floor (enemies, threat) lands on every case alike.
## Cases:
##   empty      a bare Node under root, no game
##   game_off   res://game/main.tscn on a real Sami floor (fixed seed), no HitSpark,
##              every FirePit unlit (burn_left 0)
##   A_8        8 HitSpark instances alive at once under the GameManager. Each frees
##              itself after 0.55 s (33 frames at 60 fps); the fixture re-instances
##              res://effects/hit_spark.tscn on the frame after one is freed, staggered
##              one every 4 frames during warm-up, so 8 are alive through the window.
##              The price therefore includes ~8/33 instantiations a frame.
##   B_1        one FirePit fed to FIRE_MAX through feed() (ratio 1.0), others unlit
##   B_all      every FirePit on the floor fed to FIRE_MAX (the brief prices four)
## Run: ./scripts/run-test.sh cost_effects.gd 60 300

const SPARK_SCENE := preload("res://effects/hit_spark.tscn")
const SEED := 2026
const WARM_UP_FRAMES := 60
const TIMED_FRAMES := 300
const REPEATS := 5
const SPARKS := 8
const SPARK_STAGGER := 4
const FULL_FIRE := 120.0

var game: GameManager
var rig: Node
var sparks: Array[Node] = []
var spark_spawns := 0
var spark_alive_min := 0
var spark_alive_max := 0
## case -> Array of per-repeat Dictionaries {wall, proc, phys, nodes, wall_sd}
var results: Dictionary = {}
var notes: Dictionary = {}
var bad := false

func _initialize() -> void: call_deferred("run")

func step(n: int = 1) -> void:
	for i in range(n):
		await physics_frame
		await process_frame

func find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := find_game(child)
		if found != null: return found
	return null

static func mean(a: Array) -> float:
	var t := 0.0
	for v in a: t += v
	return t / maxf(1.0, a.size())

static func stdev(a: Array) -> float:
	if a.size() < 2: return 0.0
	var m := mean(a)
	var t := 0.0
	for v in a: t += (v - m) * (v - m)
	return sqrt(t / (a.size() - 1))

func live_sparks() -> Array[Node]:
	var out: Array[Node] = []
	for s in sparks:
		if is_instance_valid(s) and not s.is_queued_for_deletion(): out.append(s)
	return out

## Fixture for case A: bring the live HitSpark count up to `target`.
func top_up(target: int, counting: bool) -> void:
	sparks = live_sparks()
	if counting:
		spark_alive_min = mini(spark_alive_min, sparks.size())
		spark_alive_max = maxi(spark_alive_max, sparks.size())
	var k := sparks.size()
	while sparks.size() < target:
		var s: Node3D = SPARK_SCENE.instantiate()
		var a := TAU * float(k) / SPARKS
		game.add_child(s)
		s.global_position = game.player.global_position + Vector3(cos(a) * 1.5, 0.8, sin(a) * 1.5)
		sparks.append(s)
		k += 1
		if counting: spark_spawns += 1

func clear_sparks() -> void:
	for s in sparks:
		if is_instance_valid(s): s.queue_free()
	sparks.clear()

func keep_safe() -> void:
	if is_instance_valid(game) and is_instance_valid(game.player): game.player.hp = game.player.max_hp

func pits() -> Array:
	return game.fires.filter(func(f): return is_instance_valid(f)) if is_instance_valid(game) else []

## Measurement setup only: light `lit_count` pits through feed(), put the rest out through burn().
func set_pits(lit_count: int) -> void:
	var list := pits()
	for i in list.size():
		var pit: FirePit = list[i]
		if i < lit_count: pit.feed(FeatureCatalog.FIRE_MAX)
		elif pit.burn_left > 0.0: pit.burn(pit.burn_left)

func stray_sparks() -> int:
	if not is_instance_valid(game): return 0
	return game.find_children("*", "Node3D", false, false).filter(
		func(n): return n.scene_file_path == "res://effects/hit_spark.tscn" and not sparks.has(n)).size()

## One warm-up + timed window. The per-frame loop is the same code for every
## case; only `spark_target` differs (0 outside case A).
func window(spark_target: int) -> Dictionary:
	var wall: Array[float] = []
	var proc: Array[float] = []
	var phys: Array[float] = []
	var nodes: Array[float] = []
	spark_spawns = 0
	spark_alive_min = 1 << 20
	spark_alive_max = 0
	var f0 := Engine.get_process_frames()
	var p0 := Engine.get_physics_frames()
	var tf0 := 0
	var tp0 := 0
	var prev := Time.get_ticks_usec()
	for i in range(WARM_UP_FRAMES + TIMED_FRAMES):
		await process_frame
		var now := Time.get_ticks_usec()
		var timed := i >= WARM_UP_FRAMES
		if i == WARM_UP_FRAMES:
			tf0 = Engine.get_process_frames() - 1
			tp0 = Engine.get_physics_frames()
		if timed:
			wall.append((now - prev) / 1000.0)
			proc.append(Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0)
			phys.append(Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS) * 1000.0)
			nodes.append(Performance.get_monitor(Performance.OBJECT_NODE_COUNT))
		if spark_target > 0:
			top_up(mini(spark_target, 1 + i / SPARK_STAGGER), timed)
		keep_safe()
		prev = Time.get_ticks_usec()
	# prev is re-read after the fixture work, so each wall sample is the engine's
	# frame plus nothing of ours but the await/resume; the fixture's own spawning
	# (case A) lands in the engine's frame through add_child/_ready, as in play.
	var engine_frames := Engine.get_process_frames() - tf0
	var physics_ticks := Engine.get_physics_frames() - tp0
	if engine_frames != TIMED_FRAMES:
		print("  WARNING: %d engine frames passed in a %d-sample window" % [engine_frames, TIMED_FRAMES])
		bad = true
	return {"frames": engine_frames, "ticks": physics_ticks, "warm_frames": tf0 - f0, "warm_ticks": tp0 - p0,
		"wall": mean(wall), "wall_sd": stdev(wall), "wall_min": wall.min(), "wall_max": wall.max(),
		"proc": mean(proc), "phys": mean(phys), "nodes": mean(nodes),
		"spawns": spark_spawns, "alive_min": spark_alive_min if spark_target > 0 else 0, "alive_max": spark_alive_max}

func record(case_name: String, r: Dictionary) -> void:
	if not results.has(case_name): results[case_name] = []
	results[case_name].append(r)
	print("  %-9s wall %.4f ms (frame sd %.4f, min %.4f, max %.4f)  frames %d/ticks %d (warm-up %d/%d)  mon process %.3f physics %.3f  nodes %.0f%s" % [
		case_name, r.wall, r.wall_sd, r.wall_min, r.wall_max, r.frames, r.ticks, r.warm_frames, r.warm_ticks, r.proc, r.phys, r.nodes,
		("  sparks alive %d-%d, spawned %d in window" % [r.alive_min, r.alive_max, r.spawns]) if case_name == "A_8" else ""])

func run_case(case_name: String) -> void:
	var lit := 0
	var target := 0
	match case_name:
		"A_8": target = SPARKS
		"B_1": lit = 1
		"B_all": lit = pits().size()
	clear_sparks()
	set_pits(lit)
	var r := await window(target)
	var burn := pits().map(func(p): return p.burn_left)
	var lit_now := pits().filter(func(p): return p.lit()).size()
	var lit_min_burn: float = 1e9
	for p in pits():
		if p.lit(): lit_min_burn = minf(lit_min_burn, p.burn_left)
	if lit_now != lit or (lit > 0 and lit_min_burn < FULL_FIRE):
		print("  WARNING %s: %d pits lit (wanted %d), lowest burn_left %.1f" % [case_name, lit_now, lit, lit_min_burn])
		bad = true
	if stray_sparks() > 0:
		print("  WARNING %s: %d HitSpark nodes the fixture did not make" % [case_name, stray_sparks()])
	if case_name == "A_8" and r.alive_min < SPARKS - 1:
		print("  WARNING A_8: only %d sparks alive at some frame" % r.alive_min)
		bad = true
	notes[case_name] = "burn_left %s" % str(burn.map(func(b): return snappedf(b, 0.1)))
	record(case_name, r)

func summary(case_name: String) -> Dictionary:
	var reps: Array = results[case_name]
	var walls := reps.map(func(r): return r.wall)
	return {"wall": mean(walls), "wall_sd": stdev(walls), "wall_min": walls.min(), "wall_max": walls.max(),
		"frame_sd": mean(reps.map(func(r): return r.wall_sd)),
		"nodes": mean(reps.map(func(r): return r.nodes))}

func run() -> void:
	var args := OS.get_cmdline_args()
	print("Rendering method: %s  adapter: '%s'  display: %s" % [RenderingServer.get_current_rendering_method(), RenderingServer.get_video_adapter_name(), DisplayServer.get_name()])
	# OS.get_cmdline_args() does not list engine options such as --fixed-fps
	# (first run: it printed only --script), so the sleep is checked from the
	# empty scene's frame time below, not from the command line.
	print("user cmdline args: %s" % " ".join(args))
	print("low_processor_usage_mode %s  sleep %d usec  max_fps %d  physics_ticks %d  window can draw %s" % [
		OS.low_processor_usage_mode, OS.low_processor_usage_mode_sleep_usec, Engine.max_fps,
		Engine.physics_ticks_per_second, DisplayServer.window_can_draw()])
	print("Performance TIME_PROCESS / TIME_PHYSICS_PROCESS are not per-frame values here (first run: their sum 13.8 ms exceeded the 7.9 ms wall frame, and physics read a constant 6.373 ms in the empty scene); they are printed as 'mon' for reference only, and the wall clock is the reported number")
	print("frames: warm-up %d + timed %d per window, %d repeats per case; game cases interleaved, order rotated each round" % [WARM_UP_FRAMES, TIMED_FRAMES, REPEATS])

	# --- empty control ---
	print("ROUND empty")
	for rep in REPEATS:
		var bare := Node.new()
		root.add_child(bare)
		record("empty", await window(0))
		bare.queue_free()
		await step(2)

	# --- the game ---
	rig = load("res://game/main.tscn").instantiate()
	rig.persist_sessions = false
	root.add_child(rig)
	await step(10)
	game = find_game(rig)
	game.fixed_map_seed = SEED
	game.seed_rng(SEED)
	await game.start_contract("snow")
	await step(30)
	var n_pits := pits().size()
	print("FLOOR region %s floor %d fire pits %d enemies %d simulation_active %s" % [
		game.region_id, game.floor_number, n_pits, game.floor_enemies().size(), game.simulation_active()])
	if game.region_id != "snow" or n_pits < 1 or not game.simulation_active():
		print("FAIL no live Sami floor with fire pits")
		quit(1)
		return
	var order := ["game_off", "A_8", "B_1", "B_all"]
	for rep in REPEATS:
		print("ROUND %d" % (rep + 1))
		for k in order.size():
			await run_case(order[(k + rep) % order.size()])
	print("ENEMIES at end %d  simulation_active %s  player hp %.0f/%.0f" % [game.floor_enemies().size(), game.simulation_active(), game.player.hp, game.player.max_hp])
	for c in ["B_1", "B_all"]: print("last %s: %s" % [c, notes[c]])

	# --- report ---
	var e := summary("empty")
	var g := summary("game_off")
	print("")
	print("SUMMARY: wall-clock ms per frame at --fixed-fps 60; %d repeats x %d timed frames after %d warm-up frames per case" % [REPEATS, TIMED_FRAMES, WARM_UP_FRAMES])
	print("  mean = mean of repeat means; sd_rep and min-max over the repeat means; frame_sd = mean within-window per-frame sd")
	print("case        mean      sd_rep   min-max(rep)         frame_sd   nodes   vs game_off")
	for c in ["empty", "game_off", "A_8", "B_1", "B_all"]:
		var s := summary(c)
		var label: String = c if c != "B_all" else "B_all(%d)" % n_pits
		print("%-10s %8.4f  %7.4f  %8.4f-%-8.4f  %8.4f  %6.0f  %+9.4f" % [
			label, s.wall, s.wall_sd, s.wall_min, s.wall_max, s.frame_sd, s.nodes, s.wall - g.wall])
	print("PAIRED (case minus game_off in the same round; mean, sd, min-max over %d rounds)" % REPEATS)
	for c in ["A_8", "B_1", "B_all"]:
		var d: Array = []
		for rep in REPEATS: d.append(results[c][rep].wall - results["game_off"][rep].wall)
		var m := mean(d)
		var sd := stdev(d)
		var se := sd / sqrt(float(REPEATS))
		print("  %-6s %+8.4f ms  sd %.4f  min-max %+.4f..%+.4f  -> %s" % [c, m, sd, d.min(), d.max(),
			"within 2 standard errors of zero: not distinguishable from game_off" if absf(m) <= 2.0 * se else "beyond 2 standard errors of zero"])
	# Self-checks: is the instrument measuring itself?
	var sleep_ms := OS.low_processor_usage_mode_sleep_usec / 1000.0
	if absf(e.wall - g.wall) <= 2.0 * maxf(e.wall_sd, g.wall_sd) or g.wall < 2.0 * e.wall:
		print("WARNING: the empty scene and the game scene read the same: the script is measuring itself")
		bad = true
	else:
		print("CHECK empty (%.4f ms) and game_off (%.4f ms) differ by %.0fx: the instrument sees the scene" % [e.wall, g.wall, g.wall / maxf(e.wall, 1e-6)])
	if e.wall > 0.5 * sleep_ms:
		print("WARNING: the empty scene takes %.3f ms, near the %.3f ms low-processor sleep: measuring the sleep (run with --fixed-fps)" % [e.wall, sleep_ms])
		bad = true
	else:
		print("CHECK empty frame %.4f ms << %.3f ms sleep: no frame sleep in the timing" % [e.wall, sleep_ms])
	var effect_means := ["game_off", "A_8", "B_1", "B_all"].map(func(c): return snappedf(summary(c).wall, 0.0001))
	for i in effect_means.size():
		for j in range(i + 1, effect_means.size()):
			if effect_means[i] == effect_means[j]:
				print("NOTE: %s and %s report the same mean (%.4f ms)" % [["game_off", "A_8", "B_1", "B_all"][i], ["game_off", "A_8", "B_1", "B_all"][j], effect_means[i]])
	clear_sparks()
	rig.queue_free()
	await step(3)
	print("COST_EFFECTS %s" % ("INSTRUMENT SUSPECT" if bad else "DONE"))
	quit(1 if bad else 0)
