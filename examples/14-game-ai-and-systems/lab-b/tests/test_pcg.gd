extends SceneTree

var failures := 0

func _initialize() -> void:
	call_deferred("run")

func check(ok: bool, label: String) -> void:
	print("PASS " if ok else "FAIL ", label)
	if not ok:
		failures += 1

func key(code: Key, pressed: bool) -> void:
	var event := InputEventKey.new()
	event.physical_keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)

func run() -> void:
	var Gen = load("res://pcg/level_generator.gd")
	var Val = load("res://pcg/level_validator.gd")
	var gen = Gen.new()
	var val = Val.new()

	# --- Determinism: seed 7 twice ---
	var a: Array = gen.generate(7, 30)
	var b: Array = gen.generate(7, 30)
	check(a == b, "seed 7 twice gives identical data")

	# --- Seeds 1..200 ---
	var passing: int = 0
	var failing_seeds: Array = []
	for s in range(1, 201):
		var level: Array = gen.generate(s, 40)
		var result: Dictionary = val.validate(level)
		if result.is_empty():
			passing += 1
		else:
			failing_seeds.append(s)

	var pct := float(passing) / 200.0 * 100.0
	print("PASS_RATE %.1f%% (%d/200 pass)" % [pct, passing])
	print("FAILING_SEEDS ", failing_seeds)
	check(passing > 0 and passing < 200, "mix of passing and failing levels (not trivially all-pass or all-fail)")

	# --- Hand-made: gap wider than MAX_JUMP_RANGE_TILES (8) ---
	# 3 solid cols + 9-column gap + 3 solid cols → gap_dist = 12 - 2 = 10 > 8
	var wide_gap: Array = []
	for _i in 3:
		wide_gap.append(5)
	for _i in 9:
		wide_gap.append(-1)
	for _i in 3:
		wide_gap.append(5)
	var r1: Dictionary = val.validate(wide_gap)
	check(not r1.is_empty(), "wide-gap level is rejected")
	if not r1.is_empty():
		print("  wide-gap: col=%d  reason=%s" % [r1["col"], r1["reason"]])

	# --- Hand-made: step higher than MAX_JUMP_HEIGHT_TILES (2) ---
	# ground at row 8 then row 1 → step_up = 8 - 1 = 7 > 2
	var tall_step: Array = []
	for _i in 5:
		tall_step.append(8)   # low ground
	for _i in 5:
		tall_step.append(1)   # very high ground
	var r2: Dictionary = val.validate(tall_step)
	check(not r2.is_empty(), "tall-step level is rejected")
	if not r2.is_empty():
		print("  tall-step: col=%d  reason=%s" % [r2["col"], r2["reason"]])

	# --- Runtime TileMapLayer write + player landing ---
	var demo: Node = load("res://world.tscn").instantiate()
	root.add_child(demo)
	var ground: TileMapLayer = demo.get_node("Ground")
	var player: CharacterBody2D = demo.get_node("Player")

	# Build a flat level of width 20 at tile row 6 and write it to Ground.
	var ground_row := 6
	var flat_width := 20
	var flat_level: Array = []
	for _i in flat_width:
		flat_level.append(ground_row)

	ground.clear()
	for col in flat_level.size():
		if flat_level[col] != -1:
			# source_id=0 (the single TileSetAtlasSource), atlas tile (0,0)
			ground.set_cell(Vector2i(col, flat_level[col]), 0, Vector2i(0, 0))

	# Place player above the first column of the generated floor.
	# Tile top edge = ground_row * 16.  Player half-height = 7.  Drop from above.
	var tile_px := 16
	player.position = Vector2(float(tile_px / 2), float(ground_row * tile_px) - 60.0)
	player.velocity = Vector2.ZERO

	# Allow physics to settle (floor physics updates on next frame).
	await create_timer(1.2).timeout

	check(player.is_on_floor(), "player rests on generated Ground tile (is_on_floor)")

	demo.queue_free()
	await process_frame
	print("failures=", failures)
	quit(1 if failures else 0)
