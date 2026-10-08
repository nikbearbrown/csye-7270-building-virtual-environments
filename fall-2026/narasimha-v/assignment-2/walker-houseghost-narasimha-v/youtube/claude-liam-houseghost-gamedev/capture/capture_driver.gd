extends SceneTree
## Capture driver for the HOUSEGHOST Night-1 slice.
##
## Drives the real main scene with real input actions only: no teleporting, no
## seeding of state, no calling game functions directly. Every step waits on a
## condition the game itself reports, so the run either reaches a genuine
## contact or fails; exhausting the clock is a failure, not a pass.
##
## Writes capture/run-01-inputs.jsonl: one record per action, stamped with the
## engine tick and the elapsed seconds the capture was rendered at.

const RELIC_X := 1548.0
const RELIC2_X := 3150.0   ## his shoes, still by the door
## Where the floor stops. Measured from the scene's own collision shapes, not
## guessed: segments run -200..1180, 1350..2520, 2690..3860, 4030..5960, so the
## three gaps open at these x positions and are 170 px wide.
const GAP_STARTS := [1180.0, 2520.0, 3860.0]
const SPEED_SETTLE := 0.35

var _scene: Node
var _player: Node
var _meters: Node
var _log: FileAccess
var _tick := 0
var _t := 0.0
var _phase := "boot"
var _phase_t := 0.0
var _held := {}
var _opening_presses := 0
var _press_cooldown := 0.0
var _rec_at_contact := -1
var _days_before_fall := 99
var _stroll_log := 0.0
var _last_x := -1.0
var _stuck_for := 0.0
var _jump_cooldown := 0.0
## The jump is height-modulated: releasing early multiplies the rise by
## JUMP_CUT (0.45). A press-and-release in the same frame is therefore the
## shortest hop in the game, not a normal one, and will not clear a 170 px gap.
## Holding for this long gives the full arc a player gets.
const JUMP_HOLD := 0.30
var _jump_release_in := 0.0
## The relic arms on a press edge and resolves on the release, so the two have
## to be separated by real frames; a press and release inside one frame is
## coalesced and never arms anything.
const CONTACT_HOLD := 0.12
var _contact_release_in := 0.0
var _failed := ""

func _initialize() -> void:
	var path := "user://run-01-inputs.jsonl"
	if OS.has_environment("CAPTURE_LOG"):
		path = OS.get_environment("CAPTURE_LOG")
	_log = FileAccess.open(path, FileAccess.WRITE)
	change_scene_to_file("res://scenes/Bedroom.tscn")

func _note(event: String, detail: Dictionary = {}) -> void:
	var rec := {"tick": _tick, "t_s": snappedf(_t, 0.001), "event": event, "phase": _phase}
	for k in detail:
		rec[k] = detail[k]
	if _log:
		_log.store_line(JSON.stringify(rec))
	print("[%6.2fs] %-14s %s" % [_t, event, JSON.stringify(detail)])

## The project binds most verbs to physical keys and handles the flip in
## _unhandled_input, so a synthesized action never reaches it: Input.action_press
## only sets the polled state. Everything here is therefore a real InputEventKey,
## which both reaches _unhandled_input and updates the polled state.
const KEYS := {
	"move_right": {"physical": 68, "label": "D"},
	"move_left":  {"physical": 65, "label": "A"},
	"jump":       {"keycode": 32,  "label": "Space"},
	"flip_world": {"physical": 70, "label": "F"},
	"contact":    {"physical": 69, "label": "E"},
}

func _send(action: String, pressed: bool) -> void:
	var k: Dictionary = KEYS[action]
	var ev := InputEventKey.new()
	if k.has("physical"):
		ev.physical_keycode = k["physical"]
	else:
		ev.keycode = k["keycode"]
	ev.pressed = pressed
	Input.parse_input_event(ev)

func _press(action: String) -> void:
	if _held.has(action):
		return
	_send(action, true)
	_held[action] = true
	_note("key_down", {"action": action, "key": KEYS[action]["label"]})

func _release(action: String) -> void:
	if _held.has(action):
		_send(action, false)
		_held.erase(action)
		_note("key_up", {"action": action, "key": KEYS[action]["label"]})

func _release_all() -> void:
	for a in _held.keys():
		_send(a, false)
	if not _held.is_empty():
		_note("release_all", {"actions": _held.keys()})
	_held.clear()

## The opening advances on any key; space matches what the sound-trigger test
## uses, so both drive the game the same way.
func _key_tap(code: Key, label: String) -> void:
	var down := InputEventKey.new()
	down.keycode = code
	down.physical_keycode = code
	down.pressed = true
	Input.parse_input_event(down)
	var up := InputEventKey.new()
	up.keycode = code
	up.physical_keycode = code
	up.pressed = false
	Input.parse_input_event(up)
	_note("key", {"key": label})

## A kind contact: a short deliberate tap, not a held charge.
func _reach_out() -> void:
	if _held.has("contact"):
		return
	_press("contact")
	_contact_release_in = CONTACT_HOLD


## A jump the way a player makes one: held long enough not to be cut short.
func _jump() -> void:
	if _held.has("jump"):
		return
	_press("jump")
	_jump_release_in = JUMP_HOLD


func _tap(action: String) -> void:
	_send(action, true)
	_send(action, false)
	_note("key_tap", {"action": action, "key": KEYS[action]["label"]})

func _go(next: String) -> void:
	_note("phase", {"from": _phase, "to": next})
	_phase = next
	_phase_t = 0.0

func _fail(why: String) -> void:
	_failed = why
	_note("FAIL", {"reason": why})
	_release_all()
	quit(1)

func _process(delta: float) -> bool:
	_tick += 1
	_t += delta
	_phase_t += delta
	_press_cooldown = maxf(0.0, _press_cooldown - delta)
	if _t > 150.0:
		_fail("global time cap reached; the run did not complete")
		return true
	_jump_cooldown = maxf(0.0, _jump_cooldown - delta)
	if _jump_release_in > 0.0:
		_jump_release_in -= delta
		if _jump_release_in <= 0.0:
			_release("jump")
	if _contact_release_in > 0.0:
		_contact_release_in -= delta
		if _contact_release_in <= 0.0:
			_release("contact")

	if _scene == null:
		_scene = current_scene
		if _scene == null:
			return false
		_player = _scene.get_node_or_null("Player")
		_meters = _scene.get_node_or_null("Meters")
		if _player == null or _meters == null:
			_fail("Player or Meters missing from the main scene")
			return true
		_note("scene_ready", {"player_x": _player.position.x, "days": _meters.days_left})
		_go("opening")
		return false

	match _phase:
		"opening":
			# The opening advances only on a key press, by design. Press until
			# the game hands control over; that is the game's own signal.
			if _player.controllable and not _scene._awaiting_key:
				_note("control_handed_over", {"presses": _opening_presses, "x": _player.position.x})
				_go("walk_to_relic")
			elif _press_cooldown <= 0.0:
				_key_tap(KEY_SPACE, "space")
				_opening_presses += 1
				_press_cooldown = 0.9
				if _opening_presses > 12:
					_fail("opening never handed over control after 12 presses")
			if _phase_t > 25.0:
				_fail("opening timed out")

		"walk_to_relic":
			if not _held.has("move_right"):
				_press("move_right")
			# Jump the gap rather than walking into it. Holding right without
			# this costs every night in a few seconds: the fall catcher sets the
			# player down again short of the same hole, so they walk straight
			# back into it until the nights run out.
			for g in GAP_STARTS:
				if _player.position.x > g - 110.0 and _player.position.x < g - 30.0 and _jump_cooldown <= 0.0:
					_jump()
					_jump_cooldown = 0.55
					_note("jump_gap", {"gap_x": g, "x": snappedf(_player.position.x, 1.0)})
			if _meters.ended:
				_fail("the night ended before reaching the relic (fell into a gap)")
			if _player.position.x >= RELIC_X - 40.0:
				_release_all()
				_note("reached_relic_x", {"x": _player.position.x, "moved": _scene._has_moved})
				_go("settle")
			elif _phase_t > 30.0:
				_fail("never reached the relic x position")

		"settle":
			if _phase_t > SPEED_SETTLE:
				_go("flip")

		"flip":
			if not _scene.is_inverted:
				if _press_cooldown <= 0.0:
					_tap("flip_world")
					_press_cooldown = 1.2
			else:
				_note("world_inverted", {"has_flipped": _scene._has_flipped})
				_go("reach")
			if _phase_t > 8.0:
				_fail("world never inverted")

		"reach":
			# Walk under the relic in the inverted world and jump toward it.
			var dx: float = RELIC_X - _player.position.x
			if absf(dx) > 30.0:
				var want := "move_right" if dx > 0.0 else "move_left"
				var other := "move_left" if dx > 0.0 else "move_right"
				_release(other)
				if not _held.has(want):
					_press(want)
			else:
				_release_all()
			# Inverted, he stands on the ceiling and jumps *down* the screen,
			# because up_direction has flipped. The music box hangs below that
			# ceiling, so reaching it is a jump, and the hand has to go out while
			# he is inside the relic's area rather than on the way past it.
			if _jump_cooldown <= 0.0:
				_jump()
				_jump_cooldown = 0.9
			if _press_cooldown <= 0.0:
				_reach_out()
				_press_cooldown = 0.22
			if _meters.recognition > 0:
				_release_all()
				_rec_at_contact = _meters.recognition
				_note("contact_landed", {"recognition": _meters.recognition, "days_left": _meters.days_left})
				_go("watch")
			if _phase_t > 25.0:
				_fail("contact never landed in the inverted world")

		"watch":
			# Hold still and let the consequence play: the child turns, a day tears.
			if _phase_t > 3.0:
				_go("flip_back")

		"flip_back":
			if _scene.is_inverted:
				if _press_cooldown <= 0.0:
					_tap("flip_world")
					_press_cooldown = 1.2
			else:
				_note("world_upright", {})
				_go("stroll")
			if _phase_t > 8.0:
				_fail("world never returned upright")

		"stroll":
			# Upright, in the room he remembers. His own furniture is solid here
			# and theirs is not, so this walk ends against a shelf that only
			# exists in the memory. That is the obstacle design working, not a
			# stuck driver: the way past it is to stop remembering.
			if not _held.has("move_right"):
				_press("move_right")
			for g in GAP_STARTS:
				if _player.position.x > g - 110.0 and _player.position.x < g - 30.0 and _jump_cooldown <= 0.0:
					_jump()
					_jump_cooldown = 0.55
					_note("jump_gap", {"gap_x": g, "x": snappedf(_player.position.x, 1.0)})
			if _meters.ended:
				_fail("the night ended during the walk to the second relic")
			if absf(_player.position.x - _last_x) < 1.0 and _player.is_on_floor():
				_stuck_for += delta
			else:
				_stuck_for = 0.0
			_last_x = _player.position.x
			if _stuck_for > 1.3:
				_release_all()
				_note("blocked_in_memory", {"x": snappedf(_player.position.x, 1.0), "obstacle_x": 2200.0})
				_stuck_for = 0.0
				_go("flip2")
			elif _phase_t > 25.0:
				_fail("never reached his furniture")

		"flip2":
			if not _scene.is_inverted:
				if _press_cooldown <= 0.0:
					_tap("flip_world")
					_press_cooldown = 1.2
			else:
				_note("past_the_shelf", {"x": snappedf(_player.position.x, 1.0)})
				_go("walk2")
			if _phase_t > 8.0:
				_fail("world never inverted at the second relic")

		"walk2":
			# On the ceiling now, in the room as it really is. The shelf below is
			# not solid here, so the way is open.
			if not _held.has("move_right"):
				_press("move_right")
			if _player.position.x >= RELIC2_X - 40.0:
				_release_all()
				_note("reached_relic2_x", {"x": snappedf(_player.position.x, 1.0)})
				_go("reach2")
			elif _phase_t > 25.0:
				_fail("never crossed to the second relic in the truth")

		"reach2":
			var dx2: float = RELIC2_X - _player.position.x
			if absf(dx2) > 30.0:
				var want2 := "move_right" if dx2 > 0.0 else "move_left"
				var other2 := "move_left" if dx2 > 0.0 else "move_right"
				_release(other2)
				if not _held.has(want2):
					_press(want2)
			else:
				_release("move_left")
				_release("move_right")
			if _jump_cooldown <= 0.0:
				_jump()
				_jump_cooldown = 0.9
			if _press_cooldown <= 0.0:
				_reach_out()
				_press_cooldown = 0.22
			if _meters.recognition >= 2:
				_release_all()
				_note("second_contact", {"recognition": _meters.recognition, "days_left": _meters.days_left})
				_go("watch2")
			if _phase_t > 25.0:
				_fail("second contact never landed")

		"watch2":
			if _phase_t > 3.0:
				_go("flip_back2")

		"flip_back2":
			if _scene.is_inverted:
				if _press_cooldown <= 0.0:
					_tap("flip_world")
					_press_cooldown = 1.2
			else:
				_days_before_fall = _meters.days_left
				_go("the_fall")
			if _phase_t > 8.0:
				_fail("world never returned upright after the second relic")

		"the_fall":
			# Walk into the next gap on purpose, without jumping. This is the
			# only way to show the cost the floor carries: a night is spent and
			# the fall sound fires. It is a real consequence, not a staged one.
			if not _held.has("move_right"):
				_press("move_right")
			if _meters.days_left < _days_before_fall:
				_release_all()
				_note("fell_on_purpose", {"days_left": _meters.days_left, "y": snappedf(_player.position.y, 1.0)})
				_go("recover")
			if _phase_t > 20.0:
				_fail("never reached the gap to fall into")

		"recover":
			# The catcher sets him down short of the same hole, so walking right
			# again would simply fall in again. Walk away from it instead: the
			# point of this beat is that control came back, not that the gap can
			# be farmed.
			if not _held.has("move_left"):
				_press("move_left")
			if _phase_t > 3.5:
				_release_all()
				_go("done")

		"done":
			_release_all()
			if _rec_at_contact < 1:
				_fail("run ended without a recognised contact")
				return true
			_note("PASS", {
				"recognition": _meters.recognition,
				"days_left": _meters.days_left,
				"duration_s": snappedf(_t, 0.01),
				"ticks": _tick,
			})
			if _log:
				_log.close()
			quit(0)
			return true
	return false

func _finalize() -> void:
	if _log:
		_log.close()
