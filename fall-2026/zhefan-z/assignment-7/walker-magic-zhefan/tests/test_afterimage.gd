extends SceneTree
## Assignment 7 visual upgrade: the lunge afterimage (features/wolf/lunge_afterimage.gd, settings in wolf.tscn).
## The real game loop with the pin's take_lunge setup (player 780, wolf 860, no input), 180 physics ticks: the wolf
## growls, lunges into the player, recovers, and does it again. Every ghost is recorded as it enters the level and
## as it leaves the tree. Checks: ghosts appear only on LUNGE ticks, on the first LUNGE tick and every 3 ticks after;
## each holds both rig parts at their pose; it starts tinted warm orange at alpha 0.6 and is gone about 0.25 s later
## (r1, 2026-11-12; process clock, within one frame plus one tick); none is left at the end; the wolf's states match the take_lunge pin.
## From fall-2026/zhefan-z/assignment-7/, at 30, 60 and 144 fps:
##   ./scripts/run-test.sh test_afterimage.gd 60
## Prints one JSON line per check and "WALKER TESTS: N checks / F failures"; exit code 1 on any failure.

const GROUND_TOP := 327.0
const LENGTH := 180
const INTERVAL := 3
const ALPHA := 0.6
const LIFE := 0.25
const TINT := Color(1.0, 0.55, 0.2)


class Clock extends Node:
	var t := 0.0

	func _init() -> void:
		process_priority = -1000

	func _process(delta: float) -> void:
		t += delta


class Sampler extends Node:
	var ticks := 0
	var states: Array[String] = []
	var wolf: Wolf

	func _init() -> void:
		process_physics_priority = 1000

	func _physics_process(_delta: float) -> void:
		states.append(Wolf.State.keys()[wolf.state])
		ticks += 1


var results: Array[Dictionary] = []
var failures := 0


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


func run() -> void:
	var counts := {}
	for i in 40:
		await process_frame
		var dd := root.get_process_delta_time()
		counts[dd] = counts.get(dd, 0) + 1
	var frame_s: float = counts.keys().reduce(func(a: float, b: float) -> float: return a if counts[a] >= counts[b] else b)

	var clock := Clock.new()
	root.add_child(clock)
	var main: Node = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	var wolf: Wolf = main.get_node("Level/Wolf")
	main.player.global_position = Vector2(780, GROUND_TOP)
	wolf.global_position = Vector2(860, GROUND_TOP)
	var sampler := Sampler.new()
	sampler.wolf = wolf
	root.add_child(sampler)
	var ghosts: Array[Dictionary] = []
	var rig := [wolf.get_node("Facing/Rig/RearPivot/Rear"), wolf.get_node("Facing/Rig/FrontPivot/Front")]
	main.get_node("Level").child_entered_tree.connect(func(node: Node) -> void:
		if "LungeGhost" in str(node.name):
			var g := {"tick": sampler.ticks, "t_in": clock.t, "t_out": -1.0, "alpha": node.modulate.a,
				"tint": Color(node.modulate, 1.0), "node": node, "pose_ok": false}
			ghosts.append(g)
			node.tree_exited.connect(func() -> void: g.t_out = clock.t)
			# The parts are added right after the ghost enters the tree; read them at the end of this physics step.
			(func() -> void:
				var kids := node.get_children()
				g.pose_ok = kids.size() == 2 and kids.all(func(k: Node) -> bool: return k is Sprite2D) \
					and (kids[0] as Sprite2D).global_transform.is_equal_approx(rig[0].global_transform) \
					and (kids[1] as Sprite2D).global_transform.is_equal_approx(rig[1].global_transform)
				).call_deferred())
	while sampler.ticks < LENGTH:
		await process_frame
	for i in roundi(LIFE / frame_s) + 3:
		await process_frame

	var states := sampler.states.slice(0, LENGTH)
	# Expected spawn ticks: the first tick of each LUNGE run and every INTERVAL ticks after, while it lasts.
	var expected := []
	var run_start := -1
	for t in states.size():
		if states[t] == "LUNGE":
			if run_start < 0:
				run_start = t
			if (t - run_start) % INTERVAL == 0:
				expected.append(t)
		else:
			run_start = -1
	var spawned := ghosts.map(func(g: Dictionary) -> int: return g.tick)
	var outside := spawned.filter(func(t: int) -> bool: return t >= states.size() or states[t] != "LUNGE")
	check("ghosts-only-in-lunge-every-3-ticks", spawned == expected and outside.is_empty() and not expected.is_empty(),
		{"spawn_ticks": spawned, "expected": expected, "outside_lunge": outside})
	check("ghost-holds-the-rig-pose", ghosts.all(func(g: Dictionary) -> bool: return g.pose_ok), {"ghosts": ghosts.size()})
	check("ghost-tinted-orange-at-60-percent", ghosts.all(func(g: Dictionary) -> bool:
		return absf(g.alpha - ALPHA) < 0.01 and (g.tint as Color).is_equal_approx(TINT)),
		{"alphas": ghosts.map(func(g: Dictionary) -> float: return snappedf(g.alpha, 0.001)).slice(0, 3), "tint": TINT})
	var lives := ghosts.map(func(g: Dictionary) -> float: return g.t_out - g.t_in if g.t_out >= 0.0 else -1.0)
	var tol := frame_s + 1.0 / 60.0 + 1e-4
	check("ghost-gone-after-about-0.25s", not lives.is_empty() and lives.all(func(l: float) -> bool:
		return l >= LIFE - 1e-4 and l <= LIFE + tol),
		{"life_min_s": snappedf(lives.min(), 0.0001), "life_max_s": snappedf(lives.max(), 0.0001), "tolerance_s": snappedf(tol, 0.0001),
		"fps": roundi(1.0 / frame_s)})
	var left := main.get_node("Level").get_children().filter(func(n: Node) -> bool: return "LungeGhost" in str(n.name))
	check("no-ghost-left-after-the-lunges", left.is_empty(), {"left": left.size()})
	var pin: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(
		ProjectSettings.globalize_path("res://").path_join("../logs/pin/take_lunge.json").simplify_path()))
	var pinned := (pin.ticks as Array).map(func(row: Array) -> String: return row[4])
	check("wolf-states-match-the-take-lunge-pin", states == pinned, {"ticks": states.size(), "pinned": pinned.size()})

	main.queue_free()
	sampler.queue_free()
	clock.queue_free()
	await process_frame
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)
