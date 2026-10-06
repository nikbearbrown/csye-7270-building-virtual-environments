extends SceneTree
## Chapter-author audit of Task 1 (written by hand, not by the agent).
## Kept outside the project so the later agent runs never see it.
## Measures what test_guard_nav.gd does not:
##  A. per-physics-frame behaviour when the target is set in the same frame
##     the arena is added (map iteration id, path size, guard position);
##  B. whether the guard ever touches the obstacle (slide collisions), how
##     close its centre gets to the obstacle rectangle, and where it stops;
##  C. for the unreachable target: final position vs get_final_position(),
##     and whether the guard is still pushing (velocity) after it settles.

const OBSTACLE := Rect2(520, 260, 240, 200)


func _initialize() -> void:
	call_deferred("run")


func dist_to_rect(p: Vector2, r: Rect2) -> float:
	var dx := maxf(maxf(r.position.x - p.x, 0.0), p.x - r.end.x)
	var dy := maxf(maxf(r.position.y - p.y, 0.0), p.y - r.end.y)
	return sqrt(dx * dx + dy * dy)


func run() -> void:
	root.size = Vector2i(1280, 720)
	# A. same-frame request
	var arena: Node = load("res://npc/guard_arena.tscn").instantiate()
	root.add_child(arena)
	var guard: CharacterBody2D = arena.get_node("Guard")
	var agent: NavigationAgent2D = guard.get_node("NavigationAgent2D")
	var start := guard.global_position
	guard.set_target(Vector2(1080, 360))
	print("A frame=0 (same frame) map_iteration=", NavigationServer2D.map_get_iteration_id(agent.get_navigation_map()), " path_size=", agent.get_current_navigation_path().size())
	for i in range(1, 6):
		await physics_frame
		print("A physics_frame=", i, " map_iteration=", NavigationServer2D.map_get_iteration_id(agent.get_navigation_map()), " path_size=", agent.get_current_navigation_path().size(), " moved_px=", snappedf(guard.global_position.distance_to(start), 0.01), " reachable=", agent.is_target_reachable())
	arena.queue_free()
	await process_frame

	# B. far-side trip, every physics frame
	arena = load("res://npc/guard_arena.tscn").instantiate()
	root.add_child(arena)
	guard = arena.get_node("Guard")
	agent = guard.get_node("NavigationAgent2D")
	await physics_frame
	await physics_frame
	var target := Vector2(1080, 360)
	guard.set_target(target)
	var obstacle_hits := 0
	var min_clearance := INF
	var frames := 0
	while frames < 120 * 20 and not agent.is_navigation_finished():
		await physics_frame
		frames += 1
		min_clearance = minf(min_clearance, dist_to_rect(guard.global_position, OBSTACLE))
		for i in guard.get_slide_collision_count():
			var c := guard.get_slide_collision(i)
			if c.get_collider() and c.get_collider().name == "Obstacle":
				obstacle_hits += 1
	print("B frames=", frames, " seconds=", snappedf(frames / 120.0, 0.01), " finished=", agent.is_navigation_finished(), " reached=", agent.is_target_reached(), " stop_distance_to_target_px=", snappedf(guard.global_position.distance_to(target), 0.1), " min_centre_clearance_to_obstacle_px=", snappedf(min_clearance, 0.1), " obstacle_slide_collisions=", obstacle_hits)
	arena.queue_free()
	await process_frame

	# C. unreachable target
	arena = load("res://npc/guard_arena.tscn").instantiate()
	root.add_child(arena)
	guard = arena.get_node("Guard")
	agent = guard.get_node("NavigationAgent2D")
	await physics_frame
	await physics_frame
	guard.set_target(OBSTACLE.get_center())
	obstacle_hits = 0
	frames = 0
	while frames < 120 * 8:
		await physics_frame
		frames += 1
		for i in guard.get_slide_collision_count():
			var c := guard.get_slide_collision(i)
			if c.get_collider() and c.get_collider().name == "Obstacle":
				obstacle_hits += 1
	var p1 := guard.global_position
	await create_timer(0.5).timeout
	print("C reachable=", agent.is_target_reachable(), " finished=", agent.is_navigation_finished(), " reached=", agent.is_target_reached(), " final_position=", agent.get_final_position(), " guard=", guard.global_position, " gap_to_final_px=", snappedf(guard.global_position.distance_to(agent.get_final_position()), 0.1), " moved_in_last_0.5s_px=", snappedf(guard.global_position.distance_to(p1), 0.01), " obstacle_slide_collisions=", obstacle_hits)
	arena.queue_free()
	await process_frame
	quit(0)
