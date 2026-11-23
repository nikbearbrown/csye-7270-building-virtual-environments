# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: run directly with --script, no scene needed; it loads base.tscn itself
## A7 edge tests for the committing action (the one-handed raise), at every phase boundary of CHANGE-BRIEF's phase table, with an interrupt in each phase.
## Run: ./scripts/run-test.sh test_tablet_raise_edges.gd 60
## Frame map (measured, CHANGE-BRIEF revision "2 physics frames late"): the press is read on physics frame N (clip frame 0); the clip's position read on
## physics frame N + k is (k - 2) / 60 s, so clip frame f (f / 30 s) is read on N + 2 + 2f; "raise finished" is read on N + 42.
## What it can prove: driven by real key events at 60 fps, the screen, the raise query, the movement lock, the clip position at each boundary, and what an
## interrupt in startup, active or recovery does. What it cannot prove: how the motion looks (frame strip and my eyes).

# ============================================================
# Constants: the numbers from the brief and the measured frame map
# ============================================================
const BASE_SCENE := "res://base.tscn"  # The main game scene with the player
const SPAWN := Vector3(2.0, 0.25, 1.5)  # The player's spawn point; we reset to it before each case
const CLIP_FPS := 30.0  # The phase table's frame rate
const PHYSICS_FPS := 60.0  # The wrapper pins --fixed-fps 60
const READ_LAG := 2  # Measured: physics frames between a clip frame's time and the game reading it
const FINISH_FRAME := 42  # Measured: "raise finished" (screen lit, raise over) is read on physics frame N + 42
const PHASES := [["startup", 0], ["active", 7], ["recovery", 16], ["end", 20]]  # Phase name and the clip frame it begins on
const INTERRUPT_AT := {"startup": 6, "active": 20, "recovery": 36}  # Physics frame N + k where we interrupt: clip frames about 2, 9 and 17
const SETTLE_FRAMES := 90  # 1.5 s: enough for any raise or blend to finish
const BLEND_FRAMES := 12  # The 0.2 s cross-fade at 60 fps
const POS_EPS := 1.0 / PHYSICS_FPS + 0.0001  # Tolerance on the clip position: one physics frame
const HIP_EPS := 0.03  # How close (m) the tablet must come back to its hip position after a put-away interrupt
const TEST_LONG_PRESS := 0.095  # For this test only, a long press fires after 6 physics frames instead of 0.4 s (PlayerController.tablet_long_press_seconds), so a long press can land inside the 7-frame startup
const LONG_FRAMES := 6  # Physics frames the key is down when the long press fires at TEST_LONG_PRESS

# ============================================================
# Member variables: what the test records while it runs
# ============================================================
var failures := 0  # How many checks failed
var player: Humanoid  # The player body (driven through its real brain)
var playback: AnimationNodeStateMachinePlayback  # The state machine's playback, read only
var change_frame := -1  # The physics frame of the latest tablet_hold_changed
var hip_position := Vector3.ZERO  # Where the tablet is (relative to the body) when it is put away and settled

# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (these act as the entry points)
# ============================================================
## Called by Godot once when the script starts as the SceneTree. Starts the whole run.
func _initialize() -> void:
	_run()


# ============================================================
# Functions: the parts of the run
# ============================================================
## The whole run: load the scene, check an uninterrupted raise frame by frame, then interrupt it in each phase both ways; print the result and quit.
func _run() -> void:
	var base: Node = load(BASE_SCENE).instantiate()
	root.add_child(base)
	player = base.get_node("Player") as Humanoid
	player.tablet_hold_changed.connect(func(_o, _n): change_frame = Engine.get_physics_frames())  # We write down the physics frame of every hold change
	await _frames(SETTLE_FRAMES)
	playback = player.get_node("AnimationTree").get("parameters/playback")
	player.get_node("PlayerController").tablet_long_press_seconds = TEST_LONG_PRESS  # A tuning value on the brain, changed only inside this test
	hip_position = _tablet_local()  # The put-away tablet position, for checking that a put-away interrupt really goes back
	await _uninterrupted_raise()
	for phase in ["startup", "active", "recovery"]:
		await _interrupt(phase, "short")
		await _interrupt(phase, "long")
	print("== %s: %d failure(s) ==" % ["ALL PASS" if failures == 0 else "FAILED", failures])
	quit(1 if failures > 0 else 0)


## Records one check: prints PASS if it passed, otherwise prints FAIL and counts it.
func _check(ok: bool, what: String) -> void:
	print(("  PASS  " if ok else "  FAIL  ") + what)
	if not ok:
		failures += 1


## Waits the given number of physics frames.
func _frames(count: int) -> void:
	for i in count:
		await physics_frame


## Waits until the physics frame with the given number has started (the brain has not run yet in it, so input set now is read in it).
func _until_frame(frame: int) -> void:
	while Engine.get_physics_frames() < frame:
		await physics_frame


## The tablet's position relative to the body, so it does not depend on where the body stands.
func _tablet_local() -> Vector3:
	return player.global_transform.affine_inverse() * player.get_tablet().global_position


## Puts the tablet away (if it is out), puts the player back on its spawn point and waits until everything has settled.
func _reset() -> void:
	Input.action_release(&"move_forward")
	if player.get_tablet_hold() != Humanoid.TabletHold.NONE:
		await _short_press_now()
		if player.get_tablet_hold() != Humanoid.TabletHold.NONE:
			await _short_press_now()  # From two hands a short press goes to one hand, so a second press puts it away
	player.global_position = SPAWN
	player.velocity = Vector3.ZERO
	await _frames(SETTLE_FRAMES)


## A short Tab press whose release is read on the next physics frame; returns once that frame has run.
func _short_press_now() -> void:
	Input.action_press(&"tablet")
	await _frames(2)
	Input.action_release(&"tablet")  # The brain reads "released before the long-press time" on the next physics frame: that frame turns into a short press
	await _frames(2)


## Takes the tablet out with a short press and returns N, the physics frame on which the brain read it; it returns at the start of frame N + 1.
func _take_out() -> int:
	change_frame = -1
	Input.action_press(&"tablet")
	await _frames(2)
	Input.action_release(&"tablet")  # The brain reads a short press on the next physics frame
	while change_frame == -1:
		await physics_frame  # We wait only until the hold has changed, so the checks can start on the very next frame
	return change_frame


## One uninterrupted raise, frame by frame: screen dark and raise under way through N + 41, both flip on N + 42; the clip position on each phase boundary;
## and holding the walk key the whole time moves the player only after the raise.
func _uninterrupted_raise() -> void:
	await _reset()
	var n := await _take_out()
	Input.action_press(&"move_forward")  # From just after the press we hold walk: the lock must hold it back for the whole raise
	_check(n > 0 and player.get_tablet_hold() == Humanoid.TabletHold.ONE_HAND, "raise: the short press took the tablet out (read on physics frame N = %d)" % n)
	var dark_ok := true  # Screen dark on every frame N .. N+41
	var raising_ok := true  # Raise query true on every frame N .. N+41
	var still_ok := true  # Player not moving on every frame N .. N+42 (the intent for N+42 is built before the raise ends)
	var positions := {}  # Clip position as read by the game on each physics frame
	while Engine.get_physics_frames() <= n + FINISH_FRAME + 4:
		await physics_frame
		# At the start of physics frame F the body's values are those its frame F - 1 left, and the clip position is the one frame F will read
		var body_k := Engine.get_physics_frames() - 1 - n
		var clip_k := Engine.get_physics_frames() - n
		positions[clip_k] = playback.get_current_play_position() if playback.get_current_node() == &"raise_1h" else -1.0
		if body_k < 1:
			continue  # Frame N itself still built its intent before the press was read, so we start checking from N + 1
		var speed := Vector2(player.velocity.x, player.velocity.z).length()
		if body_k < FINISH_FRAME:
			dark_ok = dark_ok and not player.is_tablet_screen_lit()
			raising_ok = raising_ok and player.is_raising_tablet()
		if body_k <= FINISH_FRAME:
			still_ok = still_ok and speed < 0.01
	Input.action_release(&"move_forward")
	_check(dark_ok, "raise: screen dark on every physics frame N+1 .. N+41")
	_check(raising_ok, "raise: is_raising_tablet() true on every physics frame N+1 .. N+41 (no walking, running or jumping)")
	_check(still_ok, "raise: walk held from N+1, the player does not move through N+42")
	_check(player.is_tablet_screen_lit() and not player.is_raising_tablet(), "raise: screen lit and raise over from N+42 (clip frame 20, read 2 frames late)")
	_check(Vector2(player.velocity.x, player.velocity.z).length() > 0.5, "raise: walking resumes right after the raise")
	for phase in PHASES:
		var f: int = phase[1]
		var k: int = READ_LAG + 2 * f  # The physics frame on which clip frame f is read
		if f == 20:
			continue  # Frame 20 is the end: checked above as the screen lighting
		var want := f / CLIP_FPS
		_check(positions.has(k) and absf(positions[k] - want) <= POS_EPS,
			"raise: %s begins on clip frame %d, read on N+%d at position %.3f s (got %.3f)" % [phase[0], f, k, want, positions.get(k, -9.0)])


## One interrupt: start the raise, then on physics frame N + INTERRUPT_AT[phase] make a short press (put it back) or a long press (switch to two hands).
func _interrupt(phase: String, kind: String) -> void:
	await _reset()
	var n := await _take_out()
	var m: int = n + INTERRUPT_AT[phase]  # The physics frame on which the brain must read the interrupt
	if kind == "short":
		await _until_frame(m - 3)
		Input.action_press(&"tablet")
		await _until_frame(m)
		Input.action_release(&"tablet")  # Released at the start of frame m: the brain reads a short press in m
	else:
		await _until_frame(m - LONG_FRAMES + 1)  # A long press fires on the frame the key has been down LONG_FRAMES physics frames, which is frame m
		Input.action_press(&"tablet")
		await _until_frame(m)
	var position_at := playback.get_current_play_position()  # The clip position frame m reads, before the press changes anything
	var in_raise := playback.get_current_node() == &"raise_1h"
	await _frames(1)  # Let frame m run
	if kind == "long":
		Input.action_release(&"tablet")
	var tag := "%s interrupt (%s press on N+%d)" % [phase, kind, INTERRUPT_AT[phase]]
	_check(in_raise, "%s: the raise was still playing when the press was read (clip at %.3f s)" % [tag, position_at])
	_check(change_frame == m, "%s: the hold changed on exactly that physics frame (got N+%d)" % [tag, change_frame - n])
	_check(not player.is_raising_tablet(), "%s: the raise is over at once (movement unlocked)" % tag)
	var lit_frame := -1
	for i in SETTLE_FRAMES:
		await physics_frame
		if lit_frame == -1 and player.is_tablet_screen_lit():
			lit_frame = i
	if kind == "short":
		_check(player.get_tablet_hold() == Humanoid.TabletHold.NONE, "%s: the tablet is put away" % tag)
		_check(lit_frame == -1, "%s: the screen never lit" % tag)
		_check(playback.get_current_node() == &"hip", "%s: the state machine is back in hip" % tag)
		_check(_tablet_local().distance_to(hip_position) < HIP_EPS, "%s: the tablet is back on the hip (%.3f m away)" % [tag, _tablet_local().distance_to(hip_position)])
	else:
		_check(player.get_tablet_hold() == Humanoid.TabletHold.TWO_HAND, "%s: the hold is two-handed" % tag)
		_check(playback.get_current_node() == &"hold_2h", "%s: the state machine is in hold_2h" % tag)
		_check(lit_frame >= BLEND_FRAMES - 1 and lit_frame <= BLEND_FRAMES + READ_LAG + 1, "%s: dark during the 0.2 s blend, lit right after it (lit %d frames later)" % [tag, lit_frame + 1])
