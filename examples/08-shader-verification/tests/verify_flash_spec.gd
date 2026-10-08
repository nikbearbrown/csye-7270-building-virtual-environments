extends SceneTree
## Black-box timing evidence for CLAUDE.md failure-flash rule 1.
## This deliberately does not read retry_remaining or reproduce the player's
## frame counter. Time is accumulated only from process-frame deltas observed
## after a real fall begins.

const Game = preload("res://game/session.gd")
const FADE_SECONDS := 0.55
var failures := 0


class Sampler extends Node:
	## A high priority value makes this run after the game and player _process().
	var game: Node2D
	var material: ShaderMaterial
	var rows: Array[Dictionary] = []
	var frame := 0
	var failure_time := 0.0
	var was_dying := false

	func _ready() -> void:
		process_priority = 1000

	func _process(delta: float) -> void:
		frame += 1
		var dying: bool = game.state == Game.State.DYING
		if dying:
			if not was_dying:
				failure_time = 0.0
			failure_time += delta
		rows.append({
			"frame": frame,
			"delta": delta,
			"state": game.state,
			"failure_time": failure_time if dying else 0.0,
			"flash": float(material.get_shader_parameter("flash_amount")),
		})
		was_dying = dying


func check(id: String, passed: bool, observed) -> void:
	print(JSON.stringify({"id": id, "status": "PASS" if passed else "FAIL", "observed": observed}))
	if not passed:
		failures += 1


func _initialize() -> void:
	run.call_deferred()


func run() -> void:
	var game: Node2D = Game.new()
	game.test_mode = true
	root.add_child(game)
	await process_frame
	game.start_session()
	for i in range(4):
		await process_frame

	var material := game.player.material as ShaderMaterial
	check("Clawd carries a ShaderMaterial", material != null, str(material))
	if material == null:
		game.queue_free()
		await process_frame
		print("VERIFY_FLASH_SPEC failures=", failures)
		quit(1)
		return

	var sampler := Sampler.new()
	sampler.game = game
	sampler.material = material
	root.add_child(sampler)
	await process_frame
	sampler.rows.clear()

	# Cause a real failure; session.gd detects this in its regular physics loop.
	game.player.position.y = float(game.level.fall_y) + 5.0
	var guard := 0
	while guard < 500:
		await process_frame
		guard += 1
		var saw_dying := sampler.rows.any(func(row): return row.state == Game.State.DYING)
		if saw_dying and sampler.rows[-1].state == Game.State.PLAYING:
			break

	var dying: Array[Dictionary] = sampler.rows.filter(func(row): return row.state == Game.State.DYING)
	var after: Array[Dictionary] = []
	if not dying.is_empty():
		after = sampler.rows.filter(func(row): return row.state == Game.State.PLAYING and row.frame > dying[-1].frame)

	var physics_tick := 1.0 / float(Engine.physics_ticks_per_second)
	var max_error := 0.0
	var worst := {}
	var within_tolerance := not dying.is_empty()
	for row in dying:
		var expected := clampf(1.0 - row.failure_time / FADE_SECONDS, 0.0, 1.0)
		# Human review: a correct fade can trail the ideal line by one physics
		# tick (the countdown moves in ticks) plus one frame (the failure is
		# seen inside a frame). max(delta, tick) failed the known-good
		# Chapter 6 driver at 144 fps (error 0.0369 > 0.0303).
		var tolerance: float = (row.delta + physics_tick) / FADE_SECONDS
		var error: float = absf(row.flash - expected)
		if error > max_error:
			max_error = error
			worst = {"frame": row.frame, "t": row.failure_time, "flash": row.flash, "expected": expected, "error": error, "tolerance": tolerance}
		if error > tolerance + 0.0001:
			within_tolerance = false

	var summary := {
		"frames_in_failure": dying.size(),
		"accumulated_game_time": dying[-1].failure_time if not dying.is_empty() else 0.0,
		"first_flash": dying[0].flash if not dying.is_empty() else null,
		"last_flash_before_retry": dying[-1].flash if not dying.is_empty() else null,
		"first_flash_after_retry": after[0].flash if not after.is_empty() else null,
		"max_error": max_error,
		"worst_sample": worst,
	}
	print("FLASH_SPEC_SAMPLES: ", JSON.stringify(summary))
	check("real fall produced failure samples", not dying.is_empty(), dying.size())
	check("time-linear flash stays within one frame plus one physics tick", within_tolerance, worst)
	check("first failure frame flash >= 0.96", not dying.is_empty() and dying[0].flash >= 0.96, dying[0].flash if not dying.is_empty() else null)
	check("last failure frame flash <= 0.07", not dying.is_empty() and dying[-1].flash <= 0.07, dying[-1].flash if not dying.is_empty() else null)
	check("flash is 0 on first frame after retry", not after.is_empty() and is_zero_approx(after[0].flash), after[0].flash if not after.is_empty() else null)

	sampler.queue_free()
	game.queue_free()
	await process_frame
	print("VERIFY_FLASH_SPEC failures=", failures)
	quit(1 if failures else 0)
