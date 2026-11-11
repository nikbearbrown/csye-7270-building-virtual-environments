# ============================================================
# Class declaration: class name, what it extends, what the whole script does
# ============================================================
extends SceneTree  # Extends SceneTree: run directly with --script, no scene needed; it loads base.tscn itself
## A6 headless event test for Effect A (landing dust): loads the real base.tscn (real player, real PlayerController, the LandingDust instance
## with its trigger script), presses the real jump and move keys through Input, and records what the effect does. It never calls the trigger itself.
## The seven assertions follow CHANGE-BRIEF "Effect A: Observable rules":
##   1 nothing on scene load; 2 the first landing fires at the feet; 3 nothing on take-off or in the air;
##   4 the second landing is inside the first burst's lifetime; 5 it fires again at the new feet, both emitters;
##   6 restart, not emitting = true: the first Dust burst is cleared and both emitters finish one lifetime after the second landing;
##   7 nothing afterwards while standing.
## Run: ./scripts/run-test.sh test_landing_dust_events.gd 60 (the frame counts below assume 60 rendered frames = 60 physics ticks per second)
## How we see the emitters headless (probed on 4.7.2, dummy renderer): emitting reads true right after restart() but false from the next frame on,
## so we read it only inside the landed handler, right after the trigger. The finished signal does keep real time: it fires one lifetime after a
## restart(), a restart() during a live burst clears it (no finished for the old burst), and emitting = true during a live Dust burst does not move it.
## What it can prove: the input -> brain -> body -> landed -> trigger chain, when each burst starts and ends, and where the effect stands.
## What it cannot prove: what the GPU draws (headless draws no particles): that the old specks vanish on screen, the look, the height and the fade.

# ============================================================
# Constants: the scene, the brief's numbers, and the key presses
# ============================================================
const BASE_SCENE := "res://base.tscn"  # The real main scene, the same one the game runs
const FPS := 60  # Frames per second this test is run at (run-test.sh ... 60)
const DUST_LIFETIME_FRAMES := 96  # Dust lifetime 1.6 s at 60 fps
const RING_LIFETIME_FRAMES := 27  # GroundRing lifetime 0.45 s at 60 fps
const END_TOLERANCE_FRAMES := 2  # How many frames early or late a burst may finish and still count as "on time"
const FLOOR_TOP := 0.25  # The floor surface is at world y = 0.25 (base.tscn room/floor)
const POSITION_EPS := 0.001  # How close two positions must be to count as the same point, metres
const FLOOR_EPS := 0.02  # How close the effect must sit to the floor top, metres
const MIN_JUMP_HEIGHT := 0.5  # A real 4.5 m/s jump rises about 1.03 m; above 0.5 m we know the body really left the floor
const MIN_RETRIGGER_DISTANCE := 0.3  # The second landing must be this far from the first, so the two points can be told apart
const IDLE_FRAMES := 60  # Frames we wait after scene load before touching any key
const JUMP_HOLD_FRAMES := 3  # Frames we hold Space; the brain only jumps on the frame it was just pressed
const GAP_FRAMES := 10  # Frames we stand after the first landing before the second jump
const MOVE_HOLD_FRAMES := 9  # Frames we hold D for the second jump (0.15 s), so it lands a little to the side
const LANDING_TIMEOUT_FRAMES := 180  # If no landing comes within 3 s, the chain is broken and we stop waiting
const STAND_FRAMES := 120  # Frames we stand still at the end (2 s) to check that nothing fires by itself

var _failures := 0  # How many checks have failed; turned into the exit code at the end
var _passes := 0  # How many checks have passed; printed in the summary
var _player: Humanoid  # The real player body from base.tscn
var _effect: Node3D  # The LandingDust instance in base.tscn
var _dust: GPUParticles3D  # Its dust emitter
var _ring: GPUParticles3D  # Its ground-ring emitter
var _sampler: Sampler  # Records one line per frame, after every other script has run
var _landings: Array[Dictionary] = []  # One entry per landed signal: physics frame, feet, and the effect as the trigger left it
var _dust_finished: Array[int] = []  # The physics frames on which Dust's burst finished
var _ring_finished: Array[int] = []  # The physics frames on which GroundRing's burst finished


# ============================================================
# Inner classes: the small node the test uses
# ============================================================
## Sampler node: its process_priority is high, so every frame it runs after the player brain and the trigger, and reads that frame's final values.
class Sampler extends Node:
	var player: Humanoid
	var effect: Node3D
	var samples: Array[Dictionary] = []  # One record per rendered frame

	## Called by Godot once per rendered frame. We write down this frame's physics frame number, the effect's place and the feet height.
	func _process(_delta: float) -> void:
		samples.append({
			"pf": Engine.get_physics_frames(),  # Which physics frame we are at, so records can be matched to the landings
			"effect_pos": effect.global_position,  # Where the effect stands
			"player_y": player.global_position.y,  # How high the feet are, to see the jump really happen
		})


# ============================================================
# Engine callbacks: functions Godot calls automatically at set times (the entry points)
# ============================================================
## Called by Godot once when the script starts as the SceneTree. Starts the whole test.
func _initialize() -> void:
	_run()


# ============================================================
# Feature functions: the parts of the test
# ============================================================
## The whole test: build the scene, play the key presses, check the records, print the summary and quit.
func _run() -> void:
	if not await _build_scene():  # If the scene is not wired as expected, there is nothing to drive
		_finish()
		return
	await _wait_frames(IDLE_FRAMES)  # First we stand still after load, touching nothing
	_check_scene_load()  # Assertion 1
	var load_landings := _landings.size()  # Landings heard during load (should be 0); the jumps' landings are counted after these
	var jump1_start := _sampler.samples.size()  # The first record of the first jump
	await _jump(0)  # Then we jump straight up with the real Space key
	if not await _wait_for_landings(load_landings + 1):  # If the body never lands, the rest cannot run
		_finish()
		return
	_check_first_landing(_landings[load_landings], jump1_start)  # Assertions 2 and 3
	await _wait_frames(GAP_FRAMES)  # We stand a moment, still inside the first dust's life
	await _jump(MOVE_HOLD_FRAMES)  # Then we jump again while holding D for a short while, so we land a little to the right
	if not await _wait_for_landings(load_landings + 2):  # If the second landing never comes, the retrigger cannot be checked
		_finish()
		return
	await _wait_frames(DUST_LIFETIME_FRAMES + 30)  # We let the second burst play out fully, plus half a second
	_check_retrigger(_landings[load_landings], _landings[load_landings + 1], load_landings)  # Assertions 4, 5 and 6
	var landings_before_stand := _landings.size()  # Landings so far; standing still must not add any
	var finishes_before_stand := _dust_finished.size() + _ring_finished.size()  # Bursts finished so far; standing still must not add any
	var stand_start := _sampler.samples.size()  # The first record of the final standing
	await _wait_frames(STAND_FRAMES)  # Finally we stand still for 2 s
	_check_standing(landings_before_stand, finishes_before_stand, stand_start)  # Assertion 7
	_check_never_otherwise()  # And across the whole run: the effect only moved on landing frames
	_finish()


## Called by _run() first. Loads base.tscn into the tree, finds the player and the effect, then (after one frame, once every _ready() has run)
## listens to landed and to both emitters' finished, and adds the sampler. Returns false if something the test needs is missing.
func _build_scene() -> bool:
	var base: Node = load(BASE_SCENE).instantiate()  # We build the real main scene
	root.add_child(base)  # And put it in the tree, so the player brain, the body and the trigger all run as in the game
	_player = base.get_node_or_null("Player") as Humanoid
	_effect = base.get_node_or_null("LandingDust") as Node3D
	if not _check("base.tscn has Player (Humanoid) and LandingDust (Node3D)", _player != null and _effect != null):
		return false
	_dust = _effect.get_node_or_null("Dust") as GPUParticles3D
	_ring = _effect.get_node_or_null("GroundRing") as GPUParticles3D
	if not _check("LandingDust has Dust and GroundRing", _dust != null and _ring != null):
		return false
	_check("LandingDust.body is wired to Player", _effect.get("body") == _player)  # The trigger script must listen to the real player
	_sampler = Sampler.new()
	_sampler.process_priority = 1000  # Higher numbers run later: it reads the values after all of this frame's code
	_sampler.player = _player
	_sampler.effect = _effect
	root.add_child(_sampler)
	await process_frame  # The nodes' _ready() (and so the trigger's connect) runs on this first frame, not inside _initialize()
	var listeners := _player.landed.get_connections().map(func(c: Dictionary) -> Object: return c["callable"].get_object())
	_check("LandingDust listens to Player.landed", listeners.has(_effect))  # The trigger connected in its _ready()
	_player.landed.connect(_on_player_landed)  # We listen too, only to know when landings happen; the trigger connected first, so it runs first
	_dust.finished.connect(func() -> void: _dust_finished.append(Engine.get_physics_frames()))  # We note each frame a Dust burst finishes
	_ring.finished.connect(func() -> void: _ring_finished.append(Engine.get_physics_frames()))  # And each frame a GroundRing burst finishes
	return true


## Called by the player's landed signal, after the trigger has already handled the same signal.
## We write down the frame, the feet, and the effect exactly as the trigger left it (emitting is only readable right now, see the header).
func _on_player_landed() -> void:
	_landings.append({
		"pf": Engine.get_physics_frames(),
		"feet": _player.global_position,
		"effect_pos": _effect.global_position,
		"dust": _dust.emitting,
		"ring": _ring.emitting,
	})


## Simulates one real key, press or release. It goes through Input and the InputMap, so the player brain reads it as usual.
func _key(physical_keycode: Key, pressed: bool) -> void:
	var event := InputEventKey.new()
	event.physical_keycode = physical_keycode
	event.pressed = pressed
	Input.parse_input_event(event)


## Presses Space for JUMP_HOLD_FRAMES and releases it. If move_frames > 0, we also hold D (move_right) for that many frames.
func _jump(move_frames: int) -> void:
	if move_frames > 0:  # If this jump should move sideways, we press D first
		_key(KEY_D, true)
	_key(KEY_SPACE, true)  # Then we press Space; the brain turns "just pressed" into a jump on the next physics frame
	for i in maxi(JUMP_HOLD_FRAMES, move_frames):  # We hold the keys for as long as the longer of the two needs
		await process_frame
		if i + 1 == JUMP_HOLD_FRAMES:  # When Space has been held long enough, we let it go
			_key(KEY_SPACE, false)
		if move_frames > 0 and i + 1 == move_frames:  # When D has been held long enough, we let it go
			_key(KEY_D, false)


## Waits until count landings have been heard in total, or LANDING_TIMEOUT_FRAMES have passed. Returns whether they came.
func _wait_for_landings(count: int) -> bool:
	for i in LANDING_TIMEOUT_FRAMES:
		if _landings.size() >= count:
			break
		await process_frame
	await process_frame  # One more frame, so the sampler has recorded the landing frame itself
	return _check("landing %d arrives within %d frames" % [count, LANDING_TIMEOUT_FRAMES], _landings.size() >= count)


## Waits for a number of rendered frames.
func _wait_frames(frames: int) -> void:
	for i in frames:
		await process_frame


## Assertion 1 (brief: "never otherwise, including on scene load"): during the idle frames after load, no landing, no burst, the effect not moved.
func _check_scene_load() -> void:
	var load_frames: Array[int] = []  # The frames of any landing heard during load, printed if there are any
	for l in _landings:
		load_frames.append(l["pf"])
	_check("1 scene load: no landed signal in the first %d frames (got %d, at physics frames %s)" % [IDLE_FRAMES, _landings.size(), load_frames], _landings.is_empty())
	_check("1 scene load: no Dust or GroundRing burst finished during load (dust %s, ring %s)" % [_dust_finished, _ring_finished],
		_dust_finished.is_empty() and _ring_finished.is_empty())
	var first_pos: Vector3 = _sampler.samples[0]["effect_pos"]  # Where the effect stood on the first frame
	var last_pos: Vector3 = _sampler.samples[-1]["effect_pos"]  # And where it stands now
	_check("1 scene load: the effect did not move during load (%s -> %s)" % [first_pos, last_pos], first_pos.is_equal_approx(last_pos))


## Assertions 2 and 3, after the first jump's landing.
## 2 (brief: "fires on every landing ... at the landing point"): both emitters started by the trigger; the effect at the feet, on the floor.
## 3 (brief: "never otherwise"): from the jump key to the landing frame the effect did not move and no burst finished; and the body really was in the air.
func _check_first_landing(first: Dictionary, jump_start: int) -> void:
	_check("2 first landing: Dust and GroundRing started by the trigger on the landing frame (dust %s, ring %s)" % [first["dust"], first["ring"]], first["dust"] and first["ring"])
	_check("2 first landing: effect at the feet (effect %s, feet %s)" % [first["effect_pos"], first["feet"]],
		(first["effect_pos"] as Vector3).distance_to(first["feet"]) < POSITION_EPS)
	_check("2 first landing: effect on the floor top y = %s (got %.4f)" % [FLOOR_TOP, first["effect_pos"].y], absf(first["effect_pos"].y - FLOOR_TOP) < FLOOR_EPS)
	var start_pos: Vector3 = _sampler.samples[jump_start]["effect_pos"]  # Where the effect stood when we pressed Space
	var start_pf: int = _sampler.samples[jump_start]["pf"]  # The physics frame we pressed Space on
	var highest := -INF  # The highest the feet went during the jump
	var still := true  # Whether the effect stayed in place from the key press until the landing
	for i in range(jump_start, _sampler.samples.size()):
		var s: Dictionary = _sampler.samples[i]
		if s["pf"] >= first["pf"]:  # From the landing frame on, the effect may move, so we stop looking
			break
		highest = maxf(highest, s["player_y"])
		still = still and (s["effect_pos"] as Vector3).is_equal_approx(start_pos)
	var flight_finishes := 0  # Bursts that finished during the flight; any would mean a burst was started without a landing
	for pf in _dust_finished + _ring_finished:
		if pf > start_pf and pf < first["pf"]:
			flight_finishes += 1
	_check("3 take-off and flight: the feet rose above %.2f m (highest %.3f), so this was a real jump" % [FLOOR_TOP + MIN_JUMP_HEIGHT, highest], highest > FLOOR_TOP + MIN_JUMP_HEIGHT)
	_check("3 take-off and flight: the effect did not move before the landing frame", still)
	_check("3 take-off and flight: no burst finished during the flight (got %d)" % flight_finishes, flight_finishes == 0)


## Assertions 4, 5 and 6, after the second burst has played out.
## 4: the second landing is inside the first Dust's lifetime, so this is a retrigger.
## 5 (brief: "plays again at the new landing point; both emitters replay"): one more landed; the effect moved to the new feet; both emitters started.
## 6 (brief: "the code must use restart()"): the first Dust burst is cleared (it never finishes), Dust finishes one lifetime after the second landing,
##   and GroundRing finishes one lifetime after each landing. If the trigger only set emitting = true, the live Dust would never finish at the new time.
func _check_retrigger(first: Dictionary, second: Dictionary, load_landings: int) -> void:
	var gap: int = second["pf"] - first["pf"]  # Physics frames between the two landings
	_check("4 retrigger: second landing %d frames (%.3f s) after the first, inside the Dust lifetime of %d frames" % [gap, float(gap) / FPS, DUST_LIFETIME_FRAMES], gap < DUST_LIFETIME_FRAMES)
	_check("5 retrigger: exactly 2 landed signals from the two jumps (got %d)" % (_landings.size() - load_landings), _landings.size() - load_landings == 2)
	var moved := (second["feet"] as Vector3).distance_to(first["feet"])  # How far apart the two landing points are
	_check("5 retrigger: second landing %.3f m from the first (more than %.1f m)" % [moved, MIN_RETRIGGER_DISTANCE], moved > MIN_RETRIGGER_DISTANCE)
	_check("5 retrigger: effect at the new feet (effect %s, feet %s)" % [second["effect_pos"], second["feet"]],
		(second["effect_pos"] as Vector3).distance_to(second["feet"]) < POSITION_EPS)
	_check("5 retrigger: Dust and GroundRing started by the trigger on the second landing frame (dust %s, ring %s)" % [second["dust"], second["ring"]], second["dust"] and second["ring"])
	var dust_after := _finishes_after(_dust_finished, first["pf"])  # Dust finishes since the first landing
	var ring_after := _finishes_after(_ring_finished, first["pf"])  # GroundRing finishes since the first landing
	var want_dust: int = second["pf"] + DUST_LIFETIME_FRAMES  # The one Dust finish restart() should give: one lifetime after the second landing
	var want_ring := [first["pf"] + RING_LIFETIME_FRAMES, second["pf"] + RING_LIFETIME_FRAMES]  # One ring finish per landing
	_check("6 restart: the first Dust burst was cleared: no Dust finish near physics frame %d (Dust finishes %s)" % [first["pf"] + DUST_LIFETIME_FRAMES, dust_after],
		not _has_near(dust_after, first["pf"] + DUST_LIFETIME_FRAMES))
	_check("6 restart: Dust finished exactly once, at physics frame %d +/- %d (Dust finishes %s)" % [want_dust, END_TOLERANCE_FRAMES, dust_after],
		dust_after.size() == 1 and _has_near(dust_after, want_dust))
	_check("6 restart: GroundRing finished once per landing, at %s +/- %d (GroundRing finishes %s)" % [want_ring, END_TOLERANCE_FRAMES, ring_after],
		ring_after.size() == 2 and _has_near(ring_after, want_ring[0]) and _has_near(ring_after, want_ring[1]))


## Assertion 7 (brief: "never otherwise"; one notification per landing): standing still for 2 s after the bursts, no landing, no burst, no movement.
func _check_standing(landings_before: int, finishes_before: int, stand_start: int) -> void:
	var finishes_now := _dust_finished.size() + _ring_finished.size()  # Bursts finished by the end of the standing
	var start_pos: Vector3 = _sampler.samples[stand_start]["effect_pos"]  # Where the effect stood when the standing began
	var end_pos: Vector3 = _sampler.samples[-1]["effect_pos"]  # And where it stands at the end
	_check("7 standing: no landed signal in %d more frames (got %d)" % [STAND_FRAMES, _landings.size() - landings_before], _landings.size() == landings_before)
	_check("7 standing: no burst finished while standing (got %d)" % (finishes_now - finishes_before), finishes_now == finishes_before)
	_check("7 standing: the effect did not move while standing", start_pos.is_equal_approx(end_pos))


## Across the whole run (brief: "fires on every landing and never otherwise"): on every frame the effect moved, that frame must be a landing frame.
func _check_never_otherwise() -> void:
	var landing_frames := {}  # The physics frames of all landings, for a quick lookup
	for l in _landings:
		landing_frames[l["pf"]] = true
	var stray: Array[int] = []  # Frames where the effect moved without a landing
	for i in range(1, _sampler.samples.size()):
		var moved := not (_sampler.samples[i]["effect_pos"] as Vector3).is_equal_approx(_sampler.samples[i - 1]["effect_pos"])
		if moved and not landing_frames.has(_sampler.samples[i]["pf"]):
			stray.append(_sampler.samples[i]["pf"])
	_check("whole run: the effect moved only on landing frames (stray frames %s)" % [stray], stray.is_empty())


## Returns the finish frames in list that come after from_pf.
func _finishes_after(list: Array[int], from_pf: int) -> Array[int]:
	var out: Array[int] = []
	for pf in list:
		if pf > from_pf:
			out.append(pf)
	return out


## Returns whether list holds a frame within END_TOLERANCE_FRAMES of want.
func _has_near(list: Array[int], want: int) -> bool:
	for pf in list:
		if absi(pf - want) <= END_TOLERANCE_FRAMES:
			return true
	return false


## Records one check: prints PASS or FAIL with what was checked, counts it, and returns whether it passed.
func _check(what: String, ok: bool) -> bool:
	print(("  PASS  " if ok else "  FAIL  ") + what)
	if ok:
		_passes += 1
	else:
		_failures += 1
	return ok


## Prints the summary and quits with exit code 0 (all passed) or 1 (any failure).
func _finish() -> void:
	print("== %d passed, %d failed ==" % [_passes, _failures])
	quit(1 if _failures > 0 else 0)
