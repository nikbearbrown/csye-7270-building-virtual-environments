extends SceneTree
## Input-only capture driver for the Brutalist godot-gamedev film.
##
## Same contract as `capture_walkthrough.gd`, which this follows deliberately
## rather than reusing, so Assignment 1's film stays byte-reproducible from its
## own driver:
##
##   - Instantiate the REAL main scene, not a hand-built session.
##   - Drive it through real InputEvents. `test_*` hooks bypass the InputMap and
##     teleport the player; they are useful checks and explicitly NOT footage.
##     `Input.action_press()` is also insufficient: it sets the polled action
##     state but produces no event, so it never reaches `_unhandled_input`,
##     where the menu, pause, retry and replay keys live.
##   - Log every action against the game tick, AND log every change of
##     `player.pose_key()`, because the pose mapping is what this film is about.
##   - Assert the expected result. Exhausting `--quit-after` is not success.
##
## Two takes, selected by WALKER_TAKE:
##
##   p — poses. Idle, run, rise, fall, land, jump, air dash, land, swing.
##       Seven of the eight generated poses, plus the code-drawn blade coming
##       out of the hand it is drawn from.
##   t — the trap. The run out to trap 0, the warning on the arming tick, and
##       the death that follows it, which is also the prone pose.
##
##   WALKER_TAKE=p godot --path godot --script res://tests/capture_gamedev.gd \
##     --write-movie <dir>/frame.png --fixed-fps 60 --quit-after <n>

var scene: Node
var session: Node2D
var player: CharacterBody2D
var tick: int = 0
var log_lines: Array[String] = []
var take: String = "p"
var failure: String = ""
var deaths_seen: int = 0
var last_pose: String = ""

func _initialize() -> void:
	call_deferred("run")

# --- plumbing ---------------------------------------------------------------

func note(action: String, detail: String = "") -> void:
	var entry := {
		"tick": tick,
		"t_s": snappedf(float(tick) / 60.0, 0.001),
		"action": action,
		"state": session.state if session else -1,
		"pose": player.pose_key() if player else "",
		"player_x": snappedf(player.position.x, 0.01) if player else 0.0,
		"player_y": snappedf(player.position.y, 0.01) if player else 0.0,
	}
	if detail != "":
		entry["detail"] = detail
	log_lines.append(JSON.stringify(entry))

func step(n: int = 1) -> void:
	for i in range(n):
		await physics_frame
		await process_frame
		tick += 1
		if session and session.deaths > deaths_seen:
			deaths_seen = session.deaths
			note("DIED", "%s at (%.1f, %.1f)" % [
				session.death_reason, player.position.x, player.position.y])
		# The pose mapping is the film's first component, so every transition
		# is a logged event rather than something inferred from the footage.
		if player:
			var pose: String = player.pose_key()
			if pose != last_pose:
				last_pose = pose
				note("POSE " + pose)

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

var d_held: bool = false

func hold_right(on: bool) -> void:
	if on != d_held:
		await key(KEY_D, on, "move-right")
		d_held = on

## Jump height is fixed, so hold duration is not a gameplay variable; releasing
## after one frame keeps the input log unambiguous.
func jump_once(label: String) -> void:
	await key(KEY_SPACE, true, label)
	await step(1)
	await key(KEY_SPACE, false, label)

func until(check: Callable, limit: int, label: String) -> bool:
	for i in range(limit):
		if check.call():
			return true
		await step(1)
	failure = "timed out waiting for " + label
	return false

func run_until(check: Callable, limit: int, label: String) -> bool:
	await hold_right(true)
	return await until(check, limit, label)

func at_least(x: float) -> Callable:
	return func() -> bool: return player.position.x >= x

func start_run() -> bool:
	await step(12)
	await tap(KEY_ENTER, "start")
	if not await until(func() -> bool: return session.state == 1, 60, "PLAYING"):
		return false
	await step(6)
	return true

# --- take p: the poses ------------------------------------------------------

func take_p() -> bool:
	if not await start_run():
		return false
	# Idle first, so the film has an unambiguous P1 before anything moves.
	await step(30)
	# Run east along the opening platform, then jump the 48 px step at x 160.
	if not await run_until(at_least(132.0), 240, "x >= 132"):
		return false
	await jump_once("jump the step")
	if not await until(func() -> bool: return player.position.y < 312.0, 40, "airborne"):
		return false
	await step(24)
	if not await until(func() -> bool: return player.is_on_floor(), 90, "landing"):
		return false
	await hold_right(false)
	await step(18)
	# Jump again and spend the air dash at the top, which is the only state
	# that produces the dash pose.
	await jump_once("jump for the dash")
	await step(10)
	await tap(KEY_SHIFT, "air dash", 3)
	if player.dashes != 1:
		failure = "air dash was refused (dashes=%d)" % player.dashes
		return false
	if not await until(func() -> bool: return player.is_on_floor(), 120, "landing after the dash"):
		return false
	await step(20)
	# The swing, on the ground, with nothing to kill: this beat is about the
	# blade coming from the hand, not about damage.
	await click(true)
	await step(2)
	await click(false)
	if not await until(func() -> bool: return player.attack_phase() == 2, 30, "the live window"):
		return false
	await step(26)
	if player.attacks != 1:
		failure = "the swing did not happen (attacks=%d)" % player.attacks
		return false
	# Keep going east for a second helping of the same states, so the result
	# beats have motion to spend instead of a frozen frame. The first cut of
	# this take was 4.3 s against a 10.6 s narration, which is a seven-second
	# held still - a fair device for a moment, not for most of a beat.
	await step(12)
	# 548 again. This is the third time the block at x 576 has stopped a take in
	# this file; it is written out in take t's comment and it still caught me
	# here. The level's walls set these marks, not my reading of the geometry.
	for mark in [424.0, 548.0, 712.0]:
		if not await run_until(at_least(mark), 300, "x >= %.0f" % mark):
			return false
		await jump_once("jump at %.0f" % mark)
		await step(26)
		if not await until(func() -> bool: return player.is_on_floor(), 120, "landing"):
			return false
	await hold_right(false)
	await step(16)
	# A second swing, facing right on flat ground, for the blade beat.
	await click(true)
	await step(2)
	await click(false)
	if not await until(func() -> bool: return player.attack_phase() == 2, 30, "the second live window"):
		return false
	await step(30)
	if player.attacks != 2:
		failure = "the second swing did not happen (attacks=%d)" % player.attacks
		return false
	if session.deaths != 0:
		failure = "take p died (%d)" % session.deaths
		return false
	await step(20)
	return true

# --- take t: the trap warning, and the death it precedes --------------------

func take_t() -> bool:
	if not await start_run():
		return false
	# The jump marks are the level's geometry, not taste: the 16 px step at
	# x 160, the fixed spike at x 320, and the gaps at 448-512, 736-784 and
	# 960-1008.
	#
	# Two of these marks were found by the take stalling, not by reading the
	# level: 132 after it stopped at x 151.0 against the side of the 16 px
	# step, and 548 after it stopped at x 567.0 against the 32 px block at
	# x 576. Both times the pose in the log went back to `idle` while the
	# move-right key was still held, which is what a wall looks like from the
	# input log. `move_and_slide` does not step up.
	for mark in [132.0, 292.0, 424.0, 548.0, 712.0, 930.0]:
		if not await run_until(at_least(mark), 400, "x >= %.0f" % mark):
			return false
		await jump_once("jump at %.0f" % mark)
		await step(26)
		if not await until(func() -> bool: return player.is_on_floor(), 120, "landing"):
			return false
	# Walk into trap 0's trigger at x 1064 and do NOT jump. The warning fires
	# on the tick `trap_risen` leaves 0; the spike starts at x 1160.
	await hold_right(true)
	if not await until(func() -> bool: return session.trap_risen[0] > 0, 400, "trap 0 arming"):
		return false
	note("TRAP ARMED", "trap_risen[0]=1 at x=%.1f" % player.position.x)
	if not await until(func() -> bool: return session.state == 3, 240, "the death"):
		return false
	await hold_right(false)
	# Read the sound log BEFORE holding for the footage. `restart_attempt()`
	# clears `sfx_log` so it stays bounded and a test never subtracts a
	# previous life's events -- which means the evidence has to be taken inside
	# the attempt that produced it. The first version of this take held for
	# 90 ticks first and then found the log empty.
	var warned := -1
	var died := -1
	for e in session.sfx_log:
		if e["id"] == "trap" and warned < 0:
			warned = e["tick"]
		if e["id"] == "death" and died < 0:
			died = e["tick"]
	# Hold on the prone pose. The retry is 0.55 s and the reaction outlasts it,
	# so this window shows P8 and then the respawn.
	await step(90)
	if warned < 0 or died < 0:
		failure = "sfx_log is missing the trap warning or the death (%s)" % str(session.sfx_log)
		return false
	var lead: int = died - warned
	note("WARNING LEAD", "warned=%d died=%d lead=%d ticks" % [warned, died, lead])
	if lead < 15:
		failure = "the warning led the death by only %d ticks" % lead
		return false
	if session.deaths != 1:
		failure = "expected exactly one death, got %d" % session.deaths
		return false
	return true

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
		take = "p"
	DisplayServer.window_set_size(Vector2i(3840, 2160))
	scene = load("res://game/main.tscn").instantiate()
	root.add_child(scene)
	session = scene
	await step(3)
	player = session.player
	print("take=%s  viewport=%s  logical=%dx%d  poses=%d" % [
		take, str(DisplayServer.window_get_size()),
		ProjectSettings.get_setting("display/window/size/viewport_width"),
		ProjectSettings.get_setting("display/window/size/viewport_height"),
		player.pose_tex.size()])
	var ok: bool = false
	if take == "t":
		ok = await take_t()
	else:
		ok = await take_p()
	write_log()
	if not ok:
		printerr("CAPTURE FAILED: " + failure)
		print("CAPTURE FAILED after %d ticks (%.2f s)" % [tick, float(tick) / 60.0])
		quit(1)
		return
	print("CAPTURE OK: take=%s ticks=%d (%.2f s at 60 fps)" % [take, tick, float(tick) / 60.0])
	quit(0)
