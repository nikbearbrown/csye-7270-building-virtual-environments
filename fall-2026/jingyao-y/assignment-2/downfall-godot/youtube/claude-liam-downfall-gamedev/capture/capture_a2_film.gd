extends SceneTree

## Film capture choreography for the Assignment 2 explainer (not shipped game
## code; copied into an isolated clone's tests/ folder before recording).
## Drives the real main scene: Lappland moves through Player.set_move_target
## (the right-click path) or real WASD InputEventKeys, attacks through
## Player.attack (the left-click path), pauses with a real Esc InputEventKey and
## clicks camp buttons with real mouse events. Sessions are not persisted
## (PixelDisplay.persist_sessions = false), so the player's save is untouched.
##
## godot --path <clone> --script res://tests/capture_a2_film.gd
##       --write-movie <out>.avi --fixed-fps 30 -- <clip>
## Clips: hall | warehouse | combat | death | extract   (optional 2nd arg: map seed)
## Every decision is appended to user args' <clip>-inputs.jsonl next to the video.

var rig: Node
var game: GameManager
var clip := ""
var log_lines: PackedStringArray = []
var frame := 0

func _initialize() -> void: call_deferred("run")

func note(event: String, data: Dictionary = {}) -> void:
	data["frame"] = frame
	data["event"] = event
	log_lines.append(JSON.stringify(data))

func frames(n: int) -> void:
	for i in range(n):
		await process_frame
		frame += 1

func seconds(s: float) -> void:
	await frames(int(round(s * 30.0)))

func find_game(node: Node) -> GameManager:
	if node is GameManager: return node
	for child in node.get_children():
		var found := find_game(child)
		if found != null: return found
	return null

func key(code: Key, pressed: bool) -> void:
	var e := InputEventKey.new()
	e.keycode = code
	e.physical_keycode = code
	e.pressed = pressed
	Input.parse_input_event(e)

func tap(code: Key) -> void:
	key(code, true)
	await frames(2)
	key(code, false)
	await frames(1)

func click(at: Vector2) -> void:
	for pressed in [true, false]:
		var e := InputEventMouseButton.new()
		e.button_index = MOUSE_BUTTON_LEFT
		e.pressed = pressed
		e.position = at
		e.global_position = at
		Input.parse_input_event(e)
		await frames(2)

func find_button(node: Node, text: String) -> Button:
	if node is Button and node.visible and (str(node.text).contains(text) or str(node.get_meta("label", "")).contains(text)): return node
	for child in node.get_children():
		var found := find_button(child, text)
		if found != null: return found
	return null

## A real mouse click on the button whose text contains `text`, aimed through the
## viewport's screen transform, so it lands at any window size.
func click_button(text: String) -> void:
	var b := find_button(root, text)
	if b == null:
		note("button_missing", {"text": text})
		return
	var at: Vector2 = b.get_viewport().get_screen_transform() * b.get_global_rect().get_center()
	note("click", {"button": text, "window_xy": [at.x, at.y]})
	await click(at)

func walk_base(x: float, z: float, hold: float, cap_s: float = 30.0) -> void:
	var goal := game.base_map.to_world(x, z, BaseMap.PLAYER_Y)
	note("move_target", {"layout": [x, z]})
	game.player.set_move_target(goal)
	var n := 0
	while n < int(cap_s * 30) and Vector2(game.player.global_position.x - goal.x, game.player.global_position.z - goal.z).length() > 0.6:
		await frames(1)
		n += 1
	game.player.clear_move_target()
	await seconds(hold)

func nearest_enemy() -> Enemy:
	var best: Enemy = null
	var best_d := INF
	for node in game.get_tree().get_nodes_in_group("enemies"):
		var e := node as Enemy
		if not is_instance_valid(e) or e.health <= 0: continue
		var d := e.global_position.distance_to(game.player.global_position)
		if d < best_d:
			best_d = d
			best = e
	return best

## Fight with the left-click path for `limit` seconds. `dodge` = sidestep a
## telegraphed normal attack the way AiDriver does; off for the death clip.
func fight(limit: float, dodge: bool) -> void:
	var n := 0
	while n < int(limit * 30) and not game.in_base and game.player.hp > 0:
		if game.modal == "build" and not game.build_offers.is_empty():
			await seconds(2.5)  # hold the three-choice screen so it is readable
			note("choose_build", {"id": game.build_offers[0].id})
			game.choose_build(game.build_offers[0].id)
		var target := nearest_enemy()
		var threat := Vector3.ZERO
		if dodge:
			for node in game.get_tree().get_nodes_in_group("enemies"):
				var e := node as Enemy
				if is_instance_valid(e) and e.preparing_attack and not e.elite and e.threatens(game.player.global_position):
					threat += e.attack_direction.cross(Vector3.UP)
		if threat.length_squared() > 0.0001:
			game.player.set_move_target(game.player.global_position + threat.normalized() * 4.0)
		elif is_instance_valid(target):
			if game.player.is_target_in_range(target):
				game.player.clear_move_target()
				game.player.attack(target)
			else:
				game.player.set_move_target(target.global_position)
		await frames(1)
		n += 1

func run() -> void:
	var args := OS.get_cmdline_user_args()
	clip = args[0] if args.size() > 0 else "warehouse"
	var seed := int(args[1]) if args.size() > 1 else 0
	rig = load("res://game/main.tscn").instantiate()
	rig.persist_sessions = false
	root.add_child(rig)
	await frames(20)
	game = find_game(rig)
	if seed: game.fixed_map_seed = seed  # same map and spawns on every take
	note("start", {"clip": clip, "seed": seed, "engine": Engine.get_version_info().string})
	match clip:
		"warehouse": await warehouse()
		"hall": await hall()
		"combat": await combat()
		"death": await death()
		"extract": await extract()
	note("end")
	var f := FileAccess.open("user://%s-inputs.jsonl" % clip, FileAccess.WRITE)
	if f != null: f.store_string("\n".join(log_lines) + "\n")
	game.queue_free()
	await create_timer(0.3).timeout
	quit()

## Base music, then the four warehouse events: lights on bank by bank, hatches,
## shelves rising, and lights off after walking out (record_warehouse_reveal.gd's route).
func warehouse() -> void:
	game.player.teleport(game.base_map.to_world(8.0, -26.0, BaseMap.PLAYER_Y))
	game.camera.global_position = game.camera_target() + GameManager.CAMERA_OFFSET
	note("setup_teleport", {"layout": [8.0, -26.0], "why": "start beside the warehouse door instead of a 26 s hall walk"})
	await seconds(2.0)
	await walk_base(-4.0, -26.0, 1.7)
	await walk_base(-44.0, -26.0, 1.0)
	await walk_base(-52.0, -26.0, 2.5)
	await walk_base(8.0, -26.0, 3.0)

## The base hall with its music: from the arrival point across the floor logo to
## the dispatch console, then on toward the warehouse terminal. No setup teleport.
func hall() -> void:
	await seconds(1.5)
	for id in ["dispatch", "stash"]:
		var goal: Vector3 = game.base_map.station(id).position
		note("move_target", {"station": id})
		game.player.set_move_target(goal)
		var n := 0
		while n < 30 * 30 and Vector2(game.player.global_position.x - goal.x, game.player.global_position.z - goal.z).length() > 1.2:
			await frames(1)
			n += 1
		game.player.clear_move_target()
		await seconds(1.0)

## Field music and Lappland's states: WASD walking in four directions (facing
## follows input), then fighting with combo, sword wave and hurt; Esc pause
## freezes the field and the music in place, Esc resumes.
func combat() -> void:
	note("start_contract", {"region": "city", "how": "GameManager.start_contract, the call the dispatch console makes"})
	await game.start_contract("city")
	await seconds(1.5)
	for k in [KEY_D, KEY_S, KEY_A, KEY_W]:
		note("hold_key", {"key": OS.get_keycode_string(k), "s": 0.8})
		key(k, true)
		await seconds(0.8)
		key(k, false)
		await seconds(0.3)
	await fight(28.0, true)
	note("tap", {"key": "Escape"})
	await tap(KEY_ESCAPE)
	await seconds(4.0)
	note("tap", {"key": "Escape"})
	await tap(KEY_ESCAPE)
	await fight(8.0, true)

## A real loss: from the city's 30|31 camp (unlocked in memory first, as reaching
## floor 30 would), a real mouse click on 继续 enters floor 31, where the hidden
## danger is D = 3.5 x 30. Lappland fights without dodging or drinking until she
## is killed; the field track stops, STING-FAIL plays once, the KIA settlement shows.
func death() -> void:
	game.base.unlock_camp("city", 30)
	note("setup_unlock_camp", {"region": "city", "depth": 30, "why": "stands in for walking floors 1-30"})
	note("start_contract", {"region": "city", "start_camp": 30})
	await game.start_contract("city", 30)
	await seconds(2.0)
	await click_button("继续")
	var n := 0
	while game.transitioning and n < 300:
		await frames(1)
		n += 1
	await seconds(1.0)
	await fight(150.0, false)
	note("hp_zero_or_timeout", {"hp": game.player.hp, "in_base": game.in_base})
	await seconds(13.0)

## A camp start (the camp unlock is set in memory first, as reaching floor 10
## would): the camp screen, then a real mouse click on the green 撤离 button;
## STING-EXTRACT plays once over the 行动结束 settlement.
func extract() -> void:
	game.base.unlock_camp("mine", 10)
	note("setup_unlock_camp", {"region": "mine", "depth": 10, "why": "stands in for walking floors 1-10"})
	note("start_contract", {"region": "mine", "start_camp": 10})
	await game.start_contract("mine", 10)
	await seconds(3.0)
	await click_button("撤离")
	await seconds(8.0)
