extends SceneTree
## The headless CPU price of the two effects (CHANGE-BRIEF.md, section 8),
## adapted from Chapter 9's examples/09-particle-effects/tests/particle_cost.gd.
## Run from this folder, at a fixed rate:
##   scripts/run-test.sh cost_effects.gd 60 300
## Without --fixed-fps, headless frames sleep toward 6.9 ms and every case reads
## the same (CHANGE-BRIEF.md, failure 13).
##
## It times whole frames, as the chapter's script does, in five cases:
## - empty: an empty Node2D, the chapter's control;
## - game, effects off: Main with Effects and DustTrail removed before it enters
##   the tree, Rudy idle at the start;
## - game, effects off, running: the same, with Rudy running, a control for B;
## - Effect A at its most: Main as it ships, Rudy idle, with 2 SlashSparks
##   bursts alive on every timed frame (rule A3: at most 2 at once). A new burst
##   starts whenever one finishes, the way EffectsDriver starts one, because
##   real swings keep 2 alive for only part of each 0.3 s;
## - Effect B at its most: Main as it ships, Rudy running at full speed on the
##   ground, so RunDust emits on every timed frame and no burst is alive.
## Rudy runs by holding move_right, on the flat stretch x 2050–2350 between
## GoblinA's patrol and the pickup; each time he reaches its end, this script
## moves him back to its start without touching his velocity, as checks.gd's
## _teleport moves him. That is the only game state it writes.
## Each round builds every case afresh and times it, so drift over the run falls
## on every case alike. It reports each case's per-frame mean and spread over
## all rounds, the spread of the round means, and what each case did on its
## timed frames, so a case that did not reach its state shows.
## Headless Godot uses a dummy renderer: no particle is processed or drawn, so
## this measures node bookkeeping and the driver's code, not the effects' GPU
## time (CLAUDE.md, Headless facts).

const WARM_UP_FRAMES := 60
const TIMED_FRAMES := 300
const ROUNDS := 5
const MOST_BURSTS := 2 ## rule A3
const BURST_GAP := 10 ## frames at least between two bursts, so they stay staggered
const LAP_START_X := 2050.0
const LAP_END_X := 2350.0
const CASES := ["empty", "game_off", "game_off_running", "effect_a", "effect_b"]
const LABELS := {
	"empty": "Empty scene",
	"game_off": "Game, both effects off, Rudy idle",
	"game_off_running": "Game, both effects off, Rudy running (control for B)",
	"effect_a": "Effect A, 2 bursts alive, Rudy idle",
	"effect_b": "Effect B, Rudy running, emitting",
}


## One case being built and timed.
class Run:
	var name := ""
	var node: Node
	var rudy: CharacterBody2D
	var sword_box: CollisionShape2D
	var slash_bursts: Node2D
	var run_dust: GPUParticles2D
	var running := false
	var bursts := false
	var frame := 0
	var last_burst := -BURST_GAP
	# What it did on its timed frames:
	var started := 0
	var alive_min := 1 << 30
	var alive_max := 0
	var sparks_emitting_min := 1 << 30
	var cond_ticks := 0
	var dust_ticks := 0
	var particle_nodes := 0


## A --script run compiles this file before the autoloads exist, so it names no
## game class: main.gd and rudy.gd use Music and Sfx, and would fail to compile.
## It loads them once the tree is up.
var _main_scene: PackedScene
var _sparks_scene: PackedScene
var _main_script: GDScript
var _play_mode: int ## Rudy.Mode.PLAY
var _times := {} ## case -> every timed frame's ms
var _round_means := {} ## case -> each round's mean ms
var _did := {} ## case -> the last round's Run


func _initialize() -> void:
	call_deferred("run")


func run() -> void:
	print("Rendering method: ", RenderingServer.get_current_rendering_method())
	print("Video adapter: ", RenderingServer.get_video_adapter_name())
	print("Command line: ", " ".join(OS.get_cmdline_args()))
	print("Headless Godot uses a dummy renderer, so GPU particle simulation and all drawing are not measured.")
	print("%d rounds; each case per round: %d warm-up frames, then %d timed frames." % [
		ROUNDS, WARM_UP_FRAMES, TIMED_FRAMES])
	_main_scene = load("res://app/main.tscn")
	_sparks_scene = load("res://effects/slash_sparks.tscn")
	_main_script = load("res://app/main.gd")
	_play_mode = (load("res://content/rudy/rudy.gd") as GDScript).get("Mode")["PLAY"]
	for name in CASES:
		_times[name] = []
		_round_means[name] = []

	for round_index in ROUNDS:
		for name in CASES:
			var r := _build(name)
			for _frame in WARM_UP_FRAMES:
				_step(r, false)
				await process_frame
			var started_usec := Time.get_ticks_usec()
			var last_usec := started_usec
			for _frame in TIMED_FRAMES:
				_step(r, true)
				await process_frame
				var now_usec := Time.get_ticks_usec()
				_times[name].append((now_usec - last_usec) / 1000.0)
				last_usec = now_usec
			_round_means[name].append((last_usec - started_usec) / 1000.0 / TIMED_FRAMES)
			_did[name] = r
			_tear_down(r)
			for _frame in 3:
				await process_frame
		print("round %d of %d done" % [round_index + 1, ROUNDS])

	print("")
	print("Per frame, over %d timed frames in %d rounds:" % [ROUNDS * TIMED_FRAMES, ROUNDS])
	for name in CASES:
		_report(name)
	print("")
	print("What each case did on its timed frames (last round):")
	for name in CASES:
		print("  %-52s %s" % [LABELS[name], _did_line(_did[name])])
	print("")
	print("Differences of the mean, with the round means' ranges:")
	_compare("game_off", "empty", true)
	_compare("effect_a", "game_off", false)
	_compare("effect_b", "game_off_running", false)
	_compare("game_off_running", "game_off", false)
	_compare("effect_b", "game_off", false)
	var means: Array[float] = []
	for name in CASES:
		means.append(_mean(_times[name]))
	if means.max() - means.min() <= 0.05 * means.max():
		print("WARNING: every case reads within 5 % of the others, the empty scene included: the script may be measuring itself.")
	quit()


func _build(name: String) -> Run:
	var r := Run.new()
	r.name = name
	if name == "empty":
		r.node = Node2D.new()
		root.add_child(r.node)
		return r
	_main_script.title_shown = true # straight to play, as test_slash_sparks_state.gd's _start_level does
	var main: Node2D = _main_scene.instantiate()
	if name.begins_with("game_off"):
		for path in ["Effects", "DustTrail"]:
			var node := main.get_node(path)
			main.remove_child(node)
			node.free()
	root.add_child(main)
	r.node = main
	r.rudy = main.get_node("Rudy")
	r.sword_box = r.rudy.get_node("SwordHitbox/Shape")
	if main.has_node("Effects"):
		r.slash_bursts = main.get_node("Effects/SlashBursts")
		r.run_dust = main.get_node("DustTrail/RunDust")
	r.running = name in ["game_off_running", "effect_b"]
	r.bursts = name == "effect_a"
	if r.running:
		r.rudy.global_position.x = LAP_START_X
		Input.action_press(&"move_right")
	return r


## Runs once before each frame, warm-up and timed alike.
func _step(r: Run, timed: bool) -> void:
	r.frame += 1
	if r.running and r.rudy.global_position.x >= LAP_END_X:
		r.rudy.global_position.x = LAP_START_X
	if r.bursts:
		var alive := _alive_bursts(r)
		if alive.size() < MOST_BURSTS and r.frame - r.last_burst >= BURST_GAP:
			_start_burst(r)
			alive = _alive_bursts(r)
			if timed:
				r.started += 1
		if timed:
			var emitting := 0
			for burst in alive:
				if (burst.get_node("Sparks") as GPUParticles2D).emitting:
					emitting += 1
			r.alive_min = mini(r.alive_min, alive.size())
			r.alive_max = maxi(r.alive_max, alive.size())
			r.sparks_emitting_min = mini(r.sparks_emitting_min, emitting)
	if timed and r.rudy != null:
		if r.rudy.mode == _play_mode and r.rudy.is_on_floor() and absf(r.rudy.velocity.x) > 1.0:
			r.cond_ticks += 1
		if r.run_dust != null and r.run_dust.emitting:
			r.dust_ticks += 1
		if r.frame == WARM_UP_FRAMES + 1:
			r.particle_nodes = r.node.find_children("*", "GPUParticles2D", true, false).size()


## As EffectsDriver._fire_slash_sparks starts one: at the hitbox, facing his way.
func _start_burst(r: Run) -> void:
	var burst: Node2D = _sparks_scene.instantiate()
	r.slash_bursts.add_child(burst)
	burst.global_position = r.sword_box.global_position
	burst.scale.x = r.rudy.facing
	(burst.get_node("Sparks") as GPUParticles2D).finished.connect(burst.queue_free)
	for emitter: GPUParticles2D in burst.get_children():
		emitter.emitting = true
	r.last_burst = r.frame


func _alive_bursts(r: Run) -> Array[Node]:
	return r.slash_bursts.get_children().filter(func(n: Node) -> bool: return not n.is_queued_for_deletion())


func _tear_down(r: Run) -> void:
	if r.running:
		Input.action_release(&"move_right")
	r.node.queue_free()


func _did_line(r: Run) -> String:
	if r.name == "empty":
		return "nothing"
	var line := "%d GPUParticles2D in the tree, condition held %d/%d, RunDust emitting %d/%d" % [
		r.particle_nodes, r.cond_ticks, TIMED_FRAMES, r.dust_ticks, TIMED_FRAMES]
	if r.bursts:
		line += ", bursts alive %d–%d, sparks emitting at least %d, %d bursts started" % [
			r.alive_min, r.alive_max, r.sparks_emitting_min, r.started]
	return line


func _report(name: String) -> void:
	var times: Array = _times[name]
	var sorted := times.duplicate()
	sorted.sort()
	var rounds: Array = _round_means[name]
	print("  %-52s mean %.4f ms, sd %.4f, median %.4f, p95 %.4f, max %.4f; round means %.4f–%.4f ms" % [
		LABELS[name], _mean(times), _sd(times), sorted[sorted.size() / 2],
		sorted[int(sorted.size() * 0.95)], sorted[-1], rounds.min(), rounds.max()])


func _compare(a: String, b: String, should_differ: bool) -> void:
	var diff := _mean(_times[a]) - _mean(_times[b])
	var ra: Array = _round_means[a]
	var rb: Array = _round_means[b]
	var overlap: bool = ra.min() <= rb.max() and rb.min() <= ra.max()
	var verdict := "round-mean ranges overlap: not told apart" if overlap else "round-mean ranges apart"
	if overlap and should_differ:
		verdict += "  WARNING: these should differ; the script may be measuring itself"
	print("  %-18s - %-18s %+.4f ms  (%s)" % [a, b, diff, verdict])


func _mean(values: Array) -> float:
	var total := 0.0
	for v: float in values:
		total += v
	return total / values.size()


func _sd(values: Array) -> float:
	var m := _mean(values)
	var total := 0.0
	for v: float in values:
		total += (v - m) * (v - m)
	return sqrt(total / values.size())
