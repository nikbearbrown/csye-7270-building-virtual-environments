extends SceneTree
## A7 Step 2 behaviour pins (agent, 2026-11-22), written before any clip
## exists. They pin what the game does today, through the real game loop
## (res://game/main.tscn, PixelDisplay -> SubViewport -> GameManager) and real
## input (Input.parse_input_event), and must still pass after the change,
## except the pins CHANGE-BRIEF.md says change (marked BRIEF-CHANGES below:
## change 1, the release; r1 lists the existing suites it alters).
##
## Run: ./scripts/run-test.sh test_a7_pins.gd 60   (one physics tick and one
## process frame per step at --fixed-fps 60; every count below is in those).
##
## Pinned:
##  N  NPC idle (可露希尔, base store): cell order and the 20-frame cell hold.
##  S  Lappland's states in order for one scripted run: held attack on an
##     enemy -> attack_1, attack_2, attack_3, wave (release), attack_1.
##  T  Existing timings: swing interval, a swing's move lock, the dodge's
##     invulnerable ticks, a ground-click walk.
##  G  The gameplay fact the committing action is read against: the tick the
##     wave spawns and the charge clears, relative to the release swing, and
##     what a dodge right after a release click leaves (BRIEF-CHANGES).

var rig: Node
var game: GameManager
var failures := 0
var passes := 0

func _initialize() -> void: call_deferred("run")

func step(n: int = 1) -> void:
	for i in range(n):
		await physics_frame
		await process_frame

func check(label: String, passed: bool) -> void:
	print(("PASS " if passed else "FAIL ") + label)
	if passed: passes += 1
	else: failures += 1

func find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := find_game(child)
		if found != null: return found
	return null

## Real events, as tests/test_hit_spark_state.gd:151-161 (A6) measured:
## under --headless the display server drops the window dispatch of injected
## events, so the same event is also pushed into the root window and travels
## root -> SubViewportContainer -> SubViewport -> GameManager._input.
func send(event: InputEvent) -> void:
	Input.parse_input_event(event)
	if DisplayServer.get_name() == "headless": root.push_input(event, true)

func hover(point: Vector3) -> Vector2:
	var screen := game.camera.unproject_position(point) * root.get_visible_rect().size / game.get_viewport().get_visible_rect().size
	var motion := InputEventMouseMotion.new()
	motion.position = screen
	motion.global_position = screen
	motion.button_mask = MOUSE_BUTTON_MASK_LEFT if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) else 0
	send(motion)
	return screen

func mouse(point: Vector3, pressed: bool) -> void:
	var screen := hover(point)
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.position = screen
	event.global_position = screen
	event.pressed = pressed
	event.button_mask = MOUSE_BUTTON_MASK_LEFT if pressed else 0
	send(event)

func dash_key(pressed: bool) -> void:
	var event := InputEventAction.new()
	event.action = &"dash"
	event.pressed = pressed
	send(event)

func waves() -> int:
	var n := 0
	for node in game.get_children():
		if node is SwordWave: n += 1
	return n

func clear_waves() -> void:
	for node in game.get_children():
		if node is SwordWave: node.queue_free()

func run() -> void:
	rig = load("res://game/main.tscn").instantiate()
	rig.persist_sessions = false
	root.add_child(rig)
	await step(10)
	game = find_game(rig)
	game.fixed_map_seed = 1729
	game.seed_rng(1729)

	# ---- N: NPC idle at the base store ---------------------------------
	var closure := game.base_map.get_node_or_null("store/Closure")
	check("N0 可露希尔 stands at the base store", closure != null and closure.is_inside_tree())
	if closure != null:
		var cells: Array[int] = []
		var change_frames: Array[int] = []
		var last := int(closure.frame)
		for i in range(200):
			await step()
			var now := int(closure.frame)
			if now != last:
				cells.append(now)
				change_frames.append(i)
				last = now
		var holds: Array[int] = []
		for i in range(1, change_frames.size()): holds.append(change_frames[i] - change_frames[i - 1])
		print("N cells ", cells, " holds ", holds)
		var ordered := cells.size() >= 8
		for i in range(1, cells.size()): ordered = ordered and cells[i] == (cells[i - 1] + 1) % 4
		check("N1 cells advance 0,1,2,3 and wrap to 0, no skip, no repeat (%d changes)" % cells.size(), ordered)
		var steady := holds.size() >= 7
		for h in holds: steady = steady and absi(h - 20) <= 1
		check("N2 each cell holds 20 frames at 60 fps (1/3 s; a breath 80 frames = 1.333 s)", steady)
		check("N3 only cells 0-3 appear", cells.all(func(c): return c >= 0 and c < 4))

	# ---- field setup -----------------------------------------------------
	await game.start_contract("mine")
	game._clear_field()
	await step(3)
	var p := game.player
	p.set_operator("lappland")
	var item := Item.create("A7 pin sword", Item.Category.WEAPON, 2, 1)
	item.modifiers = [ItemModifier.trigger_mod(ItemModifier.Trigger.SWORD_WAVE)]
	p.equip(item)
	var origin := p.global_position
	var enemy := game._spawn_enemy(origin + Vector3(2, 0, 0), true, false)
	enemy.global_position = origin + Vector3(2, 0, 0)
	enemy.max_health = 1000000
	enemy.health = 1000000
	enemy.set_physics_process(false)
	await step(3)
	check("S0 Lappland in the field, simulation running, charge 0", p.operator_id == "lappland" and not p.is_amiya() and game.simulation_active() and p.sword_charge == 0)

	# ---- S, T, G: hold the attack on the enemy ---------------------------
	var actions: Array[String] = []
	var swing_ticks: Array[int] = []
	var swing_actions: Array[String] = []
	var swing_locks: Array[float] = []
	var release_tick := -1
	var wave_tick := -1
	var charge_zero_tick := -1
	var charge_before := p.sword_charge
	var waves_before := waves()
	var last_cooldown := p._attack_cooldown
	await mouse(enemy.global_position, true)
	for i in range(200):
		hover(enemy.global_position)
		await step()
		var name := p._sprite.action_name
		if name != "" and (actions.is_empty() or actions[-1] != name): actions.append(name)
		if p._attack_cooldown > last_cooldown + 0.0001:
			swing_ticks.append(i)
			swing_actions.append(name)
			swing_locks.append(p.swing_remaining)
			if charge_before >= p.wave_hits_needed() and release_tick < 0: release_tick = i
		last_cooldown = p._attack_cooldown
		if wave_tick < 0 and waves() > waves_before: wave_tick = i
		if release_tick >= 0 and charge_zero_tick < 0 and p.sword_charge == 0: charge_zero_tick = i
		charge_before = p.sword_charge
		if swing_ticks.size() >= 6: break
	await mouse(enemy.global_position, false)
	var intervals: Array[int] = []
	for i in range(1, swing_ticks.size()): intervals.append(swing_ticks[i] - swing_ticks[i - 1])
	print("S actions ", actions, " swings ", swing_actions, " at ", swing_ticks, " intervals ", intervals, " locks ", swing_locks)
	print("G release tick ", release_tick, " wave tick ", wave_tick, " charge-zero tick ", charge_zero_tick, " cooldown ", p.current_cooldown(), " rate ", p.animation_rate())
	check("S1 states in order: attack_1, attack_2, attack_3, wave, attack_1",
		actions.size() >= 5 and actions.slice(0, 5) == ["attack_1", "attack_2", "attack_3", "wave", "attack_1"])
	check("T1 swings %s ticks apart while held (current_cooldown %.3f s)" % [str(intervals), p.current_cooldown()],
		intervals.size() >= 4 and intervals.all(func(d): return d == roundi(p.current_cooldown() * 60.0) or d == roundi(p.current_cooldown() * 60.0) + 1))
	check("T2 a normal swing locks movement for 0.25 s at rate 1 (swing_remaining %.4f)" % (swing_locks[0] if not swing_locks.is_empty() else -1.0),
		not swing_locks.is_empty() and absf(swing_locks[0] - 3.0 / 12.0) < 0.02)
	# BRIEF-CHANGES (change 1): the release locks 20/30 s, and the sprite plays no "wave".
	var release_lock: float = swing_locks[swing_ticks.find(release_tick)] if release_tick in swing_ticks else -1.0
	check("G1 [BRIEF-CHANGES] the release locks movement 0.25 s (swing_remaining %.4f)" % release_lock, absf(release_lock - 3.0 / 12.0) < 0.02)
	check("G2 [BRIEF-CHANGES] the release is the 4th swing", release_tick >= 0 and swing_ticks.find(release_tick) == 3)
	check("G3 [BRIEF-CHANGES] the wave spawns on the release swing's tick (offset %d)" % (wave_tick - release_tick), release_tick >= 0 and wave_tick == release_tick)
	check("G4 [BRIEF-CHANGES] the charge clears on the release swing's tick (offset %d)" % (charge_zero_tick - release_tick), release_tick >= 0 and charge_zero_tick == release_tick)

	# ---- G: a dodge two ticks after a release click ----------------------
	await step(90)
	clear_waves()
	await step(2)
	p.sword_charge = p.wave_hits_needed()
	p.stamina = 100.0  # the cap, entities/player.gd:561
	p._dash_cooldown = 0.0
	await mouse(enemy.global_position, true)
	await step()
	await mouse(enemy.global_position, false)
	await step()
	dash_key(true)
	await step()
	dash_key(false)
	await step(30)
	print("G dodge-after-release: waves ", waves(), " charge ", p.sword_charge)
	check("G5 [BRIEF-CHANGES] dodge 2 ticks after a release click: the wave is out (1) and the charge is spent (0)", waves() == 1 and p.sword_charge == 0)

	# ---- T: the dodge's invulnerable window ------------------------------
	await step(120)
	p.stamina = 100.0  # the cap, entities/player.gd:561
	p._dash_cooldown = 0.0
	var invulnerable_ticks := 0
	dash_key(true)
	await step()
	dash_key(false)
	for i in range(60):
		if p.invulnerable: invulnerable_ticks += 1
		await step()
	print("T dash invulnerable ticks ", invulnerable_ticks)
	check("T3 a dodge is invulnerable for 17 ticks (DASH_INVULN_DURATION 0.28 s)", invulnerable_ticks == 17)

	# ---- T: a ground click walks, no swing -------------------------------
	await step(30)
	var start := p.global_position
	var target := start + Vector3(0, 0, -3)
	var cooldown_before := p._attack_cooldown
	await mouse(target, true)
	await step()
	await mouse(target, false)
	var arrive := -1
	for i in range(180):
		await step()
		if not p._has_move_target:
			arrive = i
			break
	var moved := Vector2(p.global_position.x - start.x, p.global_position.z - start.z).length()
	print("T walk 3 units: arrived after ", arrive, " ticks; moved ", moved)
	check("T4 a ground click walks there and does not swing", arrive > 0 and p._attack_cooldown <= cooldown_before)
	# Measured, not derived: the first draft predicted 31-36 ticks for 3 units at
	# 5.5/s and failed; the walk ends after 26 ticks having moved 2.38 units
	# (same in two runs). Pinned as measured; the pin is that it does not change.
	check("T5 the click walk ends after 26 ticks (+-1), 2.38 units (+-0.05) (%d, %.3f)" % [arrive, moved], absi(arrive - 26) <= 1 and absf(moved - 2.383) < 0.05)

	print("A7_PINS: %d passed / %d failed" % [passes, failures])
	rig.queue_free()
	await step(3)
	quit(1 if failures else 0)
