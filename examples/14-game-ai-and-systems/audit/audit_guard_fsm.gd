extends SceneTree
## Chapter-author audit of the guard brain (written by hand, not by the agent).
## Reads only guard.mode and positions; moves only the player (fixture).
## Works for any brain that sets `mode` (FSM, or BT via --brain=BT when the
## Guard has a `brain` property).
##  H1: while chasing, hold the player exactly 260 px from the guard (between
##      sight_radius 200 and lose_radius 350) every physics frame for 1 s and
##      count mode changes per frame. The agent's own test let the guard walk
##      toward a stationary player, so the band was never held.
##  H2: while patrolling, hold the player 260 px away for 1 s: a patrolling
##      guard must NOT start chasing (the band is not the sight radius).
##  H3: single-threshold counterfactual is not built; see chapter text.

const BAND := 260.0


func _initialize() -> void:
	call_deferred("run")


func brain_arg() -> String:
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--brain="):
			return a.trim_prefix("--brain=")
	return ""


func load_arena() -> Node:
	var arena: Node = load("res://npc/guard_arena.tscn").instantiate()
	if brain_arg() == "BT":
		arena.get_node("Guard").brain = 1  # Guard.Brain.BT
	root.add_child(arena)
	return arena


func run() -> void:
	root.size = Vector2i(1280, 720)
	# H1
	var arena := load_arena()
	var guard: Node2D = arena.get_node("Guard")
	var player: Node2D = arena.get_node("Player")
	for i in 4:
		await physics_frame
	player.global_position = Vector2(220, 540)
	var f := 0
	while guard.mode != "Chase" and f < 240:
		await physics_frame
		f += 1
	print("H1 entered Chase after ", f, " physics frames")
	# lead the chasing guard down into the corridor below the obstacle
	player.global_position = Vector2(230, 650)
	f = 0
	while guard.global_position.y < 500 and f < 480:
		await physics_frame
		f += 1
	print("H1 guard at ", guard.global_position.round(), " mode=", guard.mode, " before holding the band (player moved along the corridor below the obstacle)")
	var changes := 0
	var last: String = guard.mode
	var modes_seen := {}
	for i in 120:
		player.global_position = guard.global_position + Vector2(BAND, 0)
		await physics_frame
		modes_seen[guard.mode] = true
		if guard.mode != last:
			changes += 1
			last = guard.mode
	print("H1 band=", BAND, "px held 120 physics frames: mode_changes=", changes, " modes_seen=", modes_seen.keys(), " final=", guard.mode)
	arena.queue_free()
	await process_frame
	# H2
	arena = load_arena()
	guard = arena.get_node("Guard")
	player = arena.get_node("Player")
	for i in 4:
		await physics_frame
	changes = 0
	last = guard.mode
	modes_seen = {}
	for i in 120:
		player.global_position = guard.global_position + Vector2(0, BAND)
		await physics_frame
		modes_seen[guard.mode] = true
		if guard.mode != last:
			changes += 1
			last = guard.mode
	print("H2 patrolling guard, player held at ", BAND, "px for 120 physics frames: mode_changes=", changes, " modes_seen=", modes_seen.keys(), " final=", guard.mode)
	arena.queue_free()
	await process_frame
	quit(0)
