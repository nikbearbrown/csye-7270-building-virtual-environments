extends SceneTree

const DEMO_SCENE := preload("res://Demo.tscn")
const SWORD_PATH := ^"Player/BodyPivot/WeaponPivot/Offset/Sword"
const STATE_MACHINE_PATH := ^"Player/StateMachine"
const MAX_FRAMES := 240
const EPSILON := 0.001

# re-pinned 2026-09-27 after approved changes: hitbox window keyed in the animation; every swing restarts
const SINGLE_HITBOX_ON_FRAME := 1
const SINGLE_HITBOX_OFF_FRAME := 19
const SINGLE_BUFFER_OPEN_FRAME := 13
const SINGLE_READY_FRAME := 31
const SINGLE_IDLE_FRAME := 55
const COMBO_START_FRAMES := [1, 31, 61]
const COMBO_START_ANIMATIONS := [&"attack_fast", &"attack_fast", &"attack_medium"]
const COMBO_START_POSITIONS := [0.0, 0.0, 0.0]
const COMBO_START_ROTATIONS := [-79.999992, 74.999992, 95.0]
const COMBO_ROTATION_TRAVEL := [174.999985, 289.749779, 195.0]
const EARLY_TAP_CHAINS := false

var failures := 0
var checks := 0

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	root.size = Vector2i(1280, 720)
	var single := await run_scenario(&"single")
	var combo := await run_scenario(&"combo")
	var early := await run_scenario(&"early")
	print("TIMING")
	check_equal(first_frame(single.records, func(row): return row.monitoring), SINGLE_HITBOX_ON_FRAME, "single: hitbox turns on at frame %d" % SINGLE_HITBOX_ON_FRAME)
	check_equal(first_frame(single.records, func(row): return row.frame > SINGLE_HITBOX_ON_FRAME and not row.monitoring), SINGLE_HITBOX_OFF_FRAME, "single: hitbox turns off at frame %d" % SINGLE_HITBOX_OFF_FRAME)
	check_equal(first_frame(single.records, func(row): return row.input_state == 1), SINGLE_BUFFER_OPEN_FRAME, "single: combo buffer opens at frame %d" % SINGLE_BUFFER_OPEN_FRAME)
	check_equal(first_frame(single.records, func(row): return row.ready), SINGLE_READY_FRAME, "single: ready_for_next_attack at frame %d" % SINGLE_READY_FRAME)
	check_equal(first_frame(single.records, func(row): return row.frame > 0 and row.player_state == &"Idle"), SINGLE_IDLE_FRAME, "single: player returns to Idle at frame %d" % SINGLE_IDLE_FRAME)
	check_equal(combo.swings.size(), 3, "combo: exactly three swing starts were observed")
	for index in mini(combo.swings.size(), 3):
		var swing: Dictionary = combo.swings[index]
		var details := "combo: swing %d starts frame=%d animation=%s position=%.6f rotation=%.6f" % [index + 1, COMBO_START_FRAMES[index], COMBO_START_ANIMATIONS[index], COMBO_START_POSITIONS[index], COMBO_START_ROTATIONS[index]]
		check(swing.frame == COMBO_START_FRAMES[index] and swing.animation == COMBO_START_ANIMATIONS[index] and is_equal_approx(swing.position, COMBO_START_POSITIONS[index]) and is_equal_approx(swing.rotation, COMBO_START_ROTATIONS[index]), details)
		check_float(combo.travel[index], COMBO_ROTATION_TRAVEL[index], "combo: swing %d rotation travel is %.6f degrees" % [index + 1, COMBO_ROTATION_TRAVEL[index]])
	check(early.chained == EARLY_TAP_CHAINS, "early: tap five frames into swing chains = %s" % EARLY_TAP_CHAINS)
	print("INVARIANT")
	var all_records: Array = single.records + combo.records + combo.next_records + early.records
	check(all_records.all(func(row): return not row.monitoring or row.player_state == &"Attack"), "hitbox is never on outside Attack")
	check(all_records.all(func(row): return row.player_state != &"Idle" or (not row.visible and not row.monitoring)), "in Idle the sword is hidden and not monitoring")
	check(combo.swing_had_hitbox.all(func(value): return value), "every combo swing has at least one hitbox-on frame")
	check(combo.third_animation == &"attack_medium" and combo.third_damage == 3, "swing 3 plays attack_medium with damage 3")
	check(combo.maximum_combo == 3, "a fourth tap does not start a fourth swing")
	check(combo.player_transitions == [&"Attack", &"Idle"] and combo.maximum_stack_size == 2 and combo.final_stack_size == 1, "whole combo is one push and one pop of Attack")
	check(combo.next_combo == 1, "next attack after combo starts at combo 1")
	print("RESULT %d checks; %d failures" % [checks, failures])
	quit(1 if failures else 0)

func run_scenario(kind: StringName) -> Dictionary:
	var demo: Node = DEMO_SCENE.instantiate()
	root.add_child(demo)
	await process_frame
	var sword: Node = demo.get_node(SWORD_PATH)
	var machine: Node = demo.get_node(STATE_MACHINE_PATH)
	var records: Array[Dictionary] = []
	var swings: Array[Dictionary] = []
	var frame := 0
	var previous_combo: int = sword.combo_count
	var player_transitions: Array[StringName] = []
	var previous_player_state: StringName = machine.current_state.name
	var maximum_stack_size: int = machine.states_stack.size()
	var maximum_combo := 0
	var third_animation: StringName = &""
	var third_damage = null
	press_f(true)
	records.append(snapshot(frame, sword, machine))
	while frame < MAX_FRAMES:
		await process_frame
		frame += 1
		if frame == 1:
			press_f(false)
		var row := snapshot(frame, sword, machine)
		records.append(row)
		maximum_stack_size = maxi(maximum_stack_size, machine.states_stack.size())
		maximum_combo = maxi(maximum_combo, sword.combo_count)
		if row.player_state != previous_player_state:
			player_transitions.append(row.player_state)
			previous_player_state = row.player_state
		if row.combo_count > previous_combo:
			swings.append(row.duplicate())
			if row.combo_count == 3:
				third_animation = row.animation
				third_damage = sword.attack_current.get("damage")
		previous_combo = row.combo_count
		if kind == &"combo" and not swings.is_empty() and frame == swings[-1].frame + 20:
			press_f(true)
		if kind == &"combo" and not swings.is_empty() and frame == swings[-1].frame + 21:
			press_f(false)
		if kind == &"early" and not swings.is_empty() and frame == swings[0].frame + 5:
			press_f(true)
		if kind == &"early" and not swings.is_empty() and frame == swings[0].frame + 6:
			press_f(false)
		if frame > 2 and row.player_state == &"Idle":
			break
	var travel := rotation_travel_by_swing(records, swings)
	var swing_had_hitbox := hitbox_by_swing(records, swings)
	var next_records: Array[Dictionary] = []
	var next_combo := -1
	if kind == &"combo":
		press_f(true)
		next_records.append(snapshot(0, sword, machine))
		for next_frame in range(1, MAX_FRAMES + 1):
			await process_frame
			if next_frame == 1:
				press_f(false)
			var next_row := snapshot(next_frame, sword, machine)
			next_records.append(next_row)
			if next_combo == -1 and next_row.combo_count > 0:
				next_combo = next_row.combo_count
			if next_frame > 2 and next_row.player_state == &"Idle":
				break
	var result := {
		"records": records, "swings": swings, "travel": travel,
		"swing_had_hitbox": swing_had_hitbox, "chained": swings.size() > 1,
		"maximum_combo": maximum_combo, "third_animation": third_animation,
		"third_damage": third_damage, "player_transitions": player_transitions,
		"maximum_stack_size": maximum_stack_size, "final_stack_size": machine.states_stack.size(),
		"next_records": next_records, "next_combo": next_combo,
	}
	demo.queue_free()
	await process_frame
	return result

func snapshot(frame: int, sword: Node, machine: Node) -> Dictionary:
	var animation_player: AnimationPlayer = sword.get_node(^"AnimationPlayer")
	var animation: StringName = animation_player.current_animation
	return {
		"frame": frame, "animation": animation,
		"position": 0.0 if animation.is_empty() else animation_player.current_animation_position,
		"visible": sword.visible, "monitoring": sword.monitoring,
		"rotation": sword.rotation_degrees, "input_state": sword.attack_input_state,
		"ready": sword.ready_for_next_attack, "combo_count": sword.combo_count,
		"player_state": StringName(machine.current_state.name),
	}

func press_f(pressed: bool) -> void:
	var event := InputEventKey.new()
	event.keycode = KEY_F
	event.pressed = pressed
	Input.parse_input_event(event)

func first_frame(records: Array, predicate: Callable) -> int:
	for row in records:
		if predicate.call(row):
			return row.frame
	return -1

func rotation_travel_by_swing(records: Array[Dictionary], swings: Array[Dictionary]) -> Array[float]:
	var travel: Array[float] = []
	for _swing in swings:
		travel.append(0.0)
	for index in range(1, records.size()):
		var previous := records[index - 1]
		var current := records[index]
		if current.combo_count > 0 and current.combo_count == previous.combo_count:
			travel[current.combo_count - 1] += absf(current.rotation - previous.rotation)
	return travel

func hitbox_by_swing(records: Array[Dictionary], swings: Array[Dictionary]) -> Array[bool]:
	var result: Array[bool] = []
	for _swing in swings:
		result.append(false)
	for row in records:
		if row.combo_count > 0 and row.combo_count <= result.size() and row.monitoring:
			result[row.combo_count - 1] = true
	return result

func check(ok: bool, label: String) -> void:
	checks += 1
	if not ok:
		failures += 1
	print(("PASS " if ok else "FAIL ") + label)

func check_equal(actual: int, expected: int, label: String) -> void:
	check(actual == expected, "%s (actual %d)" % [label, actual])

func check_float(actual: float, expected: float, label: String) -> void:
	check(absf(actual - expected) <= EPSILON, "%s (actual %.6f)" % [label, actual])
