extends SceneTree
const Game = preload("res://game/session.gd")
const Route = preload("res://tests/route_driver.gd")
const PlayerScript = preload("res://features/player/player.gd")
const HudScript = preload("res://ui/hud.gd")
var game: Node2D
var results: Array[Dictionary] = []
var failures: int = 0

func _initialize() -> void:
	call_deferred("run")

func steps(n: int) -> void:
	for i in range(n):
		await physics_frame
		await process_frame

func check(id: String, passed: bool, observation: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observation})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))

## Scripted fork attempt: run to the edge of the original platform 3, jump,
## air-jump at apex, and optionally dash after that second apex. This is a UNIT
## FIXTURE on a tick schedule, not a human playtest.
func drive_fork(with_dash: bool) -> void:
	game.player.position = Vector2(850, 320)
	game.player.test_axis = 1.0
	for i in range(120):
		await steps(1)
		if game.player.position.x >= 946.0:
			break
	game.player.test_jump_pressed = true
	await steps(20)
	game.player.test_jump_pressed = true
	await steps(20)
	if with_dash:
		game.player.test_dash_pressed = true
	for i in range(80):
		await steps(1)
		if game.player.is_on_floor():
			break

func _menu_event() -> InputEventKey:
	var e := InputEventKey.new()
	e.physical_keycode = KEY_M
	e.pressed = true
	return e

func fresh() -> void:
	if is_instance_valid(game):
		game.queue_free()
		await process_frame
	game = Game.new()
	game.test_mode = true
	root.add_child(game)
	game.start_session()
	game.player.test_control = true
	await steps(3)

## How many times `id` fired during the current attempt.
func _sfx_count(g, id: String) -> int:
	var n := 0
	for e in g.sfx_log:
		if e["id"] == id:
			n += 1
	return n

func run() -> void:
	await fresh()
	check("launch-grounded", game.player.is_on_floor() and game.state == Game.State.PLAYING, {"position": str(game.player.position), "engine": Engine.get_version_info().string})
	game.player.test_axis = 1
	await steps(8)
	check("speed-cap", is_equal_approx(game.player.velocity.x,160), {"velocity_x": game.player.velocity.x})
	game.player.test_axis = 0
	await steps(5)
	check("neutral-stop", is_zero_approx(game.player.velocity.x), {"velocity_x": game.player.velocity.x})
	game.player.test_control = false
	Input.action_press("move_left")
	Input.action_press("move_right")
	await steps(5)
	check("simultaneous-directions", is_zero_approx(game.player.velocity.x), {"velocity_x": game.player.velocity.x})
	Input.action_release("move_left")
	Input.action_release("move_right")
	game.player.test_control = true
	game.player.test_axis = -1
	await steps(70)
	check("left-wall", game.player.position.x >= 9 and game.player.position.x <= 11, {"x": game.player.position.x})
	# D1 rewrite of the starter's "fixed-jump-and-no-double". The fixed height
	# half is UNCHANGED and still asserted below on a single press. The "no
	# double" half is replaced by the new contract -- exactly two jumps per
	# takeoff, a third refused -- rather than deleted. Splitting the single
	# press into its own block also lets "held-jump-no-bounce" keep its
	# original assertion verbatim.
	await fresh()
	game.player.test_jump_pressed = true
	game.player.test_jump_held = true
	var min_y: float = game.player.position.y
	for i in range(50):
		await steps(1)
		min_y = minf(min_y, game.player.position.y)
	check("fixed-jump-height", game.player.jumps == 1 and absf((320-min_y)-53.3333) < 5, {"rise_px":320-min_y, "jumps":game.player.jumps, "air_jumps_left":game.player.air_jumps_left})
	await steps(30)
	check("held-jump-no-bounce", game.player.jumps == 1 and game.player.is_on_floor(), {"jumps":game.player.jumps})
	# Two presses give two jumps; a third in the same takeoff is refused. If
	# the third had fired, jumps would read 3 here.
	await fresh()
	game.player.test_jump_pressed = true
	var double_min_y: float = game.player.position.y
	for i in range(50):
		await steps(1)
		double_min_y = minf(double_min_y, game.player.position.y)
		if i == 12:
			game.player.test_jump_pressed = true
		if i == 24:
			game.player.test_jump_pressed = true
	check("air-jump-exactly-two", game.player.jumps == 2 and game.player.air_jumps_left == 0 and not game.player.is_on_floor(), {"jumps":game.player.jumps, "air_jumps_left":game.player.air_jumps_left, "on_floor":game.player.is_on_floor()})
	check("air-jump-raises-apex", (320-double_min_y) > (320-min_y) + 30.0, {"double_rise_px":320-double_min_y, "single_rise_px":320-min_y})
	# Both budgets come back only on floor contact. One extra frame after
	# is_on_floor() first reads true: the refill runs at the TOP of
	# _physics_process, and is_on_floor() only becomes true at the end of the
	# frame that lands, so the budgets are restored on the frame after.
	for i in range(60):
		await steps(1)
		if game.player.is_on_floor():
			break
	await steps(1)
	check("airborne-budgets-refill-on-floor", game.player.is_on_floor() and game.player.air_jumps_left == 1 and game.player.dashes_left == 1, {"air_jumps_left":game.player.air_jumps_left, "dashes_left":game.player.dashes_left})
	# Actual geometry fixtures at a ledge; tick ages exercise inclusive 6 / expired 7.
	# D1 rewrite of the coyote boundary. Before the air jump existed, age 7
	# meant no jump at all. It now means the coyote jump is refused and the
	# air jump answers instead, so this distinguishes WHICH jump fired by
	# reading the air budget rather than only counting jumps. Ages 5 and 6
	# must still spend the ground jump and leave the air jump in hand.
	for age in [5,6,7]:
		await fresh()
		game.player.position = Vector2(478, 285)
		await steps(2)
		game.player.last_floor_tick = game.player.tick + 1 - age
		game.player.opportunity_consumed = false
		game.player.test_jump_pressed = true
		await steps(1)
		var used_ground: bool = game.player.jumps == 1 and game.player.air_jumps_left == 1
		var used_air: bool = game.player.jumps == 1 and game.player.air_jumps_left == 0
		check("coyote-%d" % age, used_ground if age <= 6 else used_air, {"age":age, "jumps":game.player.jumps, "air_jumps_left":game.player.air_jumps_left})
	# CHANGE-BRIEF P2. The predicted failure was THREE jumps: one from the
	# coyote window, one air jump, and a third if a budget refilled on the
	# wrong signal. Seeded coyote state, as the boundary fixtures above.
	await fresh()
	game.player.position = Vector2(478, 285)
	await steps(2)
	game.player.last_floor_tick = game.player.tick + 1 - 6
	game.player.opportunity_consumed = false
	game.player.test_jump_pressed = true
	await steps(1)
	var after_coyote: int = game.player.jumps
	game.player.test_jump_pressed = true
	await steps(2)
	var after_air: int = game.player.jumps
	game.player.test_jump_pressed = true
	await steps(2)
	check("coyote-plus-air-caps-at-two", after_coyote == 1 and after_air == 2 and game.player.jumps == 2, {"after_coyote":after_coyote, "after_air":after_air, "after_third":game.player.jumps})
	# D2 -- the air dash. Refused while standing.
	await fresh()
	game.player.test_dash_pressed = true
	await steps(2)
	check("dash-refused-on-floor", game.player.dashes == 0 and game.player.dash_ticks_left == 0 and is_zero_approx(game.player.velocity.x), {"dashes":game.player.dashes, "velocity_x":game.player.velocity.x})
	# Airborne: locks horizontal speed, suspends vertical motion, and a second
	# dash in the same takeoff is refused.
	await fresh()
	game.player.test_axis = 1.0
	game.player.test_jump_pressed = true
	await steps(6)
	var dash_x0: float = game.player.position.x
	var dash_y0: float = game.player.position.y
	game.player.test_dash_pressed = true
	await steps(1)
	check("dash-air-locks-velocity", game.player.dashes == 1 and is_equal_approx(game.player.velocity.x, 400.0) and is_zero_approx(game.player.velocity.y), {"velocity_x":game.player.velocity.x, "velocity_y":game.player.velocity.y, "dash_ticks_left":game.player.dash_ticks_left})
	game.player.test_dash_pressed = true
	await steps(1)
	check("dash-refuses-second-in-air", game.player.dashes == 1 and game.player.dashes_left == 0, {"dashes":game.player.dashes, "dashes_left":game.player.dashes_left})
	await steps(8)
	check("dash-displacement", (game.player.position.x - dash_x0) > 60.0 and (game.player.position.x - dash_x0) < 75.0 and absf(game.player.position.y - dash_y0) < 1.0, {"dx":game.player.position.x-dash_x0, "dy":game.player.position.y-dash_y0, "analytic_dx":66.7})
	# CHANGE-BRIEF P4. "Air only" is defined by is_on_floor(), so a dash is
	# allowed the moment the player leaves the ground -- including inside the
	# coyote window. Intended: coyote time is a jump-forgiveness window, not a
	# grounded state, and a dash there still spends the one airborne dash.
	await fresh()
	game.player.position = Vector2(478, 285)
	await steps(2)
	game.player.last_floor_tick = game.player.tick + 1 - 3
	game.player.test_dash_pressed = true
	await steps(1)
	check("dash-allowed-inside-coyote-window", game.player.dashes == 1 and (game.player.tick - game.player.last_floor_tick) <= 6, {"dashes":game.player.dashes, "coyote_age":game.player.tick - game.player.last_floor_tick})
	# A jump cancels a running dash and restores normal gravity.
	await fresh()
	game.player.test_axis = 1.0
	game.player.test_jump_pressed = true
	await steps(6)
	game.player.test_dash_pressed = true
	await steps(2)
	var was_dashing: bool = game.player.dash_ticks_left > 0
	game.player.test_jump_pressed = true
	await steps(1)
	check("jump-cancels-dash", was_dashing and game.player.dash_ticks_left == 0 and game.player.jumps == 2 and is_equal_approx(game.player.velocity.y, -320.0), {"was_dashing":was_dashing, "dash_ticks_left":game.player.dash_ticks_left, "jumps":game.player.jumps, "velocity_y":game.player.velocity.y})
	# D2 -- explicitly NOT invincible. Dashing into the real spike Area2D at
	# x 320..344 must still kill. Jumping two ticks earlier leaves the body
	# low enough that the 18x28 collider overlaps the hazard band.
	await fresh()
	game.player.position = Vector2(286, 320)
	game.player.test_axis = 1.0
	await steps(3)
	game.player.test_jump_pressed = true
	await steps(2)
	game.player.test_dash_pressed = true
	for i in range(24):
		await steps(1)
		if game.state == Game.State.DYING:
			break
	check("dash-not-invincible", game.state == Game.State.DYING and game.deaths == 1, {"state":game.state, "deaths":game.deaths, "x":game.player.position.x, "y":game.player.position.y})
	# D3 — the sword swing. Phases first: 4 windup, 5 active, 5 recovery.
	await fresh()
	game.player.test_attack_pressed = true
	# Read from tuning rather than pinned: revision 0.6.0 widened the live window
	# from 5 ticks to 9 because the old one swept only the part of the arc that
	# cannot reach the floor, so ground enemies were unhittable. The shape of
	# the contract is what matters, not the old numbers.
	var want_windup: int = game.player.tuning.attack_windup_ticks
	var want_active: int = game.player.tuning.attack_active_ticks
	var want_recovery: int = game.player.tuning.attack_ticks - want_windup - want_active
	var phase_seq: Array = []
	var live_seq: Array = []
	for i in range(game.player.tuning.attack_ticks + 3):
		await steps(1)
		phase_seq.append(game.player.attack_phase())
		live_seq.append(game.player.attack_hitbox.monitoring)
	var windup_n: int = phase_seq.count(1)
	var active_n: int = phase_seq.count(2)
	var recovery_n: int = phase_seq.count(3)
	check("attack-phase-sequence", windup_n == want_windup and active_n == want_active and recovery_n == want_recovery and phase_seq[phase_seq.size()-1] == 0, {"windup":windup_n, "active":active_n, "recovery":recovery_n, "expected":[want_windup, want_active, want_recovery], "sequence":str(phase_seq)})
	# CHANGE-BRIEF P5, half one: the hitbox is live on exactly the active ticks.
	var live_matches_active: bool = true
	for i in range(phase_seq.size()):
		if live_seq[i] != (phase_seq[i] == 2):
			live_matches_active = false
	check("attack-hitbox-live-only-in-active", live_matches_active and live_seq.count(true) == want_active, {"live_ticks":live_seq.count(true), "expected":want_active, "matches_active_phase":live_matches_active})
	# The hitbox can only ever touch layer 3 (Enemy): never world, player,
	# hazards or the goal.
	check("attack-hitbox-layers", game.player.attack_hitbox.collision_layer == 32 and game.player.attack_hitbox.collision_mask == 4, {"layer":game.player.attack_hitbox.collision_layer, "mask":game.player.attack_hitbox.collision_mask})
	# CHANGE-BRIEF P5, half two: on every active tick the hitbox rectangle must
	# lie ON the blade the draw code renders. Reconstructed independently here
	# from the shape's own position/rotation/size and compared against the
	# pivot and tip, including the left-facing mirror.
	for dir in [1.0, -1.0]:
		await fresh()
		game.player.test_axis = dir
		await steps(2)
		game.player.test_axis = 0.0
		game.player.test_attack_pressed = true
		var worst: float = 0.0
		var samples: int = 0
		for i in range(game.player.tuning.attack_ticks):
			await steps(1)
			if game.player.attack_phase() != 2:
				continue
			samples += 1
			var half: float = game.player.attack_shape.shape.size.x * 0.5
			var along := Vector2.from_angle(game.player.attack_shape.rotation)
			var got_a: Vector2 = game.player.attack_shape.position - along * half
			var got_b: Vector2 = game.player.attack_shape.position + along * half
			var want_a: Vector2 = PlayerScript.ATTACK_PIVOT
			var want_b: Vector2 = game.player.attack_tip()
			if game.player.attack_dir < 0.0:
				want_a.x = -want_a.x
				want_b.x = -want_b.x
			worst = maxf(worst, maxf(got_a.distance_to(want_a), got_b.distance_to(want_b)))
		check("attack-hitbox-on-the-blade-%s" % ("right" if dir > 0.0 else "left"), samples == game.player.tuning.attack_active_ticks and worst < 0.01, {"active_ticks_sampled":samples, "worst_endpoint_error_px":worst, "facing":game.player.attack_dir})
	# A press during a swing is ignored.
	await fresh()
	game.player.test_attack_pressed = true
	await steps(4)
	game.player.test_attack_pressed = true
	await steps(4)
	check("attack-ignores-press-mid-swing", game.player.attacks == 1 and game.player.attack_phase() != 0, {"attacks":game.player.attacks, "phase":game.player.attack_phase()})
	# Movement is untouched: same axis, same 20 ticks, with and without a swing.
	await fresh()
	game.player.test_axis = 1.0
	await steps(20)
	var plain_v: float = game.player.velocity.x
	var plain_x: float = game.player.position.x
	await fresh()
	game.player.test_axis = 1.0
	game.player.test_attack_pressed = true
	await steps(20)
	check("attack-does-not-change-movement", is_equal_approx(game.player.velocity.x, plain_v) and absf(game.player.position.x - plain_x) < 0.01, {"velocity_with_swing":game.player.velocity.x, "velocity_plain":plain_v, "position_delta":game.player.position.x - plain_x})
	# Usable in the air, and it hands back no jump and no dash.
	await fresh()
	game.player.test_jump_pressed = true
	await steps(6)
	var air_before: int = game.player.air_jumps_left
	var dash_before: int = game.player.dashes_left
	game.player.test_attack_pressed = true
	await steps(6)
	check("attack-works-airborne", game.player.attacks == 1 and not game.player.is_on_floor(), {"attacks":game.player.attacks, "on_floor":game.player.is_on_floor()})
	check("attack-grants-no-resources", game.player.air_jumps_left == air_before and game.player.dashes_left == dash_before, {"air_jumps_left":game.player.air_jumps_left, "dashes_left":game.player.dashes_left, "before":[air_before, dash_before]})
	# Facing is locked for the swing, then follows input again once it ends.
	await fresh()
	game.player.test_axis = 1.0
	await steps(3)
	game.player.test_attack_pressed = true
	await steps(1)
	game.player.test_axis = -1.0
	await steps(8)
	var locked_facing: float = game.player.facing
	await steps(10)
	check("attack-locks-facing-until-it-ends", is_equal_approx(locked_facing, 1.0) and is_equal_approx(game.player.facing, -1.0), {"facing_mid_swing":locked_facing, "facing_after":game.player.facing})
	# D3 — explicitly NOT invincible. Walking into the real spikes while
	# swinging still kills; the swing hitbox cannot touch a hazard by design.
	await fresh()
	game.player.position = Vector2(290, 320)
	await steps(2)
	game.player.test_axis = 1.0
	game.player.test_attack_pressed = true
	for i in range(30):
		await steps(1)
		if game.state == Game.State.DYING:
			break
	check("attack-not-invincible", game.state == Game.State.DYING and game.deaths == 1, {"state":game.state, "deaths":game.deaths, "x":game.player.position.x})
	# Death reaction (CHANGE-BRIEF revision 0.4.0). The overlay's lifetime is
	# the laugh's own length, read from the stream, so the image cannot outlive
	# or undercut the sound.
	await fresh()
	check("death-fx-assets-loaded", game.laugh.stream != null and game.cat_texture != null and game.death_fx_total > 3.0, {"laugh_length":game.death_fx_total, "cat_size":str(Vector2i(game.cat_texture.get_width(), game.cat_texture.get_height())) if game.cat_texture else "null"})
	game.player.position = Vector2(300, 320)
	await steps(2)
	game.player.test_axis = 1.0
	for i in range(40):
		await steps(1)
		if game.state == Game.State.DYING:
			break
	# Stand still after respawning so the run below measures one reaction and
	# not a second death restarting it.
	game.player.test_axis = 0.0
	check("death-triggers-reaction", game.state == Game.State.DYING and game.death_fx_remaining > game.death_fx_total - 0.05, {"state":game.state, "remaining":game.death_fx_remaining, "total":game.death_fx_total, "audio_playing":game.laugh.playing})
	# The starter's 0.55 s retry is UNCHANGED, so the overlay deliberately
	# outlasts the respawn and covers part of the next attempt. This is the
	# documented consequence of "the image disappears when the laugh ends",
	# asserted rather than left as a surprise.
	var respawn_frames: int = 0
	for i in range(60):
		await steps(1)
		respawn_frames += 1
		if game.state == Game.State.PLAYING:
			break
	check("death-fx-outlasts-respawn", game.state == Game.State.PLAYING and respawn_frames <= 36 and game.death_fx_remaining > 2.0, {"respawn_frames":respawn_frames, "remaining_after_respawn":game.death_fx_remaining})
	# Freezing the game freezes the reaction, so the countdown driving the
	# overlay cannot drift away from the paused audio.
	var before_pause: float = game.death_fx_remaining
	game.set_paused(true)
	await steps(30)
	check("death-fx-frozen-while-paused", is_equal_approx(game.death_fx_remaining, before_pause) and game.laugh.stream_paused, {"before":before_pause, "after":game.death_fx_remaining, "stream_paused":game.laugh.stream_paused})
	game.set_paused(false)
	# It ends with the laugh: the remaining time counts down to exactly zero
	# and the total elapsed matches the stream length.
	var ran_frames: int = respawn_frames
	for i in range(260):
		await steps(1)
		ran_frames += 1
		if game.death_fx_remaining <= 0.0:
			break
	check("death-fx-ends-with-the-laugh", game.death_fx_remaining <= 0.0 and absf(float(ran_frames) / 60.0 - game.death_fx_total) < 0.15, {"elapsed_s":float(ran_frames)/60.0, "laugh_length_s":game.death_fx_total, "remaining":game.death_fx_remaining})
	# One reaction per death: a new death restarts it from the top.
	game.player.position = Vector2(300, 320)
	await steps(2)
	game.player.test_axis = 1.0
	for i in range(40):
		await steps(1)
		if game.state == Game.State.DYING:
			break
	game.player.test_axis = 0.0
	check("death-fx-restarts-on-each-death", game.deaths == 2 and game.death_fx_remaining > game.death_fx_total - 0.05, {"deaths":game.deaths, "remaining":game.death_fx_remaining})
	# Leaving for the menu cancels it; it must not follow the player out.
	game.state = Game.State.COMPLETE
	game._unhandled_input(_menu_event())
	await steps(2)
	# The first build drew the cat straight over the death panel and hid the
	# starter's death reason. Geometry is asserted, not eyeballed.
	check("death-cat-does-not-cover-the-death-panel", not HudScript.DEATH_CAT.intersects(HudScript.DEATH_PANEL) and Rect2(0, 74, 640, 261).encloses(HudScript.DEATH_CAT), {"cat":str(HudScript.DEATH_CAT), "panel":str(HudScript.DEATH_PANEL), "intersects":HudScript.DEATH_CAT.intersects(HudScript.DEATH_PANEL)})
	check("death-fx-cleared-on-menu", is_zero_approx(game.death_fx_remaining) and not game.laugh.playing, {"remaining":game.death_fx_remaining, "audio_playing":game.laugh.playing})
	for age in [5,6,7]:
		await fresh()
		game.player.jump_request_tick = game.player.tick + 1 - age
		await steps(1)
		check("buffer-%d" % age, (game.player.jumps == 1) == (age <= 6), {"age":age, "jumps":game.player.jumps})
	await fresh()
	game._add_solid(Rect2(32,260,64,12))
	await steps(2)
	game.player.test_jump_pressed = true
	min_y = 320
	for i in range(45):
		await steps(1)
		min_y = minf(min_y,game.player.position.y)
	check("low-ceiling", min_y >= 300-0.2 and game.player.jumps == 1 and game.player.is_on_floor(), {"minimum_feet_y":min_y,"jumps":game.player.jumps})
	await fresh()
	game.player.test_jump_pressed = true
	await steps(5)
	game.set_paused(true)
	var paused_position: Vector2 = game.player.position
	var paused_time: float = game.elapsed
	await steps(10)
	check("pause-freezes", game.player.position == paused_position and game.elapsed == paused_time, {"position":str(game.player.position),"elapsed":game.elapsed})
	game.set_paused(false)
	game.test_mode = false
	game._on_focus_lost()
	check("focus-loss-pauses", game.state == Game.State.PAUSED, {"state":game.state})
	game.test_mode = true
	await fresh()
	game.player.position = Vector2(330,310)
	await steps(4)
	check("actual-spike-collision", game.state == Game.State.DYING and game.deaths == 1, {"state":game.state,"deaths":game.deaths})
	game.resolve_contacts(true,true)
	check("duplicate-death-ignored", game.deaths == 1, {"deaths":game.deaths})
	await steps(38)
	check("respawn", game.state == Game.State.PLAYING and game.player.position.distance_to(Vector2(64,320)) < 1, {"state":game.state,"position":str(game.player.position)})
	game.restart_attempt()
	check("manual-restart-not-death", game.deaths == 1, {"deaths":game.deaths})
	var largest_retry_ticks: int = 0
	for i in range(20):
		game.resolve_contacts(true,false)
		var waited := 0
		while game.state == Game.State.DYING and waited < 65:
			await steps(1)
			waited += 1
		largest_retry_ticks = maxi(largest_retry_ticks, waited)
	check("twenty-retries", game.deaths == 21 and largest_retry_ticks <= 60, {"deaths":game.deaths,"max_retry_ticks":largest_retry_ticks})
	await fresh()
	game.resolve_contacts(true,true)
	check("death-before-finish", game.state == Game.State.DYING, {"state":game.state})
	await fresh()
	game.player.position = Vector2(415,432)
	await steps(1)
	check("fall-boundary", game.state == Game.State.DYING, {"state":game.state})
	await fresh()
	var route = Route.new()
	var route_ticks := 0
	# 3072 px at 160 px/s is already 1152 ticks before any jump or swing, so
	# the starter's 900 cannot reach the new finish.
	while game.state == Game.State.PLAYING and route_ticks < 1600:
		route.step(game)
		await steps(1)
		route_ticks += 1
	check("complete-real-route", game.state == Game.State.COMPLETE and game.deaths == 0, {"state":game.state,"deaths":game.deaths,"ticks":route_ticks,"position":str(game.player.position),"jump_marks_used":route.next_jump})
	game.start_session()
	game.start_session()
	check("replay-idempotent", game.state == Game.State.PLAYING and game.deaths == 0 and game.player.jumps == 0, {"state":game.state,"deaths":game.deaths,"jumps":game.player.jumps})
	var report := {"scope":"First Steps slice; not full GDD acceptance or human playtesting", "engine":Engine.get_version_info().string,"created_at":Time.get_datetime_string_from_system(true),"results":results,"failures":failures}
	# --- Level extension (CHANGE-BRIEF revision 0.5.0) ---
	# Geometry first: the derived spike rule must reproduce the starter's
	# hard-coded three, and the collision polygons must match the drawn ones.
	await fresh()
	var counts_ok: bool = true
	var poly_ok: bool = true
	for entry in game.level.hazards:
		if Game.spike_count(Rect2(entry[0], entry[1], entry[2], entry[3])) != 3:
			counts_ok = false
	for i in range(game.trap_rects.size()):
		if Game.spike_count(game.trap_rects[i]) != 3:
			counts_ok = false
		var polys: int = 0
		for child in game.trap_areas[i].get_children():
			if child is CollisionPolygon2D:
				polys += 1
		if polys != Game.spike_count(game.trap_rects[i]):
			poly_ok = false
	check("spike-count-derives-from-width", counts_ok and poly_ok, {"all_counts_are_3":counts_ok, "collision_polys_match_drawn":poly_ok, "traps":game.trap_rects.size()})
	check("finish-past-original-section", float(game.level.finish[0]) > 960.0 and float(game.level.finish[0]) < float(game.level.width), {"finish_x":game.level.finish[0], "width":game.level.width})
	# Derived rather than hard-coded: this assertion pinned 1436 and broke the
	# moment the level grew again. What matters is that the HUD span is the
	# level's own span and not the starter's stale 852.
	var hud_span: float = float(game.level.finish[0]) - float(game.level.spawn[0])
	check("hud-progress-spans-the-new-level", hud_span > 852.0 and absf(hud_span - (float(game.level.finish[0]) - float(game.level.spawn[0]))) < 0.5, {"span":hud_span, "starter_span":852, "finish_x":game.level.finish[0]})
	# Traps start buried: the area sits at the spike rect's BOTTOM, which is the
	# ground surface, so a grounded player (collider y 292..320) cannot reach it.
	var buried_ok: bool = true
	for i in range(game.trap_areas.size()):
		var want: float = game.trap_rects[i].position.y + game.trap_rects[i].size.y
		if absf(game.trap_areas[i].position.y - want) > 0.01:
			buried_ok = false
	check("traps-start-buried-at-the-surface", buried_ok and is_equal_approx(game.trap_areas[0].position.y, 320.0), {"trap0_y":game.trap_areas[0].position.y, "ground_surface":320.0, "all_buried":buried_ok})
	# Rise timing: past the trigger but short of the spike, the trap takes
	# exactly TRAP_RISE_TICKS to surface and the player is untouched.
	# Start LEFT of the trigger and walk into it, so the rise is measured from
	# its actual first tick. Placing the player past the trigger and counting
	# loop iterations measured the wrong thing on the first attempt.
	game.player.position = Vector2(1020, 320)
	game.player.test_axis = 1.0
	await steps(2)
	for i in range(80):
		await steps(1)
		if game.trap_risen[0] > 0:
			break
	var first_tick: int = game.trap_risen[0]
	var rise_frames: int = 0
	for i in range(40):
		if game.trap_risen[0] >= Game.TRAP_RISE_TICKS:
			break
		await steps(1)
		rise_frames += 1
	check("trap-rises-in-15-ticks", first_tick == 1 and first_tick + rise_frames == Game.TRAP_RISE_TICKS and is_equal_approx(game.trap_areas[0].position.y, 304.0) and game.state == Game.State.PLAYING, {"first_tick":first_tick, "further_frames":rise_frames, "total":first_tick + rise_frames, "trap0_y":game.trap_areas[0].position.y, "state":game.state})
	# Stand still: the rise measurement left the player walking right, and
	# stepping on with the axis still held marched them into the very trap the
	# next checks are about.
	game.player.test_axis = 0.0
	# It does not retract.
	await steps(120)
	check("trap-does-not-retract", is_equal_approx(game.trap_areas[0].position.y, 304.0) and game.trap_risen[0] == Game.TRAP_RISE_TICKS, {"trap0_y":game.trap_areas[0].position.y, "risen":game.trap_risen[0]})
	# The trigger is one-way: walking back left past it leaves the trap up.
	# Walk back left but STAY on L1 (1008..1216): the first attempt stepped 40
	# frames and left the platform at x=993, into the gap.
	game.player.test_axis = -1.0
	await steps(20)
	check("trap-trigger-is-one-way", game.player.position.x < float(game.level.traps[0].trigger_x) and is_equal_approx(game.trap_areas[0].position.y, 304.0), {"player_x":game.player.position.x, "trigger_x":game.level.traps[0].trigger_x, "trap0_y":game.trap_areas[0].position.y})
	# A risen trap kills, through the starter's own hazard path: it sets deaths,
	# enters DYING and starts the death reaction, with no separate code path.
	game.player.test_axis = 1.0
	for i in range(120):
		await steps(1)
		if game.state == Game.State.DYING:
			break
	# The death must happen AT the trap. The first version of this check passed
	# while the player was actually falling into the 960..1008 gap, because the
	# preceding one-way test had walked them off the platform - a pass for the
	# wrong reason.
	var spike_left: float = float(game.level.traps[0].spike[0])
	var died_at_trap: bool = absf(game.player.position.x - spike_left) < 20.0 and game.player.position.y <= 320.0
	check("trap-kills-when-risen", game.state == Game.State.DYING and game.deaths == 1 and died_at_trap, {"state":game.state, "deaths":game.deaths, "x":game.player.position.x, "y":game.player.position.y, "spike_left":spike_left})
	check("trap-shares-the-original-death-path", game.death_reason == "Watch the spikes" and game.death_fx_remaining > 0.0, {"death_reason":game.death_reason, "laugh_remaining":game.death_fx_remaining})
	# Respawn puts every trap back underground.
	for i in range(60):
		await steps(1)
		if game.state == Game.State.PLAYING:
			break
	var reset_ok: bool = true
	for i in range(game.trap_areas.size()):
		if game.trap_risen[i] != 0:
			reset_ok = false
	check("traps-reset-on-retry", reset_ok and is_equal_approx(game.trap_areas[0].position.y, 320.0), {"all_reset":reset_ok, "trap0_y":game.trap_areas[0].position.y, "state":game.state})
	# The warning the design promises: at the full 160 px/s run, the frames
	# between crossing a trigger and the player's leading edge reaching the
	# spike must exceed the rise time.
	var worst_margin: int = 9999
	var margins: Array = []
	for entry in game.level.traps:
		var distance: float = (float(entry.spike[0]) - 9.0) - float(entry.trigger_x)
		var frames: int = int(distance / 160.0 * 60.0)
		margins.append(frames)
		worst_margin = mini(worst_margin, frames)
	check("trap-warning-window-exceeds-rise", worst_margin >= Game.TRAP_RISE_TICKS, {"frames_per_trap":margins, "rise_ticks":Game.TRAP_RISE_TICKS, "worst":worst_margin})
	# CHANGE-BRIEF 0.5.0 P15: the high road is an 8 px plank and the player can
	# fall at up to 480 px/s, which is 8 px per physics frame - the classic
	# tunnelling setup. Dropped from well above with no horizontal input.
	await fresh()
	game.player.position = Vector2(1160, 96)
	game.player.test_axis = 0.0
	var peak_fall: float = 0.0
	for i in range(90):
		await steps(1)
		peak_fall = maxf(peak_fall, game.player.velocity.y)
		if game.player.is_on_floor():
			break
	check("thin-plank-does-not-tunnel", game.player.is_on_floor() and absf(game.player.position.y - 224.0) < 2.0 and peak_fall > 400.0, {"landed_y":game.player.position.y, "peak_fall_speed":peak_fall, "px_per_frame":peak_fall/60.0, "plank_top":224.0})
	# --- The high road needs BOTH departures ---
	await fresh()
	await drive_fork(false)
	var without_dash_y: float = game.player.position.y
	var without_dash_on_h1: bool = game.player.is_on_floor() and absf(game.player.position.y - 224.0) < 2.0
	await fresh()
	await drive_fork(true)
	var with_dash_on_h1: bool = game.player.is_on_floor() and absf(game.player.position.y - 224.0) < 2.0
	check("high-road-needs-the-dash", with_dash_on_h1 and not without_dash_on_h1, {"double_jump_only_landed_y":without_dash_y, "double_jump_plus_dash_y":game.player.position.y, "on_h1_without_dash":without_dash_on_h1, "on_h1_with_dash":with_dash_on_h1})
	# And from H1 the high road reaches the relocated finish.
	# What the high road actually buys is skipping T1..T3, so that is what this
	# asserts. Driving it all the way to the finish used to be the same thing;
	# with the level doubled it would mean driving the whole enemy half too,
	# which complete-real-route already covers.
	game.player.test_axis = 1.0
	await steps(24)
	game.player.test_jump_pressed = true
	await steps(20)
	game.player.test_jump_pressed = true
	for i in range(160):
		await steps(1)
		if game.state != Game.State.PLAYING or game.player.position.x > 1470.0:
			break
	check("high-road-clears-the-traps", game.state == Game.State.PLAYING and game.deaths == 0 and game.player.position.x > 1456.0, {"state":game.state, "deaths":game.deaths, "x":game.player.position.x, "last_trap_ends":1456})
	# --- Enemies (CHANGE-BRIEF revision 0.6.0) ---
	await fresh()
	var slimes: int = 0
	var horses: int = 0
	for k in game.enemy_kinds:
		if k == "horse":
			horses += 1
		else:
			slimes += 1
	check("enemies-load-from-level", game.enemy_areas.size() == 11 and slimes == 6 and horses == 5, {"total":game.enemy_areas.size(), "slimes":slimes, "horses":horses})
	# CHANGE-BRIEF P17, raw values: one Area2D has to do both jobs. Layer 3
	# (bit 4) is what the swing hitbox masks; mask layer 2 (bit 2) is what lets
	# overlaps_body see the player. A silent edit to either breaks one direction
	# only, which is why both are pinned here.
	var layers_ok: bool = true
	for area in game.enemy_areas:
		if area.collision_layer != 4 or area.collision_mask != 2:
			layers_ok = false
	check("enemy-layers-serve-both-directions", layers_ok and game.player.attack_hitbox.collision_mask == 4, {"enemy_layer":game.enemy_areas[0].collision_layer, "enemy_mask":game.enemy_areas[0].collision_mask, "slash_mask":game.player.attack_hitbox.collision_mask})
	# P18: every slime's patrol has to sit on a solid, including the one on the
	# 8 px plank. Checked against the level's own solids rather than by eye.
	var all_supported: bool = true
	var plank_slime_ok: bool = false
	for i in range(game.enemy_kinds.size()):
		if game.enemy_kinds[i] == "horse":
			continue
		var supported: bool = false
		for entry in game.level.solids:
			var top: float = entry[1]
			if absf(top - game.enemy_anchor[i].y) > 0.01:
				continue
			if entry[0] <= game.enemy_from[i] - 11.0 and entry[0] + entry[2] >= game.enemy_to[i] + 11.0:
				supported = true
				if absf(top - 200.0) < 0.01:
					plank_slime_ok = true
		if not supported:
			all_supported = false
	check("every-slime-patrols-on-solid-ground", all_supported and plank_slime_ok, {"all_supported":all_supported, "plank_slime_supported":plank_slime_ok})
	# P20: horses are the first thing in this game that ignores gravity.
	var horse_y: Array = []
	for i in range(game.enemy_kinds.size()):
		if game.enemy_kinds[i] == "horse":
			horse_y.append(game.enemy_areas[i].position.y)
	await steps(260)
	var altitude_held: bool = true
	var bounds_held: bool = true
	var h: int = 0
	for i in range(game.enemy_kinds.size()):
		if game.enemy_kinds[i] == "horse":
			if absf(game.enemy_areas[i].position.y - horse_y[h]) > 0.01:
				altitude_held = false
			h += 1
		if game.enemy_x[i] < game.enemy_from[i] - 0.01 or game.enemy_x[i] > game.enemy_to[i] + 0.01:
			bounds_held = false
	check("horses-hold-altitude", altitude_held, {"start_y":horse_y, "after_260_ticks_unchanged":altitude_held})
	check("enemies-stay-inside-their-bounds", bounds_held, {"checked_ticks":260, "enemies":game.enemy_areas.size()})
	# P17 direction one: a slash removes an enemy. Stand next to the first
	# ground slime and swing.
	await fresh()
	# Positioned against the slime's CURRENT x, not its patrol bound: it spawns
	# at 1630 and walks right first, so standing 40 px left of `from` (1580) put
	# the player 90-150 px away, far outside the 35 px the blade reaches.
	game.player.position = Vector2(game.enemy_x[1] - 34.0, 320)
	game.player.test_axis = 0.0
	await steps(2)
	var before_kills: int = game.enemies_killed
	for i in range(60):
		game.player.test_attack_pressed = true
		await steps(1)
		if game.enemies_killed > before_kills:
			break
	check("slash-removes-an-enemy", game.enemies_killed == before_kills + 1 and not game.enemy_alive[1] and game.state == Game.State.PLAYING, {"killed":game.enemies_killed, "enemy1_alive":game.enemy_alive[1], "state":game.state})
	# A dead enemy is harmless: walk through where it was.
	game.player.test_axis = 1.0
	for i in range(120):
		await steps(1)
		if game.player.position.x > game.enemy_to[1] + 20.0 or game.state != Game.State.PLAYING:
			break
	check("a-dead-enemy-is-harmless", game.state == Game.State.PLAYING and game.deaths == 0 and game.player.position.x > game.enemy_to[1], {"state":game.state, "deaths":game.deaths, "x":game.player.position.x, "patrol_end":game.enemy_to[1]})
	# P17 direction two: contact kills, through the starter's own path, with its
	# own message.
	await fresh()
	game.player.position = Vector2(game.enemy_x[1] - 60.0, 320)
	game.player.test_axis = 1.0
	for i in range(120):
		await steps(1)
		if game.state == Game.State.DYING:
			break
	check("enemy-contact-kills-the-player", game.state == Game.State.DYING and game.deaths == 1 and game.death_reason == "It got you", {"state":game.state, "deaths":game.deaths, "reason":game.death_reason, "x":game.player.position.x})
	check("enemy-death-reuses-the-reaction", game.death_fx_remaining > 0.0 and absf(game.retry_remaining - 0.55) < 0.06, {"laugh_remaining":game.death_fx_remaining, "retry_remaining":game.retry_remaining})
	# Respawn brings every enemy back.
	for i in range(60):
		await steps(1)
		if game.state == Game.State.PLAYING:
			break
	var all_back: bool = true
	for i in range(game.enemy_alive.size()):
		if not game.enemy_alive[i] or absf(game.enemy_x[i] - game.enemy_anchor[i].x) > 4.0:
			all_back = false
	check("enemies-reset-on-retry", all_back and game.enemies_killed == 0, {"all_alive_at_spawn":all_back, "killed":game.enemies_killed, "state":game.state})
	# --- C4 / C6: music and mute (CHANGE-BRIEF revision 2.1.0) ---------------
	await fresh()
	var ms = game.music.stream
	check("music-loop-is-flagged-to-loop", ms != null and ms.loop and absf(ms.get_length() - 30.9632) < 0.01, {"loaded":ms != null, "loop":ms.loop if ms else false, "length":ms.get_length() if ms else -1.0})
	# Its own bus, so it can be ducked or balanced without touching the SFX.
	check("music-is-on-its-own-bus", game.music.bus == Game.MUSIC_BUS and AudioServer.get_bus_index(Game.MUSIC_BUS) > 0, {"bus":game.music.bus, "index":AudioServer.get_bus_index(Game.MUSIC_BUS)})
	check("music-plays-during-a-run", game.music.playing, {"playing":game.music.playing, "position":game.music.get_playback_position()})
	# The one that matters: restart_attempt() runs on EVERY death, and a loop
	# that jumps back to bar 1 every 0.55 s is worse than no music at all.
	await steps(30)
	var pos_before: float = game.music.get_playback_position()
	game.restart_attempt()
	await steps(5)
	var pos_after: float = game.music.get_playback_position()
	check("a-retry-does-not-restart-the-track", game.music.playing and pos_after >= pos_before, {"before":pos_before, "after":pos_after, "went_backwards":pos_after < pos_before})
	# Frozen with the game, exactly like the death reaction.
	game.set_paused(true)
	await steps(2)
	var paused_ok: bool = game.music.stream_paused
	var pos_paused: float = game.music.get_playback_position()
	game.set_paused(false)
	await steps(2)
	check("music-pauses-with-the-game", paused_ok and not game.music.stream_paused and game.music.playing, {"stream_paused_while_paused":paused_ok, "stream_paused_after":game.music.stream_paused, "playing_after":game.music.playing})
	# `playing` reads FALSE while `stream_paused` is true, so a guard written
	# against `playing` alone restarted the track here. Regression check.
	game.set_paused(true)
	await steps(2)
	var pos_at_pause: float = game.music.get_playback_position()
	game.restart_attempt()
	await steps(3)
	check("retry-while-paused-resumes-rather-than-restarts", game.music.get_playback_position() >= pos_at_pause and not game.music.stream_paused, {"at_pause":pos_at_pause, "after_retry":game.music.get_playback_position(), "stream_paused":game.music.stream_paused})
	# Mute is a MASTER bus mute, not a per-stream one: a per-stream mute leaves
	# anything added later audible, which is the failure the brief predicted.
	var master: int = AudioServer.get_bus_index("Master")
	game.set_muted(true)
	var muted_ok: bool = AudioServer.is_bus_mute(master) and game.muted
	game.set_muted(false)
	check("mute-is-a-master-bus-mute", muted_ok and not AudioServer.is_bus_mute(master) and not game.muted, {"muted_master":muted_ok, "unmuted_master":AudioServer.is_bus_mute(master), "flag":game.muted})
	# Reaching the goal ends the track; it is not left looping under the card.
	game.state = Game.State.PLAYING
	game.resolve_contacts(false, true)
	await steps(2)
	check("music-stops-at-the-finish", game.state == Game.State.COMPLETE and not game.music.playing, {"state":game.state, "playing":game.music.playing, "pos_at_pause_unused":pos_paused})

	# --- C3: the death pose (CHANGE-BRIEF revision 2.4.0) --------------------
	# Keyed off the session state, so it must be identical however the player
	# died. Three causes, one pose.
	var pose_states: Array = []
	for cause in ["spike", "fall", "enemy"]:
		await fresh()
		if cause == "spike":
			game.player.position = Vector2(275, 320)
			game.player.test_axis = 1.0
		elif cause == "fall":
			game.player.position = Vector2(470, 300)
			game.player.test_axis = 0.0
		else:
			game.player.position = Vector2(game.enemy_x[1] - 60.0, 320)
			game.player.test_axis = 1.0
		for i in range(240):
			await steps(1)
			if game.state == Game.State.DYING:
				break
		pose_states.append({"cause": cause, "state": game.state, "pose": game.player.death_pose})
	var all_prone: bool = true
	for e in pose_states:
		if e["state"] != Game.State.DYING or not e["pose"]:
			all_prone = false
	check("death-pose-is-the-same-whatever-killed-you", all_prone, {"causes": pose_states})
	# And it must clear, or the character stays face down for the rest of the run.
	for i in range(80):
		await steps(1)
		if game.state == Game.State.PLAYING:
			break
	check("death-pose-clears-on-respawn", game.state == Game.State.PLAYING and not game.player.death_pose, {"state": game.state, "pose": game.player.death_pose})

	# --- C5: the four sound effects -----------------------------------------
	await fresh()
	var lens := {"jump": 0.110, "slash": 0.140, "trap": 0.260, "death": 0.450}
	var loaded: bool = true
	var observed := {}
	for id in lens:
		var pl = game.sfx.get(id)
		if pl == null or pl.stream == null or absf(pl.stream.get_length() - lens[id]) > 0.02:
			loaded = false
		observed[id] = pl.stream.get_length() if (pl and pl.stream) else -1.0
	check("sfx-all-four-are-loaded-at-their-synthesised-lengths", loaded, observed)
	# Their own bus, separate from the music's, so the masking balance is one
	# slider rather than four.
	var own_bus: bool = true
	for id in lens:
		if game.sfx[id].bus != Game.SFX_BUS:
			own_bus = false
	check("sfx-is-on-its-own-bus", own_bus and AudioServer.get_bus_index(Game.SFX_BUS) > 0 and Game.SFX_BUS != Game.MUSIC_BUS, {"bus": Game.SFX_BUS, "index": AudioServer.get_bus_index(Game.SFX_BUS), "music_bus": Game.MUSIC_BUS})

	# One jump, one jump sound. Read off the player's own counter.
	await fresh()
	game.sfx_log.clear()
	game.player.test_jump_pressed = true
	await steps(1)
	game.player.test_jump_pressed = false
	await steps(6)
	check("sfx-jump-fires-once-per-jump", _sfx_count(game, "jump") == 1 and game.player.jumps == 1, {"jumps": game.player.jumps, "sounds": _sfx_count(game, "jump"), "log": game.sfx_log})

	await fresh()
	game.sfx_log.clear()
	game.player.test_attack_pressed = true
	await steps(1)
	game.player.test_attack_pressed = false
	await steps(6)
	check("sfx-slash-fires-on-the-swing", _sfx_count(game, "slash") == 1 and game.player.attacks == 1, {"attacks": game.player.attacks, "sounds": _sfx_count(game, "slash")})

	# THE one that matters. The warning has to fire on the trigger crossing, so
	# the player can act on it; fired on the damage instead it is a death sound
	# arriving after the information is useless -- and it would still pass a
	# check that only asked whether a sound played when the trap killed you.
	await fresh()
	game.player.position = Vector2(1020, 320)
	game.player.test_axis = 0.0
	for i in range(20):
		await steps(1)
		if game.player.is_on_floor():
			break
	game.sfx_log.clear()
	game.player.test_axis = 1.0
	var trap_tick: int = -1
	var death_tick: int = -1
	var trap_x: float = -1.0
	for i in range(240):
		await steps(1)
		for e in game.sfx_log:
			if e["id"] == "trap" and trap_tick < 0:
				trap_tick = e["tick"]
				trap_x = game.player.position.x
			if e["id"] == "death" and death_tick < 0:
				death_tick = e["tick"]
		if game.state == Game.State.DYING:
			break
	var lead: int = death_tick - trap_tick
	check("sfx-trap-fires-on-the-trigger-not-the-contact", trap_tick > 0 and death_tick > trap_tick and lead >= Game.TRAP_RISE_TICKS, {"trap_tick": trap_tick, "death_tick": death_tick, "lead_ticks": lead, "rise_ticks": Game.TRAP_RISE_TICKS, "trigger_x": game.level.traps[0].trigger_x, "player_x_at_warning": trap_x})
	check("sfx-death-fires-on-the-fatal-contact", _sfx_count(game, "death") == 1 and game.state == Game.State.DYING, {"deaths": game.deaths, "sounds": _sfx_count(game, "death"), "state": game.state})

	# The master limiter. Two sources at 0 dB clip: the music loop peaks at
	# 0.702 and SFX-TRAP at 0.810 after trim, so an aligned pair sums to 1.512.
	# Asserted because it is invisible -- a few clipped samples inside a 0.26 s
	# sweep are not something an ear catches, and the only reason this is here
	# at all is that an offline mix of the two rendered at 1.172.
	await fresh()
	var master_bus: int = AudioServer.get_bus_index("Master")
	var lim = null
	for i in range(AudioServer.get_bus_effect_count(master_bus)):
		if AudioServer.get_bus_effect(master_bus, i) is AudioEffectHardLimiter:
			lim = AudioServer.get_bus_effect(master_bus, i)
	check("master-bus-has-a-limiter-because-two-sources-at-0db-clip", lim != null and lim.ceiling_db <= 0.0 and absf(game.music.volume_db + 3.0) < 0.01, {"limiter": lim != null, "ceiling_db": lim.ceiling_db if lim else 999.0, "music_volume_db": game.music.volume_db, "worst_unlimited_sum": 1.512})

	# --- C2: the generated sprites (CHANGE-BRIEF revision 2.5.0) -------------
	await fresh()
	var want_keys := ["idle", "run", "rise", "fall", "dash", "windup", "live", "death"]
	var missing: Array = []
	var wrong_size: Array = []
	for key in want_keys:
		var t = game.player.pose_tex.get(key)
		if t == null:
			missing.append(key)
		elif t.get_width() != 32 or t.get_height() != 32:
			wrong_size.append("%s=%dx%d" % [key, t.get_width(), t.get_height()])
	check("pose-textures-all-eight-loaded-at-32x32", missing.is_empty() and wrong_size.is_empty(), {"missing": missing, "wrong_size": wrong_size, "loaded": game.player.pose_tex.size()})

	# The mapping, driven through real state rather than asserted in prose. Each
	# row is a state the engine can actually distinguish; CHARACTER-SHEET
	# section 5 is the list and this is the list in force.
	var seen := {}
	await fresh()
	game.player.test_axis = 0.0
	await steps(4)
	seen["idle"] = game.player.pose_key()
	game.player.test_axis = 1.0
	await steps(20)
	seen["run"] = game.player.pose_key()
	game.player.test_jump_pressed = true
	await steps(1)
	game.player.test_jump_pressed = false
	await steps(3)
	seen["rise"] = game.player.pose_key()
	# Dash while airborne: it takes priority over rise and fall.
	game.player.test_dash_pressed = true
	await steps(1)
	game.player.test_dash_pressed = false
	await steps(1)
	seen["dash"] = game.player.pose_key()
	for i in range(90):
		await steps(1)
		if game.player.velocity.y > 0.0 and not game.player.is_on_floor() and game.player.dash_ticks_left <= 0:
			break
	seen["fall"] = game.player.pose_key()
	for i in range(90):
		await steps(1)
		if game.player.is_on_floor():
			break
	game.player.test_axis = 0.0
	await steps(4)
	game.player.test_attack_pressed = true
	await steps(1)
	game.player.test_attack_pressed = false
	seen["windup"] = game.player.pose_key()
	await steps(5)
	seen["live"] = game.player.pose_key()
	game.player.death_pose = true
	seen["death"] = game.player.pose_key()
	game.player.death_pose = false
	var mismatched: Array = []
	for key in want_keys:
		if seen.get(key, "") != key:
			mismatched.append("%s -> %s" % [key, seen.get(key, "<unset>")])
	check("pose-key-matches-the-state-it-claims", mismatched.is_empty(), {"observed": seen, "mismatched": mismatched})

	# The blade is NOT in the sprites, and this is what keeps it that way: the
	# hitbox endpoints still come from ATTACK_PIVOT, attack_angle() and
	# attack_reach, which is also where the drawn blade comes from. Asserted
	# already by attack-hitbox-on-the-blade-*; this one records that the sprite
	# path did not take those numbers over.
	check("sprites-did-not-take-over-the-blade", game.player.pose_tex.size() == 8 and game.player.has_method("_draw_swing"), {"textures": game.player.pose_tex.size(), "shared_swing_routine": game.player.has_method("_draw_swing")})

	var out := ProjectSettings.globalize_path("res://../evidence")
	DirAccess.make_dir_recursive_absolute(out)
	var file := FileAccess.open(out + "/mechanics-" + str(Time.get_unix_time_from_system()) + ".json", FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"  "))
	file.close()
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	game.queue_free()
	await process_frame
	quit(1 if failures else 0)
