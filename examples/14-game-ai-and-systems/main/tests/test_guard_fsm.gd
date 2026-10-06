extends SceneTree

# Shared observable checks for both guard brains.
const Guard = preload("res://npc/guard.gd")
var brain := Guard.Brain.FSM
# Fixtures: player position is set via player.position (printed as FIXTURE).
# Invariant: guard.mode and guard.position are read-only; guard state is never set directly.

var failures := 0
var checks   := 0

func _initialize() -> void:
	call_deferred("run")

func check(ok: bool, label: String) -> void:
	checks += 1
	if not ok:
		failures += 1
	print("PASS " if ok else "FAIL ", label)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

func _load_arena() -> Node:
	var arena: Node = load("res://npc/guard_arena.tscn").instantiate()
	arena.get_node("Guard").brain = brain
	root.add_child(arena)
	return arena

func _wait_for_mode(guard: Node, target_mode: String, timeout: float) -> float:
	var elapsed := 0.0
	while guard.mode != target_mode and elapsed < timeout:
		await create_timer(0.1).timeout
		elapsed += 0.1
	return elapsed

# ---------------------------------------------------------------------------
# Test 1 — full sequence: Patrol → Chase → Search → Patrol
# ---------------------------------------------------------------------------

func test_full_sequence() -> void:
	print("--- Test 1: Patrol -> Chase -> Search -> Patrol ---")
	var arena := _load_arena()
	var guard = arena.get_node("Guard")
	var player = arena.get_node("Player")

	await process_frame
	await process_frame

	check(guard.mode == "Patrol", "initial mode is Patrol")
	var fsm = guard.get_node("GuardFSM")
	if brain == Guard.Brain.BT:
		check(not fsm.can_process() and fsm.current_state == null,
			"inactive FSM remains uninitialized and cannot process after startup")
	else:
		check(fsm.can_process() and fsm.current_state != null,
			"selected FSM is initialized and can process after startup")

	# Fixture: place player inside sight_radius with clear LOS.
	# Guard starts at (160,360); player at (280,360) is 120 px away, no obstacle between.
	print("FIXTURE: player → (280, 360)  dist=120 < sight_radius=200, LOS clear")
	player.position = Vector2(280, 360)

	var t := await _wait_for_mode(guard, "Chase", 3.0)
	check(guard.mode == "Chase",
		"mode -> Chase when player in sight (%.1f s)" % t)

	# Fixture: move player far beyond lose_radius so guard loses sight.
	print("FIXTURE: player → (800, 560)  dist >> lose_radius=350")
	player.position = Vector2(800, 560)

	t = await _wait_for_mode(guard, "Search", 3.0)
	check(guard.mode == "Search",
		"mode -> Search when player beyond lose_radius (%.1f s)" % t)

	# Search navigates to last_known_pos (~280,360), waits 1 s, then Patrol.
	t = await _wait_for_mode(guard, "Patrol", 20.0)
	check(guard.mode == "Patrol",
		"mode -> Patrol after Search completes (%.1f s)" % t)

	arena.queue_free()
	await process_frame

# ---------------------------------------------------------------------------
# Test 2 — player hidden behind obstacle does not trigger Chase
# ---------------------------------------------------------------------------

func test_hidden_player() -> void:
	print("--- Test 2: player hidden behind obstacle stays in Patrol ---")
	var arena := _load_arena()
	var guard = arena.get_node("Guard")
	var player = arena.get_node("Player")

	await process_frame
	await process_frame

	# Fixture: guard at (160,360); obstacle spans x=520-760 y=260-460.
	# A ray from (160,360) to (900,360) passes through the obstacle → LOS blocked.
	print("FIXTURE: player → (900, 360)  behind obstacle, LOS blocked")
	player.position = Vector2(900, 360)

	await create_timer(2.0).timeout
	check(guard.mode == "Patrol",
		"player hidden behind obstacle does not trigger Chase")

	arena.queue_free()
	await process_frame

# ---------------------------------------------------------------------------
# Test 3 — player between sight_radius and lose_radius during Chase → no change ≥1 s
# ---------------------------------------------------------------------------

func test_hysteresis_zone() -> void:
	print("--- Test 3: player between sight_radius and lose_radius stays Chase >=1s ---")
	var arena := _load_arena()
	var guard = arena.get_node("Guard")
	var player = arena.get_node("Player")

	await process_frame
	await process_frame

	# Fixture: bring guard into Chase.
	print("FIXTURE: player → (280, 360)  trigger Chase")
	player.position = Vector2(280, 360)
	await _wait_for_mode(guard, "Chase", 3.0)

	# Fixture: move player into hysteresis zone.
	# Guard is near (160,360); player at (400,360) is ~240 px away.
	# sight_radius=200 < 240 < lose_radius=350, LOS clear (left of obstacle x=520).
	print("FIXTURE: player → (400, 360)  dist≈240, sight_radius<dist<lose_radius, LOS clear")
	player.position = Vector2(400, 360)

	await create_timer(1.5).timeout
	check(guard.mode == "Chase",
		"player between sight_radius and lose_radius: mode stays Chase for >=1 s")

	arena.queue_free()
	await process_frame

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

func run() -> void:
	root.size = Vector2i(1280, 720)

	for selected in [Guard.Brain.FSM, Guard.Brain.BT]:
		brain = selected
		print("=== Brain: ", Guard.Brain.keys()[brain], " ===")
		await test_full_sequence()
		await test_hidden_player()
		await test_hysteresis_zone()

	print("RESULT ", checks, " checks; ", failures, " failures")
	quit(1 if failures else 0)
