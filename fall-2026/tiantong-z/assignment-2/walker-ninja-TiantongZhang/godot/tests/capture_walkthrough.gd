extends SceneTree
## Input-only capture driver for the Brutalist godot-waikthrough film.
##
## Contract: skills/make/godot-waikthrough/references/capture-and-coverage.md
##
##   - Instantiate the REAL main scene, not a hand-built session.
##   - Drive it through real InputEvents. The mechanical suite's `test_*` hooks
##     bypass the InputMap, teleport the player and seed coyote/buffer state;
##     the contract says those are useful checks but explicitly NOT walkthrough
##     footage. Input.action_press() is also insufficient here: it sets the
##     polled action state but never produces an event, so it cannot reach
##     _unhandled_input, which is where the menu, pause, retry and replay keys
##     are handled. Real events go through the same path a keyboard does.
##   - Log every action against the game tick.
##   - Assert the expected result. Exhausting --quit-after is not success, so a
##     failed expectation quits nonzero and says which one failed.
##
## Take selected by the WALKER_TAKE environment variable: "a" or "b".
##
##   WALKER_TAKE=a godot --path godot --script res://tests/capture_walkthrough.gd \
##     --write-movie <dir>/frame.png --fixed-fps 60 --quit-after <n>

var scene: Node
var session: Node2D
var player: CharacterBody2D
var tick: int = 0
var log_lines: Array[String] = []
var take: String = "a"
var failure: String = ""

func _initialize() -> void:
	call_deferred("run")

# --- plumbing ---------------------------------------------------------------

func note(action: String, detail: String = "") -> void:
	var entry := {
		"tick": tick,
		"t_s": snappedf(float(tick) / 60.0, 0.001),
		"action": action,
		"state": session.state if session else -1,
		"player_x": snappedf(player.position.x, 0.01) if player else 0.0,
		"player_y": snappedf(player.position.y, 0.01) if player else 0.0,
	}
	if detail != "":
		entry["detail"] = detail
	log_lines.append(JSON.stringify(entry))

var deaths_seen: int = 0

func step(n: int = 1) -> void:
	for i in range(n):
		await physics_frame
		await process_frame
		tick += 1
		if session and session.deaths > deaths_seen:
			deaths_seen = session.deaths
			note("DIED", "%s at (%.1f, %.1f)" % [
				session.death_reason, player.position.x, player.position.y])

func key(code: Key, pressed: bool, label: String) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.physical_keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)
	note(("press " if pressed else "release ") + label)

func tap(code: Key, label: String, hold_ticks: int = 3) -> void:
	await key(code, true, label)
	await step(hold_ticks)
	await key(code, false, label)
	await step(2)

func click(pressed: bool) -> void:
	var event := InputEventMouseButton.new()
	event.button_index = MOUSE_BUTTON_LEFT
	event.pressed = pressed
	Input.parse_input_event(event)
	note(("press " if pressed else "release ") + "mouse-left")

## Held-key bookkeeping, so a take never presses a key that is already down
## and the input log stays a truthful press/release record.
var d_held: bool = false

func hold_right(on: bool) -> void:
	if on != d_held:
		await key(KEY_D, on, "move-right")
		d_held = on

## A one-frame jump press. Jump height is fixed, so hold duration is not a
## gameplay variable; releasing immediately keeps the log unambiguous.
func jump_once(label: String) -> void:
	await key(KEY_SPACE, true, label)
	await step(1)
	await key(KEY_SPACE, false, label)

func run_until(check: Callable, limit: int, label: String) -> bool:
	await hold_right(true)
	return await until(check, limit, label)

## The starter's own five marks, which carry the player through the original
## 0..960 section onto the ground before the fork. Every step here is a jump
## the level requires: the 16 px lip at 160 and the 32 px block at 576 are both
## taller than the character can walk up, so a take that skips them simply
## stands against a wall until its timeout - which is how this helper came to
## exist.
func run_original_section() -> bool:
	for mark in [138.0, 292.0, 424.0, 548.0, 712.0]:
		if not await run_and_jump_at(mark, 300):
			return false
		await step(26)
	return true

func run_and_jump_at(mark: float, limit: int) -> bool:
	if not await run_until(func(): return player.position.x >= mark and player.is_on_floor(),
			limit, "reached the %.0f jump mark" % mark):
		return false
	await jump_once("jump @%.0f" % mark)
	return true

## Step until `check` is true. Returns false and records the failure otherwise.
func until(check: Callable, limit: int, label: String) -> bool:
	for i in range(limit):
		if check.call():
			note("reached: " + label)
			return true
		await step(1)
	if check.call():
		note("reached: " + label)
		return true
	# A timeout is almost always a death somewhere earlier in the route, so say
	# so rather than reporting only the position the respawn left behind.
	failure = "timed out waiting for %s after %d ticks (x=%.1f y=%.1f state=%d deaths=%d reason=%s)" % [
		label, limit, player.position.x, player.position.y, session.state,
		session.deaths, session.death_reason]
	return false

func expect(condition: bool, label: String) -> bool:
	if condition:
		note("verified: " + label)
		return true
	failure = "expectation failed: " + label
	return false

# --- takes ------------------------------------------------------------------

## Control, failure and recovery: menu, start, walk, jump, a real spike death
## with its reaction, the automatic retry, pause/resume, manual retry, and back
## out to the menu.
func take_a() -> bool:
	note("take-a begin")
	await step(72)                                   # hold on the menu
	if not await run_start():
		return false
	await key(KEY_D, true, "move-right")
	if not await until(func(): return player.position.x > 150.0, 180, "walked past x=150"):
		return false
	await tap(KEY_SPACE, "jump")                     # a jump with nothing under it
	await step(30)
	# Walk into the starter's spike on purpose. No teleport: the player runs
	# there, dies, and the reaction plays.
	if not await until(func(): return session.state == session.State.DYING, 240, "spike death"):
		return false
	if not expect(session.deaths == 1 and session.death_reason == "Watch the spikes", "death reason is the spike"):
		return false
	if not expect(session.death_fx_remaining > 0.0, "death reaction started"):
		return false
	await key(KEY_D, false, "move-right")
	if not await until(func(): return session.state == session.State.PLAYING, 90, "automatic retry"):
		return false
	if not expect(player.position.x < 80.0, "respawned at the start"):
		return false
	await step(30)
	# Pause and resume.
	await key(KEY_D, true, "move-right")
	await step(45)
	await tap(KEY_ESCAPE, "pause")
	if not expect(session.state == session.State.PAUSED, "paused"):
		return false
	var frozen := player.position.x
	await step(60)
	if not expect(absf(player.position.x - frozen) < 0.01, "pause freezes the player"):
		return false
	await tap(KEY_ENTER, "resume")
	if not expect(session.state == session.State.PLAYING, "resumed"):
		return false
	await step(45)
	# Manual retry, then out to the menu.
	await tap(KEY_R, "manual-retry")
	if not await until(func(): return player.position.x < 80.0, 30, "manual retry respawn"):
		return false
	if not expect(session.deaths == 1, "manual retry is not a death"):
		return false
	await key(KEY_D, false, "move-right")
	await step(24)
	await tap(KEY_ESCAPE, "pause")
	await tap(KEY_M, "main-menu")
	if not expect(session.state == session.State.MENU, "back at the menu"):
		return false
	await step(36)
	note("take-a end")
	return true

## The course: the low road end to end, with traps, both enemy kinds, the sword
## and the relocated finish, then a replay.
##
## The swing policy is route_driver.gd's, which took six attempts to find, and
## the first version of this take proved again why: holding the button from
## x=1500 onward put the blade nine ticks into its sweep at the x=2020 takeoff,
## so the driver jumped into the second flying horse and died at (2040, 288).
## A flying horse can only be hit from the air but collides about seven frames
## after takeoff, so the live window has to be open AT takeoff: go quiet from 58
## px before a jump mark, press again at 12 px before it. Fighting a ground
## enemy outranks that timing.
##
## Everything below is real input. The loop therefore runs exactly one frame per
## iteration - the earlier version used tap(), whose 4 idle ticks fell right on
## the takeoff and stopped the policy running on the frames that matter.
const SLASH_FROM := 1500.0
const STOP_AT := 48.0
const GROUND_BAND := 20.0

## True when a live ground enemy is close enough ahead that walking on would
## collide. Reading enemy positions is observation, which the walkthrough
## contract allows; no teleporting, no forced completion, no disabled collision.
func blocking_ground_enemy() -> bool:
	if not player.is_on_floor():
		return false
	for i in range(session.enemy_areas.size()):
		if not session.enemy_alive[i]:
			continue
		if absf(session.enemy_anchor[i].y - player.position.y) > GROUND_BAND:
			continue
		var ahead: float = session.enemy_x[i] - player.position.x
		if ahead > 0.0 and ahead <= STOP_AT:
			return true
	return false

## The mark-driven low road, extracted from take B so take D can reuse the one
## route that is known to cross the trap fork and the enemy half without dying.
##
## Runs exactly one frame per iteration: the earlier version used tap(), whose
## four idle ticks fell on the takeoff and stopped the swing policy running on
## the frames that decide whether a flying horse connects.
##
## `slash_from` is the x past which the sword is used; pass a huge value to
## travel the same route with the sword down.
func run_course(stop_x: float, slash_from: float) -> bool:
	var ground_marks: Array = [138.0, 292.0, 424.0, 548.0, 712.0, 930.0, 1096.0, 1205.0, 1390.0,
		1700.0, 2020.0, 2212.0, 2404.0, 2596.0, 2770.0]
	var air_mark := 1258.0
	var next_ground := 0
	var air_done := false
	var mouse_down := false
	var jump_label := ""
	for i in range(2400):
		if session.state != session.State.PLAYING:
			break
		if player.position.x >= stop_x:
			break
		# Jump is a one-frame press, released at the top of the next frame so
		# the rest of the policy keeps running while airborne.
		if jump_label != "":
			await key(KEY_SPACE, false, jump_label)
			jump_label = ""
		var x := player.position.x
		var fighting := blocking_ground_enemy()
		# Stand and fight rather than walking into a ground enemy.
		if fighting == d_held:
			await key(KEY_D, not fighting, "move-right" + (" (hold ground)" if fighting else ""))
			d_held = not fighting
		var mark: float = ground_marks[next_ground] if next_ground < ground_marks.size() else 1.0e9
		var aiming: bool = x >= mark - 12.0 and x < mark
		var going_quiet: bool = x >= mark - 58.0 and x < mark - 12.0
		var want_attack: bool = fighting or aiming or (x >= slash_from and not going_quiet)
		if want_attack:
			# The player reads Input.is_action_just_pressed("attack"), so a held
			# button is one swing. Re-press only once a swing has ended;
			# pressing every frame would flood the log with ignored presses.
			if player.attack_ticks_left <= 0:
				if mouse_down:
					await click(false)
				await click(true)
				mouse_down = true
		elif mouse_down:
			await click(false)
			mouse_down = false
		if next_ground < ground_marks.size() and x >= ground_marks[next_ground] and player.is_on_floor():
			jump_label = "jump @%.0f" % ground_marks[next_ground]
			await key(KEY_SPACE, true, jump_label)
			next_ground += 1
		elif not air_done and x >= air_mark and not player.is_on_floor():
			jump_label = "air-jump @%.0f" % air_mark
			await key(KEY_SPACE, true, jump_label)
			air_done = true
		await step(1)
	if mouse_down:
		await click(false)
	return true

func take_b() -> bool:
	note("take-b begin")
	await step(36)
	if not await run_start():
		return false
	if not await run_course(1.0e9, SLASH_FROM):
		return false
	await hold_right(false)
	if not expect(session.state == session.State.COMPLETE, "reached the finish"):
		return false
	if not expect(session.deaths == 0, "finished without dying"):
		return false
	if not expect(session.enemies_killed > 0, "killed at least one enemy with the sword"):
		return false
	note("finished", "enemies_killed=%d" % session.enemies_killed)
	await step(90)                                   # hold the results card
	await tap(KEY_ENTER, "replay")
	if not expect(session.state == session.State.PLAYING and player.position.x < 80.0, "replay restarts at the spawn"):
		return false
	await step(48)
	note("take-b end")
	return true

## Take C - the other road: the HUD's mouse start, facing, the coyote jump, the
## air dash, and the HIGH road, which take B never uses.
##
## The two abilities do different jobs and the route shows each doing its own.
## Getting onto the first plank is 96 px above L1 and a single 53.33 px jump
## cannot reach it, so that is the air jump. The 116 px gap between the planks
## is a distance problem, so that is the dash, from one jump only.
func take_c() -> bool:
	note("take-c begin")
	await step(30)
	if not await mouse_start():
		return false
	# Facing. The visor slit, the scarf and the sheathed blade all mirror.
	await key(KEY_A, true, "move-left")
	await step(20)
	if not expect(player.facing < 0.0, "the character faces left"):
		return false
	await key(KEY_A, false, "move-left")
	await step(8)
	if not await run_and_jump_at(138.0, 240):      # onto the starter's step
		return false
	await step(24)
	if not await run_and_jump_at(292.0, 240):      # over the starter's spike
		return false
	# Land first. The first version of this looked for "not on the floor" right
	# after the 292 jump, found it two frames later while still airborne, and
	# called the resulting AIR jump a coyote jump. The assertion below caught
	# it, which is the whole reason it is phrased in terms of air_jumps_left.
	if not await run_until(func(): return player.is_on_floor() and player.position.x > 350.0,
			180, "landed past the spike"):
		return false
	# The coyote jump: run off the ledge at x=448 with NO ground jump, then
	# press in mid-air inside the 6-tick window. If this were the air jump
	# instead, air_jumps_left would drop - so the assertion distinguishes them.
	if not await run_until(func(): return not player.is_on_floor(), 240, "ran off the ledge with no jump"):
		return false
	if not expect(player.position.x > 440.0, "left the ground at the ledge, not from a jump"):
		return false
	var jumps_before: int = player.jumps
	await jump_once("coyote-jump")
	await step(2)
	if not expect(player.jumps == jumps_before + 1, "a jump fired after leaving the ground"):
		return false
	if not expect(player.air_jumps_left == player.tuning.air_jumps,
			"the coyote jump spent the ground jump and left the air jump in hand"):
		return false
	if not await run_until(func(): return player.is_on_floor() and player.position.x > 512.0, 180, "landed across the gap"):
		return false
	# The 32 px step at 576 is taller than the player can walk up, so it is a
	# jump, not a slope - the first run of this take walked into its wall and
	# stood there until the timeout said so.
	if not await run_and_jump_at(548.0, 150):
		return false
	await step(26)
	if not await run_and_jump_at(712.0, 300):
		return false
	await step(30)
	# THE HIGH ROAD, on the schedule test_game.gd's drive_fork() proves:
	# jump from the ground before the 960..1008 gap, air-jump 20 ticks later at
	# the apex, dash 20 ticks after that. All three abilities in one move, which
	# is what CHANGE-BRIEF 0.5.0 designed the fork around - the plank's
	# underside at y=232 deliberately blocks a plain double jump from below.
	#
	# The first version of this take tried exactly that blocked route: it jumped
	# from L1 underneath the plank, the air jump put the character's head into
	# the plank's underside, it dropped back onto L1 and died on trap T1 at
	# (1186.8, 316.1). The design note had predicted that; I had not read it.
	if not await run_until(func(): return player.position.x >= 946.0 and player.is_on_floor(),
			300, "the launch point before the gap"):
		return false
	await jump_once("jump 1 of 3")
	await step(20)
	await jump_once("jump 2 of 3 - air jump for height")
	await step(20)
	var dashes_before: int = player.dashes
	await dash()
	if not expect(player.dashes == dashes_before + 1, "the air dash carries the last of the distance"):
		return false
	if not await until(func(): return player.is_on_floor(), 150, "landed on the high plank"):
		return false
	if not expect(absf(player.position.y - 224.0) < 2.0,
			"landed on the plank at y=224, not back on the floor below"):
		return false
	if not expect(session.deaths == 0, "reached the high road without dying"):
		return false
	# Let go before pausing to show the plank. The first version held right
	# through the pause, walked off the 1224 edge and landed on trap T2's spike
	# at (1304.1, 317.7) - the plank is only 120 px long and there is no room
	# on it for a standing beat with the run key down.
	await hold_right(false)
	note("on the high road", "x=%.1f y=%.1f" % [player.position.x, player.position.y])
	await step(24)
	# What the high road actually BUYS: leave H1's right end and carry the
	# 1224..1280 gap, trap T2 at 1296 and trap T3 at 1432 in one arc, landing on
	# L2 past all three. This is the schedule test_game.gd's
	# `high-road-clears-the-traps` already proves: walk off the plank, jump
	# inside the coyote window, air-jump 20 ticks later.
	#
	# The route this replaced tried to hop H1 -> H2 -> L2 instead. It reached H2
	# but the plank guard patrols 1356..1424 of a 1340..1440 plank, so the only
	# safe landing is a 16 px lip; landing at 1381 died on contact, and arriving
	# mid-swing did not save it either - the blade sweeps forward from the pivot
	# and the slime was closing from the right, inside the arc's near edge. H2 is
	# geometry, not a feature, so the film takes the route the game rewards.
	# Leave the plank, THEN jump, rather than jumping on a tick count. A fixed
	# 24 ticks is only inside the 6-tick coyote window if the walk started from
	# a standstill: at full speed the plank's 1224 edge arrives on tick 18, the
	# press lands on tick 24, and the coyote jump silently becomes the AIR jump
	# - which leaves nothing for the second press and drops the arc onto H2 and
	# its guard. That is exactly how take D died at (1418.7, 199.6).
	await hold_right(true)
	if not await until(func(): return not player.is_on_floor(), 150, "walked off the plank's right end"):
		return false
	await jump_once("off the plank, inside the coyote window")
	await step(20)
	await jump_once("air-jump over both traps")
	# The arc lands ON H2 (1340..1440) rather than over it: at x=1416 the feet
	# are 199.1, nine tenths of a pixel above the plank. Two earlier versions
	# of this ending were wrong about that. One walked across H2 to L2 and
	# called it the high road - it survived only because the guard happened to
	# be at the far end of its patrol that run, and take D, whose arc matches
	# to the pixel, landed on the guard and died at (1416.1, 199.1). The other
	# aimed for H2's left lip on purpose and died at (1354.5, 199.1), because
	# the guard patrols 1356..1424 of a 1340..1440 plank: there is no landing
	# on H2 that is safe independently of where the patrol happens to be.
	#
	# So don't land on it. The dash refilled on touching H1, and spent at the
	# apex it carries 66 px with vertical motion suspended, which puts the
	# descent past H2's right end entirely. The high road needs the dash twice:
	# once to get up, once to get out.
	if not await until(func(): return player.velocity.y >= -8.0, 60, "apex of the leap"):
		return false
	var dashes_before_exit: int = player.dashes
	await dash()
	if not expect(player.dashes == dashes_before_exit + 1, "the second dash clears the guarded plank"):
		return false
	if not await until(func(): return player.is_on_floor() and player.position.y > 300.0,
			300, "back down on the low road"):
		return false
	if not expect(session.enemies_killed == 0,
			"the high road went over the guard rather than through it"):
		return false
	if not expect(player.position.x > 1456.0,
			"landed past trap T3, so the high road skipped T1, T2 and T3"):
		return false
	if not expect(session.deaths == 0, "the whole high road, no deaths"):
		return false
	await hold_right(false)
	await step(24)
	note("take-c end", "x=%.1f deaths=%d killed=%d" % [
		player.position.x, session.deaths, session.enemies_killed])
	await step(48)
	return true

## Move the real pointer to a logical-canvas point and verify it arrived.
##
## The HUD start button is hit-tested against hud.get_local_mouse_position(),
## which reads the OS pointer, so an event position alone does nothing. The
## mapping from warp_mouse coordinates to the 640x360 logical canvas depends on
## the window size and the display scale, so rather than assume a factor this
## warps, measures the residual and corrects. Linear, so it converges at once,
## and it asserts the pointer is inside the target before anything is clicked.
func point_at_logical(target: Vector2, box: Rect2) -> bool:
	var guess: float = float(DisplayServer.window_get_size().x) / 640.0
	var probe := target * guess
	for attempt in range(6):
		Input.warp_mouse(probe)
		await step(1)
		var at: Vector2 = session.hud.get_local_mouse_position()
		if box.has_point(at):
			note("pointer on the start button", "logical=(%.1f, %.1f)" % [at.x, at.y])
			return true
		if at.is_equal_approx(Vector2.ZERO):
			break
		# Residual correction: probe maps to `at`, so scale the probe by the
		# ratio of where we wanted to be to where we landed.
		probe *= Vector2(target.x / maxf(at.x, 0.001), target.y / maxf(at.y, 0.001))
	failure = "could not place the pointer inside %s (last local %s)" % [
		str(box), str(session.hud.get_local_mouse_position())]
	return false

## Start the session from the HUD's mouse affordance rather than Enter.
func mouse_start() -> bool:
	if not await point_at_logical(Vector2(320.0, 232.0), Rect2(220, 215, 200, 34)):
		return false
	await click(true)
	await step(2)
	await click(false)
	return await until(func(): return session.state == session.State.PLAYING, 30, "started from the HUD button")

## Dash is a key like any other; it is refused on the ground by design.
func dash() -> void:
	await key(KEY_SHIFT, true, "dash")
	await step(2)
	await key(KEY_SHIFT, false, "dash")

## Take D - the ways this game says no: the focus-loss pause, the dash's two
## refusals, the jump buffer, and all three death reasons with their reaction
## and retry. Every death here is deliberate and every one is a real collision.
func take_d() -> bool:
	note("take-d begin")
	await step(30)
	if not await run_start():
		return false
	# Auto-pause when the window loses focus (session.gd:469). Triggered by
	# genuinely taking focus away: a second real OS window pops up and grabs
	# it, so the engine delivers its own focus_exited exactly as it would on
	# alt-tab. Window.notification(NOTIFICATION_WM_WINDOW_FOCUS_OUT) was tried
	# first and does nothing - that notification does not emit the signal - and
	# emitting focus_exited by hand would have demonstrated the handler rather
	# than the behaviour. The popup is a separate OS window, so it is not in
	# the recorded viewport.
	var thief := Window.new()
	thief.size = Vector2i(200, 120)
	thief.title = "focus thief"
	root.add_child(thief)
	thief.popup()
	thief.grab_focus()
	await step(6)
	note("another window took the focus")
	if not expect(session.state == session.State.PAUSED, "losing focus pauses the game"):
		return false
	await step(30)
	thief.queue_free()
	await step(6)
	await tap(KEY_ENTER, "resume")
	if not expect(session.state == session.State.PLAYING, "resumed after the focus pause"):
		return false
	await step(12)
	# The dash is refused on the ground. Nothing happens and nothing is spent.
	var dashes_before: int = player.dashes
	await dash()
	await step(3)
	if not expect(player.dashes == dashes_before, "the dash is refused while standing"):
		return false
	if not expect(player.dashes_left == player.tuning.air_dashes, "a refused dash costs nothing"):
		return false
	await step(12)
	# The jump buffer. Spend the air jump first, so the press below cannot be
	# taken by either the ground jump or the air jump - then it can only be the
	# buffer, and the two assertions separate "did not fire in the air" from
	# "fired on the landing frame".
	await jump_once("ground jump")
	await step(6)
	await jump_once("air jump, spending the air budget")
	await step(2)
	if not expect(player.air_jumps_left == 0, "the air jump is spent"):
		return false
	if not await until(func(): return player.velocity.y > 0.0 and player.position.y > 306.0,
			120, "falling back toward the floor"):
		return false
	var jumps_before: int = player.jumps
	await key(KEY_SPACE, true, "buffered jump press")
	await step(1)
	if not expect(player.jumps == jumps_before, "the buffered press does not fire in mid-air"):
		return false
	await key(KEY_SPACE, false, "buffered jump press")
	if not await until(func(): return player.jumps > jumps_before,
			player.tuning.buffer_ticks + 6, "the buffered jump fired on the landing frame"):
		return false
	await step(30)
	# DEATH 1 of 3 - the fall. Run off the 448 ledge and press nothing.
	if not await run_and_jump_at(138.0, 240):
		return false
	await step(24)
	if not await run_and_jump_at(292.0, 240):
		return false
	if not await run_until(func(): return player.is_on_floor() and player.position.x > 350.0,
			180, "landed past the spike"):
		return false
	if not await run_until(func(): return session.state == session.State.DYING,
			300, "fell into the gap"):
		return false
	if not expect(session.death_reason == "Missed the landing", "the fall names the fall"):
		return false
	if not expect(session.death_fx_remaining > 0.0, "the death reaction plays for a fall too"):
		return false
	await hold_right(false)
	if not await until(func(): return session.state == session.State.PLAYING, 90, "automatic retry"):
		return false
	await step(24)
	# DEATH 2 of 3 - the pop-up trap, watched rather than jumped. Cross T1's
	# trigger at 1064, then STAND at 1070, 90 px clear of the spike at
	# 1160..1184, so the rise is on screen with nothing at risk.
	if not await run_and_jump_at(138.0, 240):
		return false
	await step(24)
	if not await run_and_jump_at(292.0, 240):
		return false
	await step(30)
	if not await run_and_jump_at(424.0, 240):
		return false
	await step(30)
	if not await run_and_jump_at(548.0, 240):
		return false
	await step(26)
	if not await run_and_jump_at(712.0, 300):
		return false
	await step(30)
	if not await run_and_jump_at(930.0, 300):
		return false
	if not await run_until(func(): return player.is_on_floor() and player.position.x >= 1070.0,
			300, "across T1's trigger at 1064"):
		return false
	await hold_right(false)
	if not expect(session.trap_risen[0] > 0, "the trap started rising when the trigger was crossed"):
		return false
	if not await until(func(): return session.trap_risen[0] >= session.TRAP_RISE_TICKS,
			40, "the trap is fully up"):
		return false
	if not expect(player.position.x < 1140.0, "watched the rise from clear of the spike"):
		return false
	note("trap fully risen", "player_x=%.1f spike=1160..1184" % player.position.x)
	await step(36)
	# The dash confers no invulnerability. Jump, then dash within three ticks,
	# while the feet are still inside the spike's 304..320 band, and drive
	# straight through it. This is the same overlap test a walk-in uses.
	if not await run_until(func(): return player.position.x >= 1130.0 and player.is_on_floor(),
			120, "in position beside the spike"):
		return false
	await hold_right(false)
	await step(8)
	await jump_once("jump beside the spike")
	await dash()
	if not await until(func(): return session.state == session.State.DYING,
			120, "dashed into the risen spike"):
		return false
	if not expect(session.death_reason == "Watch the spikes", "the dash gave no invulnerability"):
		return false
	if not await until(func(): return session.state == session.State.PLAYING, 90, "automatic retry"):
		return false
	await step(24)
	# DEATH 3 of 3 - an enemy, on the low road. The high road was tried first
	# and is the wrong tool: its arc lands on H2 at (1416, 199) among the plank
	# guard's patrol, so the death it produces is a plank accident rather than
	# the walk-into-a-slime this beat is for. take B's route crosses the fork
	# and the traps with the sword down, and the first ground slime patrols
	# 1580..1690 on the platform right after it - so stop at 1560 and walk.
	# Stop at 1500, not 1560. run_course() stands and fights any ground enemy
	# within 48 px REGARDLESS of slash_from - that rule is what gets it through
	# the enemy half - so stopping at 1560 let it kill this very slime on the
	# way in, and the take walked the whole platform and fell in the 1728..1792
	# gap at (1785.1, 435.9) instead. The patrol's left bound is 1580, so 1500
	# is 80 px clear of the closest it ever comes.
	if not await run_course(1500.0, 1.0e9):
		return false
	if not expect(session.deaths == 2, "no accidental deaths on the way to the slime"):
		return false
	if not expect(session.enemies_killed == 0, "the slime is still alive to walk into"):
		return false
	if not expect(player.position.x >= 1500.0, "reached the platform before the first slime"):
		return false
	if not await run_until(func(): return session.state == session.State.DYING,
			300, "walked into the slime"):
		return false
	if not expect(session.death_reason == "It got you", "the enemy names the enemy"):
		return false
	await hold_right(false)
	if not expect(session.deaths == 3, "three deliberate deaths, three reasons"):
		return false
	if not await until(func(): return session.state == session.State.PLAYING, 90, "automatic retry"):
		return false
	note("take-d end", "deaths=%d" % session.deaths)
	await step(36)
	return true

func run_start() -> bool:
	await tap(KEY_ENTER, "start")
	return await until(func(): return session.state == session.State.PLAYING, 30, "session started")

# --- entry ------------------------------------------------------------------

func write_log() -> void:
	var dir := OS.get_environment("WALKER_LOG_DIR")
	if dir == "":
		dir = ProjectSettings.globalize_path("res://../evidence")
	DirAccess.make_dir_recursive_absolute(dir)
	var f := FileAccess.open("%s/take-%s-inputs.jsonl" % [dir, take], FileAccess.WRITE)
	for line in log_lines:
		f.store_line(line)
	f.close()
	print("input log: %s/take-%s-inputs.jsonl (%d entries)" % [dir, take, log_lines.size()])

func run() -> void:
	take = OS.get_environment("WALKER_TAKE")
	if take == "":
		take = "a"
	DisplayServer.window_set_size(Vector2i(3840, 2160))
	scene = load("res://game/main.tscn").instantiate()
	root.add_child(scene)
	session = scene
	await step(3)
	player = session.player
	print("take=%s  viewport=%s  logical=%dx%d" % [
		take, str(DisplayServer.window_get_size()),
		ProjectSettings.get_setting("display/window/size/viewport_width"),
		ProjectSettings.get_setting("display/window/size/viewport_height")])
	var ok: bool = false
	if take == "b":
		ok = await take_b()
	elif take == "c":
		ok = await take_c()
	elif take == "d":
		ok = await take_d()
	else:
		ok = await take_a()
	write_log()
	if not ok:
		printerr("CAPTURE FAILED: " + failure)
		print("CAPTURE FAILED after %d ticks (%.2f s)" % [tick, float(tick) / 60.0])
		quit(1)
		return
	print("CAPTURE OK: take=%s ticks=%d (%.2f s at 60 fps)" % [take, tick, float(tick) / 60.0])
	quit(0)
