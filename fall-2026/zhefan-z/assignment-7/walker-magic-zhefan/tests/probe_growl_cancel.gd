extends SceneTree
## Assignment 7 probe, not a test (prints, asserts nothing): does a fireball cast during GROWL land during GROWL? The
## player stands at x 700; the wolf patrols in from x 860 (walking left) and first sees her at dx <= 120 (SIGHT_X,
## wolf.gd:19) on tick g0, found by a dry run. For each cast offset k = 0..30 after g0 (the click is a real event through
## Input.parse_input_event, aimed at the wolf's body centre at that moment, as a player would aim), one fresh run of
## the main scene reports the cast tick (cast_fired), the hit tick (wolf HP drops), the phase the wolf was in when hit,
## its state on the hit tick and the travel ticks. Ticks are counted from the scene's first physics tick.
## From fall-2026/zhefan-z/assignment-7/:
##   ./scripts/run-test.sh probe_growl_cancel.gd 60

const GROUND_TOP := 327.0


class Sampler extends Node:
	var ticks := 0
	var rows: Array[Dictionary] = []
	var wolf: Wolf

	func _init() -> void:
		process_physics_priority = 1000

	func _physics_process(_delta: float) -> void:
		if is_instance_valid(wolf):
			rows.append({"s": Wolf.State.keys()[wolf.state], "hp": wolf.hp, "x": wolf.global_position.x})
		else:
			rows.append({"s": "FREED", "hp": 0, "x": 0.0})
		ticks += 1


var main: Node


func _initialize() -> void:
	call_deferred("run")


func click(screen: Vector2, pressed: bool) -> void:
	var ev := InputEventMouseButton.new()
	ev.button_index = MOUSE_BUTTON_LEFT
	ev.pressed = pressed
	ev.position = screen
	ev.global_position = screen
	Input.parse_input_event(ev)


func one(k: int) -> Dictionary:   # k < 0: dry run, no cast
	main = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	var player: Player = main.player
	var wolf: Wolf = main.get_node("Level/Wolf")
	player.global_position = Vector2(700, GROUND_TOP)
	wolf.global_position = Vector2(860, GROUND_TOP)
	var s := Sampler.new()
	s.wolf = wolf
	root.add_child(s)
	var cast := {"tick": -1, "origin": Vector2.ZERO, "dir": Vector2.ZERO}
	player.cast_fired.connect(func(o: Vector2, d: Vector2) -> void:
		if cast.tick < 0:
			cast.tick = s.ticks
			cast.origin = o
			cast.dir = d)
	var screen := Vector2.ZERO
	var sent_at := -1
	while s.ticks < 200:
		if s.ticks == k and sent_at < 0:
			var aim := wolf.global_position + Vector2(8 * wolf.facing, -14)   # body centre (wolf.tscn:27-29)
			screen = aim - Vector2(main.camera.get_screen_center_position().x - 320.0, 0.0)
			var motion := InputEventMouseMotion.new()
			motion.position = screen
			motion.global_position = screen
			Input.parse_input_event(motion)
			click(screen, true)
			sent_at = s.ticks
		elif sent_at >= 0 and s.ticks >= sent_at + 4:
			click(screen, false)
		await process_frame
	click(screen, false)
	var hit := -1
	for i in range(1, s.rows.size()):
		if s.rows[i].hp < s.rows[i - 1].hp:
			hit = i
			break
	var g0 := -1
	for i in s.rows.size():
		if s.rows[i].s == "GROWL":
			g0 = i
			break
	var out := {"click_before_tick": sent_at, "cast_tick": cast.tick, "hit_tick": hit,
		"phase_when_hit": s.rows[hit - 1].s if hit > 0 else "-", "state_on_hit_tick": s.rows[hit].s if hit > 0 else "-",
		"travel_ticks": hit - cast.tick if hit > 0 else -1, "first_growl_tick": g0,
		"cast_after_growl_start": cast.tick - g0 if cast.tick >= 0 else -1,
		"wolf_x_at_sight": snappedf(s.rows[g0].x, 0.01) if g0 >= 0 else -1, "wolf_x_at_hit": snappedf(s.rows[hit].x, 0.01) if hit > 0 else -1,
		"wolf_states": _runs(s.rows)}
	main.queue_free()
	s.queue_free()
	await process_frame
	await process_frame
	return out


func _runs(rows: Array) -> Array:
	var out := []
	for r: Dictionary in rows:
		if out.is_empty() or out.back()[0] != r.s:
			out.append([r.s, 0])
		out.back()[1] += 1
	return out.map(func(r: Array) -> String: return "%s x%d" % r)


func run() -> void:
	await process_frame
	var dry: Dictionary = await one(-1)
	var g0: int = dry.first_growl_tick
	print(JSON.stringify({"dry_run": dry}))
	for k in range(0, 31):
		print(JSON.stringify(await one(g0 + k)))
	quit(0)
