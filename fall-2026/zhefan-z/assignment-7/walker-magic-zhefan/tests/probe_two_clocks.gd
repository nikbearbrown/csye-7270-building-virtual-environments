extends SceneTree
## Assignment 7 probe (prompt 8, step 6): the two clocks of the wolf lunge, measured in the real game loop.
## Scenario: the edges test's reference run (player at 680, wolf at 860 patrolling left, no input, 200 physics ticks).
## Per physics tick it records the wolf's state before its update (a node at physics priority -2, before the
## AnimationPlayer at -1 and the wolf at 0), the clip frame after the AnimationPlayer advanced, the state and the
## hitbox's `monitoring` at the end of the tick (priority 1000). Per process frame it records the physics frame count
## and the clip position, so a clip that moved without a physics tick would show.
## Gameplay reads the lunge's active window in wolf.gd's LUNGE branch (get_overlapping_bodies), which runs on the
## ticks whose state before the wolf's update is LUNGE. The clip's active section is frames 31..52 (LUNGE starts at
## 31, RECOVER at 53). Reports, in seconds: the largest |clip time - phase time| over every lunge-clip tick, any clip
## advance between physics ticks, and the offset of the gameplay read window and of `monitoring` against the clip's
## active section. Nothing here calls a wolf or player function.
## From fall-2026/zhefan-z/assignment-7/, at 30, 60 and 144 fps:
##   ./scripts/run-test.sh probe_two_clocks.gd 60
## Prints "observation" lines and "WALKER TESTS: N checks / F failures" (checks: the clip runs on the physics tick).

const GROUND_TOP := 327.0
const LENGTH := 200
const TICK := 1.0 / 60.0


class Pre extends Node:
	var rows: Array[Dictionary] = []
	var wolf: Wolf

	func _init() -> void:
		process_physics_priority = -2

	func _physics_process(_delta: float) -> void:
		rows.append({"state_before": Wolf.State.keys()[wolf.state], "physics_frames": Engine.get_physics_frames()})


class Post extends Node:
	var rows: Array[Dictionary] = []
	var wolf: Wolf

	func _init() -> void:
		process_physics_priority = 1000

	func _physics_process(_delta: float) -> void:
		rows.append({"state_after": Wolf.State.keys()[wolf.state], "clip": str(wolf.anim.current_animation),
			"pos": wolf.anim.current_animation_position, "monitoring": wolf.lunge_hitbox.monitoring})


class Frames extends Node:
	var rows: Array[Dictionary] = []
	var wolf: Wolf

	func _process(_delta: float) -> void:
		rows.append({"physics_frames": Engine.get_physics_frames(), "pos": wolf.anim.current_animation_position,
			"clip": str(wolf.anim.current_animation)})


var results: Array[Dictionary] = []
var failures := 0


func _initialize() -> void:
	call_deferred("run")


func check(id: String, passed: bool, observed: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))


func observe(id: String, observed: Dictionary) -> void:
	print(JSON.stringify({"id": id, "observation": observed}))


func span(ticks: Array) -> Array:
	return [ticks.front(), ticks.back()] if not ticks.is_empty() else [-1, -1]


func run() -> void:
	var main: Node = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	var player: Player = main.player
	var wolf: Wolf = main.get_node("Level/Wolf")
	player.global_position = Vector2(680.0, GROUND_TOP)
	wolf.global_position = Vector2(860.0, GROUND_TOP)
	var pre := Pre.new()
	var post := Post.new()
	var frames := Frames.new()
	for n: Node in [pre, post, frames]:
		n.set("wolf", wolf)
		root.add_child(n)
	while post.rows.size() < LENGTH:
		await process_frame
	var fps := Engine.max_fps if Engine.max_fps > 0 else -1

	var g0 := -1
	for t in LENGTH:
		if post.rows[t].state_after == "GROWL":
			g0 = t
			break
	# Every tick of the lunge clip from GROWL entry: clip time against phase time (ticks since GROWL entry / 60).
	var worst := 0.0
	var worst_tick := -1
	var lunge_ticks := []
	for t in range(g0, LENGTH):
		if post.rows[t].clip != "lunge":
			break
		lunge_ticks.append(t)
		var d := absf(post.rows[t].pos - (t - g0) * TICK)
		if d > worst:
			worst = d
			worst_tick = t
	# Clip moved in a process frame with no physics tick since the previous process frame.
	var moved_between_ticks := 0
	var process_frames := 0
	for i in range(1, frames.rows.size()):
		var a: Dictionary = frames.rows[i - 1]
		var b: Dictionary = frames.rows[i]
		if a.clip != "lunge" or b.clip != "lunge":
			continue
		process_frames += 1
		if b.physics_frames == a.physics_frames and absf(b.pos - a.pos) > 1e-9:
			moved_between_ticks += 1
	# The clip's active section (frames 31..52), the ticks gameplay reads the hitbox on (state LUNGE before the wolf's
	# update), and the ticks `monitoring` is on at the end of the tick.
	var active := lunge_ticks.filter(func(t: int) -> bool:
		var f := roundi(post.rows[t].pos * 60.0)
		return f >= 31 and f < 53)
	var reads := range(LENGTH).filter(func(t: int) -> bool: return pre.rows[t].state_before == "LUNGE")
	var armed := range(LENGTH).filter(func(t: int) -> bool: return post.rows[t].monitoring)
	var a_span := span(active)
	var r_span := span(reads)
	var m_span := span(armed)
	var offsets := {
		"read_window_start_s": (r_span[0] - a_span[0]) * TICK, "read_window_end_s": (r_span[1] - a_span[1]) * TICK,
		"monitoring_start_s": (m_span[0] - a_span[0]) * TICK, "monitoring_end_s": (m_span[1] - a_span[1]) * TICK}
	var largest := 0.0
	for v: float in offsets.values():
		largest = maxf(largest, absf(v))

	check("clip-time-equals-phase-time-on-every-lunge-clip-tick", worst < 1e-6 and lunge_ticks.size() == 89,
		{"lunge_clip_ticks": lunge_ticks.size(), "growl_tick": g0, "largest_abs_difference_s": worst,
		"at_tick": worst_tick})
	check("clip-never-advances-between-physics-ticks", moved_between_ticks == 0 and process_frames > 0,
		{"process_frames_in_lunge_clip": process_frames, "clip_moved_without_a_physics_tick": moved_between_ticks})
	observe("lunge-active-window", {
		"clip_active_section_ticks": a_span, "clip_active_section_frames": [a_span[0] - g0, a_span[1] - g0],
		"gameplay_reads_hitbox_ticks": r_span, "gameplay_reads_hitbox_frames": [r_span[0] - g0, r_span[1] - g0],
		"monitoring_on_ticks": m_span, "monitoring_on_frames": [m_span[0] - g0, m_span[1] - g0],
		"ticks": {"active": active.size(), "reads": reads.size(), "monitoring": armed.size()},
		"offsets_against_clip_active_section": offsets, "largest_offset_s": largest})
	observe("rates", {"physics_ticks_per_second": Engine.physics_ticks_per_second, "process_frames": frames.rows.size(),
		"physics_ticks": post.rows.size(), "max_fps": fps})
	main.queue_free()
	for n: Node in [pre, post, frames]:
		n.queue_free()
	await process_frame
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	quit(1 if failures else 0)
