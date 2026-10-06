extends SceneTree

# Obstacle collision bounds (used for penetration checks in tests 1 and 2).
# The StaticBody2D obstacle is 240x200 centred at (640,360).
const OBS_L := 520.0
const OBS_R := 760.0
const OBS_T := 260.0
const OBS_B := 460.0

var failures := 0
var checks := 0

func _initialize() -> void:
	call_deferred("run")

func check(ok: bool, label: String) -> void:
	checks += 1
	if not ok:
		failures += 1
	print("PASS " if ok else "FAIL ", label)

func inside_obstacle(pos: Vector2) -> bool:
	return pos.x > OBS_L and pos.x < OBS_R and pos.y > OBS_T and pos.y < OBS_B

func run() -> void:
	root.size = Vector2i(1280, 720)

	# ------------------------------------------------------------------ #
	# Check 3 — same-frame target request before navigation map sync.     #
	# Observe actual behaviour; no PASS/FAIL assertion on the outcome.    #
	# ------------------------------------------------------------------ #
	print("--- Check 3: same-frame set_target before nav-map sync ---")
	var arena3: Node = load("res://npc/guard_arena.tscn").instantiate()
	root.add_child(arena3)
	var guard3: CharacterBody2D = arena3.get_node("Guard")
	var agent3: NavigationAgent2D = guard3.get_node("NavigationAgent2D")
	var pos3_before := guard3.global_position
	# Call set_target in the same frame – nav map has not synced yet.
	guard3.set_target(Vector2(1080, 360))
	# Record the path status immediately (before any physics tick).
	var finished_before := agent3.is_navigation_finished()
	var reachable_before := agent3.is_target_reachable()
	await create_timer(0.3).timeout
	var pos3_after := guard3.global_position
	var moved3 := pos3_after.distance_to(pos3_before) > 5.0
	print("OBSERVE same-frame: nav_finished_before_tick=", finished_before,
		" reachable_before_tick=", reachable_before,
		" moved_after_0.3s=", moved3,
		" guard.position=", pos3_after)
	arena3.queue_free()
	await process_frame

	# ------------------------------------------------------------------ #
	# Check 1 — guard reaches target on far side of obstacle; no         #
	# recorded position lies inside the obstacle collision bounds.        #
	# ------------------------------------------------------------------ #
	print("--- Check 1: guard navigates around obstacle ---")
	var arena1: Node = load("res://npc/guard_arena.tscn").instantiate()
	root.add_child(arena1)
	var guard1: CharacterBody2D = arena1.get_node("Guard")

	# Wait for navigation map to synchronise (one physics frame is enough
	# per Godot docs; one extra frame adds safety).
	await process_frame
	await process_frame

	var target1 := Vector2(1080, 360)
	guard1.set_target(target1)

	var inside_obs := false
	var reached := false
	var elapsed := 0.0
	const TIME_LIMIT := 20.0

	while elapsed < TIME_LIMIT:
		await create_timer(0.1).timeout
		elapsed += 0.1
		var gp := guard1.global_position
		if inside_obstacle(gp):
			inside_obs = true
			print("WARN guard inside obstacle at t=", elapsed, " pos=", gp)
		if gp.distance_to(target1) < 64.0:
			reached = true
			break

	check(reached, "guard reaches far-side target within " + str(TIME_LIMIT) + "s")
	check(not inside_obs, "guard never enters obstacle collision bounds")
	arena1.queue_free()
	await process_frame

	# ------------------------------------------------------------------ #
	# Check 2 — target inside obstacle: is_target_reachable() is false;  #
	# guard stops at closest reachable point without pushing into solid.  #
	# ------------------------------------------------------------------ #
	print("--- Check 2: unreachable target inside obstacle ---")
	var arena2: Node = load("res://npc/guard_arena.tscn").instantiate()
	root.add_child(arena2)
	var guard2: CharacterBody2D = arena2.get_node("Guard")
	var agent2: NavigationAgent2D = guard2.get_node("NavigationAgent2D")

	await process_frame
	await process_frame

	guard2.set_target(Vector2(640, 360))  # centre of obstacle
	await create_timer(0.5).timeout       # let the path request resolve

	var reachable2 := agent2.is_target_reachable()
	check(not reachable2, "target inside obstacle: is_target_reachable() == false")

	await create_timer(4.0).timeout  # give guard time to settle

	var gp2 := guard2.global_position
	check(not inside_obstacle(gp2),
		"guard rests outside obstacle bounds for unreachable target (pos=" + str(gp2) + ")")

	arena2.queue_free()
	await process_frame

	print("RESULT ", checks, " checks; ", failures, " failures")
	quit(1 if failures else 0)
