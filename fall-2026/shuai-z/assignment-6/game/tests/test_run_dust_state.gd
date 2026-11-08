extends Node
## Headless state checks for Effect B, the running dust trail (CHANGE-BRIEF.md,
## section 3, rules B1–B5). Run from this folder:
##   scripts/run-test.sh test_run_dust_state.tscn 60
## It plays Main through the real game loop: every run, stop, turn, jump, hit
## and pause comes from an input action, and it never calls the driver. Besides
## Main.title_shown, set before load so the title shows, the main sequence
## writes no game state: the only nodes it writes are RunDust's and DustTrail's
## visibility, for rule B4, which are presentation nodes. D14 alone writes
## Rudy's place once, as checks.gd's _teleport does, to put him by a cliff.
## A recorder reads, each physics tick, the brief's condition from Rudy and
## RunDust's state. This node runs before Main's nodes in each tick, so what it
## reads is the state at the end of the tick before, with the condition and
## emitting read at the same moment: a driver a tick late would show as a
## mismatch at every edge. A visibility write is made by the recorder right
## after it reads, so no sample falls between that write and the driver's tick.
## Headless, the dummy renderer draws nothing and runs no particle process, so
## these checks read node state only (CLAUDE.md, Headless facts).
## Prints one line per check and exits with code 1 if any check fails.

const MAIN := preload("res://app/main.tscn")
const OFFSET := Vector2(0, -4) ## the emitter's place relative to Rudy's soles (B2)


## One physics tick as the recorder saw it.
class Sample:
	var tick := 0
	var cond := false ## the brief's condition: in play, on the floor, |velocity.x| > 1
	var emitting := false
	var shown := false ## RunDust.is_visible_in_tree()
	var dust_pos: Vector2
	var rudy_pos: Vector2
	var vx := 0.0
	var on_floor := false
	var mode := 0
	var facing := 0
	var amount := 0
	var ratio := 0.0


var _failures := 0
var _main: Main
var _rudy: Rudy
var _dust_trail: Node2D
var _run_dust: GPUParticles2D
var _tick := 0
var _samples: Array[Sample] = []
var _pending := Callable() ## a write the recorder makes right after it reads


func _ready() -> void:
	await _run()
	print("all checks passed" if _failures == 0 else "%d check(s) FAILED" % _failures)
	get_tree().quit(1 if _failures > 0 else 0)


func _physics_process(_delta: float) -> void:
	if not is_instance_valid(_rudy):
		return
	_tick += 1
	var s := Sample.new()
	s.tick = _tick
	s.vx = _rudy.velocity.x
	s.on_floor = _rudy.is_on_floor()
	s.mode = _rudy.mode
	s.facing = _rudy.facing
	s.cond = s.mode == Rudy.Mode.PLAY and s.on_floor and absf(s.vx) > 1.0
	s.emitting = _run_dust.emitting
	s.shown = _run_dust.is_visible_in_tree()
	s.dust_pos = _run_dust.global_position
	s.rudy_pos = _rudy.global_position
	s.amount = _run_dust.amount
	s.ratio = _run_dust.amount_ratio
	_samples.append(s)
	if _pending.is_valid():
		var write := _pending
		_pending = Callable()
		write.call()


func _run() -> void:
	# D1: on load, with the title showing.
	Main.title_shown = false
	_main = MAIN.instantiate()
	add_child(_main)
	_rudy = _main.get_node("Rudy")
	_dust_trail = _main.get_node("DustTrail")
	_run_dust = _dust_trail.get_node("RunDust")
	Input.action_press(&"move_right")
	await _wait_until(func() -> bool: return _samples.size() >= 30, 40)
	Input.action_release(&"move_right")
	var window := _samples.slice(0)
	_check("D1 on load and on the title, move_right held 30 ticks: emitting false every tick",
		window.size() >= 30 and _count(window, "emitting") == 0 and _main.state == Main.State.TITLE
		and _rudy.mode == Rudy.Mode.WAITING,
		"%d ticks, %d emitting, state %s, mode %s"
		% [window.size(), _count(window, "emitting"), Main.State.keys()[_main.state], Rudy.Mode.keys()[_rudy.mode]])

	# D2: play starts; he stands.
	await _tap(&"restart")
	var i := _samples.size()
	await _frames(30)
	window = _samples.slice(i)
	_check("D2 play started, standing 30 ticks: condition and emitting false every tick",
		window.size() >= 30 and _count(window, "cond") == 0 and _count(window, "emitting") == 0
		and _main.state == Main.State.PLAYING,
		"%d ticks, condition %d, emitting %d, state %s"
		% [window.size(), _count(window, "cond"), _count(window, "emitting"), Main.State.keys()[_main.state]])

	# D3: he starts running right.
	i = _samples.size()
	Input.action_press(&"move_right")
	await _wait_until(func() -> bool: return _rudy.velocity.x >= _rudy.run_speed, 30)
	await _frames(5)
	var cond_up := _edges(i, "cond", true)
	var emit_up := _edges(i, "emitting", true)
	_check("D3 move_right held: one rising edge of the condition and one of emitting, on the same tick",
		cond_up.size() == 1 and cond_up == emit_up,
		"condition rose on %s, emitting on %s" % [cond_up, emit_up])

	# D7: still running right, he jumps and lands.
	i = _samples.size()
	await _tap(&"jump")
	await _wait_until(func() -> bool: return _rudy.is_on_floor(), 90)
	await _frames(5)
	var take_off := _first(i, func(s: Sample) -> bool: return not s.on_floor)
	var landing := _first(take_off + 1, func(s: Sample) -> bool: return s.on_floor) if take_off >= 0 else -1
	if take_off > 0 and landing > 0:
		var air := _samples.slice(take_off, landing)
		var before := _samples[take_off - 1]
		_check("D7 a jump while running: both false from take-off through the air, both true again on the landing tick",
			before.cond and before.emitting and _count(air, "cond") == 0 and _count(air, "emitting") == 0
			and air.size() >= 30 and _samples[landing].cond and _samples[landing].emitting
			and _edges(i, "emitting", false) == [_samples[take_off].tick]
			and _edges(i, "emitting", true) == [_samples[landing].tick]
			and _edges(i, "cond", true) == _edges(i, "emitting", true),
			"take-off tick %d, landing tick %d: %d air ticks, emitting in the air %d; emitting fell on %s, rose on %s; condition rose on %s"
			% [_samples[take_off].tick, _samples[landing].tick, air.size(), _count(air, "emitting"),
			_edges(i, "emitting", false), _edges(i, "emitting", true), _edges(i, "cond", true)])
	else:
		_check("D7 a jump while running: both false from take-off through the air, both true again on the landing tick",
			false, "take-off index %d, landing index %d" % [take_off, landing])

	# D5: he lets go and slows to a stop.
	i = _samples.size()
	Input.action_release(&"move_right")
	await _wait_until(func() -> bool: return _rudy.velocity.x == 0.0, 30)
	await _frames(5)
	var cond_down := _edges(i, "cond", false)
	var emit_down := _edges(i, "emitting", false)
	var at := _index_of_tick(cond_down[0]) if cond_down.size() == 1 else -1
	_check("D5 move_right released: emitting falls on the tick the condition falls, once speed is <= 1 px/s",
		cond_down.size() == 1 and cond_down == emit_down and at > 0
		and absf(_samples[at].vx) <= 1.0 and absf(_samples[at - 1].vx) > 1.0,
		"condition fell on %s, emitting on %s; speed then %.2f, the tick before %.2f"
		% [cond_down, emit_down, absf(_samples[at].vx) if at > 0 else -1.0,
		absf(_samples[at - 1].vx) if at > 0 else -1.0])

	# D6: running right, he turns left.
	Input.action_press(&"move_right")
	await _wait_until(func() -> bool: return _rudy.velocity.x >= _rudy.run_speed, 30)
	await _frames(3)
	i = _samples.size()
	Input.action_release(&"move_right")
	Input.action_press(&"move_left")
	await _wait_until(func() -> bool: return _rudy.velocity.x <= -_rudy.run_speed, 40)
	await _frames(3)
	var turn := _first(i, func(s: Sample) -> bool: return s.facing == -1)
	cond_up = _edges(i, "cond", true)
	emit_up = _edges(i, "emitting", true)
	if turn > 0:
		var gap: int = (cond_up[0] - _samples[turn].tick) if cond_up.size() == 1 else -1
		_check("D6 a turn while running: both false on the turn tick and through the hold, both true again on the same tick once he moves left",
			_samples[turn - 1].cond and _samples[turn - 1].emitting and not _samples[turn].cond
			and not _samples[turn].emitting and absf(_samples[turn].vx) <= 1.0
			and _edges(i, "cond", false) == [_samples[turn].tick] and _edges(i, "emitting", false) == [_samples[turn].tick]
			and cond_up.size() == 1 and cond_up == emit_up and gap >= 5,
			"turn tick %d, speed then %.2f; condition fell on %s, rose on %s; emitting fell on %s, rose on %s; %d ticks still"
			% [_samples[turn].tick, absf(_samples[turn].vx), _edges(i, "cond", false), cond_up,
			_edges(i, "emitting", false), emit_up, gap])
	else:
		_check("D6 a turn while running: both false on the turn tick and through the hold, both true again on the same tick once he moves left",
			false, "no turn recorded")

	# D8: still running left, the tree pauses and resumes.
	await _tap(&"pause")
	var paused := _main.is_paused()
	var emitting_paused := _run_dust.emitting
	var processing_paused := _run_dust.can_process()
	var pos_paused := _run_dust.global_position
	var n := _samples.size()
	await _frames(30)
	var emitting_later := _run_dust.emitting
	var pos_later := _run_dust.global_position
	var recorded := _samples.size() - n
	await _tap(&"pause")
	var resumed := not _main.is_paused()
	_check("D8 paused while running for 30 ticks: emitting stays true, the node does not process, the emitter does not move; on resume it processes and emits",
		paused and emitting_paused and emitting_later and not processing_paused and pos_paused == pos_later
		and recorded == 0 and resumed and _run_dust.can_process() and _run_dust.emitting,
		"paused %s; emitting %s then %s; processing %s; at %s then %s; ticks recorded while paused %d; resumed %s, processing %s, emitting %s"
		% [paused, emitting_paused, emitting_later, processing_paused, pos_paused, pos_later, recorded,
		resumed, _run_dust.can_process(), _run_dust.emitting])

	# D9: still running left, RunDust is hidden and shown.
	await _hide_and_show(_run_dust,
		"D9 RunDust hidden while running: emitting false on the next tick; shown again: emitting true on the next tick")

	# D10: the same with its parent, DustTrail.
	await _hide_and_show(_dust_trail,
		"D10 DustTrail (its parent) hidden while running: not visible in the tree, emitting false; shown again: emitting true")
	Input.action_release(&"move_left")
	await _wait_until(func() -> bool: return _rudy.velocity.x == 0.0, 30)
	await _frames(2) # so the recorder has seen the stop before D13's window opens

	# D13: he runs right into SpikesA and is knocked back.
	i = _samples.size()
	Input.action_press(&"move_right")
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.HURT, 240)
	Input.action_release(&"move_right")
	await _frames(2)
	var hit := _first(i, func(s: Sample) -> bool: return s.mode == Rudy.Mode.HURT)
	if hit > 0:
		_check("D13 a hit on SpikesA while running: condition and emitting fall together on the hit tick",
			_samples[hit - 1].cond and _samples[hit - 1].emitting and not _samples[hit].cond
			and not _samples[hit].emitting and _samples[hit].vx < 0.0
			and _edges(i, "emitting", false) == [_samples[hit].tick] and _edges(i, "cond", false) == [_samples[hit].tick],
			"hit tick %d, knocked back at %.0f px/s; condition fell on %s, emitting on %s"
			% [_samples[hit].tick, _samples[hit].vx, _edges(i, "cond", false), _edges(i, "emitting", false)])
	else:
		_check("D13 a hit on SpikesA while running: condition and emitting fall together on the hit tick",
			false, "no hit recorded; at x %.0f" % _rudy.global_position.x)
	await _wait_until(func() -> bool:
		return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor() and _rudy.velocity.x == 0.0, 120)

	# D14: he runs off the cliff at the end of Segment 1, falls out and respawns.
	var ground_y := (_main.get_node("Level1/StartPoint") as Marker2D).global_position.y
	_rudy.global_position = Vector2(4200.0, ground_y)
	_rudy.velocity = Vector2.ZERO
	await _frames(2)
	i = _samples.size()
	Input.action_press(&"move_right")
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.FALLEN, 120)
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.RESPAWNING, 180)
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY, 180)
	await _wait_until(_condition, 30)
	await _frames(3)
	Input.action_release(&"move_right")
	var leave := _first(i, func(s: Sample) -> bool: return not s.on_floor)
	var back := _first(leave + 1, func(s: Sample) -> bool: return s.cond) if leave >= 0 else -1
	if leave > 0 and back > 0:
		var out := _samples.slice(leave, back)
		var jumps: Array[int] = []
		for j in range(leave, back + 1):
			if _samples[j].dust_pos.distance_to(_samples[j - 1].dust_pos) > 200.0:
				jumps.append(j)
		var jump_quiet := jumps.size() == 1 and not _samples[jumps[0]].emitting and not _samples[jumps[0] - 1].emitting
		var modes := {}
		for s in out:
			modes[Rudy.Mode.keys()[s.mode]] = true
		_check("D14 off a cliff, out and respawned, holding move_right: emitting false from leaving the floor until control returns, the emitter's jump to the checkpoint on a tick without emitting, emitting true when he runs again",
			_samples[leave - 1].cond and _samples[leave - 1].emitting and _count(out, "emitting") == 0
			and modes.has("FALLEN") and modes.has("RESPAWNING") and jump_quiet
			and _samples[back].emitting and _edges(leave, "emitting", true) == [_samples[back].tick],
			"left the floor on tick %d, ran again on tick %d: %d ticks out, emitting %d; modes %s; emitter jumps on ticks %s, emitting then %s; emitting rose on %s"
			% [_samples[leave].tick, _samples[back].tick, out.size(), _count(out, "emitting"), modes.keys(),
			jumps.map(func(j: int) -> int: return _samples[j].tick),
			jumps.map(func(j: int) -> bool: return _samples[j].emitting or _samples[j - 1].emitting),
			_edges(leave, "emitting", true)])
	else:
		_check("D14 off a cliff, out and respawned: emitting false from leaving the floor until control returns",
			false, "left the floor at index %d, ran again at index %d; mode %s"
			% [leave, back, Rudy.Mode.keys()[_rudy.mode]])
	await _frames(10)

	# D4: on every tick the condition holds, the emitter is at his soles + (0, -4).
	var running := 0
	var worst := 0.0
	for s in _samples:
		if s.cond:
			running += 1
			worst = maxf(worst, s.dust_pos.distance_to(s.rudy_pos + OFFSET))
	_check("D4 on every tick the condition holds, the emitter is at Rudy + (0, -4) within 1 px",
		running > 0 and worst <= 1.0, "%d ticks, largest error %.3f px" % [running, worst])

	# D11: the whole run.
	var mismatches := 0
	var wrong_amount := 0
	var speeds := {}
	for s in _samples:
		if s.emitting != (s.cond and s.shown):
			mismatches += 1
		if s.amount != 40 or s.ratio != 1.0:
			wrong_amount += 1
		speeds[snappedf(absf(s.vx), 0.01)] = true
	_check("D11 on every recorded tick, emitting == (condition and visible in the tree); amount 40 and amount_ratio 1.0 throughout",
		mismatches == 0 and wrong_amount == 0 and speeds.size() >= 2,
		"%d ticks, %d mismatches, %d with another amount or ratio, %d distinct speeds"
		% [_samples.size(), mismatches, wrong_amount, speeds.size()])

	# D12: where the emitter lives.
	var look: Node = _rudy.get_node("Look")
	_check("D12 RunDust's parent is DustTrail, DustTrail comes before Rudy in Main, and neither Rudy nor Look is its ancestor",
		_run_dust.get_parent() == _dust_trail and _dust_trail.get_parent() == _main
		and _dust_trail.get_index() < _rudy.get_index()
		and not _rudy.is_ancestor_of(_run_dust) and not look.is_ancestor_of(_run_dust),
		"parent %s, DustTrail index %d, Rudy index %d" % [_run_dust.get_parent().name, _dust_trail.get_index(), _rudy.get_index()])


## While he runs: hides `node`, checks, shows it again, checks (rule B4).
func _hide_and_show(node: CanvasItem, what: String) -> void:
	var held := _condition()
	_pending = func() -> void: node.visible = false
	await _frames(1)
	var hidden_ok := _condition() and not _run_dust.is_visible_in_tree() and not _run_dust.emitting
	var detail := "hidden: condition %s, visible in tree %s, emitting %s" % [
		_condition(), _run_dust.is_visible_in_tree(), _run_dust.emitting]
	await _frames(5)
	var stayed_off := not _run_dust.emitting
	_pending = func() -> void: node.visible = true
	await _frames(1)
	var shown_ok := _condition() and _run_dust.is_visible_in_tree() and _run_dust.emitting
	detail += "; 5 ticks later emitting %s; shown: condition %s, visible in tree %s, emitting %s" % [
		not stayed_off, _condition(), _run_dust.is_visible_in_tree(), _run_dust.emitting]
	_check(what, held and hidden_ok and stayed_off and shown_ok, detail)


## The brief's condition, read from Rudy now.
func _condition() -> bool:
	return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor() and absf(_rudy.velocity.x) > 1.0


func _count(samples: Array[Sample], key: String) -> int:
	var count := 0
	for s in samples:
		if s.get(key):
			count += 1
	return count


## The ticks, from sample index `from` on, on which `key` rose (or fell).
func _edges(from: int, key: String, rising: bool) -> Array[int]:
	var ticks: Array[int] = []
	for j in range(maxi(from, 1), _samples.size()):
		var was: bool = _samples[j - 1].get(key)
		var now: bool = _samples[j].get(key)
		if now != was and now == rising:
			ticks.append(_samples[j].tick)
	return ticks


## The index of the first sample from `from` on that matches, or -1.
func _first(from: int, matches: Callable) -> int:
	for j in range(from, _samples.size()):
		if matches.call(_samples[j]):
			return j
	return -1


func _index_of_tick(tick: int) -> int:
	for j in _samples.size():
		if _samples[j].tick == tick:
			return j
	return -1


func _check(what: String, ok: bool, detail: String = "") -> void:
	print("%s  %s%s" % ["PASS" if ok else "FAIL", what, "" if detail.is_empty() else "  (%s)" % detail])
	if not ok:
		_failures += 1


func _frames(n: int) -> void:
	for i in n:
		await get_tree().physics_frame


## Waits until `condition` is true, for at most `max_ticks`; returns the ticks waited.
func _wait_until(condition: Callable, max_ticks: int) -> int:
	for t in max_ticks:
		if condition.call():
			return t
		await get_tree().physics_frame
	return max_ticks


func _tap(action: StringName) -> void:
	Input.action_press(action)
	await _frames(2)
	Input.action_release(action)
